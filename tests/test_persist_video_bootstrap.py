"""Tests for scripts/persist_video.py's bootstrap idempotency (the fix for
demo-trafficlight getting silently reprocessed on every `docker compose up`/
restart -- see repository.camera_has_persisted_data's docstring for the full
reasoning).

scripts/ isn't part of the installed `trace` package, so it's imported the
same way test_upload_worker.py imports upload_worker: sys.path.insert.

main() builds its own engine/session internally (from --database-url /
DATABASE_URL), separate from the db_session fixture's rolled-back
transaction -- so these tests point it at the real trace_test database and
clean up the camera they create via delete_camera_cascade at the end,
rather than relying on transaction rollback.

process_video is monkeypatched to a fake that just persists one object,
standing in for "the real pipeline ran" -- this suite is about the
skip/proceed decision itself, not about re-running real detection.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import persist_video  # noqa: E402

from database import repository  # noqa: E402
from database.db import get_engine, get_session_factory  # noqa: E402

# Same default tests/conftest.py's own TEST_DATABASE_URL uses -- not imported
# from there directly since tests/ has no __init__.py (not a real package).
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", "postgresql://trace:trace@localhost:5433/trace_test")


@pytest.fixture
def cleanup_camera():
    """Deletes whatever camera_id(s) the test registers, against the same
    real trace_test database main() itself writes to -- these tests bypass
    the db_session fixture's rollback safety net on purpose (main() opens
    its own session), so cleanup has to be explicit."""
    camera_ids: list[str] = []
    yield camera_ids
    engine = get_engine(TEST_DATABASE_URL)
    Session = get_session_factory(engine)
    with Session() as session:
        for camera_id in camera_ids:
            camera = repository.get_camera(session, camera_id)
            if camera is not None:
                repository.delete_camera_cascade(session, camera)
        session.commit()


def _run(monkeypatch, camera_id: str, *, force: bool = False):
    argv = [
        "persist_video.py",
        "some/fake/source.mp4",
        "--camera-id", camera_id,
        "--database-url", TEST_DATABASE_URL,
    ]
    if force:
        argv.append("--force")
    monkeypatch.setattr(sys, "argv", argv)
    persist_video.main()


def test_bootstrap_runs_the_pipeline_for_a_camera_with_no_existing_data(monkeypatch, cleanup_camera):
    camera_id = "cam_bootstrap_fresh"
    cleanup_camera.append(camera_id)
    calls = []

    def fake_process_video(session, camera, source, **kwargs):
        calls.append((camera.camera_id, source))
        repository.get_or_create_object(session, camera, object_id=1, class_name="car", timestamp=0.0)
        session.commit()
        return (10, 1, 0)

    monkeypatch.setattr(persist_video, "process_video", fake_process_video)

    _run(monkeypatch, camera_id)

    assert calls == [(camera_id, "some/fake/source.mp4")]


def test_bootstrap_skips_reprocessing_once_the_camera_already_has_data(monkeypatch, cleanup_camera):
    camera_id = "cam_bootstrap_stable"
    cleanup_camera.append(camera_id)
    calls = []

    def fake_process_video(session, camera, source, **kwargs):
        calls.append(1)
        repository.get_or_create_object(session, camera, object_id=1, class_name="car", timestamp=0.0)
        session.commit()
        return (10, 1, 0)

    monkeypatch.setattr(persist_video, "process_video", fake_process_video)

    _run(monkeypatch, camera_id)
    assert len(calls) == 1  # first run: no data yet, proceeds

    _run(monkeypatch, camera_id)
    assert len(calls) == 1  # second run (e.g. a container restart): already has data, skipped

    _run(monkeypatch, camera_id)
    assert len(calls) == 1  # a third restart -- still stable, not 2 or 3


def test_bootstrap_force_flag_reprocesses_anyway(monkeypatch, cleanup_camera):
    camera_id = "cam_bootstrap_forced"
    cleanup_camera.append(camera_id)
    calls = []

    def fake_process_video(session, camera, source, **kwargs):
        calls.append(1)
        repository.get_or_create_object(session, camera, object_id=1, class_name="car", timestamp=0.0)
        session.commit()
        return (10, 1, 0)

    monkeypatch.setattr(persist_video, "process_video", fake_process_video)

    _run(monkeypatch, camera_id)
    assert len(calls) == 1

    _run(monkeypatch, camera_id, force=True)
    assert len(calls) == 2  # --force bypasses the skip for a deliberate re-seed
