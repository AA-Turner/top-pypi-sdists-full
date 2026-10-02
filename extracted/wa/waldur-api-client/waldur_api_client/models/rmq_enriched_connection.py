import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.rmq_client_properties import RmqClientProperties


T = TypeVar("T", bound="RmqEnrichedConnection")


@_attrs_define
class RmqEnrichedConnection:
    """
    Attributes:
        source_ip (str): Client IP address
        vhost (str): Virtual host name
        connected_at (Union[None, datetime.datetime]): Connection establishment timestamp
        state (str): Connection state: 'running', 'blocked', 'blocking'
        recv_oct (int): Bytes received on this connection
        send_oct (int): Bytes sent on this connection
        channels (int): Number of channels on this connection
        timeout (Union[None, int]): Heartbeat timeout in seconds
        client_properties (Union['RmqClientProperties', None]): Client identification properties
    """

    source_ip: str
    vhost: str
    connected_at: Union[None, datetime.datetime]
    state: str
    recv_oct: int
    send_oct: int
    channels: int
    timeout: Union[None, int]
    client_properties: Union["RmqClientProperties", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.rmq_client_properties import RmqClientProperties

        source_ip = self.source_ip

        vhost = self.vhost

        connected_at: Union[None, str]
        if isinstance(self.connected_at, datetime.datetime):
            connected_at = self.connected_at.isoformat()
        else:
            connected_at = self.connected_at

        state = self.state

        recv_oct = self.recv_oct

        send_oct = self.send_oct

        channels = self.channels

        timeout: Union[None, int]
        timeout = self.timeout

        client_properties: Union[None, dict[str, Any]]
        if isinstance(self.client_properties, RmqClientProperties):
            client_properties = self.client_properties.to_dict()
        else:
            client_properties = self.client_properties

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source_ip": source_ip,
                "vhost": vhost,
                "connected_at": connected_at,
                "state": state,
                "recv_oct": recv_oct,
                "send_oct": send_oct,
                "channels": channels,
                "timeout": timeout,
                "client_properties": client_properties,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rmq_client_properties import RmqClientProperties

        d = dict(src_dict)
        source_ip = d.pop("source_ip")

        vhost = d.pop("vhost")

        def _parse_connected_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                connected_at_type_0 = isoparse(data)

                return connected_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        connected_at = _parse_connected_at(d.pop("connected_at"))

        state = d.pop("state")

        recv_oct = d.pop("recv_oct")

        send_oct = d.pop("send_oct")

        channels = d.pop("channels")

        def _parse_timeout(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        timeout = _parse_timeout(d.pop("timeout"))

        def _parse_client_properties(data: object) -> Union["RmqClientProperties", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                client_properties_type_1 = RmqClientProperties.from_dict(data)

                return client_properties_type_1
            except:  # noqa: E722
                pass
            return cast(Union["RmqClientProperties", None], data)

        client_properties = _parse_client_properties(d.pop("client_properties"))

        rmq_enriched_connection = cls(
            source_ip=source_ip,
            vhost=vhost,
            connected_at=connected_at,
            state=state,
            recv_oct=recv_oct,
            send_oct=send_oct,
            channels=channels,
            timeout=timeout,
            client_properties=client_properties,
        )

        rmq_enriched_connection.additional_properties = d
        return rmq_enriched_connection

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
