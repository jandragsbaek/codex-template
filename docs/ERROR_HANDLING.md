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

## Logging

- Log at warn for expected issues (email bounce, invalid input)
- Log at error for unexpected failures (timeout, nil where not expected)
- Include context (record ID, user ID, action) in log messages
