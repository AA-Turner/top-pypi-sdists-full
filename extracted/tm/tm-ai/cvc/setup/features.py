"""cvc.setup.features — Catalog of every CVC capability shown in the setup wizard.

The wizard walks users through enabling each surface so nothing built stays hidden.
Each FeatureSpec describes a capability, how to enable it, and a verification command.

Categories:
  • core         — always-on baseline (commit, branch, restore, recall)
  • dashboard    — Vite/React browser dashboard at localhost:8765
  • mcp          — Model Context Protocol server for IDE integration
  • agent        — CVC agent loop (chat, tools, sub-agents)
  • integration  — third-party bridges (Telegram, VS Code, Claude Code, etc.)
  • hive         — Sofia/Tina/Samantha/Robin core team + multi-agent coordination
  • observability— trajectory, providers panel, loop state, COGNOME audit
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(frozen=True)
class FeatureSpec:
    key: str                    # canonical identifier
    name: str                   # display name
    category: str               # core | dashboard | mcp | agent | integration | hive | observability
    description: str
    default_enabled: bool = True
    cli_command: str = ""       # how to verify / launch (e.g. "cvc dashboard")
    docs_anchor: str = ""       # docs/website/DOCUMENTATION.md anchor
    optional: bool = True       # if False, cannot be disabled (core)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Feature catalog — every surface the user should know exists.
# ORDER = tour order in the wizard.
# ---------------------------------------------------------------------------

FEATURE_SPECS: tuple[FeatureSpec, ...] = (
    # --- CORE (always on) ----------------------------------------------------
    FeatureSpec(
        key="cognitive_vc",
        name="Cognitive Version Control",
        category="core",
        description="commit · branch · merge · restore · diff for AI conversations",
        cli_command="cvc commit -m 'checkpoint'",
        optional=False,
    ),
    FeatureSpec(
        key="semantic_recall",
        name="Semantic Recall",
        category="core",
        description="Vector search across every past conversation (`cvc recall <query>`)",
        cli_command="cvc recall 'how did we fix auth?'",
        optional=False,
    ),
    FeatureSpec(
        key="cognome",
        name="COGNOME Engram Compiler",
        category="core",
        description="Smart-librarian context compiler — token-budgeted preamble per query",
        cli_command="cvc cognome status",
    ),

    # --- AGENT ---------------------------------------------------------------
    FeatureSpec(
        key="agent_chat",
        name="CVC Agent (chat)",
        category="agent",
        description="Interactive AI agent with tools, sub-agents, and credential pooling",
        cli_command="cvc chat",
    ),
    FeatureSpec(
        key="iteration_budget",
        name="Iteration Budget Guardrails",
        category="agent",
        description="Hard cap on agent loop iterations (env: CVC_MAX_ITER, default 200)",
        cli_command="cvc loop state",
    ),
    FeatureSpec(
        key="trajectory",
        name="Trajectory Recorder",
        category="observability",
        description="Append-only JSONL log of every agent turn → ~/.cvc/trajectories/",
        cli_command="cvc trajectory tail",
    ),
    FeatureSpec(
        key="credential_pool",
        name="Credential Pool",
        category="agent",
        description="Multi-token rotation for Copilot / NVIDIA / API keys (rate-limit defeat)",
        cli_command="cvc copilot status",
    ),

    # --- HIVE / TEAM ---------------------------------------------------------
    FeatureSpec(
        key="core_team",
        name="Core 4 Hive (Sofia · Tina · Samantha · Robin)",
        category="hive",
        description="Pre-registered orchestrator + 3 specialist agents in the hive memory",
        cli_command="cvc team list",
    ),
    FeatureSpec(
        key="hive_memory",
        name="Hive Memory (Plüberous)",
        category="hive",
        description="Shared memory space for inter-agent knowledge transfer",
        cli_command="cvc hive status",
    ),

    # --- DASHBOARD -----------------------------------------------------------
    FeatureSpec(
        key="dashboard",
        name="Browser Dashboard",
        category="dashboard",
        description="Vite/React dashboard at http://localhost:8765 — providers, loop, team, trajectory",
        cli_command="cvc dashboard",
    ),
    FeatureSpec(
        key="providers_panel",
        name="Providers Panel",
        category="dashboard",
        description="Live view of all registered providers + credential pool health",
        cli_command="cvc providers list",
    ),
    FeatureSpec(
        key="loop_panel",
        name="Loop State Panel",
        category="dashboard",
        description="Real-time agent loop telemetry over /ws/dashboard",
        cli_command="cvc loop state",
    ),

    # --- MCP / IDE INTEGRATION -----------------------------------------------
    FeatureSpec(
        key="mcp_server",
        name="MCP Server",
        category="mcp",
        description="Model Context Protocol server for VS Code / Cursor / Windsurf / Copilot",
        cli_command="cvc mcp serve",
    ),
    FeatureSpec(
        key="vscode_extension",
        name="VS Code Extension",
        category="integration",
        description="Native VS Code integration with auto-commit on Copilot turns",
        cli_command="code --install-extension cvc-vscode",
    ),
    FeatureSpec(
        key="launch_bridge",
        name="Tool Launchers",
        category="integration",
        description="`cvc launch <tool>` routes Claude Code / Cursor / Aider through CVC",
        cli_command="cvc launch claude",
    ),

    # --- COMMUNICATION BRIDGES -----------------------------------------------
    FeatureSpec(
        key="telegram_bridge",
        name="Telegram Bridge",
        category="integration",
        description="Bidirectional Telegram I/O for the agent (env: TELEGRAM_BOT_TOKEN)",
        default_enabled=False,
        cli_command="cvc telegram start",
    ),
)


# ---------------------------------------------------------------------------
# Lookups
# ---------------------------------------------------------------------------

def list_feature_specs(category: str | None = None) -> list[FeatureSpec]:
    if category is None:
        return list(FEATURE_SPECS)
    return [f for f in FEATURE_SPECS if f.category == category]


def get_feature_spec(key: str) -> FeatureSpec | None:
    for f in FEATURE_SPECS:
        if f.key == key:
            return f
    return None


def feature_categories() -> list[str]:
    """Ordered, de-duplicated list of categories present in the catalog."""
    seen: list[str] = []
    for f in FEATURE_SPECS:
        if f.category not in seen:
            seen.append(f.category)
    return seen


__all__ = [
    "FeatureSpec",
    "FEATURE_SPECS",
    "list_feature_specs",
    "get_feature_spec",
    "feature_categories",
]
