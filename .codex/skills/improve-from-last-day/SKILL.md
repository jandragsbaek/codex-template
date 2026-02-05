---
name: improve-from-last-day
description: Review the last 24 hours of Codex CLI conversations between Jan and the assistant, extract improvements, and update docs/ and/or AGENTS.md accordingly. Use when asked to audit recent chats, harvest lessons learned, or turn conversation gaps into documentation/instruction changes.
---

# Improve From Last Day

## Goal

Systematically scan the last 24 hours of Codex CLI conversations, identify improvements, and apply doc/agent updates.

## Workflow

### 1) Locate Codex CLI history

- Determine CODEX_HOME: use `$CODEX_HOME` if set; else default to `~/.codex`.
- Prefer session logs: `CODEX_HOME/sessions/YYYY/MM/DD/rollout-*.jsonl`.
- Use `CODEX_HOME/history.jsonl` as fallback (typically user prompts only).
- If nothing exists, ask user to provide/export history.

### 2) Extract last-24h transcript

- Use the script below to extract user + assistant messages from the last 24 hours:

```bash
python3 /Users/dragsbaek/src/pje1/.codex/skills/improve-from-last-day/scripts/collect_codex_conversations.py \
  --since-hours 24 \
  --out /Users/dragsbaek/src/pje1/tmp/codex-last-24h.txt
```

- If the script fails, inspect a recent session file directly and continue manually.

### 3) Identify improvements

Look for:
- Repeated clarifications or back-and-forths
- Missing/unclear instructions in `AGENTS.md`
- Missing/unclear docs in `docs/`
- Common errors/tool friction
- Process gaps (tests, CI, PR flow, repo conventions)

Classify each improvement as:
- `AGENTS.md` update (rules, workflow, tooling)
- New or updated doc under `docs/`

Avoid verbatim conversation text in docs; summarize and generalize.

### 4) Apply updates

- Keep notes short; use existing doc patterns.
- Add `read_when` hints if the new guidance is cross-cutting.
- Update only `docs/` and `AGENTS.md` (no other files) unless explicitly asked.

### 5) Report

- Summarize updates and where they landed.
- Call out any missing history/permissions.

## Notes

- Sessions JSONL is authoritative for assistant replies; `history.jsonl` may omit assistant output.
- If a CLI history tool exists, it can help find session IDs, but the JSONL files are the source of truth.
- History persistence is controlled in `CODEX_HOME/config.toml` via `[history]` settings; if persistence is `none`, only sessions/logs may exist.
