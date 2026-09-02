from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_script_by_hash_inline_json_body_args import RunScriptByHashInlineJsonBodyArgs


T = TypeVar("T", bound="RunScriptByHashInlineJsonBody")


@_attrs_define
class RunScriptByHashInlineJsonBody:
    """
    Attributes:
        args (Union[Unset, RunScriptByHashInlineJsonBodyArgs]): The arguments to pass to the script or flow
    """

    args: Union[Unset, "RunScriptByHashInlineJsonBodyArgs"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if args is not UNSET:
            field_dict["args"] = args

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_script_by_hash_inline_json_body_args import RunScriptByHashInlineJsonBodyArgs

        d = src_dict.copy()
        _args = d.pop("args", UNSET)
        args: Union[Unset, RunScriptByHashInlineJsonBodyArgs]
        if isinstance(_args, Unset):
            args = UNSET
        else:
            args = RunScriptByHashInlineJsonBodyArgs.from_dict(_args)

        run_script_by_hash_inline_json_body = cls(
            args=args,
        )

        run_script_by_hash_inline_json_body.additional_properties = d
        return run_script_by_hash_inline_json_body

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
