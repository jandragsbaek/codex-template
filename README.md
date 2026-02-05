# Codex Template

Opinionated Rails 8 starter for Codex CLI, built on 37signals/Basecamp conventions.

## Stack

- Propshaft
- Importmap
- Hotwire (Turbo + Stimulus)
- Solid Queue/Cache/Cable
- SQLite
- Minitest + Fixtures
- rubocop-rails-omakase

See `docs/ARCHITECTURE.md` for full details.

## How It Works

- Long, specific prompts -> Codex CLI (`gpt-5.2-codex high`)
- End prompts with `$ask-questions-if-underspecified` when needed
- Ask codex to run full gate
- Invoke `$create-pr` to open a PR with required labels
- PR labels flow into Release Drafter -> cut a release when ready

## Docs

- `docs/ARCHITECTURE.md` — Rails-first structure and patterns to avoid. Use when shaping app layout.
- `docs/BASECAMP_RAILS_GUIDE.md` — practical Rails workflow + deploy norms. Use when deciding dev/test/deploy defaults.
- `docs/CODEX_CLI.md` — where Codex skills/history live. Use when working on agent tooling.
- `docs/PRINCIPLES.md` — core Rails principles + testing posture. Use for architectural tradeoffs.
- `docs/STYLE.md` — Ruby style + lint baseline. Use when editing or setting lint rules.

## Skills

- `ask-questions-if-underspecified` — Clarify before implementing
- `brave-search` — Web search without a browser
- `create-pr` — Branch, commit, and open a PR
- `frontend-design` — Distinctive UI generation (no AI slop)
- `humanizer` — Strip AI writing patterns
- `improve-from-last-day` — Audit recent Codex sessions for doc improvements

## Scripts

- `scripts/committer` — Safe commit helper (stages only listed paths)
- `scripts/docs-list` — List docs with front-matter summaries
- `scripts/browser-tools` — Chrome DevTools CLI (macOS)
- `scripts/trash.ts` — Move files to trash instead of rm
- `bin/coverage_insights` — Coverage analysis with priority-based recommendations

## CI/CD

Required PR labels -> tests on self-hosted runner -> Release Drafter builds changelog -> publish when ready. See `.github/workflows/` for details.

## Getting Started

1. Use this template (or fork)
2. Update `AGENTS.md` with your contact info and project-specific rules
3. Customize `docs/` for your domain
4. `rails new . --skip-jbuilder`

Rails 8 defaults already include Propshaft, Importmap, and SQLite. See `docs/ARCHITECTURE.md` for stack rationale.

## Credit

Inspired by `github.com/steipete` and his agent-skills repository. Rails conventions informed by 37signals/Basecamp.
