"""Static guards: sensitive-paths regex pass + budget caps."""

import re

from .models import RunConfig, RunResult, Ticket

OVERRIDE_LABEL = "agent-override-sensitive"

SENSITIVE_PATTERNS: list[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"\bauth(entication)?\b",
        r"\boauth\b",
        r"\blogin\b",
        r"\bsecret(s)?\b",
        r"\bcredentials?\b",
        r"\.env\b",
        r"\bmigration(s)?\b",
        r"\balembic\b",
        r"\bterraform\b",
        r"\bkubernetes\b",
        r"\bk8s\b",
        r"\binfra\b",
        r"\bbilling\b",
        r"\bpayment(s)?\b",
        r"\bstripe\b",
        r"\brotate\b.{0,20}\bsecret",
    ]
]


def has_sensitive_keywords(ticket: Ticket) -> bool:
    # Labels are organizational metadata (e.g. `Infra`, `Security`), not scope
    # signals — matching on them produces false positives that block safe CI/doc
    # tickets. Sensitive scope must be inferable from title/description.
    haystack = f"{ticket.title}\n{ticket.description or ''}"
    return any(p.search(haystack) for p in SENSITIVE_PATTERNS)


def has_override(ticket: Ticket) -> bool:
    return OVERRIDE_LABEL in ticket.labels


def budget_exhausted(result: RunResult, cfg: RunConfig, elapsed_seconds: int) -> bool:
    if len(result.outcomes) >= cfg.max_tickets:
        return True
    if result.total_tokens >= cfg.max_tokens:
        return True
    if elapsed_seconds >= cfg.timeout_seconds:
        return True
    return False
