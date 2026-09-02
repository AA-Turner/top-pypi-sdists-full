"""Initiate node: validate LLM config and detect issue provider.

Entry point for the work-on-issue workflow. Validates that the LLM
provider configuration exists and determines whether the issue is
from Jira or GitHub based on the key format.
"""

from __future__ import annotations

from typing import Any

from agentic_devtools.orchestration.nodes._helpers import detect_issue_provider, normalize_issue_key, utc_now
from agentic_devtools.orchestration.state_schema import WorkOnIssueState


def initiate_node(state: WorkOnIssueState) -> dict[str, Any]:
    """Validate LLM config and detect issue provider.

    Reads the issue key from state, detects the provider (Jira vs GitHub),
    validates that an LLM provider is configured, and sets routing signals.

    Fails fast with ``ProviderNotConfiguredError`` info in the error field
    if no LLM provider configuration is found.
    """
    issue_key = state.get("issue_key", "")

    # Fail fast when issue_key is missing, blank, or not a string — downstream
    # nodes (retrieve, pull_request, completion) all require a valid key, and
    # detect_issue_provider("") silently returns "github" which produces
    # confusing failures later.
    if not isinstance(issue_key, str) or not issue_key.strip():
        _missing_error = "issue_key is required and must be a non-empty string"
        return {
            "step": "initiate",
            "status": "failed",
            "error": _missing_error,
            "events": [
                {
                    "event": "initiate_failed",
                    "timestamp": utc_now(),
                    "signals": {"error": "missing_issue_key"},
                }
            ],
        }

    normalized_key = normalize_issue_key(issue_key)
    if not normalized_key:
        invalid_error = "issue_key must normalize to a non-empty issue identifier"
        return {
            "step": "initiate",
            "status": "failed",
            "error": invalid_error,
            "events": [
                {
                    "event": "initiate_failed",
                    "timestamp": utc_now(),
                    "signals": {"error": "invalid_issue_key"},
                }
            ],
        }

    # Detect issue provider from key format
    issue_provider = detect_issue_provider(issue_key)

    # Validate LLM configuration exists
    llm_config_error = _validate_llm_config()
    if llm_config_error:
        return {
            "step": "initiate",
            "status": "failed",
            "error": llm_config_error,
            "issue_provider": issue_provider,
            "events": [
                {
                    "event": "initiate_failed",
                    "timestamp": utc_now(),
                    "signals": {"error": llm_config_error},
                }
            ],
        }

    # Translate any pre-flight error (e.g., wrong worktree/branch) into the
    # ``needs_setup`` routing signal. ``issue_retrieved`` is intentionally NOT set
    # here: it means "the issue was actually fetched" and is set solely by
    # ``retrieve_node`` (and read by ``route_after_retrieve``). Setting it in this
    # node would overload the signal with a second meaning ("pre-flight OK").
    # ``route_after_initiate`` always proceeds to ``setup`` when there is no error.
    pre_flight_error = state.get("error")
    needs_setup = bool(pre_flight_error)

    # Include the original pre-flight error detail in signals to aid diagnostics
    # when reviewing workflow events / checkpoints. Only include when it is a
    # non-empty string; truthy non-string values (e.g. dicts from corrupted state)
    # are omitted to keep the signal payload consistent.
    signals: dict[str, Any] = {
        "needs_setup": needs_setup,
        "issue_provider": issue_provider,
    }
    if isinstance(pre_flight_error, str) and pre_flight_error:
        signals["pre_flight_error_detail"] = pre_flight_error

    return {
        "step": "initiate",
        "status": "active",
        "error": None,
        "issue_provider": issue_provider,
        "needs_setup": needs_setup,
        "events": [
            {
                "event": "initiate_completed",
                "timestamp": utc_now(),
                "signals": signals,
            }
        ],
    }


def _validate_llm_config() -> str | None:
    """Validate LLM provider configuration exists.

    Returns:
        Error message string if configuration is invalid, None if valid.
    """
    try:
        from agentic_devtools.orchestration.llm.config import load_config

        config = load_config()
        if not config.providers:
            return (
                "ProviderNotConfiguredError: No LLM providers configured in "
                ".agdt/config/llm-providers.yml. Configure at least one provider "
                "before running the workflow."
            )
        return None
    except Exception as exc:
        return f"ProviderNotConfiguredError: Failed to load LLM config: {exc}"
