"""Typed prompt-block refusals. ``error_info`` is the shape the streaming layer surfaces."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PromptBlockErrorInfo:
    error_type: str
    message: str
    user_message: str
    status_code: int = 422


class PromptBlockError(Exception):
    """Base class for prompt-block failures."""


class PromptBlocksMissing(PromptBlockError):
    """A block the agent DECLARES has no row at any rung: the run is refused before any provider call."""

    def __init__(self, names: list[str]) -> None:
        self.names = list(names)
        listed = ", ".join(self.names)
        super().__init__(f"prompt block(s) not found: {listed}")
        self.error_info = PromptBlockErrorInfo(
            error_type="prompt_block_missing",
            message=f"Declared prompt block(s) not found at any level: {listed}",
            user_message=f"Missing prompt block: {listed}. Create it or remove it from the agent.",
        )


class PromptBlocksNotResolved(PromptBlockError):
    """replace_variables ran on a config whose declared blocks were never resolved (a code-path bug)."""

    def __init__(self, names: list[str]) -> None:
        self.names = list(names)
        super().__init__(
            "prompt blocks declared but never resolved before substitution: " + ", ".join(self.names)
        )
        self.error_info = PromptBlockErrorInfo(
            error_type="prompt_blocks_not_resolved",
            message=str(self),
            user_message="This agent's prompt blocks could not be prepared. Try again.",
            status_code=500,
        )


class PromptBlockSourceUnavailable(PromptBlockError):
    """Blocks are declared but the host installed no BlockSource."""

    def __init__(self) -> None:
        super().__init__("prompt blocks are declared but no BlockSource is installed")
        self.error_info = PromptBlockErrorInfo(
            error_type="prompt_block_source_unavailable",
            message=str(self),
            user_message="Prompt blocks are unavailable on this host.",
            status_code=503,
        )
