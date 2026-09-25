from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_api_key_response import UserApiKeyResponse


T = TypeVar("T", bound="ListPageUserApiKeyResponse")


@_attrs_define
class ListPageUserApiKeyResponse:
    """
    Attributes:
        items (list[UserApiKeyResponse]): The rows of this page, in sort order.
        limit (int): The page size this page was fetched with.
        offset (int): How many rows were skipped before this page.
        total (int): Rows matching the filters, reported up to 10001.
        next_cursor (None | str | Unset): Cursor for the page after this one; null on the last.
    """

    items: list[UserApiKeyResponse]
    limit: int
    offset: int
    total: int
    next_cursor: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        limit = self.limit

        offset = self.offset

        total = self.total

        next_cursor: None | str | Unset
        if isinstance(self.next_cursor, Unset):
            next_cursor = UNSET
        else:
            next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "limit": limit,
                "offset": offset,
                "total": total,
            }
        )
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_api_key_response import UserApiKeyResponse

        d = dict(src_dict)
        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = UserApiKeyResponse.from_dict(items_item_data)

            items.append(items_item)

        limit = d.pop("limit")

        offset = d.pop("offset")

        total = d.pop("total")

        def _parse_next_cursor(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor", UNSET))

        list_page_user_api_key_response = cls(
            items=items,
            limit=limit,
            offset=offset,
            total=total,
            next_cursor=next_cursor,
        )

        list_page_user_api_key_response.additional_properties = d
        return list_page_user_api_key_response

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
