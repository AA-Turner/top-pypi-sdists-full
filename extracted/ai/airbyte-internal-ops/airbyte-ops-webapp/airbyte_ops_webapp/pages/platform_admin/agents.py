"""Agents callout content for the Platform Admin page."""

from __future__ import annotations

from airbyte_ops_webapp.pages.shared_components.agents_callout import (
    AgentLink,
    AgentsCalloutContent,
    AgentSection,
)

PLATFORM_CONFIG_API_SPEC = (
    "https://github.com/airbytehq/airbyte-platform-internal/blob/master/"
    "oss/airbyte-api/server-api/src/main/openapi/config.yaml"
)

PLATFORM_ADMIN_AGENTS_CALLOUT = AgentsCalloutContent(
    title="🤖 Continue with an agent",
    intro="An agent can continue these instance-admin operations against the Config API.",
    sections=[
        AgentSection(
            title="Reference Docs",
            links=[
                AgentLink(
                    "Config API spec (data_worker_allocation)",
                    href=PLATFORM_CONFIG_API_SPEC,
                )
            ],
        )
    ],
)
