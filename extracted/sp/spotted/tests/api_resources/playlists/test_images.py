# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from spotted import Spotted, AsyncSpotted
from tests.utils import assert_matches_type
from spotted._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)
from spotted.types.playlists import ImageListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestImages:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_update(self, client: Spotted, respx_mock: MockRouter) -> None:
        respx_mock.put("/playlists/3cEYpjA9oz9GiPac4AsH4n/images").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        image = client.playlists.images.update(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            body=b"Example data",
        )
        assert image.is_closed
        assert image.json() == {"foo": "bar"}
        assert cast(Any, image.is_closed) is True
        assert isinstance(image, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_update(self, client: Spotted, respx_mock: MockRouter) -> None:
        respx_mock.put("/playlists/3cEYpjA9oz9GiPac4AsH4n/images").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        image = client.playlists.images.with_raw_response.update(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            body=b"Example data",
        )

        assert image.is_closed is True
        assert image.http_request.headers.get("X-Stainless-Lang") == "python"
        assert image.json() == {"foo": "bar"}
        assert isinstance(image, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_update(self, client: Spotted, respx_mock: MockRouter) -> None:
        respx_mock.put("/playlists/3cEYpjA9oz9GiPac4AsH4n/images").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.playlists.images.with_streaming_response.update(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            body=b"Example data",
        ) as image:
            assert not image.is_closed
            assert image.http_request.headers.get("X-Stainless-Lang") == "python"

            assert image.json() == {"foo": "bar"}
            assert cast(Any, image.is_closed) is True
            assert isinstance(image, StreamedBinaryAPIResponse)

        assert cast(Any, image.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_update(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
            client.playlists.images.with_raw_response.update(
                playlist_id="",
                body=b"Example data",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Spotted) -> None:
        image = client.playlists.images.list(
            "3cEYpjA9oz9GiPac4AsH4n",
        )
        assert_matches_type(ImageListResponse, image, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Spotted) -> None:
        response = client.playlists.images.with_raw_response.list(
            "3cEYpjA9oz9GiPac4AsH4n",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = response.parse()
        assert_matches_type(ImageListResponse, image, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Spotted) -> None:
        with client.playlists.images.with_streaming_response.list(
            "3cEYpjA9oz9GiPac4AsH4n",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = response.parse()
            assert_matches_type(ImageListResponse, image, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_list(self, client: Spotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
            client.playlists.images.with_raw_response.list(
                "",
            )


class TestAsyncImages:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_update(self, async_client: AsyncSpotted, respx_mock: MockRouter) -> None:
        respx_mock.put("/playlists/3cEYpjA9oz9GiPac4AsH4n/images").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        image = await async_client.playlists.images.update(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            body=b"Example data",
        )
        assert image.is_closed
        assert await image.json() == {"foo": "bar"}
        assert cast(Any, image.is_closed) is True
        assert isinstance(image, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_update(self, async_client: AsyncSpotted, respx_mock: MockRouter) -> None:
        respx_mock.put("/playlists/3cEYpjA9oz9GiPac4AsH4n/images").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        image = await async_client.playlists.images.with_raw_response.update(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            body=b"Example data",
        )

        assert image.is_closed is True
        assert image.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await image.json() == {"foo": "bar"}
        assert isinstance(image, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_update(self, async_client: AsyncSpotted, respx_mock: MockRouter) -> None:
        respx_mock.put("/playlists/3cEYpjA9oz9GiPac4AsH4n/images").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.playlists.images.with_streaming_response.update(
            playlist_id="3cEYpjA9oz9GiPac4AsH4n",
            body=b"Example data",
        ) as image:
            assert not image.is_closed
            assert image.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await image.json() == {"foo": "bar"}
            assert cast(Any, image.is_closed) is True
            assert isinstance(image, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, image.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_update(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
            await async_client.playlists.images.with_raw_response.update(
                playlist_id="",
                body=b"Example data",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncSpotted) -> None:
        image = await async_client.playlists.images.list(
            "3cEYpjA9oz9GiPac4AsH4n",
        )
        assert_matches_type(ImageListResponse, image, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSpotted) -> None:
        response = await async_client.playlists.images.with_raw_response.list(
            "3cEYpjA9oz9GiPac4AsH4n",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = await response.parse()
        assert_matches_type(ImageListResponse, image, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSpotted) -> None:
        async with async_client.playlists.images.with_streaming_response.list(
            "3cEYpjA9oz9GiPac4AsH4n",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = await response.parse()
            assert_matches_type(ImageListResponse, image, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncSpotted) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `playlist_id` but received ''"):
            await async_client.playlists.images.with_raw_response.list(
                "",
            )
