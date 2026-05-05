# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from scale_gp_beta import SGPClient, AsyncSGPClient
from scale_gp_beta.types import Question
from scale_gp_beta.pagination import SyncCursorPage, AsyncCursorPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestQuestions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SGPClient) -> None:
        question = client.questions.create(
            question={
                "configuration": {"choices": ["string"]},
                "name": "name",
                "prompt": "prompt",
                "question_type": "categorical",
            },
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SGPClient) -> None:
        question = client.questions.create(
            question={
                "configuration": {
                    "choices": ["string"],
                    "dropdown": True,
                    "multi": True,
                },
                "name": "name",
                "prompt": "prompt",
                "conditions": [{"foo": "bar"}],
                "question_type": "categorical",
            },
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SGPClient) -> None:
        response = client.questions.with_raw_response.create(
            question={
                "configuration": {"choices": ["string"]},
                "name": "name",
                "prompt": "prompt",
                "question_type": "categorical",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = response.parse()
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SGPClient) -> None:
        with client.questions.with_streaming_response.create(
            question={
                "configuration": {"choices": ["string"]},
                "name": "name",
                "prompt": "prompt",
                "question_type": "categorical",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = response.parse()
            assert_matches_type(Question, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SGPClient) -> None:
        question = client.questions.retrieve(
            "question_id",
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SGPClient) -> None:
        response = client.questions.with_raw_response.retrieve(
            "question_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = response.parse()
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SGPClient) -> None:
        with client.questions.with_streaming_response.retrieve(
            "question_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = response.parse()
            assert_matches_type(Question, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_id` but received ''"):
            client.questions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: SGPClient) -> None:
        question = client.questions.update(
            question_id="question_id",
            name="x",
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SGPClient) -> None:
        response = client.questions.with_raw_response.update(
            question_id="question_id",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = response.parse()
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SGPClient) -> None:
        with client.questions.with_streaming_response.update(
            question_id="question_id",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = response.parse()
            assert_matches_type(Question, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_id` but received ''"):
            client.questions.with_raw_response.update(
                question_id="",
                name="x",
            )

    @parametrize
    def test_method_list(self, client: SGPClient) -> None:
        question = client.questions.list()
        assert_matches_type(SyncCursorPage[Question], question, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: SGPClient) -> None:
        question = client.questions.list(
            ending_before="ending_before",
            ids=["string"],
            include_archived=True,
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorPage[Question], question, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SGPClient) -> None:
        response = client.questions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = response.parse()
        assert_matches_type(SyncCursorPage[Question], question, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SGPClient) -> None:
        with client.questions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = response.parse()
            assert_matches_type(SyncCursorPage[Question], question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_archive(self, client: SGPClient) -> None:
        question = client.questions.archive(
            "question_id",
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_raw_response_archive(self, client: SGPClient) -> None:
        response = client.questions.with_raw_response.archive(
            "question_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = response.parse()
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_streaming_response_archive(self, client: SGPClient) -> None:
        with client.questions.with_streaming_response.archive(
            "question_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = response.parse()
            assert_matches_type(Question, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_archive(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_id` but received ''"):
            client.questions.with_raw_response.archive(
                "",
            )

    @parametrize
    def test_method_restore(self, client: SGPClient) -> None:
        question = client.questions.restore(
            "question_id",
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_raw_response_restore(self, client: SGPClient) -> None:
        response = client.questions.with_raw_response.restore(
            "question_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = response.parse()
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    def test_streaming_response_restore(self, client: SGPClient) -> None:
        with client.questions.with_streaming_response.restore(
            "question_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = response.parse()
            assert_matches_type(Question, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_restore(self, client: SGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_id` but received ''"):
            client.questions.with_raw_response.restore(
                "",
            )


class TestAsyncQuestions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSGPClient) -> None:
        question = await async_client.questions.create(
            question={
                "configuration": {"choices": ["string"]},
                "name": "name",
                "prompt": "prompt",
                "question_type": "categorical",
            },
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSGPClient) -> None:
        question = await async_client.questions.create(
            question={
                "configuration": {
                    "choices": ["string"],
                    "dropdown": True,
                    "multi": True,
                },
                "name": "name",
                "prompt": "prompt",
                "conditions": [{"foo": "bar"}],
                "question_type": "categorical",
            },
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.questions.with_raw_response.create(
            question={
                "configuration": {"choices": ["string"]},
                "name": "name",
                "prompt": "prompt",
                "question_type": "categorical",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = await response.parse()
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSGPClient) -> None:
        async with async_client.questions.with_streaming_response.create(
            question={
                "configuration": {"choices": ["string"]},
                "name": "name",
                "prompt": "prompt",
                "question_type": "categorical",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = await response.parse()
            assert_matches_type(Question, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSGPClient) -> None:
        question = await async_client.questions.retrieve(
            "question_id",
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.questions.with_raw_response.retrieve(
            "question_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = await response.parse()
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSGPClient) -> None:
        async with async_client.questions.with_streaming_response.retrieve(
            "question_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = await response.parse()
            assert_matches_type(Question, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_id` but received ''"):
            await async_client.questions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSGPClient) -> None:
        question = await async_client.questions.update(
            question_id="question_id",
            name="x",
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.questions.with_raw_response.update(
            question_id="question_id",
            name="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = await response.parse()
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSGPClient) -> None:
        async with async_client.questions.with_streaming_response.update(
            question_id="question_id",
            name="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = await response.parse()
            assert_matches_type(Question, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_id` but received ''"):
            await async_client.questions.with_raw_response.update(
                question_id="",
                name="x",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSGPClient) -> None:
        question = await async_client.questions.list()
        assert_matches_type(AsyncCursorPage[Question], question, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSGPClient) -> None:
        question = await async_client.questions.list(
            ending_before="ending_before",
            ids=["string"],
            include_archived=True,
            limit=1,
            sort_by="sort_by",
            sort_order="asc",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorPage[Question], question, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.questions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = await response.parse()
        assert_matches_type(AsyncCursorPage[Question], question, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSGPClient) -> None:
        async with async_client.questions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = await response.parse()
            assert_matches_type(AsyncCursorPage[Question], question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_archive(self, async_client: AsyncSGPClient) -> None:
        question = await async_client.questions.archive(
            "question_id",
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.questions.with_raw_response.archive(
            "question_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = await response.parse()
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncSGPClient) -> None:
        async with async_client.questions.with_streaming_response.archive(
            "question_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = await response.parse()
            assert_matches_type(Question, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_archive(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_id` but received ''"):
            await async_client.questions.with_raw_response.archive(
                "",
            )

    @parametrize
    async def test_method_restore(self, async_client: AsyncSGPClient) -> None:
        question = await async_client.questions.restore(
            "question_id",
        )
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_raw_response_restore(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.questions.with_raw_response.restore(
            "question_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        question = await response.parse()
        assert_matches_type(Question, question, path=["response"])

    @parametrize
    async def test_streaming_response_restore(self, async_client: AsyncSGPClient) -> None:
        async with async_client.questions.with_streaming_response.restore(
            "question_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            question = await response.parse()
            assert_matches_type(Question, question, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_restore(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `question_id` but received ''"):
            await async_client.questions.with_raw_response.restore(
                "",
            )
