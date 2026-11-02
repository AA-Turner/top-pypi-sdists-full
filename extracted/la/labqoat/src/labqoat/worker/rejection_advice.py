"""What to do about a worker command the platform refused, by its reason code."""

from typing import ClassVar


class RejectionAdvice:
    """One sentence per refusal whose fix is not obvious from its code."""

    ADVICE: ClassVar[dict[str, str]] = {
        "child_input_not_authorized": (
            ". A child run may receive only the artifacts, datasets and checkpoints its parent received as arguments "
            "or produced itself, and only functions published with the parent. To reuse an earlier run's output, "
            "pass it to this run as an Artifact, Dataset or Checkpoint argument and hand it on."
        ),
    }

    @staticmethod
    def explain(reason: str | None) -> str:
        """The advice to append to a refusal's message, or nothing for a self-explanatory code."""
        return RejectionAdvice.ADVICE.get(reason or "", "")
