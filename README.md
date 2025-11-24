# AIEngineering Project

Rough outline of a small RAG playground wired to Airflow. The stack includes:
- Airflow (webserver + scheduler + Postgres) for orchestration.
- LangChain-based ingestion that builds a FAISS vector store from Markdown notes.
- A FastAPI `rag_service` that uses a HuggingFace embedding model and a small text-generation model (`microsoft/phi-1_5`) to answer questions over the ingested notes.

## Repository Layout
- `docker-compose.yaml` — Airflow + Postgres services for local orchestration.
- `Dockerfile.airflow` — placeholder for a custom Airflow image (install Python deps here to make them persistent).
- `dags/agentic_maintenance_dag.py` — DAG scaffold to run ingestion/eval (currently needs fixes to run).
- `rag/ingest.py` — builds the FAISS index from notes in `data/notes`.
- `rag/retriever.py` — loads the FAISS index and returns a LangChain retriever.
- `services/rag_service/app.py` — FastAPI API with an `/ask` endpoint backed by the retriever and text-generation pipeline.
- `scripts/ingest.py` — CLI wrapper for ingestion.
- `config.yaml` — mode-specific paths and RAG parameters.
- `requirements.txt` — Python dependencies (LangChain, FAISS, FastAPI, etc.).

## Prerequisites
- Docker + Docker Compose
- Python 3.11 (matches the Airflow 2.10.x default image)
- Optional: a virtual environment for local Python work

## Quickstart (Docker)
1. Build/install deps into the Airflow image (preferred: bake into `Dockerfile.airflow`; temporary: install in running containers):
   - `docker compose exec airflow-web pip install -r /opt/airflow/repo/requirements.txt`
   - `docker compose exec airflow-scheduler pip install -r /opt/airflow/repo/requirements.txt`
2. Start services: `docker compose up -d`
3. Airflow UI: http://localhost:8080 (uses LocalExecutor, Postgres at `airflow-db:5432`).
4. Mounts: `./dags`, `./scripts`, and the repo are mounted at `/opt/airflow` in the Airflow containers.

## Running Ingestion
The ingestion script reads Markdown files from `data/notes` (see `config.yaml`) and writes a FAISS index to `artifacts/faiss_index`.
- Local: `python -m scripts.ingest --mode local`
- In container: `docker compose exec airflow-web python -m scripts.ingest --mode docker`

## Using the RAG API
- Service code: `services/rag_service/app.py`
- Start locally (after ingestion): `uvicorn services.rag_service.app:app --reload --port 8000`
- Endpoint:
  - `POST /ask` with JSON `{"question": "...", "temperature": 0.0}`
  - Returns the answer plus the retrieved document metadata.
- Health check: `GET /health`

## Airflow DAG Status
`dags/agentic_maintenance_dag.py` is a skeleton and currently has syntax issues (e.g., task args, missing embed task). To make it runnable:
- Fix task definitions and wiring.
- Decide on the command(s) to trigger ingestion/evaluation inside the container.

## Development Notes
- Config is mode-aware: see `config.yaml` for paths and RAG parameters.
- Default embedding model: `sentence-transformers/all-MiniLM-L6-v2`.
- Vector store: FAISS persisted under `artifacts/faiss_index` by default.
- Generation model: `microsoft/phi-1_5` via `transformers.pipeline` (can be swapped for hosted LLM).

## Forward Improvements / Add-ons
- Harden the Airflow DAG: correct syntax, add scheduling, logging, and alerts.
- Build a custom Airflow image that installs Python deps at build time (no runtime `pip install`).
- Add evaluation: scripted QA set, metrics export, and dashboarding.
- Add auth/rate limiting to the FastAPI service; wire in tracing/metrics (OpenTelemetry/Prometheus).
- Support alternative LLM backends (Azure/OpenAI/Anthropic) with config-based selection.
- Improve ingestion coverage (PDF/HTML loaders, chunking strategies, deduping).
- CI/CD: linting/formatting, unit tests, and container build/test on push.
- Kubernetes deployment manifests (Airflow, API, and vector store volume).
