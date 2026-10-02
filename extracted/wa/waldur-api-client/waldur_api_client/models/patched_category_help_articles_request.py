from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.category_serializer_for_for_nested_fields_request import CategorySerializerForForNestedFieldsRequest


T = TypeVar("T", bound="PatchedCategoryHelpArticlesRequest")


@_attrs_define
class PatchedCategoryHelpArticlesRequest:
    """
    Attributes:
        title (Union[None, Unset, str]):
        url (Union[Unset, str]):
        categories (Union[Unset, list['CategorySerializerForForNestedFieldsRequest']]):
    """

    title: Union[None, Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    categories: Union[Unset, list["CategorySerializerForForNestedFieldsRequest"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title: Union[None, Unset, str]
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        url = self.url

        categories: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.to_dict()
                categories.append(categories_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if url is not UNSET:
            field_dict["url"] = url
        if categories is not UNSET:
            field_dict["categories"] = categories

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.category_serializer_for_for_nested_fields_request import (
            CategorySerializerForForNestedFieldsRequest,
        )

        d = dict(src_dict)

        def _parse_title(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        title = _parse_title(d.pop("title", UNSET))

        url = d.pop("url", UNSET)

        categories = []
        _categories = d.pop("categories", UNSET)
        for categories_item_data in _categories or []:
            categories_item = CategorySerializerForForNestedFieldsRequest.from_dict(categories_item_data)

            categories.append(categories_item)

        patched_category_help_articles_request = cls(
            title=title,
            url=url,
            categories=categories,
        )

        patched_category_help_articles_request.additional_properties = d
        return patched_category_help_articles_request

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
