import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_type_enum import AgentTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="IntegrationStatus")


@_attrs_define
class IntegrationStatus:
    """
    Attributes:
        agent_type (Union[Unset, AgentTypeEnum]):
        status (Union[Unset, str]):
        last_request_timestamp (Union[None, Unset, datetime.datetime]):
        service_name (Union[Unset, str]):
    """

    agent_type: Union[Unset, AgentTypeEnum] = UNSET
    status: Union[Unset, str] = UNSET
    last_request_timestamp: Union[None, Unset, datetime.datetime] = UNSET
    service_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agent_type: Union[Unset, str] = UNSET
        if not isinstance(self.agent_type, Unset):
            agent_type = self.agent_type.value

        status = self.status

        last_request_timestamp: Union[None, Unset, str]
        if isinstance(self.last_request_timestamp, Unset):
            last_request_timestamp = UNSET
        elif isinstance(self.last_request_timestamp, datetime.datetime):
            last_request_timestamp = self.last_request_timestamp.isoformat()
        else:
            last_request_timestamp = self.last_request_timestamp

        service_name = self.service_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agent_type is not UNSET:
            field_dict["agent_type"] = agent_type
        if status is not UNSET:
            field_dict["status"] = status
        if last_request_timestamp is not UNSET:
            field_dict["last_request_timestamp"] = last_request_timestamp
        if service_name is not UNSET:
            field_dict["service_name"] = service_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _agent_type = d.pop("agent_type", UNSET)
        agent_type: Union[Unset, AgentTypeEnum]
        if isinstance(_agent_type, Unset):
            agent_type = UNSET
        else:
            agent_type = AgentTypeEnum(_agent_type)

        status = d.pop("status", UNSET)

        def _parse_last_request_timestamp(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_request_timestamp_type_0 = isoparse(data)

                return last_request_timestamp_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_request_timestamp = _parse_last_request_timestamp(d.pop("last_request_timestamp", UNSET))

        service_name = d.pop("service_name", UNSET)

        integration_status = cls(
            agent_type=agent_type,
            status=status,
            last_request_timestamp=last_request_timestamp,
            service_name=service_name,
        )

        integration_status.additional_properties = d
        return integration_status

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
