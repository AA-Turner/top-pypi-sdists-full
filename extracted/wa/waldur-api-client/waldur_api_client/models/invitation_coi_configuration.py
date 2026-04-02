from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InvitationCOIConfiguration")


@_attrs_define
class InvitationCOIConfiguration:
    """
    Attributes:
        recusal_required_types (list[str]): COI types requiring automatic recusal
        management_allowed_types (list[str]): COI types where a management plan can be submitted
        disclosure_only_types (list[str]): COI types that only need disclosure
        proposal_disclosure_level (str): How much proposal info is disclosed to reviewers
    """

    recusal_required_types: list[str]
    management_allowed_types: list[str]
    disclosure_only_types: list[str]
    proposal_disclosure_level: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recusal_required_types = self.recusal_required_types

        management_allowed_types = self.management_allowed_types

        disclosure_only_types = self.disclosure_only_types

        proposal_disclosure_level = self.proposal_disclosure_level

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recusal_required_types": recusal_required_types,
                "management_allowed_types": management_allowed_types,
                "disclosure_only_types": disclosure_only_types,
                "proposal_disclosure_level": proposal_disclosure_level,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recusal_required_types = cast(list[str], d.pop("recusal_required_types"))

        management_allowed_types = cast(list[str], d.pop("management_allowed_types"))

        disclosure_only_types = cast(list[str], d.pop("disclosure_only_types"))

        proposal_disclosure_level = d.pop("proposal_disclosure_level")

        invitation_coi_configuration = cls(
            recusal_required_types=recusal_required_types,
            management_allowed_types=management_allowed_types,
            disclosure_only_types=disclosure_only_types,
            proposal_disclosure_level=proposal_disclosure_level,
        )

        invitation_coi_configuration.additional_properties = d
        return invitation_coi_configuration

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
