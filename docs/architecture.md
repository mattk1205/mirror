# Architecture decisions

This document records Lesson 1 decisions. It describes intended architecture;
implementation and verification status must be tracked separately.

## Platform and application boundaries

| Area | Decision and rationale |
| --- | --- |
| Display | Pi 3 with Raspberry Pi OS and graphical Chromium kiosk. Keep the device primarily a thin client and allow migration to Pi 5. |
| Initial server | Existing Windows 11 PC with WSL. Reusing current hardware removes the old PC assessment as a blocker. |
| Frontend | React, TypeScript, Vite, Tailwind. Reuse React experience; alternatives need a measurable practical benefit. |
| Frontend tooling | Deno for dependencies and development tasks, chosen as a learning opportunity and preferred project direction. It does not run the deployed browser UI. |
| Backend | One Django project with DRF. Reuse Django experience and its models, migrations, authentication, and API validation. |
| Python tooling | uv project workflow with `pyproject.toml`, committed `uv.lock`, and a local managed environment. |
| Persistence | SQLite on the server's local Linux filesystem. Expected write concurrency does not justify a separate database service initially. |
| Web serving | Caddy serves built frontend assets and proxies API requests to Gunicorn/Django under one browser origin. |
| Repository | Separate `frontend/` and `backend/` directories in one repository, with independent dependency manifests and lockfiles. |
| Development | Podman Compose starts development services together, with mounted source and live reload. Explicitly use the `podman-compose` provider. |
| Deployment | Rootless Podman with Quadlet/systemd; Caddy and Gunicorn replace development servers. Keep development and deployed data separate. |

The Pi renders and handles interaction. Django owns application rules, persistence,
authentication, and provider-specific integrations. Presentation does not couple
directly to third-party APIs. Integrations must support mocking during development.

## Dashboard behavior

- One frontend application contains modular widgets and fullscreen application views.
- A widget registry identifies available widgets. No runtime plugin platform initially.
- Typed TypeScript configuration defines widget instances, grid positions, sizes,
  and settings. Rebuild and redeploy for layout changes; touch layout editing is deferred.
- Keep widget-specific state local and data access behind hooks/services.
- Prioritize touch responsiveness and smooth updates. Avoid hover-dependent controls
  and unnecessary background work. Validate performance on the Pi rather than
  assume a framework or bundle-size advantage proves suitability.
- Use ordinary HTTP requests: fetch on load, refresh after edits, and modest polling
  where needed. Intervals are integration-specific; roughly a minute is an initial
  reference, not a requirement for every widget. No SSE or WebSockets initially.
- During disconnection, show already loaded data as potentially stale, disable
  edits, and retry. Do not acknowledge unconfirmed changes as saved. Offline startup
  and queued writes are deferred.
- Development mode exposes useful widget diagnostics. Production shows a small
  failure note and keeps other widgets usable where possible. Detailed UI design is deferred.

## Identity and first applications

- One user account, Django session authentication, authenticated APIs, and CSRF
  protection for changes. No registration or profile switching initially.
- The mirror stays signed in and unlocked; physical access permits viewing and
  editing. Sessions can expire and require reauthentication.
- Phone-specific work is deferred. If remote access is needed later, the developer
  intends to use a home VPN; authentication still applies.
- Calendar and to-do are the first planned applications, with backend-owned data.
  Calendar recurrence is required, but application schemas and recurrence details
  are separate planning tasks. Do not implement them during infrastructure setup.

## Operations and verification

- Brief planned downtime for updates is acceptable. Back up before migrations.
- Target a recovery point of one day: daily consistent SQLite snapshots, seven
  daily recovery points, retained snapshots and retry after delivery failure, plus
  pre-migration backups and a restore test.
- Initially copy snapshots to a separate physical backup HDD in the Windows host.
  This is separate-drive protection, not off-machine protection. Loss of the whole
  PC remains an accepted gap. Keep delivery configurable for later cloud storage.
- Client-side backup encryption is deferred. Google Drive and rclone are not fixed
  dependencies. Do not synchronize the live database as a backup strategy.
- **Unit tests:** individual behaviors.
- **Gate 1 — subsystem verification:** frontend, backend, and Pi workflows checked
  separately, using appropriate unit/integration tests and device checks.
- **Gate 2 — system verification:** complete connected workflows plus touchscreen,
  startup/recovery, and performance checks on the actual Pi.
- Django's test runner and DRF's `APISimpleTestCase` are used for the health endpoint
  test. Vitest and Playwright remain candidates; verify the frontend test runtime
  with Deno before committing to it.

## Deferred decisions and setup checks

- Display hardware, resolution, orientation, and measured performance targets.
- WSL version/distribution, systemd and rootless Podman support, LAN access from
  the Pi, and startup/sleep behavior of the host.
- HTTPS, stable home-network addressing, exact supported tool versions, and backup transport.
- Frontend test-tool compatibility and concrete gate commands.
- Dedicated server hardware, Electron/native desktop features, runtime plugins,
  real-time messaging, cloud backups, and offline writes remain deferred.

## Current implementation status

Django and Django REST Framework are installed and tracked with a uv manifest and
lockfile. The `core` app exposes an anonymous `GET /api/health/` endpoint returning
`{"status": "ok"}`. Its automated test, local Django system check, and lockfile
consistency check pass. Built-in migrations were previously verified as applied
to the host database; container data is separate. A backend development
Containerfile and Podman Compose configuration now exist, with mounted source,
Django live reload, and a separate named volume for development SQLite data.
The developer reported successful rootless Podman and browser health checks in
WSL. Container-specific test execution, live reload, and database persistence
across container recreation remain to be explicitly verified. The health test
does not check database access. Application authentication remains unimplemented.
Frontend, production containers, and hardware validation remain unimplemented.
Neither Gate 1 nor Gate 2 is complete.
