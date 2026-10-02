# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import share_link_create_params, share_link_list_pipeline_results_params
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncCursorPage, AsyncCursorPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.share_link_read_response import ShareLinkReadResponse
from ..types.share_link_create_response import ShareLinkCreateResponse
from ..types.share_link_archive_response import ShareLinkArchiveResponse
from ..types.share_link_retrieve_response import ShareLinkRetrieveResponse
from ..types.share_link_list_pipeline_results_response import ShareLinkListPipelineResultsResponse

__all__ = ["ShareLinksResource", "AsyncShareLinksResource"]


class ShareLinksResource(SyncAPIResource):
    """
    Share read-only access to predictions and pipeline runs by issuing time-limited links that visitors can open without an API key or, for email-restricted links, after signing in with an allowed email. A share link is scoped to a single workspace and bundles one or more predictions and pipeline runs. The link ID is itself the bearer credential; treat it as a secret. Create, retrieve, and archive require an API key or supported OAuth bearer token with read permission on every referenced resource. Retrieving metadata remains available after expiry or archive. Viewing content and listing shared pipeline results are gated by the link ID and the link's access mode. Archiving a link revokes public access immediately; subsequent content reads return 404. The underlying predictions and pipelines are unaffected and remain accessible through their own authenticated endpoints.
    """

    @cached_property
    def with_raw_response(self) -> ShareLinksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return ShareLinksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ShareLinksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return ShareLinksResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        expires_at: str,
        access_parameters: share_link_create_params.AccessParameters | Omit = omit,
        pipeline_ids: SequenceNotStr[str] | Omit = omit,
        prediction_ids: SequenceNotStr[str] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ShareLinkCreateResponse:
        """
        Create a read-only share link covering one or more predictions and/or pipelines
        that all live in the same workspace. Public links require only the returned
        bearer ID; email-restricted links also require a signed-in viewer whose email is
        allowed. Treat the returned `id` as a secret.

        Args:
          access_parameters:
              Access-control parameters for the share link. Discriminated by `access_mode`:
              `public` requires no other fields; `email` requires a non-empty `allowed_emails`
              list.

          pipeline_ids: Pipelines to expose through the share link. Must belong to the resolved
              workspace. Up to 100 entries.

          prediction_ids: Predictions to expose through the share link. Must belong to the resolved
              workspace. Up to 100 entries.

          workspace_id: Workspace to target. Admin API keys and OAuth callers may select an authorized
              workspace; for workspace-scoped keys the value must match the key assignment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/compute/v1/share-links",
            body=maybe_transform(
                {
                    "expires_at": expires_at,
                    "access_parameters": access_parameters,
                    "pipeline_ids": pipeline_ids,
                    "prediction_ids": prediction_ids,
                    "workspace_id": workspace_id,
                },
                share_link_create_params.ShareLinkCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ShareLinkCreateResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ShareLinkRetrieveResponse:
        """
        Retrieve metadata for a share link owned by the authenticated organization.
        Archived and expired links remain retrievable.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/compute/v1/share-links/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ShareLinkRetrieveResponse,
        )

    def archive(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ShareLinkArchiveResponse:
        """Archive a share link so it no longer grants public access.

        Metadata remains
        retrievable and repeated calls preserve the first archive timestamp.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/compute/v1/share-links/{id}/archive", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ShareLinkArchiveResponse,
        )

    def list_pipeline_results(
        self,
        pipeline_id: str,
        *,
        id: str,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        ids: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[ShareLinkListPipelineResultsResponse]:
        """Paginated results for one pipeline exposed by a share link.

        The response shape
        matches the authed pipeline-results endpoints exactly. Access is gated by the
        share-link ID and — for email-mode links — a signed compute-API JWT. Pipeline
        IDs not covered by the link return 404 indistinguishably from unknown links.

        Args:
          after_id: Return results after this ID

          before_id: Return results before this ID

          ids: Comma-separated list of result IDs to filter by (max 200). Only results whose ID
              matches one of these is returned; missing IDs are silently skipped. Composes
              with `limit`, `after_id`, and `before_id` — the filter is applied before
              pagination.

          limit: Max results to return. Defaults to 100.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not pipeline_id:
            raise ValueError(f"Expected a non-empty value for `pipeline_id` but received {pipeline_id!r}")
        return self._get_api_list(
            path_template("/compute/v1/share/{id}/pipelines/{pipeline_id}/results", id=id, pipeline_id=pipeline_id),
            page=SyncCursorPage[ShareLinkListPipelineResultsResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "ids": ids,
                        "limit": limit,
                    },
                    share_link_list_pipeline_results_params.ShareLinkListPipelineResultsParams,
                ),
            ),
            model=ShareLinkListPipelineResultsResponse,
        )

    def read(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ShareLinkReadResponse:
        """Read the predictions and pipelines exposed by a share link.

        Public links require
        no authentication — the share link ID itself is the access credential.
        Email-mode links additionally require a signed compute-API JWT (minted for the
        browser session by Lab, or presented directly by CLI/SDK callers). Returns 404
        indistinguishably for unknown, expired, or archived links.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/compute/v1/share/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ShareLinkReadResponse,
        )


class AsyncShareLinksResource(AsyncAPIResource):
    """
    Share read-only access to predictions and pipeline runs by issuing time-limited links that visitors can open without an API key or, for email-restricted links, after signing in with an allowed email. A share link is scoped to a single workspace and bundles one or more predictions and pipeline runs. The link ID is itself the bearer credential; treat it as a secret. Create, retrieve, and archive require an API key or supported OAuth bearer token with read permission on every referenced resource. Retrieving metadata remains available after expiry or archive. Viewing content and listing shared pipeline results are gated by the link ID and the link's access mode. Archiving a link revokes public access immediately; subsequent content reads return 404. The underlying predictions and pipelines are unaffected and remain accessible through their own authenticated endpoints.
    """

    @cached_property
    def with_raw_response(self) -> AsyncShareLinksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncShareLinksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncShareLinksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncShareLinksResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        expires_at: str,
        access_parameters: share_link_create_params.AccessParameters | Omit = omit,
        pipeline_ids: SequenceNotStr[str] | Omit = omit,
        prediction_ids: SequenceNotStr[str] | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ShareLinkCreateResponse:
        """
        Create a read-only share link covering one or more predictions and/or pipelines
        that all live in the same workspace. Public links require only the returned
        bearer ID; email-restricted links also require a signed-in viewer whose email is
        allowed. Treat the returned `id` as a secret.

        Args:
          access_parameters:
              Access-control parameters for the share link. Discriminated by `access_mode`:
              `public` requires no other fields; `email` requires a non-empty `allowed_emails`
              list.

          pipeline_ids: Pipelines to expose through the share link. Must belong to the resolved
              workspace. Up to 100 entries.

          prediction_ids: Predictions to expose through the share link. Must belong to the resolved
              workspace. Up to 100 entries.

          workspace_id: Workspace to target. Admin API keys and OAuth callers may select an authorized
              workspace; for workspace-scoped keys the value must match the key assignment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/compute/v1/share-links",
            body=await async_maybe_transform(
                {
                    "expires_at": expires_at,
                    "access_parameters": access_parameters,
                    "pipeline_ids": pipeline_ids,
                    "prediction_ids": prediction_ids,
                    "workspace_id": workspace_id,
                },
                share_link_create_params.ShareLinkCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ShareLinkCreateResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ShareLinkRetrieveResponse:
        """
        Retrieve metadata for a share link owned by the authenticated organization.
        Archived and expired links remain retrievable.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/compute/v1/share-links/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ShareLinkRetrieveResponse,
        )

    async def archive(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ShareLinkArchiveResponse:
        """Archive a share link so it no longer grants public access.

        Metadata remains
        retrievable and repeated calls preserve the first archive timestamp.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/compute/v1/share-links/{id}/archive", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ShareLinkArchiveResponse,
        )

    def list_pipeline_results(
        self,
        pipeline_id: str,
        *,
        id: str,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        ids: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ShareLinkListPipelineResultsResponse, AsyncCursorPage[ShareLinkListPipelineResultsResponse]]:
        """Paginated results for one pipeline exposed by a share link.

        The response shape
        matches the authed pipeline-results endpoints exactly. Access is gated by the
        share-link ID and — for email-mode links — a signed compute-API JWT. Pipeline
        IDs not covered by the link return 404 indistinguishably from unknown links.

        Args:
          after_id: Return results after this ID

          before_id: Return results before this ID

          ids: Comma-separated list of result IDs to filter by (max 200). Only results whose ID
              matches one of these is returned; missing IDs are silently skipped. Composes
              with `limit`, `after_id`, and `before_id` — the filter is applied before
              pagination.

          limit: Max results to return. Defaults to 100.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        if not pipeline_id:
            raise ValueError(f"Expected a non-empty value for `pipeline_id` but received {pipeline_id!r}")
        return self._get_api_list(
            path_template("/compute/v1/share/{id}/pipelines/{pipeline_id}/results", id=id, pipeline_id=pipeline_id),
            page=AsyncCursorPage[ShareLinkListPipelineResultsResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "ids": ids,
                        "limit": limit,
                    },
                    share_link_list_pipeline_results_params.ShareLinkListPipelineResultsParams,
                ),
            ),
            model=ShareLinkListPipelineResultsResponse,
        )

    async def read(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ShareLinkReadResponse:
        """Read the predictions and pipelines exposed by a share link.

        Public links require
        no authentication — the share link ID itself is the access credential.
        Email-mode links additionally require a signed compute-API JWT (minted for the
        browser session by Lab, or presented directly by CLI/SDK callers). Returns 404
        indistinguishably for unknown, expired, or archived links.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/compute/v1/share/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ShareLinkReadResponse,
        )


