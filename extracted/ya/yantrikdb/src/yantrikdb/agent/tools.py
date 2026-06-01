"""Companion tool definitions and execution."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

log = logging.getLogger("yantrik.tools")

# OpenAI function-calling schema for companion tools
COMPANION_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "remember",
            "description": "Store something important about the user for later.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "What to remember"},
                    "importance": {"type": "number", "description": "0.0-1.0, how important"},
                    "memory_type": {
                        "type": "string",
                        "enum": ["episodic", "semantic", "procedural"],
                        "description": "Type of memory",
                    },
                    "domain": {
                        "type": "string",
                        "description": "Topic: work, health, family, finance, hobby, general",
                    },
                },
                "required": ["text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recall",
            "description": "Search your memory for something about the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "What to search for"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "relate_entities",
            "description": "Note a relationship between two things (people, places, concepts).",
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "target": {"type": "string"},
                    "relationship": {"type": "string", "description": "e.g. works_with, likes, is_about"},
                },
                "required": ["source", "target", "relationship"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_reminder",
            "description": "Set a reminder for the user at a specific time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "What to remind about"},
                    "remind_at": {"type": "string", "description": "When to remind, ISO format (YYYY-MM-DDTHH:MM)"},
                },
                "required": ["text", "remind_at"],
            },
        },
    },
]


def execute_tool(db, name: str, arguments: dict) -> str:
    """Execute a companion tool call synchronously. Returns result string."""
    try:
        if name == "remember":
            rid = db.record(
                text=arguments["text"],
                memory_type=arguments.get("memory_type", "episodic"),
                importance=arguments.get("importance", 0.5),
                valence=arguments.get("valence", 0.0),
                domain=arguments.get("domain", "general"),
                source="companion",
            )
            log.info("Tool remember: stored %s", rid)
            return f"Remembered. (id: {rid})"

        elif name == "recall":
            results = db.recall(
                query=arguments["query"],
                top_k=5,
                skip_reinforce=True,
            )
            if not results:
                return "No memories found about that."
            lines = [f"- {r['text']}" for r in results[:5]]
            return "\n".join(lines)

        elif name == "relate_entities":
            edge_id = db.relate(
                arguments["source"],
                arguments["target"],
                arguments["relationship"],
            )
            log.info("Tool relate: %s -> %s (%s)",
                     arguments["source"], arguments["target"], arguments["relationship"])
            return f"Connected {arguments['source']} to {arguments['target']}."

        elif name == "set_reminder":
            try:
                remind_dt = datetime.fromisoformat(arguments["remind_at"])
                remind_ts = remind_dt.timestamp()
            except (ValueError, KeyError):
                return "Could not parse reminder time. Use ISO format: YYYY-MM-DDTHH:MM"

            rid = db.record(
                text=arguments["text"],
                memory_type="episodic",
                importance=0.8,
                domain="reminder",
                metadata={"remind_at": remind_ts, "type": "reminder"},
                source="companion",
            )
            log.info("Tool set_reminder: %s at %s", arguments["text"][:50], arguments["remind_at"])
            return f"Reminder set for {arguments['remind_at']}."

        else:
            return f"Unknown tool: {name}"

    except Exception as e:
        log.error("Tool %s failed: %s", name, e)
        return f"Tool error: {e}"
