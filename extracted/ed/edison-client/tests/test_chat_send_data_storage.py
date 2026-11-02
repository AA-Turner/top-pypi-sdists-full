from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import httpx
import pytest

from edison_client.clients.chat_methods import ChatMethods


class _StubChatClient(ChatMethods):
    def __init__(self, response: MagicMock):
        self.sync_post = MagicMock(return_value=response)
        self.async_post = AsyncMock(return_value=response)
        self._sync = MagicMock(spec=httpx.Client)
        self._sync.post = self.sync_post
        self._async = MagicMock(spec=httpx.AsyncClient)
        self._async.post = self.async_post

    @property
    def client(self) -> httpx.Client:
        return self._sync

    @property
    def async_client(self) -> httpx.AsyncClient:
        return self._async


def _stub_response(status_code: int, body: dict | None = None) -> MagicMock:
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.text = "" if body is None else str(body)
    if status_code >= 400:
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "err",
            request=MagicMock(),
            response=response,
        )
    else:
        response.raise_for_status.return_value = None
        response.json.return_value = body or {}
    return response


class TestSendChatMessageDataStorageIds:
    def test_send_includes_data_storage_ids_in_info(self) -> None:
        project_id = uuid4()
        session_id = uuid4()
        entry_id = uuid4()
        chat = _StubChatClient(
            _stub_response(
                200,
                {
                    "session_id": str(session_id),
                    "status": "pending",
                },
            )
        )

        result = chat.send_chat_message(
            project_id,
            "analyze this",
            job_name="job-futurehouse-chat",
            data_storage_ids=[f"data_entry:{entry_id}"],
            timeout=900,
        )

        assert result.session_id == session_id
        posted = chat.sync_post.call_args.kwargs["json"]
        assert posted["project_id"] == str(project_id)
        assert posted["message"] == "analyze this"
        assert posted["timeout"] == 900
        assert posted["info"] == {
            "channel": "app",
            "data_storage_ids": [str(entry_id)],
        }

    @pytest.mark.asyncio
    async def test_asend_includes_data_storage_ids_in_info(self) -> None:
        project_id = uuid4()
        session_id = uuid4()
        entry_id = uuid4()
        chat = _StubChatClient(
            _stub_response(
                200,
                {
                    "session_id": str(session_id),
                    "status": "pending",
                },
            )
        )

        result = await chat.asend_chat_message(
            project_id,
            "analyze this",
            data_storage_ids=[entry_id],
            timeout=900,
        )

        assert result.session_id == session_id
        posted = chat.async_post.call_args.kwargs["json"]
        assert posted["info"]["data_storage_ids"] == [str(entry_id)]
        assert posted["timeout"] == 900

    def test_send_normalizes_uuid_and_data_entry_uri(self) -> None:
        project_id = uuid4()
        session_id = uuid4()
        entry_id = uuid4()
        chat = _StubChatClient(
            _stub_response(
                200,
                {"session_id": str(session_id), "status": "pending"},
            )
        )

        chat.send_chat_message(
            project_id,
            "analyze this",
            data_storage_ids=[entry_id, f"data_entry:{entry_id}", str(entry_id)],
        )
        posted = chat.sync_post.call_args.kwargs["json"]
        assert posted["info"]["data_storage_ids"] == [
            str(entry_id),
            str(entry_id),
            str(entry_id),
        ]

    def test_send_omits_data_storage_ids_when_absent(self) -> None:
        project_id = uuid4()
        session_id = uuid4()
        chat = _StubChatClient(
            _stub_response(
                200,
                {"session_id": str(session_id), "status": "pending"},
            )
        )

        chat.send_chat_message(project_id, "hi")
        posted = chat.sync_post.call_args.kwargs["json"]
        assert posted["info"] == {"channel": "app"}
        assert "data_storage_ids" not in posted["info"]
