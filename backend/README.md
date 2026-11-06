# Backend

The Django backend provides server-side services and external integrations for the
touchscreen home dashboard, keeping the Raspberry Pi primarily a thin client.
Django is initialized. Python dependencies are managed with uv and tracked in
`pyproject.toml` and `uv.lock`. Django REST Framework is installed, and
`GET /api/health/` returns `{"status": "ok"}` without requiring authentication.

## Development with Podman

Run these commands from the repository root, which contains `compose.yaml`,
without sudo:

```bash
podman-compose build backend
podman-compose run --rm backend python manage.py check
podman-compose run --rm backend python manage.py migrate
podman-compose up backend
```

Open http://localhost:8000/api/health/. Stop the server with Ctrl+C, then run
`podman-compose down` to remove the containers and network.

The root Compose file will coordinate backend and frontend services when the
frontend is added. `backend/Containerfile.dev` defines the backend development
image using Python 3.12 and uv. Production deployment remains separate.

Backend source is mounted read-only at `/app`. Edit files on the host; Django's
development server reloads when Python files change. Container dependencies live
at `/opt/venv`, separate from the host `.venv`. Rebuild after changing dependency
manifests or the lockfile.

## Database and migrations

The container uses `/data/db.sqlite3` in the `backend-dev-data` named volume.
This persists across container removal and is separate from the host database
at `backend/db.sqlite3`. `DJANGO_DATABASE_PATH` selects the container database;
direct host execution uses the existing default path.

`podman-compose down -v` deletes the development data volume. Use it only when
you intend to discard that database. Keep deployed data separate.

Because container source is read-only, generate migrations on the host from
`backend/`:

```bash
uv run python manage.py makemigrations
```

Then apply them to the container database from the repository root:

```bash
podman-compose run --rm backend python manage.py migrate
```

Track dependency manifests, lockfiles, and Django migrations. Never commit
credentials, virtual environments, or live databases.

## Current verification status

The local Django system check, uv lockfile consistency check, and health endpoint
test passed. The test checks anonymous access, HTTP 200, and the expected JSON
through Django's routing and DRF response handling; it does not use the database
or a running server.

Run the test from `backend/`:

```bash
uv run python manage.py test core
```

Or run it in a development container from the repository root:

```bash
podman-compose run --rm backend python manage.py test core
```

The developer reported successful rootless Podman and browser health checks in
WSL. Container-specific test execution, live reload, and database persistence
across container recreation still need explicit verification. The development
server is exposed only on `127.0.0.1:8000`. Caddy, Gunicorn, and Quadlet deployment
have not been configured. These checks do not complete Gate 1 or Gate 2.
