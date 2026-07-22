"""Agents callout content for the MotherDuck Diagnostics page.

Keep this in sync with the tools this page drives (see `_mcp_tools.py` and the
Ops MCP `motherduck_diagnostics` tools) and the skills/docs that cover the same
work. The "Agents callout" section of the repo's `CONTRIBUTING.md` documents
this upkeep.
"""

from __future__ import annotations

from airbyte_ops_webapp.pages.shared_components.agents_callout import (
    AgentLink,
    AgentsCalloutContent,
    AgentSection,
    mcp_tool_url,
    skill_url,
)

MOTHERDUCK_DIAGNOSTICS_AGENTS_CALLOUT = AgentsCalloutContent(
    title="🤖 Continue with an agent",
    intro=(
        "Everything on this page — compute-usage trends, recent / failed / slow "
        "queries, and live server connections — an agent can pull too. Name one "
        "of the tools, skills, or docs below to keep the analysis going."
    ),
    sections=[
        AgentSection(
            title="MCP Servers & Tools",
            intro="Airbyte Ops MCP (mcp.internal.airbyte.ai/ops-mcp).",
            links=[
                AgentLink(
                    "query_motherduck_queries",
                    href=mcp_tool_url("context_store_ops", "query_motherduck_queries"),
                    description="recent / failed / slow query history",
                ),
                AgentLink(
                    "query_motherduck_active_connections",
                    href=mcp_tool_url(
                        "context_store_ops", "query_motherduck_active_connections"
                    ),
                    description="live server connections",
                ),
            ],
        ),
        AgentSection(
            title="Related Skills",
            intro="internal.airbyte.ai/skills",
            links=[
                AgentLink(
                    "check-datadog-metrics",
                    href=skill_url("check-datadog-metrics"),
                ),
                AgentLink("check-sentry-errors", href=skill_url("check-sentry-errors")),
            ],
        ),
        AgentSection(
            title="Reference Docs",
            links=[
                AgentLink(
                    "MotherDuck Diagnostics",
                    href="https://github.com/airbytehq/airbyte-ops-mcp/blob/main/airbyte-ops-webapp/docs/motherduck-diagnostics.md",
                ),
                AgentLink(
                    "Ops MCP authentication",
                    href="https://github.com/airbytehq/airbyte-ops-mcp/blob/main/docs/authentication.md",
                ),
            ],
        ),
    ],
)