class ShareLinksResourceWithRawResponse:
    def __init__(self, share_links: ShareLinksResource) -> None:
        self._share_links = share_links

        self.create = to_raw_response_wrapper(
            share_links.create,
        )
        self.retrieve = to_raw_response_wrapper(
            share_links.retrieve,
        )
        self.archive = to_raw_response_wrapper(
            share_links.archive,
        )
        self.list_pipeline_results = to_raw_response_wrapper(
            share_links.list_pipeline_results,
        )
        self.read = to_raw_response_wrapper(
            share_links.read,
        )


class AsyncShareLinksResourceWithRawResponse:
    def __init__(self, share_links: AsyncShareLinksResource) -> None:
        self._share_links = share_links

        self.create = async_to_raw_response_wrapper(
            share_links.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            share_links.retrieve,
        )
        self.archive = async_to_raw_response_wrapper(
            share_links.archive,
        )
        self.list_pipeline_results = async_to_raw_response_wrapper(
            share_links.list_pipeline_results,
        )
        self.read = async_to_raw_response_wrapper(
            share_links.read,
        )


class ShareLinksResourceWithStreamingResponse:
    def __init__(self, share_links: ShareLinksResource) -> None:
        self._share_links = share_links

        self.create = to_streamed_response_wrapper(
            share_links.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            share_links.retrieve,
        )
        self.archive = to_streamed_response_wrapper(
            share_links.archive,
        )
        self.list_pipeline_results = to_streamed_response_wrapper(
            share_links.list_pipeline_results,
        )
        self.read = to_streamed_response_wrapper(
            share_links.read,
        )


class AsyncShareLinksResourceWithStreamingResponse:
    def __init__(self, share_links: AsyncShareLinksResource) -> None:
        self._share_links = share_links

        self.create = async_to_streamed_response_wrapper(
            share_links.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            share_links.retrieve,
        )
        self.archive = async_to_streamed_response_wrapper(
            share_links.archive,
        )
        self.list_pipeline_results = async_to_streamed_response_wrapper(
            share_links.list_pipeline_results,
        )
        self.read = async_to_streamed_response_wrapper(
            share_links.read,
        )
