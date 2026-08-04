# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import annotation_task_batch_update_params
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.annotation_task_batch_update_response import AnnotationTaskBatchUpdateResponse

__all__ = ["AnnotationTasksResource", "AsyncAnnotationTasksResource"]


class AnnotationTasksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AnnotationTasksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AnnotationTasksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AnnotationTasksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AnnotationTasksResourceWithStreamingResponse(self)

    def batch_update(
        self,
        *,
        assigned_to: str | Omit = omit,
        audit_assignment: annotation_task_batch_update_params.AuditAssignment | Omit = omit,
        ids: SequenceNotStr[str] | Omit = omit,
        status: Literal["PENDING_REDO", "COMPLETED"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AnnotationTaskBatchUpdateResponse:
        """
        Update many annotation tasks in one request, operating in one of two mutually
        exclusive modes.

        In ids mode, provide a list of task IDs together with an `assigned_to` and/or a
        `status` (limited to `pending_redo` or `completed`) to apply those field changes
        to each listed task; only tasks that currently exist are affected and IDs that
        do not resolve are silently skipped. In audit_assignment mode, provide an
        evaluation ID, queue ID, and evaluation item IDs to assign Level 1 and/or Level
        2 auditors for those items, creating the underlying audit tasks when they do not
        yet exist; a Level 2 auditor cannot be assigned unless a Level 1 auditor is
        already present. Exactly one of `ids` or `audit_assignment` must be supplied,
        and `assigned_to`/`status` are only valid in ids mode. Access and state checks
        run before any write, so the request is rejected as a whole with nothing
        persisted if any task is inaccessible, if a status change is attempted without a
        modification role, or if an already-completed task would be reassigned; audit
        assignment also requires a modification role. Reassigning a task to a new user
        emits a task-start lineage event, and the response returns the affected
        annotation tasks.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._patch(
            "/v5/annotation-tasks/batch",
            body=maybe_transform(
                {
                    "assigned_to": assigned_to,
                    "audit_assignment": audit_assignment,
                    "ids": ids,
                    "status": status,
                },
                annotation_task_batch_update_params.AnnotationTaskBatchUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AnnotationTaskBatchUpdateResponse,
        )


class AsyncAnnotationTasksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAnnotationTasksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncAnnotationTasksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAnnotationTasksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncAnnotationTasksResourceWithStreamingResponse(self)

    async def batch_update(
        self,
        *,
        assigned_to: str | Omit = omit,
        audit_assignment: annotation_task_batch_update_params.AuditAssignment | Omit = omit,
        ids: SequenceNotStr[str] | Omit = omit,
        status: Literal["PENDING_REDO", "COMPLETED"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AnnotationTaskBatchUpdateResponse:
        """
        Update many annotation tasks in one request, operating in one of two mutually
        exclusive modes.

        In ids mode, provide a list of task IDs together with an `assigned_to` and/or a
        `status` (limited to `pending_redo` or `completed`) to apply those field changes
        to each listed task; only tasks that currently exist are affected and IDs that
        do not resolve are silently skipped. In audit_assignment mode, provide an
        evaluation ID, queue ID, and evaluation item IDs to assign Level 1 and/or Level
        2 auditors for those items, creating the underlying audit tasks when they do not
        yet exist; a Level 2 auditor cannot be assigned unless a Level 1 auditor is
        already present. Exactly one of `ids` or `audit_assignment` must be supplied,
        and `assigned_to`/`status` are only valid in ids mode. Access and state checks
        run before any write, so the request is rejected as a whole with nothing
        persisted if any task is inaccessible, if a status change is attempted without a
        modification role, or if an already-completed task would be reassigned; audit
        assignment also requires a modification role. Reassigning a task to a new user
        emits a task-start lineage event, and the response returns the affected
        annotation tasks.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._patch(
            "/v5/annotation-tasks/batch",
            body=await async_maybe_transform(
                {
                    "assigned_to": assigned_to,
                    "audit_assignment": audit_assignment,
                    "ids": ids,
                    "status": status,
                },
                annotation_task_batch_update_params.AnnotationTaskBatchUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AnnotationTaskBatchUpdateResponse,
        )


class AnnotationTasksResourceWithRawResponse:
    def __init__(self, annotation_tasks: AnnotationTasksResource) -> None:
        self._annotation_tasks = annotation_tasks

        self.batch_update = to_raw_response_wrapper(
            annotation_tasks.batch_update,
        )


class AsyncAnnotationTasksResourceWithRawResponse:
    def __init__(self, annotation_tasks: AsyncAnnotationTasksResource) -> None:
        self._annotation_tasks = annotation_tasks

        self.batch_update = async_to_raw_response_wrapper(
            annotation_tasks.batch_update,
        )


class AnnotationTasksResourceWithStreamingResponse:
    def __init__(self, annotation_tasks: AnnotationTasksResource) -> None:
        self._annotation_tasks = annotation_tasks

        self.batch_update = to_streamed_response_wrapper(
            annotation_tasks.batch_update,
        )


class AsyncAnnotationTasksResourceWithStreamingResponse:
    def __init__(self, annotation_tasks: AsyncAnnotationTasksResource) -> None:
        self._annotation_tasks = annotation_tasks

        self.batch_update = async_to_streamed_response_wrapper(
            annotation_tasks.batch_update,
        )
