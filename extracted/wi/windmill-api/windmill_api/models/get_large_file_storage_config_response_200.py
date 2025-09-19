from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_large_file_storage_config_response_200_type import GetLargeFileStorageConfigResponse200Type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_large_file_storage_config_response_200_advanced_permissions_item import (
        GetLargeFileStorageConfigResponse200AdvancedPermissionsItem,
    )
    from ..models.get_large_file_storage_config_response_200_secondary_storage import (
        GetLargeFileStorageConfigResponse200SecondaryStorage,
    )


T = TypeVar("T", bound="GetLargeFileStorageConfigResponse200")


@_attrs_define
class GetLargeFileStorageConfigResponse200:
    """
    Attributes:
        type (Union[Unset, GetLargeFileStorageConfigResponse200Type]):
        s3_resource_path (Union[Unset, str]):
        azure_blob_resource_path (Union[Unset, str]):
        gcs_resource_path (Union[Unset, str]):
        public_resource (Union[Unset, bool]):
        advanced_permissions (Union[Unset, List['GetLargeFileStorageConfigResponse200AdvancedPermissionsItem']]):
        secondary_storage (Union[Unset, GetLargeFileStorageConfigResponse200SecondaryStorage]):
    """

    type: Union[Unset, GetLargeFileStorageConfigResponse200Type] = UNSET
    s3_resource_path: Union[Unset, str] = UNSET
    azure_blob_resource_path: Union[Unset, str] = UNSET
    gcs_resource_path: Union[Unset, str] = UNSET
    public_resource: Union[Unset, bool] = UNSET
    advanced_permissions: Union[Unset, List["GetLargeFileStorageConfigResponse200AdvancedPermissionsItem"]] = UNSET
    secondary_storage: Union[Unset, "GetLargeFileStorageConfigResponse200SecondaryStorage"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        s3_resource_path = self.s3_resource_path
        azure_blob_resource_path = self.azure_blob_resource_path
        gcs_resource_path = self.gcs_resource_path
        public_resource = self.public_resource
        advanced_permissions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.advanced_permissions, Unset):
            advanced_permissions = []
            for advanced_permissions_item_data in self.advanced_permissions:
                advanced_permissions_item = advanced_permissions_item_data.to_dict()

                advanced_permissions.append(advanced_permissions_item)

        secondary_storage: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.secondary_storage, Unset):
            secondary_storage = self.secondary_storage.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if s3_resource_path is not UNSET:
            field_dict["s3_resource_path"] = s3_resource_path
        if azure_blob_resource_path is not UNSET:
            field_dict["azure_blob_resource_path"] = azure_blob_resource_path
        if gcs_resource_path is not UNSET:
            field_dict["gcs_resource_path"] = gcs_resource_path
        if public_resource is not UNSET:
            field_dict["public_resource"] = public_resource
        if advanced_permissions is not UNSET:
            field_dict["advanced_permissions"] = advanced_permissions
        if secondary_storage is not UNSET:
            field_dict["secondary_storage"] = secondary_storage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_large_file_storage_config_response_200_advanced_permissions_item import (
            GetLargeFileStorageConfigResponse200AdvancedPermissionsItem,
        )
        from ..models.get_large_file_storage_config_response_200_secondary_storage import (
            GetLargeFileStorageConfigResponse200SecondaryStorage,
        )

        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, GetLargeFileStorageConfigResponse200Type]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = GetLargeFileStorageConfigResponse200Type(_type)

        s3_resource_path = d.pop("s3_resource_path", UNSET)

        azure_blob_resource_path = d.pop("azure_blob_resource_path", UNSET)

        gcs_resource_path = d.pop("gcs_resource_path", UNSET)

        public_resource = d.pop("public_resource", UNSET)

        advanced_permissions = []
        _advanced_permissions = d.pop("advanced_permissions", UNSET)
        for advanced_permissions_item_data in _advanced_permissions or []:
            advanced_permissions_item = GetLargeFileStorageConfigResponse200AdvancedPermissionsItem.from_dict(
                advanced_permissions_item_data
            )

            advanced_permissions.append(advanced_permissions_item)

        _secondary_storage = d.pop("secondary_storage", UNSET)
        secondary_storage: Union[Unset, GetLargeFileStorageConfigResponse200SecondaryStorage]
        if isinstance(_secondary_storage, Unset):
            secondary_storage = UNSET
        else:
            secondary_storage = GetLargeFileStorageConfigResponse200SecondaryStorage.from_dict(_secondary_storage)

        get_large_file_storage_config_response_200 = cls(
            type=type,
            s3_resource_path=s3_resource_path,
            azure_blob_resource_path=azure_blob_resource_path,
            gcs_resource_path=gcs_resource_path,
            public_resource=public_resource,
            advanced_permissions=advanced_permissions,
            secondary_storage=secondary_storage,
        )

        get_large_file_storage_config_response_200.additional_properties = d
        return get_large_file_storage_config_response_200

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
