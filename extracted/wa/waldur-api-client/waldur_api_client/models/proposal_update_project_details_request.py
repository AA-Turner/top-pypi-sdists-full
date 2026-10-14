from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProposalUpdateProjectDetailsRequest")


@_attrs_define
class ProposalUpdateProjectDetailsRequest:
    """
    Attributes:
        name (str):
        description (Union[Unset, str]):
        project_summary (Union[Unset, str]):
        science_sub_domain (Union[None, UUID, Unset]):
    """

    name: str
    description: Union[Unset, str] = UNSET
    project_summary: Union[Unset, str] = UNSET
    science_sub_domain: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        project_summary = self.project_summary

        science_sub_domain: Union[None, Unset, str]
        if isinstance(self.science_sub_domain, Unset):
            science_sub_domain = UNSET
        elif isinstance(self.science_sub_domain, UUID):
            science_sub_domain = str(self.science_sub_domain)
        else:
            science_sub_domain = self.science_sub_domain

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if project_summary is not UNSET:
            field_dict["project_summary"] = project_summary
        if science_sub_domain is not UNSET:
            field_dict["science_sub_domain"] = science_sub_domain

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        project_summary = d.pop("project_summary", UNSET)

        def _parse_science_sub_domain(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                science_sub_domain_type_0 = UUID(data)

                return science_sub_domain_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        science_sub_domain = _parse_science_sub_domain(d.pop("science_sub_domain", UNSET))

        proposal_update_project_details_request = cls(
            name=name,
            description=description,
            project_summary=project_summary,
            science_sub_domain=science_sub_domain,
        )

        proposal_update_project_details_request.additional_properties = d
        return proposal_update_project_details_request

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
