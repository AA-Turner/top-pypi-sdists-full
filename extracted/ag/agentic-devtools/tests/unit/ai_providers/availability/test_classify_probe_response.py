import pytest

from agentic_devtools.ai_providers.availability import classify_probe_response
from agentic_devtools.ai_providers.errors import ProviderError


@pytest.mark.parametrize(
    ("status_code", "body", "expected"),
    [
        (400, "Invalid model: claude-sonnet-4.6 is not supported", "REJECTED"),
        (412, "base_ref 'refs/heads/does-not-exist' was not found", "ACCEPTED"),
        (
            412,
            "model claude-opus-5 accepted; base_ref 'refs/heads/does-not-exist' was not found",
            "ACCEPTED",
        ),
        (412, "base_ref 'refs/heads/feature;foo' was not found", "ACCEPTED"),
        (412, "base_ref 'refs/heads/feature,but' was not found", "ACCEPTED"),
        (412, "base_ref `refs/heads/feature;foo` was not found", "ACCEPTED"),
        (412, "base_ref 'refs/heads/release/1.2' was not found", "ACCEPTED"),
        (412, "base_ref is invalid", "ACCEPTED"),
        (412, "base_ref is missing", "ACCEPTED"),
        (412, "base_ref is invalidated", "INVALID_INPUT"),
        (412, "base_ref 'refs/heads/does-not-exist' is invalid", "ACCEPTED"),
        (412, "base_ref 'refs/heads/does-not-exist' is missing", "ACCEPTED"),
        (401, "Unauthorized", "AUTH_ERROR"),
        (403, "Forbidden", "AUTH_ERROR"),
        (429, "Rate limited", "RETRYABLE_ERROR"),
        (500, "Upstream timeout", "RETRYABLE_ERROR"),
        (400, "malformed request body", "INVALID_INPUT"),
        (400, "custom_agent is not valid", "INVALID_INPUT"),
        (400, "custom_agent not found for model claude-opus-5", "INVALID_INPUT"),
        (412, "task accepted but body was empty", "INVALID_INPUT"),
        (412, "base_ref validation succeeded; custom_agent failed", "INVALID_INPUT"),
        # "invalid" appears in the body but refers to custom_agent, not base_ref
        (412, "base_ref validation succeeded; custom_agent is invalid", "INVALID_INPUT"),
        (412, "custom_agent ref not found", "INVALID_INPUT"),
        # Mixed-surface bodies: failure signal ("not found") is in a different clause
        # from the base_ref mention — must not be classified as ACCEPTED.
        (412, "base_ref validation succeeded; custom_agent is not found", "INVALID_INPUT"),
        (412, "base_ref is valid; model not found", "INVALID_INPUT"),
        # Sentence boundary: "not found" follows a full-stop sentence boundary rather than
        # appearing in the same clause as the base_ref marker.
        (412, "base_ref validation succeeded. custom_agent is not found", "INVALID_INPUT"),
        (412, "base_ref validation succeeded in phase 1. custom_agent is not found", "INVALID_INPUT"),
        (412, "base_ref validation succeeded, but custom_agent is not found", "INVALID_INPUT"),
        (412, "custom_agent is not found while base_ref validation succeeded", "INVALID_INPUT"),
        (412, "base_ref validation succeeded and custom_agent is not found", "INVALID_INPUT"),
        (412, "base_ref validation pending and repository not found", "INVALID_INPUT"),
        (412, "base_ref validation pending and repository ref not found", "INVALID_INPUT"),
        # Escaped apostrophe in a single-quoted ref value must not truncate the match
        (412, "base_ref 'refs/heads/it\\'s-gone' was not found", "ACCEPTED"),
    ],
)
def test_classify_probe_response(status_code: int, body: str, expected: str) -> None:
    assert classify_probe_response(status_code, body) == expected


@pytest.mark.parametrize(
    ("bad_status_code", "message"),
    [
        (True, "status_code must be an integer"),
        ("bad", "status_code must be an integer"),
    ],
)
def test_classify_probe_response_rejects_invalid_status_code(bad_status_code: object, message: str) -> None:
    with pytest.raises(ProviderError, match=message):
        classify_probe_response(bad_status_code)  # type: ignore[arg-type]


def test_classify_probe_response_tracks_invalid_unclassified_statuses() -> None:
    assert classify_probe_response(200, "accepted but not a task response") == "INVALID_INPUT"
    assert classify_probe_response(422, "unprocessable") == "INVALID_INPUT"


def test_classify_probe_response_rejects_non_canonical_validation_order() -> None:
    with pytest.raises(ProviderError, match="validation_order must be exactly"):
        classify_probe_response(400, "invalid model", validation_order=("custom_agent", "model", "base_ref"))
