from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_run_assets_response_200_assets_item import ListRunAssetsResponse200AssetsItem


T = TypeVar("T", bound="ListRunAssetsResponse200")


@_attrs_define
class ListRunAssetsResponse200:
    """
    Attributes:
        truncated (bool): whether the run touched more assets than are listed
        assets (List['ListRunAssetsResponse200AssetsItem']):
    """

    truncated: bool
    assets: List["ListRunAssetsResponse200AssetsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        truncated = self.truncated
        assets = []
        for assets_item_data in self.assets:
            assets_item = assets_item_data.to_dict()

            assets.append(assets_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "truncated": truncated,
                "assets": assets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_run_assets_response_200_assets_item import ListRunAssetsResponse200AssetsItem

        d = src_dict.copy()
        truncated = d.pop("truncated")

        assets = []
        _assets = d.pop("assets")
        for assets_item_data in _assets:
            assets_item = ListRunAssetsResponse200AssetsItem.from_dict(assets_item_data)

            assets.append(assets_item)

        list_run_assets_response_200 = cls(
            truncated=truncated,
            assets=assets,
        )

        list_run_assets_response_200.additional_properties = d
        return list_run_assets_response_200

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
