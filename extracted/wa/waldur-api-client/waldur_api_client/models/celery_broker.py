from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.celery_broker_transport_options import CeleryBrokerTransportOptions


T = TypeVar("T", bound="CeleryBroker")


@_attrs_define
class CeleryBroker:
    """
    Attributes:
        hostname (str): Broker hostname
        userid (str): Broker user ID
        virtual_host (str): Virtual host
        port (int): Broker port
        insist (bool):
        ssl (bool):
        transport (str): Transport protocol
        connect_timeout (int): Connection timeout in seconds
        transport_options (CeleryBrokerTransportOptions): Additional transport options
        login_method (str): Authentication method
        uri_prefix (str):
        heartbeat (float): Heartbeat interval
        failover_strategy (str):
        alternates (list[str]):
    """

    hostname: str
    userid: str
    virtual_host: str
    port: int
    insist: bool
    ssl: bool
    transport: str
    connect_timeout: int
    transport_options: "CeleryBrokerTransportOptions"
    login_method: str
    uri_prefix: str
    heartbeat: float
    failover_strategy: str
    alternates: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hostname = self.hostname

        userid = self.userid

        virtual_host = self.virtual_host

        port = self.port

        insist = self.insist

        ssl = self.ssl

        transport = self.transport

        connect_timeout = self.connect_timeout

        transport_options = self.transport_options.to_dict()

        login_method = self.login_method

        uri_prefix = self.uri_prefix

        heartbeat = self.heartbeat

        failover_strategy = self.failover_strategy

        alternates = self.alternates

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hostname": hostname,
                "userid": userid,
                "virtual_host": virtual_host,
                "port": port,
                "insist": insist,
                "ssl": ssl,
                "transport": transport,
                "connect_timeout": connect_timeout,
                "transport_options": transport_options,
                "login_method": login_method,
                "uri_prefix": uri_prefix,
                "heartbeat": heartbeat,
                "failover_strategy": failover_strategy,
                "alternates": alternates,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.celery_broker_transport_options import CeleryBrokerTransportOptions

        d = dict(src_dict)
        hostname = d.pop("hostname")

        userid = d.pop("userid")

        virtual_host = d.pop("virtual_host")

        port = d.pop("port")

        insist = d.pop("insist")

        ssl = d.pop("ssl")

        transport = d.pop("transport")

        connect_timeout = d.pop("connect_timeout")

        transport_options = CeleryBrokerTransportOptions.from_dict(d.pop("transport_options"))

        login_method = d.pop("login_method")

        uri_prefix = d.pop("uri_prefix")

        heartbeat = d.pop("heartbeat")

        failover_strategy = d.pop("failover_strategy")

        alternates = cast(list[str], d.pop("alternates"))

        celery_broker = cls(
            hostname=hostname,
            userid=userid,
            virtual_host=virtual_host,
            port=port,
            insist=insist,
            ssl=ssl,
            transport=transport,
            connect_timeout=connect_timeout,
            transport_options=transport_options,
            login_method=login_method,
            uri_prefix=uri_prefix,
            heartbeat=heartbeat,
            failover_strategy=failover_strategy,
            alternates=alternates,
        )

        celery_broker.additional_properties = d
        return celery_broker

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
