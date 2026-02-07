# Run using bin/ci
# Use --no-signoff to skip the gh signoff gate (for local dev before pushing)

CI.run do
  skip_signoff = ARGV.include?("--no-signoff")
  step "Setup", "bin/setup --skip-server"

  step "Style: Ruby", "bundle exec rubocop"
  step "Style: YAML", "yamllint ."

  step "Security: Bundler audit", "bundle exec bundle-audit check --update"
  step "Security: Brakeman", "bundle exec brakeman --exit-on-warn --no-pager"
  step "Security: Importmap audit", "bin/importmap audit"

  step "Tests: All", "bin/rails test:all"

  if success? && !skip_signoff
    step "Signoff: All systems go. Ready for merge and deploy.", "gh signoff"
  elsif !success?
    failure "Signoff: CI failed. Do not merge or deploy.", "Fix the issues and try again."
  end
end
