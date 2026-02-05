---
title: Codex CLI
read_when: "working on Codex skills, session history, or agent tooling"
summary: "Skill locations, precedence, and history logs for Codex CLI."
---
# Codex CLI

## Skills

- Repo skills live at `./.codex/skills` and are the only source of truth.

## History / Sessions

- Session logs: `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` (authoritative for user + assistant).
- Prompt-only fallback: `~/.codex/history.jsonl` (often lacks assistant output).
- History persistence: `~/.codex/config.toml` `[history]` settings.
