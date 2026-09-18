# SmartRoom AI

An AI-powered spatial memory assistant that can scan a room using a camera, detect and track objects, remember their locations over time, and answer natural-language questions.

## Tech Stack

- Python
- OpenCV
- YOLO
- PyTorch
- NumPy
- FastAPI
- PostgreSQL
- SQLAlchemy
- LLM API
- Embeddings/vector database (later)
- React or another frontend (later)
- Docker (later)

## Architecture Phases

### Phase 0: Project setup
- Folder structure, Git, Python environment, configuration

### Phase 1: Camera/room scanning
- Capture video, extract frames, simple interface to start/stop scan

### Phase 2: Object detection using YOLO
- Detect objects in room frames, store classes, confidence, bounding boxes, visualize

### Phase 3: Persistent spatial memory
- PostgreSQL, store detected objects, scans, timestamps, locations, confidence
- Compare scans, update object observations, handle object movement

### Phase 4: Natural language interface
- Integrate LLM, implement tool/function calling
- Tools: find_object(), get_recent_location(), list_objects(), get_objects_near()
- LLM retrieves facts from database instead of hallucinating

### Phase 5: Spatial intelligence
- Represent spatial relationships (ON, NEAR, LEFT_OF, RIGHT_OF, INSIDE, BEHIND)
- Spatial knowledge representation, improve location estimation

### Phase 6: Agentic behavior
- Agent reasons about requests, calls tools, inspects memory, determines uncertainty
- Requests new camera scan when necessary, confidence-aware responses

### Phase 7: AR navigation
- Investigate ARCore/ARKit, SLAM, spatial anchors, camera pose
- Guide user toward detected object

### Phase 8: Optional wearable camera
- Explore camera mounted on glasses/forehead, stream video to phone/computer for inference

## Development Rules

1. Build one phase at a time.
2. Do not generate the entire project at once.
3. Explain important code and architectural decisions.
4. Prefer clean, modular production-style code.
5. Do not hide complexity behind unnecessary libraries.
6. Explain why each technology is being used.
7. Include tests where appropriate.
8. Use Git commits at meaningful milestones.
9. Keep security, API keys and environment variables out of source control.
10. At the end of each phase, document:
    - What we built
    - What we learned
    - How components work together
    - Interview questions to answer
    - What the next phase will add

## Getting Started

See the documentation for each phase.

