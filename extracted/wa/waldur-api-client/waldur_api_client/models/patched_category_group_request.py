from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="PatchedCategoryGroupRequest")


@_attrs_define
class PatchedCategoryGroupRequest:
    """
    Attributes:
        title (Union[Unset, str]):
        description (Union[Unset, str]):
        icon (Union[File, None, Unset]):
    """

    title: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    icon: Union[File, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        description = self.description

        icon: Union[None, Unset, types.FileTypes]
        if isinstance(self.icon, Unset):
            icon = UNSET
        elif isinstance(self.icon, File):
            icon = self.icon.to_tuple()

        else:
            icon = self.icon

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if icon is not UNSET:
            field_dict["icon"] = icon

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        def _parse_icon(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                icon_type_0 = File(payload=BytesIO(data))

                return icon_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        icon = _parse_icon(d.pop("icon", UNSET))

        patched_category_group_request = cls(
            title=title,
            description=description,
            icon=icon,
        )

        patched_category_group_request.additional_properties = d
        return patched_category_group_request

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
