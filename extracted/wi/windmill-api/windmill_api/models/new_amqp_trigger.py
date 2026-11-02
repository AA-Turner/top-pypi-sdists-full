from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.new_amqp_trigger_mode import NewAmqpTriggerMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_amqp_trigger_error_handler_args import NewAmqpTriggerErrorHandlerArgs
    from ..models.new_amqp_trigger_exchange import NewAmqpTriggerExchange
    from ..models.new_amqp_trigger_options import NewAmqpTriggerOptions
    from ..models.new_amqp_trigger_retry import NewAmqpTriggerRetry


T = TypeVar("T", bound="NewAmqpTrigger")


@_attrs_define
class NewAmqpTrigger:
    """
    Attributes:
        amqp_resource_path (str): Path to the AMQP resource containing broker connection configuration
        queue_name (str): Name of the queue to consume messages from
        path (str): The unique Windmill path for this trigger. Must be of the form `u/<user>/<path>` or
            `f/<folder>/<path>`.
        script_path (str): Path to the script or flow to execute when a message is received
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        exchange (Union[Unset, None, NewAmqpTriggerExchange]): Optional exchange binding for the consumed queue
        options (Union[Unset, None, NewAmqpTriggerOptions]): Optional consumer options (queue declaration, prefetch)
        mode (Union[Unset, NewAmqpTriggerMode]): job trigger mode
        error_handler_path (Union[Unset, str]): Path to a script to run when the triggered job fails. A bare path,
            without the script/ or flow/ prefix a schedule error handler takes; it cannot be a flow.
        error_handler_args (Union[Unset, NewAmqpTriggerErrorHandlerArgs]): The arguments to pass to the script or flow
        retry (Union[Unset, NewAmqpTriggerRetry]): Retry configuration for failed module executions
        permissioned_as (Union[Unset, str]): The user or group this trigger runs as. Used during deployment to preserve
            the original trigger owner.
        preserve_permissioned_as (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group,
            preserves the original permissioned_as value instead of overwriting it.
        labels (Union[Unset, List[str]]):
    """

    amqp_resource_path: str
    queue_name: str
    path: str
    script_path: str
    is_flow: bool
    exchange: Union[Unset, None, "NewAmqpTriggerExchange"] = UNSET
    options: Union[Unset, None, "NewAmqpTriggerOptions"] = UNSET
    mode: Union[Unset, NewAmqpTriggerMode] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "NewAmqpTriggerErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "NewAmqpTriggerRetry"] = UNSET
    permissioned_as: Union[Unset, str] = UNSET
    preserve_permissioned_as: Union[Unset, bool] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        amqp_resource_path = self.amqp_resource_path
        queue_name = self.queue_name
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        exchange: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.exchange, Unset):
            exchange = self.exchange.to_dict() if self.exchange else None

        options: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict() if self.options else None

        mode: Union[Unset, str] = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        permissioned_as = self.permissioned_as
        preserve_permissioned_as = self.preserve_permissioned_as
        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amqp_resource_path": amqp_resource_path,
                "queue_name": queue_name,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
            }
        )
        if exchange is not UNSET:
            field_dict["exchange"] = exchange
        if options is not UNSET:
            field_dict["options"] = options
        if mode is not UNSET:
            field_dict["mode"] = mode
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
        if labels is not UNSET:
            field_dict["labels"] = labels

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_amqp_trigger_error_handler_args import NewAmqpTriggerErrorHandlerArgs
        from ..models.new_amqp_trigger_exchange import NewAmqpTriggerExchange
        from ..models.new_amqp_trigger_options import NewAmqpTriggerOptions
        from ..models.new_amqp_trigger_retry import NewAmqpTriggerRetry

        d = src_dict.copy()
        amqp_resource_path = d.pop("amqp_resource_path")

        queue_name = d.pop("queue_name")

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        _exchange = d.pop("exchange", UNSET)
        exchange: Union[Unset, None, NewAmqpTriggerExchange]
        if _exchange is None:
            exchange = None
        elif isinstance(_exchange, Unset):
            exchange = UNSET
        else:
            exchange = NewAmqpTriggerExchange.from_dict(_exchange)

        _options = d.pop("options", UNSET)
        options: Union[Unset, None, NewAmqpTriggerOptions]
        if _options is None:
            options = None
        elif isinstance(_options, Unset):
            options = UNSET
        else:
            options = NewAmqpTriggerOptions.from_dict(_options)

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, NewAmqpTriggerMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = NewAmqpTriggerMode(_mode)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, NewAmqpTriggerErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = NewAmqpTriggerErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, NewAmqpTriggerRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = NewAmqpTriggerRetry.from_dict(_retry)

        permissioned_as = d.pop("permissioned_as", UNSET)

        preserve_permissioned_as = d.pop("preserve_permissioned_as", UNSET)

        labels = cast(List[str], d.pop("labels", UNSET))

        new_amqp_trigger = cls(
            amqp_resource_path=amqp_resource_path,
            queue_name=queue_name,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            exchange=exchange,
            options=options,
            mode=mode,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            permissioned_as=permissioned_as,
            preserve_permissioned_as=preserve_permissioned_as,
            labels=labels,
        )

        new_amqp_trigger.additional_properties = d
        return new_amqp_trigger

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
