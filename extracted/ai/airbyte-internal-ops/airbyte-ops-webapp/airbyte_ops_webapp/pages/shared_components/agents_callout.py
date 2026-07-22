"""Shared "Continue with an agent" callout dialog.

Every operational Ops Webapp page (auth-only screens excepted) carries a 🤖
button whose tooltip reads *Continue with an agent*. Clicking it opens a wide
modal that explains that everything the page does by hand can also be driven by
(or handed off to) an agent, and points at the off-page materials that let an
agent pick up the work: the MCP servers and
tools behind the page, related skills on `internal.airbyte.ai/skills`, reference
docs, and playbooks.

The content is data, not markup: each page declares an `AgentsCalloutContent`
(intro prose plus a few `AgentSection`s of `AgentLink`s) and passes it to
`render_agents_callout`, so every page shares one visual language and structure
while the copy stays page-specific. Keep page content current per the
"Agents callout" section of the repo's `CONTRIBUTING.md`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from prefab_ui.components import (
    H4,
    Button,
    Column,
    Dialog,
    Div,
    Grid,
    Link,
    Muted,
    Row,
    Text,
    Tooltip,
)

AGENTS_CALLOUT_BUTTON_LABEL = "🤖 / ℹ️"  # noqa: RUF001
"""Label on the callout trigger button: robot paired with an info glyph."""

AGENTS_CALLOUT_TOOLTIP = "Continue with an agent"
"""Hover text shared by the trigger button on every page."""

SKILLS_INDEX_URL = "https://internal.airbyte.ai/skills"
"""Base URL for the shared skills index; anchors are `#<skill-name>`."""

MCP_TOOL_DOCS_URL = "https://airbytehq.github.io/airbyte-ops-mcp/airbyte_ops_mcp/mcp"
"""Base URL for the pdoc-generated Ops MCP tool reference."""


def skill_url(skill_name: str) -> str:
    """Return the `internal.airbyte.ai/skills#<skill-name>` deep link."""
    return f"{SKILLS_INDEX_URL}#{skill_name}"


def mcp_tool_url(module: str, tool: str) -> str:
    """Return the pdoc deep link for an Ops MCP `tool` in `mcp/<module>.py`.

    Resolves to `.../mcp/<module>.html#<tool>`, e.g.
    `mcp_tool_url("context_store_ops", "query_motherduck_queries")`.
    """
    return f"{MCP_TOOL_DOCS_URL}/{module}.html#{tool}"


@dataclass(frozen=True)
class AgentLink:
    """A single labeled entry inside a callout section.

    `href` is optional so a section can list a name to say aloud to an agent
    (e.g. a skill slug or MCP tool) even when there is no page to link to.
    `description` is an optional short gloss shown after the label.
    """

    label: str
    href: str = ""
    description: str = ""


@dataclass(frozen=True)
class AgentSection:
    """A titled group of `AgentLink`s (e.g. *MCP Servers & Tools*)."""

    title: str
    intro: str = ""
    links: list[AgentLink] = field(default_factory=list)


@dataclass(frozen=True)
class AgentsCalloutContent:
    """Full content for one page's Agents callout dialog."""

    title: str
    intro: str
    sections: list[AgentSection] = field(default_factory=list)


def render_agents_callout(content: AgentsCalloutContent) -> None:
    """Render the 🤖 trigger button and its "Continue with an agent" dialog.

    Place this in the page hero's actions area. The trigger is a compact emoji
    button with a shared tooltip; the dialog body uses most of the page width
    and lays the sections out in a responsive grid.
    """
    with Dialog(
        title=content.title,
        description=content.intro,
        name="agents_callout_open",
        css_class="w-[min(1040px,92vw)] max-w-[92vw]",
    ):
        with Tooltip(AGENTS_CALLOUT_TOOLTIP, side="left"):
            Button(
                AGENTS_CALLOUT_BUTTON_LABEL,
                variant="outline",
                css_class="text-base leading-none whitespace-nowrap",
                style={"padding": "0.4rem 0.7rem"},
            )
        with Grid(columns=2, gap=4, css_class="mt-2"):
            for section in content.sections:
                _render_section(section)


def _render_section(section: AgentSection) -> None:
    with Column(gap=2):
        H4(section.title)
        if section.intro:
            Muted(section.intro)
        with Column(gap=2):
            for link in section.links:
                _render_link(link)


def _render_link(link: AgentLink) -> None:
    with Div():
        if link.href:
            Link(link.label, href=link.href, target="_blank", css_class="font-medium")
        else:
            Text(link.label, css_class="font-medium")
        if link.description:
            with Row(gap=1):
                Muted(link.description)
