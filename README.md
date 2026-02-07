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
- Run `bin/ci` before merging (lint + security + tests + signoff)
- Use `bin/ci --no-signoff` for local dev
- Invoke `$create-pr` to open a PR with required labels
- PR labels flow into Release Drafter -> cut a release when ready

## Docs

- `docs/ARCHITECTURE.md` — Rails-first structure and patterns to avoid. Use when shaping app layout.
- `docs/BASECAMP_RAILS_GUIDE.md` — practical Rails workflow + deploy norms. Use when deciding dev/test/deploy defaults.
- `docs/CODEX_CLI.md` — where Codex skills/history live. Use when working on agent tooling.
- `docs/CONCURRENCY.md` — Real-time patterns and concurrent writes. Use when adding ActionCable or Turbo Streams.
- `docs/ERROR_HANDLING.md` — Exception strategy and resilience. Use when adding rescue blocks or external services.
- `docs/MULTI_TENANCY.md` — acts_as_tenant patterns. Use when adding models or writing queries.
- `docs/PERFORMANCE.md` — Query budgets and baselines. Use when optimizing or adding eager loading.
- `docs/PRINCIPLES.md` — core Rails principles + testing posture. Use for architectural tradeoffs.
- `docs/STYLE.md` — Ruby style + lint baseline. Use when editing or setting lint rules.

## Skills

- [`ask-questions-if-underspecified`](https://github.com/trailofbits/skills/tree/main/plugins/ask-questions-if-underspecified) — Clarify before implementing
- [`brave-search`](https://github.com/steipete/agent-scripts/tree/main/skills/brave-search) — Web search without a browser
- `create-pr` — Branch, commit, and open a PR
- [`frontend-design`](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design/skills/frontend-design) — Distinctive UI generation (no AI slop)
- [`game-changing-features`](https://github.com/softaworks/agent-toolkit/tree/main/skills/game-changing-features)
- [`humanizer`](https://github.com/softaworks/agent-toolkit/tree/main/skills/humanizer) — Strip AI writing patterns
- `improve-from-last-day` — Audit recent Codex sessions for doc improvements
- [`seo-audit`](https://github.com/coreyhaines31/marketingskills/tree/main/skills/seo-audit) - SEO audit
- [`ui-ux-pro-max`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) - UI/UX and design system things

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
4. Generate the Rails app:
   ```bash
   rails new . --skip-jbuilder
   ```
5. **Restore customized CI gate** — `rails new` overwrites `bin/ci` and `config/ci.rb` with defaults. Replace `config/ci.rb` with the full gate:
   ```ruby
   CI.run do
     skip_signoff = ARGV.include?("--no-signoff")
     step "Setup", "bin/setup --skip-server"
     step "Style: Ruby", "bundle exec rubocop"
     step "Style: YAML", "yamllint ."
     step "Security: Bundler audit", "bundle exec bundle-audit check --update"
     step "Security: Brakeman", "bundle exec brakeman --exit-on-warn --no-pager"
     step "Security: Importmap audit", "bin/importmap audit"
     step "Tests: All", "bin/rails test:all"
     if success? && !skip_signoff
       step "Signoff", "gh signoff"
     elsif !success?
       failure "CI failed.", "Fix issues and retry."
     end
   end
   ```
6. Add lint + security gems to Gemfile:
   ```ruby
   gem "rubocop-rails-omakase", require: false
   group :development, :test do
     gem "brakeman"
     gem "bundler-audit"
   end
   ```
7. Run `bundle install && bin/ci --no-signoff` to verify

Rails 8 defaults already include Propshaft, Importmap, Solid Queue/Cache/Cable, and SQLite. See `docs/ARCHITECTURE.md` for stack rationale.

## Credit

Inspired by `github.com/steipete` and his agent-skills repository. Rails conventions informed by 37signals/Basecamp.
