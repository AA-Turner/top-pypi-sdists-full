"""Reading JSON out of an AI's reply — an injection seam.

An AI reply rarely is bare JSON: it arrives in a ```json fence, after a sentence of prose,
or with a stray comma. Reading it is the host's job, through its ONE LLM-JSON funnel
(aidream wires ``matrx_ai.agents.response_parser.extract_json``) — matrx-graph must never
import matrx_ai, and a second hand-rolled scraper here would drift from the funnel.

``data.parse_json`` calls :func:`extract_llm_json` when its ``lenient`` option is on. With no
extractor configured the call raises :class:`LlmJsonExtractorMissing`, so a lenient step
fails loudly instead of quietly falling back to strict parsing.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from pydantic import JsonValue


@dataclass(frozen=True)
class LlmJsonExtraction:
    ok: bool
    value: JsonValue = None
    #: Why nothing was found (``ok`` False), in the funnel's own words.
    reason: str = ""
    #: How many JSON candidates the reply held that fit (the first one is ``value``).
    candidates: int = 0


#: ``(text, schema) -> LlmJsonExtraction``. ``schema`` is a JSON Schema the value must fit
#: at its top level, or None.
LlmJsonExtractor = Callable[[str, dict | None], LlmJsonExtraction]

_extractor: LlmJsonExtractor | None = None


class LlmJsonExtractorMissing(RuntimeError):
    pass


def configure_llm_json_extractor(extractor: LlmJsonExtractor | None) -> None:
    """Register (or clear, with None) the host's LLM-JSON funnel. Called once at startup."""
    global _extractor
    _extractor = extractor


def is_llm_json_extractor_configured() -> bool:
    return _extractor is not None


def extract_llm_json(text: str, schema: dict | None = None) -> LlmJsonExtraction:
    if _extractor is None:
        raise LlmJsonExtractorMissing(
            "Lenient JSON reading needs the host's LLM-JSON funnel, and none is configured "
            "(matrx_graph.configure_llm_json_extractor)."
        )
    return _extractor(text, schema)
