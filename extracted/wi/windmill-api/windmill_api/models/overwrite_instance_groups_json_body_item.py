from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OverwriteInstanceGroupsJsonBodyItem")


@_attrs_define
class OverwriteInstanceGroupsJsonBodyItem:
    """
    Attributes:
        name (str):
        summary (Union[Unset, str]):
        emails (Union[Unset, List[str]]):
        id (Union[Unset, str]):
        scim_display_name (Union[Unset, str]):
        external_id (Union[Unset, str]):
    """

    name: str
    summary: Union[Unset, str] = UNSET
    emails: Union[Unset, List[str]] = UNSET
    id: Union[Unset, str] = UNSET
    scim_display_name: Union[Unset, str] = UNSET
    external_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        summary = self.summary
        emails: Union[Unset, List[str]] = UNSET
        if not isinstance(self.emails, Unset):
            emails = self.emails

        id = self.id
        scim_display_name = self.scim_display_name
        external_id = self.external_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary
        if emails is not UNSET:
            field_dict["emails"] = emails
        if id is not UNSET:
            field_dict["id"] = id
        if scim_display_name is not UNSET:
            field_dict["scim_display_name"] = scim_display_name
        if external_id is not UNSET:
            field_dict["external_id"] = external_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        summary = d.pop("summary", UNSET)

        emails = cast(List[str], d.pop("emails", UNSET))

        id = d.pop("id", UNSET)

        scim_display_name = d.pop("scim_display_name", UNSET)

        external_id = d.pop("external_id", UNSET)

        overwrite_instance_groups_json_body_item = cls(
            name=name,
            summary=summary,
            emails=emails,
            id=id,
            scim_display_name=scim_display_name,
            external_id=external_id,
        )

        overwrite_instance_groups_json_body_item.additional_properties = d
        return overwrite_instance_groups_json_body_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
