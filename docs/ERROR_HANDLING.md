---
title: Error handling
read_when: "adding error handling, rescue blocks, or external service integrations"
summary: "Exception strategy, retry policies, and resilience patterns."
---
# Error handling

## Exception Strategy

**Raise for programmer errors:**
```ruby
raise ArgumentError, "status must be one of: #{STATUSES}" unless STATUSES.include?(status)
```

**Handle expected failures gracefully:**
```ruby
def deliver_email
  PostmarkClient.deliver(message)
rescue Postmark::ApiInputError => e
  Rails.logger.warn("Postmark rejected message: #{e.message}")
rescue Net::OpenTimeout, Net::ReadTimeout => e
  Rails.logger.error("Postmark timeout: #{e.message}")
  raise # Let Solid Queue retry
end
```

**Never swallow exceptions silently:**
```ruby
# Bad
begin
  do_something
rescue => e
  # silence
end

# Good
begin
  do_something
rescue SpecificError => e
  Rails.logger.error("Context: #{e.message}")
end
```

## Job Retry Policy

```ruby
class ImportantJob < ApplicationJob
  retry_on Net::OpenTimeout, wait: :polynomially_longer, attempts: 5
  discard_on ActiveRecord::RecordNotFound

  def perform(record)
    record.process_now
  end
end
```

## External Service Resilience

1. Timeout everything — set connect and read timeouts
2. Retry transient failures — network errors, 5xx responses
3. Don't retry client errors — 4xx means our request is wrong
4. Degrade gracefully — if email fails, don't block incident creation

## Controller Error Handling

```ruby
class ApplicationController < ActionController::Base
  rescue_from ActiveRecord::RecordNotFound, with: :not_found
  rescue_from ActiveRecord::StaleObjectError, with: :conflict

  private
    def not_found
      render "errors/not_found", status: :not_found
    end

    def conflict
      redirect_back fallback_location: root_path,
        alert: "Record was updated by someone else. Please try again."
    end
end
```

## APM Integration (AppSignal / Sentry)

Both AppSignal and Sentry auto-capture unhandled exceptions via Rack middleware. But when you rescue an exception (in controllers, models, or jobs), it never reaches the middleware — so the APM tool never sees it.

**Rule: If you rescue and handle an error gracefully, still report it to APM if it's unexpected or worth tracking.**

### In controllers (rescue_from)

```ruby
class ApplicationController < ActionController::Base
  rescue_from ActiveRecord::StaleObjectError, with: :conflict

  private
    def conflict(exception)
      report_error(exception) # Rails 7.1+ built-in, sends to registered error reporters
      redirect_back fallback_location: root_path,
        alert: "Record was updated by someone else. Please try again."
    end
end
```

### In models or services

```ruby
def deliver_email
  PostmarkClient.deliver(message)
rescue Net::OpenTimeout, Net::ReadTimeout => e
  Rails.error.report(e, handled: true, context: { message_id: message.id })
  raise # Re-raise for job retry
end
```

### In jobs

```ruby
class ImportantJob < ApplicationJob
  retry_on Net::OpenTimeout, wait: :polynomially_longer, attempts: 5

  def perform(record)
    record.process_now
  rescue => e
    Rails.error.report(e, handled: false, context: { record_id: record.id })
    raise # Let retry_on handle it
  end
end
```

### Which method to use

| Method                                | When                                             |
| ------------------------------------- | ------------------------------------------------ |
| Don't rescue (let it bubble)          | Unexpected errors — APM captures automatically   |
| Rails.error.report(e, handled: true)  | You handle it gracefully but want visibility     |
| Rails.error.report(e, handled: false) | You're about to re-raise but want to add context |
| Rails.error.handle { ... }            | Wrap a block, swallow errors, report to APM      |

### Rails error reporter setup

Rails 7.1+ has Rails.error which forwards to all registered subscribers. Both AppSignal and Sentry register automatically when their gems are loaded. Prefer Rails.error.report over vendor-specific calls (Appsignal.send_error, Sentry.capture_exception) to stay vendor-neutral.

### What NOT to do

```ruby
# Bad — exception is lost, APM never sees it
rescue => e
  Rails.logger.error(e.message)
end

# Bad — vendor lock-in
rescue => e
  Appsignal.send_error(e)
end

# Good — vendor-neutral, works with any APM
rescue => e
  Rails.error.report(e, handled: true)
end
```

## Logging

- Log at warn for expected issues (email bounce, invalid input)
- Log at error for unexpected failures (timeout, nil where not expected)
- Include context (record ID, user ID, action) in log messages
