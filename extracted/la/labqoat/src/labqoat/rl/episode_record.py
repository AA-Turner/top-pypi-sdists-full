"""What one episode came to."""

import json
from dataclasses import dataclass

from labqoat.json_document import JsonDocument, JsonValue


@dataclass(frozen=True)
class EpisodeRecord:
    """One task's outcome: its reward, or why it has none, and what it took.

    ``reward`` is what the episode returned. It is ``None`` when the episode produced no reward: its sandbox
    was lost on every attempt, a sandbox operation failed, or it ran past its time; ``error`` then says which.
    ``attempts`` counts sandboxes started for the task and ``seconds`` covers all of them, waiting for room
    included. ``detail`` is whatever JSON the episode returned beside its reward, such as a transcript.
    """

    task: str
    reward: float | None
    attempts: int
    seconds: float
    error: str | None = None
    detail: JsonValue = None

    @property
    def completed(self) -> bool:
        """Report whether the episode produced a reward."""
        return self.reward is not None

    def to_json(self) -> str:
        """Write the record as one line of JSON."""
        document = {
            "task": self.task,
            "reward": self.reward,
            "attempts": self.attempts,
            "seconds": round(self.seconds, 3),
            "error": self.error,
            "detail": self.detail,
        }
        return json.dumps(document, separators=(",", ":"), allow_nan=False)

    @classmethod
    def from_json(cls, line: str) -> "EpisodeRecord":
        """Read a record written by ``to_json``; anything else raises ``ValueError``, ``TypeError`` or ``KeyError``."""
        document = JsonDocument.expect_dict(json.loads(line))
        reward = document["reward"]
        return cls(
            JsonDocument.expect_scalar(document["task"], str),
            None if reward is None else cls._number(reward),
            JsonDocument.expect_scalar(document["attempts"], int),
            cls._number(document["seconds"]),
            JsonDocument.expect_optional_scalar(document["error"], str),
            document["detail"],
        )

    @staticmethod
    def _number(value: object) -> float:
        """Require a JSON number, whole or not."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"expected a number, found {type(value).__name__}")
        return float(value)
