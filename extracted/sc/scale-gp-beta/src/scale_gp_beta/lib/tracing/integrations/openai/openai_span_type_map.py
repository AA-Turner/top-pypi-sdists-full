from typing import Dict, Optional

from scale_gp_beta.types import SpanType

OPENAI_SPAN_TYPE_MAP: Dict[str, SpanType] = {
    "generation": "COMPLETION",
    "agent": "AGENT_WORKFLOW",
    "function": "CODE_EXECUTION",
    "response": "COMPLETION",
    "handoff": "CUSTOM",
    "custom": "CUSTOM",
    "guardrail": "STANDALONE",
    "transcription": "STANDALONE",
    "speech": "STANDALONE",
    "speech_group": "STANDALONE",
    "mcp_tools": "STANDALONE",
}


def openai_span_type_map(span_type: Optional[str]) -> SpanType:
    """
    Maps an OpenAI span type string to its corresponding SGP SpanTypeLiteral.

    Returns "CUSTOM" if the input is None or not found in the map.
    """
    if not span_type:
        return "CUSTOM"

    return OPENAI_SPAN_TYPE_MAP.get(span_type, "CUSTOM")
