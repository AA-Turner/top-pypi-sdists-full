import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.export_type_enum import ExportTypeEnum
from ..models.matrix_history_export_state_enum import MatrixHistoryExportStateEnum

T = TypeVar("T", bound="MatrixHistoryExport")


@_attrs_define
class MatrixHistoryExport:
    """
    Attributes:
        uuid (UUID):
        url (str):
        room_uuid (UUID):
        room_name (str):
        export_type (ExportTypeEnum):
        message_count (int):
        media_count (int):
        state (MatrixHistoryExportStateEnum):
        error_message (str):
        export_file_url (Union[None, str]):
        media_file_url (Union[None, str]):
        started_at (Union[None, datetime.datetime]):
        completed_at (Union[None, datetime.datetime]):
        created (datetime.datetime):
    """

    uuid: UUID
    url: str
    room_uuid: UUID
    room_name: str
    export_type: ExportTypeEnum
    message_count: int
    media_count: int
    state: MatrixHistoryExportStateEnum
    error_message: str
    export_file_url: Union[None, str]
    media_file_url: Union[None, str]
    started_at: Union[None, datetime.datetime]
    completed_at: Union[None, datetime.datetime]
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        room_uuid = str(self.room_uuid)

        room_name = self.room_name

        export_type = self.export_type.value

        message_count = self.message_count

        media_count = self.media_count

        state = self.state.value

        error_message = self.error_message

        export_file_url: Union[None, str]
        export_file_url = self.export_file_url

        media_file_url: Union[None, str]
        media_file_url = self.media_file_url

        started_at: Union[None, str]
        if isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        completed_at: Union[None, str]
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "room_uuid": room_uuid,
                "room_name": room_name,
                "export_type": export_type,
                "message_count": message_count,
                "media_count": media_count,
                "state": state,
                "error_message": error_message,
                "export_file_url": export_file_url,
                "media_file_url": media_file_url,
                "started_at": started_at,
                "completed_at": completed_at,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        room_uuid = UUID(d.pop("room_uuid"))

        room_name = d.pop("room_name")

        export_type = ExportTypeEnum(d.pop("export_type"))

        message_count = d.pop("message_count")

        media_count = d.pop("media_count")

        state = MatrixHistoryExportStateEnum(d.pop("state"))

        error_message = d.pop("error_message")

        def _parse_export_file_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        export_file_url = _parse_export_file_url(d.pop("export_file_url"))

        def _parse_media_file_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        media_file_url = _parse_media_file_url(d.pop("media_file_url"))

        def _parse_started_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = isoparse(data)

                return started_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        started_at = _parse_started_at(d.pop("started_at"))

        def _parse_completed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)

                return completed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        completed_at = _parse_completed_at(d.pop("completed_at"))

        created = isoparse(d.pop("created"))

        matrix_history_export = cls(
            uuid=uuid,
            url=url,
            room_uuid=room_uuid,
            room_name=room_name,
            export_type=export_type,
            message_count=message_count,
            media_count=media_count,
            state=state,
            error_message=error_message,
            export_file_url=export_file_url,
            media_file_url=media_file_url,
            started_at=started_at,
            completed_at=completed_at,
            created=created,
        )

        matrix_history_export.additional_properties = d
        return matrix_history_export

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
