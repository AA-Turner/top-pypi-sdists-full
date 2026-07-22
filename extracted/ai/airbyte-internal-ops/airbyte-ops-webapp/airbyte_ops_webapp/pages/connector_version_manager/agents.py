"""Agents callout content for the Connector Version Manager page.

Keep this in sync with the tools this page actually drives (see
`_mcp_tools.py`) and the skills/docs/playbooks that cover the same work. The
"Agents callout" section of the repo's `CONTRIBUTING.md` documents this upkeep.
"""

from __future__ import annotations

from airbyte_ops_webapp.pages.shared_components.agents_callout import (
    AgentLink,
    AgentsCalloutContent,
    AgentSection,
    mcp_tool_url,
    skill_url,
)

CONNECTOR_VERSION_MANAGER_AGENTS_CALLOUT = AgentsCalloutContent(
    title="🤖 Continue with an agent",
    intro=(
        "Everything on this page — searching connectors, inspecting version and "
        "pin state, setting scoped overrides, driving rollouts, and yanking bad "
        "versions — an agent can do too. Name one of the tools, skills, or "
        "playbooks below to have your agent pick up the work or take it further."
    ),
    sections=[
        AgentSection(
            title="MCP Servers & Tools",
            intro="Airbyte Ops MCP (mcp.internal.airbyte.ai/ops-mcp).",
            links=[
                AgentLink(
                    "get_cloud_connector_version",
                    href=mcp_tool_url(
                        "connector_versions", "get_cloud_connector_version"
                    ),
                    description="read live version & pin state",
                ),
                AgentLink(
                    "set_cloud_connector_version_override",
                    href=mcp_tool_url(
                        "connector_versions",
                        "set_cloud_connector_version_override",
                    ),
                    description="pin at actor / workspace / org scope",
                ),
                AgentLink(
                    "start_connector_rollout",
                    href=mcp_tool_url("connector_versions", "start_connector_rollout"),
                    description="begin a progressive rollout",
                ),
                AgentLink(
                    "progress_connector_rollout",
                    href=mcp_tool_url(
                        "connector_versions", "progress_connector_rollout"
                    ),
                    description="advance rollout to the next tier",
                ),
                AgentLink(
                    "finalize_connector_rollout",
                    href=mcp_tool_url(
                        "connector_versions", "finalize_connector_rollout"
                    ),
                    description="complete or roll back",
                ),
                AgentLink(
                    "yank_connector_version",
                    href=mcp_tool_url("connector_registry", "yank_connector_version"),
                    description="withdraw a bad version (or restore with unyank=true)",
                ),
                AgentLink(
                    "lookup_customer_tiers",
                    href=mcp_tool_url("organization_admin", "lookup_customer_tiers"),
                    description="check tier before sensitive ops",
                ),
            ],
        ),
        AgentSection(
            title="Related Skills",
            intro="internal.airbyte.ai/skills",
            links=[
                AgentLink(
                    "connector-version-pinning",
                    href=skill_url("connector-version-pinning"),
                ),
                AgentLink(
                    "progressive-connector-rollouts",
                    href=skill_url("progressive-connector-rollouts"),
                ),
                AgentLink(
                    "yank-connector-version",
                    href=skill_url("yank-connector-version"),
                ),
                AgentLink(
                    "publish-connector-prerelease",
                    href=skill_url("publish-connector-prerelease"),
                ),
                AgentLink(
                    "connector-regression-tests",
                    href=skill_url("connector-regression-tests"),
                ),
            ],
        ),
        AgentSection(
            title="Reference Docs",
            links=[
                AgentLink(
                    "Customer tiers & safety model",
                    href="https://github.com/airbytehq/airbyte-ops-mcp/blob/main/docs/customer-tiers.md",
                ),
                AgentLink(
                    "Managing breaking changes in connectors",
                    href="https://docs.airbyte.com/platform/connector-development/connector-metadata-file",
                ),
                AgentLink(
                    "Ops MCP authentication",
                    href="https://github.com/airbytehq/airbyte-ops-mcp/blob/main/docs/authentication.md",
                ),
            ],
        ),
        AgentSection(
            title="Playbooks",
            links=[
                AgentLink(
                    "slack_connector_progressive_rollout",
                    href="https://github.com/airbytehq/ai-skills/blob/main/devin/playbooks/slack_connector_progressive_rollout.md",
                ),
                AgentLink(
                    "canary_prerelease",
                    href="https://github.com/airbytehq/ai-skills/blob/main/devin/playbooks/canary_prerelease.md",
                ),
            ],
        ),
    ],
)
