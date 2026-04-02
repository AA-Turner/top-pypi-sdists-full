import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Section")


@_attrs_define
class Section:
    """
    Attributes:
        url (str):
        key (str):
        created (datetime.datetime):
        title (str):
        category (str):
        category_title (str):
        is_standalone (Union[Unset, bool]): Whether section is rendered as a separate tab.
    """

    url: str
    key: str
    created: datetime.datetime
    title: str
    category: str
    category_title: str
    is_standalone: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        key = self.key

        created = self.created.isoformat()

        title = self.title

        category = self.category

        category_title = self.category_title

        is_standalone = self.is_standalone

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "key": key,
                "created": created,
                "title": title,
                "category": category,
                "category_title": category_title,
            }
        )
        if is_standalone is not UNSET:
            field_dict["is_standalone"] = is_standalone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        key = d.pop("key")

        created = isoparse(d.pop("created"))

        title = d.pop("title")

        category = d.pop("category")

        category_title = d.pop("category_title")

        is_standalone = d.pop("is_standalone", UNSET)

        section = cls(
            url=url,
            key=key,
            created=created,
            title=title,
            category=category,
            category_title=category_title,
            is_standalone=is_standalone,
        )

        section.additional_properties = d
        return section

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
