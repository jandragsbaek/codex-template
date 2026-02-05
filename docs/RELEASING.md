---
title: Releasing
read_when: "cutting a release or changing release workflow"
summary: "How Release Drafter builds notes and how to publish a release."
---
# Releasing

## How it works

Release Drafter builds draft notes from PR labels. When you publish a release, the current draft becomes the release notes.

## Version bumping

Default: patch. Add `version:bump-minor` or `version:bump-major` on the PR for larger bumps.

## Cut a release

1. Open GitHub Releases.
2. Open the draft release.
3. Review and edit notes if needed.
4. Publish.

## Excluding PRs

Label PRs with `type/skip-changelog` to keep them out of the release notes.
