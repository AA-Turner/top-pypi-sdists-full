from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import httpx
import pytest

from edison_client.clients.directive_methods import (
    DirectiveMethods,
    DirectiveResolveError,
)
from edison_client.models.directive import ResolvedSystemPromptDirective


class _Stub(DirectiveMethods):
    def __init__(self, sync=None, async_=None):
        self._sync = sync
        self._async = async_

    @property
    def client(self):
        return self._sync

    @property
    def async_client(self):
        return self._async


def _ok_response() -> MagicMock:
    version_id = str(uuid4())
    body = {
        "directives": [
            {
                "directive_id": str(uuid4()),
                "key": "tone",
                "injection": "system_prompt",
                "order": 0,
                "version_id": version_id,
                "version": 3,
                "name": None,
                "description": None,
                "body": "Be terse.",
                "directive_metadata": None,
                "dss_entry_id": None,
                "version_created_at": datetime.now(UTC).isoformat(),
            }
        ],
    }
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json = MagicMock(return_value=body)
    return resp


def _error_response(status: int = 400) -> httpx.Response:
    request = httpx.Request("POST", "http://test/v0.1/directives/resolve")
    return httpx.Response(status, text="bad request", request=request)


class TestResolveDirectivesSync:
    def test_returns_typed_response(self):
        sync = MagicMock()
        sync.post = MagicMock(return_value=_ok_response())
        stub = _Stub(sync=sync)

        result = stub.resolve_directives(profile_key="p")

        directive = result.directives[0]
        assert isinstance(directive, ResolvedSystemPromptDirective)
        assert directive.key == "tone"
        assert directive.version == 3
        assert directive.body == "Be terse."

    def test_sends_expected_payload(self):
        sync = MagicMock()
        sync.post = MagicMock(return_value=_ok_response())
        stub = _Stub(sync=sync)

        stub.resolve_directives(profile_key="my-profile")

        args, kwargs = sync.post.call_args
        assert args[0] == "/v0.1/directives/resolve"
        assert kwargs["json"] == {"profile_key": "my-profile"}

    def test_non_retryable_http_error_raises_directive_error(self):
        error_resp = _error_response(400)
        sync = MagicMock()
        sync.post = MagicMock(
            return_value=MagicMock(
                raise_for_status=MagicMock(
                    side_effect=httpx.HTTPStatusError(
                        "400", request=error_resp.request, response=error_resp
                    )
                )
            )
        )
        stub = _Stub(sync=sync)

        with pytest.raises(DirectiveResolveError):
            stub.resolve_directives(profile_key="p")


class TestResolveDirectivesAsync:
    @pytest.mark.asyncio
    async def test_returns_typed_response(self):
        async_client = MagicMock()
        async_client.post = AsyncMock(return_value=_ok_response())
        stub = _Stub(async_=async_client)

        result = await stub.aresolve_directives(profile_key="p")

        assert result.directives[0].key == "tone"
