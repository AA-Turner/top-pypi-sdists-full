from __future__ import annotations

from pydantic import BaseModel

from matrx_ai.agent_runners.research import AgentResult
from matrx_ai.agents.named import NamedAgent
from matrx_ai.agents.source_tracking import stamp_source_context
from matrx_ai.mandates import run_mandated
from matrx_ai.tools.models import ToolContext


class PdfCleanerAgent(NamedAgent):
    """Canonical PDF-extracted-text cleaner (THE ONE — NamedAgent).

    Declarative variable mapping (Inputs ``content`` -> the agent's declared
    ``text_extracted_from_pdf`` variable) is validated at ship time via
    ``NamedAgent.validate()`` against the agent row's ``variable_definitions``.
    That is the structural guard against the 2026-05-26 drift incident (a
    runner kwarg silently rendering an empty template placeholder).
    """

    name = "clean_pdf_extracted_content"
    # DB-managed slot: the pinned source below is the standalone seed; when a
    # host installs a mandate resolver, the bound agent runs instead.
    mandate_key = "pdf.content_cleaner"
    # Machine-parsed cleanup output — ratified citations exclusion (explicit,
    # loud at the provider gate when documents are present).
    citations_enabled = False
    # Pinned snapshot (version 2 of "Clean PDF Extracted Content") — reads from
    # agx_version so future master edits are invisible here.
    variable_map = {"content": "text_extracted_from_pdf"}

    class Inputs(BaseModel):
        content: str


async def clean_pdf_extracted_content(
    content: str,
    ctx: ToolContext = None,
    *,
    suppress_stream: bool = True,
) -> AgentResult:
    """Canonical entry point — runs through THE ONE (NamedAgent/run_agent).

    ``suppress_stream`` defaults to True for NESTED callers (a tool or an
    ingestion step already streaming something else to the person). A caller
    whose own stream IS this cleanup — the manual "AI Clean" endpoint — passes
    False so the person watches the cleaned text arrive instead of minutes of
    heartbeats."""
    stamp_source_context(source_app="matrx-ai", source_feature="pdf-cleaner")
    result = await run_mandated(
        PdfCleanerAgent,
        inputs=PdfCleanerAgent.Inputs(content=content),
        label="PDF Cleanup",
        # NESTED-AGENT STREAM LEAK (the default): inside a tool / ingestion
        # step the caller is already streaming to a user, so unmuted the whole
        # cleaned PDF pours onto that caller's NDJSON stream. The cleaned text
        # still returns via AgentRunResult either way.
        suppress_stream=suppress_stream,
    )
    return AgentResult(
        success=result.success,
        output=result.output,
        usage=dict(result.usage),
        usage_history=list(result.usage_history),
        metadata=dict(result.metadata),
        error=getattr(result, "error", None),
        exception=getattr(result, "exception", None),
    )
