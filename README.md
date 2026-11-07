<div align="center">

# 🌊 StreamScope Analytics

### Advanced Multi-Object Tracking & Spatial Intelligence Platform

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-19.0-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-302_Passed-2e7d5b?style=flat-square)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](./LICENSE)

<p align="center">
  <b>Convert raw video streams into actionable spatial intelligence with AI-powered tracking and forensic analysis</b><br>
  Edge AI (YOLOv8 + ByteTrack) • Geometric Calibration • Intelligent Event Detection • LLM-Powered Investigation
</p>

<br>

<img src="docs/demo_hero.gif" alt="StreamScope Analytics Demo" width="760" />

<p align="center">
  <sub><b>Real-Time Tracking & Spatial Intelligence</b> — YOLOv8 + ByteTrack with metric homography and automated event detection.</sub>
</p>

**Engineered by [Keshav](https://github.com/keshav) • 2026**

</div>

---

## 📋 Table of Contents

1. [Platform Overview](#-platform-overview)
2. [Architecture](#️-system-architecture)
3. [Vision Pipeline](#-computer-vision--tracking-pipeline)
4. [Event Intelligence](#-intelligent-event-engine)
5. [Model Training](#-model-training--adaptation)
6. [Performance Metrics](#-performance-benchmarks)
7. [Analytics Dashboard](#-analytics-dashboard)
8. [AI Investigation Agent](#-ai-investigation-agent)
9. [Technology Stack](#-technology-stack)
10. [Quick Start](#-quick-start)
11. [Development Setup](#️-development-setup)
12. [API Reference](#-api-reference)
13. [Testing](#-testing--validation)
14. [License](#-license)

---

## 🌟 Platform Overview

Surveillance infrastructure generates massive volumes of unstructured video data daily. **StreamScope Analytics** transforms passive video streams into structured, queryable spatial intelligence with automated event detection and AI-powered forensic analysis.

### 🎯 Core Platform Capabilities

| Capability | Implementation | Intelligence Output |
|:-----------|:---------------|:--------------------|
| **Vision & Tracking** | YOLOv8 + ByteTrack Kalman Filter | Persistent multi-class object tracking with stable IDs |
| **Spatial Mapping** | 3×3 Metric Homography Transform | Real-world coordinates (meters) with velocity estimation |
| **Event Intelligence** | Deterministic Spatio-Temporal Engine | Automated detection: crossings, intrusions, dwell, speed |
| **Data & Analytics** | PostgreSQL 16 + FastAPI + React 19 | Sub-second forensic queries with AI investigation assistant |

> **Innovation:** *StreamScope doesn't just track objects — it understands spatial behavior and temporal patterns.*

---

## 🏗️ System Architecture

```mermaid
flowchart LR
    subgraph EDGE["Edge Processing Layer"]
        CAM["Video Stream (RTSP)"] --> YOLO["YOLOv8 Detection"]
        YOLO --> TRACK["ByteTrack Kalman Filter"]
        TRACK --> GEO["Homography Transform"]
        GEO --> EVENT["Event Intelligence Engine"]
    end

    subgraph DATA["Data & API Layer"]
        EVENT -->|Batch Sync| DB[("PostgreSQL 16<br/>Time-Series Storage")]
        DB <--> API["FastAPI REST Gateway"]
    end

    subgraph UI["User Interface Layer"]
        API <--> DASH["React 19<br/>Analytics Dashboard"]
        API <--> AGENT["Claude AI<br/>Investigation Agent"]
    end
```

### 📦 Architectural Layers

1. **Edge Processing** (`src/detection/` & `src/tracking/`)
   - Video stream ingestion and frame extraction
   - YOLOv8 multi-class object detection (6 urban classes)
   - ByteTrack two-stage Kalman filtering for ID persistence

2. **Spatial Intelligence** (`src/geometry/` & `src/events/`)
   - 3×3 homography matrix for ground-plane projection
   - Real-time velocity estimation with smoothing
   - Deterministic event rules with hysteresis filtering

3. **Data Layer** (`src/database/` & `src/api/`)
   - PostgreSQL 16 optimized for time-series trajectories
   - FastAPI with Pydantic v2 schema validation
   - Efficient batch insertion for high-throughput streams

4. **Intelligence Layer** (`dashboard/` & `src/agent/`)
   - React 19 dashboard with live vector overlays
   - Claude AI agent with tool-based investigation
   - Human-in-the-loop safety approvals

---

## 🎥 Computer Vision & Tracking Pipeline

```mermaid
flowchart LR
    A["Input Frame<br/>(1080p)"] --> B["Letterbox<br/>Resize 640²"]
    B --> C["YOLOv8<br/>Multi-Class Detection"]
    C --> D["ByteTrack<br/>Kalman Association"]
    D --> E["Homography<br/>Spatial Transform"]
    E --> F["Event Rules<br/>Evaluation"]
    F --> G[("PostgreSQL<br/>Persistence")]
```

### Pipeline Components

1. **Frame Processing** → Decode and resize to 640×640 with padding
2. **Object Detection** → YOLOv8 inference across 6 classes (person, car, motorcycle, bus, truck, bicycle)
3. **Identity Tracking** → Two-stage Kalman filter maintaining persistent track IDs through occlusions
4. **Spatial Calibration** → Homography-based pixel-to-meter coordinate transformation
5. **Event Detection** → Real-time evaluation of spatial and kinematic trigger rules
6. **Data Persistence** → Asynchronous batch insertion to time-series database

---

## ⚡ Intelligent Event Engine

The Event Engine implements deterministic spatial and kinematic rules with hysteresis-based noise filtering.

### 📊 Supported Event Types

| Event | Detection Logic | Mathematical Condition | State Management |
|:------|:----------------|:------------------------|:-----------------|
| `LINE_CROSSED` | Trajectory vector intersection | Cross-product sign change | Immediate trigger |
| `ZONE_ENTERED` | Footprint enters polygon | Point-in-polygon test | N-frame confirmation |
| `ZONE_EXITED` | Footprint exits polygon | Point-in-polygon test | N-frame confirmation |
| `LOITERING` | Extended dwell time | Accumulated time ≥ threshold | Maintained until exit |
| `OVERSPEED` | Velocity threshold breach | Speed > configured limit | Moving-window filter |
| `STOPPED` | Prolonged stationary state | Velocity ≈ 0 for duration | Reset on movement |
| `SUDDEN_STOP` | Rapid deceleration | Acceleration < emergency threshold | Multi-frame verification |

### 📐 Kinematic Calculations

$$
v = \frac{\|p_t - p_{t-\Delta t}\|}{\Delta t} \qquad\qquad a = \frac{v_t - v_{t-\Delta t}}{\Delta t}
$$

- **Velocity (v)**: Instantaneous ground-plane speed via homography projection
- **Acceleration (a)**: Rate of velocity change for emergency braking detection
- **Dwell Duration**: `T_dwell = t_current - t_entry ≥ T_threshold`
- **Crossing Detection**: Vector intersection via cross-product sign analysis

### ✅ Validation Results

Real-world street intersection footage (26.7s duration, 801 frames):

| Performance Metric | Measured Value | Operational Context |
|:-------------------|:---------------|:--------------------|
| **Detection Density** | 16.13 objects/frame | Multi-class simultaneous detection |
| **Track Persistence** | 130 unique tracks | Continuous ID maintenance |
| **Line Crossings** | 1 verified event | Object #134 crossing at t=9.5s |
| **Stop Events** | 30 detected | Traffic signal queue detection |
| **Track Lifecycle** | 130 entries / 112 exits | Boundary transition logging |

---

## 🎓 Model Training & Adaptation

### Two-Stage Training Architecture

- **Stage 1: Class Specialization**  
  Fine-tuning from COCO128 to isolate 6 urban mobility classes while freezing backbone

- **Stage 2: Domain Adaptation**  
  Optimization for surveillance camera characteristics (angles, lighting, compression)

### 📊 Training Loss Function

$$
\mathcal{L}_{\text{total}} = \lambda_{\text{box}}\mathcal{L}_{\text{box}} + \lambda_{\text{cls}}\mathcal{L}_{\text{cls}} + \lambda_{\text{dfl}}\mathcal{L}_{\text{dfl}}
$$

- **Learning Schedule**: `1e-3` (initial) → `1e-4` (fine-tuning)
- **Data Augmentation**: Mosaic composition, HSV jittering, perspective warping

### 🎯 Target Classification Schema

| Class ID | Label | Monitoring Objective |
|:--------:|:------|:---------------------|
| 0 | person | Pedestrian flow, loitering, unauthorized access |
| 1 | bicycle | Cycle infrastructure usage, compliance |
| 2 | car | Traffic flow, parking enforcement, speed |
| 3 | motorcycle | Lane usage, speed violations |
| 4 | bus | Transit route adherence, schedule tracking |
| 5 | truck | Commercial vehicle routing, weight restrictions |

---

## 📊 Performance Benchmarks

### Inference Runtime Analysis

**Hardware:** Intel Core i7 (16 threads), **Dataset:** 244 frames, **Precision:** FP32

| Execution Backend | Detection FPS | Tracking FPS | End-to-End FPS | Mean Latency | p95 Latency | CPU Usage |
|:------------------|:--------------|:-------------|:---------------|:-------------|:------------|:----------|
| **PyTorch (CPU)** | 5.58 | 706.2 | **5.49** | 182.0 ms | 229.6 ms | 285% |
| **ONNX Runtime** | 1.22 | 165.9 | **1.20** | 831.8 ms | 976.1 ms | 316% |

### Real-World Stream Performance

**Configuration:** YOLOv8n.pt, confidence=0.25, CPU inference

| Video Stream | Total Frames | Detection FPS | End-to-End FPS | Mean Latency | p95 Latency |
|:-------------|:-------------|:--------------|:---------------|:-------------|:------------|
| `demo_trafficlight.mp4` | 801 | 16.27 | **14.47** | 69.0 ms | 82.5 ms |
| `demo_intersection.mp4` | 472 | 15.12 | **12.57** | 79.4 ms | 99.2 ms |
| `demo_junction_trimmed.mp4` | 384 | 16.51 | **14.88** | 67.0 ms | 76.9 ms |

**Key Finding:** ByteTrack tracking overhead is negligible (>300 FPS throughput = <1.5ms per frame)

---

## 🎨 Analytics Dashboard

Built with **React 19**, **Vite**, **TypeScript**, and **Tailwind CSS v4**.

### Dashboard Modules

| Module | Capabilities |
|:-------|:-------------|
| **Live Telemetry View** | Real-time video playback with synchronized SVG overlays (bounding boxes, trajectories, zones) |
| **Forensic Event Feed** | Chronological incident log with severity classification and instant video seeking |
| **Object Inspector** | Deep-dive trajectory analysis with coordinate history and associated events |
| **Analytics Dashboard** | Class distribution charts, violation statistics, multi-camera fleet status |

### Technical Features

- ✅ **SVG Overlay Synchronization**: Frame-accurate projection via `requestAnimationFrame`
- ✅ **Sub-Second Navigation**: Click-to-seek functionality with millisecond precision
- ✅ **Zero Mock Data**: 100% live PostgreSQL/FastAPI integration
- ✅ **Interactive Scenarios**: Pre-configured demo cases with real footage

---

## 🤖 AI Investigation Agent

### Architecture

Pluggable LLM backend via standardized `LLMClient` protocol:

| Provider | Model | Authentication Required |
|:---------|:------|:------------------------|
| `anthropic` (default) | `claude-sonnet-4-5` | `ANTHROPIC_API_KEY` |
| `openrouter` | `openrouter/free` | `OPENROUTER_API_KEY` |

### 🛠️ Agent Tool Inventory

**Read Operations (7 tools):**
- `get_camera_events` - Filtered event queries by camera/type/time
- `get_object_stats` - Complete object lifecycle and event history
- `get_zone_events` - Zone-specific activity logs
- `get_line_crossings` - Crossing event retrieval
- `get_traffic_stats` - Volume metrics and crossing counts
- `get_event` - Single event detail lookup
- `get_video_segment` - Temporal video window extraction

**Write Operations (5 tools - approval required):**
- `create_alert` - Alert configuration proposal
- `configure_zone` - New polygon zone definition
- `configure_line` - Virtual line creation
- `generate_report` - Analytics report generation
- `send_notification` - Notification dispatch proposal

> **Safety Protocol:** All write operations generate pending actions requiring explicit human approval via `POST /agent/actions/{id}/approve`

---

## 💻 Technology Stack

| Layer | Technologies | Purpose |
|:------|:-------------|:--------|
| **Computer Vision** | YOLOv8, ByteTrack, OpenCV | Object detection, tracking, frame processing |
| **Spatial Math** | NumPy, OpenCV | Homography transforms, point-in-polygon tests |
| **Inference** | PyTorch 2.0+, ONNX, TensorRT | Multi-backend model execution |
| **Backend** | Python 3.10+, FastAPI, Pydantic v2 | Async API, schema validation |
| **Database** | PostgreSQL 16, SQLAlchemy 2.0 | Time-series trajectory storage |
| **AI Agent** | Anthropic Claude / OpenRouter | Natural language investigation |
| **Frontend** | React 19, TypeScript, Tailwind CSS v4 | Interactive analytics dashboard |
| **Testing** | Pytest (243), Vitest (70) | Comprehensive test coverage |
| **DevOps** | Docker Compose | Multi-service orchestration |

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone <your-repo-url>
cd streamscope-analytics

# 2. Launch entire stack
docker compose up --build
```

### 🌐 Service Endpoints

| Service | URL | Port | Function |
|:--------|:----|:----:|:---------|
| **Analytics Dashboard** | [localhost:5173](http://localhost:5173) | 5173 | React UI |
| **API Gateway** | [localhost:8000](http://localhost:8000) | 8000 | FastAPI |
| **API Documentation** | [localhost:8000/docs](http://localhost:8000/docs) | 8000 | OpenAPI/Swagger |
| **PostgreSQL** | `localhost:5433` | 5433 | Database (trace/trace) |

---

## 🛠️ Development Setup

### Backend Configuration

```bash
# Start database container
docker compose up -d db

# Create Python environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev,agent]"

# Launch API server
uvicorn api.app:app --reload --app-dir src --port 8000
```

### Frontend Configuration

```bash
cd dashboard
npm install
npm run dev  # Launches on http://localhost:5173
```

### Video Processing

```bash
python scripts/persist_video.py data/demo_trafficlight.mp4 --camera-id demo-trafficlight
```

---

## ⚙️ Environment Configuration

| Variable | Default | Purpose |
|:---------|:--------|:--------|
| `DATABASE_URL` | `postgresql://trace:trace@localhost:5433/trace` | Database connection string |
| `TRACE_CAMERA_SOURCE` | `data/demo_trafficlight.mp4` | Video file or RTSP stream URL |
| `TRACE_CAMERA_ID` | `demo-trafficlight` | Camera configuration identifier |
| `TRACE_DETECTOR_WEIGHTS` | `yolov8n.pt` | YOLOv8 model checkpoint |
| `TRACE_DETECTOR_CONFIDENCE` | `0.25` | Detection confidence threshold |
| `TRACE_LLM_PROVIDER` | `anthropic` | AI agent backend (anthropic/openrouter) |
| `ANTHROPIC_API_KEY` | *(required for anthropic)* | Anthropic API authentication |
| `OPENROUTER_API_KEY` | *(required for openrouter)* | OpenRouter API authentication |
| `VITE_API_BASE_URL` | `http://localhost:8000` | Backend URL for frontend |

---

## 🌐 API Reference

**Interactive Documentation:** http://localhost:8000/docs

### Core Endpoints

| Method | Endpoint | Functionality |
|:------:|:---------|:--------------|
| **GET** | `/cameras` | List registered cameras |
| **GET** | `/cameras/{id}/zones` | Retrieve polygon zones |
| **GET** | `/cameras/{id}/lines` | Retrieve virtual lines |
| **GET** | `/cameras/{id}/objects` | Query tracked objects |
| **GET** | `/objects/{id}/trajectory` | Fetch coordinate path |
| **GET** | `/cameras/{id}/events` | Query spatial events |
| **POST** | `/videos/upload` | Async video ingestion |
| **GET** | `/videos/{id}/status` | Processing progress |
| **POST** | `/alerts` | Create alert configuration |
| **GET** | `/analytics` | Aggregated statistics |
| **POST** | `/agent/query` | AI agent investigation |

---

## 🧪 Testing & Validation

- ✅ **313 Automated Tests**: 243 backend (pytest) + 70 frontend (vitest)
- ✅ **CLEAR MOT Metrics**: Multi-object tracking accuracy evaluation
- ✅ **Detection Metrics**: mAP@50, mAP@50-95 validation
- ✅ **CI/CD Pipeline**: Automated testing on commits

---

## 📁 Repository Structure

```text
StreamScope-Analytics/
├── src/                  # Core Python engine
├── dashboard/            # React 19 frontend (70 tests)
├── configs/              # Camera calibration configs
├── scripts/              # Video processing utilities
├── training/             # YOLOv8 fine-tuning pipeline
├── evaluation/           # CLEAR MOT evaluation suite
├── benchmarks/           # Performance testing tools
├── tests/                # Backend tests (243 tests)
├── docker-compose.yml    # Multi-service orchestration
└── Dockerfile            # Python backend container
```

---

## 📜 License

Licensed under the **MIT License**

Copyright © 2026 **Keshav**

[Full License Text](./LICENSE)

---

## 🙏 Acknowledgments

Built with:
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [PostgreSQL](https://www.postgresql.org/)
- [Anthropic Claude](https://www.anthropic.com/)

---

<div align="center">

**Engineered with 🌊 by Keshav**

⭐ Star this repository to support the project!

[Report Bug](../../issues) • [Feature Request](../../issues) • [Documentation](./docs)

</div>
