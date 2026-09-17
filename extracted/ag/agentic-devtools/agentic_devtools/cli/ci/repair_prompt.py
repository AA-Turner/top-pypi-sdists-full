"""Structured repair prompt serialization."""

from __future__ import annotations

import re
from dataclasses import dataclass

from agentic_devtools.cli.ci.dispatch_state import MAX_DISPATCHES_PER_SHA

_REPO_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")

CANONICAL_EXECUTION_INSTRUCTIONS = (
    "Execute agdt.address-copilot-review.evaluate-and-respond using the supplied structured "
    "repair context. Resolve the repair request, make only necessary changes, run focused "
    "validation, and report the result."
)


def _positive_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _artifact(value: object, name: str, *, optional: bool = False) -> str | None:
    if optional and value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    return value


@dataclass(frozen=True)
class RepairPromptInput:
    """Validated context used to serialize one repair-dispatch prompt."""

    repo: str
    pull_request_id: int
    sha: str
    ordinal: int
    review_context: str
    ci_diagnostics: str
    prior_round_state: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.repo, str) or not _REPO_RE.fullmatch(self.repo):
            raise ValueError("repo must be a non-empty canonical lowercase repository name")
        _positive_int(self.pull_request_id, "pull_request_id")
        if not isinstance(self.sha, str) or not _SHA_RE.fullmatch(self.sha):
            raise ValueError("sha must be a 40-character lowercase hexadecimal string")
        _positive_int(self.ordinal, "ordinal")
        if self.ordinal > MAX_DISPATCHES_PER_SHA:
            raise ValueError(f"ordinal must not exceed {MAX_DISPATCHES_PER_SHA}")
        _artifact(self.review_context, "review_context")
        _artifact(self.ci_diagnostics, "ci_diagnostics")
        _artifact(self.prior_round_state, "prior_round_state", optional=True)


def serialize_repair_prompt(prompt_input: RepairPromptInput) -> str:
    """Serialize validated repair context with deterministic section boundaries."""
    if not isinstance(prompt_input, RepairPromptInput):
        raise ValueError("prompt_input must be a RepairPromptInput")

    token = (
        f"agdt-dispatch-{prompt_input.repo}-{prompt_input.pull_request_id}-{prompt_input.sha}-{prompt_input.ordinal}"
    )
    prior_round_state = "none" if prompt_input.prior_round_state is None else prompt_input.prior_round_state
    return (
        f"{token}\n\n"
        "## Header / Metadata\n"
        f"correlation_token: {token}\n"
        f"repo: {prompt_input.repo}\n"
        f"pull_request_id: {prompt_input.pull_request_id}\n"
        f"sha: {prompt_input.sha}\n"
        f"ordinal: {prompt_input.ordinal}\n\n"
        f"## Review Comments & Context\n{prompt_input.review_context}\n\n"
        f"## CI Failure Diagnostics / Condensed Logs\n{prompt_input.ci_diagnostics}\n\n"
        f"## Prior-round Resolution State\n{prior_round_state}\n\n"
        f"## Execution Instructions\n{CANONICAL_EXECUTION_INSTRUCTIONS}\n"
    )
