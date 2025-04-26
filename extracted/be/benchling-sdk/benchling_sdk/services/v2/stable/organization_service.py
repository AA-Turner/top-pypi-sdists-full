from typing import Iterable, List, Optional, Union

from benchling_api_client.v2.stable.api.organizations import (
    create_organization_membership,
    delete_organization_membership,
    get_organization,
    get_organization_membership,
    list_organization_memberships,
    list_organizations,
    update_organization_membership,
)
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.constants import _translate_to_string_enum
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.logging_helpers import log_not_implemented
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset, optional_array_query_param
from benchling_sdk.models import (
    ListOrganizationsSort,
    Membership,
    MembershipCreate,
    MembershipsPaginatedList,
    MembershipUpdate,
    Organization,
    OrganizationsPaginatedList,
)
from benchling_sdk.services.v2.base_service import BaseService


class OrganizationService(BaseService):
    """
    Organizations.

    View organization objects.

    See https://benchling.com/api/reference#/Organizations
    """

    @api_method
    def get_by_id(self, organization_id: str) -> Organization:
        """
        Get an organization by ID.

        Returns an organization by ID if the caller has permission to view. The following roles have view permission:
        * tenant admins
        * members of the organization

        See https://benchling.com/api/reference#/Organizations/getOrganization
        """
        response = get_organization.sync_detailed(client=self.client, organization_id=organization_id)
        return model_from_detailed(response)

    @api_method
    def _organizations_page(
        self,
        *,
        ids: Optional[Iterable[str]] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        names_any_of: Optional[Iterable[str]] = None,
        names_any_of_case_sensitive: Optional[Iterable[str]] = None,
        modified_at: Optional[str] = None,
        has_members: Optional[Iterable[str]] = None,
        has_admins: Optional[Iterable[str]] = None,
        sort: Optional[ListOrganizationsSort] = None,
        page_size: Optional[int] = 50,
        next_token: Optional[str] = None,
    ) -> Response[OrganizationsPaginatedList]:
        response = list_organizations.sync_detailed(
            client=self.client,
            ids=none_as_unset(optional_array_query_param(ids)),
            name=none_as_unset(name),
            name_includes=none_as_unset(name_includes),
            namesany_of=none_as_unset(optional_array_query_param(names_any_of)),
            namesany_ofcase_sensitive=none_as_unset(optional_array_query_param(names_any_of_case_sensitive)),
            modified_at=none_as_unset(modified_at),
            has_members=none_as_unset(optional_array_query_param(has_members)),
            has_admins=none_as_unset(optional_array_query_param(has_admins)),
            page_size=none_as_unset(page_size),
            next_token=none_as_unset(next_token),
            sort=none_as_unset(sort),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list(
        self,
        *,
        ids: Optional[Iterable[str]] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        names_any_of: Optional[Iterable[str]] = None,
        names_any_of_case_sensitive: Optional[Iterable[str]] = None,
        modified_at: Optional[str] = None,
        has_members: Optional[Iterable[str]] = None,
        has_admins: Optional[Iterable[str]] = None,
        sort: Optional[Union[str, ListOrganizationsSort]] = None,
        page_size: Optional[int] = 50,
        mentioned_in: Optional[List[str]] = None,
    ) -> PageIterator[Organization]:
        """
        List organizations.

        Returns all organizations that the caller has permission to view. The following roles have view permission:
        * tenant admins
        * members of the organization

        See https://benchling.com/api/reference#/Organizations/listOrganizations
        """
        if mentioned_in:
            log_not_implemented("mentioned_in")

        def api_call(next_token: NextToken) -> Response[OrganizationsPaginatedList]:
            return self._organizations_page(
                ids=ids,
                name=name,
                name_includes=name_includes,
                names_any_of=names_any_of,
                names_any_of_case_sensitive=names_any_of_case_sensitive,
                modified_at=modified_at,
                has_members=has_members,
                has_admins=has_admins,
                sort=_translate_to_string_enum(ListOrganizationsSort, sort),
                next_token=next_token,
                page_size=page_size,
            )

        def results_extractor(body: OrganizationsPaginatedList) -> Optional[List[Organization]]:
            return body.organizations

        return PageIterator(api_call, results_extractor)

    @api_method
    def _list_memberships_page(
        self,
        organization_id: str,
        role: Optional[str],
        page_size: Optional[int],
        next_token: NextToken,
    ) -> Response[MembershipsPaginatedList]:
        response = list_organization_memberships.sync_detailed(
            client=self.client,
            organization_id=organization_id,
            page_size=none_as_unset(page_size),
            next_token=next_token,
            role=none_as_unset(role),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list_memberships(
        self,
        organization_id: str,
        role: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[MembershipsPaginatedList]:
        """
        Return all organization memberships in the given organization.

        See https://benchling.com/api/reference#/Organizations/listOrganizationMemberships
        """

        def api_call(next_token: NextToken) -> Response[MembershipsPaginatedList]:
            return self._list_memberships_page(organization_id, role, page_size, next_token)

        return PageIterator(api_call, lambda body: body.memberships)

    @api_method
    def get_membership(self, organization_id: str, user_id: str) -> Membership:
        """
        Get organization membership.

        See https://benchling.com/api/reference#/Organizations/getOrganizationMembership
        """
        response = get_organization_membership.sync_detailed(
            client=self.client, organization_id=organization_id, user_id=user_id
        )
        return model_from_detailed(response)

    @api_method
    def create_membership(self, organization_id: str, membership: MembershipCreate) -> Membership:
        """
        Create organization membership.

        See https://benchling.com/api/reference#/Organizations/createOrganizationMembership
        """
        response = create_organization_membership.sync_detailed(
            client=self.client,
            organization_id=organization_id,
            json_body=membership,
        )
        return model_from_detailed(response)

    @api_method
    def update_membership(
        self, organization_id: str, user_id: str, membership: MembershipUpdate
    ) -> Membership:
        """
        Update organization membership by user ID and organization ID.

        See https://benchling.com/api/reference#/Organizations/updateOrganizationMembership
        """
        response = update_organization_membership.sync_detailed(
            client=self.client,
            organization_id=organization_id,
            user_id=user_id,
            json_body=membership,
        )
        return model_from_detailed(response)

    @api_method
    def delete_membership(self, organization_id: str, user_id: str) -> None:
        """
        Delete a single team membership.

        See https://benchling.com/api/reference#/Organizations/deleteOrganizationMembership
        """
        raise_for_status(
            delete_organization_membership.sync_detailed(
                client=self.client, organization_id=organization_id, user_id=user_id
            )
        )
