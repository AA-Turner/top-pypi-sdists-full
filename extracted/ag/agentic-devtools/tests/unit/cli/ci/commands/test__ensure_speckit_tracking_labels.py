"""Tests for ``_ensure_speckit_tracking_labels``."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.commands import _ensure_speckit_tracking_labels


@patch("agentic_devtools.cli.ci.commands._gh_api_call")
def test__ensure_speckit_tracking_labels_creates_missing_and_ignores_already_exists(mock_api) -> None:
    mock_api.side_effect = [
        json.dumps([{"name": "speckit:processing"}]),
        RuntimeError("HTTP 422 already_exists"),
    ]
    _ensure_speckit_tracking_labels(repo="owner/repo", phase=2, token="secret")
    assert mock_api.call_count == 2


@patch("agentic_devtools.cli.ci.commands._gh_api_call")
def test__ensure_speckit_tracking_labels_skips_when_already_present(mock_api) -> None:
    mock_api.return_value = json.dumps([{"name": "speckit:processing"}, {"name": "speckit:agent-assigned-phase-2"}])
    _ensure_speckit_tracking_labels(repo="owner/repo", phase=2, token="secret")
    assert mock_api.call_count == 1


@patch("agentic_devtools.cli.ci.commands._gh_api_call")
def test__ensure_speckit_tracking_labels_raises_for_non_validation_errors(mock_api) -> None:
    mock_api.side_effect = [json.dumps([]), RuntimeError("HTTP 500")]
    with pytest.raises(RuntimeError, match="HTTP 500"):
        _ensure_speckit_tracking_labels(repo="owner/repo", phase=2, token="secret")
