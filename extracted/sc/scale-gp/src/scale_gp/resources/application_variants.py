# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Dict, Union, Iterable, cast
from datetime import datetime
from typing_extensions import Literal, overload

import httpx

from ..types import (
    application_variant_list_params,
    application_variant_patch_params,
    application_variant_create_params,
    application_variant_process_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import required_args, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncPageResponse, AsyncPageResponse
from .._base_client import AsyncPaginator, make_request_options
from ..types.paginated_application_variants import Item
from ..types.shared.generic_delete_response import GenericDeleteResponse
from ..types.application_configuration_param import ApplicationConfigurationParam
from ..types.application_variant_patch_response import ApplicationVariantPatchResponse
from ..types.application_variant_create_response import ApplicationVariantCreateResponse
from ..types.application_variant_retrieve_response import ApplicationVariantRetrieveResponse
from ..types.offline_application_configuration_param import OfflineApplicationConfigurationParam
from ..types.application_agents_service_configuration_param import ApplicationAgentsServiceConfigurationParam

__all__ = ["ApplicationVariantsResource", "AsyncApplicationVariantsResource"]


class ApplicationVariantsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ApplicationVariantsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ApplicationVariantsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ApplicationVariantsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ApplicationVariantsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        configuration: ApplicationConfigurationParam,
        name: str,
        version: Literal["V0"],
        description: str | Omit = omit,
        draft: bool | Omit = omit,
        published_at: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationVariantCreateResponse:
        """
        ### Description

        Creates a application variant

        ### Details

        This API can be used to create a application variant. To use this API, review
        the request schema and pass in all fields that are required to create a
        application variant.

        Args:
          account_id: The ID of the account that owns the given entity.

          description: Optional description of the application variant

          draft: Boolean to indicate whether the variant is in draft mode

          published_at: The date and time that the variant was published.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        configuration: ApplicationAgentsServiceConfigurationParam,
        name: str,
        version: Literal["AGENTS_SERVICE"],
        description: str | Omit = omit,
        draft: bool | Omit = omit,
        published_at: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationVariantCreateResponse:
        """
        ### Description

        Creates a application variant

        ### Details

        This API can be used to create a application variant. To use this API, review
        the request schema and pass in all fields that are required to create a
        application variant.

        Args:
          account_id: The ID of the account that owns the given entity.

          description: Optional description of the application variant

          draft: Boolean to indicate whether the variant is in draft mode

          published_at: The date and time that the variant was published.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        configuration: OfflineApplicationConfigurationParam,
        name: str,
        version: Literal["OFFLINE"],
        description: str | Omit = omit,
        draft: bool | Omit = omit,
        published_at: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationVariantCreateResponse:
        """
        ### Description

        Creates a application variant

        ### Details

        This API can be used to create a application variant. To use this API, review
        the request schema and pass in all fields that are required to create a
        application variant.

        Args:
          account_id: The ID of the account that owns the given entity.

          description: Optional description of the application variant

          draft: Boolean to indicate whether the variant is in draft mode

          published_at: The date and time that the variant was published.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["account_id", "application_spec_id", "configuration", "name", "version"])
    def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        configuration: ApplicationConfigurationParam
        | ApplicationAgentsServiceConfigurationParam
        | OfflineApplicationConfigurationParam,
        name: str,
        version: Literal["V0"] | Literal["AGENTS_SERVICE"] | Literal["OFFLINE"],
        description: str | Omit = omit,
        draft: bool | Omit = omit,
        published_at: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationVariantCreateResponse:
        return cast(
            ApplicationVariantCreateResponse,
            self._post(
                "/v4/application-variants",
                body=maybe_transform(
                    {
                        "account_id": account_id,
                        "application_spec_id": application_spec_id,
                        "configuration": configuration,
                        "name": name,
                        "version": version,
                        "description": description,
                        "draft": draft,
                        "published_at": published_at,
                    },
                    application_variant_create_params.ApplicationVariantCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ApplicationVariantCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def retrieve(
        self,
        application_variant_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationVariantRetrieveResponse:
        """
        ### Description

        Gets the details of a application variant

        ### Details

        This API can be used to get information about a single application variant by
        ID. To use this API, pass in the `id` that was returned from your Create
        Application Variant API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_id` but received {application_variant_id!r}"
            )
        return cast(
            ApplicationVariantRetrieveResponse,
            self._get(
                f"/v4/application-variants/{application_variant_id}",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ApplicationVariantRetrieveResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        application_spec_id: Union[int, str] | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[Item]:
        """
        ### Description

        Lists all application variants accessible to the user.

        ### Details

        This API can be used to list application variants. If a user has access to
        multiple accounts, all application variants from all accounts the user is
        associated with will be returned.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v4/application-variants",
            page=SyncPageResponse[Item],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "application_spec_id": application_spec_id,
                        "limit": limit,
                        "page": page,
                    },
                    application_variant_list_params.ApplicationVariantListParams,
                ),
            ),
            model=cast(Any, Item),  # Union types cannot be passed in as arguments in the type system
        )

    def delete(
        self,
        application_variant_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericDeleteResponse:
        """
        ### Description

        Deletes a application variant

        ### Details

        This API can be used to delete a application variant by ID. To use this API,
        pass in the `id` that was returned from your Create Application Variant API call
        as a path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_id` but received {application_variant_id!r}"
            )
        return self._delete(
            f"/v4/application-variants/{application_variant_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )

    def patch(
        self,
        application_variant_id: str,
        *,
        configuration: application_variant_patch_params.Configuration | Omit = omit,
        description: str | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationVariantPatchResponse:
        """
        ### Description

        Updates a application variant

        ### Details

        This API can be used to update the application variant that matches the ID that
        was passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Application Variant API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_id` but received {application_variant_id!r}"
            )
        return cast(
            ApplicationVariantPatchResponse,
            self._patch(
                f"/v4/application-variants/{application_variant_id}",
                body=maybe_transform(
                    {
                        "configuration": configuration,
                        "description": description,
                        "name": name,
                    },
                    application_variant_patch_params.ApplicationVariantPatchParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ApplicationVariantPatchResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def process(
        self,
        application_variant_id: str,
        *,
        inputs: Dict[str, object],
        history: Iterable[application_variant_process_params.History] | Omit = omit,
        operation_metadata: Dict[str, object] | Omit = omit,
        overrides: application_variant_process_params.Overrides | Omit = omit,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """Process Application By Id

        Args:
          inputs: Input data for the application.

        For agents service variants, you must provide
              inputs as a mapping from `{input_name: input_value}`. For V0 variants, you must
              specify the node your input should be passed to, structuring your input as
              `{node_id: {input_name: input_value}}`.

          history: History of the application

          operation_metadata: Arbitrary user-defined metadata that can be attached to the process operations
              and will be registered in the interaction.

          overrides: Optional overrides for the application

          stream: Control to have streaming of the endpoint. If the last node before the output is
              a completion node, you can set this to true to get the output as soon as the
              completion node has a token

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_id` but received {application_variant_id!r}"
            )
        return self._post(
            f"/v4/applications/{application_variant_id}/process",
            body=maybe_transform(
                {
                    "inputs": inputs,
                    "history": history,
                    "operation_metadata": operation_metadata,
                    "overrides": overrides,
                    "stream": stream,
                },
                application_variant_process_params.ApplicationVariantProcessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncApplicationVariantsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncApplicationVariantsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncApplicationVariantsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncApplicationVariantsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncApplicationVariantsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        configuration: ApplicationConfigurationParam,
        name: str,
        version: Literal["V0"],
        description: str | Omit = omit,
        draft: bool | Omit = omit,
        published_at: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationVariantCreateResponse:
        """
        ### Description

        Creates a application variant

        ### Details

        This API can be used to create a application variant. To use this API, review
        the request schema and pass in all fields that are required to create a
        application variant.

        Args:
          account_id: The ID of the account that owns the given entity.

          description: Optional description of the application variant

          draft: Boolean to indicate whether the variant is in draft mode

          published_at: The date and time that the variant was published.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        configuration: ApplicationAgentsServiceConfigurationParam,
        name: str,
        version: Literal["AGENTS_SERVICE"],
        description: str | Omit = omit,
        draft: bool | Omit = omit,
        published_at: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationVariantCreateResponse:
        """
        ### Description

        Creates a application variant

        ### Details

        This API can be used to create a application variant. To use this API, review
        the request schema and pass in all fields that are required to create a
        application variant.

        Args:
          account_id: The ID of the account that owns the given entity.

          description: Optional description of the application variant

          draft: Boolean to indicate whether the variant is in draft mode

          published_at: The date and time that the variant was published.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        configuration: OfflineApplicationConfigurationParam,
        name: str,
        version: Literal["OFFLINE"],
        description: str | Omit = omit,
        draft: bool | Omit = omit,
        published_at: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationVariantCreateResponse:
        """
        ### Description

        Creates a application variant

        ### Details

        This API can be used to create a application variant. To use this API, review
        the request schema and pass in all fields that are required to create a
        application variant.

        Args:
          account_id: The ID of the account that owns the given entity.

          description: Optional description of the application variant

          draft: Boolean to indicate whether the variant is in draft mode

          published_at: The date and time that the variant was published.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["account_id", "application_spec_id", "configuration", "name", "version"])
    async def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        configuration: ApplicationConfigurationParam
        | ApplicationAgentsServiceConfigurationParam
        | OfflineApplicationConfigurationParam,
        name: str,
        version: Literal["V0"] | Literal["AGENTS_SERVICE"] | Literal["OFFLINE"],
        description: str | Omit = omit,
        draft: bool | Omit = omit,
        published_at: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationVariantCreateResponse:
        return cast(
            ApplicationVariantCreateResponse,
            await self._post(
                "/v4/application-variants",
                body=await async_maybe_transform(
                    {
                        "account_id": account_id,
                        "application_spec_id": application_spec_id,
                        "configuration": configuration,
                        "name": name,
                        "version": version,
                        "description": description,
                        "draft": draft,
                        "published_at": published_at,
                    },
                    application_variant_create_params.ApplicationVariantCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ApplicationVariantCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def retrieve(
        self,
        application_variant_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationVariantRetrieveResponse:
        """
        ### Description

        Gets the details of a application variant

        ### Details

        This API can be used to get information about a single application variant by
        ID. To use this API, pass in the `id` that was returned from your Create
        Application Variant API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_id` but received {application_variant_id!r}"
            )
        return cast(
            ApplicationVariantRetrieveResponse,
            await self._get(
                f"/v4/application-variants/{application_variant_id}",
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ApplicationVariantRetrieveResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        application_spec_id: Union[int, str] | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Item, AsyncPageResponse[Item]]:
        """
        ### Description

        Lists all application variants accessible to the user.

        ### Details

        This API can be used to list application variants. If a user has access to
        multiple accounts, all application variants from all accounts the user is
        associated with will be returned.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v4/application-variants",
            page=AsyncPageResponse[Item],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "application_spec_id": application_spec_id,
                        "limit": limit,
                        "page": page,
                    },
                    application_variant_list_params.ApplicationVariantListParams,
                ),
            ),
            model=cast(Any, Item),  # Union types cannot be passed in as arguments in the type system
        )

    async def delete(
        self,
        application_variant_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericDeleteResponse:
        """
        ### Description

        Deletes a application variant

        ### Details

        This API can be used to delete a application variant by ID. To use this API,
        pass in the `id` that was returned from your Create Application Variant API call
        as a path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_id` but received {application_variant_id!r}"
            )
        return await self._delete(
            f"/v4/application-variants/{application_variant_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )

    async def patch(
        self,
        application_variant_id: str,
        *,
        configuration: application_variant_patch_params.Configuration | Omit = omit,
        description: str | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationVariantPatchResponse:
        """
        ### Description

        Updates a application variant

        ### Details

        This API can be used to update the application variant that matches the ID that
        was passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Application Variant API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_id` but received {application_variant_id!r}"
            )
        return cast(
            ApplicationVariantPatchResponse,
            await self._patch(
                f"/v4/application-variants/{application_variant_id}",
                body=await async_maybe_transform(
                    {
                        "configuration": configuration,
                        "description": description,
                        "name": name,
                    },
                    application_variant_patch_params.ApplicationVariantPatchParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ApplicationVariantPatchResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def process(
        self,
        application_variant_id: str,
        *,
        inputs: Dict[str, object],
        history: Iterable[application_variant_process_params.History] | Omit = omit,
        operation_metadata: Dict[str, object] | Omit = omit,
        overrides: application_variant_process_params.Overrides | Omit = omit,
        stream: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """Process Application By Id

        Args:
          inputs: Input data for the application.

        For agents service variants, you must provide
              inputs as a mapping from `{input_name: input_value}`. For V0 variants, you must
              specify the node your input should be passed to, structuring your input as
              `{node_id: {input_name: input_value}}`.

          history: History of the application

          operation_metadata: Arbitrary user-defined metadata that can be attached to the process operations
              and will be registered in the interaction.

          overrides: Optional overrides for the application

          stream: Control to have streaming of the endpoint. If the last node before the output is
              a completion node, you can set this to true to get the output as soon as the
              completion node has a token

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_id` but received {application_variant_id!r}"
            )
        return await self._post(
            f"/v4/applications/{application_variant_id}/process",
            body=await async_maybe_transform(
                {
                    "inputs": inputs,
                    "history": history,
                    "operation_metadata": operation_metadata,
                    "overrides": overrides,
                    "stream": stream,
                },
                application_variant_process_params.ApplicationVariantProcessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ApplicationVariantsResourceWithRawResponse:
    def __init__(self, application_variants: ApplicationVariantsResource) -> None:
        self._application_variants = application_variants

        self.create = to_raw_response_wrapper(
            application_variants.create,
        )
        self.retrieve = to_raw_response_wrapper(
            application_variants.retrieve,
        )
        self.list = to_raw_response_wrapper(
            application_variants.list,
        )
        self.delete = to_raw_response_wrapper(
            application_variants.delete,
        )
        self.patch = to_raw_response_wrapper(
            application_variants.patch,
        )
        self.process = to_raw_response_wrapper(
            application_variants.process,
        )


class AsyncApplicationVariantsResourceWithRawResponse:
    def __init__(self, application_variants: AsyncApplicationVariantsResource) -> None:
        self._application_variants = application_variants

        self.create = async_to_raw_response_wrapper(
            application_variants.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            application_variants.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            application_variants.list,
        )
        self.delete = async_to_raw_response_wrapper(
            application_variants.delete,
        )
        self.patch = async_to_raw_response_wrapper(
            application_variants.patch,
        )
        self.process = async_to_raw_response_wrapper(
            application_variants.process,
        )


class ApplicationVariantsResourceWithStreamingResponse:
    def __init__(self, application_variants: ApplicationVariantsResource) -> None:
        self._application_variants = application_variants

        self.create = to_streamed_response_wrapper(
            application_variants.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            application_variants.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            application_variants.list,
        )
        self.delete = to_streamed_response_wrapper(
            application_variants.delete,
        )
        self.patch = to_streamed_response_wrapper(
            application_variants.patch,
        )
        self.process = to_streamed_response_wrapper(
            application_variants.process,
        )


class AsyncApplicationVariantsResourceWithStreamingResponse:
    def __init__(self, application_variants: AsyncApplicationVariantsResource) -> None:
        self._application_variants = application_variants

        self.create = async_to_streamed_response_wrapper(
            application_variants.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            application_variants.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            application_variants.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            application_variants.delete,
        )
        self.patch = async_to_streamed_response_wrapper(
            application_variants.patch,
        )
        self.process = async_to_streamed_response_wrapper(
            application_variants.process,
        )
