from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExpertiseCategory")


@_attrs_define
class ExpertiseCategory:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        code (str):
        description (Union[Unset, str]):
        parent (Union[None, Unset, str]):
        level (Union[Unset, int]): Depth in hierarchy (0 = root)
    """

    url: str
    uuid: UUID
    name: str
    code: str
    description: Union[Unset, str] = UNSET
    parent: Union[None, Unset, str] = UNSET
    level: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        code = self.code

        description = self.description

        parent: Union[None, Unset, str]
        if isinstance(self.parent, Unset):
            parent = UNSET
        else:
            parent = self.parent

        level = self.level

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "code": code,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if parent is not UNSET:
            field_dict["parent"] = parent
        if level is not UNSET:
            field_dict["level"] = level

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        code = d.pop("code")

        description = d.pop("description", UNSET)

        def _parse_parent(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parent = _parse_parent(d.pop("parent", UNSET))

        level = d.pop("level", UNSET)

        expertise_category = cls(
            url=url,
            uuid=uuid,
            name=name,
            code=code,
            description=description,
            parent=parent,
            level=level,
        )

        expertise_category.additional_properties = d
        return expertise_category

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
