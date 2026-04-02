from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.category_serializer_for_for_nested_fields import CategorySerializerForForNestedFields


T = TypeVar("T", bound="CategoryHelpArticles")


@_attrs_define
class CategoryHelpArticles:
    """
    Attributes:
        url (str):
        categories (list['CategorySerializerForForNestedFields']):
        title (Union[None, Unset, str]):
    """

    url: str
    categories: list["CategorySerializerForForNestedFields"]
    title: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        categories = []
        for categories_item_data in self.categories:
            categories_item = categories_item_data.to_dict()
            categories.append(categories_item)

        title: Union[None, Unset, str]
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "categories": categories,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.category_serializer_for_for_nested_fields import CategorySerializerForForNestedFields

        d = dict(src_dict)
        url = d.pop("url")

        categories = []
        _categories = d.pop("categories")
        for categories_item_data in _categories:
            categories_item = CategorySerializerForForNestedFields.from_dict(categories_item_data)

            categories.append(categories_item)

        def _parse_title(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        title = _parse_title(d.pop("title", UNSET))

        category_help_articles = cls(
            url=url,
            categories=categories,
            title=title,
        )

        category_help_articles.additional_properties = d
        return category_help_articles

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
