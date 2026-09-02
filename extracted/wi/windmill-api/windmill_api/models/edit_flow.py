from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_flow_schema import EditFlowSchema
    from ..models.edit_flow_value import EditFlowValue


T = TypeVar("T", bound="EditFlow")


@_attrs_define
class EditFlow:
    """
    Attributes:
        summary (str): Short description of what this flow does
        value (EditFlowValue): The flow structure containing modules and optional preprocessor/failure handlers
        description (Union[Unset, str]): Detailed documentation for this flow
        schema (Union[Unset, EditFlowSchema]): JSON Schema for flow inputs. Use this to define input parameters, their
            types, defaults, and validation. For resource inputs, set type to 'object' and format to 'resource-<type>'
            (e.g., 'resource-stripe')
        on_behalf_of_email (Union[Unset, str]):
        on_behalf_of (Union[Unset, str]): Authorization identity to run as: u/{username}, g/{group}, or a bare email
            when the username is itself email-shaped. Supply this or on_behalf_of_email; when only the address is given it
            is resolved to the account it names, and an address naming nobody is rejected. A pair that disagrees is
            rejected.
        path (Union[Unset, str]):
        tag (Union[Unset, str]):
        ws_error_handler_muted (Union[Unset, bool]):
        priority (Union[Unset, int]):
        dedicated_worker (Union[Unset, bool]):
        timeout (Union[Unset, float]):
        visible_to_runner_only (Union[Unset, bool]):
        preserve_on_behalf_of (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group,
            preserves the original on_behalf_of_email / on_behalf_of pair instead of overwriting it with the caller's own
            identity.
        labels (Union[Unset, List[str]]):
    """

    summary: str
    value: "EditFlowValue"
    description: Union[Unset, str] = UNSET
    schema: Union[Unset, "EditFlowSchema"] = UNSET
    on_behalf_of_email: Union[Unset, str] = UNSET
    on_behalf_of: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    tag: Union[Unset, str] = UNSET
    ws_error_handler_muted: Union[Unset, bool] = UNSET
    priority: Union[Unset, int] = UNSET
    dedicated_worker: Union[Unset, bool] = UNSET
    timeout: Union[Unset, float] = UNSET
    visible_to_runner_only: Union[Unset, bool] = UNSET
    preserve_on_behalf_of: Union[Unset, bool] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        summary = self.summary
        value = self.value.to_dict()

        description = self.description
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        on_behalf_of_email = self.on_behalf_of_email
        on_behalf_of = self.on_behalf_of
        path = self.path
        tag = self.tag
        ws_error_handler_muted = self.ws_error_handler_muted
        priority = self.priority
        dedicated_worker = self.dedicated_worker
        timeout = self.timeout
        visible_to_runner_only = self.visible_to_runner_only
        preserve_on_behalf_of = self.preserve_on_behalf_of
        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "summary": summary,
                "value": value,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if schema is not UNSET:
            field_dict["schema"] = schema
        if on_behalf_of_email is not UNSET:
            field_dict["on_behalf_of_email"] = on_behalf_of_email
        if on_behalf_of is not UNSET:
            field_dict["on_behalf_of"] = on_behalf_of
        if path is not UNSET:
            field_dict["path"] = path
        if tag is not UNSET:
            field_dict["tag"] = tag
        if ws_error_handler_muted is not UNSET:
            field_dict["ws_error_handler_muted"] = ws_error_handler_muted
        if priority is not UNSET:
            field_dict["priority"] = priority
        if dedicated_worker is not UNSET:
            field_dict["dedicated_worker"] = dedicated_worker
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if visible_to_runner_only is not UNSET:
            field_dict["visible_to_runner_only"] = visible_to_runner_only
        if preserve_on_behalf_of is not UNSET:
            field_dict["preserve_on_behalf_of"] = preserve_on_behalf_of
        if labels is not UNSET:
            field_dict["labels"] = labels

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_flow_schema import EditFlowSchema
        from ..models.edit_flow_value import EditFlowValue

        d = src_dict.copy()
        summary = d.pop("summary")

        value = EditFlowValue.from_dict(d.pop("value"))

        description = d.pop("description", UNSET)

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, EditFlowSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = EditFlowSchema.from_dict(_schema)

        on_behalf_of_email = d.pop("on_behalf_of_email", UNSET)

        on_behalf_of = d.pop("on_behalf_of", UNSET)

        path = d.pop("path", UNSET)

        tag = d.pop("tag", UNSET)

        ws_error_handler_muted = d.pop("ws_error_handler_muted", UNSET)

        priority = d.pop("priority", UNSET)

        dedicated_worker = d.pop("dedicated_worker", UNSET)

        timeout = d.pop("timeout", UNSET)

        visible_to_runner_only = d.pop("visible_to_runner_only", UNSET)

        preserve_on_behalf_of = d.pop("preserve_on_behalf_of", UNSET)

        labels = cast(List[str], d.pop("labels", UNSET))

        edit_flow = cls(
            summary=summary,
            value=value,
            description=description,
            schema=schema,
            on_behalf_of_email=on_behalf_of_email,
            on_behalf_of=on_behalf_of,
            path=path,
            tag=tag,
            ws_error_handler_muted=ws_error_handler_muted,
            priority=priority,
            dedicated_worker=dedicated_worker,
            timeout=timeout,
            visible_to_runner_only=visible_to_runner_only,
            preserve_on_behalf_of=preserve_on_behalf_of,
            labels=labels,
        )

        edit_flow.additional_properties = d
        return edit_flow

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
