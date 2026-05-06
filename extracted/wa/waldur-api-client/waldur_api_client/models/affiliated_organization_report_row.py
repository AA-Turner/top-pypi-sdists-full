from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AffiliatedOrganizationReportRow")


@_attrs_define
class AffiliatedOrganizationReportRow:
    """
    Attributes:
        org_uuid (Union[None, UUID]):
        org_name (str):
        org_abbreviation (str):
        projects_count (int):
        resources_count (int):
        estimated_cost (str):
    """

    org_uuid: Union[None, UUID]
    org_name: str
    org_abbreviation: str
    projects_count: int
    resources_count: int
    estimated_cost: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        org_uuid: Union[None, str]
        if isinstance(self.org_uuid, UUID):
            org_uuid = str(self.org_uuid)
        else:
            org_uuid = self.org_uuid

        org_name = self.org_name

        org_abbreviation = self.org_abbreviation

        projects_count = self.projects_count

        resources_count = self.resources_count

        estimated_cost = self.estimated_cost

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "org_uuid": org_uuid,
                "org_name": org_name,
                "org_abbreviation": org_abbreviation,
                "projects_count": projects_count,
                "resources_count": resources_count,
                "estimated_cost": estimated_cost,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_org_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                org_uuid_type_0 = UUID(data)

                return org_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        org_uuid = _parse_org_uuid(d.pop("org_uuid"))

        org_name = d.pop("org_name")

        org_abbreviation = d.pop("org_abbreviation")

        projects_count = d.pop("projects_count")

        resources_count = d.pop("resources_count")

        estimated_cost = d.pop("estimated_cost")

        affiliated_organization_report_row = cls(
            org_uuid=org_uuid,
            org_name=org_name,
            org_abbreviation=org_abbreviation,
            projects_count=projects_count,
            resources_count=resources_count,
            estimated_cost=estimated_cost,
        )

        affiliated_organization_report_row.additional_properties = d
        return affiliated_organization_report_row

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
