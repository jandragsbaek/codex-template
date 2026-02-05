---
title: Multi-tenancy
read_when: "working with tenant-scoped data, adding models, or writing queries"
summary: "acts_as_tenant patterns, scoping rules, and testing with tenants."
---
# Multi-tenancy

We use `acts_as_tenant` for row-level tenant isolation. Every request runs in the context of one organization.

## Adding a New Tenanted Model

1. Add `organization_id` column with foreign key
2. Add `acts_as_tenant :organization` to the model
3. Add `belongs_to :organization` (acts_as_tenant handles scoping, but the association is still useful)
4. Add index on `organization_id`

```ruby
class Widget < ApplicationRecord
  acts_as_tenant :organization
end
```

## Scoping Rules

Default: All queries are scoped to `ActsAsTenant.current_tenant`. You don't need `where(organization: current_organization)`.

When to use unscoped:

- Cross-tenant admin queries (backoffice only)
- Background jobs that process multiple tenants
- Always wrap in `ActsAsTenant.without_tenant { ... }` or `ActsAsTenant.with_tenant(org) { ... }`

Never: Skip tenant scoping in user-facing controllers. This is a data isolation boundary.

## Setting the Tenant

Tenant is set in the controller layer:

```ruby
class AuthenticatedController < ApplicationController
  set_current_tenant_through_filter
  before_action :set_tenant

  private
    def set_tenant
      set_current_tenant(current_organization)
    end
end
```

## Testing with Tenants

Tests must set a tenant. Use fixtures:

```ruby
class ActiveSupport::TestCase
  setup do
    ActsAsTenant.current_tenant = organizations(:default)
  end

  teardown do
    ActsAsTenant.current_tenant = nil
  end
end
```

For tests that need a different tenant:

```ruby
test "scopes data to tenant" do
  ActsAsTenant.with_tenant(organizations(:other)) do
    assert_empty Widget.all
  end
end
```

## Common Mistakes

1. Forgetting `acts_as_tenant` on a new model — data leaks across orgs
2. Using `unscoped` in controllers — bypasses tenant isolation
3. Direct SQL queries — bypass `acts_as_tenant` scoping entirely
4. Background jobs without tenant context — must explicitly set tenant
