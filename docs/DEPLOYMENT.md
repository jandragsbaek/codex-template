---
title: Deployment
read_when: "Use when preparing for production deployment."
summary: "Production deployment with Kamal + Litestream for SQLite durability."
---
# Deployment

Default production posture: SQLite + Litestream + Kamal.

See also:
- `docs/ARCHITECTURE.md` for stack defaults and database posture.
- `docs/BASECAMP_RAILS_GUIDE.md` for deployment workflow context.

## Why SQLite in Production

- Simpler operations: no separate DB service to run, patch, or tune.
- Lower cost and fewer moving parts on single-node or low-concurrency apps.
- Predictable behavior: same adapter in dev/test/prod.
- Durable enough when paired with Litestream continuous replication.

SQLite is the default. Move to MySQL/PostgreSQL only when write concurrency or topology requires it.

## Litestream for Durability

Litestream continuously replicates SQLite WAL changes to object storage.

### Example `litestream.yml` (S3 or S3-compatible)

```yaml
dbs:
  - path: /rails/storage/production.sqlite3
    replicas:
      - type: s3
        bucket: my-app-litestream
        path: production.sqlite3
        region: us-east-1
        endpoint: https://s3.us-east-1.amazonaws.com
        access-key-id: ${LITESTREAM_ACCESS_KEY_ID}
        secret-access-key: ${LITESTREAM_SECRET_ACCESS_KEY}
```

Notes:
- `endpoint` can target compatible providers (Cloudflare R2, MinIO, Backblaze, etc.).
- Keep bucket/path stable per environment (`production`, `staging`) to avoid overlap.
- Run Litestream restore on boot when local DB file is missing.

## Kamal Setup Basics (`config/deploy.yml`)

Minimal shape:

```yaml
service: my_app
image: ghcr.io/my-org/my_app

servers:
  web:
    - 203.0.113.10

proxy:
  ssl: true
  host: app.example.com
  healthcheck:
    path: /up

registry:
  server: ghcr.io
  username: my-org
  password:
    - KAMAL_REGISTRY_PASSWORD

env:
  clear:
    RAILS_ENV: production
  secret:
    - SECRET_KEY_BASE
    - DATABASE_URL
    - LITESTREAM_ACCESS_KEY_ID
    - LITESTREAM_SECRET_ACCESS_KEY
```

Keep deployment config in repo; keep secrets out of repo.

## Environment Variables + Secrets Management

Core runtime env:
- `RAILS_ENV=production`
- `RAILS_LOG_TO_STDOUT=1`
- `RAILS_SERVE_STATIC_FILES=1`
- `SECRET_KEY_BASE`
- `DATABASE_URL` (SQLite path, e.g. `sqlite3:/rails/storage/production.sqlite3`)
- Litestream credentials + bucket settings

Secrets rules:
- Store secrets via Kamal secrets mechanism (`.kamal/secrets`).
- Commit only variable names in `config/deploy.yml`, never secret values.
- Rotate credentials periodically and after incidents.

## Health Checks

Use a cheap, deterministic endpoint:
- `GET /up` should return 200 when app, DB file, and essential boot dependencies are ready.
- No external API calls in health check path.
- Keep response small and fast.

During deploy, Kamal should only shift traffic after healthy status.

## Zero-Downtime Deploys

Use rolling deploys with health checks:
- Build/push image.
- Start new container(s).
- Wait for health check pass.
- Shift traffic.
- Stop old container(s).

Operational rules:
- Run migrations in a deploy phase compatible with both old/new code.
- Avoid destructive schema changes in same deploy as code that still references old shape.
- Keep web and job process startup fast to reduce handover window.

## Rollback Procedures

When deploy is bad:

1. Roll back app image to last known good release (Kamal rollback).
2. Confirm `/up` passes and core user flow works.
3. If DB corruption/data-loss suspected, stop writes and restore from Litestream snapshot.
4. Redeploy stable image after restore and verification.

Keep rollback runbook tested; do not improvise during incident.

## Backup Verification

Backups are only real if restore works.

Verification cadence:
- Daily: check new replica objects are arriving in bucket.
- Weekly: restore latest backup into a disposable environment.
- Monthly: perform timed recovery drill and record RTO/RPO.

Example restore drill:

```bash
litestream restore -o /tmp/restore.sqlite3 s3://my-app-litestream/production.sqlite3
sqlite3 /tmp/restore.sqlite3 "PRAGMA integrity_check;"
```

Expect `ok` from integrity check. Then run a few read queries on critical tables.
