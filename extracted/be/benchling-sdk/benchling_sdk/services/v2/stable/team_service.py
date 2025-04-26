from typing import Iterable, List, Optional, Union

from benchling_api_client.v2.stable.api.teams import (
    create_team,
    create_team_membership,
    delete_team_membership,
    get_team,
    get_team_membership,
    list_team_memberships,
    list_teams,
    update_team,
    update_team_membership,
)
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.constants import _translate_to_string_enum
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset, optional_array_query_param
from benchling_sdk.models import (
    ListTeamsSort,
    Membership,
    MembershipCreate,
    MembershipsPaginatedList,
    MembershipUpdate,
    Team,
    TeamCreate,
    TeamsPaginatedList,
    TeamUpdate,
)
from benchling_sdk.services.v2.base_service import BaseService


class TeamService(BaseService):
    """
    Teams.

    View team objects.

    See https://benchling.com/api/reference#/Teams
    """

    @api_method
    def get_by_id(self, team_id: str) -> Team:
        """
        Get a team by ID.

        See https://benchling.com/api/reference#/Teams/getTeam
        """
        response = get_team.sync_detailed(client=self.client, team_id=team_id)
        return model_from_detailed(response)

    @api_method
    def _teams_page(
        self,
        *,
        ids: Optional[Iterable[str]] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        names_any_of: Optional[Iterable[str]] = None,
        names_any_of_case_sensitive: Optional[Iterable[str]] = None,
        modified_at: Optional[str] = None,
        mentioned_in: Optional[Iterable[str]] = None,
        organization_id: Optional[str] = None,
        has_members: Optional[Iterable[str]] = None,
        has_admins: Optional[Iterable[str]] = None,
        sort: Optional[ListTeamsSort] = None,
        page_size: Optional[int] = 50,
        next_token: Optional[str] = None,
    ) -> Response[TeamsPaginatedList]:
        response = list_teams.sync_detailed(
            client=self.client,
            ids=none_as_unset(optional_array_query_param(ids)),
            name=none_as_unset(name),
            name_includes=none_as_unset(name_includes),
            namesany_of=none_as_unset(optional_array_query_param(names_any_of)),
            namesany_ofcase_sensitive=none_as_unset(optional_array_query_param(names_any_of_case_sensitive)),
            modified_at=none_as_unset(modified_at),
            mentioned_in=none_as_unset(optional_array_query_param(mentioned_in)),
            organization_id=none_as_unset(organization_id),
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
        mentioned_in: Optional[Iterable[str]] = None,
        organization_id: Optional[str] = None,
        has_members: Optional[Iterable[str]] = None,
        has_admins: Optional[Iterable[str]] = None,
        sort: Optional[Union[str, ListTeamsSort]] = None,
        page_size: Optional[int] = 50,
    ) -> PageIterator[Team]:
        """
        List teams.

        Returns all teams that the caller has permission to view. The following roles have view permission:
        * tenant admins
        * members of the team's organization

        See https://benchling.com/api/reference#/Teams/listTeams
        """

        def api_call(next_token: NextToken) -> Response[TeamsPaginatedList]:
            return self._teams_page(
                ids=ids,
                name=name,
                name_includes=name_includes,
                names_any_of=names_any_of,
                names_any_of_case_sensitive=names_any_of_case_sensitive,
                modified_at=modified_at,
                mentioned_in=mentioned_in,
                organization_id=organization_id,
                has_members=has_members,
                has_admins=has_admins,
                sort=_translate_to_string_enum(ListTeamsSort, sort),
                next_token=next_token,
                page_size=page_size,
            )

        def results_extractor(body: TeamsPaginatedList) -> Optional[List[Team]]:
            return body.teams

        return PageIterator(api_call, results_extractor)

    @api_method
    def create(self, team: TeamCreate) -> Team:
        """
        Create team.

        See https://benchling.com/api/reference#/Teams/createTeam
        """
        response = create_team.sync_detailed(client=self.client, json_body=team)
        return model_from_detailed(response)

    @api_method
    def update(self, team_id: str, team: TeamUpdate) -> Team:
        """
        Update team.

        See https://benchling.com/api/reference#/Teams/updateTeam
        """
        response = update_team.sync_detailed(client=self.client, team_id=team_id, json_body=team)
        return model_from_detailed(response)

    @api_method
    def _list_memberships_page(
        self,
        team_id: str,
        role: Optional[str],
        page_size: Optional[int],
        next_token: NextToken,
    ) -> Response[MembershipsPaginatedList]:
        response = list_team_memberships.sync_detailed(
            client=self.client,
            team_id=team_id,
            page_size=none_as_unset(page_size),
            next_token=next_token,
            role=none_as_unset(role),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list_memberships(
        self,
        team_id: str,
        role: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[MembershipsPaginatedList]:
        """
        Return all team memberships in the given team.

        See https://benchling.com/api/reference#/Teams/listTeamMemberships
        """

        def api_call(next_token: NextToken) -> Response[MembershipsPaginatedList]:
            return self._list_memberships_page(team_id, role, page_size, next_token)

        return PageIterator(api_call, lambda body: body.memberships)

    @api_method
    def get_membership(self, team_id: str, user_id: str) -> Membership:
        """
        Get team membership.

        See https://benchling.com/api/reference#/Teams/getTeamMembership
        """
        response = get_team_membership.sync_detailed(client=self.client, team_id=team_id, user_id=user_id)
        return model_from_detailed(response)

    @api_method
    def create_membership(self, team_id: str, membership: MembershipCreate) -> Membership:
        """
        Create team membership for the given user, role, and team.

        See https://benchling.com/api/reference#/Teams/createTeamMembership
        """
        response = create_team_membership.sync_detailed(
            client=self.client,
            team_id=team_id,
            json_body=membership,
        )
        return model_from_detailed(response)

    @api_method
    def update_membership(self, team_id: str, user_id: str, membership: MembershipUpdate) -> Membership:
        """
        Update a single team membership.

        See https://benchling.com/api/reference#/Teams/updateTeamMembership
        """
        response = update_team_membership.sync_detailed(
            client=self.client,
            team_id=team_id,
            user_id=user_id,
            json_body=membership,
        )
        return model_from_detailed(response)

    @api_method
    def delete_membership(self, team_id: str, user_id: str) -> None:
        """
        Delete a single team membership.

        See https://benchling.com/api/reference#/Teams/deleteTeamMembership
        """
        raise_for_status(
            delete_team_membership.sync_detailed(client=self.client, team_id=team_id, user_id=user_id)
        )
