from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Sequence, Literal, Union

from typing_extensions import TypeAliasType

JSONValue = TypeAliasType("JSONValue", Union[Mapping[str, Any], Sequence[Any], str, int, float, bool, None])
JSONObject = Mapping[str, JSONValue]

@dataclass
class Server:
    name: str

@dataclass
class Environment:
    server_name: str
    environment_name: str
    namespace: str = "matrix"

    @property
    def deployment_name(self) -> str:
        """Get the full deployment identifier in namespace/server_name format."""
        if "/" in self.server_name:
            # Already contains namespace
            return self.server_name
        return f"{self.namespace}/{self.server_name}"

@dataclass
class Task:
    server_name: str
    environment_name: str
    task_spec: JSONObject
    namespace: Optional[str]

    @property
    def deployment_name(self) -> str:
        """Get the full deployment identifier in namespace/server_name format."""
        if self.namespace is None:
            return self.server_name
        else:
            return f"{self.namespace}/{self.server_name}"

@dataclass
class ToolSpec:
    name: str
    description: str
    input_schema: Optional[JSONObject]

@dataclass
class TextBlock:
    text: str
    detail: Optional[JSONObject] = None
    type: Literal["text"] = "text"

@dataclass
class ImageBlock:
    data: str
    mimeType: str
    detail: Optional[JSONObject] = None
    type: Literal["image"] = "image"


@dataclass
class ToolOutput:
    blocks: list[Union[TextBlock, ImageBlock]]
    metadata: Optional[JSONObject] = None
    reward: Optional[float] = None
    finished: bool = False


@dataclass
class ResponseChars:
    """Per-task response-length stats, in characters.

    Length is the number of characters of model-generated content (assistant
    text + tool-call arguments + reasoning) summed over each rollout, with
    percentiles taken across the task's rollouts. Reasoning that is stored only
    as an opaque reference (not inline) is not counted, so this is a best-effort
    lower bound for some providers. These are characters, not tokens.
    """
    mean: float
    p1: float
    p10: float
    p25: float
    p50: float
    p75: float
    p90: float
    p99: float


@dataclass
class TaskDifficulty:
    """Per-task reward + response-length aggregates from the rollout-rewards
    materialized view.

    Returned by :meth:`AsyncEnvironment.get_task_difficulty`. Each instance is
    one ``(split, variant, task_index)`` group, with the statistics computed
    over all matching logged rollouts.
    """
    task_index: int
    avg_reward: float
    min_reward: float
    max_reward: float
    num_rollouts: int
    response_chars: ResponseChars
    split: Optional[str] = None
    variant: Optional[str] = None

# Re-exported for backwards compatibility — defined in openreward.api.errors.
from openreward.api.errors import ToolCallError as ToolCallError  # noqa: F401
from openreward.api._session.http import AuthenticationError as AuthenticationError  # noqa: F401

Provider = Literal[
    "openai",
    "anthropic",
    "google",
    "openrouter"
]