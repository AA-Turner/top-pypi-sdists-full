from collections.abc import Mapping
from types import MappingProxyType
from typing import Any, cast

import pytest

from agentic_devtools.ai_providers.models import TaskRequest


def test_task_request_validates_and_freezes_payload_fields() -> None:
    parameters: dict[str, Any] = {"token": "transport-secret", "nested": {"safe": [1]}}
    metadata: dict[str, Any] = {"api_key": "hidden"}

    request = TaskRequest(
        model_id="model-1",
        prompt="hello",
        context="prior context",
        parameters=parameters,
        metadata=metadata,
    )
    nested = cast(Mapping[str, object], request.parameters["nested"])
    request_metadata = cast(Mapping[str, object], request.metadata)

    # parameters must reach the provider verbatim — no redaction
    assert request.parameters["token"] == "transport-secret"
    assert cast(tuple[int, ...], nested["safe"]) == (1,)
    # metadata is an audit artifact — credentials are redacted
    assert request_metadata["api_key"] == "<redacted>"
    assert isinstance(request.parameters, MappingProxyType)

    parameters["nested"]["safe"].append(2)
    assert cast(tuple[int, ...], nested["safe"]) == (1,)


def test_task_request_repr_omits_verbatim_transport_parameters() -> None:
    request = TaskRequest(
        model_id="model-1",
        prompt="hello",
        context=None,
        parameters={"access_token": "transport-secret"},
        metadata={"api_key": "hidden"},
    )

    rendered = repr(request)

    assert "parameters=" not in rendered
    assert "transport-secret" not in rendered
    assert "<redacted>" in rendered


@pytest.mark.parametrize("model_id", ["", None, 1])
def test_task_request_rejects_invalid_model_id(model_id: object) -> None:
    with pytest.raises(ValueError, match="model_id must be a non-empty string"):
        TaskRequest(
            model_id=model_id,  # type: ignore[arg-type]
            prompt="hello",
            context=None,
            parameters={},
            metadata=None,
        )


@pytest.mark.parametrize(
    ("field_name", "kwargs", "message"),
    [
        (
            "prompt",
            {"model_id": "model-1", "prompt": 123, "context": None, "parameters": {}, "metadata": None},
            "prompt must be a string",
        ),
        (
            "context",
            {"model_id": "model-1", "prompt": "hello", "context": [], "parameters": {}, "metadata": None},
            "context must be a string or None",
        ),
    ],
)
def test_task_request_rejects_invalid_prompt_or_context_types(
    field_name: str,
    kwargs: dict[str, object],
    message: str,
) -> None:
    del field_name

    with pytest.raises(ValueError, match=message):
        TaskRequest(**kwargs)  # type: ignore[arg-type]
