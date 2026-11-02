import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="AISessionBackupListing")


@_attrs_define
class AISessionBackupListing:
    """
    Attributes:
        id (str):
        updated_at (datetime.datetime):
        epoch (int): the session's move count when this copy was pushed; of a session two workspaces list, the copy with
            the higher one is the later
    """

    id: str
    updated_at: datetime.datetime
    epoch: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        updated_at = self.updated_at.isoformat()

        epoch = self.epoch

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "updated_at": updated_at,
                "epoch": epoch,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        updated_at = isoparse(d.pop("updated_at"))

        epoch = d.pop("epoch")

        ai_session_backup_listing = cls(
            id=id,
            updated_at=updated_at,
            epoch=epoch,
        )

        ai_session_backup_listing.additional_properties = d
        return ai_session_backup_listing

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
