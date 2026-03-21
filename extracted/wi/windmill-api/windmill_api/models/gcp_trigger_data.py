from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.gcp_trigger_data_delivery_type import GcpTriggerDataDeliveryType
from ..models.gcp_trigger_data_mode import GcpTriggerDataMode
from ..models.gcp_trigger_data_subscription_mode import GcpTriggerDataSubscriptionMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.gcp_trigger_data_delivery_config import GcpTriggerDataDeliveryConfig
    from ..models.gcp_trigger_data_error_handler_args import GcpTriggerDataErrorHandlerArgs
    from ..models.gcp_trigger_data_retry import GcpTriggerDataRetry


T = TypeVar("T", bound="GcpTriggerData")


@_attrs_define
class GcpTriggerData:
    """Data for creating or updating a Google Cloud Pub/Sub trigger.

    Attributes:
        gcp_resource_path (str): Path to the GCP resource containing service account credentials for authentication.
        subscription_mode (GcpTriggerDataSubscriptionMode): The mode of subscription. 'existing' means using an existing
            GCP subscription, while 'create_update' involves creating or updating a new subscription.
        topic_id (str): Google Cloud Pub/Sub topic ID to subscribe to.
        path (str): The unique path identifier for this trigger.
        script_path (str): Path to the script or flow to execute when a message is received.
        is_flow (bool): True if script_path points to a flow, false if it points to a script.
        subscription_id (Union[Unset, str]): Google Cloud Pub/Sub subscription ID.
        base_endpoint (Union[Unset, str]): Base URL for push delivery endpoint.
        delivery_type (Union[Unset, GcpTriggerDataDeliveryType]): Delivery mode for messages. 'push' for HTTP push
            delivery where messages are sent to a webhook endpoint, 'pull' for polling where the trigger actively fetches
            messages.
        delivery_config (Union[Unset, None, GcpTriggerDataDeliveryConfig]): Configuration for push delivery mode.
        mode (Union[Unset, GcpTriggerDataMode]): job trigger mode
        auto_acknowledge_msg (Union[Unset, bool]): If true, automatically acknowledge messages after processing.
        ack_deadline (Union[Unset, int]): Time in seconds within which the message must be acknowledged. If not
            provided, defaults to the subscription's acknowledgment deadline (600 seconds).
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails.
        error_handler_args (Union[Unset, GcpTriggerDataErrorHandlerArgs]): The arguments to pass to the script or flow
        retry (Union[Unset, GcpTriggerDataRetry]): Retry configuration for failed module executions
        permissioned_as (Union[Unset, str]): The user or group this trigger runs as. Used during deployment to preserve
            the original trigger owner.
        preserve_permissioned_as (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group,
            preserves the original permissioned_as value instead of overwriting it.
    """

    gcp_resource_path: str
    subscription_mode: GcpTriggerDataSubscriptionMode
    topic_id: str
    path: str
    script_path: str
    is_flow: bool
    subscription_id: Union[Unset, str] = UNSET
    base_endpoint: Union[Unset, str] = UNSET
    delivery_type: Union[Unset, GcpTriggerDataDeliveryType] = UNSET
    delivery_config: Union[Unset, None, "GcpTriggerDataDeliveryConfig"] = UNSET
    mode: Union[Unset, GcpTriggerDataMode] = UNSET
    auto_acknowledge_msg: Union[Unset, bool] = UNSET
    ack_deadline: Union[Unset, int] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "GcpTriggerDataErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "GcpTriggerDataRetry"] = UNSET
    permissioned_as: Union[Unset, str] = UNSET
    preserve_permissioned_as: Union[Unset, bool] = UNSET
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

        delivery_config: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.delivery_config, Unset):
            delivery_config = self.delivery_config.to_dict() if self.delivery_config else None

        mode: Union[Unset, str] = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        auto_acknowledge_msg = self.auto_acknowledge_msg
        ack_deadline = self.ack_deadline
        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        permissioned_as = self.permissioned_as
        preserve_permissioned_as = self.preserve_permissioned_as

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
        if mode is not UNSET:
            field_dict["mode"] = mode
        if auto_acknowledge_msg is not UNSET:
            field_dict["auto_acknowledge_msg"] = auto_acknowledge_msg
        if ack_deadline is not UNSET:
            field_dict["ack_deadline"] = ack_deadline
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry
        if permissioned_as is not UNSET:
            field_dict["permissioned_as"] = permissioned_as
        if preserve_permissioned_as is not UNSET:
            field_dict["preserve_permissioned_as"] = preserve_permissioned_as

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.gcp_trigger_data_delivery_config import GcpTriggerDataDeliveryConfig
        from ..models.gcp_trigger_data_error_handler_args import GcpTriggerDataErrorHandlerArgs
        from ..models.gcp_trigger_data_retry import GcpTriggerDataRetry

        d = src_dict.copy()
        gcp_resource_path = d.pop("gcp_resource_path")

        subscription_mode = GcpTriggerDataSubscriptionMode(d.pop("subscription_mode"))

        topic_id = d.pop("topic_id")

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        subscription_id = d.pop("subscription_id", UNSET)

        base_endpoint = d.pop("base_endpoint", UNSET)

        _delivery_type = d.pop("delivery_type", UNSET)
        delivery_type: Union[Unset, GcpTriggerDataDeliveryType]
        if isinstance(_delivery_type, Unset):
            delivery_type = UNSET
        else:
            delivery_type = GcpTriggerDataDeliveryType(_delivery_type)

        _delivery_config = d.pop("delivery_config", UNSET)
        delivery_config: Union[Unset, None, GcpTriggerDataDeliveryConfig]
        if _delivery_config is None:
            delivery_config = None
        elif isinstance(_delivery_config, Unset):
            delivery_config = UNSET
        else:
            delivery_config = GcpTriggerDataDeliveryConfig.from_dict(_delivery_config)

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, GcpTriggerDataMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = GcpTriggerDataMode(_mode)

        auto_acknowledge_msg = d.pop("auto_acknowledge_msg", UNSET)

        ack_deadline = d.pop("ack_deadline", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, GcpTriggerDataErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = GcpTriggerDataErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, GcpTriggerDataRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = GcpTriggerDataRetry.from_dict(_retry)

        permissioned_as = d.pop("permissioned_as", UNSET)

        preserve_permissioned_as = d.pop("preserve_permissioned_as", UNSET)

        gcp_trigger_data = cls(
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
            mode=mode,
            auto_acknowledge_msg=auto_acknowledge_msg,
            ack_deadline=ack_deadline,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            permissioned_as=permissioned_as,
            preserve_permissioned_as=preserve_permissioned_as,
        )

        gcp_trigger_data.additional_properties = d
        return gcp_trigger_data

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
