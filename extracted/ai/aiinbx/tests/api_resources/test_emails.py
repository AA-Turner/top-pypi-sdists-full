# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from aiinbx import AIInbx, AsyncAIInbx
from tests.utils import assert_matches_type
from aiinbx.types import (
    EmailSendResponse,
    EmailReplyResponse,
    EmailRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEmails:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: AIInbx) -> None:
        email = client.emails.retrieve(
            "emailId",
        )
        assert_matches_type(EmailRetrieveResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: AIInbx) -> None:
        response = client.emails.with_raw_response.retrieve(
            "emailId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        email = response.parse()
        assert_matches_type(EmailRetrieveResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: AIInbx) -> None:
        with client.emails.with_streaming_response.retrieve(
            "emailId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            email = response.parse()
            assert_matches_type(EmailRetrieveResponse, email, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: AIInbx) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `email_id` but received ''"):
            client.emails.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_reply(self, client: AIInbx) -> None:
        email = client.emails.reply(
            email_id="emailId",
            from_="dev@stainless.com",
            html="html",
        )
        assert_matches_type(EmailReplyResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_reply_with_all_params(self, client: AIInbx) -> None:
        email = client.emails.reply(
            email_id="emailId",
            from_="dev@stainless.com",
            html="html",
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
            from_name="from_name",
            is_draft=True,
            reply_all=True,
            subject="subject",
            text="text",
            to="dev@stainless.com",
            track_clicks=True,
            track_opens=True,
        )
        assert_matches_type(EmailReplyResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_reply(self, client: AIInbx) -> None:
        response = client.emails.with_raw_response.reply(
            email_id="emailId",
            from_="dev@stainless.com",
            html="html",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        email = response.parse()
        assert_matches_type(EmailReplyResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_reply(self, client: AIInbx) -> None:
        with client.emails.with_streaming_response.reply(
            email_id="emailId",
            from_="dev@stainless.com",
            html="html",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            email = response.parse()
            assert_matches_type(EmailReplyResponse, email, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_reply(self, client: AIInbx) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `email_id` but received ''"):
            client.emails.with_raw_response.reply(
                email_id="",
                from_="dev@stainless.com",
                html="html",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_send(self, client: AIInbx) -> None:
        email = client.emails.send(
            from_="dev@stainless.com",
            html="html",
            subject="subject",
            to="dev@stainless.com",
        )
        assert_matches_type(EmailSendResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_send_with_all_params(self, client: AIInbx) -> None:
        email = client.emails.send(
            from_="dev@stainless.com",
            html="html",
            subject="subject",
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
            from_name="from_name",
            in_reply_to="in_reply_to",
            is_draft=True,
            references=["string"],
            reply_to="dev@stainless.com",
            text="text",
            thread_id="threadId",
            track_clicks=True,
            track_opens=True,
        )
        assert_matches_type(EmailSendResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_send(self, client: AIInbx) -> None:
        response = client.emails.with_raw_response.send(
            from_="dev@stainless.com",
            html="html",
            subject="subject",
            to="dev@stainless.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        email = response.parse()
        assert_matches_type(EmailSendResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_send(self, client: AIInbx) -> None:
        with client.emails.with_streaming_response.send(
            from_="dev@stainless.com",
            html="html",
            subject="subject",
            to="dev@stainless.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            email = response.parse()
            assert_matches_type(EmailSendResponse, email, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEmails:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncAIInbx) -> None:
        email = await async_client.emails.retrieve(
            "emailId",
        )
        assert_matches_type(EmailRetrieveResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncAIInbx) -> None:
        response = await async_client.emails.with_raw_response.retrieve(
            "emailId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        email = await response.parse()
        assert_matches_type(EmailRetrieveResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncAIInbx) -> None:
        async with async_client.emails.with_streaming_response.retrieve(
            "emailId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            email = await response.parse()
            assert_matches_type(EmailRetrieveResponse, email, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncAIInbx) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `email_id` but received ''"):
            await async_client.emails.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_reply(self, async_client: AsyncAIInbx) -> None:
        email = await async_client.emails.reply(
            email_id="emailId",
            from_="dev@stainless.com",
            html="html",
        )
        assert_matches_type(EmailReplyResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_reply_with_all_params(self, async_client: AsyncAIInbx) -> None:
        email = await async_client.emails.reply(
            email_id="emailId",
            from_="dev@stainless.com",
            html="html",
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
            from_name="from_name",
            is_draft=True,
            reply_all=True,
            subject="subject",
            text="text",
            to="dev@stainless.com",
            track_clicks=True,
            track_opens=True,
        )
        assert_matches_type(EmailReplyResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_reply(self, async_client: AsyncAIInbx) -> None:
        response = await async_client.emails.with_raw_response.reply(
            email_id="emailId",
            from_="dev@stainless.com",
            html="html",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        email = await response.parse()
        assert_matches_type(EmailReplyResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_reply(self, async_client: AsyncAIInbx) -> None:
        async with async_client.emails.with_streaming_response.reply(
            email_id="emailId",
            from_="dev@stainless.com",
            html="html",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            email = await response.parse()
            assert_matches_type(EmailReplyResponse, email, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_reply(self, async_client: AsyncAIInbx) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `email_id` but received ''"):
            await async_client.emails.with_raw_response.reply(
                email_id="",
                from_="dev@stainless.com",
                html="html",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_send(self, async_client: AsyncAIInbx) -> None:
        email = await async_client.emails.send(
            from_="dev@stainless.com",
            html="html",
            subject="subject",
            to="dev@stainless.com",
        )
        assert_matches_type(EmailSendResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_send_with_all_params(self, async_client: AsyncAIInbx) -> None:
        email = await async_client.emails.send(
            from_="dev@stainless.com",
            html="html",
            subject="subject",
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
            from_name="from_name",
            in_reply_to="in_reply_to",
            is_draft=True,
            references=["string"],
            reply_to="dev@stainless.com",
            text="text",
            thread_id="threadId",
            track_clicks=True,
            track_opens=True,
        )
        assert_matches_type(EmailSendResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_send(self, async_client: AsyncAIInbx) -> None:
        response = await async_client.emails.with_raw_response.send(
            from_="dev@stainless.com",
            html="html",
            subject="subject",
            to="dev@stainless.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        email = await response.parse()
        assert_matches_type(EmailSendResponse, email, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_send(self, async_client: AsyncAIInbx) -> None:
        async with async_client.emails.with_streaming_response.send(
            from_="dev@stainless.com",
            html="html",
            subject="subject",
            to="dev@stainless.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            email = await response.parse()
            assert_matches_type(EmailSendResponse, email, path=["response"])

        assert cast(Any, response.is_closed) is True
