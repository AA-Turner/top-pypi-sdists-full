"""Agents callout content for the Customer Billing page.

Keep this in sync with the tools this page drives (see `_mcp_tools.py`) and the
skills/docs/playbooks that cover the same work. The "Agents callout" section of
the repo's `CONTRIBUTING.md` documents this upkeep.
"""

from __future__ import annotations

from airbyte_ops_webapp.pages.shared_components.agents_callout import (
    AgentLink,
    AgentsCalloutContent,
    AgentSection,
    mcp_tool_url,
    skill_url,
)

CUSTOMER_BILLING_AGENTS_CALLOUT = AgentsCalloutContent(
    title="🤖 Continue with an agent",
    intro=(
        "Everything on this page — finding an organization, reading its payment "
        "config, and setting grace periods, waivers, or usage overrides — an "
        "agent can do too. Name one of the tools, skills, or playbooks below to "
        "hand the work off or take it further."
    ),
    sections=[
        AgentSection(
            title="MCP Servers & Tools",
            intro="Airbyte Ops MCP (mcp.internal.airbyte.ai/ops-mcp).",
            links=[
                AgentLink(
                    "get_organization_payment_config",
                    href=mcp_tool_url(
                        "organization_admin",
                        "get_organization_payment_config",
                    ),
                    description="read an org's billing state",
                ),
                AgentLink(
                    "update_organization_payment_config",
                    href=mcp_tool_url(
                        "organization_admin",
                        "update_organization_payment_config",
                    ),
                    description="set grace period / waiver / usage override",
                ),
                AgentLink(
                    "lookup_customer_tiers",
                    href=mcp_tool_url("organization_admin", "lookup_customer_tiers"),
                    description="confirm tier before sensitive changes",
                ),
            ],
        ),
        AgentSection(
            title="Related Skills",
            intro="internal.airbyte.ai/skills",
            links=[
                AgentLink("escalate-to-human", href=skill_url("escalate-to-human")),
                AgentLink("lookup-team-member", href=skill_url("lookup-team-member")),
            ],
        ),
        AgentSection(
            title="Reference Docs",
            links=[
                AgentLink(
                    "Organization payment config",
                    href="https://github.com/airbytehq/airbyte-ops-mcp/blob/main/docs/organization-payment-config.md",
                ),
                AgentLink(
                    "Customer tiers & safety model",
                    href="https://github.com/airbytehq/airbyte-ops-mcp/blob/main/docs/customer-tiers.md",
                ),
            ],
        ),
        AgentSection(
            title="Playbooks",
            links=[
                AgentLink(
                    "customer_rca",
                    href="https://github.com/airbytehq/ai-skills/blob/main/devin/playbooks/customer_rca.md",
                ),
                AgentLink(
                    "support_ops_work_item",
                    href="https://github.com/airbytehq/ai-skills/blob/main/devin/playbooks/support_ops_work_item.md",
                ),
            ],
        ),
    ],
)
