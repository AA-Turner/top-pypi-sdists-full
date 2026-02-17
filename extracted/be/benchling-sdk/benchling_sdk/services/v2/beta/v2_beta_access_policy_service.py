from typing import List, Optional

from benchling_api_client.v2.beta.api.access_policies import (
    get_general_access_policy,
    get_schema_access_policy,
    list_general_access_policies,
    list_schema_access_policies,
)
from benchling_api_client.v2.beta.models.access_policies_paginated_list import AccessPoliciesPaginatedList
from benchling_api_client.v2.beta.models.access_policy import AccessPolicy
from benchling_api_client.v2.beta.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset
from benchling_sdk.services.v2.base_service import BaseService


def _list_results_extractor(body: AccessPoliciesPaginatedList) -> Optional[List[AccessPolicy]]:
    return body.policies


class V2BetaAccessPolicyService(BaseService):
    """
    V2-Beta Access Policies.

    View access policies.

    https://benchling.com/api/v2-beta/reference#/Access%20Policies
    """

    @api_method
    def _general_access_policies_page(
        self,
        next_token: Optional[NextToken] = None,
        page_size: Optional[int] = 50,
    ) -> Response[AccessPoliciesPaginatedList]:
        response = list_general_access_policies.sync_detailed(
            client=self.client,
            next_token=none_as_unset(next_token),
            page_size=none_as_unset(page_size),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list_general_access_policies(self, page_size: Optional[int] = None):
        """
        Return a list of general (project/registry) access policies.

        See https://benchling.com/api/v2-beta/reference#/Access%20Policies/listGeneralAccessPolicies
        """
        def api_call(next_token: NextToken) -> Response[AccessPoliciesPaginatedList]:
            return self._general_access_policies_page(next_token, page_size)

        return PageIterator(api_call, _list_results_extractor)

    @api_method
    def get_general_access_policy_by_id(self, policy_id: str) -> AccessPolicy:
        """
        Return a general (project/registry) policy by ID.

        See https://benchling.com/api/v2-beta/reference#/Access%20Policies/getGeneralAccessPolicy
        """
        response = get_general_access_policy.sync_detailed(client=self.client, policy_id=policy_id)
        return model_from_detailed(response)  # type: ignore

    @api_method
    def _schema_access_policies_page(
        self,
        next_token: Optional[NextToken] = None,
        page_size: Optional[int] = 50,
    ) -> Response[AccessPoliciesPaginatedList]:
        response = list_schema_access_policies.sync_detailed(
            client=self.client,
            next_token=none_as_unset(next_token),
            page_size=none_as_unset(page_size),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list_schema_access_policies(self, page_size: Optional[int] = None):
        """
        Return a list of schema access policies.

        See https://benchling.com/api/v2-beta/reference#/Access%20Policies/listSchemaAccessPolicies
        """
        def api_call(next_token: NextToken) -> Response[AccessPoliciesPaginatedList]:
            return self._schema_access_policies_page(next_token, page_size)

        return PageIterator(api_call, _list_results_extractor)

    @api_method
    def get_schema_access_policy_by_id(self, policy_id: str) -> AccessPolicy:
        """
        Return a schema access policy by ID.

        See https://benchling.com/api/v2-beta/reference#/Access%20Policies/getSchemaAccessPolicy
        """
        response = get_schema_access_policy.sync_detailed(client=self.client, policy_id=policy_id)
        return model_from_detailed(response)  # type: ignore