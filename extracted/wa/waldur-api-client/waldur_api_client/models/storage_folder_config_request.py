from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.default_permission_enum import DefaultPermissionEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.storage_data_type_request import StorageDataTypeRequest


T = TypeVar("T", bound="StorageFolderConfigRequest")


@_attrs_define
class StorageFolderConfigRequest:
    """
    Attributes:
        component_type (str):
        storage_data_types (list['StorageDataTypeRequest']):
        default_hard_quota_multiplier (Union[Unset, float]):  Default: 1.0.
        inode_soft_multiplier (Union[Unset, int]):  Default: 7000.
        inode_hard_multiplier (Union[Unset, int]):  Default: 10000.
        default_permission (Union[Unset, DefaultPermissionEnum]):  Default: DefaultPermissionEnum.VALUE_0.
    """

    component_type: str
    storage_data_types: list["StorageDataTypeRequest"]
    default_hard_quota_multiplier: Union[Unset, float] = 1.0
    inode_soft_multiplier: Union[Unset, int] = 7000
    inode_hard_multiplier: Union[Unset, int] = 10000
    default_permission: Union[Unset, DefaultPermissionEnum] = DefaultPermissionEnum.VALUE_0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        component_type = self.component_type

        storage_data_types = []
        for storage_data_types_item_data in self.storage_data_types:
            storage_data_types_item = storage_data_types_item_data.to_dict()
            storage_data_types.append(storage_data_types_item)

        default_hard_quota_multiplier = self.default_hard_quota_multiplier

        inode_soft_multiplier = self.inode_soft_multiplier

        inode_hard_multiplier = self.inode_hard_multiplier

        default_permission: Union[Unset, str] = UNSET
        if not isinstance(self.default_permission, Unset):
            default_permission = self.default_permission.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "component_type": component_type,
                "storage_data_types": storage_data_types,
            }
        )
        if default_hard_quota_multiplier is not UNSET:
            field_dict["default_hard_quota_multiplier"] = default_hard_quota_multiplier
        if inode_soft_multiplier is not UNSET:
            field_dict["inode_soft_multiplier"] = inode_soft_multiplier
        if inode_hard_multiplier is not UNSET:
            field_dict["inode_hard_multiplier"] = inode_hard_multiplier
        if default_permission is not UNSET:
            field_dict["default_permission"] = default_permission

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.storage_data_type_request import StorageDataTypeRequest

        d = dict(src_dict)
        component_type = d.pop("component_type")

        storage_data_types = []
        _storage_data_types = d.pop("storage_data_types")
        for storage_data_types_item_data in _storage_data_types:
            storage_data_types_item = StorageDataTypeRequest.from_dict(storage_data_types_item_data)

            storage_data_types.append(storage_data_types_item)

        default_hard_quota_multiplier = d.pop("default_hard_quota_multiplier", UNSET)

        inode_soft_multiplier = d.pop("inode_soft_multiplier", UNSET)

        inode_hard_multiplier = d.pop("inode_hard_multiplier", UNSET)

        _default_permission = d.pop("default_permission", UNSET)
        default_permission: Union[Unset, DefaultPermissionEnum]
        if isinstance(_default_permission, Unset):
            default_permission = UNSET
        else:
            default_permission = DefaultPermissionEnum(_default_permission)

        storage_folder_config_request = cls(
            component_type=component_type,
            storage_data_types=storage_data_types,
            default_hard_quota_multiplier=default_hard_quota_multiplier,
            inode_soft_multiplier=inode_soft_multiplier,
            inode_hard_multiplier=inode_hard_multiplier,
            default_permission=default_permission,
        )

        storage_folder_config_request.additional_properties = d
        return storage_folder_config_request

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
