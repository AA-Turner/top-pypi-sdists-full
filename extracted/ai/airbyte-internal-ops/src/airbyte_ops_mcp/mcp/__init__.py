"""MCP tools organized by functional domain.

This package contains all MCP tool implementations organized by module name.
Domain is automatically inferred from the file stem where tools are defined:
- `connector_versions`: cloud version overrides, rollouts, pre-release publish
- `connector_registry`: registry reads/yank plus monorepo list/bump
- `connector_qa`: regression tests and release blocking
- `connection_medic`: connection state/catalog reads plus emergency writes
- `prod_db_ops`: Prod Cloud DB-replica SQL queries
- `logging`: GCP Cloud Logging backend-error lookup
- `context_store_ops`: MotherDuck / context-store diagnostics
- `organization_admin`: is_agentic flag, payment config, customer tiers
- `github_ops`: CI workflow trigger/status, Docker image info, subscriptions
- `human_in_the_loop`: human escalation, team-roster lookup, Slack newsletter posting
- `devin_ops`: reminders, secret requests, session feedback and naming
- `prompts`: prompt templates for common workflows
"""
