"""Agents callout content for the Data Worker Allocation page."""

from __future__ import annotations

from airbyte_ops_webapp.pages.platform_admin.agents import PLATFORM_CONFIG_API_SPEC
from airbyte_ops_webapp.pages.shared_components.agents_callout import (
    AgentLink,
    AgentsCalloutContent,
    AgentSection,
)

DATA_WORKER_ALLOCATION_AGENTS_CALLOUT = AgentsCalloutContent(
    title="🤖 Continue with an agent",
    intro="An agent can continue this organization capacity operation.",
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
