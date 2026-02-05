---
title: Core Principles
read_when: "making architecture or testing tradeoffs"
summary: "Vanilla Rails principles and testing posture."
---
# Core Principles

1. **"Vanilla Rails is plenty"** — Trust the framework, minimize dependencies
2. **Rich domain models** — Models expose natural language APIs (`recording.incinerate`)
3. **Controllers talk directly to models** — No intermediary layers for simple operations
4. **Concerns for organization** — Group by domain concept, delegate complex work to POROs
5. **Everything is CRUD** — Create new controllers rather than custom actions
6. **Minitest + Fixtures** — Fast, simple, built into Rails
7. **Model and controller tests over system tests** — System tests for smoke tests only
8. **Database-backed infrastructure** — Solid Queue/Cache/Cable eliminate Redis
9. **Hotwire for interactivity** — HTML over the wire, minimal JavaScript
10. **Build small things first** — Don't abstract until you have a reason
11. **Convention over configuration** — Follow Rails defaults whenever possible
12. **Authorization in models** — Permission logic lives close to domain, not in policy classes
13. **Human testing for UI feel** — Automation tests logic, humans test experience

---

> *"Every single time I've regretted the state of my controllers, it's been because I've had too few of them."* — DHH

> *"System tests remain as slow, brittle, and full of false negatives as they did a decade ago..."* — DHH
