from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_flow_preview_and_wait_result_json_body_args import RunFlowPreviewAndWaitResultJsonBodyArgs
    from ..models.run_flow_preview_and_wait_result_json_body_temp_script_refs import (
        RunFlowPreviewAndWaitResultJsonBodyTempScriptRefs,
    )
    from ..models.run_flow_preview_and_wait_result_json_body_value import RunFlowPreviewAndWaitResultJsonBodyValue


T = TypeVar("T", bound="RunFlowPreviewAndWaitResultJsonBody")


@_attrs_define
class RunFlowPreviewAndWaitResultJsonBody:
    """
    Attributes:
        value (RunFlowPreviewAndWaitResultJsonBodyValue): The flow structure containing modules and optional
            preprocessor/failure handlers
        args (RunFlowPreviewAndWaitResultJsonBodyArgs): The arguments to pass to the script or flow
        path (Union[Unset, str]):
        tag (Union[Unset, str]):
        restarted_from (Union[Unset, Any]):
        temp_script_refs (Union[Unset, None, RunFlowPreviewAndWaitResultJsonBodyTempScriptRefs]): Map of relative-import
            script path -> temp storage hash, propagated to each flow step so inline-script relative imports resolve from
            not-yet-deployed local content instead of the deployed script
    """

    value: "RunFlowPreviewAndWaitResultJsonBodyValue"
    args: "RunFlowPreviewAndWaitResultJsonBodyArgs"
    path: Union[Unset, str] = UNSET
    tag: Union[Unset, str] = UNSET
    restarted_from: Union[Unset, Any] = UNSET
    temp_script_refs: Union[Unset, None, "RunFlowPreviewAndWaitResultJsonBodyTempScriptRefs"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value.to_dict()

        args = self.args.to_dict()

        path = self.path
        tag = self.tag
        restarted_from = self.restarted_from
        temp_script_refs: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.temp_script_refs, Unset):
            temp_script_refs = self.temp_script_refs.to_dict() if self.temp_script_refs else None

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
        if temp_script_refs is not UNSET:
            field_dict["temp_script_refs"] = temp_script_refs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_flow_preview_and_wait_result_json_body_args import RunFlowPreviewAndWaitResultJsonBodyArgs
        from ..models.run_flow_preview_and_wait_result_json_body_temp_script_refs import (
            RunFlowPreviewAndWaitResultJsonBodyTempScriptRefs,
        )
        from ..models.run_flow_preview_and_wait_result_json_body_value import RunFlowPreviewAndWaitResultJsonBodyValue

        d = src_dict.copy()
        value = RunFlowPreviewAndWaitResultJsonBodyValue.from_dict(d.pop("value"))

        args = RunFlowPreviewAndWaitResultJsonBodyArgs.from_dict(d.pop("args"))

        path = d.pop("path", UNSET)

        tag = d.pop("tag", UNSET)

        restarted_from = d.pop("restarted_from", UNSET)

        _temp_script_refs = d.pop("temp_script_refs", UNSET)
        temp_script_refs: Union[Unset, None, RunFlowPreviewAndWaitResultJsonBodyTempScriptRefs]
        if _temp_script_refs is None:
            temp_script_refs = None
        elif isinstance(_temp_script_refs, Unset):
            temp_script_refs = UNSET
        else:
            temp_script_refs = RunFlowPreviewAndWaitResultJsonBodyTempScriptRefs.from_dict(_temp_script_refs)

        run_flow_preview_and_wait_result_json_body = cls(
            value=value,
            args=args,
            path=path,
            tag=tag,
            restarted_from=restarted_from,
            temp_script_refs=temp_script_refs,
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
