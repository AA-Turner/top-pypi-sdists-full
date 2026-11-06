import math
from enum import StrEnum
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, model_validator

from mistralai.vibe.harness.app_server.session import BuiltinsConfig
from mistralai.vibe.harness.app_server.session import (
    ProgrammaticToolCallingConfig as HarnessProgrammaticToolCallingConfig,
)
from mistralai.vibe_agents.session_workflow.commands import ReasoningEffort

from .errors import SdkError

PermissionMode = Literal["auto", "ask", "deny"]
"""Which tool calls need an approval: ``"auto"`` runs every call that the agent's ``permission_policy``
allows (every call without one), ``"ask"`` opens an approval for each call, and ``"deny"`` refuses them."""


class LLMProvider(StrEnum):
    MISTRAL = "mistral"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


# The range every built-in provider config accepts. A model may allow less, and then the
# provider's refusal names its own limit.
MIN_TEMPERATURE = 0.0
MAX_TEMPERATURE = 2.0


def check_temperature(temperature: object, *, owner: str) -> None:
    """Reject a temperature no built-in provider accepts, before any Turn runs."""

    if temperature is None:
        return
    if isinstance(temperature, bool) or not isinstance(temperature, int | float):
        raise SdkError(f"{owner} temperature must be a number, got {temperature!r}")
    # The range check comes first: math.isnan() cannot convert a very large integer.
    if not MIN_TEMPERATURE <= temperature <= MAX_TEMPERATURE or math.isnan(temperature):
        raise SdkError(
            f"{owner} temperature must be between {MIN_TEMPERATURE:g} and {MAX_TEMPERATURE:g}, got {temperature!r}"
        )


class ProgrammaticToolCallingConfig(BaseModel):
    """Options of programmatic tool calling. Passing them turns the feature on."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    sleep: bool = True
    """Let programs wait with `tools.self.sleep`."""


class Builtins(BaseModel):
    """Built-in features of the agent. Everything is on by default; set a field to False to opt out.

    File and shell tools are not here: they come from the sandbox `access` level.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    skills: bool = True
    """The `skill` tool, offered while the agent has at least one skill. An agent with it off cannot declare skills."""
    subagents: bool = True
    """Starting subagents. Needs programmatic tool calling. An agent with it off cannot declare subagents."""
    programmatic_tool_calling: bool | ProgrammaticToolCallingConfig = True
    """`run_typescript`, `search_tool_functions` and your tools as typed functions."""
    background_processes: bool | None = None
    """Long-running processes, called from programs. Need `full` sandbox access and programmatic tool calling.

    `None` turns them on when the sandbox supports them.
    """

    @model_validator(mode="after")
    def _check_with_the_harness(self) -> Self:
        builtins_to_config(self)
        return self

    @classmethod
    def none(cls) -> Self:
        """No built-in features. With the default `NoSandbox`, the model sees only your tools.

        A sandbox still gives the file and shell tools its `access` level allows.
        """

        return cls(skills=False, subagents=False, programmatic_tool_calling=False, background_processes=False)


def builtins_to_config(builtins: Builtins) -> BuiltinsConfig:
    # Private to the SDK: the Harness BuiltinsConfig is the wire encoding of the Builtins switches.
    programmatic = builtins.programmatic_tool_calling
    return BuiltinsConfig(
        skills=builtins.skills,
        subagents=builtins.subagents,
        programmatic_tool_calling=(
            programmatic
            if isinstance(programmatic, bool)
            else HarnessProgrammaticToolCallingConfig(sleep=programmatic.sleep)
        ),
        background_processes=builtins.background_processes,
    )


__all__ = [
    "MAX_TEMPERATURE",
    "MIN_TEMPERATURE",
    "Builtins",
    "LLMProvider",
    "PermissionMode",
    "ProgrammaticToolCallingConfig",
    "ReasoningEffort",
    "check_temperature",
]
