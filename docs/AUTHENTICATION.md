---
title: Authentication
read_when: "Use when adding user authentication."
summary: "Rails 8 session-based authentication patterns with simple authorization and tenant safety."
---
# Authentication

Rails-first auth: generated, session-based, minimal moving parts.

See also:
- `docs/MULTI_TENANCY.md` for tenant scoping rules.
- `docs/PRINCIPLES.md` for Rails-first architecture/testing defaults.

## Start with Rails 8 Generator

Generate baseline auth:

```bash
bin/rails generate authentication
bin/rails db:migrate
```

Generator adds core pieces:
- `User`, `Session`, `Current` models
- `SessionsController`
- `Authentication` concern
- `PasswordsController` + mailer/views (reset flow)
- session + password routes

Use generator as baseline. Customize in app code; do not replace with heavy auth framework by default.

## Session-Based Auth (Not JWT)

Default Rails 8 pattern:
- Cookie-backed session id (`cookies.signed[:session_id]`)
- Server-side `sessions` table linked to `user`
- `Current.session` for request context

Why this default:
- Works naturally with Rails controllers, CSRF protections, and browser flows.
- Supports server-side session invalidation.
- Lower complexity than rolling JWT lifecycle/rotation/revocation.

JWT can fit API-specific constraints, but web app default here is session auth.

## `Current.user` Pattern

Use `Current` as per-request auth context:

```ruby
class Current < ActiveSupport::CurrentAttributes
  attribute :session
  delegate :user, to: :session, allow_nil: true
end
```

In auth concern:
- resume `Current.session` from signed cookie
- expose `authenticated?`
- redirect to sign-in when missing session

Prefer `Current.user` in controllers/views/policies over repeatedly re-querying user from params/cookies.

## Authorization Patterns (Keep It Simple)

Default approach:
- Keep coarse checks in controller concerns (`admin_access_only`, `authenticated?`).
- Keep domain rules in model methods (close to business logic).
- Prefer simple role flags or membership checks first.

Avoid introducing complex authorization gems unless requirements clearly justify it (deep policy matrix, externalized authorization, etc.).

## Multi-Tenant Considerations

Authentication must never bypass tenant boundaries.

Patterns:
- Scope user access through current tenant/account (`Current.user` + `Current.account`/tenant context).
- Ensure session user belongs to active account before granting access.
- For row-level tenancy (`acts_as_tenant`), set tenant in authenticated base controller.
- Never run user-facing requests with tenant scoping disabled.

Common shape:
- `User` belongs to one `Account`, or
- `Membership` join model (`User` <-> `Account`) with selected active account in session.

## Password Reset Flow

Rails generator includes:
- `PasswordsController` (`new/create/edit/update`)
- `PasswordsMailer` with reset link
- token-based reset route (`resources :passwords, param: :token`)

Expected behavior:
- “Forgot password?” on sign-in form
- email with short-lived reset token (default 15 minutes in Rails docs)
- update password via tokenized reset form
- generic responses to avoid account enumeration

## Rate Limiting Login Attempts

Add controller-level rate limiting on session creation:

```ruby
class SessionsController < ApplicationController
  rate_limit to: 10, within: 3.minutes, only: :create,
    with: -> { redirect_to new_session_url, alert: "Try again later." }
end
```

Also recommended:
- generic login failure message ("email or password incorrect")
- same generic response on forgot-password submission
- optional CAPTCHA escalation after repeated failures

## Practical Defaults Checklist

- Use `bin/rails generate authentication`
- Keep session-based auth for browser app paths
- Use `Current.user` as request identity
- Keep authorization simple + explicit
- Enforce tenant membership on every authenticated request
- Keep reset flow enabled and tested
- Rate-limit login and reset endpoints
