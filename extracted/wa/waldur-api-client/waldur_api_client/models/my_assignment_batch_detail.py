import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.my_assignment_item import MyAssignmentItem


T = TypeVar("T", bound="MyAssignmentBatchDetail")


@_attrs_define
class MyAssignmentBatchDetail:
    """
    Attributes:
        uuid (UUID):
        call_uuid (UUID):
        call_name (str):
        status (str):
        status_display (str):
        sent_at (datetime.datetime):
        expires_at (Union[None, datetime.datetime]):
        is_expired (bool):
        items_count (int):
        items_pending_count (int):
        manager_notes (str):
        items (list['MyAssignmentItem']):
    """

    uuid: UUID
    call_uuid: UUID
    call_name: str
    status: str
    status_display: str
    sent_at: datetime.datetime
    expires_at: Union[None, datetime.datetime]
    is_expired: bool
    items_count: int
    items_pending_count: int
    manager_notes: str
    items: list["MyAssignmentItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        call_uuid = str(self.call_uuid)

        call_name = self.call_name

        status = self.status

        status_display = self.status_display

        sent_at = self.sent_at.isoformat()

        expires_at: Union[None, str]
        if isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        is_expired = self.is_expired

        items_count = self.items_count

        items_pending_count = self.items_pending_count

        manager_notes = self.manager_notes

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "call_uuid": call_uuid,
                "call_name": call_name,
                "status": status,
                "status_display": status_display,
                "sent_at": sent_at,
                "expires_at": expires_at,
                "is_expired": is_expired,
                "items_count": items_count,
                "items_pending_count": items_pending_count,
                "manager_notes": manager_notes,
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.my_assignment_item import MyAssignmentItem

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        call_uuid = UUID(d.pop("call_uuid"))

        call_name = d.pop("call_name")

        status = d.pop("status")

        status_display = d.pop("status_display")

        sent_at = isoparse(d.pop("sent_at"))

        def _parse_expires_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        expires_at = _parse_expires_at(d.pop("expires_at"))

        is_expired = d.pop("is_expired")

        items_count = d.pop("items_count")

        items_pending_count = d.pop("items_pending_count")

        manager_notes = d.pop("manager_notes")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = MyAssignmentItem.from_dict(items_item_data)

            items.append(items_item)

        my_assignment_batch_detail = cls(
            uuid=uuid,
            call_uuid=call_uuid,
            call_name=call_name,
            status=status,
            status_display=status_display,
            sent_at=sent_at,
            expires_at=expires_at,
            is_expired=is_expired,
            items_count=items_count,
            items_pending_count=items_pending_count,
            manager_notes=manager_notes,
            items=items,
        )

        my_assignment_batch_detail.additional_properties = d
        return my_assignment_batch_detail

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
