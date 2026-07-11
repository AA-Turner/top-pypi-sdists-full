# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.evaluation import Evaluation
from ...types.evaluations import task_add_params, task_update_params
from ...types.evaluation_task_param import EvaluationTaskParam

__all__ = ["TasksResource", "AsyncTasksResource"]


class TasksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TasksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return TasksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TasksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return TasksResourceWithStreamingResponse(self)

    def update(
        self,
        alias: str,
        *,
        evaluation_id: str,
        configuration: Dict[str, object],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Evaluation:
        """
        Replace the full configuration of a single test criteria, identified by its
        alias.

        The alias must match an existing test criteria on the evaluation, and the
        replacement configuration is validated against the evaluation's current items
        before being applied. The request is rejected if the evaluation is archived, if
        no test criteria matches the alias, or if any contributor annotation task for
        the evaluation has already been claimed or completed — at that point labelers
        are in-flight and mutating the task definition would corrupt their work.

        Args:
          configuration: Full replacement for the test criteria's configuration JSON. Only allowed when
              no contributor annotation tasks for this evaluation have been claimed or
              completed.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        if not alias:
            raise ValueError(f"Expected a non-empty value for `alias` but received {alias!r}")
        return self._patch(
            path_template("/v5/evaluations/{evaluation_id}/tasks/{alias}", evaluation_id=evaluation_id, alias=alias),
            body=maybe_transform({"configuration": configuration}, task_update_params.TaskUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Evaluation,
        )

    def add(
        self,
        evaluation_id: str,
        *,
        task: EvaluationTaskParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Evaluation:
        """
        Add a new test criteria to an existing evaluation.

        Narrowed to contributor question tasks (`contributor_evaluation.question`);
        other task types must be configured when the evaluation is first created and are
        rejected here. The request is also rejected if the evaluation is archived, if a
        test criteria with the same alias already exists, or if any contributor
        annotation task for the evaluation has already been claimed or completed.
        Because only contributor question tasks are accepted, the added criteria is
        applied synchronously and contributors answer it against the evaluation's
        existing items — no async job or Temporal workflow is started.

        Args:
          task: New test criteria to add to the evaluation. Rejected when contributor annotation
              tasks for this evaluation have already been claimed or completed. Triggers a
              rerun so the new task executes against existing items.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._post(
            path_template("/v5/evaluations/{evaluation_id}/tasks", evaluation_id=evaluation_id),
            body=maybe_transform({"task": task}, task_add_params.TaskAddParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Evaluation,
        )


class AsyncTasksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTasksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncTasksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTasksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncTasksResourceWithStreamingResponse(self)

    async def update(
        self,
        alias: str,
        *,
        evaluation_id: str,
        configuration: Dict[str, object],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Evaluation:
        """
        Replace the full configuration of a single test criteria, identified by its
        alias.

        The alias must match an existing test criteria on the evaluation, and the
        replacement configuration is validated against the evaluation's current items
        before being applied. The request is rejected if the evaluation is archived, if
        no test criteria matches the alias, or if any contributor annotation task for
        the evaluation has already been claimed or completed — at that point labelers
        are in-flight and mutating the task definition would corrupt their work.

        Args:
          configuration: Full replacement for the test criteria's configuration JSON. Only allowed when
              no contributor annotation tasks for this evaluation have been claimed or
              completed.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        if not alias:
            raise ValueError(f"Expected a non-empty value for `alias` but received {alias!r}")
        return await self._patch(
            path_template("/v5/evaluations/{evaluation_id}/tasks/{alias}", evaluation_id=evaluation_id, alias=alias),
            body=await async_maybe_transform({"configuration": configuration}, task_update_params.TaskUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Evaluation,
        )

    async def add(
        self,
        evaluation_id: str,
        *,
        task: EvaluationTaskParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Evaluation:
        """
        Add a new test criteria to an existing evaluation.

        Narrowed to contributor question tasks (`contributor_evaluation.question`);
        other task types must be configured when the evaluation is first created and are
        rejected here. The request is also rejected if the evaluation is archived, if a
        test criteria with the same alias already exists, or if any contributor
        annotation task for the evaluation has already been claimed or completed.
        Because only contributor question tasks are accepted, the added criteria is
        applied synchronously and contributors answer it against the evaluation's
        existing items — no async job or Temporal workflow is started.

        Args:
          task: New test criteria to add to the evaluation. Rejected when contributor annotation
              tasks for this evaluation have already been claimed or completed. Triggers a
              rerun so the new task executes against existing items.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._post(
            path_template("/v5/evaluations/{evaluation_id}/tasks", evaluation_id=evaluation_id),
            body=await async_maybe_transform({"task": task}, task_add_params.TaskAddParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Evaluation,
        )


class TasksResourceWithRawResponse:
    def __init__(self, tasks: TasksResource) -> None:
        self._tasks = tasks

        self.update = to_raw_response_wrapper(
            tasks.update,
        )
        self.add = to_raw_response_wrapper(
            tasks.add,
        )


class AsyncTasksResourceWithRawResponse:
    def __init__(self, tasks: AsyncTasksResource) -> None:
        self._tasks = tasks

        self.update = async_to_raw_response_wrapper(
            tasks.update,
        )
        self.add = async_to_raw_response_wrapper(
            tasks.add,
        )


class TasksResourceWithStreamingResponse:
    def __init__(self, tasks: TasksResource) -> None:
        self._tasks = tasks

        self.update = to_streamed_response_wrapper(
            tasks.update,
        )
        self.add = to_streamed_response_wrapper(
            tasks.add,
        )


class AsyncTasksResourceWithStreamingResponse:
    def __init__(self, tasks: AsyncTasksResource) -> None:
        self._tasks = tasks

        self.update = async_to_streamed_response_wrapper(
            tasks.update,
        )
        self.add = async_to_streamed_response_wrapper(
            tasks.add,
        )
