# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from langsmith import Langsmith, AsyncLangsmith
from tests.utils import assert_matches_type
from langsmith._utils import parse_datetime
from langsmith.types.annotation_queues import (
    RunListResponse,
    RunCreateResponse,
    RunCreateByKeyResponse,
)

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRuns:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_overload_1(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            )

        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                extend_trace_retention=True,
            )

        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create_overload_1(self, client: Langsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = client.annotation_queues.runs.with_raw_response.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_1(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with client.annotation_queues.runs.with_streaming_response.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = response.parse()
                assert_matches_type(RunCreateResponse, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_create_overload_1(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                client.annotation_queues.runs.with_raw_response.create(
                    queue_id="",
                    body=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_overload_2(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
            )

        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[
                    {
                        "run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "source_proposed_example_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
                extend_trace_retention=True,
            )

        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create_overload_2(self, client: Langsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = client.annotation_queues.runs.with_raw_response.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_2(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with client.annotation_queues.runs.with_streaming_response.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = response.parse()
                assert_matches_type(RunCreateResponse, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_create_overload_2(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                client.annotation_queues.runs.with_raw_response.create(
                    queue_id="",
                    body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_overload_3(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
            )

        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params_overload_3(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[
                    {
                        "run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "parent_run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "session_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "trace_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "trace_tier": "longlived",
                    }
                ],
                extend_trace_retention=True,
            )

        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create_overload_3(self, client: Langsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = client.annotation_queues.runs.with_raw_response.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_3(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with client.annotation_queues.runs.with_streaming_response.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = response.parse()
                assert_matches_type(RunCreateResponse, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_create_overload_3(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                client.annotation_queues.runs.with_raw_response.create(
                    queue_id="",
                    body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.update(
                queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.update(
                queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                added_at=parse_datetime("2019-12-27T18:11:19.117Z"),
                last_reviewed_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            )

        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: Langsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = client.annotation_queues.runs.with_raw_response.update(
                queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with client.annotation_queues.runs.with_streaming_response.update(
                queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = response.parse()
                assert_matches_type(object, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_update(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                client.annotation_queues.runs.with_raw_response.update(
                    queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    queue_id="",
                )

            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_run_id` but received ''"):
                client.annotation_queues.runs.with_raw_response.update(
                    queue_run_id="",
                    queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.list(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert_matches_type(RunListResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.list(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                archived=True,
                include_stats=True,
                limit=1,
                offset=0,
                status="needs_my_review",
            )

        assert_matches_type(RunListResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Langsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = client.annotation_queues.runs.with_raw_response.list(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(RunListResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with client.annotation_queues.runs.with_streaming_response.list(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = response.parse()
                assert_matches_type(RunListResponse, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_list(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                client.annotation_queues.runs.with_raw_response.list(
                    queue_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_by_key(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.create_by_key(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[
                    {
                        "run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "session_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    }
                ],
            )

        assert_matches_type(RunCreateByKeyResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_by_key_with_all_params(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.create_by_key(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[
                    {
                        "run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "session_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "source_proposed_example_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
                extend_trace_retention=True,
            )

        assert_matches_type(RunCreateByKeyResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create_by_key(self, client: Langsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = client.annotation_queues.runs.with_raw_response.create_by_key(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[
                    {
                        "run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "session_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    }
                ],
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(RunCreateByKeyResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create_by_key(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with client.annotation_queues.runs.with_streaming_response.create_by_key(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[
                    {
                        "run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "session_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    }
                ],
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = response.parse()
                assert_matches_type(RunCreateByKeyResponse, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_create_by_key(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                client.annotation_queues.runs.with_raw_response.create_by_key(
                    queue_id="",
                    body=[
                        {
                            "run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "session_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                        }
                    ],
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete_all(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.delete_all(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete_all_with_all_params(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.delete_all(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                delete_all=True,
                exclude_run_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                run_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            )

        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete_all(self, client: Langsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = client.annotation_queues.runs.with_raw_response.delete_all(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete_all(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with client.annotation_queues.runs.with_streaming_response.delete_all(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = response.parse()
                assert_matches_type(object, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete_all(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                client.annotation_queues.runs.with_raw_response.delete_all(
                    queue_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete_queue(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = client.annotation_queues.runs.delete_queue(
                queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete_queue(self, client: Langsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = client.annotation_queues.runs.with_raw_response.delete_queue(
                queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = response.parse()
        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete_queue(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with client.annotation_queues.runs.with_streaming_response.delete_queue(
                queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = response.parse()
                assert_matches_type(object, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete_queue(self, client: Langsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                client.annotation_queues.runs.with_raw_response.delete_queue(
                    queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    queue_id="",
                )

            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_run_id` but received ''"):
                client.annotation_queues.runs.with_raw_response.delete_queue(
                    queue_run_id="",
                    queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                )


class TestAsyncRuns:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            )

        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                extend_trace_retention=True,
            )

        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncLangsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = await async_client.annotation_queues.runs.with_raw_response.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.annotation_queues.runs.with_streaming_response.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = await response.parse()
                assert_matches_type(RunCreateResponse, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_create_overload_1(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                await async_client.annotation_queues.runs.with_raw_response.create(
                    queue_id="",
                    body=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
            )

        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[
                    {
                        "run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "source_proposed_example_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
                extend_trace_retention=True,
            )

        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncLangsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = await async_client.annotation_queues.runs.with_raw_response.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.annotation_queues.runs.with_streaming_response.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = await response.parse()
                assert_matches_type(RunCreateResponse, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_create_overload_2(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                await async_client.annotation_queues.runs.with_raw_response.create(
                    queue_id="",
                    body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_overload_3(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
            )

        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params_overload_3(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[
                    {
                        "run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "parent_run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "session_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "trace_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "trace_tier": "longlived",
                    }
                ],
                extend_trace_retention=True,
            )

        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_3(self, async_client: AsyncLangsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = await async_client.annotation_queues.runs.with_raw_response.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(RunCreateResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_3(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.annotation_queues.runs.with_streaming_response.create(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = await response.parse()
                assert_matches_type(RunCreateResponse, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_create_overload_3(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                await async_client.annotation_queues.runs.with_raw_response.create(
                    queue_id="",
                    body=[{"run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"}],
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.update(
                queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.update(
                queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                added_at=parse_datetime("2019-12-27T18:11:19.117Z"),
                last_reviewed_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            )

        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncLangsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = await async_client.annotation_queues.runs.with_raw_response.update(
                queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.annotation_queues.runs.with_streaming_response.update(
                queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = await response.parse()
                assert_matches_type(object, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                await async_client.annotation_queues.runs.with_raw_response.update(
                    queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    queue_id="",
                )

            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_run_id` but received ''"):
                await async_client.annotation_queues.runs.with_raw_response.update(
                    queue_run_id="",
                    queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.list(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert_matches_type(RunListResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.list(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                archived=True,
                include_stats=True,
                limit=1,
                offset=0,
                status="needs_my_review",
            )

        assert_matches_type(RunListResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncLangsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = await async_client.annotation_queues.runs.with_raw_response.list(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(RunListResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.annotation_queues.runs.with_streaming_response.list(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = await response.parse()
                assert_matches_type(RunListResponse, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                await async_client.annotation_queues.runs.with_raw_response.list(
                    queue_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_by_key(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.create_by_key(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[
                    {
                        "run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "session_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    }
                ],
            )

        assert_matches_type(RunCreateByKeyResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_by_key_with_all_params(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.create_by_key(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[
                    {
                        "run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "session_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                        "source_proposed_example_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    }
                ],
                extend_trace_retention=True,
            )

        assert_matches_type(RunCreateByKeyResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create_by_key(self, async_client: AsyncLangsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = await async_client.annotation_queues.runs.with_raw_response.create_by_key(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[
                    {
                        "run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "session_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    }
                ],
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(RunCreateByKeyResponse, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create_by_key(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.annotation_queues.runs.with_streaming_response.create_by_key(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                body=[
                    {
                        "run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "session_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                        "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                    }
                ],
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = await response.parse()
                assert_matches_type(RunCreateByKeyResponse, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_create_by_key(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                await async_client.annotation_queues.runs.with_raw_response.create_by_key(
                    queue_id="",
                    body=[
                        {
                            "run_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "session_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "start_time": parse_datetime("2019-12-27T18:11:19.117Z"),
                        }
                    ],
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete_all(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.delete_all(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete_all_with_all_params(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.delete_all(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                delete_all=True,
                exclude_run_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
                run_ids=["182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"],
            )

        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete_all(self, async_client: AsyncLangsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = await async_client.annotation_queues.runs.with_raw_response.delete_all(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete_all(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.annotation_queues.runs.with_streaming_response.delete_all(
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = await response.parse()
                assert_matches_type(object, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete_all(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                await async_client.annotation_queues.runs.with_raw_response.delete_all(
                    queue_id="",
                )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete_queue(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            run = await async_client.annotation_queues.runs.delete_queue(
                queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete_queue(self, async_client: AsyncLangsmith) -> None:

        with pytest.warns(DeprecationWarning):
            response = await async_client.annotation_queues.runs.with_raw_response.delete_queue(
                queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        run = await response.parse()
        assert_matches_type(object, run, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete_queue(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.annotation_queues.runs.with_streaming_response.delete_queue(
                queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                run = await response.parse()
                assert_matches_type(object, run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete_queue(self, async_client: AsyncLangsmith) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_id` but received ''"):
                await async_client.annotation_queues.runs.with_raw_response.delete_queue(
                    queue_run_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    queue_id="",
                )

            with pytest.raises(ValueError, match=r"Expected a non-empty value for `queue_run_id` but received ''"):
                await async_client.annotation_queues.runs.with_raw_response.delete_queue(
                    queue_run_id="",
                    queue_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                )
