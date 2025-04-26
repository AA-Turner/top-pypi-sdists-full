from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.triggers_count_primary_schedule import TriggersCountPrimarySchedule


T = TypeVar("T", bound="TriggersCount")


@_attrs_define
class TriggersCount:
    """
    Attributes:
        primary_schedule (Union[Unset, TriggersCountPrimarySchedule]):
        schedule_count (Union[Unset, float]):
        http_routes_count (Union[Unset, float]):
        webhook_count (Union[Unset, float]):
        email_count (Union[Unset, float]):
        websocket_count (Union[Unset, float]):
        postgres_count (Union[Unset, float]):
        kafka_count (Union[Unset, float]):
        nats_count (Union[Unset, float]):
        mqtt_count (Union[Unset, float]):
        gcp_count (Union[Unset, float]):
        sqs_count (Union[Unset, float]):
    """

    primary_schedule: Union[Unset, "TriggersCountPrimarySchedule"] = UNSET
    schedule_count: Union[Unset, float] = UNSET
    http_routes_count: Union[Unset, float] = UNSET
    webhook_count: Union[Unset, float] = UNSET
    email_count: Union[Unset, float] = UNSET
    websocket_count: Union[Unset, float] = UNSET
    postgres_count: Union[Unset, float] = UNSET
    kafka_count: Union[Unset, float] = UNSET
    nats_count: Union[Unset, float] = UNSET
    mqtt_count: Union[Unset, float] = UNSET
    gcp_count: Union[Unset, float] = UNSET
    sqs_count: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        primary_schedule: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.primary_schedule, Unset):
            primary_schedule = self.primary_schedule.to_dict()

        schedule_count = self.schedule_count
        http_routes_count = self.http_routes_count
        webhook_count = self.webhook_count
        email_count = self.email_count
        websocket_count = self.websocket_count
        postgres_count = self.postgres_count
        kafka_count = self.kafka_count
        nats_count = self.nats_count
        mqtt_count = self.mqtt_count
        gcp_count = self.gcp_count
        sqs_count = self.sqs_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if primary_schedule is not UNSET:
            field_dict["primary_schedule"] = primary_schedule
        if schedule_count is not UNSET:
            field_dict["schedule_count"] = schedule_count
        if http_routes_count is not UNSET:
            field_dict["http_routes_count"] = http_routes_count
        if webhook_count is not UNSET:
            field_dict["webhook_count"] = webhook_count
        if email_count is not UNSET:
            field_dict["email_count"] = email_count
        if websocket_count is not UNSET:
            field_dict["websocket_count"] = websocket_count
        if postgres_count is not UNSET:
            field_dict["postgres_count"] = postgres_count
        if kafka_count is not UNSET:
            field_dict["kafka_count"] = kafka_count
        if nats_count is not UNSET:
            field_dict["nats_count"] = nats_count
        if mqtt_count is not UNSET:
            field_dict["mqtt_count"] = mqtt_count
        if gcp_count is not UNSET:
            field_dict["gcp_count"] = gcp_count
        if sqs_count is not UNSET:
            field_dict["sqs_count"] = sqs_count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.triggers_count_primary_schedule import TriggersCountPrimarySchedule

        d = src_dict.copy()
        _primary_schedule = d.pop("primary_schedule", UNSET)
        primary_schedule: Union[Unset, TriggersCountPrimarySchedule]
        if isinstance(_primary_schedule, Unset):
            primary_schedule = UNSET
        else:
            primary_schedule = TriggersCountPrimarySchedule.from_dict(_primary_schedule)

        schedule_count = d.pop("schedule_count", UNSET)

        http_routes_count = d.pop("http_routes_count", UNSET)

        webhook_count = d.pop("webhook_count", UNSET)

        email_count = d.pop("email_count", UNSET)

        websocket_count = d.pop("websocket_count", UNSET)

        postgres_count = d.pop("postgres_count", UNSET)

        kafka_count = d.pop("kafka_count", UNSET)

        nats_count = d.pop("nats_count", UNSET)

        mqtt_count = d.pop("mqtt_count", UNSET)

        gcp_count = d.pop("gcp_count", UNSET)

        sqs_count = d.pop("sqs_count", UNSET)

        triggers_count = cls(
            primary_schedule=primary_schedule,
            schedule_count=schedule_count,
            http_routes_count=http_routes_count,
            webhook_count=webhook_count,
            email_count=email_count,
            websocket_count=websocket_count,
            postgres_count=postgres_count,
            kafka_count=kafka_count,
            nats_count=nats_count,
            mqtt_count=mqtt_count,
            gcp_count=gcp_count,
            sqs_count=sqs_count,
        )

        triggers_count.additional_properties = d
        return triggers_count

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
