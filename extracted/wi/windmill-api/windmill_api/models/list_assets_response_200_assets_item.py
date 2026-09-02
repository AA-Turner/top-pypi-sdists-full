from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_assets_response_200_assets_item_kind import ListAssetsResponse200AssetsItemKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_assets_response_200_assets_item_metadata import ListAssetsResponse200AssetsItemMetadata
    from ..models.list_assets_response_200_assets_item_usages_item import ListAssetsResponse200AssetsItemUsagesItem


T = TypeVar("T", bound="ListAssetsResponse200AssetsItem")


@_attrs_define
class ListAssetsResponse200AssetsItem:
    """
    Attributes:
        path (str):
        kind (ListAssetsResponse200AssetsItemKind):
        usages (List['ListAssetsResponse200AssetsItemUsagesItem']):
        metadata (Union[Unset, ListAssetsResponse200AssetsItemMetadata]):
    """

    path: str
    kind: ListAssetsResponse200AssetsItemKind
    usages: List["ListAssetsResponse200AssetsItemUsagesItem"]
    metadata: Union[Unset, "ListAssetsResponse200AssetsItemMetadata"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        kind = self.kind.value

        usages = []
        for usages_item_data in self.usages:
            usages_item = usages_item_data.to_dict()

            usages.append(usages_item)

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "kind": kind,
                "usages": usages,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_assets_response_200_assets_item_metadata import ListAssetsResponse200AssetsItemMetadata
        from ..models.list_assets_response_200_assets_item_usages_item import ListAssetsResponse200AssetsItemUsagesItem

        d = src_dict.copy()
        path = d.pop("path")

        kind = ListAssetsResponse200AssetsItemKind(d.pop("kind"))

        usages = []
        _usages = d.pop("usages")
        for usages_item_data in _usages:
            usages_item = ListAssetsResponse200AssetsItemUsagesItem.from_dict(usages_item_data)

            usages.append(usages_item)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, ListAssetsResponse200AssetsItemMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ListAssetsResponse200AssetsItemMetadata.from_dict(_metadata)

        list_assets_response_200_assets_item = cls(
            path=path,
            kind=kind,
            usages=usages,
            metadata=metadata,
        )

        list_assets_response_200_assets_item.additional_properties = d
        return list_assets_response_200_assets_item

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
