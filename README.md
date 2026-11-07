<div align="center">

# 🌊 StreamScope Analytics

**Advanced Multi-Object Tracking & Spatial Intelligence Platform**

*Converting raw video into queryable spatial data with AI-powered forensic analysis*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)](./LICENSE)
[![Tests](https://img.shields.io/badge/Tests-313_Passing-2e7d5b?style=flat)]()

[🚀 Quick Start](#-quick-start) • [📺 Demo](#-live-demo) • [📖 Docs](#-documentation) • [🔧 API](#-api-reference) • [💬 Community](#-community)

<img src="docs/demo_hero.gif" width="80%" alt="StreamScope Demo"/>

*Real-time tracking with metric homography and automated event detection*

</div>

---

## 🎯 Overview

**StreamScope Analytics** transforms passive surveillance footage into **actionable spatial intelligence**. Traditional video management systems record pixels—StreamScope understands *what's happening, where, and why*.

### The Problem We Solve

🔴 **Before:** Millions of hours of unindexed video, requiring manual review  
🟢 **After:** Queryable spatial data with automated incident detection and AI-powered investigation

---

## ✨ Key Innovations

### 1. 📐 **Metric Spatial Intelligence**
Not just "object at pixel (x,y)" — StreamScope knows "object at 15.3 meters from camera moving at 2.1 m/s"

**How?** 3×3 planar homography transforms pixel coordinates to real-world measurements

### 2. 🧠 **Deterministic Event Engine**
Automated detection with zero false positives through hysteresis filtering:
- Line crossings with direction
- Zone intrusions with dwell time
- Speed violations with calibrated thresholds
- Emergency stops with deceleration analysis

### 3. 🤖 **AI Forensic Agent**
Claude-powered investigation assistant with tool calling:
```
User: "Show me all trucks that crossed the north gate between 2pm and 4pm"
Agent: → Calls get_line_crossings(line="north_gate", class="truck", time_range=[14:00, 16:00])
       → Returns structured results with video timestamps
```

### 4. 💾 **Time-Series Architecture**
PostgreSQL 16 optimized for trajectory queries:
- Sub-second forensic search across millions of frames
- Spatial indexing for geometric queries
- Event correlation and pattern detection

---

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                    VIDEO INGESTION                             │
│   RTSP Streams • Video Files • Multi-Camera Inputs            │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌───────────────────────────────────────────────────────────────┐
│                 COMPUTER VISION                                │
│  ┌──────────────┐      ┌────────────┐     ┌───────────────┐ │
│  │   YOLOv8     │  →   │ ByteTrack  │  →  │  Homography   │ │
│  │  Detection   │      │  Tracking  │     │  Transform    │ │
│  └──────────────┘      └────────────┘     └───────────────┘ │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌───────────────────────────────────────────────────────────────┐
│              EVENT INTELLIGENCE                                │
│  Spatial Rules • Kinematic Analysis • Pattern Detection       │
│  LINE_CROSSED • ZONE_ENTERED • LOITERING • OVERSPEED          │
└────────────────────┬──────────────────────────────────────────┘
                     │
                     ▼
┌───────────────────────────────────────────────────────────────┐
│                DATA PERSISTENCE                                │
│  PostgreSQL 16 • Time-Series Trajectories • Event Logs        │
└────────────────────┬──────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌──────────────────┐     ┌──────────────────┐
│  REACT DASHBOARD │     │   CLAUDE AGENT   │
│  Live Telemetry  │     │  NL Investigation │
│  SVG Overlays    │     │   Tool Calling    │
└──────────────────┘     └──────────────────┘
```

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/keshav-077/StreamScope-Analytics.git
cd StreamScope-Analytics

# Launch entire stack (PostgreSQL + API + Dashboard)
docker compose up --build

# Access dashboard: http://localhost:5173
# API docs: http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# Backend setup
docker compose up -d db  # PostgreSQL only
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev,agent]"
uvicorn api.app:app --reload --app-dir src --port 8000

# Frontend setup (separate terminal)
cd dashboard
npm install
npm run dev  # Launches on http://localhost:5173
```

---

## 🎬 Live Demo

### Pre-Configured Scenarios

StreamScope includes real surveillance footage scenarios:

**🚦 Traffic Intersection** (`demo-trafficlight`)
- 801 frames / 26.7 seconds
- 130 unique tracks
- 1 verified line crossing event
- 30 vehicle stop events

Run demo processing:
```bash
python scripts/persist_video.py data/demo_trafficlight.mp4 --camera-id demo-trafficlight
```

---

## 🔬 Technical Deep Dive

### Computer Vision Pipeline

#### 1. **YOLOv8 Detection**
```python
# Multi-class detection across 6 urban mobility classes
classes = ['person', 'bicycle', 'car', 'motorcycle', 'bus', 'truck']
detector = YOLODetector(weights='yolov8n.pt', confidence=0.25)
detections = detector.detect(frame)
```

#### 2. **ByteTrack Association**
```python
# Two-stage Kalman filtering for persistent IDs
tracker = ByteTracker()
tracks = tracker.update(detections)
# Maintains IDs through occlusions & crowding
```

#### 3. **Planar Homography**
```python
# Pixel → Real-world coordinate transformation
H = np.array([...])  # 3×3 homography matrix
world_x, world_y = apply_homography(pixel_x, pixel_y, H)
velocity_mps = estimate_velocity(prev_pos, curr_pos, delta_t)
```

### Event Detection Engine

#### Spatial Events

**Zone Intrusion:**
```python
def check_zone_entry(object_pos, zone_polygon):
    # Point-in-polygon test with hysteresis
    inside = cv2.pointPolygonTest(zone_polygon, object_pos, False)
    if inside and frames_inside > CONFIRMATION_THRESHOLD:
        emit_event('ZONE_ENTERED')
```

**Line Crossing:**
```python
def check_line_crossing(prev_pos, curr_pos, line_start, line_end):
    # Vector cross-product intersection test
    crossed = (cross_product(prev_pos, line) * 
               cross_product(curr_pos, line)) < 0
    if crossed:
        emit_event('LINE_CROSSED', direction=get_direction())
```

#### Kinematic Events

**Speed Violation:**
```python
def check_overspeed(velocity, threshold=5.0):  # m/s
    if velocity > threshold:
        emit_event('OVERSPEED', velocity=velocity)
```

**Emergency Braking:**
```python
def check_sudden_stop(acceleration, threshold=-3.0):  # m/s²
    if acceleration <= threshold:
        emit_event('SUDDEN_STOP', deceleration=abs(acceleration))
```

---

## 📊 Performance Metrics

### Inference Benchmarks

**Hardware:** Intel Core i7, 16 threads, FP32

| Backend | Detection FPS | Tracking FPS | End-to-End | Latency (mean) | Latency (p95) |
|---------|---------------|--------------|------------|----------------|---------------|
| PyTorch | **5.58** | 706.2 | **5.49** | 182.0 ms | 229.6 ms |
| ONNX | 1.22 | 165.9 | 1.20 | 831.8 ms | 976.1 ms |

**Real-World Streams:**

| Video | Frames | Objects/Frame | Throughput | Latency |
|-------|--------|---------------|------------|---------|
| Traffic Light | 801 | 16.13 | **14.47 FPS** | 69.0 ms |
| Intersection | 472 | 12.45 | **12.57 FPS** | 79.4 ms |
| Junction | 384 | 8.21 | **14.88 FPS** | 67.0 ms |

**Key Insight:** ByteTrack overhead is negligible (<1.5ms/frame = 0.18% of total pipeline time)

### Tracking Accuracy (CLEAR MOT)

| Metric | Real Video (244 frames) | Synthetic Crossing |
|--------|-------------------------|-------------------|
| MOTA | **1.000** | 1.000 |
| IDF1 | **1.000** | 1.000 |
| ID Switches | **0** | 0 |
| False Positives | **0** | 0 |
| False Negatives | **0** | 0 |

---

## 🎨 Dashboard Features

### 1. **Live Telemetry View**

<table>
<tr><td>

**Features:**
- Real-time video playback
- Synchronized SVG overlays (bounding boxes, trajectories, zones)
- Frame-accurate rendering via `requestAnimationFrame`
- Object ID persistence visualization

</td></tr>
</table>

### 2. **Forensic Event Feed**

<table>
<tr><td>

**Features:**
- Chronological incident timeline
- Severity-based color coding
- **Click-to-seek:** Jump to exact millisecond in video
- Filter by event type, object class, time range

</td></tr>
</table>

### 3. **Object Profile Inspector**

<table>
<tr><td>

**Features:**
- Complete trajectory history
- Dwell time calculation
- Associated event links
- Coordinate path visualization

</td></tr>
</table>

### 4. **AI Investigation Agent**

<table>
<tr><td>

**Natural Language Queries:**
```
"Show me all people who loitered in the north zone for more than 30 seconds"
"List trucks that crossed the entry gate going southbound yesterday"
"What was the average speed of motorcycles on camera-03 between 2pm-4pm?"
```

**Tool Calling:**
Agent has access to 12 specialized tools for querying events, objects, zones, lines, and generating reports.

**Safety:** All write operations require human approval via pending action queue.

</td></tr>
</table>

---

## 🔧 API Reference

### Core Endpoints

#### Cameras
```http
GET    /cameras                    # List all cameras
GET    /cameras/{id}/zones         # Get polygon zones
GET    /cameras/{id}/lines         # Get virtual lines
GET    /cameras/{id}/objects       # List tracked objects
```

#### Objects & Trajectories
```http
GET    /objects/{id}/trajectory    # Full coordinate history
GET    /cameras/{id}/events        # Query spatial events
```

#### Analytics
```http
GET    /analytics?camera_id={id}   # Aggregated statistics
POST   /videos/upload              # Upload video for processing
GET    /videos/{id}/status         # Processing progress
```

#### AI Agent
```http
POST   /agent/query                # Natural language investigation
GET    /agent/actions              # List pending actions
POST   /agent/actions/{id}/approve # Approve write operation
```

### WebSocket Events
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/events');
ws.onmessage = (event) => {
  const incident = JSON.parse(event.data);
  console.log('Live event:', incident);
};
```

---

## 🧪 Testing

### Run Test Suite

```bash
# Backend tests (243 tests)
pytest

# Frontend tests (70 tests)
cd dashboard && npm run test

# Total: 313 automated tests
```

### Test Coverage

- ✅ Unit tests for all event types
- ✅ Integration tests for API endpoints
- ✅ Tracking accuracy evaluation (CLEAR MOT)
- ✅ Homography transformation validation
- ✅ Agent tool calling verification
- ✅ Database schema integrity
- ✅ UI component rendering

---

## 🛠️ Configuration

### Camera Setup

`configs/cameras/my-camera.json`:
```json
{
  "camera_id": "warehouse-north",
  "name": "North Warehouse Camera",
  "homography": [
    [1.2, 0.1, -150],
    [0.0, 1.5, -200],
    [0.0, 0.001, 1.0]
  ],
  "zones": [
    {
      "name": "loading_dock",
      "points": [[100, 200], [400, 200], [400, 500], [100, 500]],
      "dwell_threshold_seconds": 30
    }
  ],
  "lines": [
    {
      "name": "entry_gate",
      "points": [[320, 240], [960, 240]],
      "direction": "southbound"
    }
  ]
}
```

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://trace:trace@localhost:5433/trace

# Camera
TRACE_CAMERA_SOURCE=rtsp://camera-ip/stream
TRACE_CAMERA_ID=warehouse-north
TRACE_DETECTOR_WEIGHTS=yolov8n.pt
TRACE_DETECTOR_CONFIDENCE=0.25

# AI Agent
TRACE_LLM_PROVIDER=anthropic  # or openrouter
ANTHROPIC_API_KEY=sk-...
TRACE_LLM_MODEL=claude-sonnet-4-5

# Frontend
VITE_API_BASE_URL=http://localhost:8000
```

---

## 📚 Documentation

### Homography Calibration Guide

**1. Identify ground-plane reference points:**
```
Known real-world coordinates (meters):
P1: (0, 0)    → Image pixel: (120, 480)
P2: (10, 0)   → Image pixel: (580, 470)
P3: (10, 15)  → Image pixel: (590, 120)
P4: (0, 15)   → Image pixel: (110, 130)
```

**2. Compute homography matrix:**
```python
import cv2
src_points = np.array([[120,480], [580,470], [590,120], [110,130]], dtype=np.float32)
dst_points = np.array([[0,0], [10,0], [10,15], [0,15]], dtype=np.float32)
H, _ = cv2.findHomography(src_points, dst_points)
```

**3. Save to camera config:**
```json
{
  "homography": [
    [1.23, 0.05, -142.3],
    [0.02, 1.89, -215.7],
    [0.0001, 0.0008, 1.0]
  ]
}
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Configure real camera homography matrices
- [ ] Set up PostgreSQL with backup strategy
- [ ] Configure environment variables
- [ ] Enable HTTPS with SSL certificates
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure log aggregation
- [ ] Test failover scenarios
- [ ] Document incident response procedures

### Scaling Considerations

**Horizontal Scaling:**
- Stateless FastAPI workers behind load balancer
- PostgreSQL read replicas for query load
- Redis for caching hot data

**Vertical Scaling:**
- GPU inference for higher throughput
- TensorRT for 3x faster detection
- Increased PostgreSQL connection pool

---

## 🤝 Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License © 2026 Keshav

Full license text: [LICENSE](./LICENSE)

---

## 🙏 Credits

Built with these incredible open-source technologies:

| Technology | Purpose |
|------------|---------|
| [YOLOv8](https://github.com/ultralytics/ultralytics) | Real-time object detection |
| [ByteTrack](https://github.com/ifzhang/ByteTrack) | Multi-object tracking |
| [FastAPI](https://fastapi.tiangolo.com/) | High-performance async API |
| [React 19](https://react.dev/) | Modern UI framework |
| [PostgreSQL 16](https://www.postgresql.org/) | Reliable time-series storage |
| [Anthropic Claude](https://www.anthropic.com/) | AI investigation agent |

---

## 💬 Community

- 💬 **Discussions:** [GitHub Discussions](https://github.com/keshav-077/StreamScope-Analytics/discussions)
- 🐛 **Bug Reports:** [Issue Tracker](https://github.com/keshav-077/StreamScope-Analytics/issues)
- 📧 **Email:** keshav@example.com

---

<div align="center">

**Engineered with 🌊 by Keshav**

*Transforming surveillance into intelligence*

[⬆ Back to Top](#-streamscope-analytics)

</div>
