"""Tests for variable document validation."""

import json

import pytest

from agentic_devtools.cli.ci.cooldown_document import _variable_payload


class TestVariablePayload:
    def test_missing_and_valid_documents(self):
        assert _variable_payload(None) == {}
        assert _variable_payload('{"future": 1}') == {"future": 1}

    def test_malformed_documents_are_not_silently_reset(self):
        with pytest.raises(json.JSONDecodeError):
            _variable_payload("{")
        with pytest.raises(ValueError):
            _variable_payload("[]")
