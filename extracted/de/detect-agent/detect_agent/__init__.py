"""Detect if code is running in an AI agent or automated development environment."""

from __future__ import annotations

import os
from typing import Literal, TypedDict, Union

from detect_agent._evaluate import evaluate_condition
from detect_agent._spec import known_agents_map, load_agents_file

# Kept for backward-compatible imports/tests; Devin detection reads path from agents.json.
DEVIN_LOCAL_PATH = "/opt/.devin"

KNOWN_AGENTS: dict[str, str] = known_agents_map()

CURSOR: Literal["cursor"] = "cursor"
CURSOR_CLI: Literal["cursor-cli"] = "cursor-cli"
CLAUDE: Literal["claude"] = "claude"
COWORK: Literal["cowork"] = "cowork"
DEVIN: Literal["devin"] = "devin"
REPLIT: Literal["replit"] = "replit"
GEMINI: Literal["gemini"] = "gemini"
CODEX: Literal["codex"] = "codex"
ANTIGRAVITY: Literal["antigravity"] = "antigravity"
AUGMENT_CLI: Literal["augment-cli"] = "augment-cli"
OPENCODE: Literal["opencode"] = "opencode"
GITHUB_COPILOT: Literal["github-copilot"] = "github-copilot"
CLINE: Literal["cline"] = "cline"
GOOSE: Literal["goose"] = "goose"
JUNIE: Literal["junie"] = "junie"
PI: Literal["pi"] = "pi"
KIRO: Literal["kiro"] = "kiro"
OPENCLAW: Literal["openclaw"] = "openclaw"

KnownAgentNames = Literal[
    "cursor",
    "cursor-cli",
    "claude",
    "cowork",
    "devin",
    "replit",
    "gemini",
    "codex",
    "antigravity",
    "augment-cli",
    "opencode",
    "github-copilot",
    "cline",
    "goose",
    "junie",
    "pi",
    "kiro",
    "openclaw",
]


class KnownAgentDetails(TypedDict):
    name: str


class AgentResultAgent(TypedDict):
    is_agent: Literal[True]
    agent: KnownAgentDetails


class AgentResultNone(TypedDict):
    is_agent: Literal[False]
    agent: None


AgentResult = Union[AgentResultAgent, AgentResultNone]


def _resolve_ai_agent_standard(ai_agent_var: str) -> str | None:
    raw = os.environ.get(ai_agent_var)
    if not raw:
        return None
    value = raw.strip()
    if not value:
        return None
    return value


def determine_agent() -> AgentResult:
    """Inspect the environment and return which AI agent is running, if any.

    ``AI_AGENT`` takes highest priority. After that, agents from ``agents.json``
    are evaluated in order and the first match wins.

    Python-port extension: ``PI_CODING_AGENT`` also detects Pi for backward
    compatibility with earlier releases of this package.
    """
    spec = load_agents_file()

    ai_agent = _resolve_ai_agent_standard(spec["aiAgentVar"])
    if ai_agent:
        return {"is_agent": True, "agent": {"name": ai_agent}}

    # Backward-compatible Pi marker from earlier Python port releases.
    if os.environ.get("PI_CODING_AGENT"):
        return {"is_agent": True, "agent": {"name": KNOWN_AGENTS["PI"]}}

    for agent in spec["agents"]:
        if evaluate_condition(agent["match"]):
            return {"is_agent": True, "agent": {"name": agent["name"]}}

    return {"is_agent": False, "agent": None}
