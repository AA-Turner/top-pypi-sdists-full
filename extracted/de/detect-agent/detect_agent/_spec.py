"""Load the language-agnostic agents.json specification."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Any, TypedDict


class AgentSpec(TypedDict):
    key: str
    name: str
    match: dict[str, Any]


class AgentsFile(TypedDict):
    version: int
    aiAgentVar: str
    agents: list[AgentSpec]


def _read_agents_json() -> str:
    # Prefer importlib.resources (installed wheel); fall back to source tree path.
    try:
        return (resources.files("detect_agent") / "agents.json").read_text(encoding="utf-8")
    except (FileNotFoundError, TypeError, ModuleNotFoundError, AttributeError):
        return (Path(__file__).with_name("agents.json")).read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def load_agents_file() -> AgentsFile:
    data = json.loads(_read_agents_json())
    return {
        "version": int(data["version"]),
        "aiAgentVar": str(data["aiAgentVar"]),
        "agents": [
            {
                "key": str(agent["key"]),
                "name": str(agent["name"]),
                "match": agent["match"],
            }
            for agent in data["agents"]
        ],
    }


def known_agents_map() -> dict[str, str]:
    return {agent["key"]: agent["name"] for agent in load_agents_file()["agents"]}
