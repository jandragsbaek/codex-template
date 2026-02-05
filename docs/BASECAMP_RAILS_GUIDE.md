---
title: Basecamp Rails Guide
read_when: "building/refactoring Rails architecture, dev workflow, or deployment"
summary: "Basecamp/37signals Rails patterns for dev, test, deploy."
---
# Basecamp Rails Guide

Short, practical guidelines distilled from Basecamp/37signals open repos (Fizzy, Once Campfire) and aligned with our local vanilla-Rails docs.

## Defaults to follow
- Vanilla Rails first: thin controllers + rich models + RESTful resources (see `docs/PRINCIPLES.md`, `docs/ARCHITECTURE.md`).
- Simple deployables: single-container, single-machine friendly; scale by adding instances.
- Min deps: prefer Rails built-ins; no extra layers unless justified.
- Inline edits: prefer Turbo Frames + partial replace over full-page reloads for row-level edits.

## Development workflow (Basecamp-style)
- Setup via `bin/setup`; use `bin/setup --reset` to wipe/seed.
- Start dev via `bin/dev` (or `bin/rails server` for simpler apps).
- Provide seeded login paths; keep onboarding scripted.
- Use env for feature switches (VAPID keys, mailer behavior, etc.).

## Database posture
- SQLite first for dev; MySQL supported where parity needed.
- Switch adapter via `DATABASE_ADAPTER` env and re-run setup/tests.
- CI should exercise SQLite + MySQL where feasible.

## Testing + CI
- Fast loop: `bin/rails test`.
- Full gate: `bin/ci` that runs lint + security + tests.
- Keep system tests serial/limited; cover behavior with model/controller tests.

## Deployment posture
- **Self-host/simple**: ship a Docker image that includes web, jobs, caching, file serving, SSL.
- Persist storage under `/rails/storage` via volume mounts.
- Configure via env: `SECRET_KEY_BASE`, `BASE_URL`, TLS/SSL domain, SMTP, VAPID keys, `ACTIVE_STORAGE_SERVICE`, `MULTI_TENANT`.
- **Customizable**: use Kamal with `config/deploy.yml`; secrets in `.kamal/secrets`.

## SaaS vs OSS split (when needed)
- Keep hosted-only integrations in a vendored engine/gem (e.g., `saas/`).
- Toggle mode via app tasks; keep OSS path clean.

## Linting + style enforcement
- Base style: `rubocop-rails-omakase` with minimal overrides.
- Local style rules still apply (see `docs/STYLE.md`).

## Delta vs `basecamp-vanilla-rails-guide.md`
- Added deployment patterns (Docker/Kamal, env config, `/rails/storage`).
- Added dev workflow norms (`bin/setup`, `bin/dev`, env toggles).
- Added DB posture (SQLite default, MySQL optional, CI on both).
- Added CI gate emphasis (`bin/ci` runs lint + security + tests).
- Added SaaS/OSS split pattern (vendored engine).
