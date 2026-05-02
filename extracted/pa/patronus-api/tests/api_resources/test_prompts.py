# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from patronus_api import PatronusAPI, AsyncPatronusAPI
from patronus_api.types import (
    PromptListRevisionsResponse,
    PromptCreateRevisionResponse,
    PromptListDefinitionsResponse,
    PromptUpdateDefinitionResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPrompts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_revision(self, client: PatronusAPI) -> None:
        prompt = client.prompts.create_revision(
            body="body",
        )
        assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

    @parametrize
    def test_method_create_revision_with_all_params(self, client: PatronusAPI) -> None:
        prompt = client.prompts.create_revision(
            body="body",
            create_only_if_not_exists=True,
            metadata={},
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
            prompt_description="prompt_description",
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            prompt_name="prompt_name",
        )
        assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

    @parametrize
    def test_raw_response_create_revision(self, client: PatronusAPI) -> None:
        response = client.prompts.with_raw_response.create_revision(
            body="body",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

    @parametrize
    def test_streaming_response_create_revision(self, client: PatronusAPI) -> None:
        with client.prompts.with_streaming_response.create_revision(
            body="body",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete_definitions(self, client: PatronusAPI) -> None:
        prompt = client.prompts.delete_definitions()
        assert prompt is None

    @parametrize
    def test_method_delete_definitions_with_all_params(self, client: PatronusAPI) -> None:
        prompt = client.prompts.delete_definitions(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert prompt is None

    @parametrize
    def test_raw_response_delete_definitions(self, client: PatronusAPI) -> None:
        response = client.prompts.with_raw_response.delete_definitions()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert prompt is None

    @parametrize
    def test_streaming_response_delete_definitions(self, client: PatronusAPI) -> None:
        with client.prompts.with_streaming_response.delete_definitions() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert prompt is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_definitions(self, client: PatronusAPI) -> None:
        prompt = client.prompts.list_definitions()
        assert_matches_type(PromptListDefinitionsResponse, prompt, path=["response"])

    @parametrize
    def test_method_list_definitions_with_all_params(self, client: PatronusAPI) -> None:
        prompt = client.prompts.list_definitions(
            limit=0,
            name="name",
            name_startswith="name_startswith",
            offset=0,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PromptListDefinitionsResponse, prompt, path=["response"])

    @parametrize
    def test_raw_response_list_definitions(self, client: PatronusAPI) -> None:
        response = client.prompts.with_raw_response.list_definitions()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(PromptListDefinitionsResponse, prompt, path=["response"])

    @parametrize
    def test_streaming_response_list_definitions(self, client: PatronusAPI) -> None:
        with client.prompts.with_streaming_response.list_definitions() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(PromptListDefinitionsResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_revisions(self, client: PatronusAPI) -> None:
        prompt = client.prompts.list_revisions()
        assert_matches_type(PromptListRevisionsResponse, prompt, path=["response"])

    @parametrize
    def test_method_list_revisions_with_all_params(self, client: PatronusAPI) -> None:
        prompt = client.prompts.list_revisions(
            label="label",
            latest_revision_only=True,
            limit=0,
            normalized_body_sha256="normalized_body_sha256",
            offset=0,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            prompt_name="prompt_name",
            prompt_name_startswith="prompt_name_startswith",
            revision=0,
            revision_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PromptListRevisionsResponse, prompt, path=["response"])

    @parametrize
    def test_raw_response_list_revisions(self, client: PatronusAPI) -> None:
        response = client.prompts.with_raw_response.list_revisions()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(PromptListRevisionsResponse, prompt, path=["response"])

    @parametrize
    def test_streaming_response_list_revisions(self, client: PatronusAPI) -> None:
        with client.prompts.with_streaming_response.list_revisions() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(PromptListRevisionsResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_remove_labels(self, client: PatronusAPI) -> None:
        prompt = client.prompts.remove_labels(
            revision_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            labels=["-_-k..W2K-1V"],
        )
        assert prompt is None

    @parametrize
    def test_raw_response_remove_labels(self, client: PatronusAPI) -> None:
        response = client.prompts.with_raw_response.remove_labels(
            revision_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            labels=["-_-k..W2K-1V"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert prompt is None

    @parametrize
    def test_streaming_response_remove_labels(self, client: PatronusAPI) -> None:
        with client.prompts.with_streaming_response.remove_labels(
            revision_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            labels=["-_-k..W2K-1V"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert prompt is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_remove_labels(self, client: PatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `revision_id` but received ''"):
            client.prompts.with_raw_response.remove_labels(
                revision_id="",
                labels=["-_-k..W2K-1V"],
            )

    @parametrize
    def test_method_set_labels(self, client: PatronusAPI) -> None:
        prompt = client.prompts.set_labels(
            revision_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            labels=["-_-k..W2K-1V"],
        )
        assert prompt is None

    @parametrize
    def test_raw_response_set_labels(self, client: PatronusAPI) -> None:
        response = client.prompts.with_raw_response.set_labels(
            revision_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            labels=["-_-k..W2K-1V"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert prompt is None

    @parametrize
    def test_streaming_response_set_labels(self, client: PatronusAPI) -> None:
        with client.prompts.with_streaming_response.set_labels(
            revision_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            labels=["-_-k..W2K-1V"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert prompt is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_set_labels(self, client: PatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `revision_id` but received ''"):
            client.prompts.with_raw_response.set_labels(
                revision_id="",
                labels=["-_-k..W2K-1V"],
            )

    @parametrize
    def test_method_update_definition(self, client: PatronusAPI) -> None:
        prompt = client.prompts.update_definition(
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PromptUpdateDefinitionResponse, prompt, path=["response"])

    @parametrize
    def test_method_update_definition_with_all_params(self, client: PatronusAPI) -> None:
        prompt = client.prompts.update_definition(
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="x",
            name="name",
        )
        assert_matches_type(PromptUpdateDefinitionResponse, prompt, path=["response"])

    @parametrize
    def test_raw_response_update_definition(self, client: PatronusAPI) -> None:
        response = client.prompts.with_raw_response.update_definition(
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = response.parse()
        assert_matches_type(PromptUpdateDefinitionResponse, prompt, path=["response"])

    @parametrize
    def test_streaming_response_update_definition(self, client: PatronusAPI) -> None:
        with client.prompts.with_streaming_response.update_definition(
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = response.parse()
            assert_matches_type(PromptUpdateDefinitionResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update_definition(self, client: PatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `prompt_id` but received ''"):
            client.prompts.with_raw_response.update_definition(
                prompt_id="",
            )


class TestAsyncPrompts:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create_revision(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.create_revision(
            body="body",
        )
        assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

    @parametrize
    async def test_method_create_revision_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.create_revision(
            body="body",
            create_only_if_not_exists=True,
            metadata={},
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
            prompt_description="prompt_description",
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            prompt_name="prompt_name",
        )
        assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

    @parametrize
    async def test_raw_response_create_revision(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.prompts.with_raw_response.create_revision(
            body="body",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

    @parametrize
    async def test_streaming_response_create_revision(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.prompts.with_streaming_response.create_revision(
            body="body",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(PromptCreateRevisionResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete_definitions(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.delete_definitions()
        assert prompt is None

    @parametrize
    async def test_method_delete_definitions_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.delete_definitions(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert prompt is None

    @parametrize
    async def test_raw_response_delete_definitions(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.prompts.with_raw_response.delete_definitions()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert prompt is None

    @parametrize
    async def test_streaming_response_delete_definitions(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.prompts.with_streaming_response.delete_definitions() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert prompt is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_definitions(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.list_definitions()
        assert_matches_type(PromptListDefinitionsResponse, prompt, path=["response"])

    @parametrize
    async def test_method_list_definitions_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.list_definitions(
            limit=0,
            name="name",
            name_startswith="name_startswith",
            offset=0,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PromptListDefinitionsResponse, prompt, path=["response"])

    @parametrize
    async def test_raw_response_list_definitions(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.prompts.with_raw_response.list_definitions()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(PromptListDefinitionsResponse, prompt, path=["response"])

    @parametrize
    async def test_streaming_response_list_definitions(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.prompts.with_streaming_response.list_definitions() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(PromptListDefinitionsResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_revisions(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.list_revisions()
        assert_matches_type(PromptListRevisionsResponse, prompt, path=["response"])

    @parametrize
    async def test_method_list_revisions_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.list_revisions(
            label="label",
            latest_revision_only=True,
            limit=0,
            normalized_body_sha256="normalized_body_sha256",
            offset=0,
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_name="project_name",
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            prompt_name="prompt_name",
            prompt_name_startswith="prompt_name_startswith",
            revision=0,
            revision_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PromptListRevisionsResponse, prompt, path=["response"])

    @parametrize
    async def test_raw_response_list_revisions(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.prompts.with_raw_response.list_revisions()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(PromptListRevisionsResponse, prompt, path=["response"])

    @parametrize
    async def test_streaming_response_list_revisions(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.prompts.with_streaming_response.list_revisions() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(PromptListRevisionsResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_remove_labels(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.remove_labels(
            revision_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            labels=["-_-k..W2K-1V"],
        )
        assert prompt is None

    @parametrize
    async def test_raw_response_remove_labels(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.prompts.with_raw_response.remove_labels(
            revision_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            labels=["-_-k..W2K-1V"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert prompt is None

    @parametrize
    async def test_streaming_response_remove_labels(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.prompts.with_streaming_response.remove_labels(
            revision_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            labels=["-_-k..W2K-1V"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert prompt is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_remove_labels(self, async_client: AsyncPatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `revision_id` but received ''"):
            await async_client.prompts.with_raw_response.remove_labels(
                revision_id="",
                labels=["-_-k..W2K-1V"],
            )

    @parametrize
    async def test_method_set_labels(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.set_labels(
            revision_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            labels=["-_-k..W2K-1V"],
        )
        assert prompt is None

    @parametrize
    async def test_raw_response_set_labels(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.prompts.with_raw_response.set_labels(
            revision_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            labels=["-_-k..W2K-1V"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert prompt is None

    @parametrize
    async def test_streaming_response_set_labels(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.prompts.with_streaming_response.set_labels(
            revision_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            labels=["-_-k..W2K-1V"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert prompt is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_set_labels(self, async_client: AsyncPatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `revision_id` but received ''"):
            await async_client.prompts.with_raw_response.set_labels(
                revision_id="",
                labels=["-_-k..W2K-1V"],
            )

    @parametrize
    async def test_method_update_definition(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.update_definition(
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PromptUpdateDefinitionResponse, prompt, path=["response"])

    @parametrize
    async def test_method_update_definition_with_all_params(self, async_client: AsyncPatronusAPI) -> None:
        prompt = await async_client.prompts.update_definition(
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="x",
            name="name",
        )
        assert_matches_type(PromptUpdateDefinitionResponse, prompt, path=["response"])

    @parametrize
    async def test_raw_response_update_definition(self, async_client: AsyncPatronusAPI) -> None:
        response = await async_client.prompts.with_raw_response.update_definition(
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        prompt = await response.parse()
        assert_matches_type(PromptUpdateDefinitionResponse, prompt, path=["response"])

    @parametrize
    async def test_streaming_response_update_definition(self, async_client: AsyncPatronusAPI) -> None:
        async with async_client.prompts.with_streaming_response.update_definition(
            prompt_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            prompt = await response.parse()
            assert_matches_type(PromptUpdateDefinitionResponse, prompt, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update_definition(self, async_client: AsyncPatronusAPI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `prompt_id` but received ''"):
            await async_client.prompts.with_raw_response.update_definition(
                prompt_id="",
            )
