from typing import Any, cast

import pytest

from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module


def test_rejects_non_mapping_evidence() -> None:
    with pytest.raises(ValueError):
        dispatch_state_module._bounded_evidence(cast(Any, []))


def test_rejects_oversized_evidence() -> None:
    with pytest.raises(ValueError):
        dispatch_state_module._bounded_evidence({str(index): "é" * 512 for index in range(5)})


def test_filters_sensitive_credential_aliases_and_key_tokens() -> None:
    bounded = dispatch_state_module._bounded_evidence(
        {
            "apikey": "secret",
            "pat": "secret",
            "auth": "secret",
            "credentials": "secret",
            "request_body": "secret",
            "response_headers": "secret",
            "authorization_header": "secret",
            "task_prompt": "secret",
            "private_key": "secret",
            "key": "secret",
            "nested": {"safe": "value", "secret_key": "secret"},
        }
    )

    assert bounded == {"nested": {"safe": "value"}}


def test_redacts_serialized_secrets_in_string_values() -> None:
    bounded = dispatch_state_module._bounded_evidence(
        {"message": '{"token":"secret","authorization":"******","private_key":"pem"}'}
    )

    assert bounded == {"message": '{"token":[REDACTED],"authorization":[REDACTED],"private_key":[REDACTED]}'}


def test_replaces_recursive_containers_with_stable_placeholder() -> None:
    nested: dict[str, Any] = {}
    nested["self"] = nested
    items: list[Any] = []
    items.append(items)

    bounded = dispatch_state_module._bounded_evidence({"dict": nested, "list": items})

    assert bounded == {
        "dict": {"self": dispatch_state_module._EVIDENCE_CYCLE_PLACEHOLDER},
        "list": [dispatch_state_module._EVIDENCE_CYCLE_PLACEHOLDER],
    }


def test_replaces_excessive_nesting_with_stable_placeholder() -> None:
    nested: dict[str, Any] = {"value": "leaf"}
    for _ in range(dispatch_state_module._MAX_EVIDENCE_DEPTH + 5):
        nested = {"next": nested}

    bounded = dispatch_state_module._bounded_evidence(nested)

    cursor: Any = bounded
    for _ in range(dispatch_state_module._MAX_EVIDENCE_DEPTH):
        assert isinstance(cursor, dict)
        cursor = cursor["next"]
    assert cursor == dispatch_state_module._EVIDENCE_DEPTH_PLACEHOLDER
