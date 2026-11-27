from typing import Any

import pytest
from pydantic import TypeAdapter, ValidationError

from mistralai.workflows.protocol.v1.workflow import CallContext, call_context_to_payload

call_context = TypeAdapter(CallContext)

# 16 keys of 247 characters serialise to 4097 bytes; shortening one value by a character gives 4096.
AT_SIZE_LIMIT = {f"k{i:02d}": "v" * (246 if i == 15 else 247) for i in range(16)}
OVER_SIZE_LIMIT = {f"k{i:02d}": "v" * 247 for i in range(16)}


def test_size_fixtures_sit_on_each_side_of_the_limit() -> None:
    assert len(call_context_to_payload(AT_SIZE_LIMIT).data) == 4096
    assert len(call_context_to_payload(OVER_SIZE_LIMIT).data) == 4097


@pytest.mark.parametrize(
    "value",
    [
        None,
        {},
        {"command_id": "6f1c2a3e-6b1d-5c4e-9a8b-1f2e3d4c5b6a", "turn_id": "turn_42", "tracing": True},
        {"attempt": 3, "session_id": "sess:abc/def@v1.2"},
        {"largest": 2**53 - 1, "smallest": -(2**53 - 1)},
        {f"key_{i}": i for i in range(16)},
        AT_SIZE_LIMIT,
    ],
)
def test_accepts_small_technical_values(value: Any) -> None:
    assert call_context.validate_python(value) == value


@pytest.mark.parametrize(
    "value",
    [
        pytest.param({"Command-Id": "x"}, id="key-not-snake-case"),
        pytest.param({"1st": "x"}, id="key-starts-with-digit"),
        pytest.param({"k" * 65: "x"}, id="key-too-long"),
        pytest.param({"note": "hello world"}, id="free-form-text"),
        pytest.param({"note": ""}, id="empty-string"),
        pytest.param({"note": "x" * 257}, id="string-too-long"),
        pytest.param({"ratio": 0.5}, id="float"),
        pytest.param({"too_big": 2**53}, id="int-above-javascript-precision"),
        pytest.param({"too_small": -(2**53)}, id="int-below-javascript-precision"),
        pytest.param({"nested": {"a": "b"}}, id="nested-object"),
        pytest.param({"ids": ["a", "b"]}, id="list"),
        pytest.param({"missing": None}, id="null"),
        pytest.param({f"key_{i}": i for i in range(17)}, id="too-many-keys"),
        pytest.param(OVER_SIZE_LIMIT, id="serialized-too-large"),
    ],
)
def test_rejects_values_that_could_carry_content(value: Any) -> None:
    with pytest.raises(ValidationError):
        call_context.validate_python(value)
