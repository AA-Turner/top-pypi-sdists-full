from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ServiceProviderComplianceOverview")


@_attrs_define
class ServiceProviderComplianceOverview:
    """
    Attributes:
        offering_uuid (UUID):
        offering_name (str):
        checklist_name (Union[None, str]):
        total_users (int):
        users_with_completions (int):
        completed_users (int):
        pending_users (int):
        compliance_rate (float):
    """

    offering_uuid: UUID
    offering_name: str
    checklist_name: Union[None, str]
    total_users: int
    users_with_completions: int
    completed_users: int
    pending_users: int
    compliance_rate: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        checklist_name: Union[None, str]
        checklist_name = self.checklist_name

        total_users = self.total_users

        users_with_completions = self.users_with_completions

        completed_users = self.completed_users

        pending_users = self.pending_users

        compliance_rate = self.compliance_rate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "checklist_name": checklist_name,
                "total_users": total_users,
                "users_with_completions": users_with_completions,
                "completed_users": completed_users,
                "pending_users": pending_users,
                "compliance_rate": compliance_rate,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        def _parse_checklist_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        checklist_name = _parse_checklist_name(d.pop("checklist_name"))

        total_users = d.pop("total_users")

        users_with_completions = d.pop("users_with_completions")

        completed_users = d.pop("completed_users")

        pending_users = d.pop("pending_users")

        compliance_rate = d.pop("compliance_rate")

        service_provider_compliance_overview = cls(
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            checklist_name=checklist_name,
            total_users=total_users,
            users_with_completions=users_with_completions,
            completed_users=completed_users,
            pending_users=pending_users,
            compliance_rate=compliance_rate,
        )

        service_provider_compliance_overview.additional_properties = d
        return service_provider_compliance_overview

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
