from __future__ import annotations

from contextlib import nullcontext
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mistralai.client import models as mistralai_models

from mistralai.workflows.plugins.mistralai import activities
from mistralai.workflows.plugins.mistralai.connectors.run_as import ConnectorRunAs
from mistralai.workflows.plugins.mistralai.models import AgentUpdateRequest, ConversationAppendRequest

_PATCH_CLIENT = "mistralai.workflows.plugins.mistralai.activities.get_mistral_client"
_PATCH_STREAM = "mistralai.workflows.plugins.mistralai.activities.handle_conversation_stream"

_NO_RUN_AS = object()


def _client() -> MagicMock:
    client = MagicMock()
    client.beta.agents.create_async = AsyncMock(return_value=MagicMock())
    client.beta.agents.update_async = AsyncMock(return_value=MagicMock())
    client.beta.conversations.start_async = AsyncMock(return_value=MagicMock())
    client.beta.conversations.append_async = AsyncMock(return_value=MagicMock())
    client.beta.conversations.start_stream_async = AsyncMock(return_value=MagicMock())
    client.beta.conversations.append_stream_async = AsyncMock(return_value=MagicMock())
    return client


class TestConversationActivitiesForwardRunAs:
    @pytest.mark.parametrize(
        ("activity", "request_factory", "stream", "run_as", "expected"),
        [
            pytest.param(
                activities.mistralai_create_agent,
                lambda: mistralai_models.CreateAgentRequest(model="m", name="n"),
                False,
                ConnectorRunAs.DEPLOYMENT,
                ConnectorRunAs.DEPLOYMENT,
                id="create_agent",
            ),
            pytest.param(
                activities.mistralai_update_agent,
                lambda: AgentUpdateRequest(agent_id="ag_1"),
                False,
                ConnectorRunAs.DEPLOYMENT,
                ConnectorRunAs.DEPLOYMENT,
                id="update_agent",
            ),
            pytest.param(
                activities.mistralai_start_conversation,
                lambda: mistralai_models.ConversationRequest(inputs="hi"),
                False,
                ConnectorRunAs.DEPLOYMENT,
                ConnectorRunAs.DEPLOYMENT,
                id="start_conversation",
            ),
            pytest.param(
                activities.mistralai_append_conversation,
                lambda: ConversationAppendRequest(conversation_id="c", inputs="hi"),
                False,
                ConnectorRunAs.DEPLOYMENT,
                ConnectorRunAs.DEPLOYMENT,
                id="append_conversation",
            ),
            pytest.param(
                activities.mistralai_start_conversation,
                lambda: mistralai_models.ConversationRequest(inputs="hi"),
                False,
                _NO_RUN_AS,
                ConnectorRunAs.AUTO,
                id="start_conversation_defaults_to_auto",
            ),
            pytest.param(
                activities.mistralai_start_conversation_stream,
                lambda: mistralai_models.ConversationRequest(inputs="hi"),
                True,
                ConnectorRunAs.DEPLOYMENT,
                ConnectorRunAs.DEPLOYMENT,
                id="start_conversation_stream",
            ),
            pytest.param(
                activities.mistralai_append_conversation_stream,
                lambda: ConversationAppendRequest(conversation_id="c", inputs="hi"),
                True,
                ConnectorRunAs.DEPLOYMENT,
                ConnectorRunAs.DEPLOYMENT,
                id="append_conversation_stream",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_activity_forwards_run_as(self, activity, request_factory, stream, run_as, expected) -> None:
        stream_patch = patch(_PATCH_STREAM, new=AsyncMock(return_value=MagicMock())) if stream else nullcontext()
        with patch(_PATCH_CLIENT, return_value=_client()) as get_client, stream_patch:
            kwargs = {} if run_as is _NO_RUN_AS else {"run_as": run_as}
            await activity.__wrapped__(request_factory(), **kwargs)
        get_client.assert_called_once_with(expected)
