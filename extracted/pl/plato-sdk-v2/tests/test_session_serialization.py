"""Tests for Session serialization/deserialization."""

import pytest

from plato.v2 import SerializedSession
from plato.v2.async_.session import SerializedEnv


class TestSerializedSession:
    """Test SerializedSession model."""

    def test_serialization_roundtrip(self):
        """Test that SerializedSession can be serialized and deserialized."""
        # Create a serialized session with test data
        original = SerializedSession(
            session_id="test-session-123",
            task_public_id=None,
            envs=[
                SerializedEnv(
                    job_id="job-abc",
                    alias="runtime",
                    artifact_id="62cc14ff-8f0c-470b-ab47-5a7f022a86f1",
                    simulator="code",
                ),
            ],
            api_key="test-api-key",
            base_url="https://plato.so",
            closed=False,
        )

        # Serialize to dict (what gets passed through JSON config)
        serialized_dict = original.model_dump()

        # Verify dict structure
        assert serialized_dict["session_id"] == "test-session-123"
        assert serialized_dict["api_key"] == "test-api-key"
        assert serialized_dict["base_url"] == "https://plato.so"
        assert serialized_dict["closed"] is False
        assert len(serialized_dict["envs"]) == 1
        assert serialized_dict["envs"][0]["artifact_id"] == "62cc14ff-8f0c-470b-ab47-5a7f022a86f1"
        assert serialized_dict["envs"][0]["simulator"] == "code"

        # Deserialize back to model
        restored = SerializedSession.model_validate(serialized_dict)

        # Verify all fields match
        assert restored.session_id == original.session_id
        assert restored.task_public_id == original.task_public_id
        assert restored.api_key == original.api_key
        assert restored.base_url == original.base_url
        assert restored.closed == original.closed
        assert len(restored.envs) == len(original.envs)
        assert restored.envs[0].job_id == original.envs[0].job_id
        assert restored.envs[0].alias == original.envs[0].alias
        assert restored.envs[0].artifact_id == original.envs[0].artifact_id
        assert restored.envs[0].simulator == original.envs[0].simulator

    def test_serialization_with_multiple_envs(self):
        """Test serialization with multiple environments."""
        original = SerializedSession(
            session_id="multi-env-session",
            task_public_id="task-xyz",
            envs=[
                SerializedEnv(
                    job_id="job-1",
                    alias="runtime",
                    artifact_id="62cc14ff-8f0c-470b-ab47-5a7f022a86f1",
                    simulator="code",
                ),
                SerializedEnv(
                    job_id="job-2",
                    alias="database",
                    artifact_id="another-artifact-id",
                    simulator="postgres",
                ),
            ],
            api_key="multi-env-key",
            base_url="https://staging.plato.so",
            closed=False,
        )

        # Roundtrip
        serialized_dict = original.model_dump()
        restored = SerializedSession.model_validate(serialized_dict)

        assert len(restored.envs) == 2
        assert restored.envs[0].alias == "runtime"
        assert restored.envs[1].alias == "database"
        assert restored.task_public_id == "task-xyz"

    def test_serialization_minimal(self):
        """Test serialization with minimal required fields."""
        original = SerializedSession(
            session_id="minimal-session",
            envs=[],
            api_key="minimal-key",
        )

        serialized_dict = original.model_dump()
        restored = SerializedSession.model_validate(serialized_dict)

        assert restored.session_id == "minimal-session"
        assert restored.envs == []
        assert restored.api_key == "minimal-key"
        assert restored.base_url is None
        assert restored.task_public_id is None
        assert restored.closed is False

    def test_json_string_roundtrip(self):
        """Test that serialization works through JSON string (simulating config file)."""
        import json

        original = SerializedSession(
            session_id="json-test-session",
            envs=[
                SerializedEnv(
                    job_id="job-json",
                    alias="runtime",
                    artifact_id="62cc14ff-8f0c-470b-ab47-5a7f022a86f1",
                    simulator="code",
                ),
            ],
            api_key="json-api-key",
            base_url="https://plato.so",
            closed=False,
        )

        # Serialize to JSON string (what happens when writing config file)
        json_str = json.dumps(original.model_dump())

        # Parse JSON (what happens when reading config file)
        parsed_dict = json.loads(json_str)

        # Restore model
        restored = SerializedSession.model_validate(parsed_dict)

        assert restored.session_id == original.session_id
        assert restored.api_key == original.api_key
        assert restored.envs[0].artifact_id == "62cc14ff-8f0c-470b-ab47-5a7f022a86f1"


@pytest.mark.asyncio
async def test_session_load_from_serialized():
    """Test Session.load() restores session from SerializedSession.

    This simulates the Chronos -> World Runner flow:
    1. Chronos calls session.dump() and passes it in config
    2. World runner calls Session.load() to restore the session
    """
    from unittest.mock import MagicMock, patch

    from plato.v2.async_.session import Session

    # Create a SerializedSession (what Chronos would pass)
    serialized = SerializedSession(
        session_id="chronos-session-123",
        task_public_id=None,
        envs=[
            SerializedEnv(
                job_id="runtime-job-id",
                alias="runtime",
                artifact_id="62cc14ff-8f0c-470b-ab47-5a7f022a86f1",
                simulator="code",
            ),
        ],
        api_key="user-api-key",
        base_url="https://plato.so",
        closed=False,
    )

    # Mock the httpx client to avoid actual network calls
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        # Load session without starting heartbeat (to avoid background task)
        session = await Session.load(serialized, start_heartbeat=False)

        # Verify session was restored correctly
        assert session.session_id == "chronos-session-123"
        assert session._api_key == "user-api-key"
        assert len(session.envs) == 1
        assert session.envs[0].alias == "runtime"
        assert session.envs[0].job_id == "runtime-job-id"
        assert session.envs[0].artifact_id == "62cc14ff-8f0c-470b-ab47-5a7f022a86f1"


@pytest.mark.asyncio
async def test_session_heartbeat_uses_api_key():
    """Test that heartbeat uses the API key from serialized session.

    This verifies the critical flow:
    1. Session is restored from SerializedSession
    2. Heartbeat is called
    3. The API key from SerializedSession is used in the request
    """
    from unittest.mock import AsyncMock, MagicMock, patch

    import httpx

    from plato.v2.async_.session import Session

    # Create a SerializedSession with a specific API key
    serialized = SerializedSession(
        session_id="heartbeat-test-session",
        task_public_id=None,
        envs=[
            SerializedEnv(
                job_id="runtime-job-id",
                alias="runtime",
                artifact_id="62cc14ff-8f0c-470b-ab47-5a7f022a86f1",
                simulator="code",
            ),
        ],
        api_key="test-heartbeat-api-key",
        base_url="https://plato.so",
        closed=False,
    )

    # Create a real httpx client but mock the request method
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "session_id": "heartbeat-test-session",
        "timestamp": "2024-01-01T00:00:00Z",
        "results": {},
    }

    async with httpx.AsyncClient(base_url="https://plato.so") as client:
        # Patch the request method to capture the call
        with patch.object(client, "request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = mock_response

            # Load session with the real client
            session = await Session.load(
                serialized,
                http_client=client,
                start_heartbeat=False,
            )

            # Verify API key is stored
            assert session._api_key == "test-heartbeat-api-key"

            # Call heartbeat
            await session.heartbeat()

            # Verify the request was made with the correct API key
            mock_request.assert_called_once()
            call_kwargs = mock_request.call_args
            # The headers should contain the API key
            assert call_kwargs.kwargs.get("headers", {}).get("X-API-Key") == "test-heartbeat-api-key"
