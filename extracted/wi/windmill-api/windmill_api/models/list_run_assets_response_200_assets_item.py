from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_run_assets_response_200_assets_item_access_type import ListRunAssetsResponse200AssetsItemAccessType
from ..models.list_run_assets_response_200_assets_item_kind import ListRunAssetsResponse200AssetsItemKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListRunAssetsResponse200AssetsItem")


@_attrs_define
class ListRunAssetsResponse200AssetsItem:
    """
    Attributes:
        path (str):
        kind (ListRunAssetsResponse200AssetsItemKind):
        access_type (Union[Unset, None, ListRunAssetsResponse200AssetsItemAccessType]):
    """

    path: str
    kind: ListRunAssetsResponse200AssetsItemKind
    access_type: Union[Unset, None, ListRunAssetsResponse200AssetsItemAccessType] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        kind = self.kind.value

        access_type: Union[Unset, None, str] = UNSET
        if not isinstance(self.access_type, Unset):
            access_type = self.access_type.value if self.access_type else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "kind": kind,
            }
        )
        if access_type is not UNSET:
            field_dict["access_type"] = access_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        kind = ListRunAssetsResponse200AssetsItemKind(d.pop("kind"))

        _access_type = d.pop("access_type", UNSET)
        access_type: Union[Unset, None, ListRunAssetsResponse200AssetsItemAccessType]
        if _access_type is None:
            access_type = None
        elif isinstance(_access_type, Unset):
            access_type = UNSET
        else:
            access_type = ListRunAssetsResponse200AssetsItemAccessType(_access_type)

        list_run_assets_response_200_assets_item = cls(
            path=path,
            kind=kind,
            access_type=access_type,
        )

        list_run_assets_response_200_assets_item.additional_properties = d
        return list_run_assets_response_200_assets_item

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
