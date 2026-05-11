"""Item #17 — PR-aware sessions."""

from __future__ import annotations

import re
from dataclasses import dataclass

__all__ = ["PRTarget", "parse_pr_target"]


@dataclass
class PRTarget:
    number: int
    owner: str = ""
    repo: str = ""


_PR_URL_RE = re.compile(
    r"https?://github\.com/([\w.-]+)/([\w.-]+)/pull/(\d+)"
)
_PR_BARE_RE = re.compile(r"^#?(\d+)$")


def parse_pr_target(target: str) -> PRTarget | None:
    if not target:
        return None
    target = target.strip()

    m = _PR_URL_RE.match(target)
    if m:
        return PRTarget(
            number=int(m.group(3)),
            owner=m.group(1),
            repo=m.group(2),
        )

    m = _PR_BARE_RE.match(target)
    if m:
        return PRTarget(number=int(m.group(1)))

    return None
