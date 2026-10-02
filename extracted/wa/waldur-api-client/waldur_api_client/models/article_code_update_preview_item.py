from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ArticleCodeUpdatePreviewItem")


@_attrs_define
class ArticleCodeUpdatePreviewItem:
    """
    Attributes:
        component_uuid (UUID):
        component_type (str):
        component_name (str):
        offering_uuid (UUID):
        offering_name (str):
        offering_customer_name (str):
        old_article_code (str):
        new_article_code (str):
    """

    component_uuid: UUID
    component_type: str
    component_name: str
    offering_uuid: UUID
    offering_name: str
    offering_customer_name: str
    old_article_code: str
    new_article_code: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        component_uuid = str(self.component_uuid)

        component_type = self.component_type

        component_name = self.component_name

        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        offering_customer_name = self.offering_customer_name

        old_article_code = self.old_article_code

        new_article_code = self.new_article_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "component_uuid": component_uuid,
                "component_type": component_type,
                "component_name": component_name,
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "offering_customer_name": offering_customer_name,
                "old_article_code": old_article_code,
                "new_article_code": new_article_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        component_uuid = UUID(d.pop("component_uuid"))

        component_type = d.pop("component_type")

        component_name = d.pop("component_name")

        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        offering_customer_name = d.pop("offering_customer_name")

        old_article_code = d.pop("old_article_code")

        new_article_code = d.pop("new_article_code")

        article_code_update_preview_item = cls(
            component_uuid=component_uuid,
            component_type=component_type,
            component_name=component_name,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            offering_customer_name=offering_customer_name,
            old_article_code=old_article_code,
            new_article_code=new_article_code,
        )

        article_code_update_preview_item.additional_properties = d
        return article_code_update_preview_item

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
