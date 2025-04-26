import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_gcp_triggers_response_200_item_delivery_type import ListGcpTriggersResponse200ItemDeliveryType
from ..models.list_gcp_triggers_response_200_item_subscription_mode import (
    ListGcpTriggersResponse200ItemSubscriptionMode,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_gcp_triggers_response_200_item_delivery_config import (
        ListGcpTriggersResponse200ItemDeliveryConfig,
    )
    from ..models.list_gcp_triggers_response_200_item_extra_perms import ListGcpTriggersResponse200ItemExtraPerms


T = TypeVar("T", bound="ListGcpTriggersResponse200Item")


@_attrs_define
class ListGcpTriggersResponse200Item:
    """
    Attributes:
        gcp_resource_path (str):
        topic_id (str):
        subscription_id (str):
        delivery_type (ListGcpTriggersResponse200ItemDeliveryType):
        subscription_mode (ListGcpTriggersResponse200ItemSubscriptionMode): The mode of subscription. 'existing' means
            using an existing GCP subscription, while 'create_update' involves creating or updating a new subscription.
        enabled (bool):
        path (str):
        script_path (str):
        email (str):
        extra_perms (ListGcpTriggersResponse200ItemExtraPerms):
        workspace_id (str):
        edited_by (str):
        edited_at (datetime.datetime):
        is_flow (bool):
        server_id (Union[Unset, str]):
        delivery_config (Union[Unset, ListGcpTriggersResponse200ItemDeliveryConfig]):
        last_server_ping (Union[Unset, datetime.datetime]):
        error (Union[Unset, str]):
    """

    gcp_resource_path: str
    topic_id: str
    subscription_id: str
    delivery_type: ListGcpTriggersResponse200ItemDeliveryType
    subscription_mode: ListGcpTriggersResponse200ItemSubscriptionMode
    enabled: bool
    path: str
    script_path: str
    email: str
    extra_perms: "ListGcpTriggersResponse200ItemExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    server_id: Union[Unset, str] = UNSET
    delivery_config: Union[Unset, "ListGcpTriggersResponse200ItemDeliveryConfig"] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        gcp_resource_path = self.gcp_resource_path
        topic_id = self.topic_id
        subscription_id = self.subscription_id
        delivery_type = self.delivery_type.value

        subscription_mode = self.subscription_mode.value

        enabled = self.enabled
        path = self.path
        script_path = self.script_path
        email = self.email
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
        server_id = self.server_id
        delivery_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.delivery_config, Unset):
            delivery_config = self.delivery_config.to_dict()

        last_server_ping: Union[Unset, str] = UNSET
        if not isinstance(self.last_server_ping, Unset):
            last_server_ping = self.last_server_ping.isoformat()

        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "gcp_resource_path": gcp_resource_path,
                "topic_id": topic_id,
                "subscription_id": subscription_id,
                "delivery_type": delivery_type,
                "subscription_mode": subscription_mode,
                "enabled": enabled,
                "path": path,
                "script_path": script_path,
                "email": email,
                "extra_perms": extra_perms,
                "workspace_id": workspace_id,
                "edited_by": edited_by,
                "edited_at": edited_at,
                "is_flow": is_flow,
            }
        )
        if server_id is not UNSET:
            field_dict["server_id"] = server_id
        if delivery_config is not UNSET:
            field_dict["delivery_config"] = delivery_config
        if last_server_ping is not UNSET:
            field_dict["last_server_ping"] = last_server_ping
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_gcp_triggers_response_200_item_delivery_config import (
            ListGcpTriggersResponse200ItemDeliveryConfig,
        )
        from ..models.list_gcp_triggers_response_200_item_extra_perms import ListGcpTriggersResponse200ItemExtraPerms

        d = src_dict.copy()
        gcp_resource_path = d.pop("gcp_resource_path")

        topic_id = d.pop("topic_id")

        subscription_id = d.pop("subscription_id")

        delivery_type = ListGcpTriggersResponse200ItemDeliveryType(d.pop("delivery_type"))

        subscription_mode = ListGcpTriggersResponse200ItemSubscriptionMode(d.pop("subscription_mode"))

        enabled = d.pop("enabled")

        path = d.pop("path")

        script_path = d.pop("script_path")

        email = d.pop("email")

        extra_perms = ListGcpTriggersResponse200ItemExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        server_id = d.pop("server_id", UNSET)

        _delivery_config = d.pop("delivery_config", UNSET)
        delivery_config: Union[Unset, ListGcpTriggersResponse200ItemDeliveryConfig]
        if isinstance(_delivery_config, Unset):
            delivery_config = UNSET
        else:
            delivery_config = ListGcpTriggersResponse200ItemDeliveryConfig.from_dict(_delivery_config)

        _last_server_ping = d.pop("last_server_ping", UNSET)
        last_server_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_server_ping, Unset):
            last_server_ping = UNSET
        else:
            last_server_ping = isoparse(_last_server_ping)

        error = d.pop("error", UNSET)

        list_gcp_triggers_response_200_item = cls(
            gcp_resource_path=gcp_resource_path,
            topic_id=topic_id,
            subscription_id=subscription_id,
            delivery_type=delivery_type,
            subscription_mode=subscription_mode,
            enabled=enabled,
            path=path,
            script_path=script_path,
            email=email,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            server_id=server_id,
            delivery_config=delivery_config,
            last_server_ping=last_server_ping,
            error=error,
        )

        list_gcp_triggers_response_200_item.additional_properties = d
        return list_gcp_triggers_response_200_item

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
