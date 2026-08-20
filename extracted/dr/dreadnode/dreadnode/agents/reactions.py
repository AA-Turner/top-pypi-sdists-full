from pydantic import ConfigDict, Field
from pydantic.dataclasses import dataclass

import dreadnode
from dreadnode.generators.message import Message


@dataclass
class Reaction(Exception): ...  # noqa: N818


@dataclass
class Continue(Reaction):
    """Continue execution, optionally with feedback to guide the agent."""

    messages: list[Message] = Field(default_factory=list, repr=False)
    feedback: str | None = None

    def log_metrics(self, *, step: int) -> None:
        """Record continuation metrics for tracing and analytics."""
        dreadnode.log_metric("continues", 1, step=step, mode="count")
        dreadnode.log_metric("messages", len(self.messages), step=step)


@dataclass
class Retry(Reaction):
    messages: list[Message] | None = Field(default=None, repr=False)

    def log_metrics(self, *, step: int) -> None:
        """Record retry metrics for tracing and analytics."""
        dreadnode.log_metric("retries", 1, step=step, mode="count")
        if self.messages is not None:
            dreadnode.log_metric("messages", len(self.messages), step=step)


@dataclass
class RetryWithFeedback(Reaction):
    feedback: str
    tool_call_id: str | None = None
    metadata: dict[str, object] = Field(default_factory=dict)


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class Fail(Reaction):
    error: Exception | str


@dataclass
class Finish(Reaction):
    reason: str | None = None
