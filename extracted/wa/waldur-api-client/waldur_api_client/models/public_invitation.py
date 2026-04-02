import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.invitation_coi_configuration import InvitationCOIConfiguration
    from ..models.invitation_proposal_summary import InvitationProposalSummary


T = TypeVar("T", bound="PublicInvitation")


@_attrs_define
class PublicInvitation:
    """
    Attributes:
        call_name (str):
        call_uuid (UUID):
        invitation_status (str):
        expires_at (Union[None, datetime.datetime]):
        is_expired (bool):
        max_assignments (Union[None, int]):
        invited_by_name (Union[None, str]): Name of the person who sent the invitation
        profile_status (Union[None, str]): User's profile status: 'published', 'unpublished', 'missing', or null if not
            authenticated
        requires_profile (bool): Whether the invitation requires creating a reviewer profile
        coi_configuration (Union['InvitationCOIConfiguration', None]): COI configuration for this call
        coi_types (list[list[str]]): Available COI types as list of [value, label] tuples
        proposals (list['InvitationProposalSummary']): Proposals for which conflicts can be declared
    """

    call_name: str
    call_uuid: UUID
    invitation_status: str
    expires_at: Union[None, datetime.datetime]
    is_expired: bool
    max_assignments: Union[None, int]
    invited_by_name: Union[None, str]
    profile_status: Union[None, str]
    requires_profile: bool
    coi_configuration: Union["InvitationCOIConfiguration", None]
    coi_types: list[list[str]]
    proposals: list["InvitationProposalSummary"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.invitation_coi_configuration import InvitationCOIConfiguration

        call_name = self.call_name

        call_uuid = str(self.call_uuid)

        invitation_status = self.invitation_status

        expires_at: Union[None, str]
        if isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        is_expired = self.is_expired

        max_assignments: Union[None, int]
        max_assignments = self.max_assignments

        invited_by_name: Union[None, str]
        invited_by_name = self.invited_by_name

        profile_status: Union[None, str]
        profile_status = self.profile_status

        requires_profile = self.requires_profile

        coi_configuration: Union[None, dict[str, Any]]
        if isinstance(self.coi_configuration, InvitationCOIConfiguration):
            coi_configuration = self.coi_configuration.to_dict()
        else:
            coi_configuration = self.coi_configuration

        coi_types = []
        for coi_types_item_data in self.coi_types:
            coi_types_item = coi_types_item_data

            coi_types.append(coi_types_item)

        proposals = []
        for proposals_item_data in self.proposals:
            proposals_item = proposals_item_data.to_dict()
            proposals.append(proposals_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "call_name": call_name,
                "call_uuid": call_uuid,
                "invitation_status": invitation_status,
                "expires_at": expires_at,
                "is_expired": is_expired,
                "max_assignments": max_assignments,
                "invited_by_name": invited_by_name,
                "profile_status": profile_status,
                "requires_profile": requires_profile,
                "coi_configuration": coi_configuration,
                "coi_types": coi_types,
                "proposals": proposals,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.invitation_coi_configuration import InvitationCOIConfiguration
        from ..models.invitation_proposal_summary import InvitationProposalSummary

        d = dict(src_dict)
        call_name = d.pop("call_name")

        call_uuid = UUID(d.pop("call_uuid"))

        invitation_status = d.pop("invitation_status")

        def _parse_expires_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        expires_at = _parse_expires_at(d.pop("expires_at"))

        is_expired = d.pop("is_expired")

        def _parse_max_assignments(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_assignments = _parse_max_assignments(d.pop("max_assignments"))

        def _parse_invited_by_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        invited_by_name = _parse_invited_by_name(d.pop("invited_by_name"))

        def _parse_profile_status(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        profile_status = _parse_profile_status(d.pop("profile_status"))

        requires_profile = d.pop("requires_profile")

        def _parse_coi_configuration(data: object) -> Union["InvitationCOIConfiguration", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                coi_configuration_type_1 = InvitationCOIConfiguration.from_dict(data)

                return coi_configuration_type_1
            except:  # noqa: E722
                pass
            return cast(Union["InvitationCOIConfiguration", None], data)

        coi_configuration = _parse_coi_configuration(d.pop("coi_configuration"))

        coi_types = []
        _coi_types = d.pop("coi_types")
        for coi_types_item_data in _coi_types:
            coi_types_item = cast(list[str], coi_types_item_data)

            coi_types.append(coi_types_item)

        proposals = []
        _proposals = d.pop("proposals")
        for proposals_item_data in _proposals:
            proposals_item = InvitationProposalSummary.from_dict(proposals_item_data)

            proposals.append(proposals_item)

        public_invitation = cls(
            call_name=call_name,
            call_uuid=call_uuid,
            invitation_status=invitation_status,
            expires_at=expires_at,
            is_expired=is_expired,
            max_assignments=max_assignments,
            invited_by_name=invited_by_name,
            profile_status=profile_status,
            requires_profile=requires_profile,
            coi_configuration=coi_configuration,
            coi_types=coi_types,
            proposals=proposals,
        )

        public_invitation.additional_properties = d
        return public_invitation

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
