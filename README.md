# Intellex Orchestrator

Agent/LLM workers that handle research workflows, plan updates, and chat responses triggered by the API.

## Scope
- Execute user/agent message flows and update research plans asynchronously.
- Manage LLM providers, tool runners, and retries without blocking the public API.
- Emit telemetry/events and write results back through shared clients.

## Proposed stack
- Python worker (shares deps/models with the API).
- Queue + scheduler (Redis-backed; pick Arq/RQ/Celery) for job dispatch from the API.
- Optional internal FastAPI/gRPC endpoint for control-plane ops and callbacks.

## Repo layout (proposed)
- `app/core/` — config, logging, metrics, settings.
- `app/clients/` — API + Supabase clients using `intellex-shared`.
- `app/services/` — LLM provider adapters, tool runners.
- `app/workers/` — job definitions/routers and worker entrypoints.
- `scripts/` — local dev helpers, seeders, smoke jobs.
- `tests/` — unit/integration for job flows and tool execution.

## Workflow
1) Install deps and pull contracts from `intellex-shared` + env from `intellex-infra`.
2) Run the worker against the chosen queue backend; point callbacks to `intellex-api`.
3) Validate job schemas and result writes against Supabase policies before rollout.

## Next actions
- Choose queue runtime and define job envelope (idempotency, tracing, retry budget).
- Port the current `app/services/orchestrator.py` + `llm.py` from `intellex-api` into workers.
- Add smoke jobs and a minimal control endpoint for health/metrics.

## Current worker scaffold
- In-memory queue (`app/workers/queue.py`) with `MessageJob` handling (`app/workers/jobs.py`).
- API callback client (`app/clients/api.py`) posts results to `API_BASE_URL`.
- Entry: `python scripts/run_worker.py` (uses in-memory queue; replace with Redis-backed queue for prod).
