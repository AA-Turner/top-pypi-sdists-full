from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CustomerMemberSummary")


@_attrs_define
class CustomerMemberSummary:
    """
    Attributes:
        total_organizations (int): Total number of organizations
        total_members (int): Total number of members across all organizations
        organizations_with_resources (int): Number of organizations with active resources
        average_members_per_org (int): Average number of members per organization
    """

    total_organizations: int
    total_members: int
    organizations_with_resources: int
    average_members_per_org: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_organizations = self.total_organizations

        total_members = self.total_members

        organizations_with_resources = self.organizations_with_resources

        average_members_per_org = self.average_members_per_org

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_organizations": total_organizations,
                "total_members": total_members,
                "organizations_with_resources": organizations_with_resources,
                "average_members_per_org": average_members_per_org,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_organizations = d.pop("total_organizations")

        total_members = d.pop("total_members")

        organizations_with_resources = d.pop("organizations_with_resources")

        average_members_per_org = d.pop("average_members_per_org")

        customer_member_summary = cls(
            total_organizations=total_organizations,
            total_members=total_members,
            organizations_with_resources=organizations_with_resources,
            average_members_per_org=average_members_per_org,
        )

        customer_member_summary.additional_properties = d
        return customer_member_summary

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
