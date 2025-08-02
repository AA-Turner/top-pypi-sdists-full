from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetUsedTriggersResponse200")


@_attrs_define
class GetUsedTriggersResponse200:
    """
    Attributes:
        http_routes_used (bool):
        websocket_used (bool):
        kafka_used (bool):
        nats_used (bool):
        postgres_used (bool):
        mqtt_used (bool):
        gcp_used (bool):
        sqs_used (bool):
    """

    http_routes_used: bool
    websocket_used: bool
    kafka_used: bool
    nats_used: bool
    postgres_used: bool
    mqtt_used: bool
    gcp_used: bool
    sqs_used: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        http_routes_used = self.http_routes_used
        websocket_used = self.websocket_used
        kafka_used = self.kafka_used
        nats_used = self.nats_used
        postgres_used = self.postgres_used
        mqtt_used = self.mqtt_used
        gcp_used = self.gcp_used
        sqs_used = self.sqs_used

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "http_routes_used": http_routes_used,
                "websocket_used": websocket_used,
                "kafka_used": kafka_used,
                "nats_used": nats_used,
                "postgres_used": postgres_used,
                "mqtt_used": mqtt_used,
                "gcp_used": gcp_used,
                "sqs_used": sqs_used,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        http_routes_used = d.pop("http_routes_used")

        websocket_used = d.pop("websocket_used")

        kafka_used = d.pop("kafka_used")

        nats_used = d.pop("nats_used")

        postgres_used = d.pop("postgres_used")

        mqtt_used = d.pop("mqtt_used")

        gcp_used = d.pop("gcp_used")

        sqs_used = d.pop("sqs_used")

        get_used_triggers_response_200 = cls(
            http_routes_used=http_routes_used,
            websocket_used=websocket_used,
            kafka_used=kafka_used,
            nats_used=nats_used,
            postgres_used=postgres_used,
            mqtt_used=mqtt_used,
            gcp_used=gcp_used,
            sqs_used=sqs_used,
        )

        get_used_triggers_response_200.additional_properties = d
        return get_used_triggers_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
