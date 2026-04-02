from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blank_enum import BlankEnum
from ..models.oecd_fos_2007_code_enum import OecdFos2007CodeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProposalRequest")


@_attrs_define
class ProposalRequest:
    """
    Attributes:
        name (str):
        round_uuid (UUID):
        description (Union[Unset, str]):
        project_summary (Union[Unset, str]):
        project_is_confidential (Union[Unset, bool]):
        project_has_civilian_purpose (Union[Unset, bool]):
        duration_in_days (Union[None, Unset, int]): Duration in days after provisioning of resources.
        oecd_fos_2007_code (Union[BlankEnum, None, OecdFos2007CodeEnum, Unset]):
    """

    name: str
    round_uuid: UUID
    description: Union[Unset, str] = UNSET
    project_summary: Union[Unset, str] = UNSET
    project_is_confidential: Union[Unset, bool] = UNSET
    project_has_civilian_purpose: Union[Unset, bool] = UNSET
    duration_in_days: Union[None, Unset, int] = UNSET
    oecd_fos_2007_code: Union[BlankEnum, None, OecdFos2007CodeEnum, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        round_uuid = str(self.round_uuid)

        description = self.description

        project_summary = self.project_summary

        project_is_confidential = self.project_is_confidential

        project_has_civilian_purpose = self.project_has_civilian_purpose

        duration_in_days: Union[None, Unset, int]
        if isinstance(self.duration_in_days, Unset):
            duration_in_days = UNSET
        else:
            duration_in_days = self.duration_in_days

        oecd_fos_2007_code: Union[None, Unset, str]
        if isinstance(self.oecd_fos_2007_code, Unset):
            oecd_fos_2007_code = UNSET
        elif isinstance(self.oecd_fos_2007_code, OecdFos2007CodeEnum):
            oecd_fos_2007_code = self.oecd_fos_2007_code.value
        elif isinstance(self.oecd_fos_2007_code, BlankEnum):
            oecd_fos_2007_code = self.oecd_fos_2007_code.value
        else:
            oecd_fos_2007_code = self.oecd_fos_2007_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "round_uuid": round_uuid,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if project_summary is not UNSET:
            field_dict["project_summary"] = project_summary
        if project_is_confidential is not UNSET:
            field_dict["project_is_confidential"] = project_is_confidential
        if project_has_civilian_purpose is not UNSET:
            field_dict["project_has_civilian_purpose"] = project_has_civilian_purpose
        if duration_in_days is not UNSET:
            field_dict["duration_in_days"] = duration_in_days
        if oecd_fos_2007_code is not UNSET:
            field_dict["oecd_fos_2007_code"] = oecd_fos_2007_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        round_uuid = UUID(d.pop("round_uuid"))

        description = d.pop("description", UNSET)

        project_summary = d.pop("project_summary", UNSET)

        project_is_confidential = d.pop("project_is_confidential", UNSET)

        project_has_civilian_purpose = d.pop("project_has_civilian_purpose", UNSET)

        def _parse_duration_in_days(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        duration_in_days = _parse_duration_in_days(d.pop("duration_in_days", UNSET))

        def _parse_oecd_fos_2007_code(data: object) -> Union[BlankEnum, None, OecdFos2007CodeEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                oecd_fos_2007_code_type_0 = OecdFos2007CodeEnum(data)

                return oecd_fos_2007_code_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                oecd_fos_2007_code_type_1 = BlankEnum(data)

                return oecd_fos_2007_code_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BlankEnum, None, OecdFos2007CodeEnum, Unset], data)

        oecd_fos_2007_code = _parse_oecd_fos_2007_code(d.pop("oecd_fos_2007_code", UNSET))

        proposal_request = cls(
            name=name,
            round_uuid=round_uuid,
            description=description,
            project_summary=project_summary,
            project_is_confidential=project_is_confidential,
            project_has_civilian_purpose=project_has_civilian_purpose,
            duration_in_days=duration_in_days,
            oecd_fos_2007_code=oecd_fos_2007_code,
        )

        proposal_request.additional_properties = d
        return proposal_request

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
