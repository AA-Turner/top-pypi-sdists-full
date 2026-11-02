import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_object_storage_usage_response_200_folders_item import GetObjectStorageUsageResponse200FoldersItem


T = TypeVar("T", bound="GetObjectStorageUsageResponse200")


@_attrs_define
class GetObjectStorageUsageResponse200:
    """
    Attributes:
        running (bool):
        started_at (datetime.datetime):
        scanned_objects (int):
        folders (List['GetObjectStorageUsageResponse200FoldersItem']):
        finished_at (Union[Unset, None, datetime.datetime]):
        current_prefix (Union[Unset, None, str]):
        error (Union[Unset, None, str]):
    """

    running: bool
    started_at: datetime.datetime
    scanned_objects: int
    folders: List["GetObjectStorageUsageResponse200FoldersItem"]
    finished_at: Union[Unset, None, datetime.datetime] = UNSET
    current_prefix: Union[Unset, None, str] = UNSET
    error: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        running = self.running
        started_at = self.started_at.isoformat()

        scanned_objects = self.scanned_objects
        folders = []
        for folders_item_data in self.folders:
            folders_item = folders_item_data.to_dict()

            folders.append(folders_item)

        finished_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.finished_at, Unset):
            finished_at = self.finished_at.isoformat() if self.finished_at else None

        current_prefix = self.current_prefix
        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "running": running,
                "started_at": started_at,
                "scanned_objects": scanned_objects,
                "folders": folders,
            }
        )
        if finished_at is not UNSET:
            field_dict["finished_at"] = finished_at
        if current_prefix is not UNSET:
            field_dict["current_prefix"] = current_prefix
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_object_storage_usage_response_200_folders_item import (
            GetObjectStorageUsageResponse200FoldersItem,
        )

        d = src_dict.copy()
        running = d.pop("running")

        started_at = isoparse(d.pop("started_at"))

        scanned_objects = d.pop("scanned_objects")

        folders = []
        _folders = d.pop("folders")
        for folders_item_data in _folders:
            folders_item = GetObjectStorageUsageResponse200FoldersItem.from_dict(folders_item_data)

            folders.append(folders_item)

        _finished_at = d.pop("finished_at", UNSET)
        finished_at: Union[Unset, None, datetime.datetime]
        if _finished_at is None:
            finished_at = None
        elif isinstance(_finished_at, Unset):
            finished_at = UNSET
        else:
            finished_at = isoparse(_finished_at)

        current_prefix = d.pop("current_prefix", UNSET)

        error = d.pop("error", UNSET)

        get_object_storage_usage_response_200 = cls(
            running=running,
            started_at=started_at,
            scanned_objects=scanned_objects,
            folders=folders,
            finished_at=finished_at,
            current_prefix=current_prefix,
            error=error,
        )

        get_object_storage_usage_response_200.additional_properties = d
        return get_object_storage_usage_response_200

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
