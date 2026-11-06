# Backend agent instructions

These instructions apply to `backend/`. Follow the repository's shared project
instructions and the backend-specific guidance below. Current user instructions
take precedence over historical plans.

## Read first

- `../docs/architecture.md`: selected architecture and verification status.
- `README.md`: backend workflow, container storage, and known limitations.
- The plan applicable to the requested task. `../docs/plans/backend-bootstrap.md`
  records the original bootstrap and is historical; Django is already initialized.
- Inspect the actual implementation before making changes. Documentation records
  prior verification, not proof that checks pass in the current environment.

## Purpose and boundaries

- Keep the Raspberry Pi a thin client. Django owns application rules, persistence,
  authentication, and external-service integration.
- Work on the backend requested by the developer. Do not modify frontend or
  deployment behavior as an incidental cleanup.
- The developer owns architecture and important application logic. Explain
  significant changes, favor small reviewable steps, and ask one question at a
  time when clarification is needed.
- Do not reinitialize Django or replace the existing skeleton. The developer's
  initial installation step is complete; further work needs a scoped task.
- Calendar, tasks, recurrence, and other integrations are planned capabilities,
  not authorization to implement them now.

## Stack and code organization

- Use Python, Django, Django REST Framework, SQLite, and uv.
- `pyproject.toml` and `uv.lock` define Python dependencies. Use uv for dependency
  changes; keep the lockfile consistent and do not maintain a separate dependency
  list by hand. Inspect consumers before changing the existing `requirements.txt`.
- `manage.py` is the Django entry point; `config/` contains project configuration.
- `core/` currently provides `GET /api/health/` and its test.
- Do not relocate code into the existing `src/backend/` package or add settings
  packages, generic repositories, or service layers without a concrete need.
- Use DRF serializers for API input/output and validation when endpoints require
  them. Keep integration-specific code out of views and isolate it for mocking.
- Keep business rules reusable across API endpoints and other entry points;
  introduce abstractions only when they simplify the actual behavior.
- Use Django's ORM and migrations. Commit migrations with model changes; do not
  change schemas manually or rewrite applied migrations as routine cleanup.

## API, identity, and persistence

- The selected identity model is one account with Django sessions, authenticated
  application APIs, and CSRF protection for state-changing browser requests.
- Authentication is not yet implemented. Preserve the explicitly anonymous health
  endpoint; do not copy its `AllowAny` permission to private application endpoints.
- Enforce validation and authorization on the server. Frontend checks are not an
  authorization boundary. Keep credentials and private payloads out of logs.
- Preserve the health contract: HTTP 200 with `{"status": "ok"}`. It is a basic
  application health check, not a database-readiness or full-system check.
- SQLite lives on local server storage. `DJANGO_DATABASE_PATH` selects the database;
  host execution defaults to `backend/db.sqlite3`, containers use `/data/db.sqlite3`.
- Keep development and deployed data separate. Never commit databases, credentials,
  virtual environments, or caches. Track dependency manifests and lockfiles.
- Ordinary HTTP and modest polling are selected. Do not introduce WebSockets,
  background workers, offline-write synchronization, or new infrastructure without
  a task that requires them.

## Development and deployment

- Use rootless Podman Compose for development, with the `podman-compose` provider.
- Run Compose commands from the repository root using `../compose.yaml`, not the
  separate backend-local Compose files. Do not delete those files as incidental work.
- `Containerfile.dev` builds the backend environment. Source mounts read-only at
  `/app`; dependencies live at `/opt/venv`; SQLite uses `backend-dev-data` at `/data`.
- Edit source on the host and use Django live reload. Rebuild the image after
  dependency changes. Generate migrations on the host because mounted source is read-only.
- Applying migrations changes the selected database. Run them only as required by
  the task and identify the target. Do not delete volumes or reset data implicitly.
- Production Caddy/Gunicorn and rootless Podman/Quadlet remain separate from the
  development server. WSL startup, networking, and deployment are not all verified.

## Verification and handoff

- Use existing Django/DRF tests before introducing another testing framework.
- From `backend/`, local checks include `uv lock --check`,
  `uv run python manage.py check`, and `uv run python manage.py test core`.
- From the repository root, container checks include
  `podman-compose run --rm backend python manage.py check` and
  `podman-compose run --rm backend python manage.py test core`.
- Scope tests to changed behavior; expand coverage when failures or integration
  risks justify it. Documentation-only changes need file/diff checks, not Django tests.
- Unit tests check individual behaviors. Gate 1 verifies backend workflows in
  isolation, including relevant API/database integration. Gate 2 verifies the real
  connected frontend/backend/Pi workflows and hardware acceptance.
- The existing health test does not establish database health, authentication,
  live reload, or persistence across container recreation. Do not declare a gate
  complete based on it alone.
- Report changed behavior, checks actually run, their results, and remaining
  limitations. Update backend documentation when workflow or verification changes.
- Preserve unrelated user edits. Do not commit, publish, deploy, or install future
  integrations merely to complete a handoff.
