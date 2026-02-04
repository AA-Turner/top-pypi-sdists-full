import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_assets_response_200_assets_item_usages_item_access_type import (
    ListAssetsResponse200AssetsItemUsagesItemAccessType,
)
from ..models.list_assets_response_200_assets_item_usages_item_kind import ListAssetsResponse200AssetsItemUsagesItemKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_assets_response_200_assets_item_usages_item_metadata import (
        ListAssetsResponse200AssetsItemUsagesItemMetadata,
    )


T = TypeVar("T", bound="ListAssetsResponse200AssetsItemUsagesItem")


@_attrs_define
class ListAssetsResponse200AssetsItemUsagesItem:
    """
    Attributes:
        path (str):
        kind (ListAssetsResponse200AssetsItemUsagesItemKind):
        access_type (Union[Unset, ListAssetsResponse200AssetsItemUsagesItemAccessType]):
        created_at (Union[Unset, datetime.datetime]): When the asset was detected
        metadata (Union[Unset, ListAssetsResponse200AssetsItemUsagesItemMetadata]):
    """

    path: str
    kind: ListAssetsResponse200AssetsItemUsagesItemKind
    access_type: Union[Unset, ListAssetsResponse200AssetsItemUsagesItemAccessType] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    metadata: Union[Unset, "ListAssetsResponse200AssetsItemUsagesItemMetadata"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        kind = self.kind.value

        access_type: Union[Unset, str] = UNSET
        if not isinstance(self.access_type, Unset):
            access_type = self.access_type.value

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

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
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_assets_response_200_assets_item_usages_item_metadata import (
            ListAssetsResponse200AssetsItemUsagesItemMetadata,
        )

        d = src_dict.copy()
        path = d.pop("path")

        kind = ListAssetsResponse200AssetsItemUsagesItemKind(d.pop("kind"))

        _access_type = d.pop("access_type", UNSET)
        access_type: Union[Unset, ListAssetsResponse200AssetsItemUsagesItemAccessType]
        if isinstance(_access_type, Unset):
            access_type = UNSET
        else:
            access_type = ListAssetsResponse200AssetsItemUsagesItemAccessType(_access_type)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, ListAssetsResponse200AssetsItemUsagesItemMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ListAssetsResponse200AssetsItemUsagesItemMetadata.from_dict(_metadata)

        list_assets_response_200_assets_item_usages_item = cls(
            path=path,
            kind=kind,
            access_type=access_type,
            created_at=created_at,
            metadata=metadata,
        )

        list_assets_response_200_assets_item_usages_item.additional_properties = d
        return list_assets_response_200_assets_item_usages_item

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
