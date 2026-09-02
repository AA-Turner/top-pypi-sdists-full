from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_assets_response_200_assets_item import ListAssetsResponse200AssetsItem
    from ..models.list_assets_response_200_next_cursor import ListAssetsResponse200NextCursor


T = TypeVar("T", bound="ListAssetsResponse200")


@_attrs_define
class ListAssetsResponse200:
    """
    Attributes:
        assets (List['ListAssetsResponse200AssetsItem']):
        next_cursor (Union[Unset, None, ListAssetsResponse200NextCursor]): Cursor for the next page (null if no more
            pages)
    """

    assets: List["ListAssetsResponse200AssetsItem"]
    next_cursor: Union[Unset, None, "ListAssetsResponse200NextCursor"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        assets = []
        for assets_item_data in self.assets:
            assets_item = assets_item_data.to_dict()

            assets.append(assets_item)

        next_cursor: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.next_cursor, Unset):
            next_cursor = self.next_cursor.to_dict() if self.next_cursor else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "assets": assets,
            }
        )
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_assets_response_200_assets_item import ListAssetsResponse200AssetsItem
        from ..models.list_assets_response_200_next_cursor import ListAssetsResponse200NextCursor

        d = src_dict.copy()
        assets = []
        _assets = d.pop("assets")
        for assets_item_data in _assets:
            assets_item = ListAssetsResponse200AssetsItem.from_dict(assets_item_data)

            assets.append(assets_item)

        _next_cursor = d.pop("next_cursor", UNSET)
        next_cursor: Union[Unset, None, ListAssetsResponse200NextCursor]
        if _next_cursor is None:
            next_cursor = None
        elif isinstance(_next_cursor, Unset):
            next_cursor = UNSET
        else:
            next_cursor = ListAssetsResponse200NextCursor.from_dict(_next_cursor)

        list_assets_response_200 = cls(
            assets=assets,
            next_cursor=next_cursor,
        )

        list_assets_response_200.additional_properties = d
        return list_assets_response_200

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
