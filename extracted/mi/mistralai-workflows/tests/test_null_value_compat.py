"""Tests for the pre-WFL-2404 backend compat shim."""

from __future__ import annotations

from typing import Any

import httpx
import pytest

from mistralai.workflows.core._registration.null_value_compat import call_stripping_nulls_on_rejection
from mistralai.workflows.worker_client.errors.sdkerror import SDKError


def _error(status_code: int) -> SDKError:
    return SDKError("error", httpx.Response(status_code))


class TestCallStrippingNullsOnRejection:
    @pytest.mark.asyncio
    async def test_success_passes_metadata_through_unchanged(self) -> None:
        async def call(metadata: dict[str, str | None] | None) -> Any:
            return metadata

        assert await call_stripping_nulls_on_rejection(call, {"a": "x", "b": None}) == {"a": "x", "b": None}

    @pytest.mark.asyncio
    async def test_422_with_nulls_retries_without_them(self) -> None:
        calls: list[dict[str, str | None] | None] = []

        async def call(metadata: dict[str, str | None] | None) -> Any:
            calls.append(metadata)
            if len(calls) == 1:
                raise _error(422)
            return "ok"

        assert await call_stripping_nulls_on_rejection(call, {"a": "x", "b": None, "c": None}) == "ok"
        assert calls == [{"a": "x", "b": None, "c": None}, {"a": "x"}]

    @pytest.mark.asyncio
    async def test_422_without_nulls_propagates(self) -> None:
        async def call(metadata: dict[str, str | None] | None) -> Any:
            raise _error(422)

        with pytest.raises(SDKError):
            await call_stripping_nulls_on_rejection(call, {"a": "x"})

    @pytest.mark.asyncio
    async def test_422_with_none_metadata_propagates(self) -> None:
        async def call(metadata: dict[str, str | None] | None) -> Any:
            raise _error(422)

        with pytest.raises(SDKError):
            await call_stripping_nulls_on_rejection(call, None)

    @pytest.mark.asyncio
    async def test_all_none_payload_retries_with_empty_dict(self) -> None:
        calls: list[dict[str, str | None] | None] = []

        async def call(metadata: dict[str, str | None] | None) -> Any:
            calls.append(metadata)
            if len(calls) == 1:
                raise _error(422)
            return "ok"

        assert await call_stripping_nulls_on_rejection(call, {"a": None}) == "ok"
        assert calls == [{"a": None}, {}]

    @pytest.mark.asyncio
    async def test_other_status_with_nulls_propagates(self) -> None:
        async def call(metadata: dict[str, str | None] | None) -> Any:
            raise _error(403)

        with pytest.raises(SDKError):
            await call_stripping_nulls_on_rejection(call, {"a": None})
