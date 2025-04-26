from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.open_flow_w_path_schema import OpenFlowWPathSchema
    from ..models.open_flow_w_path_value import OpenFlowWPathValue


T = TypeVar("T", bound="OpenFlowWPath")


@_attrs_define
class OpenFlowWPath:
    """
    Attributes:
        summary (str):
        value (OpenFlowWPathValue):
        path (str):
        description (Union[Unset, str]):
        schema (Union[Unset, OpenFlowWPathSchema]):
        tag (Union[Unset, str]):
        ws_error_handler_muted (Union[Unset, bool]):
        priority (Union[Unset, int]):
        dedicated_worker (Union[Unset, bool]):
        timeout (Union[Unset, float]):
        visible_to_runner_only (Union[Unset, bool]):
        on_behalf_of_email (Union[Unset, str]):
    """

    summary: str
    value: "OpenFlowWPathValue"
    path: str
    description: Union[Unset, str] = UNSET
    schema: Union[Unset, "OpenFlowWPathSchema"] = UNSET
    tag: Union[Unset, str] = UNSET
    ws_error_handler_muted: Union[Unset, bool] = UNSET
    priority: Union[Unset, int] = UNSET
    dedicated_worker: Union[Unset, bool] = UNSET
    timeout: Union[Unset, float] = UNSET
    visible_to_runner_only: Union[Unset, bool] = UNSET
    on_behalf_of_email: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        summary = self.summary
        value = self.value.to_dict()

        path = self.path
        description = self.description
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        tag = self.tag
        ws_error_handler_muted = self.ws_error_handler_muted
        priority = self.priority
        dedicated_worker = self.dedicated_worker
        timeout = self.timeout
        visible_to_runner_only = self.visible_to_runner_only
        on_behalf_of_email = self.on_behalf_of_email

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "summary": summary,
                "value": value,
                "path": path,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if schema is not UNSET:
            field_dict["schema"] = schema
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
        if on_behalf_of_email is not UNSET:
            field_dict["on_behalf_of_email"] = on_behalf_of_email

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.open_flow_w_path_schema import OpenFlowWPathSchema
        from ..models.open_flow_w_path_value import OpenFlowWPathValue

        d = src_dict.copy()
        summary = d.pop("summary")

        value = OpenFlowWPathValue.from_dict(d.pop("value"))

        path = d.pop("path")

        description = d.pop("description", UNSET)

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, OpenFlowWPathSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = OpenFlowWPathSchema.from_dict(_schema)

        tag = d.pop("tag", UNSET)

        ws_error_handler_muted = d.pop("ws_error_handler_muted", UNSET)

        priority = d.pop("priority", UNSET)

        dedicated_worker = d.pop("dedicated_worker", UNSET)

        timeout = d.pop("timeout", UNSET)

        visible_to_runner_only = d.pop("visible_to_runner_only", UNSET)

        on_behalf_of_email = d.pop("on_behalf_of_email", UNSET)

        open_flow_w_path = cls(
            summary=summary,
            value=value,
            path=path,
            description=description,
            schema=schema,
            tag=tag,
            ws_error_handler_muted=ws_error_handler_muted,
            priority=priority,
            dedicated_worker=dedicated_worker,
            timeout=timeout,
            visible_to_runner_only=visible_to_runner_only,
            on_behalf_of_email=on_behalf_of_email,
        )

        open_flow_w_path.additional_properties = d
        return open_flow_w_path

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
