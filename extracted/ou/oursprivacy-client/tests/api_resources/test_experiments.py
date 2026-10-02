# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from ours_privacy import OursPrivacy, AsyncOursPrivacy
from ours_privacy.types import (
    ExperimentAssignmentResponse,
    ExperimentPersonalizationResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExperiments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_assignment(self, client: OursPrivacy) -> None:
        experiment = client.experiments.assignment(
            experiment_key="experiment_key",
            token="token",
            visitor_id="x",
        )
        assert_matches_type(ExperimentAssignmentResponse, experiment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_assignment_with_all_params(self, client: OursPrivacy) -> None:
        experiment = client.experiments.assignment(
            experiment_key="experiment_key",
            token="token",
            visitor_id="x",
            context={
                "search": "search",
                "url": "url",
            },
            track_impression=True,
        )
        assert_matches_type(ExperimentAssignmentResponse, experiment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_assignment(self, client: OursPrivacy) -> None:
        response = client.experiments.with_raw_response.assignment(
            experiment_key="experiment_key",
            token="token",
            visitor_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = response.parse()
        assert_matches_type(ExperimentAssignmentResponse, experiment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_assignment(self, client: OursPrivacy) -> None:
        with client.experiments.with_streaming_response.assignment(
            experiment_key="experiment_key",
            token="token",
            visitor_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = response.parse()
            assert_matches_type(ExperimentAssignmentResponse, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_assignment(self, client: OursPrivacy) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `experiment_key` but received ''"):
            client.experiments.with_raw_response.assignment(
                experiment_key="",
                token="token",
                visitor_id="x",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_personalization(self, client: OursPrivacy) -> None:
        experiment = client.experiments.personalization(
            token="token",
            visitor_id="x",
        )
        assert_matches_type(ExperimentPersonalizationResponse, experiment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_personalization(self, client: OursPrivacy) -> None:
        response = client.experiments.with_raw_response.personalization(
            token="token",
            visitor_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = response.parse()
        assert_matches_type(ExperimentPersonalizationResponse, experiment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_personalization(self, client: OursPrivacy) -> None:
        with client.experiments.with_streaming_response.personalization(
            token="token",
            visitor_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = response.parse()
            assert_matches_type(ExperimentPersonalizationResponse, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncExperiments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_assignment(self, async_client: AsyncOursPrivacy) -> None:
        experiment = await async_client.experiments.assignment(
            experiment_key="experiment_key",
            token="token",
            visitor_id="x",
        )
        assert_matches_type(ExperimentAssignmentResponse, experiment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_assignment_with_all_params(self, async_client: AsyncOursPrivacy) -> None:
        experiment = await async_client.experiments.assignment(
            experiment_key="experiment_key",
            token="token",
            visitor_id="x",
            context={
                "search": "search",
                "url": "url",
            },
            track_impression=True,
        )
        assert_matches_type(ExperimentAssignmentResponse, experiment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_assignment(self, async_client: AsyncOursPrivacy) -> None:
        response = await async_client.experiments.with_raw_response.assignment(
            experiment_key="experiment_key",
            token="token",
            visitor_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = await response.parse()
        assert_matches_type(ExperimentAssignmentResponse, experiment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_assignment(self, async_client: AsyncOursPrivacy) -> None:
        async with async_client.experiments.with_streaming_response.assignment(
            experiment_key="experiment_key",
            token="token",
            visitor_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = await response.parse()
            assert_matches_type(ExperimentAssignmentResponse, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_assignment(self, async_client: AsyncOursPrivacy) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `experiment_key` but received ''"):
            await async_client.experiments.with_raw_response.assignment(
                experiment_key="",
                token="token",
                visitor_id="x",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_personalization(self, async_client: AsyncOursPrivacy) -> None:
        experiment = await async_client.experiments.personalization(
            token="token",
            visitor_id="x",
        )
        assert_matches_type(ExperimentPersonalizationResponse, experiment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_personalization(self, async_client: AsyncOursPrivacy) -> None:
        response = await async_client.experiments.with_raw_response.personalization(
            token="token",
            visitor_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        experiment = await response.parse()
        assert_matches_type(ExperimentPersonalizationResponse, experiment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_personalization(self, async_client: AsyncOursPrivacy) -> None:
        async with async_client.experiments.with_streaming_response.personalization(
            token="token",
            visitor_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            experiment = await response.parse()
            assert_matches_type(ExperimentPersonalizationResponse, experiment, path=["response"])

        assert cast(Any, response.is_closed) is True
