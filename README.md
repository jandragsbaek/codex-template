# Codex Template

Clean starting point for Codex projects.

## How I use it

- I write long, specific prompts. That works best for me.
- I specifically use `gpt-5.2-codex high`.
- I usually end long prompts with `$ask-questions-if-underspecified`.
- I let it run; it can take a while.
- When I'm happy, I run the full gate.
- After that, I invoke `$create-pr`.
- That gets me a PR on GitHub; automation handles the rest.
- PR labels flow into the draft release via Release Drafter until I cut a release.

Two small GitHub Action runners handle versioning.


## Docs

- `docs/ARCHITECTURE.md` — Rails-first structure and patterns to avoid. Use when shaping app layout.
- `docs/BASECAMP_RAILS_GUIDE.md` — practical Rails workflow + deploy norms. Use when deciding dev/test/deploy defaults.
- `docs/CODEX_CLI.md` — where Codex skills/history live. Use when working on agent tooling.
- `docs/PRINCIPLES.md` — core Rails principles + testing posture. Use for architectural tradeoffs.
- `docs/STYLE.md` — Ruby style + lint baseline. Use when editing or setting lint rules.

## Credit

Inspired by `github.com/steipete` and his agent-skills repository.
