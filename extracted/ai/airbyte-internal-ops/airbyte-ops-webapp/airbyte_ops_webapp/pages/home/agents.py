"""Agents callout content for the Airbyte Ops home page.

The home callout is broader than the per-tool ones: it points at the Ops MCP
server as a whole and the shared skills / docs / playbook indexes, since the home
page is the entry point rather than a single workflow. Keep it in sync with the
repo docs it links to; see the "Agents callout" section of the repo's
`CONTRIBUTING.md`.
"""

from __future__ import annotations

from airbyte_ops_webapp.pages.shared_components.agents_callout import (
    MCP_TOOL_DOCS_URL,
    SKILLS_INDEX_URL,
    AgentLink,
    AgentsCalloutContent,
    AgentSection,
    skill_url,
)

HOME_AGENTS_CALLOUT = AgentsCalloutContent(
    title="🤖 Continue with an agent",
    intro=(
        "Every Airbyte Ops workflow here is also drivable by an agent through the "
        "Airbyte Ops MCP server. Point your agent at the server and the skills, "
        "docs, and playbooks below, then open a specific tool for its own agent "
        "hand-off options."
    ),
    sections=[
        AgentSection(
            title="MCP Servers & Tools",
            links=[
                AgentLink(
                    "Airbyte Ops MCP",
                    href="https://mcp.internal.airbyte.ai/ops-mcp",
                    description="connector versions, rollouts, billing, diagnostics",
                ),
                AgentLink(
                    "Tool reference",
                    href=f"{MCP_TOOL_DOCS_URL}.html",
                    description="per-tool docs for every Ops MCP tool",
                ),
            ],
        ),
        AgentSection(
            title="Related Skills",
            links=[
                AgentLink("Skills index", href=SKILLS_INDEX_URL),
                AgentLink(
                    "mcp-ui-development-testing",
                    href=skill_url("mcp-ui-development-testing"),
                ),
            ],
        ),
        AgentSection(
            title="Reference Docs",
            links=[
                AgentLink(
                    "Ops MCP README",
                    href="https://github.com/airbytehq/airbyte-ops-mcp/blob/main/README.md",
                ),
                AgentLink(
                    "AGENTS.md",
                    href="https://github.com/airbytehq/airbyte-ops-mcp/blob/main/AGENTS.md",
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
                    "ai-skills playbooks",
                    href="https://github.com/airbytehq/ai-skills/tree/main/devin/playbooks",
                ),
            ],
        ),
    ],
)
