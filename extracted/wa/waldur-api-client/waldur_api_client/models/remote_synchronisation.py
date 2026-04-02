import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_remote_local_category import NestedRemoteLocalCategory


T = TypeVar("T", bound="RemoteSynchronisation")


@_attrs_define
class RemoteSynchronisation:
    """
    Attributes:
        uuid (UUID):
        url (str):
        api_url (str):
        token (str):
        remote_organization_uuid (UUID):
        remote_organization_name (str):
        local_service_provider (str):
        local_service_provider_name (str):
        last_execution (Union[None, datetime.datetime]):
        last_output (str):
        get_state_display (str):
        error_message (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        remotelocalcategory_set (list['NestedRemoteLocalCategory']):
        is_active (Union[Unset, bool]):
    """

    uuid: UUID
    url: str
    api_url: str
    token: str
    remote_organization_uuid: UUID
    remote_organization_name: str
    local_service_provider: str
    local_service_provider_name: str
    last_execution: Union[None, datetime.datetime]
    last_output: str
    get_state_display: str
    error_message: str
    created: datetime.datetime
    modified: datetime.datetime
    remotelocalcategory_set: list["NestedRemoteLocalCategory"]
    is_active: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        api_url = self.api_url

        token = self.token

        remote_organization_uuid = str(self.remote_organization_uuid)

        remote_organization_name = self.remote_organization_name

        local_service_provider = self.local_service_provider

        local_service_provider_name = self.local_service_provider_name

        last_execution: Union[None, str]
        if isinstance(self.last_execution, datetime.datetime):
            last_execution = self.last_execution.isoformat()
        else:
            last_execution = self.last_execution

        last_output = self.last_output

        get_state_display = self.get_state_display

        error_message = self.error_message

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        remotelocalcategory_set = []
        for remotelocalcategory_set_item_data in self.remotelocalcategory_set:
            remotelocalcategory_set_item = remotelocalcategory_set_item_data.to_dict()
            remotelocalcategory_set.append(remotelocalcategory_set_item)

        is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "api_url": api_url,
                "token": token,
                "remote_organization_uuid": remote_organization_uuid,
                "remote_organization_name": remote_organization_name,
                "local_service_provider": local_service_provider,
                "local_service_provider_name": local_service_provider_name,
                "last_execution": last_execution,
                "last_output": last_output,
                "get_state_display": get_state_display,
                "error_message": error_message,
                "created": created,
                "modified": modified,
                "remotelocalcategory_set": remotelocalcategory_set,
            }
        )
        if is_active is not UNSET:
            field_dict["is_active"] = is_active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_remote_local_category import NestedRemoteLocalCategory

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        api_url = d.pop("api_url")

        token = d.pop("token")

        remote_organization_uuid = UUID(d.pop("remote_organization_uuid"))

        remote_organization_name = d.pop("remote_organization_name")

        local_service_provider = d.pop("local_service_provider")

        local_service_provider_name = d.pop("local_service_provider_name")

        def _parse_last_execution(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_execution_type_0 = isoparse(data)

                return last_execution_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_execution = _parse_last_execution(d.pop("last_execution"))

        last_output = d.pop("last_output")

        get_state_display = d.pop("get_state_display")

        error_message = d.pop("error_message")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        remotelocalcategory_set = []
        _remotelocalcategory_set = d.pop("remotelocalcategory_set")
        for remotelocalcategory_set_item_data in _remotelocalcategory_set:
            remotelocalcategory_set_item = NestedRemoteLocalCategory.from_dict(remotelocalcategory_set_item_data)

            remotelocalcategory_set.append(remotelocalcategory_set_item)

        is_active = d.pop("is_active", UNSET)

        remote_synchronisation = cls(
            uuid=uuid,
            url=url,
            api_url=api_url,
            token=token,
            remote_organization_uuid=remote_organization_uuid,
            remote_organization_name=remote_organization_name,
            local_service_provider=local_service_provider,
            local_service_provider_name=local_service_provider_name,
            last_execution=last_execution,
            last_output=last_output,
            get_state_display=get_state_display,
            error_message=error_message,
            created=created,
            modified=modified,
            remotelocalcategory_set=remotelocalcategory_set,
            is_active=is_active,
        )

        remote_synchronisation.additional_properties = d
        return remote_synchronisation

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
