import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_type_enum import AgentTypeEnum

T = TypeVar("T", bound="IntegrationStatusDetails")


@_attrs_define
class IntegrationStatusDetails:
    """
    Attributes:
        agent_type (AgentTypeEnum):
        status (str):
        last_request_timestamp (Union[None, datetime.datetime]):
        offering (str):
        url (str):
    """

    agent_type: AgentTypeEnum
    status: str
    last_request_timestamp: Union[None, datetime.datetime]
    offering: str
    url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agent_type = self.agent_type.value

        status = self.status

        last_request_timestamp: Union[None, str]
        if isinstance(self.last_request_timestamp, datetime.datetime):
            last_request_timestamp = self.last_request_timestamp.isoformat()
        else:
            last_request_timestamp = self.last_request_timestamp

        offering = self.offering

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "agent_type": agent_type,
                "status": status,
                "last_request_timestamp": last_request_timestamp,
                "offering": offering,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_type = AgentTypeEnum(d.pop("agent_type"))

        status = d.pop("status")

        def _parse_last_request_timestamp(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_request_timestamp_type_0 = isoparse(data)

                return last_request_timestamp_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_request_timestamp = _parse_last_request_timestamp(d.pop("last_request_timestamp"))

        offering = d.pop("offering")

        url = d.pop("url")

        integration_status_details = cls(
            agent_type=agent_type,
            status=status,
            last_request_timestamp=last_request_timestamp,
            offering=offering,
            url=url,
        )

        integration_status_details.additional_properties = d
        return integration_status_details

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
