"""Contract representation for GitHub Agent Tasks requests."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

AGENT_TASKS_API_VERSION = "2026-03-10"
AGENT_TASKS_ENDPOINT_TEMPLATE = "/agents/repos/{owner}/{repo}/tasks"
AGENT_TASKS_HTTP_METHOD = "POST"
REQUIRED_CUSTOM_AGENT = "agdt.address-copilot-review.evaluate-and-respond"
AGENT_TASKS_VALIDATION_ORDER = ("model", "custom_agent", "base_ref")

_REQUIRED_FIELDS = frozenset(
    {
        "prompt",
        "custom_agent",
        "model",
        "base_ref",
        "head_ref",
        "create_pull_request",
    }
)


def _require_non_empty_string(field_name: str, value: object) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must be a non-empty string")


@dataclass(frozen=True)
class AgentTasksPayload:
    """The six-field request body accepted by the Agent Tasks endpoint."""

    prompt: str
    custom_agent: str
    model: str
    base_ref: str
    head_ref: str
    create_pull_request: bool

    def __post_init__(self) -> None:
        _require_non_empty_string("prompt", self.prompt)
        _require_non_empty_string("model", self.model)
        _require_non_empty_string("base_ref", self.base_ref)
        _require_non_empty_string("head_ref", self.head_ref)
        if not isinstance(self.custom_agent, str):
            raise TypeError("custom_agent must be a string")
        if self.custom_agent != REQUIRED_CUSTOM_AGENT:
            raise ValueError(f"custom_agent must be {REQUIRED_CUSTOM_AGENT!r}")
        if type(self.create_pull_request) is not bool:
            raise TypeError("create_pull_request must be a boolean")
        if self.create_pull_request is not False:
            raise ValueError("create_pull_request must be False")

    def to_dict(self) -> dict[str, Any]:
        """Return the payload in its canonical field order."""
        return {
            "prompt": self.prompt,
            "custom_agent": self.custom_agent,
            "model": self.model,
            "base_ref": self.base_ref,
            "head_ref": self.head_ref,
            "create_pull_request": self.create_pull_request,
        }


def build_agent_tasks_payload(
    prompt: str,
    model: str,
    base_ref: str,
    head_ref: str,
    custom_agent: str = REQUIRED_CUSTOM_AGENT,
    create_pull_request: bool = False,
) -> dict[str, Any]:
    """Build and validate a canonical Agent Tasks request body."""
    return AgentTasksPayload(
        prompt=prompt,
        custom_agent=custom_agent,
        model=model,
        base_ref=base_ref,
        head_ref=head_ref,
        create_pull_request=create_pull_request,
    ).to_dict()


def get_agent_tasks_headers(token: str) -> dict[str, str]:
    """Build the required headers for an Agent Tasks request."""
    _require_non_empty_string("token", token)
    if "\r" in token or "\n" in token:
        raise ValueError("token must not contain CR or LF characters")
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + token,
        "X-GitHub-Api-Version": AGENT_TASKS_API_VERSION,
    }


def validate_agent_tasks_payload(payload: Mapping[str, Any]) -> None:
    """Validate an already-constructed Agent Tasks request body."""
    if not isinstance(payload, Mapping):
        raise TypeError("payload must be a mapping")
    if set(payload) != _REQUIRED_FIELDS:
        missing = _REQUIRED_FIELDS - set(payload)
        extra = set(payload) - _REQUIRED_FIELDS
        details: list[str] = []
        if missing:
            details.append(f"missing fields: {', '.join(sorted(missing))}")
        if extra:
            details.append(f"unexpected fields: {', '.join(sorted(extra))}")
        raise ValueError("; ".join(details))
    AgentTasksPayload(**dict(payload))


def redact_authorization_header(headers: Mapping[str, str]) -> dict[str, str]:
    """Return headers with Authorization credentials replaced by a safe placeholder."""
    redacted: dict[str, str] = {}
    for key, value in headers.items():
        if key.lower() == "authorization":
            redacted[key] = "<redacted>"
        else:
            redacted[key] = value
    return redacted


def assert_headers_equal_redacted(
    actual: Mapping[str, str],
    expected: Mapping[str, str],
) -> None:
    """Compare complete headers while redacting bearer tokens in failures."""
    actual_dict = dict(actual)
    expected_dict = dict(expected)
    if actual_dict != expected_dict:
        raise AssertionError(
            "Headers differ: "
            f"{redact_authorization_header(actual_dict)!r} != "
            f"{redact_authorization_header(expected_dict)!r}"
        )


__all__ = [
    "AGENT_TASKS_API_VERSION",
    "AGENT_TASKS_ENDPOINT_TEMPLATE",
    "AGENT_TASKS_HTTP_METHOD",
    "AGENT_TASKS_VALIDATION_ORDER",
    "AgentTasksPayload",
    "REQUIRED_CUSTOM_AGENT",
    "assert_headers_equal_redacted",
    "build_agent_tasks_payload",
    "get_agent_tasks_headers",
    "redact_authorization_header",
    "validate_agent_tasks_payload",
]
