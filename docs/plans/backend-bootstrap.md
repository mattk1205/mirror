# Backend bootstrap handoff

## Historical scope

This plan records the original documentation-only bootstrap. Subsequent work
authorized in the conversation added Django, DRF, a health endpoint and test, and
Podman development configuration. The original stopping point below applies to
that initial task. See `../architecture.md` and `../../backend/README.md` for
current implementation and verification status.

## Objective and current state

Prepare a minimal backend skeleton before the developer installs Django. Read
`AGENTS.md` and `docs/architecture.md` first. The architecture is selected, but the
application has not been initialized.

The documentation-only skeleton already exists:

```text
backend/
├── README.md
└── .gitignore
```

`backend/README.md` explains the tooling and intended Django structure. The ignore
file excludes environments, Python caches, local databases/journals, and secret
environment files, while allowing a sanitized `.env.example`.

## Ownership and stopping point

- The developer will install dependencies with uv and initialize Django.
- Do not install dependencies, run project generators, or create `manage.py`,
  `config/`, `pyproject.toml`, or a lockfile without a subsequent explicit request.
- Do not create handwritten Django placeholders, feature apps, frontend files,
  container configuration, or backup automation in this task.
- Preserve existing user changes. Keep documentation truthful about actual state.

After developer initialization, the intended generated structure is:

```text
backend/
├── README.md
├── .gitignore
├── pyproject.toml
├── uv.lock
├── manage.py
└── config/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

Start with one settings module. Add application modules and additional settings
structure only when an actual task requires them.

## Acceptance and verification

- Root README links to the architecture record, agent instructions, and this plan.
- Agent instructions include the chosen stack, collaboration boundaries, and gates.
- Backend documentation and ignore rules exist; no application code or dependencies
  are introduced by this bootstrap.
- Inspect the file tree, diff, and whitespace. No executable application tests are
  needed for this documentation-only task.

## Status and next handoff

The documentation-only bootstrap is complete once the acceptance checks pass.
There is no remaining installation authorization in this plan. Wait for the
developer's Django setup or a new explicitly scoped task before further implementation.
