---
title: Testing
read_when: "Use when writing tests or setting up test infrastructure."
summary: "Minitest + Fixtures conventions for fast, deterministic Rails tests."
---
# Testing

Rails-first posture: Minitest + Fixtures, minimal ceremony, fast feedback.

See also:
- `docs/PRINCIPLES.md` for overall testing philosophy.
- `docs/ARCHITECTURE.md` for expected `test/` and `fixtures/` layout.

## Why Minitest over RSpec

- Rails default. Zero extra framework layer.
- Faster startup + execution in typical Rails apps.
- Simpler syntax. Easier onboarding. Fewer DSL surprises.
- Better fit for vanilla Rails: less indirection, fewer custom helpers.

Use RSpec only with a strong project-specific reason.

## Why Fixtures over FactoryBot

- Deterministic data. Same records every run.
- Fast. YAML load once; avoid deep factory graph build cost.
- Lower flake risk. No accidental N+1 factory chains in setup.
- Clear shared test vocabulary (`users(:jan)`, `projects(:active)`).

Use fixtures as baseline test data. Build ad-hoc records only when test intent is clearer that way.

## Fixture Organization Patterns

- One fixture file per model (`test/fixtures/users.yml`, `test/fixtures/projects.yml`).
- Keep records realistic: names, states, timestamps matching real workflows.
- Prefer small, reusable sets over giant fixture dumps.
- Name fixtures by role/outcome, not random IDs (`:owner`, `:archived_project`).
- Keep associations explicit via fixture references.

Example:

```yaml
# test/fixtures/projects.yml
active_project:
  account: basecamp
  name: "Roadmap"
  archived: false

archived_project:
  account: basecamp
  name: "Legacy"
  archived: true
```

## Test File Structure (Mirror `app/`)

Mirror app structure to keep navigation obvious:

```text
app/models/card.rb                  -> test/models/card_test.rb
app/controllers/cards_controller.rb -> test/controllers/cards_controller_test.rb
app/jobs/event/relay_job.rb         -> test/jobs/event/relay_job_test.rb
app/system/cards_test.rb            -> test/system/cards_test.rb
```

Rules:
- Add tests beside every new model/controller/job behavior change.
- Keep system tests for smoke flows; cover business logic in model/controller tests.
- Keep helper methods local to the test class unless broadly shared.

## System Tests with Capybara

Use system tests to verify critical end-to-end flows only:

- Sign-in + key happy path.
- High-risk UI flows (checkout, publish, destructive actions).
- Cross-browser details only when product requirements demand it.

Avoid covering every edge in system tests. Push edge coverage down to model/controller tests for speed and reliability.

## Testing Turbo + Stimulus Interactions

### Turbo

- For Turbo Stream responses, assert stream template/action + updated state.
- For Turbo Frame navigation, assert key frame content and fallback HTML behavior.
- Prefer integration/system tests over brittle HTML string snapshots.

Example checks:
- `assert_response :success`
- `assert_equal "New title", record.reload.title`
- `assert_select "turbo-frame#card_#{record.id}"`

### Stimulus

- Test Stimulus behavior through user-visible outcomes in system tests.
- Assert DOM/state changes after user actions (`click_on`, `fill_in`, `assert_text`, `assert_selector`).
- Avoid over-investing in JS-unit-style tests when behavior is already covered through browser-level flow.

## Coverage Expectations + `bin/coverage_insights`

Expectations:
- Every state-changing model method: tests.
- Every controller action: integration test.
- System tests: smoke coverage only.
- New feature or bug fix ships with matching test updates.

Use coverage tooling to target gaps with highest impact:

```bash
bin/rails test
bin/coverage_insights
```

`bin/coverage_insights` highlights weak spots and prioritizes what to test next. Use it to guide incremental coverage, not to chase vanity percentages.

## Example: Controller Action with Fixtures

```ruby
# test/controllers/projects_controller_test.rb
require "test_helper"

class ProjectsControllerTest < ActionDispatch::IntegrationTest
  test "updates project and persists change" do
    project = projects(:active_project)

    patch project_path(project), params: { project: { name: "Q2 Roadmap" } }

    assert_redirected_to project_path(project)
    assert_equal "Q2 Roadmap", project.reload.name
  end
end
```

## Example: Model Validations + Associations with Fixtures

```ruby
# test/models/project_test.rb
require "test_helper"

class ProjectTest < ActiveSupport::TestCase
  test "requires name" do
    project = Project.new(account: accounts(:basecamp), name: nil)

    assert_not project.valid?
    assert_includes project.errors[:name], "can't be blank"
  end

  test "belongs to account" do
    project = projects(:active_project)

    assert_equal accounts(:basecamp), project.account
  end
end
```
