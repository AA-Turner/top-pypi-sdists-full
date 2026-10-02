import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.remote_project_audit_entry_event_type_enum import RemoteProjectAuditEntryEventTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.award_details import AwardDetails
    from ..models.remote_project_audit_entry_remote_response_type_0 import RemoteProjectAuditEntryRemoteResponseType0


T = TypeVar("T", bound="RemoteProjectAuditEntry")


@_attrs_define
class RemoteProjectAuditEntry:
    """
    Attributes:
        id (int):
        timestamp (datetime.datetime):
        event_type (RemoteProjectAuditEntryEventTypeEnum):
        previous_details (Union['AwardDetails', None]):
        new_details (Union['AwardDetails', None]):
        performed_by_full_name (str):
        performed_by_uuid (UUID):
        remote_project_uuid (UUID):
        remote_project_url (str):
        remote_response (Union['RemoteProjectAuditEntryRemoteResponseType0', None, Unset]): Raw response received from
            the remote portal, if applicable.
        note (Union[Unset, str]): Optional free-text comment about this event.
    """

    id: int
    timestamp: datetime.datetime
    event_type: RemoteProjectAuditEntryEventTypeEnum
    previous_details: Union["AwardDetails", None]
    new_details: Union["AwardDetails", None]
    performed_by_full_name: str
    performed_by_uuid: UUID
    remote_project_uuid: UUID
    remote_project_url: str
    remote_response: Union["RemoteProjectAuditEntryRemoteResponseType0", None, Unset] = UNSET
    note: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.award_details import AwardDetails
        from ..models.remote_project_audit_entry_remote_response_type_0 import (
            RemoteProjectAuditEntryRemoteResponseType0,
        )

        id = self.id

        timestamp = self.timestamp.isoformat()

        event_type = self.event_type.value

        previous_details: Union[None, dict[str, Any]]
        if isinstance(self.previous_details, AwardDetails):
            previous_details = self.previous_details.to_dict()
        else:
            previous_details = self.previous_details

        new_details: Union[None, dict[str, Any]]
        if isinstance(self.new_details, AwardDetails):
            new_details = self.new_details.to_dict()
        else:
            new_details = self.new_details

        performed_by_full_name = self.performed_by_full_name

        performed_by_uuid = str(self.performed_by_uuid)

        remote_project_uuid = str(self.remote_project_uuid)

        remote_project_url = self.remote_project_url

        remote_response: Union[None, Unset, dict[str, Any]]
        if isinstance(self.remote_response, Unset):
            remote_response = UNSET
        elif isinstance(self.remote_response, RemoteProjectAuditEntryRemoteResponseType0):
            remote_response = self.remote_response.to_dict()
        else:
            remote_response = self.remote_response

        note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "timestamp": timestamp,
                "event_type": event_type,
                "previous_details": previous_details,
                "new_details": new_details,
                "performed_by_full_name": performed_by_full_name,
                "performed_by_uuid": performed_by_uuid,
                "remote_project_uuid": remote_project_uuid,
                "remote_project_url": remote_project_url,
            }
        )
        if remote_response is not UNSET:
            field_dict["remote_response"] = remote_response
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.award_details import AwardDetails
        from ..models.remote_project_audit_entry_remote_response_type_0 import (
            RemoteProjectAuditEntryRemoteResponseType0,
        )

        d = dict(src_dict)
        id = d.pop("id")

        timestamp = isoparse(d.pop("timestamp"))

        event_type = RemoteProjectAuditEntryEventTypeEnum(d.pop("event_type"))

        def _parse_previous_details(data: object) -> Union["AwardDetails", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                previous_details_type_1 = AwardDetails.from_dict(data)

                return previous_details_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AwardDetails", None], data)

        previous_details = _parse_previous_details(d.pop("previous_details"))

        def _parse_new_details(data: object) -> Union["AwardDetails", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                new_details_type_1 = AwardDetails.from_dict(data)

                return new_details_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AwardDetails", None], data)

        new_details = _parse_new_details(d.pop("new_details"))

        performed_by_full_name = d.pop("performed_by_full_name")

        performed_by_uuid = UUID(d.pop("performed_by_uuid"))

        remote_project_uuid = UUID(d.pop("remote_project_uuid"))

        remote_project_url = d.pop("remote_project_url")

        def _parse_remote_response(data: object) -> Union["RemoteProjectAuditEntryRemoteResponseType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                remote_response_type_0 = RemoteProjectAuditEntryRemoteResponseType0.from_dict(data)

                return remote_response_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RemoteProjectAuditEntryRemoteResponseType0", None, Unset], data)

        remote_response = _parse_remote_response(d.pop("remote_response", UNSET))

        note = d.pop("note", UNSET)

        remote_project_audit_entry = cls(
            id=id,
            timestamp=timestamp,
            event_type=event_type,
            previous_details=previous_details,
            new_details=new_details,
            performed_by_full_name=performed_by_full_name,
            performed_by_uuid=performed_by_uuid,
            remote_project_uuid=remote_project_uuid,
            remote_project_url=remote_project_url,
            remote_response=remote_response,
            note=note,
        )

        remote_project_audit_entry.additional_properties = d
        return remote_project_audit_entry

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
