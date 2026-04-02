import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mapping import Mapping


T = TypeVar("T", bound="MigrationDetails")


@_attrs_define
class MigrationDetails:
    """
    Attributes:
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        mappings (Mapping):
        created_by_uuid (UUID):
        created_by_full_name (str):
        src_offering_uuid (UUID):
        src_offering_name (str):
        dst_offering_uuid (UUID):
        dst_offering_name (str):
        src_resource_uuid (UUID):
        src_resource_name (str):
        dst_resource_uuid (UUID):
        dst_resource_name (str):
        dst_resource_state (str):
        state (str):
        error_message (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
    """

    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    mappings: "Mapping"
    created_by_uuid: UUID
    created_by_full_name: str
    src_offering_uuid: UUID
    src_offering_name: str
    dst_offering_uuid: UUID
    dst_offering_name: str
    src_resource_uuid: UUID
    src_resource_name: str
    dst_resource_uuid: UUID
    dst_resource_name: str
    dst_resource_state: str
    state: str
    error_message: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        mappings = self.mappings.to_dict()

        created_by_uuid = str(self.created_by_uuid)

        created_by_full_name = self.created_by_full_name

        src_offering_uuid = str(self.src_offering_uuid)

        src_offering_name = self.src_offering_name

        dst_offering_uuid = str(self.dst_offering_uuid)

        dst_offering_name = self.dst_offering_name

        src_resource_uuid = str(self.src_resource_uuid)

        src_resource_name = self.src_resource_name

        dst_resource_uuid = str(self.dst_resource_uuid)

        dst_resource_name = self.dst_resource_name

        dst_resource_state = self.dst_resource_state

        state = self.state

        error_message = self.error_message

        error_traceback = self.error_traceback

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "mappings": mappings,
                "created_by_uuid": created_by_uuid,
                "created_by_full_name": created_by_full_name,
                "src_offering_uuid": src_offering_uuid,
                "src_offering_name": src_offering_name,
                "dst_offering_uuid": dst_offering_uuid,
                "dst_offering_name": dst_offering_name,
                "src_resource_uuid": src_resource_uuid,
                "src_resource_name": src_resource_name,
                "dst_resource_uuid": dst_resource_uuid,
                "dst_resource_name": dst_resource_name,
                "dst_resource_state": dst_resource_state,
                "state": state,
            }
        )
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mapping import Mapping

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        mappings = Mapping.from_dict(d.pop("mappings"))

        created_by_uuid = UUID(d.pop("created_by_uuid"))

        created_by_full_name = d.pop("created_by_full_name")

        src_offering_uuid = UUID(d.pop("src_offering_uuid"))

        src_offering_name = d.pop("src_offering_name")

        dst_offering_uuid = UUID(d.pop("dst_offering_uuid"))

        dst_offering_name = d.pop("dst_offering_name")

        src_resource_uuid = UUID(d.pop("src_resource_uuid"))

        src_resource_name = d.pop("src_resource_name")

        dst_resource_uuid = UUID(d.pop("dst_resource_uuid"))

        dst_resource_name = d.pop("dst_resource_name")

        dst_resource_state = d.pop("dst_resource_state")

        state = d.pop("state")

        error_message = d.pop("error_message", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        migration_details = cls(
            uuid=uuid,
            created=created,
            modified=modified,
            mappings=mappings,
            created_by_uuid=created_by_uuid,
            created_by_full_name=created_by_full_name,
            src_offering_uuid=src_offering_uuid,
            src_offering_name=src_offering_name,
            dst_offering_uuid=dst_offering_uuid,
            dst_offering_name=dst_offering_name,
            src_resource_uuid=src_resource_uuid,
            src_resource_name=src_resource_name,
            dst_resource_uuid=dst_resource_uuid,
            dst_resource_name=dst_resource_name,
            dst_resource_state=dst_resource_state,
            state=state,
            error_message=error_message,
            error_traceback=error_traceback,
        )

        migration_details.additional_properties = d
        return migration_details

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
