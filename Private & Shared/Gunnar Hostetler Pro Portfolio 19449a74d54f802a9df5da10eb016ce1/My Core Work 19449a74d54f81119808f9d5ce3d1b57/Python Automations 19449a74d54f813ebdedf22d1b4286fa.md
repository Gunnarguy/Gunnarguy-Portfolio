# Python Automations

Key skills: Python

**What:**

- **Timeline:** Python development journey (2023 – present), totaling 30+ bespoke scripts and modules.
- **Domains:**
    - **Automation & Scripting:** Scheduled backups, image/video pipelines, system monitoring.
    - **Computer Vision:** Timelapse capture, real-time frame processing, edge detection, color correction.
    - **Embedded/Linux Control:** GPIO & I²C/SPI device drivers, sensor data collection (BME280, SSD1306), systemd services.
    - **Data Engineering:** PDF/DOCX/TXT ingestion, OCR pipelines (Tesseract, EasyOCR), batch conversions with Python-FFmpeg.
    - **AI/API Integration:** OpenAI embeddings & chat, Pinecone vector stores, LangChain-style orchestration.
    - **Utilities & DevOps:** Custom CLI tools, Flask/FastAPI microservices, GitHub Actions for CI, Docker containerization.

**Why:**

- **Universal Glue Language:** Python’s ecosystem enables rapid prototyping across hardware, data, and AI domains.
- **End-to-End Ownership:** Build complete solutions—from sensor wiring on a Pi to deploying a Flask API in the cloud.
- **Automate Repetitive Tasks:** Replace manual workflows (e.g., camera timelapses, file conversions) with reliable, scheduled scripts.
- **Bridge Research & Production:** Validate computer vision and ML concepts locally before scaling to cloud or edge devices.

**How:**

- **Core Stack:** Python 3.7–3.12, VS Code, Linux (Debian, Ubuntu), Raspberry Pi, Docker.
- **Key Libraries & Frameworks:**
    - **Vision:** opencv-python, picamera2, ffmpeg-python
    - **Data & ML:** numpy, pandas, scikit-learn, tensorflow-lite
    - **APIs:** openai, pinecone-client, requests, aiohttp (async)
    - **Web Services:** Flask, FastAPI, uvicorn, gunicorn
    - **Testing & Quality:** pytest, flake8, black, mypy
- **Architectural Patterns:**
    - **Modular Scripts:** Clear separation of I/O, processing, and orchestration layers.
    - **Asynchronous Pipelines:** asyncio for nonblocking API calls and sensor reads.
    - **Service Automation:** cron jobs and systemd units for reliable startup and error recovery.
    - **Version Control:** Git repos with tag-based releases; CI via GitHub Actions for linting, testing, and Docker image builds.
- **Troubleshooting Highlights:**
    - Resolved **dependency conflicts** across Python 3.8 vs 3.12 by standardizing on virtualenv+pip-tools.
    - Debugged **camera disconnects** under load by implementing exponential backoff and reconnect logic.
    - Overcame **PDF parsing edge cases** (embedded fonts, scanned images) by chaining Tesseract with PDFMiner and custom OCR post-processing.
    - Mitigated **memory leaks** in long-running scripts using weak references and explicit resource cleanup.

**Implications:**

- **End-to-End Expertise:** Demonstrates ability to design and ship full-stack Python solutions—from low-level hardware interfacing to cloud-deployed APIs.
- **Scalability & Reliability:** Production-grade practices (testing, CI/CD, containerization) ensure maintainable, robust pipelines.
- **Interdisciplinary Agility:** Deep fluency bridging embedded systems, data science, computer vision, and generative AI—ready for roles in IoT, MLOps, or backend engineering.
- **Productivity Gains:** Automated workflows save ≈10 hrs/week previously spent on manual conversions and monitoring.

**Current Status:**

- **Live Deployments:**
    - **Timelapse Service:** systemd-managed Python service on Pi, >100 runs with 99 % uptime.
    - **Document-Embedding API:** Flask microservice handling 200 requests/day, 0 production errors in 30 days.
- **Active Enhancements:** Integrating async sensor dashboards via FastAPI, migrating select scripts to lightweight Docker containers for remote execution.
- **Next Steps:** Deepen async architecture with trio or anyio, add real-time WebSocket feeds for vision data, expand test coverage to 90 %+ for all core modules.

---