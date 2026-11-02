# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from coreweave_evaluations import Client, AsyncClient
from coreweave_evaluations.types.scorers import VersionGetResponse, VersionCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVersions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Client) -> None:
        version = client.scorers.versions.create(
            scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            allowed_target_kinds=["case"],
            name="x",
            value_type="null",
        )
        assert_matches_type(VersionCreateResponse, version, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Client) -> None:
        version = client.scorers.versions.create(
            scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            allowed_target_kinds=["case"],
            name="x",
            value_type="null",
            description="description",
        )
        assert_matches_type(VersionCreateResponse, version, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Client) -> None:
        response = client.scorers.versions.with_raw_response.create(
            scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            allowed_target_kinds=["case"],
            name="x",
            value_type="null",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(VersionCreateResponse, version, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Client) -> None:
        with client.scorers.versions.with_streaming_response.create(
            scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            allowed_target_kinds=["case"],
            name="x",
            value_type="null",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = response.parse()
            assert_matches_type(VersionCreateResponse, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.scorers.versions.with_raw_response.create(
                scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                allowed_target_kinds=["case"],
                name="x",
                value_type="null",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.scorers.versions.with_raw_response.create(
                scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                allowed_target_kinds=["case"],
                name="x",
                value_type="null",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scorer_id` but received ''"):
            client.scorers.versions.with_raw_response.create(
                scorer_id="",
                namespace="wandb",
                scope_id="scope_id",
                allowed_target_kinds=["case"],
                name="x",
                value_type="null",
            )

    @parametrize
    def test_method_get(self, client: Client) -> None:
        version = client.scorers.versions.get(
            scorer_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VersionGetResponse, version, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Client) -> None:
        response = client.scorers.versions.with_raw_response.get(
            scorer_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = response.parse()
        assert_matches_type(VersionGetResponse, version, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Client) -> None:
        with client.scorers.versions.with_streaming_response.get(
            scorer_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = response.parse()
            assert_matches_type(VersionGetResponse, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get(self, client: Client) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            client.scorers.versions.with_raw_response.get(
                scorer_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            client.scorers.versions.with_raw_response.get(
                scorer_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scorer_id` but received ''"):
            client.scorers.versions.with_raw_response.get(
                scorer_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="scope_id",
                scorer_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scorer_version_id` but received ''"):
            client.scorers.versions.with_raw_response.get(
                scorer_version_id="",
                namespace="wandb",
                scope_id="scope_id",
                scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )


class TestAsyncVersions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncClient) -> None:
        version = await async_client.scorers.versions.create(
            scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            allowed_target_kinds=["case"],
            name="x",
            value_type="null",
        )
        assert_matches_type(VersionCreateResponse, version, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncClient) -> None:
        version = await async_client.scorers.versions.create(
            scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            allowed_target_kinds=["case"],
            name="x",
            value_type="null",
            description="description",
        )
        assert_matches_type(VersionCreateResponse, version, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncClient) -> None:
        response = await async_client.scorers.versions.with_raw_response.create(
            scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            allowed_target_kinds=["case"],
            name="x",
            value_type="null",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = await response.parse()
        assert_matches_type(VersionCreateResponse, version, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncClient) -> None:
        async with async_client.scorers.versions.with_streaming_response.create(
            scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            allowed_target_kinds=["case"],
            name="x",
            value_type="null",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = await response.parse()
            assert_matches_type(VersionCreateResponse, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.scorers.versions.with_raw_response.create(
                scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                allowed_target_kinds=["case"],
                name="x",
                value_type="null",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.scorers.versions.with_raw_response.create(
                scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                allowed_target_kinds=["case"],
                name="x",
                value_type="null",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scorer_id` but received ''"):
            await async_client.scorers.versions.with_raw_response.create(
                scorer_id="",
                namespace="wandb",
                scope_id="scope_id",
                allowed_target_kinds=["case"],
                name="x",
                value_type="null",
            )

    @parametrize
    async def test_method_get(self, async_client: AsyncClient) -> None:
        version = await async_client.scorers.versions.get(
            scorer_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VersionGetResponse, version, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncClient) -> None:
        response = await async_client.scorers.versions.with_raw_response.get(
            scorer_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        version = await response.parse()
        assert_matches_type(VersionGetResponse, version, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncClient) -> None:
        async with async_client.scorers.versions.with_streaming_response.get(
            scorer_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            namespace="wandb",
            scope_id="scope_id",
            scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            version = await response.parse()
            assert_matches_type(VersionGetResponse, version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get(self, async_client: AsyncClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `namespace` but received ''"):
            await async_client.scorers.versions.with_raw_response.get(
                scorer_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="",
                scope_id="scope_id",
                scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scope_id` but received ''"):
            await async_client.scorers.versions.with_raw_response.get(
                scorer_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="",
                scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scorer_id` but received ''"):
            await async_client.scorers.versions.with_raw_response.get(
                scorer_version_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                namespace="wandb",
                scope_id="scope_id",
                scorer_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `scorer_version_id` but received ''"):
            await async_client.scorers.versions.with_raw_response.get(
                scorer_version_id="",
                namespace="wandb",
                scope_id="scope_id",
                scorer_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )
