import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="AgentRmqConnection")


@_attrs_define
class AgentRmqConnection:
    """
    Attributes:
        connected (bool): Whether the agent has an active connection
        source_ip (Union[None, str]): Client IP address of active connection
        connected_at (Union[None, datetime.datetime]): Connection establishment timestamp
        state (Union[None, str]): Connection state: 'running', 'blocked', 'blocking'
        recv_oct (Union[None, int]): Bytes received on this connection
        send_oct (Union[None, int]): Bytes sent on this connection
    """

    connected: bool
    source_ip: Union[None, str]
    connected_at: Union[None, datetime.datetime]
    state: Union[None, str]
    recv_oct: Union[None, int]
    send_oct: Union[None, int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        connected = self.connected

        source_ip: Union[None, str]
        source_ip = self.source_ip

        connected_at: Union[None, str]
        if isinstance(self.connected_at, datetime.datetime):
            connected_at = self.connected_at.isoformat()
        else:
            connected_at = self.connected_at

        state: Union[None, str]
        state = self.state

        recv_oct: Union[None, int]
        recv_oct = self.recv_oct

        send_oct: Union[None, int]
        send_oct = self.send_oct

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "connected": connected,
                "source_ip": source_ip,
                "connected_at": connected_at,
                "state": state,
                "recv_oct": recv_oct,
                "send_oct": send_oct,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connected = d.pop("connected")

        def _parse_source_ip(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        source_ip = _parse_source_ip(d.pop("source_ip"))

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

        def _parse_state(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        state = _parse_state(d.pop("state"))

        def _parse_recv_oct(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        recv_oct = _parse_recv_oct(d.pop("recv_oct"))

        def _parse_send_oct(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        send_oct = _parse_send_oct(d.pop("send_oct"))

        agent_rmq_connection = cls(
            connected=connected,
            source_ip=source_ip,
            connected_at=connected_at,
            state=state,
            recv_oct=recv_oct,
            send_oct=send_oct,
        )

        agent_rmq_connection.additional_properties = d
        return agent_rmq_connection

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
