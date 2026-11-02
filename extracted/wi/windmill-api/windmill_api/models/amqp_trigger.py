import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.amqp_trigger_mode import AmqpTriggerMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.amqp_trigger_error_handler_args import AmqpTriggerErrorHandlerArgs
    from ..models.amqp_trigger_exchange import AmqpTriggerExchange
    from ..models.amqp_trigger_extra_perms import AmqpTriggerExtraPerms
    from ..models.amqp_trigger_options import AmqpTriggerOptions
    from ..models.amqp_trigger_retry import AmqpTriggerRetry


T = TypeVar("T", bound="AmqpTrigger")


@_attrs_define
class AmqpTrigger:
    """
    Attributes:
        amqp_resource_path (str): Path to the AMQP resource containing broker connection configuration
        queue_name (str): Name of the queue to consume messages from
        path (str): The unique Windmill path for this trigger. Must be of the form `u/<user>/<path>` or
            `f/<folder>/<path>`. This is the trigger object path, not the HTTP route path.
        script_path (str): Path to the script or flow to execute when triggered
        permissioned_as (str): The user or group this trigger runs as (permissioned_as)
        extra_perms (AmqpTriggerExtraPerms): Additional permissions for this trigger
        workspace_id (str): The workspace this trigger belongs to
        edited_by (str): Username of the last person who edited this trigger
        edited_at (datetime.datetime): Timestamp of the last edit
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        mode (AmqpTriggerMode): job trigger mode
        exchange (Union[Unset, None, AmqpTriggerExchange]): Optional exchange binding for the consumed queue
        options (Union[Unset, None, AmqpTriggerOptions]): Optional consumer options (queue declaration, prefetch)
        server_id (Union[Unset, str]): ID of the server currently handling this trigger (internal)
        last_server_ping (Union[Unset, datetime.datetime]): Timestamp of last server heartbeat (internal)
        error (Union[Unset, str]): Last error message if the trigger failed
        error_handler_path (Union[Unset, str]): Path to a script to run when the triggered job fails. A bare path,
            without the script/ or flow/ prefix a schedule error handler takes; it cannot be a flow.
        error_handler_args (Union[Unset, AmqpTriggerErrorHandlerArgs]): The arguments to pass to the script or flow
        retry (Union[Unset, AmqpTriggerRetry]): Retry configuration for failed module executions
        labels (Union[Unset, List[str]]):
        draft_only (Union[Unset, bool]): True when this row is a per-user draft with no deployed
            trigger at the same path. Set by list endpoints when
            `include_draft_only=true` synthesizes the row from the
            draft. Frontend renders a "Draft" badge.
        is_draft (Union[Unset, bool]): True when the authed user has a per-user draft at this path
            (over a deployed row or a synthesized draft-only row).
            Frontend appends a `*` to the displayed name.
    """

    amqp_resource_path: str
    queue_name: str
    path: str
    script_path: str
    permissioned_as: str
    extra_perms: "AmqpTriggerExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    mode: AmqpTriggerMode
    exchange: Union[Unset, None, "AmqpTriggerExchange"] = UNSET
    options: Union[Unset, None, "AmqpTriggerOptions"] = UNSET
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "AmqpTriggerErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "AmqpTriggerRetry"] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    draft_only: Union[Unset, bool] = UNSET
    is_draft: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amqp_resource_path = self.amqp_resource_path
        queue_name = self.queue_name
        path = self.path
        script_path = self.script_path
        permissioned_as = self.permissioned_as
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
        mode = self.mode.value

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

        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        draft_only = self.draft_only
        is_draft = self.is_draft

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amqp_resource_path": amqp_resource_path,
                "queue_name": queue_name,
                "path": path,
                "script_path": script_path,
                "permissioned_as": permissioned_as,
                "extra_perms": extra_perms,
                "workspace_id": workspace_id,
                "edited_by": edited_by,
                "edited_at": edited_at,
                "is_flow": is_flow,
                "mode": mode,
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
        if labels is not UNSET:
            field_dict["labels"] = labels
        if draft_only is not UNSET:
            field_dict["draft_only"] = draft_only
        if is_draft is not UNSET:
            field_dict["is_draft"] = is_draft

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.amqp_trigger_error_handler_args import AmqpTriggerErrorHandlerArgs
        from ..models.amqp_trigger_exchange import AmqpTriggerExchange
        from ..models.amqp_trigger_extra_perms import AmqpTriggerExtraPerms
        from ..models.amqp_trigger_options import AmqpTriggerOptions
        from ..models.amqp_trigger_retry import AmqpTriggerRetry

        d = src_dict.copy()
        amqp_resource_path = d.pop("amqp_resource_path")

        queue_name = d.pop("queue_name")

        path = d.pop("path")

        script_path = d.pop("script_path")

        permissioned_as = d.pop("permissioned_as")

        extra_perms = AmqpTriggerExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        mode = AmqpTriggerMode(d.pop("mode"))

        _exchange = d.pop("exchange", UNSET)
        exchange: Union[Unset, None, AmqpTriggerExchange]
        if _exchange is None:
            exchange = None
        elif isinstance(_exchange, Unset):
            exchange = UNSET
        else:
            exchange = AmqpTriggerExchange.from_dict(_exchange)

        _options = d.pop("options", UNSET)
        options: Union[Unset, None, AmqpTriggerOptions]
        if _options is None:
            options = None
        elif isinstance(_options, Unset):
            options = UNSET
        else:
            options = AmqpTriggerOptions.from_dict(_options)

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
        error_handler_args: Union[Unset, AmqpTriggerErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = AmqpTriggerErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, AmqpTriggerRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = AmqpTriggerRetry.from_dict(_retry)

        labels = cast(List[str], d.pop("labels", UNSET))

        draft_only = d.pop("draft_only", UNSET)

        is_draft = d.pop("is_draft", UNSET)

        amqp_trigger = cls(
            amqp_resource_path=amqp_resource_path,
            queue_name=queue_name,
            path=path,
            script_path=script_path,
            permissioned_as=permissioned_as,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            mode=mode,
            exchange=exchange,
            options=options,
            server_id=server_id,
            last_server_ping=last_server_ping,
            error=error,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            labels=labels,
            draft_only=draft_only,
            is_draft=is_draft,
        )

        amqp_trigger.additional_properties = d
        return amqp_trigger

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
