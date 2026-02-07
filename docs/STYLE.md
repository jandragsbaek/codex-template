---
title: Code Style
read_when: "editing Ruby style rules or linting configuration"
summary: "Readable Ruby style rules and lint baseline."
---
# Code Style

We aim to write code that is a pleasure to read.

## Lint baseline

Use **rubocop-rails-omakase** across the project. It runs via `bin/ci` (or `bin/gate`) as a required check.

Zero violations in CI. No exceptions, no `rubocop:disable` unless justified in a comment.

## Conditional Returns

Prefer expanded conditionals over guard clauses:

```ruby
# Preferred
def todos_for_new_group
  if ids = params.require(:todolist)[:todo_ids]
    @bucket.recordings.todos.find(ids.split(","))
  else
    []
  end
end
```

**Exception**: Guard clauses at method start for non-trivial bodies:
```ruby
def after_recorded_as_commit(recording)
  return if recording.parent.was_created?
  
  if recording.was_created?
    broadcast_new_column(recording)
  else
    broadcast_column_change(recording)
  end
end
```

## Method Ordering

1. `class` methods
2. `public` methods (`initialize` at top)
3. `private` methods

Order methods vertically by invocation order.

## Visibility Modifiers

No newline under visibility modifiers; indent content:

```ruby
class SomeClass
  def some_method
    # ...
  end

  private
    def some_private_method
      # ...
    end
end
```

## Bang Methods

Use `!` only for methods with non-`!` counterparts. Don't use `!` for destructive actions alone.

## CRUD Controllers

Model endpoints as CRUD on resources:

```ruby
# Bad
resources :cards do
  post :close
  post :reopen
end

# Good
resources :cards do
  resource :closure
end
```

## Nested Controller Naming

When extracting custom actions into resource controllers, follow this naming convention:

**File path:** `app/controllers/<parent>/<resource>_controller.rb`
**Class name:** `<Parent>::<Resource>Controller`
**Concern path:** `app/models/<parent>/<concern_name>.rb`

Examples:

| Custom action | Resource controller | Method |
|---|---|---|
| `IncidentsController#complete` | `Incidents::CompletionsController` | `#create` |
| `IncidentsController#reopen` | `Incidents::CompletionsController` | `#destroy` |
| `TeamsController#update_status` | `Teams::StatusesController` | `#update` |
| `TeamsController#deactivate` | `Teams::ActivationsController` | `#destroy` |
| `TeamsController#reactivate` | `Teams::ActivationsController` | `#create` |

**Route pattern:**
```ruby
resources :incidents do
  resource :completion, only: [:create, :destroy]
end
```

## Controller ↔ Model Interaction

Thin controllers, rich domain models. No service layers for simple ops:

```ruby
class Cards::CommentsController < ApplicationController
  def create
    @comment = @card.comments.create!(comment_params)
  end
end
```

For complex behavior, use intention-revealing model APIs:

```ruby
class Cards::GoldnessesController < ApplicationController
  def create
    @card.gild
  end
end
```

## Background Jobs

Thin jobs delegating to models:

```ruby
module Event::Relaying
  def relay_later
    Event::RelayJob.perform_later(self)
  end

  def relay_now
    # actual logic
  end
end

class Event::RelayJob < ApplicationJob
  def perform(event)
    event.relay_now
  end
end
```
