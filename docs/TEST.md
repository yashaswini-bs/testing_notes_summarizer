# Engineering Log & Architecture Evolution

**Project:** QA Insight Summarizer
**Architecture:** Decoupled Full-Stack (FastAPI / Vanilla JS SPA / Groq LLM)
**Core Value Proposition:** Converting unstructured exploratory testing notes into defensible, structured QA documentation with automated heuristic tagging and root-cause analysis.

---

## Iterative Build Phases

### Phase 0: Project Scaffold & Environment Setup

* **Objective:** Establish a clean, reproducible, and secure repository foundation.
* **Execution:** Initialized Git and created standard architectural directories (`app/`, `data/`, `tests/`, `docs/`). Configured `.gitignore` to prevent sensitive credential leakage (API keys) and set up the dependency manifest (`requirements.txt`).
* **Outcome:** A secure, standardized project structure ready for modular backend development.

### Phase 1: Test Data Curation

* **Objective:** Develop realistic test fixtures to validate the summarization engine across various edge cases.
* **Execution:** Authored diverse plain-text files representing different exploratory testing scenarios. This included a high-signal bug report (e.g., checkout crashes), a low-signal observation log, and an artificially long session to test backend token limits.
* **Outcome:** A robust suite of sample data ensuring the AI pipeline is evaluated against realistic, messy QA inputs rather than sanitized ideal cases.

### Phase 2: Core AI Summarization Pipeline

* **Objective:** Convert unstructured testing notes into structured, programmatic JSON data.
* **Execution:**
* Implemented strict data typing using Pydantic schemas for `BugCandidate` and `SummaryOutput`.
* Integrated the Groq API (Qwen 3.8-27b model) to parse raw text and return perfectly structured JSON.
* Configured the prompt to extract specific deliverables: Coverage Summary, Defect Candidates, and Open Questions.


* **Outcome:** A functional LLM engine that accurately extracts testing data into a format ready for frontend consumption.

### Phase 3: Defensive Engineering & Guardrails

* **Objective:** Protect the application from prompt injection, false positives, and API rate limits.
* **Execution:**
* **False-Positive Guardrail:** Taught the AI to evaluate intent. If non-testing text (like a recipe or a story about an actual insect) is uploaded, the system halts processing and returns a rejection reason to prevent hallucinated bugs.
* **QA Heuristic Tagging:** Programmed the AI to automatically categorize defects using professional testing frameworks (SFDPOT: Structure, Function, Data, Platform, Operations, Time).
* **Token Limit Handling:** Added character bounds and a graceful Pydantic `try/except` fallback to prevent terminal crashes if the API truncates the JSON response due to length.


* **Outcome:** A resilient backend pipeline that prioritizes accuracy and application stability over blind data extraction.

### Phase 4: Architecture Pivot (Decoupled Full-Stack)

* **Objective:** Transition from a basic prototype wrapper to a production-ready application architecture.
* **Execution:**
* Abandoned the initial UI library plan (Streamlit) in favor of a decoupled architecture.
* Built a standalone REST API using **FastAPI** (`main.py` and `pipeline.py`).
* Configured CORS middleware to allow cross-origin requests.
* Established a `/api/health` endpoint for real-time connection diagnostics.


* **Outcome:** A scalable, maintainable codebase that completely separates the AI logic from the presentation layer, mirroring enterprise software design.

### Phase 5: Workspace Architecture & Local State

* **Objective:** Elevate the user experience from a basic web form to a professional Single Page Application (SPA).
* **Execution:**
* Built a custom HTML/CSS/JS frontend styled as a modern developer workspace (dark sidebar, data-rich canvas, custom typography).
* Implemented **Local Storage** to retain a persistent history of previous analysis sessions entirely on the client side, ensuring data privacy and zero database dependency.
* Added a dynamic split-screen layout that smoothly transitions from a full-width input console to a side-by-side data review dashboard upon data generation.
* Built a settings panel to toggle UI compactness and actively ping the FastAPI `/api/health` endpoint for real-time diagnostic status.


* **Outcome:** A polished, enterprise-grade interface that seamlessly integrates with the Python backend while offering advanced client-side features.