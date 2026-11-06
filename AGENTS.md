# Project Instructions

## Project Purpose
This project is a touchscreen home dashboard / smart mirror.

## Core Stack
- React
- Vite
- TypeScript
- Tailwind CSS
- Deno for frontend dependency management and development tasks
- Python with Django and Django REST Framework for the backend
- uv for Python project, environment, and dependency management
- SQLite for initial persistence
- Caddy and Gunicorn for production web serving

## Project Context and Handoffs
- Read `docs/architecture.md` for agreed decisions, rationale, and unresolved setup checks.
- Read the applicable task plan before implementation. The initial backend plan is `docs/plans/backend-bootstrap.md`.
- Keep one repository with separate `backend/` and `frontend/` directories; create directories only when needed.
- Distinguish selected architecture from implemented or verified capabilities.
- Keep documentation consistent with changes; do not silently reopen settled decisions.

## Collaboration
- The developer retains ownership of architecture and important application logic.
- Prefer small, reviewable changes and explain unfamiliar concepts or significant changes.
- When teaching or clarifying, ask one question at a time.
- Do not implement future features merely because they appear in the architecture record.
- The developer will install dependencies and initialize Django for the initial backend bootstrap. Do not do those steps unless subsequently requested.

## Development and Deployment
- Run development services together with Podman Compose, using the `podman-compose` provider.
- Use rootless Podman with Quadlet/systemd for deployed services; development and deployment are distinct configurations.
- Initial hosting is the developer's Windows 11 PC with WSL. Verify WSL networking and service startup during deployment setup.
- Keep development and deployed databases separate and persist data outside container writable layers.
- Track dependency manifests, lockfiles, and Django migrations. Never commit credentials or live databases.

## Verification
- Unit tests cover individual behaviors.
- Gate 1 verifies frontend, backend, and Pi subsystems separately, with relevant unit tests, integration tests, and device checks.
- Gate 2 verifies the connected system through end-to-end workflows and target-hardware acceptance checks.
- Use checks appropriate to the change. Documentation-only changes do not require executable tests.
- Test tools are not finalized; verify Deno compatibility before selecting the frontend test workflow.

## Hardware Target
- Initial target display is a Raspberry Pi 3.
- Keep the project easy to migrate to a Raspberry Pi 5 later.
- The Raspberry Pi should behave primarily as a thin client.

## Performance
- Performance and low resource usage are priorities.
- Avoid unnecessary background processing on the Raspberry Pi.
- Avoid unnecessary dependencies.
- Add a dependency only when it provides significant value over a simple native implementation.

## UI / UX
- Design primarily for touchscreen interaction.
- Do not depend on mouse hover for important functionality.
- Controls should have appropriate touch targets.
- The dashboard should work well fullscreen in Chromium kiosk mode.

## Architecture
- Keep components modular and reusable.
- Keep presentation logic separate from external-service integration.
- Isolate external integrations behind services, hooks, or API abstraction layers.
- Avoid tightly coupling components directly to third-party APIs.
- Design integrations so they can be mocked during development.

## Future Integrations
The architecture should accommodate future integrations such as:
- Home Assistant
- Spotify
- Calendar
- Weather
- Tasks
- Cameras
- AI assistant

Do not implement these prematurely unless required by the current task.

## Engineering Principles
- Prefer simple solutions over unnecessary abstraction.
- Keep the codebase understandable for a single developer.
- Maintain strong TypeScript typing.
- Avoid premature optimization, but consider Raspberry Pi 3 resource limits when making architectural decisions.
- Do not perform major architectural changes without first explaining:
  - why the change is needed
  - benefits
  - drawbacks
  - migration impact
