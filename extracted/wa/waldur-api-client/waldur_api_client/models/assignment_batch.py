import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.assignment_batch_status import AssignmentBatchStatus
from ..models.assignment_source import AssignmentSource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.assignment_item import AssignmentItem


T = TypeVar("T", bound="AssignmentBatch")


@_attrs_define
class AssignmentBatch:
    """
    Attributes:
        url (str):
        uuid (UUID):
        call (str):
        call_uuid (UUID):
        call_name (str):
        reviewer_pool_entry (str):
        reviewer_pool_entry_uuid (UUID):
        reviewer_name (Union[None, str]): Get reviewer name from pool entry.
        reviewer_email (Union[None, str]): Get reviewer email from pool entry.
        reviewer_uuid (Union[None, str]): Get reviewer profile UUID if available.
        status (AssignmentBatchStatus):
        status_display (str):
        sent_at (Union[None, datetime.datetime]): When the invitation was sent to the reviewer.
        expires_at (Union[None, datetime.datetime]): When the invitation expires.
        responded_at (Union[None, datetime.datetime]): When the reviewer completed their response.
        source (AssignmentSource):
        source_display (str):
        created_by (Union[None, str]): User who created/approved this batch.
        created_by_name (str):
        items (list['AssignmentItem']):
        items_count (int): Total count of items in batch.
        items_pending_count (int): Count of pending items.
        items_accepted_count (int): Count of accepted items.
        items_declined_count (int): Count of declined items.
        is_expired (bool):
        created (datetime.datetime):
        manager_notes (Union[Unset, str]): Optional notes from call manager to reviewer.
    """

    url: str
    uuid: UUID
    call: str
    call_uuid: UUID
    call_name: str
    reviewer_pool_entry: str
    reviewer_pool_entry_uuid: UUID
    reviewer_name: Union[None, str]
    reviewer_email: Union[None, str]
    reviewer_uuid: Union[None, str]
    status: AssignmentBatchStatus
    status_display: str
    sent_at: Union[None, datetime.datetime]
    expires_at: Union[None, datetime.datetime]
    responded_at: Union[None, datetime.datetime]
    source: AssignmentSource
    source_display: str
    created_by: Union[None, str]
    created_by_name: str
    items: list["AssignmentItem"]
    items_count: int
    items_pending_count: int
    items_accepted_count: int
    items_declined_count: int
    is_expired: bool
    created: datetime.datetime
    manager_notes: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        call = self.call

        call_uuid = str(self.call_uuid)

        call_name = self.call_name

        reviewer_pool_entry = self.reviewer_pool_entry

        reviewer_pool_entry_uuid = str(self.reviewer_pool_entry_uuid)

        reviewer_name: Union[None, str]
        reviewer_name = self.reviewer_name

        reviewer_email: Union[None, str]
        reviewer_email = self.reviewer_email

        reviewer_uuid: Union[None, str]
        reviewer_uuid = self.reviewer_uuid

        status = self.status.value

        status_display = self.status_display

        sent_at: Union[None, str]
        if isinstance(self.sent_at, datetime.datetime):
            sent_at = self.sent_at.isoformat()
        else:
            sent_at = self.sent_at

        expires_at: Union[None, str]
        if isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        responded_at: Union[None, str]
        if isinstance(self.responded_at, datetime.datetime):
            responded_at = self.responded_at.isoformat()
        else:
            responded_at = self.responded_at

        source = self.source.value

        source_display = self.source_display

        created_by: Union[None, str]
        created_by = self.created_by

        created_by_name = self.created_by_name

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        items_count = self.items_count

        items_pending_count = self.items_pending_count

        items_accepted_count = self.items_accepted_count

        items_declined_count = self.items_declined_count

        is_expired = self.is_expired

        created = self.created.isoformat()

        manager_notes = self.manager_notes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "call": call,
                "call_uuid": call_uuid,
                "call_name": call_name,
                "reviewer_pool_entry": reviewer_pool_entry,
                "reviewer_pool_entry_uuid": reviewer_pool_entry_uuid,
                "reviewer_name": reviewer_name,
                "reviewer_email": reviewer_email,
                "reviewer_uuid": reviewer_uuid,
                "status": status,
                "status_display": status_display,
                "sent_at": sent_at,
                "expires_at": expires_at,
                "responded_at": responded_at,
                "source": source,
                "source_display": source_display,
                "created_by": created_by,
                "created_by_name": created_by_name,
                "items": items,
                "items_count": items_count,
                "items_pending_count": items_pending_count,
                "items_accepted_count": items_accepted_count,
                "items_declined_count": items_declined_count,
                "is_expired": is_expired,
                "created": created,
            }
        )
        if manager_notes is not UNSET:
            field_dict["manager_notes"] = manager_notes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.assignment_item import AssignmentItem

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        call = d.pop("call")

        call_uuid = UUID(d.pop("call_uuid"))

        call_name = d.pop("call_name")

        reviewer_pool_entry = d.pop("reviewer_pool_entry")

        reviewer_pool_entry_uuid = UUID(d.pop("reviewer_pool_entry_uuid"))

        def _parse_reviewer_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reviewer_name = _parse_reviewer_name(d.pop("reviewer_name"))

        def _parse_reviewer_email(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reviewer_email = _parse_reviewer_email(d.pop("reviewer_email"))

        def _parse_reviewer_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reviewer_uuid = _parse_reviewer_uuid(d.pop("reviewer_uuid"))

        status = AssignmentBatchStatus(d.pop("status"))

        status_display = d.pop("status_display")

        def _parse_sent_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                sent_at_type_0 = isoparse(data)

                return sent_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        sent_at = _parse_sent_at(d.pop("sent_at"))

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

        def _parse_responded_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                responded_at_type_0 = isoparse(data)

                return responded_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        responded_at = _parse_responded_at(d.pop("responded_at"))

        source = AssignmentSource(d.pop("source"))

        source_display = d.pop("source_display")

        def _parse_created_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        created_by = _parse_created_by(d.pop("created_by"))

        created_by_name = d.pop("created_by_name")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = AssignmentItem.from_dict(items_item_data)

            items.append(items_item)

        items_count = d.pop("items_count")

        items_pending_count = d.pop("items_pending_count")

        items_accepted_count = d.pop("items_accepted_count")

        items_declined_count = d.pop("items_declined_count")

        is_expired = d.pop("is_expired")

        created = isoparse(d.pop("created"))

        manager_notes = d.pop("manager_notes", UNSET)

        assignment_batch = cls(
            url=url,
            uuid=uuid,
            call=call,
            call_uuid=call_uuid,
            call_name=call_name,
            reviewer_pool_entry=reviewer_pool_entry,
            reviewer_pool_entry_uuid=reviewer_pool_entry_uuid,
            reviewer_name=reviewer_name,
            reviewer_email=reviewer_email,
            reviewer_uuid=reviewer_uuid,
            status=status,
            status_display=status_display,
            sent_at=sent_at,
            expires_at=expires_at,
            responded_at=responded_at,
            source=source,
            source_display=source_display,
            created_by=created_by,
            created_by_name=created_by_name,
            items=items,
            items_count=items_count,
            items_pending_count=items_pending_count,
            items_accepted_count=items_accepted_count,
            items_declined_count=items_declined_count,
            is_expired=is_expired,
            created=created,
            manager_notes=manager_notes,
        )

        assignment_batch.additional_properties = d
        return assignment_batch

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
