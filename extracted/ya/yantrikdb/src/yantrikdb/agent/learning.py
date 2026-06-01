"""Post-interaction learning — extract memories and entities from conversations."""

from __future__ import annotations

import json
import logging
from typing import Any, Optional

from yantrikdb.agent.llm import LLMClient

log = logging.getLogger("yantrik.learning")

EXTRACTION_PROMPT = """You are a memory extraction assistant. Given a conversation exchange, decide what to remember.

Output valid JSON with these fields:
- should_remember: true/false
- memory_text: concise summary of what to remember (1-2 sentences)
- memory_type: "episodic" (event), "semantic" (fact), or "procedural" (how-to)
- importance: 0.0-1.0
- valence: -1.0 (negative) to 1.0 (positive)
- domain: work/health/family/finance/hobby/travel/general
- entities: list of {"source": str, "target": str, "relationship": str} pairs
- is_open_topic: true if user mentioned something unresolved
- topic_summary: if is_open_topic, what the unresolved item is

Only set should_remember=true for substantive information (facts, preferences, events, plans).
Skip small talk, greetings, and trivial exchanges.

Respond ONLY with JSON, no other text."""


async def extract_and_learn(
    db,
    llm: LLMClient,
    user_text: str,
    response_text: str,
) -> None:
    """Extract memories and entities from a conversation turn. Fire-and-forget."""
    # Skip very short messages (likely greetings/acks)
    if len(user_text) < 25:
        return

    try:
        messages = [
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": f"User: {user_text}\nCompanion: {response_text}"},
        ]

        resp = await llm.chat(messages, max_tokens=250)
        content = resp.content.strip()

        # Try to parse JSON (handle markdown code blocks)
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()

        parsed = json.loads(content)

        if not parsed.get("should_remember", False):
            return

        # Store the memory
        memory_text = parsed.get("memory_text", user_text)
        db.record(
            text=memory_text,
            memory_type=parsed.get("memory_type", "episodic"),
            importance=parsed.get("importance", 0.5),
            valence=parsed.get("valence", 0.0),
            domain=parsed.get("domain", "general"),
            source="companion",
        )
        log.info("Learned: %s", memory_text[:80])

        # Store entity relationships
        for entity in parsed.get("entities", []):
            if all(k in entity for k in ("source", "target", "relationship")):
                db.relate(
                    entity["source"],
                    entity["target"],
                    entity["relationship"],
                )

        # Store open topics
        if parsed.get("is_open_topic") and parsed.get("topic_summary"):
            db.record(
                text=parsed["topic_summary"],
                memory_type="episodic",
                importance=0.6,
                domain="topic",
                source="companion",
                metadata={"status": "open", "type": "unresolved_topic"},
            )
            log.info("Open topic tracked: %s", parsed["topic_summary"][:60])

    except json.JSONDecodeError:
        log.debug("Could not parse extraction response as JSON")
    except Exception as e:
        log.warning("Learning extraction failed: %s", e)
