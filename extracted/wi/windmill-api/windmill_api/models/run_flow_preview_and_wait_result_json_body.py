from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_flow_preview_and_wait_result_json_body_args import RunFlowPreviewAndWaitResultJsonBodyArgs
    from ..models.run_flow_preview_and_wait_result_json_body_restarted_from import (
        RunFlowPreviewAndWaitResultJsonBodyRestartedFrom,
    )
    from ..models.run_flow_preview_and_wait_result_json_body_value import RunFlowPreviewAndWaitResultJsonBodyValue


T = TypeVar("T", bound="RunFlowPreviewAndWaitResultJsonBody")


@_attrs_define
class RunFlowPreviewAndWaitResultJsonBody:
    """
    Attributes:
        value (RunFlowPreviewAndWaitResultJsonBodyValue):
        args (RunFlowPreviewAndWaitResultJsonBodyArgs): The arguments to pass to the script or flow
        path (Union[Unset, str]):
        tag (Union[Unset, str]):
        restarted_from (Union[Unset, RunFlowPreviewAndWaitResultJsonBodyRestartedFrom]):
    """

    value: "RunFlowPreviewAndWaitResultJsonBodyValue"
    args: "RunFlowPreviewAndWaitResultJsonBodyArgs"
    path: Union[Unset, str] = UNSET
    tag: Union[Unset, str] = UNSET
    restarted_from: Union[Unset, "RunFlowPreviewAndWaitResultJsonBodyRestartedFrom"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value.to_dict()

        args = self.args.to_dict()

        path = self.path
        tag = self.tag
        restarted_from: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.restarted_from, Unset):
            restarted_from = self.restarted_from.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "args": args,
            }
        )
        if path is not UNSET:
            field_dict["path"] = path
        if tag is not UNSET:
            field_dict["tag"] = tag
        if restarted_from is not UNSET:
            field_dict["restarted_from"] = restarted_from

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_flow_preview_and_wait_result_json_body_args import RunFlowPreviewAndWaitResultJsonBodyArgs
        from ..models.run_flow_preview_and_wait_result_json_body_restarted_from import (
            RunFlowPreviewAndWaitResultJsonBodyRestartedFrom,
        )
        from ..models.run_flow_preview_and_wait_result_json_body_value import RunFlowPreviewAndWaitResultJsonBodyValue

        d = src_dict.copy()
        value = RunFlowPreviewAndWaitResultJsonBodyValue.from_dict(d.pop("value"))

        args = RunFlowPreviewAndWaitResultJsonBodyArgs.from_dict(d.pop("args"))

        path = d.pop("path", UNSET)

        tag = d.pop("tag", UNSET)

        _restarted_from = d.pop("restarted_from", UNSET)
        restarted_from: Union[Unset, RunFlowPreviewAndWaitResultJsonBodyRestartedFrom]
        if isinstance(_restarted_from, Unset):
            restarted_from = UNSET
        else:
            restarted_from = RunFlowPreviewAndWaitResultJsonBodyRestartedFrom.from_dict(_restarted_from)

        run_flow_preview_and_wait_result_json_body = cls(
            value=value,
            args=args,
            path=path,
            tag=tag,
            restarted_from=restarted_from,
        )

        run_flow_preview_and_wait_result_json_body.additional_properties = d
        return run_flow_preview_and_wait_result_json_body

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
