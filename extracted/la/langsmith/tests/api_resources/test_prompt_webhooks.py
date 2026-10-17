# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from langsmith import Langsmith, AsyncLangsmith
from tests.utils import assert_matches_type
from langsmith.types import (
    PromptWebhook,
    PromptWebhookListResponse,
    PromptWebhookTestResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPromptWebhooks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: Langsmith) -> None:
        prompt_webhook = client.prompt_webhooks.create(
            url="https://example.com",
        )
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Langsmith) -> None:
        prompt_webhook = client.prompt_webhooks.create(
            url="https://example.com",
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            exclude_prompts=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            headers={"foo": "bar"},
            include_prompts=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            triggers=["commit"],
        )
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Langsmith) -> None:

        response = client.prompt_webhooks.with_raw_response.create(
            url="https://example.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_webhook = response.parse()
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Langsmith) -> None:
        with client.prompt_webhooks.with_streaming_response.create(
            url="https://example.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_webhook = response.parse()
            assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Langsmith) -> None:
        prompt_webhook = client.prompt_webhooks.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Langsmith) -> None:

        response = client.prompt_webhooks.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_webhook = response.parse()
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Langsmith) -> None:
        with client.prompt_webhooks.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_webhook = response.parse()
            assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Langsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            client.prompt_webhooks.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update(self, client: Langsmith) -> None:
        prompt_webhook = client.prompt_webhooks.update(
            webhook_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: Langsmith) -> None:
        prompt_webhook = client.prompt_webhooks.update(
            webhook_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            exclude_prompts=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            headers={"foo": "bar"},
            include_prompts=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            triggers=["commit"],
            url="https://example.com",
        )
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: Langsmith) -> None:

        response = client.prompt_webhooks.with_raw_response.update(
            webhook_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_webhook = response.parse()
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: Langsmith) -> None:
        with client.prompt_webhooks.with_streaming_response.update(
            webhook_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_webhook = response.parse()
            assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_update(self, client: Langsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            client.prompt_webhooks.with_raw_response.update(
                webhook_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Langsmith) -> None:
        prompt_webhook = client.prompt_webhooks.list()
        assert_matches_type(PromptWebhookListResponse, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Langsmith) -> None:

        response = client.prompt_webhooks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_webhook = response.parse()
        assert_matches_type(PromptWebhookListResponse, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Langsmith) -> None:
        with client.prompt_webhooks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_webhook = response.parse()
            assert_matches_type(PromptWebhookListResponse, prompt_webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete(self, client: Langsmith) -> None:
        prompt_webhook = client.prompt_webhooks.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert prompt_webhook is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Langsmith) -> None:

        response = client.prompt_webhooks.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_webhook = response.parse()
        assert prompt_webhook is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Langsmith) -> None:
        with client.prompt_webhooks.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_webhook = response.parse()
            assert prompt_webhook is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Langsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            client.prompt_webhooks.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_test(self, client: Langsmith) -> None:
        prompt_webhook = client.prompt_webhooks.test(
            payload={
                "commit_hash": "commit_hash",
                "created_at": "created_at",
                "created_by": "created_by",
                "event": "commit",
                "manifest": {"foo": "bar"},
                "prompt_id": "prompt_id",
                "prompt_name": "prompt_name",
            },
            webhook={"url": "https://example.com"},
        )
        assert_matches_type(PromptWebhookTestResponse, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_test_with_all_params(self, client: Langsmith) -> None:
        prompt_webhook = client.prompt_webhooks.test(
            payload={
                "commit_hash": "commit_hash",
                "created_at": "created_at",
                "created_by": "created_by",
                "event": "commit",
                "manifest": {"foo": "bar"},
                "prompt_id": "prompt_id",
                "prompt_name": "prompt_name",
                "tag_name": "tag_name",
            },
            webhook={
                "url": "https://example.com",
                "exclude_prompts": ["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                "headers": {"foo": "bar"},
                "include_prompts": ["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                "triggers": ["commit"],
            },
        )
        assert_matches_type(PromptWebhookTestResponse, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_test(self, client: Langsmith) -> None:

        response = client.prompt_webhooks.with_raw_response.test(
            payload={
                "commit_hash": "commit_hash",
                "created_at": "created_at",
                "created_by": "created_by",
                "event": "commit",
                "manifest": {"foo": "bar"},
                "prompt_id": "prompt_id",
                "prompt_name": "prompt_name",
            },
            webhook={"url": "https://example.com"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_webhook = response.parse()
        assert_matches_type(PromptWebhookTestResponse, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_test(self, client: Langsmith) -> None:
        with client.prompt_webhooks.with_streaming_response.test(
            payload={
                "commit_hash": "commit_hash",
                "created_at": "created_at",
                "created_by": "created_by",
                "event": "commit",
                "manifest": {"foo": "bar"},
                "prompt_id": "prompt_id",
                "prompt_name": "prompt_name",
            },
            webhook={"url": "https://example.com"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_webhook = response.parse()
            assert_matches_type(PromptWebhookTestResponse, prompt_webhook, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPromptWebhooks:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncLangsmith) -> None:
        prompt_webhook = await async_client.prompt_webhooks.create(
            url="https://example.com",
        )
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncLangsmith) -> None:
        prompt_webhook = await async_client.prompt_webhooks.create(
            url="https://example.com",
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            exclude_prompts=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            headers={"foo": "bar"},
            include_prompts=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            triggers=["commit"],
        )
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.prompt_webhooks.with_raw_response.create(
            url="https://example.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_webhook = await response.parse()
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncLangsmith) -> None:
        async with async_client.prompt_webhooks.with_streaming_response.create(
            url="https://example.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_webhook = await response.parse()
            assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncLangsmith) -> None:
        prompt_webhook = await async_client.prompt_webhooks.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.prompt_webhooks.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_webhook = await response.parse()
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncLangsmith) -> None:
        async with async_client.prompt_webhooks.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_webhook = await response.parse()
            assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncLangsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            await async_client.prompt_webhooks.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncLangsmith) -> None:
        prompt_webhook = await async_client.prompt_webhooks.update(
            webhook_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncLangsmith) -> None:
        prompt_webhook = await async_client.prompt_webhooks.update(
            webhook_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            exclude_prompts=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            headers={"foo": "bar"},
            include_prompts=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            triggers=["commit"],
            url="https://example.com",
        )
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.prompt_webhooks.with_raw_response.update(
            webhook_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_webhook = await response.parse()
        assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncLangsmith) -> None:
        async with async_client.prompt_webhooks.with_streaming_response.update(
            webhook_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_webhook = await response.parse()
            assert_matches_type(PromptWebhook, prompt_webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncLangsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            await async_client.prompt_webhooks.with_raw_response.update(
                webhook_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncLangsmith) -> None:
        prompt_webhook = await async_client.prompt_webhooks.list()
        assert_matches_type(PromptWebhookListResponse, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.prompt_webhooks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_webhook = await response.parse()
        assert_matches_type(PromptWebhookListResponse, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncLangsmith) -> None:
        async with async_client.prompt_webhooks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_webhook = await response.parse()
            assert_matches_type(PromptWebhookListResponse, prompt_webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncLangsmith) -> None:
        prompt_webhook = await async_client.prompt_webhooks.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert prompt_webhook is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.prompt_webhooks.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_webhook = await response.parse()
        assert prompt_webhook is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncLangsmith) -> None:
        async with async_client.prompt_webhooks.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_webhook = await response.parse()
            assert prompt_webhook is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncLangsmith) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `webhook_id` but received ''"):
            await async_client.prompt_webhooks.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_test(self, async_client: AsyncLangsmith) -> None:
        prompt_webhook = await async_client.prompt_webhooks.test(
            payload={
                "commit_hash": "commit_hash",
                "created_at": "created_at",
                "created_by": "created_by",
                "event": "commit",
                "manifest": {"foo": "bar"},
                "prompt_id": "prompt_id",
                "prompt_name": "prompt_name",
            },
            webhook={"url": "https://example.com"},
        )
        assert_matches_type(PromptWebhookTestResponse, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_test_with_all_params(self, async_client: AsyncLangsmith) -> None:
        prompt_webhook = await async_client.prompt_webhooks.test(
            payload={
                "commit_hash": "commit_hash",
                "created_at": "created_at",
                "created_by": "created_by",
                "event": "commit",
                "manifest": {"foo": "bar"},
                "prompt_id": "prompt_id",
                "prompt_name": "prompt_name",
                "tag_name": "tag_name",
            },
            webhook={
                "url": "https://example.com",
                "exclude_prompts": ["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                "headers": {"foo": "bar"},
                "include_prompts": ["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                "triggers": ["commit"],
            },
        )
        assert_matches_type(PromptWebhookTestResponse, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_test(self, async_client: AsyncLangsmith) -> None:

        response = await async_client.prompt_webhooks.with_raw_response.test(
            payload={
                "commit_hash": "commit_hash",
                "created_at": "created_at",
                "created_by": "created_by",
                "event": "commit",
                "manifest": {"foo": "bar"},
                "prompt_id": "prompt_id",
                "prompt_name": "prompt_name",
            },
            webhook={"url": "https://example.com"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt_webhook = await response.parse()
        assert_matches_type(PromptWebhookTestResponse, prompt_webhook, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_test(self, async_client: AsyncLangsmith) -> None:
        async with async_client.prompt_webhooks.with_streaming_response.test(
            payload={
                "commit_hash": "commit_hash",
                "created_at": "created_at",
                "created_by": "created_by",
                "event": "commit",
                "manifest": {"foo": "bar"},
                "prompt_id": "prompt_id",
                "prompt_name": "prompt_name",
            },
            webhook={"url": "https://example.com"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt_webhook = await response.parse()
            assert_matches_type(PromptWebhookTestResponse, prompt_webhook, path=["response"])

        assert cast(Any, response.is_closed) is True
