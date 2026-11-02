from __future__ import annotations

import pytest

from agentic_devtools.cli import pull_request_approval as commands


@pytest.mark.parametrize(
    ("state", "key", "expected"),
    [
        ({"platform.code_hosting": "github"}, "platform.code_hosting", "github"),
        ({"platform": {"code_hosting": "azure_devops"}}, "platform.code_hosting", "azure_devops"),
        ({"platform": None}, "platform.code_hosting", None),
        ({}, "platform.code_hosting", None),
    ],
)
def test_state_value_resolves_flat_nested_and_missing_keys(
    state: dict[str, object], key: str, expected: object
) -> None:
    assert commands._state_value(state, key) == expected
