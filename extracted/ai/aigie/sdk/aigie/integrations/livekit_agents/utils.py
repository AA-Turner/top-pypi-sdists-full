"""
Utility functions for LiveKit Agents integration.

Provides helpers for extracting agent info, model details,
room metadata, and formatting data for traces.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def is_livekit_installed() -> bool:
    """Check if LiveKit Agents SDK is installed."""
    try:
        import livekit.agents

        return True
    except ImportError:
        return False


def extract_agent_name(agent: Any) -> str:
    """Extract a display name from a LiveKit Agent instance.

    Checks: agent.name, agent.__class__.__name__, instructions prefix.
    """
    if agent is None:
        return "unknown"

    name = getattr(agent, "name", None)
    if name:
        return str(name)

    cls_name = type(agent).__name__
    if cls_name != "Agent":
        return cls_name

    instructions = getattr(agent, "instructions", None)
    if instructions and isinstance(instructions, str):
        # Extract first meaningful phrase
        first_line = instructions.split("\n")[0].strip()
        if len(first_line) > 50:
            first_line = first_line[:47] + "..."
        if first_line:
            return first_line

    return "Agent"


def extract_model_info(session: Any) -> dict[str, str | None]:
    """Extract LLM/STT/TTS model information from an AgentSession.

    LiveKit stores model info on the session's configured providers.
    """
    info: dict[str, str | None] = {
        "llm_model": None,
        "stt_model": None,
        "tts_model": None,
        "llm_provider": None,
    }

    if session is None:
        return info

    # LLM
    llm = getattr(session, "llm", None) or getattr(session, "_llm", None)
    if llm:
        info["llm_model"] = getattr(llm, "model", None) or getattr(llm, "label", None)
        info["llm_provider"] = getattr(llm, "provider", None)

    # STT
    stt = getattr(session, "stt", None) or getattr(session, "_stt", None)
    if stt:
        info["stt_model"] = getattr(stt, "model", None) or getattr(stt, "label", None)

    # TTS
    tts = getattr(session, "tts", None) or getattr(session, "_tts", None)
    if tts:
        info["tts_model"] = getattr(tts, "model", None) or getattr(tts, "label", None)

    return info


def extract_room_info(session: Any) -> dict[str, str | None]:
    """Extract LiveKit room information from a session."""
    info: dict[str, str | None] = {
        "room_name": None,
        "room_sid": None,
        "participant_identity": None,
    }

    room = getattr(session, "room", None) or getattr(session, "_room", None)
    if room:
        info["room_name"] = getattr(room, "name", None)
        info["room_sid"] = getattr(room, "sid", None)
        local = getattr(room, "local_participant", None)
        if local:
            info["participant_identity"] = getattr(local, "identity", None)

    return info


def format_chat_context(chat_ctx: Any, max_length: int = 2000) -> str:
    """Format a LiveKit ChatContext into a readable string."""
    if chat_ctx is None:
        return ""

    items = getattr(chat_ctx, "items", None)
    if not items:
        return ""

    parts: list[str] = []
    total_len = 0

    for item in items:
        role = getattr(item, "role", "unknown")
        content = getattr(item, "content", "")

        if isinstance(content, list):
            text_parts = []
            for part in content:
                if hasattr(part, "text"):
                    text_parts.append(getattr(part, "text", ""))
                elif isinstance(part, str):
                    text_parts.append(part)
            content = " ".join(text_parts)

        line = f"{role}: {content}"
        if total_len + len(line) > max_length:
            remaining = max_length - total_len
            if remaining > 20:
                parts.append(line[:remaining] + "...")
            break
        parts.append(line)
        total_len += len(line) + 1

    return "\n".join(parts)


def truncate_transcription(text: str, max_length: int = 2000) -> str:
    """Truncate transcription text to max length."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def format_metrics_for_trace(metrics: Any) -> dict[str, Any]:
    """Format a LiveKit metrics object for trace metadata."""
    result: dict[str, Any] = {}

    for attr in (
        "ttft",
        "duration",
        "prompt_tokens",
        "completion_tokens",
        "tokens_per_second",
        "ttfb",
        "audio_duration",
        "characters_count",
        "input_tokens",
        "output_tokens",
        "end_of_utterance_delay",
        "transcription_delay",
        "num_interruptions",
    ):
        val = getattr(metrics, attr, None)
        if val is not None:
            result[attr] = val

    md = getattr(metrics, "metadata", None)
    if md:
        result["model_name"] = getattr(md, "model_name", None)
        result["model_provider"] = getattr(md, "model_provider", None)

    return result


def extract_tool_info(function_calls: list[Any]) -> list[dict[str, Any]]:
    """Extract tool call information from LiveKit function calls."""
    tools: list[dict[str, Any]] = []
    for call in function_calls or []:
        tools.append(
            {
                "name": getattr(call, "name", "unknown"),
                "call_id": getattr(call, "call_id", None),
                "arguments": str(getattr(call, "arguments", ""))[:500],
            }
        )
    return tools
