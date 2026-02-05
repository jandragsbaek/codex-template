---
title: Concurrency
read_when: "adding real-time features, ActionCable channels, or handling concurrent writes"
summary: "Patterns for real-time updates, concurrent writes, and WebSocket channels."
---
# Concurrency

## Turbo Streams vs ActionCable

| Use case | Mechanism | Example |
|---|---|---|
| Response to current user's action | Turbo Stream response | Creating an incident |
| All users see an update | Model broadcast callback | New incident appears for all operators |
| Scoped live feed | ActionCable channel | Incidents channel per event |

## Broadcasting Pattern

Use model concerns for broadcast logic:

```ruby
# app/models/incident/status_broadcaster.rb
module Incident::StatusBroadcaster
  extend ActiveSupport::Concern

  included do
    after_update_commit :broadcast_status_change, if: :saved_change_to_status?
  end

  private
    def broadcast_status_change
      broadcast_replace_to(
        [event, :incidents],
        target: dom_id(self),
        partial: "incidents/incident"
      )
    end
end
```

## Channel Scoping

Scope channels to the narrowest context:

```ruby
# Good — scoped to event
class IncidentsChannel < ApplicationCable::Channel
  def subscribed
    stream_for [current_organization, event]
  end
end

# Bad — organization-wide (too broad, unnecessary traffic)
class IncidentsChannel < ApplicationCable::Channel
  def subscribed
    stream_for current_organization
  end
end
```

## Concurrent Writes

For records multiple users may edit simultaneously:

1. Add `lock_version` column (optimistic locking)
2. Handle `ActiveRecord::StaleObjectError` in controller
3. Show user a conflict message with option to reload

```ruby
def update
  @incident.update!(incident_params)
rescue ActiveRecord::StaleObjectError
  redirect_to @incident, alert: "Someone else updated this record. Please review and try again."
end
```

## Offline / Reconnection

Assume connections will drop. Design for it:

- UI must work without WebSockets (degrade to page refresh)
- On reconnect, Turbo re-establishes streams automatically
- For critical data, add a "last updated" timestamp visible to users
- Never assume a broadcast was received by all clients
