import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_amqp_trigger_response_200_draft import GetAmqpTriggerResponse200Draft
    from ..models.get_amqp_trigger_response_200_error_handler_args import GetAmqpTriggerResponse200ErrorHandlerArgs
    from ..models.get_amqp_trigger_response_200_exchange import GetAmqpTriggerResponse200Exchange
    from ..models.get_amqp_trigger_response_200_options import GetAmqpTriggerResponse200Options
    from ..models.get_amqp_trigger_response_200_other_drafts_users_item import (
        GetAmqpTriggerResponse200OtherDraftsUsersItem,
    )
    from ..models.get_amqp_trigger_response_200_retry import GetAmqpTriggerResponse200Retry


T = TypeVar("T", bound="GetAmqpTriggerResponse200")


@_attrs_define
class GetAmqpTriggerResponse200:
    """
    Attributes:
        amqp_resource_path (str): Path to the AMQP resource containing broker connection configuration
        queue_name (str): Name of the queue to consume messages from
        is_draft (bool):
        exchange (Union[Unset, None, GetAmqpTriggerResponse200Exchange]): Optional exchange binding for the consumed
            queue
        options (Union[Unset, None, GetAmqpTriggerResponse200Options]): Optional consumer options (queue declaration,
            prefetch)
        server_id (Union[Unset, str]): ID of the server currently handling this trigger (internal)
        last_server_ping (Union[Unset, datetime.datetime]): Timestamp of last server heartbeat (internal)
        error (Union[Unset, str]): Last error message if the trigger failed
        error_handler_path (Union[Unset, str]): Path to a script to run when the triggered job fails. A bare path,
            without the script/ or flow/ prefix a schedule error handler takes; it cannot be a flow.
        error_handler_args (Union[Unset, GetAmqpTriggerResponse200ErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, GetAmqpTriggerResponse200Retry]): Retry configuration for failed module executions
        draft_saved_at (Union[Unset, datetime.datetime]):
        no_deployed (Union[Unset, bool]):
        draft (Union[Unset, GetAmqpTriggerResponse200Draft]):
        other_drafts_users (Union[Unset, List['GetAmqpTriggerResponse200OtherDraftsUsersItem']]): Other workspace users
            (and the legacy NULL-email row, if any)
            with a saved draft at the same path. Populated only on the
            authed user's "get by path" responses for kinds the editor
            surfaces a fork banner for (script, flow, app, raw_app).
            Empty / omitted for kinds without that UI.
    """

    amqp_resource_path: str
    queue_name: str
    is_draft: bool
    exchange: Union[Unset, None, "GetAmqpTriggerResponse200Exchange"] = UNSET
    options: Union[Unset, None, "GetAmqpTriggerResponse200Options"] = UNSET
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "GetAmqpTriggerResponse200ErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "GetAmqpTriggerResponse200Retry"] = UNSET
    draft_saved_at: Union[Unset, datetime.datetime] = UNSET
    no_deployed: Union[Unset, bool] = UNSET
    draft: Union[Unset, "GetAmqpTriggerResponse200Draft"] = UNSET
    other_drafts_users: Union[Unset, List["GetAmqpTriggerResponse200OtherDraftsUsersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amqp_resource_path = self.amqp_resource_path
        queue_name = self.queue_name
        is_draft = self.is_draft
        exchange: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.exchange, Unset):
            exchange = self.exchange.to_dict() if self.exchange else None

        options: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict() if self.options else None

        server_id = self.server_id
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
                "amqp_resource_path": amqp_resource_path,
                "queue_name": queue_name,
                "is_draft": is_draft,
            }
        )
        if exchange is not UNSET:
            field_dict["exchange"] = exchange
        if options is not UNSET:
            field_dict["options"] = options
        if server_id is not UNSET:
            field_dict["server_id"] = server_id
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
        from ..models.get_amqp_trigger_response_200_draft import GetAmqpTriggerResponse200Draft
        from ..models.get_amqp_trigger_response_200_error_handler_args import GetAmqpTriggerResponse200ErrorHandlerArgs
        from ..models.get_amqp_trigger_response_200_exchange import GetAmqpTriggerResponse200Exchange
        from ..models.get_amqp_trigger_response_200_options import GetAmqpTriggerResponse200Options
        from ..models.get_amqp_trigger_response_200_other_drafts_users_item import (
            GetAmqpTriggerResponse200OtherDraftsUsersItem,
        )
        from ..models.get_amqp_trigger_response_200_retry import GetAmqpTriggerResponse200Retry

        d = src_dict.copy()
        amqp_resource_path = d.pop("amqp_resource_path")

        queue_name = d.pop("queue_name")

        is_draft = d.pop("is_draft")

        _exchange = d.pop("exchange", UNSET)
        exchange: Union[Unset, None, GetAmqpTriggerResponse200Exchange]
        if _exchange is None:
            exchange = None
        elif isinstance(_exchange, Unset):
            exchange = UNSET
        else:
            exchange = GetAmqpTriggerResponse200Exchange.from_dict(_exchange)

        _options = d.pop("options", UNSET)
        options: Union[Unset, None, GetAmqpTriggerResponse200Options]
        if _options is None:
            options = None
        elif isinstance(_options, Unset):
            options = UNSET
        else:
            options = GetAmqpTriggerResponse200Options.from_dict(_options)

        server_id = d.pop("server_id", UNSET)

        _last_server_ping = d.pop("last_server_ping", UNSET)
        last_server_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_server_ping, Unset):
            last_server_ping = UNSET
        else:
            last_server_ping = isoparse(_last_server_ping)

        error = d.pop("error", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, GetAmqpTriggerResponse200ErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = GetAmqpTriggerResponse200ErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, GetAmqpTriggerResponse200Retry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = GetAmqpTriggerResponse200Retry.from_dict(_retry)

        _draft_saved_at = d.pop("draft_saved_at", UNSET)
        draft_saved_at: Union[Unset, datetime.datetime]
        if isinstance(_draft_saved_at, Unset):
            draft_saved_at = UNSET
        else:
            draft_saved_at = isoparse(_draft_saved_at)

        no_deployed = d.pop("no_deployed", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, GetAmqpTriggerResponse200Draft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = GetAmqpTriggerResponse200Draft.from_dict(_draft)

        other_drafts_users = []
        _other_drafts_users = d.pop("other_drafts_users", UNSET)
        for other_drafts_users_item_data in _other_drafts_users or []:
            other_drafts_users_item = GetAmqpTriggerResponse200OtherDraftsUsersItem.from_dict(
                other_drafts_users_item_data
            )

            other_drafts_users.append(other_drafts_users_item)

        get_amqp_trigger_response_200 = cls(
            amqp_resource_path=amqp_resource_path,
            queue_name=queue_name,
            is_draft=is_draft,
            exchange=exchange,
            options=options,
            server_id=server_id,
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

        get_amqp_trigger_response_200.additional_properties = d
        return get_amqp_trigger_response_200

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
