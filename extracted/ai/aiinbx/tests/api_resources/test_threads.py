# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from aiinbx import AIInbx, AsyncAIInbx
from tests.utils import assert_matches_type
from aiinbx.types import (
    ThreadSearchResponse,
    ThreadForwardResponse,
    ThreadRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestThreads:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: AIInbx) -> None:
        thread = client.threads.retrieve(
            "threadId",
        )
        assert_matches_type(ThreadRetrieveResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: AIInbx) -> None:
        response = client.threads.with_raw_response.retrieve(
            "threadId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(ThreadRetrieveResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: AIInbx) -> None:
        with client.threads.with_streaming_response.retrieve(
            "threadId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(ThreadRetrieveResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: AIInbx) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_forward(self, client: AIInbx) -> None:
        thread = client.threads.forward(
            thread_id="threadId",
            to="dev@stainless.com",
        )
        assert_matches_type(ThreadForwardResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_forward_with_all_params(self, client: AIInbx) -> None:
        thread = client.threads.forward(
            thread_id="threadId",
            to="dev@stainless.com",
            attachments=[
                {
                    "content": "content",
                    "file_name": "file_name",
                    "cid": "cid",
                    "content_type": "content_type",
                    "disposition": "attachment",
                }
            ],
            bcc="dev@stainless.com",
            cc="dev@stainless.com",
            from_="dev@stainless.com",
            from_name="from_name",
            include_attachments=True,
            is_draft=True,
            note="note",
            track_clicks=True,
            track_opens=True,
        )
        assert_matches_type(ThreadForwardResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_forward(self, client: AIInbx) -> None:
        response = client.threads.with_raw_response.forward(
            thread_id="threadId",
            to="dev@stainless.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(ThreadForwardResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_forward(self, client: AIInbx) -> None:
        with client.threads.with_streaming_response.forward(
            thread_id="threadId",
            to="dev@stainless.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(ThreadForwardResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_forward(self, client: AIInbx) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.threads.with_raw_response.forward(
                thread_id="",
                to="dev@stainless.com",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search(self, client: AIInbx) -> None:
        thread = client.threads.search()
        assert_matches_type(ThreadSearchResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_search_with_all_params(self, client: AIInbx) -> None:
        thread = client.threads.search(
            conversation_state="awaiting_reply",
            created_after="createdAfter",
            created_before="createdBefore",
            has_email_from_address="dev@stainless.com",
            has_email_to_address="dev@stainless.com",
            has_participant_emails=["dev@stainless.com"],
            last_email_after="lastEmailAfter",
            last_email_before="lastEmailBefore",
            limit=1,
            offset=0,
            some_email_has_direction="INBOUND",
            some_email_has_status="DRAFT",
            sort_by="createdAt",
            sort_order="asc",
            stale_threshold_days=1,
            subject_contains="subjectContains",
        )
        assert_matches_type(ThreadSearchResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_search(self, client: AIInbx) -> None:
        response = client.threads.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(ThreadSearchResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_search(self, client: AIInbx) -> None:
        with client.threads.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(ThreadSearchResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncThreads:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAIInbx) -> None:
        thread = await async_client.threads.retrieve(
            "threadId",
        )
        assert_matches_type(ThreadRetrieveResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAIInbx) -> None:
        response = await async_client.threads.with_raw_response.retrieve(
            "threadId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(ThreadRetrieveResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAIInbx) -> None:
        async with async_client.threads.with_streaming_response.retrieve(
            "threadId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(ThreadRetrieveResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAIInbx) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_forward(self, async_client: AsyncAIInbx) -> None:
        thread = await async_client.threads.forward(
            thread_id="threadId",
            to="dev@stainless.com",
        )
        assert_matches_type(ThreadForwardResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_forward_with_all_params(self, async_client: AsyncAIInbx) -> None:
        thread = await async_client.threads.forward(
            thread_id="threadId",
            to="dev@stainless.com",
            attachments=[
                {
                    "content": "content",
                    "file_name": "file_name",
                    "cid": "cid",
                    "content_type": "content_type",
                    "disposition": "attachment",
                }
            ],
            bcc="dev@stainless.com",
            cc="dev@stainless.com",
            from_="dev@stainless.com",
            from_name="from_name",
            include_attachments=True,
            is_draft=True,
            note="note",
            track_clicks=True,
            track_opens=True,
        )
        assert_matches_type(ThreadForwardResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_forward(self, async_client: AsyncAIInbx) -> None:
        response = await async_client.threads.with_raw_response.forward(
            thread_id="threadId",
            to="dev@stainless.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(ThreadForwardResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_forward(self, async_client: AsyncAIInbx) -> None:
        async with async_client.threads.with_streaming_response.forward(
            thread_id="threadId",
            to="dev@stainless.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(ThreadForwardResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_forward(self, async_client: AsyncAIInbx) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.threads.with_raw_response.forward(
                thread_id="",
                to="dev@stainless.com",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search(self, async_client: AsyncAIInbx) -> None:
        thread = await async_client.threads.search()
        assert_matches_type(ThreadSearchResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncAIInbx) -> None:
        thread = await async_client.threads.search(
            conversation_state="awaiting_reply",
            created_after="createdAfter",
            created_before="createdBefore",
            has_email_from_address="dev@stainless.com",
            has_email_to_address="dev@stainless.com",
            has_participant_emails=["dev@stainless.com"],
            last_email_after="lastEmailAfter",
            last_email_before="lastEmailBefore",
            limit=1,
            offset=0,
            some_email_has_direction="INBOUND",
            some_email_has_status="DRAFT",
            sort_by="createdAt",
            sort_order="asc",
            stale_threshold_days=1,
            subject_contains="subjectContains",
        )
        assert_matches_type(ThreadSearchResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_search(self, async_client: AsyncAIInbx) -> None:
        response = await async_client.threads.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(ThreadSearchResponse, thread, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncAIInbx) -> None:
        async with async_client.threads.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(ThreadSearchResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True
