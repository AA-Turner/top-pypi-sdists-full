import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.resource_api_key_state import ResourceApiKeyState
from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceApiKey")


@_attrs_define
class ResourceApiKey:
    """
    Attributes:
        uuid (UUID):
        resource_uuid (UUID):
        resource_backend_id (str):
        modified (datetime.datetime):
        api_key (str):
        client_id (Union[Unset, str]):
        state (Union[Unset, ResourceApiKeyState]):
        error_message (Union[Unset, str]):
    """

    uuid: UUID
    resource_uuid: UUID
    resource_backend_id: str
    modified: datetime.datetime
    api_key: str
    client_id: Union[Unset, str] = UNSET
    state: Union[Unset, ResourceApiKeyState] = UNSET
    error_message: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        resource_uuid = str(self.resource_uuid)

        resource_backend_id = self.resource_backend_id

        modified = self.modified.isoformat()

        api_key = self.api_key

        client_id = self.client_id

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        error_message = self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "resource_uuid": resource_uuid,
                "resource_backend_id": resource_backend_id,
                "modified": modified,
                "api_key": api_key,
            }
        )
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if state is not UNSET:
            field_dict["state"] = state
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        resource_uuid = UUID(d.pop("resource_uuid"))

        resource_backend_id = d.pop("resource_backend_id")

        modified = isoparse(d.pop("modified"))

        api_key = d.pop("api_key")

        client_id = d.pop("client_id", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, ResourceApiKeyState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = ResourceApiKeyState(_state)

        error_message = d.pop("error_message", UNSET)

        resource_api_key = cls(
            uuid=uuid,
            resource_uuid=resource_uuid,
            resource_backend_id=resource_backend_id,
            modified=modified,
            api_key=api_key,
            client_id=client_id,
            state=state,
            error_message=error_message,
        )

        resource_api_key.additional_properties = d
        return resource_api_key

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
