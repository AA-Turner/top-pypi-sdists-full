"""Build the reflection prompt handed to the reflector subagent."""

from pathlib import Path

from dreadnode.agents.events import AgentEnd
from self_improvement_lib.classifier import ClassifiedFailure


def build_reflection_goal(
    failures: list[ClassifiedFailure],
    end_event: AgentEnd,
    proposed_dir: Path,
) -> str:
    lines = [
        "An agent run just ended with recoverable failures that may indicate",
        "a gap in the skill library. Decide whether a new or updated skill",
        "would help future runs avoid this class of failure.",
        "",
        f"Stop reason: {end_event.stop_reason}",
        f"Proposed skills directory: {proposed_dir}",
        f"Failures observed ({len(failures)}):",
    ]
    for failure in failures:
        subject = failure.subject or "(n/a)"
        lines.append(f"  - {failure.kind.value} on {subject}: {failure.sample}")
    lines.extend(
        [
            "",
            "Principles:",
            "- Be conservative. If failures look one-off or environmental, do nothing.",
            "- Prefer updating an existing proposed skill to creating a new one.",
            "- Skill instructions must be concrete: 'when you see X, do Y'.",
            "- If you make a change, call write_skill or update_skill and then stop.",
        ]
    )
    return "\n".join(lines)
