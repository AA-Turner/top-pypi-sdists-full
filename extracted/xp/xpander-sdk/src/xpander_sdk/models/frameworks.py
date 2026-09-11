from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel


class Framework(str, Enum):
    """
    Enum representing supported frameworks within xpander.ai.

    Attributes:
        Agno (str): Agno framework identifier.
        GoogleADK (str): Google ADK framework identifier.
        LangChain (str): LangChain framework identifier.
        OpenAIAgents (str): OpenAI Agents framework identifier.
        Strands (str): Strands Agents framework identifier.
        OpenClaw (str): OpenClaw framework identifier.
        ExternalHarness (str): the always-on container running every installed CLI.
        ClaudeCode / Codex (str): legacy single-CLI values, read as ExternalHarness
            with that CLI as the default.
    """

    Agno = "agno"
    GoogleADK = "google-adk"
    LangChain = "langchain"
    OpenAIAgents = "open-ai-agents"
    Strands = "strands-agents"
    OpenClaw = "open-claw"
    ExternalHarness = "external-harness"
    ClaudeCode = "claude-code"
    Codex = "codex"


class HarnessCli(str, Enum):
    """A CLI the harness container can run.

    Chosen per conversation through ``Task.harness_cli``, never per agent.
    """

    ClaudeCode = "claude-code"
    Codex = "codex"
    OpenCode = "opencode"
    # the built-in xpander (agno) loop running inside the harness container
    Xpander = "xpander"


HARNESS_CLIS = frozenset(HarnessCli)
DEFAULT_HARNESS_CLI = HarnessCli.ClaudeCode

# the vendor values stay readable until the platform's row migration rewrites every agent
HARNESS_FRAMEWORKS = frozenset(
    {Framework.ExternalHarness, Framework.ClaudeCode, Framework.Codex}
)
LEGACY_HARNESS_FRAMEWORKS = frozenset({Framework.ClaudeCode, Framework.Codex})


def _wire(value: Union[Enum, str, None]) -> Optional[str]:
    """Lower-cased, stripped wire value of an enum member or string.

    Args:
        value: An enum member, a plain string, or None.

    Returns:
        The normalized wire value, or None for None / blank input.
    """
    if value is None:
        return None
    raw = value.value if isinstance(value, Enum) else str(value)
    raw = raw.strip().lower()
    return raw or None


def is_harness_framework(value: Union[Framework, str, None]) -> bool:
    """True for the CLI harness frameworks; accepts enum, str or None.

    Args:
        value: A framework enum member, its wire value, or None.

    Returns:
        True for ``external-harness`` and the legacy ``claude-code`` / ``codex``
        values, False for every other framework and for None.
    """
    return _wire(value) in {f.value for f in HARNESS_FRAMEWORKS}


def is_legacy_harness_framework(value: Union[Framework, str, None]) -> bool:
    """True for a pre-migration single-CLI harness value.

    Args:
        value: A framework enum member, its wire value, or None.

    Returns:
        True only for ``claude-code`` / ``codex``; ``external-harness`` and every
        non-harness framework answer False.
    """
    return _wire(value) in {f.value for f in LEGACY_HARNESS_FRAMEWORKS}


def normalize_harness_cli(
    value: Union[HarnessCli, Framework, str, None],
) -> Optional[str]:
    """Wire value of a harness CLI when the input names one.

    Args:
        value: A ``HarnessCli`` member, a legacy framework value that names a CLI,
            a plain string, or None.

    Returns:
        ``"claude-code"``, ``"codex"``, ``"opencode"`` or ``"xpander"``; None for
        ``external-harness``, any other framework, unsupported strings, blank input
        and None.
    """
    raw = _wire(value)
    return raw if raw in {c.value for c in HARNESS_CLIS} else None


def normalize_permission_mode(value: Union[Enum, str, None]) -> Optional[str]:
    """Lower-case and strip a harness permission mode; blank becomes None, unknown values pass for the platform to judge."""
    if value is None:
        return None
    normalized = str(getattr(value, "value", value)).strip().lower()
    return normalized or None


def harness_default_cli(
    framework: Union[Framework, str, None],
    default_cli: Union[HarnessCli, str, None] = None,
) -> HarnessCli:
    """The CLI a harness runs when a task names none.

    Args:
        framework: The agent's framework value (any spelling, or None).
        default_cli: The agent's configured ``harness_settings.default_cli``.

    Returns:
        The configured default when it names a CLI, else the CLI a legacy framework
        value names, else ``HarnessCli.ClaudeCode``. Never raises.
    """
    return HarnessCli(
        normalize_harness_cli(default_cli)
        or normalize_harness_cli(framework)
        or DEFAULT_HARNESS_CLI.value
    )


class AgnoSettings(BaseModel):
    """
    Configuration settings specific to the Agno framework.

    Attributes:
        session_storage (Optional[bool]): If True, enables session-level storage. Default is True.
        learning (Optional[bool]): If True, the agent learn and improve with every interaction. Default is False.
        user_memories (Optional[bool]): If True, enables memory of user interactions. Default is True.
        session_summaries (Optional[bool]): If True, enables generation of session summaries. Default is False.
        num_history_runs (Optional[int]): Number of historical runs to retain or consider. Default is 50.
        tool_call_limit (Optional[int]): Max tool calls per run.
        coordinate_mode (Optional[bool]): If True, The agent will be loaded as a Team. Default is False.
        pii_detection_enabled (Optional[bool]): If True, enables PII detection guardrail on agent input. Default is False.
        pii_detection_mask (Optional[bool]): If True, masks detected PII instead of blocking. Default is False.
        prompt_injection_detection_enabled (Optional[bool]): If True, enables prompt injection detection guardrail. Default is False.
        openai_moderation_enabled (Optional[bool]): If True, enables OpenAI content moderation guardrail. Default is False.
        openai_moderation_categories (Optional[List[str]]): List of specific OpenAI moderation categories to enforce. If None, all categories are checked.
        reasoning_tools_enabled (Optional[bool]): If True, enables Agno's reasoning tools (analyze, think, instructions and few shot). Default is True.
    """

    session_storage: Optional[bool] = True

    learning: Optional[bool] = False

    # deprecated: agno memory machinery replaced by the xpander memory layer; kept for wire compat, ignored at runtime
    user_memories: Optional[bool] = False
    agentic_memory: Optional[bool] = False
    agent_memories: Optional[bool] = False
    agentic_culture: Optional[bool] = False

    session_summaries: Optional[bool] = False
    num_history_runs: Optional[int] = 50
    # 0 == None == unset (legacy backend default); only caps >= 1 are forwarded to agno.
    max_tool_calls_from_history: Optional[int] = None
    tool_call_limit: Optional[int] = None
    coordinate_mode: Optional[bool] = False
    pii_detection_enabled: Optional[bool] = False
    pii_detection_mask: Optional[bool] = True
    prompt_injection_detection_enabled: Optional[bool] = False
    openai_moderation_enabled: Optional[bool] = False
    openai_moderation_categories: Optional[List[str]] = None
    reasoning_tools_enabled: Optional[bool] = True
