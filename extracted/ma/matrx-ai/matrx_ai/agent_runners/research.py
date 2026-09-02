from __future__ import annotations

from typing import Any

from matrx_utils import vcprint
from pydantic import BaseModel, Field

from matrx_ai.agents.executor import AgentRunResult
from matrx_ai.agents.named import NamedAgent
from matrx_ai.agents.source_tracking import stamp_source_context
from matrx_ai.config import TokenUsage
from matrx_ai.mandates import run_mandated
from matrx_ai.tools.models import ToolContext


class AgentResult(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    success: bool
    output: str = ""
    usage: dict[str, Any] = Field(default_factory=dict)
    usage_history: list[TokenUsage] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class _CondenserInputs(BaseModel):
    instructions: str
    scraped_content: str
    queries: str = ""
    search_results: str


# Pinned builtin agents (THE ONE — NamedAgent). The four Inputs fields match
# each agent's declared variable_definitions 1:1, so no variable_map is needed.
class ResearchCondenser1Agent(NamedAgent[_CondenserInputs, BaseModel]):
    name = "research_condenser_1"
    mandate_key = "research.condenser_1"
    Inputs = _CondenserInputs
    # Machine-parsed condensation feeding the research pipeline — ratified
    # citations exclusion (explicit, loud at the provider gate).
    citations_enabled = False


class ResearchCondenser2Agent(NamedAgent[_CondenserInputs, BaseModel]):
    name = "research_condenser_2"
    mandate_key = "research.condenser_2"
    Inputs = _CondenserInputs
    citations_enabled = False


def _stamp_web_research_source() -> None:
    stamp_source_context(source_app="matrx-ai", source_feature="web_research")


def _to_agent_result(run: AgentRunResult, label: str) -> AgentResult:
    if not run.success:
        vcprint(f"{label} failed: {run.error}", color="red")
        return AgentResult(success=False, output=f"Agent failed: {run.error}")
    vcprint(run.usage, title=f"[{label}] Usage", color="pink")
    return AgentResult(
        success=True,
        output=run.output,
        usage=run.usage,
        usage_history=list(run.usage_history),
        metadata=run.metadata,
    )


async def scrape_research_condenser_agent_1(
    instructions: str,
    scraped_content: str,
    queries: str,
    search_results: str,
    ctx: ToolContext,
) -> AgentResult:
    _stamp_web_research_source()
    run = await run_mandated(
        ResearchCondenser1Agent,
        inputs=_CondenserInputs(
            instructions=instructions,
            scraped_content=scraped_content,
            queries=queries,
            search_results=search_results,
        ),
    )
    return _to_agent_result(run, "research_condenser_1")


async def scrape_research_condenser_agent_2(
    instructions: str,
    scraped_content: str,
    queries: str,
    search_results: str,
    ctx: ToolContext,
) -> AgentResult:
    _stamp_web_research_source()
    run = await run_mandated(
        ResearchCondenser2Agent,
        inputs=_CondenserInputs(
            instructions=instructions,
            scraped_content=scraped_content,
            queries=queries,
            search_results=search_results,
        ),
    )
    return _to_agent_result(run, "research_condenser_2")
