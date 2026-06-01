# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for `airbyte_ops_mcp.connector_secrets.ci_masks`."""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

import pytest

from airbyte_ops_mcp.connector_secrets import ci_masks


@pytest.mark.parametrize(
    "config,expected_calls",
    [
        ({"password": "secret123", "regular": "value"}, ["secret123"]),
        ({"outer": {"api_key": "keyval"}}, ["keyval"]),
        ([{"token": "tok1"}, {"name": "v"}], ["tok1"]),
        ({"passwords": ["a", "b"]}, ["a", "b"]),
        ({"password": "multi\nline\nsecret"}, ["multi", "line", "secret"]),
        ({"a": [{"b": {"secret": "deep"}}]}, ["deep"]),
        ({"foo": "bar"}, []),
        ({"password": ["a", 123, {"nested": "val"}]}, ["a", "123", "val"]),
        ([{"password": "foo"}], ["foo"]),
    ],
)
def test_print_ci_secrets_masks_for_config(
    config: Any,
    expected_calls: list[str],
) -> None:
    with patch(
        "airbyte_ops_mcp.connector_secrets.ci_masks.get_spec_mask",
        return_value=["password", "api_key", "token", "secret"],
    ), patch(
        "airbyte_ops_mcp.connector_secrets.ci_masks.print_ci_secret_mask_for_string",
    ) as mask_mock:
        ci_masks.print_ci_secrets_masks_for_config(config)
        actual_calls = [str(call.args[0]) for call in mask_mock.call_args_list]
        assert sorted(actual_calls) == sorted(expected_calls)
