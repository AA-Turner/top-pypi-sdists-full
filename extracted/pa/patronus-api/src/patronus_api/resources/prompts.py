# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional

import httpx

from ..types import (
    prompt_set_labels_params,
    prompt_remove_labels_params,
    prompt_list_revisions_params,
    prompt_create_revision_params,
    prompt_list_definitions_params,
    prompt_update_definition_params,
    prompt_delete_definitions_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
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
from ..types.prompt_list_revisions_response import PromptListRevisionsResponse
from ..types.prompt_create_revision_response import PromptCreateRevisionResponse
from ..types.prompt_list_definitions_response import PromptListDefinitionsResponse
from ..types.prompt_update_definition_response import PromptUpdateDefinitionResponse

__all__ = ["PromptsResource", "AsyncPromptsResource"]


class PromptsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PromptsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#accessing-raw-response-data-eg-headers
        """
        return PromptsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PromptsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#with_streaming_response
        """
        return PromptsResourceWithStreamingResponse(self)

    def create_revision(
        self,
        *,
        body: str,
        create_only_if_not_exists: bool | NotGiven = NOT_GIVEN,
        metadata: Optional[object] | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_description: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_id: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptCreateRevisionResponse:
        """
        Create a new prompt revision.

        If prompt_id is provided, creates a new revision of an existing prompt
        definition. If prompt_id is not provided but prompt_name is, creates a new
        prompt definition with its first revision.

        Either project_id or project_name must be provided. If project_name is provided
        and doesn't exist, a new project will be created.

        Returns the newly created prompt revision.

        Args:
          create_only_if_not_exists: If true, creation will fail if a prompt with the same name already exists in the
              project. Only applies when creating a new prompt (not providing prompt_id).

          metadata: Optional JSON metadata to associate with this revision

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/prompt-revisions",
            body=maybe_transform(
                {
                    "body": body,
                    "create_only_if_not_exists": create_only_if_not_exists,
                    "metadata": metadata,
                    "project_id": project_id,
                    "project_name": project_name,
                    "prompt_description": prompt_description,
                    "prompt_id": prompt_id,
                    "prompt_name": prompt_name,
                },
                prompt_create_revision_params.PromptCreateRevisionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptCreateRevisionResponse,
        )

    def delete_definitions(
        self,
        *,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete prompt definitions with either a specific ID or all for a project.

        Either prompt_id or project_id must be provided. If prompt_id is provided,
        deletes only that prompt definition. If project_id is provided, deletes all
        prompt definitions for that project. Returns 204 No Content on success.

        Args:
          project_id: Delete all prompt definitions for this project

          prompt_id: Delete a specific prompt definition by ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            "/v1/prompt-definitions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "project_id": project_id,
                        "prompt_id": prompt_id,
                    },
                    prompt_delete_definitions_params.PromptDeleteDefinitionsParams,
                ),
            ),
            cast_to=NoneType,
        )

    def list_definitions(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        name_startswith: Optional[str] | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptListDefinitionsResponse:
        """
        List prompt definitions with optional filtering.

        Returns prompt definitions with their latest revision number. If no filters are
        provided, returns all prompt definitions for the account (up to limit).

        Args:
          limit: Maximum number of records to return

          name: Filter by exact prompt definition name

          name_startswith: Filter by prompt definition name prefix

          offset: Number of records to skip

          project_id: Filter by project ID

          project_name: Filter by project name

          prompt_id: Filter by specific prompt definition ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/prompt-definitions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "name": name,
                        "name_startswith": name_startswith,
                        "offset": offset,
                        "project_id": project_id,
                        "project_name": project_name,
                        "prompt_id": prompt_id,
                    },
                    prompt_list_definitions_params.PromptListDefinitionsParams,
                ),
            ),
            cast_to=PromptListDefinitionsResponse,
        )

    def list_revisions(
        self,
        *,
        label: Optional[str] | NotGiven = NOT_GIVEN,
        latest_revision_only: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        normalized_body_sha256: Optional[str] | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_id: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_name: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_name_startswith: Optional[str] | NotGiven = NOT_GIVEN,
        revision: Optional[int] | NotGiven = NOT_GIVEN,
        revision_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptListRevisionsResponse:
        """
        List prompt revisions with optional filtering.

        Returns prompt revisions matching the criteria. If project_name is provided, it
        resolves to project_id. If no filters are provided, returns all prompt revisions
        for the account.

        Args:
          label: Filter by revisions that have this label

          latest_revision_only: Only return the latest revision for each prompt

          limit: Maximum number of records to return

          normalized_body_sha256: Filter by SHA-256 hash prefix of prompt body with whitespace stripped from start
              and end

          offset: Number of records to skip

          project_id: Filter by project ID

          project_name: Filter by project name

          prompt_id: Filter by prompt definition ID

          prompt_name: Filter by prompt definition name

          prompt_name_startswith: Filter by prompt definition name prefix

          revision: Filter by revision number

          revision_id: Filter by specific revision ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/prompt-revisions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "label": label,
                        "latest_revision_only": latest_revision_only,
                        "limit": limit,
                        "normalized_body_sha256": normalized_body_sha256,
                        "offset": offset,
                        "project_id": project_id,
                        "project_name": project_name,
                        "prompt_id": prompt_id,
                        "prompt_name": prompt_name,
                        "prompt_name_startswith": prompt_name_startswith,
                        "revision": revision,
                        "revision_id": revision_id,
                    },
                    prompt_list_revisions_params.PromptListRevisionsParams,
                ),
            ),
            cast_to=PromptListRevisionsResponse,
        )

    def remove_labels(
        self,
        revision_id: str,
        *,
        labels: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Remove labels from a prompt revision.

        Returns 204 No Content on success.

        Args:
          revision_id: ID of the prompt revision to remove labels from

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not revision_id:
            raise ValueError(f"Expected a non-empty value for `revision_id` but received {revision_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/v1/prompt-revisions/{revision_id}/remove-labels",
            body=maybe_transform({"labels": labels}, prompt_remove_labels_params.PromptRemoveLabelsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def set_labels(
        self,
        revision_id: str,
        *,
        labels: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Add labels to a prompt revision.

        Removes these labels from other revisions and adds them to the specified
        revision. Returns 204 No Content on success.

        Args:
          revision_id: ID of the prompt revision to label

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not revision_id:
            raise ValueError(f"Expected a non-empty value for `revision_id` but received {revision_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/v1/prompt-revisions/{revision_id}/set-labels",
            body=maybe_transform({"labels": labels}, prompt_set_labels_params.PromptSetLabelsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def update_definition(
        self,
        prompt_id: str,
        *,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptUpdateDefinitionResponse:
        """
        Update a prompt definition's name or description.

        Only updates fields that are provided (not null). Returns the updated prompt
        definition.

        Args:
          prompt_id: ID of the prompt definition to update

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not prompt_id:
            raise ValueError(f"Expected a non-empty value for `prompt_id` but received {prompt_id!r}")
        return self._patch(
            f"/v1/prompt-definitions/{prompt_id}",
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                },
                prompt_update_definition_params.PromptUpdateDefinitionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptUpdateDefinitionResponse,
        )


class AsyncPromptsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPromptsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPromptsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPromptsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#with_streaming_response
        """
        return AsyncPromptsResourceWithStreamingResponse(self)

    async def create_revision(
        self,
        *,
        body: str,
        create_only_if_not_exists: bool | NotGiven = NOT_GIVEN,
        metadata: Optional[object] | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_description: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_id: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptCreateRevisionResponse:
        """
        Create a new prompt revision.

        If prompt_id is provided, creates a new revision of an existing prompt
        definition. If prompt_id is not provided but prompt_name is, creates a new
        prompt definition with its first revision.

        Either project_id or project_name must be provided. If project_name is provided
        and doesn't exist, a new project will be created.

        Returns the newly created prompt revision.

        Args:
          create_only_if_not_exists: If true, creation will fail if a prompt with the same name already exists in the
              project. Only applies when creating a new prompt (not providing prompt_id).

          metadata: Optional JSON metadata to associate with this revision

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/prompt-revisions",
            body=await async_maybe_transform(
                {
                    "body": body,
                    "create_only_if_not_exists": create_only_if_not_exists,
                    "metadata": metadata,
                    "project_id": project_id,
                    "project_name": project_name,
                    "prompt_description": prompt_description,
                    "prompt_id": prompt_id,
                    "prompt_name": prompt_name,
                },
                prompt_create_revision_params.PromptCreateRevisionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptCreateRevisionResponse,
        )

    async def delete_definitions(
        self,
        *,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete prompt definitions with either a specific ID or all for a project.

        Either prompt_id or project_id must be provided. If prompt_id is provided,
        deletes only that prompt definition. If project_id is provided, deletes all
        prompt definitions for that project. Returns 204 No Content on success.

        Args:
          project_id: Delete all prompt definitions for this project

          prompt_id: Delete a specific prompt definition by ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            "/v1/prompt-definitions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "project_id": project_id,
                        "prompt_id": prompt_id,
                    },
                    prompt_delete_definitions_params.PromptDeleteDefinitionsParams,
                ),
            ),
            cast_to=NoneType,
        )

    async def list_definitions(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        name_startswith: Optional[str] | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptListDefinitionsResponse:
        """
        List prompt definitions with optional filtering.

        Returns prompt definitions with their latest revision number. If no filters are
        provided, returns all prompt definitions for the account (up to limit).

        Args:
          limit: Maximum number of records to return

          name: Filter by exact prompt definition name

          name_startswith: Filter by prompt definition name prefix

          offset: Number of records to skip

          project_id: Filter by project ID

          project_name: Filter by project name

          prompt_id: Filter by specific prompt definition ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/prompt-definitions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "name": name,
                        "name_startswith": name_startswith,
                        "offset": offset,
                        "project_id": project_id,
                        "project_name": project_name,
                        "prompt_id": prompt_id,
                    },
                    prompt_list_definitions_params.PromptListDefinitionsParams,
                ),
            ),
            cast_to=PromptListDefinitionsResponse,
        )

    async def list_revisions(
        self,
        *,
        label: Optional[str] | NotGiven = NOT_GIVEN,
        latest_revision_only: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        normalized_body_sha256: Optional[str] | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_id: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_name: Optional[str] | NotGiven = NOT_GIVEN,
        prompt_name_startswith: Optional[str] | NotGiven = NOT_GIVEN,
        revision: Optional[int] | NotGiven = NOT_GIVEN,
        revision_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptListRevisionsResponse:
        """
        List prompt revisions with optional filtering.

        Returns prompt revisions matching the criteria. If project_name is provided, it
        resolves to project_id. If no filters are provided, returns all prompt revisions
        for the account.

        Args:
          label: Filter by revisions that have this label

          latest_revision_only: Only return the latest revision for each prompt

          limit: Maximum number of records to return

          normalized_body_sha256: Filter by SHA-256 hash prefix of prompt body with whitespace stripped from start
              and end

          offset: Number of records to skip

          project_id: Filter by project ID

          project_name: Filter by project name

          prompt_id: Filter by prompt definition ID

          prompt_name: Filter by prompt definition name

          prompt_name_startswith: Filter by prompt definition name prefix

          revision: Filter by revision number

          revision_id: Filter by specific revision ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/prompt-revisions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "label": label,
                        "latest_revision_only": latest_revision_only,
                        "limit": limit,
                        "normalized_body_sha256": normalized_body_sha256,
                        "offset": offset,
                        "project_id": project_id,
                        "project_name": project_name,
                        "prompt_id": prompt_id,
                        "prompt_name": prompt_name,
                        "prompt_name_startswith": prompt_name_startswith,
                        "revision": revision,
                        "revision_id": revision_id,
                    },
                    prompt_list_revisions_params.PromptListRevisionsParams,
                ),
            ),
            cast_to=PromptListRevisionsResponse,
        )

    async def remove_labels(
        self,
        revision_id: str,
        *,
        labels: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Remove labels from a prompt revision.

        Returns 204 No Content on success.

        Args:
          revision_id: ID of the prompt revision to remove labels from

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not revision_id:
            raise ValueError(f"Expected a non-empty value for `revision_id` but received {revision_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/v1/prompt-revisions/{revision_id}/remove-labels",
            body=await async_maybe_transform({"labels": labels}, prompt_remove_labels_params.PromptRemoveLabelsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def set_labels(
        self,
        revision_id: str,
        *,
        labels: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Add labels to a prompt revision.

        Removes these labels from other revisions and adds them to the specified
        revision. Returns 204 No Content on success.

        Args:
          revision_id: ID of the prompt revision to label

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not revision_id:
            raise ValueError(f"Expected a non-empty value for `revision_id` but received {revision_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/v1/prompt-revisions/{revision_id}/set-labels",
            body=await async_maybe_transform({"labels": labels}, prompt_set_labels_params.PromptSetLabelsParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def update_definition(
        self,
        prompt_id: str,
        *,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PromptUpdateDefinitionResponse:
        """
        Update a prompt definition's name or description.

        Only updates fields that are provided (not null). Returns the updated prompt
        definition.

        Args:
          prompt_id: ID of the prompt definition to update

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not prompt_id:
            raise ValueError(f"Expected a non-empty value for `prompt_id` but received {prompt_id!r}")
        return await self._patch(
            f"/v1/prompt-definitions/{prompt_id}",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "name": name,
                },
                prompt_update_definition_params.PromptUpdateDefinitionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PromptUpdateDefinitionResponse,
        )


class PromptsResourceWithRawResponse:
    def __init__(self, prompts: PromptsResource) -> None:
        self._prompts = prompts

        self.create_revision = to_raw_response_wrapper(
            prompts.create_revision,
        )
        self.delete_definitions = to_raw_response_wrapper(
            prompts.delete_definitions,
        )
        self.list_definitions = to_raw_response_wrapper(
            prompts.list_definitions,
        )
        self.list_revisions = to_raw_response_wrapper(
            prompts.list_revisions,
        )
        self.remove_labels = to_raw_response_wrapper(
            prompts.remove_labels,
        )
        self.set_labels = to_raw_response_wrapper(
            prompts.set_labels,
        )
        self.update_definition = to_raw_response_wrapper(
            prompts.update_definition,
        )


class AsyncPromptsResourceWithRawResponse:
    def __init__(self, prompts: AsyncPromptsResource) -> None:
        self._prompts = prompts

        self.create_revision = async_to_raw_response_wrapper(
            prompts.create_revision,
        )
        self.delete_definitions = async_to_raw_response_wrapper(
            prompts.delete_definitions,
        )
        self.list_definitions = async_to_raw_response_wrapper(
            prompts.list_definitions,
        )
        self.list_revisions = async_to_raw_response_wrapper(
            prompts.list_revisions,
        )
        self.remove_labels = async_to_raw_response_wrapper(
            prompts.remove_labels,
        )
        self.set_labels = async_to_raw_response_wrapper(
            prompts.set_labels,
        )
        self.update_definition = async_to_raw_response_wrapper(
            prompts.update_definition,
        )


class PromptsResourceWithStreamingResponse:
    def __init__(self, prompts: PromptsResource) -> None:
        self._prompts = prompts

        self.create_revision = to_streamed_response_wrapper(
            prompts.create_revision,
        )
        self.delete_definitions = to_streamed_response_wrapper(
            prompts.delete_definitions,
        )
        self.list_definitions = to_streamed_response_wrapper(
            prompts.list_definitions,
        )
        self.list_revisions = to_streamed_response_wrapper(
            prompts.list_revisions,
        )
        self.remove_labels = to_streamed_response_wrapper(
            prompts.remove_labels,
        )
        self.set_labels = to_streamed_response_wrapper(
            prompts.set_labels,
        )
        self.update_definition = to_streamed_response_wrapper(
            prompts.update_definition,
        )


class AsyncPromptsResourceWithStreamingResponse:
    def __init__(self, prompts: AsyncPromptsResource) -> None:
        self._prompts = prompts

        self.create_revision = async_to_streamed_response_wrapper(
            prompts.create_revision,
        )
        self.delete_definitions = async_to_streamed_response_wrapper(
            prompts.delete_definitions,
        )
        self.list_definitions = async_to_streamed_response_wrapper(
            prompts.list_definitions,
        )
        self.list_revisions = async_to_streamed_response_wrapper(
            prompts.list_revisions,
        )
        self.remove_labels = async_to_streamed_response_wrapper(
            prompts.remove_labels,
        )
        self.set_labels = async_to_streamed_response_wrapper(
            prompts.set_labels,
        )
        self.update_definition = async_to_streamed_response_wrapper(
            prompts.update_definition,
        )
