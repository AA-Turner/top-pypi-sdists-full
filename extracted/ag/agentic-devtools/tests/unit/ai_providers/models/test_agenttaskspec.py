import pytest

from agentic_devtools.ai_providers.models import AgentTaskSpec, TaskRequest


def _make_request() -> TaskRequest:
    return TaskRequest(
        model_id="test-v1",
        prompt="hello",
        context=None,
        parameters={"token": "secret"},
        metadata=None,
    )


def test_agent_task_spec_validation():
    req = _make_request()

    # Valid spec
    spec = AgentTaskSpec(
        task_id="task-123",
        provider_name="TestProvider",
        request=req,
        validation_state="passed",
        created_at="2023-01-01T00:00:00Z",
        metadata={"nested": {"api_key": "hidden"}},
    )
    assert spec.provider_name == "TestProvider"
    assert spec.request.parameters["token"] == "secret"
    assert spec.metadata["nested"]["api_key"] == "<redacted>"

    # Empty provider_name
    with pytest.raises(ValueError, match="provider_name must be a non-empty string"):
        AgentTaskSpec(
            task_id="task-123",
            provider_name="",
            request=req,
            validation_state="passed",
            created_at="2023-01-01T00:00:00Z",
            metadata={},
        )

    with pytest.raises(ValueError, match="validation_state must be one of"):
        AgentTaskSpec(
            task_id="task-123",
            provider_name="TestProvider",
            request=req,
            validation_state="unknown",
            created_at="2023-01-01T00:00:00Z",
            metadata={},
        )

    with pytest.raises(ValueError, match="created_at must be a valid ISO-8601 timestamp"):
        AgentTaskSpec(
            task_id="task-123",
            provider_name="TestProvider",
            request=req,
            validation_state="passed",
            created_at="2023-01-01",
            metadata={},
        )

    with pytest.raises(ValueError, match="created_at must be a valid ISO-8601 timestamp"):
        AgentTaskSpec(
            task_id="task-123",
            provider_name="TestProvider",
            request=req,
            validation_state="passed",
            created_at="2023-13-01T00:00:00Z",
            metadata={},
        )


def test_agent_task_spec_repr_does_not_leak_transport_parameters() -> None:
    spec = AgentTaskSpec(
        task_id="task-123",
        provider_name="TestProvider",
        request=TaskRequest(
            model_id="test-v1",
            prompt="hello",
            context=None,
            parameters={"access_token": "transport-secret"},
            metadata=None,
        ),
        validation_state="passed",
        created_at="2023-01-01T00:00:00Z",
        metadata={},
    )

    rendered = repr(spec)

    assert "transport-secret" not in rendered
    assert "access_token" not in rendered


def test_agent_task_spec_rejects_non_string_provider_name():
    req = _make_request()
    with pytest.raises(ValueError, match="provider_name must be a non-empty string"):
        AgentTaskSpec(
            task_id="task-123",
            provider_name=42,  # type: ignore[arg-type]
            request=req,
            validation_state="passed",
            created_at="2023-01-01T00:00:00Z",
            metadata={},
        )


def test_agent_task_spec_rejects_non_task_request():
    with pytest.raises(ValueError, match="request must be a TaskRequest"):
        AgentTaskSpec(
            task_id="task-123",
            provider_name="TestProvider",
            request={"model_id": "x"},  # type: ignore[arg-type]
            validation_state="passed",
            created_at="2023-01-01T00:00:00Z",
            metadata={},
        )


def test_agent_task_spec_rejects_unhashable_validation_state():
    req = _make_request()
    with pytest.raises(ValueError, match="validation_state must be one of"):
        AgentTaskSpec(
            task_id="task-123",
            provider_name="TestProvider",
            request=req,
            validation_state=["pending"],  # type: ignore[arg-type]
            created_at="2023-01-01T00:00:00Z",
            metadata={},
        )


def test_agent_task_spec_rejects_non_string_task_id():
    req = _make_request()
    with pytest.raises(
        ValueError,
        match=r"task_id must be a non-empty string matching \^\[A-Za-z0-9_-\]\+\$",
    ):
        AgentTaskSpec(
            task_id=42,  # type: ignore[arg-type]
            provider_name="TestProvider",
            request=req,
            validation_state="passed",
            created_at="2023-01-01T00:00:00Z",
            metadata={},
        )


@pytest.mark.parametrize("task_id", ["", "bad id", "slash/value"])
def test_agent_task_spec_rejects_malformed_task_id(task_id: str):
    req = _make_request()
    with pytest.raises(
        ValueError,
        match=r"task_id must be a non-empty string matching \^\[A-Za-z0-9_-\]\+\$",
    ):
        AgentTaskSpec(
            task_id=task_id,
            provider_name="TestProvider",
            request=req,
            validation_state="passed",
            created_at="2023-01-01T00:00:00Z",
            metadata={},
        )
