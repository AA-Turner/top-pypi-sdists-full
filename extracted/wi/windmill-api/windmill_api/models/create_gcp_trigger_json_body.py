from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_gcp_trigger_json_body_delivery_type import CreateGcpTriggerJsonBodyDeliveryType
from ..models.create_gcp_trigger_json_body_subscription_mode import CreateGcpTriggerJsonBodySubscriptionMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_gcp_trigger_json_body_delivery_config import CreateGcpTriggerJsonBodyDeliveryConfig


T = TypeVar("T", bound="CreateGcpTriggerJsonBody")


@_attrs_define
class CreateGcpTriggerJsonBody:
    """
    Attributes:
        gcp_resource_path (str):
        subscription_mode (CreateGcpTriggerJsonBodySubscriptionMode): The mode of subscription. 'existing' means using
            an existing GCP subscription, while 'create_update' involves creating or updating a new subscription.
        topic_id (str):
        path (str):
        script_path (str):
        is_flow (bool):
        subscription_id (Union[Unset, str]):
        base_endpoint (Union[Unset, str]):
        delivery_type (Union[Unset, CreateGcpTriggerJsonBodyDeliveryType]):
        delivery_config (Union[Unset, CreateGcpTriggerJsonBodyDeliveryConfig]):
        enabled (Union[Unset, bool]):
    """

    gcp_resource_path: str
    subscription_mode: CreateGcpTriggerJsonBodySubscriptionMode
    topic_id: str
    path: str
    script_path: str
    is_flow: bool
    subscription_id: Union[Unset, str] = UNSET
    base_endpoint: Union[Unset, str] = UNSET
    delivery_type: Union[Unset, CreateGcpTriggerJsonBodyDeliveryType] = UNSET
    delivery_config: Union[Unset, "CreateGcpTriggerJsonBodyDeliveryConfig"] = UNSET
    enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        gcp_resource_path = self.gcp_resource_path
        subscription_mode = self.subscription_mode.value

        topic_id = self.topic_id
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        subscription_id = self.subscription_id
        base_endpoint = self.base_endpoint
        delivery_type: Union[Unset, str] = UNSET
        if not isinstance(self.delivery_type, Unset):
            delivery_type = self.delivery_type.value

        delivery_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.delivery_config, Unset):
            delivery_config = self.delivery_config.to_dict()

        enabled = self.enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "gcp_resource_path": gcp_resource_path,
                "subscription_mode": subscription_mode,
                "topic_id": topic_id,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
            }
        )
        if subscription_id is not UNSET:
            field_dict["subscription_id"] = subscription_id
        if base_endpoint is not UNSET:
            field_dict["base_endpoint"] = base_endpoint
        if delivery_type is not UNSET:
            field_dict["delivery_type"] = delivery_type
        if delivery_config is not UNSET:
            field_dict["delivery_config"] = delivery_config
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_gcp_trigger_json_body_delivery_config import CreateGcpTriggerJsonBodyDeliveryConfig

        d = src_dict.copy()
        gcp_resource_path = d.pop("gcp_resource_path")

        subscription_mode = CreateGcpTriggerJsonBodySubscriptionMode(d.pop("subscription_mode"))

        topic_id = d.pop("topic_id")

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        subscription_id = d.pop("subscription_id", UNSET)

        base_endpoint = d.pop("base_endpoint", UNSET)

        _delivery_type = d.pop("delivery_type", UNSET)
        delivery_type: Union[Unset, CreateGcpTriggerJsonBodyDeliveryType]
        if isinstance(_delivery_type, Unset):
            delivery_type = UNSET
        else:
            delivery_type = CreateGcpTriggerJsonBodyDeliveryType(_delivery_type)

        _delivery_config = d.pop("delivery_config", UNSET)
        delivery_config: Union[Unset, CreateGcpTriggerJsonBodyDeliveryConfig]
        if isinstance(_delivery_config, Unset):
            delivery_config = UNSET
        else:
            delivery_config = CreateGcpTriggerJsonBodyDeliveryConfig.from_dict(_delivery_config)

        enabled = d.pop("enabled", UNSET)

        create_gcp_trigger_json_body = cls(
            gcp_resource_path=gcp_resource_path,
            subscription_mode=subscription_mode,
            topic_id=topic_id,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            subscription_id=subscription_id,
            base_endpoint=base_endpoint,
            delivery_type=delivery_type,
            delivery_config=delivery_config,
            enabled=enabled,
        )

        create_gcp_trigger_json_body.additional_properties = d
        return create_gcp_trigger_json_body

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
