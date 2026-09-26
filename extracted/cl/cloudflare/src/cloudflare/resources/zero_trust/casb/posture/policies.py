# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Type, Optional, cast

import httpx

from ....._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ....._utils import path_template, maybe_transform, async_maybe_transform
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._wrappers import ResultWrapper
from .....pagination import SyncCursorPaginationAfter, AsyncCursorPaginationAfter
from ....._base_client import AsyncPaginator, make_request_options
from .....types.zero_trust.casb.posture import policy_list_params, policy_create_params, policy_update_params
from .....types.zero_trust.casb.posture.policy_get_response import PolicyGetResponse
from .....types.zero_trust.casb.posture.policy_list_response import PolicyListResponse
from .....types.zero_trust.casb.posture.policy_create_response import PolicyCreateResponse
from .....types.zero_trust.casb.posture.policy_delete_response import PolicyDeleteResponse
from .....types.zero_trust.casb.posture.policy_update_response import PolicyUpdateResponse

__all__ = ["PoliciesResource", "AsyncPoliciesResource"]


class PoliciesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PoliciesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return PoliciesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PoliciesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return PoliciesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        actions: policy_create_params.Actions,
        applies_to_all_integrations: bool,
        display_name: str,
        enabled: bool,
        finding_type_id: str,
        description: str | Omit = omit,
        integration_ids: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[PolicyCreateResponse]:
        """
        Creates a new policy configuration that defines automated actions to be executed
        when security findings are detected. A policy can include multiple remediation
        and/or webhook actions that will be triggered automatically.

        Args:
          actions: Actions to execute when this policy is triggered, grouped by action type. A
              policy must contain at least one action across all groups and may include at
              most one remediation.

          applies_to_all_integrations: When true, the policy applies to all integrations for the account. When false,
              integration_ids must be provided.

          display_name: Display name for the policy configuration.

          enabled: Boolean specifying if the policy is enabled or disabled.

          finding_type_id: The finding type this policy is associated with. All remediation actions must
              match this finding type.

          description: Optional description of what this policy does.

          integration_ids: The integrations this policy applies to. Required when
              applies_to_all_integrations is false.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._post(
            path_template("/accounts/{account_id}/data-security/posture/policies", account_id=account_id),
            body=maybe_transform(
                {
                    "actions": actions,
                    "applies_to_all_integrations": applies_to_all_integrations,
                    "display_name": display_name,
                    "enabled": enabled,
                    "finding_type_id": finding_type_id,
                    "description": description,
                    "integration_ids": integration_ids,
                },
                policy_create_params.PolicyCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[Optional[PolicyCreateResponse]]._unwrapper,
            ),
            cast_to=cast(Type[Optional[PolicyCreateResponse]], ResultWrapper[PolicyCreateResponse]),
        )

    def update(
        self,
        policy_id: str,
        *,
        account_id: str,
        actions: policy_update_params.Actions,
        applies_to_all_integrations: bool,
        display_name: str,
        enabled: bool,
        description: str | Omit = omit,
        integration_ids: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[PolicyUpdateResponse]:
        """
        Updates an existing policy configuration and replaces its actions.

        Args:
          actions: Actions to execute when this policy is triggered, grouped by action type. A
              policy must contain at least one action across all groups and may include at
              most one remediation.

          applies_to_all_integrations: When true, the policy applies to all integrations for the account. When false,
              integration_ids must be provided.

          display_name: Display name for the policy configuration.

          enabled: Boolean specifying if the policy is enabled or disabled.

          description: Optional description of what this policy does.

          integration_ids: The integrations this policy applies to. Required when
              applies_to_all_integrations is false.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not policy_id:
            raise ValueError(f"Expected a non-empty value for `policy_id` but received {policy_id!r}")
        return self._put(
            path_template(
                "/accounts/{account_id}/data-security/posture/policies/{policy_id}",
                account_id=account_id,
                policy_id=policy_id,
            ),
            body=maybe_transform(
                {
                    "actions": actions,
                    "applies_to_all_integrations": applies_to_all_integrations,
                    "display_name": display_name,
                    "enabled": enabled,
                    "description": description,
                    "integration_ids": integration_ids,
                },
                policy_update_params.PolicyUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[Optional[PolicyUpdateResponse]]._unwrapper,
            ),
            cast_to=cast(Type[Optional[PolicyUpdateResponse]], ResultWrapper[PolicyUpdateResponse]),
        )

    def list(
        self,
        *,
        account_id: str,
        cursor: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPaginationAfter[PolicyListResponse]:
        """Returns a list of integration-scoped policy configurations for the given
        account.

        This endpoint supports cursor based pagination. By default, results are
        returned in sorted order based on created_at.

        Args:
          cursor: Cursor for pagination. Obtained from the `result_info.cursor` field of a
              previous response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get_api_list(
            path_template("/accounts/{account_id}/data-security/posture/policies", account_id=account_id),
            page=SyncCursorPaginationAfter[PolicyListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"cursor": cursor}, policy_list_params.PolicyListParams),
            ),
            model=PolicyListResponse,
        )

    def delete(
        self,
        policy_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[PolicyDeleteResponse]:
        """
        Deletes a policy configuration.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not policy_id:
            raise ValueError(f"Expected a non-empty value for `policy_id` but received {policy_id!r}")
        return self._delete(
            path_template(
                "/accounts/{account_id}/data-security/posture/policies/{policy_id}",
                account_id=account_id,
                policy_id=policy_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[Optional[PolicyDeleteResponse]]._unwrapper,
            ),
            cast_to=cast(Type[Optional[PolicyDeleteResponse]], ResultWrapper[PolicyDeleteResponse]),
        )

    def get(
        self,
        policy_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[PolicyGetResponse]:
        """
        Retrieves the details of a specific policy configuration, including its
        associated remediation and webhook actions.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not policy_id:
            raise ValueError(f"Expected a non-empty value for `policy_id` but received {policy_id!r}")
        return self._get(
            path_template(
                "/accounts/{account_id}/data-security/posture/policies/{policy_id}",
                account_id=account_id,
                policy_id=policy_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[Optional[PolicyGetResponse]]._unwrapper,
            ),
            cast_to=cast(Type[Optional[PolicyGetResponse]], ResultWrapper[PolicyGetResponse]),
        )


class AsyncPoliciesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPoliciesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPoliciesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPoliciesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cloudflare/cloudflare-python#with_streaming_response
        """
        return AsyncPoliciesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        actions: policy_create_params.Actions,
        applies_to_all_integrations: bool,
        display_name: str,
        enabled: bool,
        finding_type_id: str,
        description: str | Omit = omit,
        integration_ids: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[PolicyCreateResponse]:
        """
        Creates a new policy configuration that defines automated actions to be executed
        when security findings are detected. A policy can include multiple remediation
        and/or webhook actions that will be triggered automatically.

        Args:
          actions: Actions to execute when this policy is triggered, grouped by action type. A
              policy must contain at least one action across all groups and may include at
              most one remediation.

          applies_to_all_integrations: When true, the policy applies to all integrations for the account. When false,
              integration_ids must be provided.

          display_name: Display name for the policy configuration.

          enabled: Boolean specifying if the policy is enabled or disabled.

          finding_type_id: The finding type this policy is associated with. All remediation actions must
              match this finding type.

          description: Optional description of what this policy does.

          integration_ids: The integrations this policy applies to. Required when
              applies_to_all_integrations is false.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return await self._post(
            path_template("/accounts/{account_id}/data-security/posture/policies", account_id=account_id),
            body=await async_maybe_transform(
                {
                    "actions": actions,
                    "applies_to_all_integrations": applies_to_all_integrations,
                    "display_name": display_name,
                    "enabled": enabled,
                    "finding_type_id": finding_type_id,
                    "description": description,
                    "integration_ids": integration_ids,
                },
                policy_create_params.PolicyCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[Optional[PolicyCreateResponse]]._unwrapper,
            ),
            cast_to=cast(Type[Optional[PolicyCreateResponse]], ResultWrapper[PolicyCreateResponse]),
        )

    async def update(
        self,
        policy_id: str,
        *,
        account_id: str,
        actions: policy_update_params.Actions,
        applies_to_all_integrations: bool,
        display_name: str,
        enabled: bool,
        description: str | Omit = omit,
        integration_ids: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[PolicyUpdateResponse]:
        """
        Updates an existing policy configuration and replaces its actions.

        Args:
          actions: Actions to execute when this policy is triggered, grouped by action type. A
              policy must contain at least one action across all groups and may include at
              most one remediation.

          applies_to_all_integrations: When true, the policy applies to all integrations for the account. When false,
              integration_ids must be provided.

          display_name: Display name for the policy configuration.

          enabled: Boolean specifying if the policy is enabled or disabled.

          description: Optional description of what this policy does.

          integration_ids: The integrations this policy applies to. Required when
              applies_to_all_integrations is false.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not policy_id:
            raise ValueError(f"Expected a non-empty value for `policy_id` but received {policy_id!r}")
        return await self._put(
            path_template(
                "/accounts/{account_id}/data-security/posture/policies/{policy_id}",
                account_id=account_id,
                policy_id=policy_id,
            ),
            body=await async_maybe_transform(
                {
                    "actions": actions,
                    "applies_to_all_integrations": applies_to_all_integrations,
                    "display_name": display_name,
                    "enabled": enabled,
                    "description": description,
                    "integration_ids": integration_ids,
                },
                policy_update_params.PolicyUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[Optional[PolicyUpdateResponse]]._unwrapper,
            ),
            cast_to=cast(Type[Optional[PolicyUpdateResponse]], ResultWrapper[PolicyUpdateResponse]),
        )

    def list(
        self,
        *,
        account_id: str,
        cursor: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[PolicyListResponse, AsyncCursorPaginationAfter[PolicyListResponse]]:
        """Returns a list of integration-scoped policy configurations for the given
        account.

        This endpoint supports cursor based pagination. By default, results are
        returned in sorted order based on created_at.

        Args:
          cursor: Cursor for pagination. Obtained from the `result_info.cursor` field of a
              previous response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        return self._get_api_list(
            path_template("/accounts/{account_id}/data-security/posture/policies", account_id=account_id),
            page=AsyncCursorPaginationAfter[PolicyListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"cursor": cursor}, policy_list_params.PolicyListParams),
            ),
            model=PolicyListResponse,
        )

    async def delete(
        self,
        policy_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[PolicyDeleteResponse]:
        """
        Deletes a policy configuration.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not policy_id:
            raise ValueError(f"Expected a non-empty value for `policy_id` but received {policy_id!r}")
        return await self._delete(
            path_template(
                "/accounts/{account_id}/data-security/posture/policies/{policy_id}",
                account_id=account_id,
                policy_id=policy_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[Optional[PolicyDeleteResponse]]._unwrapper,
            ),
            cast_to=cast(Type[Optional[PolicyDeleteResponse]], ResultWrapper[PolicyDeleteResponse]),
        )

    async def get(
        self,
        policy_id: str,
        *,
        account_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[PolicyGetResponse]:
        """
        Retrieves the details of a specific policy configuration, including its
        associated remediation and webhook actions.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not account_id:
            raise ValueError(f"Expected a non-empty value for `account_id` but received {account_id!r}")
        if not policy_id:
            raise ValueError(f"Expected a non-empty value for `policy_id` but received {policy_id!r}")
        return await self._get(
            path_template(
                "/accounts/{account_id}/data-security/posture/policies/{policy_id}",
                account_id=account_id,
                policy_id=policy_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                post_parser=ResultWrapper[Optional[PolicyGetResponse]]._unwrapper,
            ),
            cast_to=cast(Type[Optional[PolicyGetResponse]], ResultWrapper[PolicyGetResponse]),
        )


class PoliciesResourceWithRawResponse:
    def __init__(self, policies: PoliciesResource) -> None:
        self._policies = policies

        self.create = to_raw_response_wrapper(
            policies.create,
        )
        self.update = to_raw_response_wrapper(
            policies.update,
        )
        self.list = to_raw_response_wrapper(
            policies.list,
        )
        self.delete = to_raw_response_wrapper(
            policies.delete,
        )
        self.get = to_raw_response_wrapper(
            policies.get,
        )


class AsyncPoliciesResourceWithRawResponse:
    def __init__(self, policies: AsyncPoliciesResource) -> None:
        self._policies = policies

        self.create = async_to_raw_response_wrapper(
            policies.create,
        )
        self.update = async_to_raw_response_wrapper(
            policies.update,
        )
        self.list = async_to_raw_response_wrapper(
            policies.list,
        )
        self.delete = async_to_raw_response_wrapper(
            policies.delete,
        )
        self.get = async_to_raw_response_wrapper(
            policies.get,
        )


class PoliciesResourceWithStreamingResponse:
    def __init__(self, policies: PoliciesResource) -> None:
        self._policies = policies

        self.create = to_streamed_response_wrapper(
            policies.create,
        )
        self.update = to_streamed_response_wrapper(
            policies.update,
        )
        self.list = to_streamed_response_wrapper(
            policies.list,
        )
        self.delete = to_streamed_response_wrapper(
            policies.delete,
        )
        self.get = to_streamed_response_wrapper(
            policies.get,
        )


class AsyncPoliciesResourceWithStreamingResponse:
    def __init__(self, policies: AsyncPoliciesResource) -> None:
        self._policies = policies

        self.create = async_to_streamed_response_wrapper(
            policies.create,
        )
        self.update = async_to_streamed_response_wrapper(
            policies.update,
        )
        self.list = async_to_streamed_response_wrapper(
            policies.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            policies.delete,
        )
        self.get = async_to_streamed_response_wrapper(
            policies.get,
        )
