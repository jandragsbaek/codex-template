---
title: Architecture
read_when: "planning app structure or refactoring architecture"
summary: "Vanilla Rails directory layout and patterns to avoid."
---
# Architecture

Vanilla Rails approach: maximize Rails built-ins, minimize dependencies.

## Directory Structure

```
app/
├── controllers/
│   ├── concerns/           # Shared controller behaviors
│   ├── cards/              # Nested resource controllers
│   └── boards/             # Sub-controllers for resources
├── models/
│   ├── concerns/           # Common model concerns
│   ├── card/               # Model-specific concerns (Card::Closeable, etc.)
│   └── current.rb          # CurrentAttributes for request context
├── views/
│   ├── cards/              # Partials, turbo streams
│   └── layouts/
├── javascript/
│   └── controllers/        # Stimulus controllers only
├── helpers/                # View helpers
├── jobs/                   # Thin job classes delegating to models
└── mailers/
config/
├── recurring.yml           # Solid Queue scheduled jobs
└── importmap.rb            # ES module imports (no bundler)
test/
├── models/                 # Unit tests
├── controllers/            # Integration tests
├── system/                 # Capybara/Selenium tests (smoke only)
└── fixtures/               # YAML fixtures (NOT factories)
```

## Eliminated Patterns

| Enterprise Rails            | Vanilla Rails             |
|-----------------------------|---------------------------|
| Service objects, interactors| Rich domain models        |
| RSpec + FactoryBot          | Minitest + Fixtures       |
| Pundit/CanCanCan policies   | Model methods             |
| Sidekiq + Redis             | Solid Queue + database    |
| ViewComponents              | ERB partials + helpers    |
| dry-rb gems                 | Rails built-ins           |
| Repository pattern          | Direct ActiveRecord       |

**Directories that should not exist**:
- `app/services/`
- `app/interactors/`
- `app/commands/`
- `app/use_cases/`
- `app/policies/`
- `spec/`

## Nested resource controllers

Prefer nested controllers under the parent resource to avoid custom member actions:

```
app/controllers/backoffice/crm/organizations/
  roles_controller.rb
  statuses_controller.rb
  follow_ups_controller.rb
  system_links_controller.rb
```
