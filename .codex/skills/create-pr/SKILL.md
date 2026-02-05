---
name: create-pr
description: Create a fresh feature branch from main, rebase on latest main, and open a GitHub PR with a solid summary/testing notes. Use when asked to “start a branch,” “rebase from main,” “open a PR,” or “get a PR going.”
---

# Create PR

## Overview

Fast, safe branch setup + rebase on `origin/main`, then open a PR with required labels and a detailed description.

## Workflow Decision Tree

- Working tree dirty? Review `git status/diff` to confirm scope; ask before proceed if unrelated/unexpected.
- User asked for new branch? Create from `origin/main`.
- User asked for rebase? Rebase branch onto `origin/main`.
- PR requested? Create via `gh pr create` and add required label.
- Skill invoked: you have consent to switch branches and must generate a sensible branch name.
- Check available skills; apply any that match the request.

## Step 1: Preflight

- `git status -sb`
- `git --no-pager diff --color=never`
- If dirty: check for unrelated/unexpected changes; ask before proceed.
- Skill invocation grants branch switch consent.
- Branch naming: infer from scope + change type. Format: `<type>/<topic>-<short-detail>`, lowercase, hyphens.
  - Examples: `chore/skills-pr-flow`, `docs/skills-docs-first`, `fix/ci-loop-q-lty`.

## Step 2: Sync main

- `git fetch origin`
- `git checkout main`
- `git pull --ff-only`

## Step 3: Create or update branch

New branch:
- `git checkout -b <branch> origin/main`

Existing branch:
- `git checkout <branch>`
- `git rebase origin/main`

## Step 4: Commit (if changes)

Always ensure you are on the PR branch before committing.

Use Conventional Commits:
- `feat:` new behavior
- `fix:` bug fix
- `refactor:` refactor only
- `chore:` tooling/docs/cleanup
- Prefer `./scripts/committer` for commits.

One-line summary: imperative, concise. Body (if needed): why + risk/impact.

## Step 5: Push + PR

- `git push -u origin <branch>`
- If skill invoked: you have permission to open the PR.
- Read the changes (`git status/diff`, key files) to build a specific PR summary/changes/testing section.
- Always provide a PR body using the template below.
  - Prefer: `gh pr create --label <type> --title "<title>" --body-file <(printf "...")`
  - If PR already exists or `--fill` is required: `gh pr edit <number> --body "<body>"`
- Use `gh pr view/diff` to inspect the PR state/diff.

Required labels:
- `type/feature`
- `type/fix`
- `type/chore`
- `type/skip-changelog`

## Step 6: CI check

- Loop: `gh run list` → `gh run view <id>` → fix → push → repeat until green (usually 60–90s).
- If CI returns qlty feedback, address it, then re-run.
- Run `bin/ci --no-signoff` before pushing; after push, run `bin/ci`.

## PR Body Template (default)

```
## Summary
- ...

## Changes
- ...

## Testing
- `...`

## Notes
- ...
```
