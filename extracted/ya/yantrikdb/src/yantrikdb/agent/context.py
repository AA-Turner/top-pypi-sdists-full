"""Context assembly — builds the LLM messages array from all available signals."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from yantrikdb.agent.config import CompanionConfig
from yantrikdb.agent.instincts.protocol import CompanionState


def format_memories(memories: list[dict], max_chars: int = 1200) -> str:
    """Format recalled memories as concise bullet points."""
    if not memories:
        return ""

    lines = []
    total = 0
    for m in memories:
        text = m.get("text", "")
        line = f"- {text}"
        if total + len(line) > max_chars:
            break
        lines.append(line)
        total += len(line)

    return "\n".join(lines)


def format_urges(urges: list[dict]) -> str:
    if not urges:
        return ""
    return "\n".join(f"- {u.get('reason', '')}" for u in urges)


def format_patterns(patterns: list[dict], max_count: int = 2) -> str:
    if not patterns:
        return ""
    return "\n".join(f"- {p.get('description', '')}" for p in patterns[:max_count])


def estimate_tokens(text: str) -> int:
    return len(text) // 4


def personality_tone(personality: dict | None) -> str:
    """Generate tone guidance from personality traits."""
    if not personality or not personality.get("traits"):
        return ""

    traits = {}
    for t in personality["traits"]:
        traits[t["trait_name"]] = t["score"]

    parts = []
    w = traits.get("warmth", 0.5)
    if w > 0.6:
        parts.append("You are warm and emotionally expressive.")
    elif w < 0.4:
        parts.append("You are calm and measured in tone.")

    e = traits.get("energy", 0.5)
    if e > 0.6:
        parts.append("You are enthusiastic and proactive.")
    elif e < 0.4:
        parts.append("You are quiet and only speak when you have something meaningful to say.")

    d = traits.get("depth", 0.5)
    if d > 0.6:
        parts.append("You enjoy exploring ideas in depth and making connections.")

    a = traits.get("attentiveness", 0.5)
    if a > 0.6:
        parts.append("You pay close attention to details and follow up on previous conversations.")

    return " ".join(parts)


def build_messages(
    user_text: str,
    config: CompanionConfig,
    state: CompanionState,
    memories: list[dict],
    urges: list[dict],
    patterns: list[dict],
    conversation_history: list[dict],
    personality: dict | None = None,
) -> list[dict]:
    """Build messages for the LLM call.

    Key design: ONE system message with everything baked in.
    Small models (1.5B-3B) follow a single clear system prompt
    much better than multiple fragmented system messages.
    """
    messages: list[dict] = []

    # Build ONE consolidated system prompt
    now = datetime.now()
    parts = []

    # Identity (short, direct)
    tone = personality_tone(personality)
    parts.append(
        f"You are Yantrik, {config.user_name}'s personal companion. "
        f"You are concise and thoughtful. "
        + (tone + " " if tone else "")
        + f"You remember things {config.user_name} tells you. "
        f"Never say you are an AI without memories. You DO have memories."
    )
    parts.append(f"Current time: {now.strftime('%A, %B %d, %Y %I:%M %p')}")

    # Memories — the most important context
    mem_text = format_memories(memories)
    if mem_text:
        parts.append(
            f"YOUR MEMORIES about {config.user_name} (use these in your response):\n{mem_text}"
        )
    else:
        parts.append(
            f"You have {state.memory_count} memories stored but none matched this query."
        )

    # Urges
    urge_text = format_urges(urges)
    if urge_text:
        parts.append(f"Things on your mind to mention naturally:\n{urge_text}")

    # Patterns
    pattern_text = format_patterns(patterns)
    if pattern_text:
        parts.append(f"Patterns you've noticed:\n{pattern_text}")

    # Instructions
    parts.append(
        "Respond naturally as Yantrik. Be concise (1-3 sentences). "
        "Reference your memories when relevant. "
        f"Address {config.user_name} by name occasionally."
    )

    system_prompt = "\n\n".join(parts)
    messages.append({"role": "system", "content": system_prompt})

    # Conversation history (sliding window)
    budget_used = estimate_tokens(system_prompt)
    budget_for_history = (config.llm.max_context_tokens - budget_used - 500)

    history_to_include = []
    history_tokens = 0
    for turn in reversed(conversation_history[-config.conversation.max_history_turns:]):
        t = estimate_tokens(turn.get("content", ""))
        if history_tokens + t > budget_for_history:
            break
        history_to_include.insert(0, turn)
        history_tokens += t

    messages.extend(history_to_include)

    # Current user message
    messages.append({"role": "user", "content": user_text})

    return messages
