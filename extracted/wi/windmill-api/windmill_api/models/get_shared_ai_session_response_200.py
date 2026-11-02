import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.get_shared_ai_session_response_200_snapshot import GetSharedAiSessionResponse200Snapshot


T = TypeVar("T", bound="GetSharedAiSessionResponse200")


@_attrs_define
class GetSharedAiSessionResponse200:
    """
    Attributes:
        id (str):
        name (str):
        is_public (bool):
        message_count (int):
        created_by (str):
        shared_at (datetime.datetime):
        snapshot (GetSharedAiSessionResponse200Snapshot):
        can_unshare (bool): whether the caller authored the share or is a workspace admin
    """

    id: str
    name: str
    is_public: bool
    message_count: int
    created_by: str
    shared_at: datetime.datetime
    snapshot: "GetSharedAiSessionResponse200Snapshot"
    can_unshare: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        is_public = self.is_public
        message_count = self.message_count
        created_by = self.created_by
        shared_at = self.shared_at.isoformat()

        snapshot = self.snapshot.to_dict()

        can_unshare = self.can_unshare

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "is_public": is_public,
                "message_count": message_count,
                "created_by": created_by,
                "shared_at": shared_at,
                "snapshot": snapshot,
                "can_unshare": can_unshare,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_shared_ai_session_response_200_snapshot import GetSharedAiSessionResponse200Snapshot

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        is_public = d.pop("is_public")

        message_count = d.pop("message_count")

        created_by = d.pop("created_by")

        shared_at = isoparse(d.pop("shared_at"))

        snapshot = GetSharedAiSessionResponse200Snapshot.from_dict(d.pop("snapshot"))

        can_unshare = d.pop("can_unshare")

        get_shared_ai_session_response_200 = cls(
            id=id,
            name=name,
            is_public=is_public,
            message_count=message_count,
            created_by=created_by,
            shared_at=shared_at,
            snapshot=snapshot,
            can_unshare=can_unshare,
        )

        get_shared_ai_session_response_200.additional_properties = d
        return get_shared_ai_session_response_200

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
