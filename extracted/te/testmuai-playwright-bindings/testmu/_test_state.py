"""Per-test verdict state — tracks fail-continue swallows for end-of-test routing."""
from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass(frozen=True)
class Verdict:
    failed: bool
    first_error: Optional[BaseException]
    count: int


_failed_steps: List[Tuple[str, BaseException]] = []


def reset() -> None:
    _failed_steps.clear()


def mark_step_failed(description: str, error: BaseException) -> None:
    _failed_steps.append((description, error))


def get_verdict() -> Verdict:
    if not _failed_steps:
        return Verdict(failed=False, first_error=None, count=0)
    _, first = _failed_steps[0]
    return Verdict(failed=True, first_error=first, count=len(_failed_steps))
