# This file was auto-generated by Fern from our API Definition.

import typing_extensions
import typing_extensions
from ..types.team_member_assigned_locations_assignment_type import TeamMemberAssignedLocationsAssignmentType
import typing


class TeamMemberAssignedLocationsParams(typing_extensions.TypedDict):
    """
    An object that represents a team member's assignment to locations.
    """

    assignment_type: typing_extensions.NotRequired[TeamMemberAssignedLocationsAssignmentType]
    """
    The current assignment type of the team member.
    See [TeamMemberAssignedLocationsAssignmentType](#type-teammemberassignedlocationsassignmenttype) for possible values
    """

    location_ids: typing_extensions.NotRequired[typing.Optional[typing.Sequence[str]]]
    """
    The explicit locations that the team member is assigned to.
    """
