from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SramRulePreviewProject")


@_attrs_define
class SramRulePreviewProject:
    """
    Attributes:
        uuid (UUID):
        name (str):
        slug (str):
        backend_id (Union[Unset, str]):
    """

    uuid: UUID
    name: str
    slug: str
    backend_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        slug = self.slug

        backend_id = self.backend_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "slug": slug,
            }
        )
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        slug = d.pop("slug")

        backend_id = d.pop("backend_id", UNSET)

        sram_rule_preview_project = cls(
            uuid=uuid,
            name=name,
            slug=slug,
            backend_id=backend_id,
        )

        sram_rule_preview_project.additional_properties = d
        return sram_rule_preview_project

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
