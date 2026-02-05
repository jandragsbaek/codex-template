---
title: Performance
read_when: "optimizing queries, adding eager loading, or setting performance expectations"
summary: "Performance baselines, N+1 prevention, and query budgets."
---
# Performance

## Baselines

Target response times for HTML requests:

| Type | Target | Alarm |
|---|---|---|
| Simple page load | < 100ms | > 300ms |
| Complex page (dashboard) | < 200ms | > 500ms |
| Turbo Stream response | < 50ms | > 150ms |
| API JSON response | < 50ms | > 200ms |

These are server-side times. Network latency is additional.

## Query Budget

- **< 10 queries per request** for simple pages
- **< 20 queries per request** for complex pages
- **0 N+1 queries** — always

## Preventing N+1 Queries

```ruby
# Good
@incidents = @event.incidents.includes(:user, :activity_type, timeline_items: :user)

# Bad — loads user for each incident in the view
@incidents = @event.incidents
```

## Caching

Use Solid Cache (database-backed):

```ruby
def activity_type_breakdown
  Rails.cache.fetch([event, "breakdown", updated_at], expires_in: 5.minutes) do
    calculate_breakdown
  end
end
```

## ActionCable Broadcast Payloads

Keep broadcasts small:

```ruby
# Good — render just the changed partial
broadcast_replace_to channel, target: dom_id(self), partial: "incidents/incident"

# Bad — render the entire page
broadcast_replace_to channel, target: "main", partial: "incidents/index"
```

## Background Job Performance

- Keep job execution under 30 seconds
- For long-running work, split into smaller jobs
- Use `perform_later` — never block the request
