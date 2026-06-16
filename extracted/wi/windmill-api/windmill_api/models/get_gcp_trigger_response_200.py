import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_gcp_trigger_response_200_delivery_type import GetGcpTriggerResponse200DeliveryType
from ..models.get_gcp_trigger_response_200_subscription_mode import GetGcpTriggerResponse200SubscriptionMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_gcp_trigger_response_200_delivery_config import GetGcpTriggerResponse200DeliveryConfig
    from ..models.get_gcp_trigger_response_200_draft import GetGcpTriggerResponse200Draft
    from ..models.get_gcp_trigger_response_200_error_handler_args import GetGcpTriggerResponse200ErrorHandlerArgs
    from ..models.get_gcp_trigger_response_200_other_drafts_users_item import (
        GetGcpTriggerResponse200OtherDraftsUsersItem,
    )
    from ..models.get_gcp_trigger_response_200_retry import GetGcpTriggerResponse200Retry


T = TypeVar("T", bound="GetGcpTriggerResponse200")


@_attrs_define
class GetGcpTriggerResponse200:
    """
    Attributes:
        gcp_resource_path (str): Path to the GCP resource containing service account credentials for authentication.
        topic_id (str): Google Cloud Pub/Sub topic ID to subscribe to.
        subscription_id (str): Google Cloud Pub/Sub subscription ID.
        delivery_type (GetGcpTriggerResponse200DeliveryType): Delivery mode for messages. 'push' for HTTP push delivery
            where messages are sent to a webhook endpoint, 'pull' for polling where the trigger actively fetches messages.
        subscription_mode (GetGcpTriggerResponse200SubscriptionMode): The mode of subscription. 'existing' means using
            an existing GCP subscription, while 'create_update' involves creating or updating a new subscription.
        is_draft (bool):
        server_id (Union[Unset, str]): ID of the server currently handling this trigger (internal use).
        delivery_config (Union[Unset, None, GetGcpTriggerResponse200DeliveryConfig]): Configuration for push delivery
            mode.
        last_server_ping (Union[Unset, datetime.datetime]): Timestamp of last server heartbeat (internal use).
        error (Union[Unset, str]): Last error message if the trigger failed.
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails.
        error_handler_args (Union[Unset, GetGcpTriggerResponse200ErrorHandlerArgs]): The arguments to pass to the script
            or flow
        retry (Union[Unset, GetGcpTriggerResponse200Retry]): Retry configuration for failed module executions
        draft_saved_at (Union[Unset, datetime.datetime]):
        no_deployed (Union[Unset, bool]):
        draft (Union[Unset, GetGcpTriggerResponse200Draft]):
        other_drafts_users (Union[Unset, List['GetGcpTriggerResponse200OtherDraftsUsersItem']]): Other workspace users
            (and the legacy NULL-email row, if any)
            with a saved draft at the same path. Populated only on the
            authed user's "get by path" responses for kinds the editor
            surfaces a fork banner for (script, flow, app, raw_app).
            Empty / omitted for kinds without that UI.
    """

    gcp_resource_path: str
    topic_id: str
    subscription_id: str
    delivery_type: GetGcpTriggerResponse200DeliveryType
    subscription_mode: GetGcpTriggerResponse200SubscriptionMode
    is_draft: bool
    server_id: Union[Unset, str] = UNSET
    delivery_config: Union[Unset, None, "GetGcpTriggerResponse200DeliveryConfig"] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "GetGcpTriggerResponse200ErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "GetGcpTriggerResponse200Retry"] = UNSET
    draft_saved_at: Union[Unset, datetime.datetime] = UNSET
    no_deployed: Union[Unset, bool] = UNSET
    draft: Union[Unset, "GetGcpTriggerResponse200Draft"] = UNSET
    other_drafts_users: Union[Unset, List["GetGcpTriggerResponse200OtherDraftsUsersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        gcp_resource_path = self.gcp_resource_path
        topic_id = self.topic_id
        subscription_id = self.subscription_id
        delivery_type = self.delivery_type.value

        subscription_mode = self.subscription_mode.value

        is_draft = self.is_draft
        server_id = self.server_id
        delivery_config: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.delivery_config, Unset):
            delivery_config = self.delivery_config.to_dict() if self.delivery_config else None

        last_server_ping: Union[Unset, str] = UNSET
        if not isinstance(self.last_server_ping, Unset):
            last_server_ping = self.last_server_ping.isoformat()

        error = self.error
        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        draft_saved_at: Union[Unset, str] = UNSET
        if not isinstance(self.draft_saved_at, Unset):
            draft_saved_at = self.draft_saved_at.isoformat()

        no_deployed = self.no_deployed
        draft: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.draft, Unset):
            draft = self.draft.to_dict()

        other_drafts_users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.other_drafts_users, Unset):
            other_drafts_users = []
            for other_drafts_users_item_data in self.other_drafts_users:
                other_drafts_users_item = other_drafts_users_item_data.to_dict()

                other_drafts_users.append(other_drafts_users_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "gcp_resource_path": gcp_resource_path,
                "topic_id": topic_id,
                "subscription_id": subscription_id,
                "delivery_type": delivery_type,
                "subscription_mode": subscription_mode,
                "is_draft": is_draft,
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
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry
        if draft_saved_at is not UNSET:
            field_dict["draft_saved_at"] = draft_saved_at
        if no_deployed is not UNSET:
            field_dict["no_deployed"] = no_deployed
        if draft is not UNSET:
            field_dict["draft"] = draft
        if other_drafts_users is not UNSET:
            field_dict["other_drafts_users"] = other_drafts_users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_gcp_trigger_response_200_delivery_config import GetGcpTriggerResponse200DeliveryConfig
        from ..models.get_gcp_trigger_response_200_draft import GetGcpTriggerResponse200Draft
        from ..models.get_gcp_trigger_response_200_error_handler_args import GetGcpTriggerResponse200ErrorHandlerArgs
        from ..models.get_gcp_trigger_response_200_other_drafts_users_item import (
            GetGcpTriggerResponse200OtherDraftsUsersItem,
        )
        from ..models.get_gcp_trigger_response_200_retry import GetGcpTriggerResponse200Retry

        d = src_dict.copy()
        gcp_resource_path = d.pop("gcp_resource_path")

        topic_id = d.pop("topic_id")

        subscription_id = d.pop("subscription_id")

        delivery_type = GetGcpTriggerResponse200DeliveryType(d.pop("delivery_type"))

        subscription_mode = GetGcpTriggerResponse200SubscriptionMode(d.pop("subscription_mode"))

        is_draft = d.pop("is_draft")

        server_id = d.pop("server_id", UNSET)

        _delivery_config = d.pop("delivery_config", UNSET)
        delivery_config: Union[Unset, None, GetGcpTriggerResponse200DeliveryConfig]
        if _delivery_config is None:
            delivery_config = None
        elif isinstance(_delivery_config, Unset):
            delivery_config = UNSET
        else:
            delivery_config = GetGcpTriggerResponse200DeliveryConfig.from_dict(_delivery_config)

        _last_server_ping = d.pop("last_server_ping", UNSET)
        last_server_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_server_ping, Unset):
            last_server_ping = UNSET
        else:
            last_server_ping = isoparse(_last_server_ping)

        error = d.pop("error", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, GetGcpTriggerResponse200ErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = GetGcpTriggerResponse200ErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, GetGcpTriggerResponse200Retry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = GetGcpTriggerResponse200Retry.from_dict(_retry)

        _draft_saved_at = d.pop("draft_saved_at", UNSET)
        draft_saved_at: Union[Unset, datetime.datetime]
        if isinstance(_draft_saved_at, Unset):
            draft_saved_at = UNSET
        else:
            draft_saved_at = isoparse(_draft_saved_at)

        no_deployed = d.pop("no_deployed", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, GetGcpTriggerResponse200Draft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = GetGcpTriggerResponse200Draft.from_dict(_draft)

        other_drafts_users = []
        _other_drafts_users = d.pop("other_drafts_users", UNSET)
        for other_drafts_users_item_data in _other_drafts_users or []:
            other_drafts_users_item = GetGcpTriggerResponse200OtherDraftsUsersItem.from_dict(
                other_drafts_users_item_data
            )

            other_drafts_users.append(other_drafts_users_item)

        get_gcp_trigger_response_200 = cls(
            gcp_resource_path=gcp_resource_path,
            topic_id=topic_id,
            subscription_id=subscription_id,
            delivery_type=delivery_type,
            subscription_mode=subscription_mode,
            is_draft=is_draft,
            server_id=server_id,
            delivery_config=delivery_config,
            last_server_ping=last_server_ping,
            error=error,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            draft_saved_at=draft_saved_at,
            no_deployed=no_deployed,
            draft=draft,
            other_drafts_users=other_drafts_users,
        )

        get_gcp_trigger_response_200.additional_properties = d
        return get_gcp_trigger_response_200

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
