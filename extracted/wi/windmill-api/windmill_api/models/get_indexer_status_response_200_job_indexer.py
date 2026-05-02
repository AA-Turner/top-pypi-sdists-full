import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_indexer_status_response_200_job_indexer_storage import (
        GetIndexerStatusResponse200JobIndexerStorage,
    )


T = TypeVar("T", bound="GetIndexerStatusResponse200JobIndexer")


@_attrs_define
class GetIndexerStatusResponse200JobIndexer:
    """
    Attributes:
        is_alive (Union[Unset, bool]):
        last_locked_at (Union[Unset, None, datetime.datetime]):
        owner (Union[Unset, None, str]):
        storage (Union[Unset, GetIndexerStatusResponse200JobIndexerStorage]):
    """

    is_alive: Union[Unset, bool] = UNSET
    last_locked_at: Union[Unset, None, datetime.datetime] = UNSET
    owner: Union[Unset, None, str] = UNSET
    storage: Union[Unset, "GetIndexerStatusResponse200JobIndexerStorage"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_alive = self.is_alive
        last_locked_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_locked_at, Unset):
            last_locked_at = self.last_locked_at.isoformat() if self.last_locked_at else None

        owner = self.owner
        storage: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.storage, Unset):
            storage = self.storage.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_alive is not UNSET:
            field_dict["is_alive"] = is_alive
        if last_locked_at is not UNSET:
            field_dict["last_locked_at"] = last_locked_at
        if owner is not UNSET:
            field_dict["owner"] = owner
        if storage is not UNSET:
            field_dict["storage"] = storage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_indexer_status_response_200_job_indexer_storage import (
            GetIndexerStatusResponse200JobIndexerStorage,
        )

        d = src_dict.copy()
        is_alive = d.pop("is_alive", UNSET)

        _last_locked_at = d.pop("last_locked_at", UNSET)
        last_locked_at: Union[Unset, None, datetime.datetime]
        if _last_locked_at is None:
            last_locked_at = None
        elif isinstance(_last_locked_at, Unset):
            last_locked_at = UNSET
        else:
            last_locked_at = isoparse(_last_locked_at)

        owner = d.pop("owner", UNSET)

        _storage = d.pop("storage", UNSET)
        storage: Union[Unset, GetIndexerStatusResponse200JobIndexerStorage]
        if isinstance(_storage, Unset):
            storage = UNSET
        else:
            storage = GetIndexerStatusResponse200JobIndexerStorage.from_dict(_storage)

        get_indexer_status_response_200_job_indexer = cls(
            is_alive=is_alive,
            last_locked_at=last_locked_at,
            owner=owner,
            storage=storage,
        )

        get_indexer_status_response_200_job_indexer.additional_properties = d
        return get_indexer_status_response_200_job_indexer

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
