from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_dynamic_select_json_body_args import RunDynamicSelectJsonBodyArgs
    from ..models.run_dynamic_select_json_body_runnable_ref_type_0 import RunDynamicSelectJsonBodyRunnableRefType0
    from ..models.run_dynamic_select_json_body_runnable_ref_type_1 import RunDynamicSelectJsonBodyRunnableRefType1


T = TypeVar("T", bound="RunDynamicSelectJsonBody")


@_attrs_define
class RunDynamicSelectJsonBody:
    """
    Attributes:
        entrypoint_function (str): Name of the function to execute for dynamic select
        runnable_ref (Union['RunDynamicSelectJsonBodyRunnableRefType0', 'RunDynamicSelectJsonBodyRunnableRefType1']):
        args (Union[Unset, RunDynamicSelectJsonBodyArgs]): Arguments to pass to the function
    """

    entrypoint_function: str
    runnable_ref: Union["RunDynamicSelectJsonBodyRunnableRefType0", "RunDynamicSelectJsonBodyRunnableRefType1"]
    args: Union[Unset, "RunDynamicSelectJsonBodyArgs"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.run_dynamic_select_json_body_runnable_ref_type_0 import RunDynamicSelectJsonBodyRunnableRefType0

        entrypoint_function = self.entrypoint_function
        runnable_ref: Dict[str, Any]

        if isinstance(self.runnable_ref, RunDynamicSelectJsonBodyRunnableRefType0):
            runnable_ref = self.runnable_ref.to_dict()

        else:
            runnable_ref = self.runnable_ref.to_dict()

        args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entrypoint_function": entrypoint_function,
                "runnable_ref": runnable_ref,
            }
        )
        if args is not UNSET:
            field_dict["args"] = args

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_dynamic_select_json_body_args import RunDynamicSelectJsonBodyArgs
        from ..models.run_dynamic_select_json_body_runnable_ref_type_0 import RunDynamicSelectJsonBodyRunnableRefType0
        from ..models.run_dynamic_select_json_body_runnable_ref_type_1 import RunDynamicSelectJsonBodyRunnableRefType1

        d = src_dict.copy()
        entrypoint_function = d.pop("entrypoint_function")

        def _parse_runnable_ref(
            data: object,
        ) -> Union["RunDynamicSelectJsonBodyRunnableRefType0", "RunDynamicSelectJsonBodyRunnableRefType1"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                runnable_ref_type_0 = RunDynamicSelectJsonBodyRunnableRefType0.from_dict(data)

                return runnable_ref_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            runnable_ref_type_1 = RunDynamicSelectJsonBodyRunnableRefType1.from_dict(data)

            return runnable_ref_type_1

        runnable_ref = _parse_runnable_ref(d.pop("runnable_ref"))

        _args = d.pop("args", UNSET)
        args: Union[Unset, RunDynamicSelectJsonBodyArgs]
        if isinstance(_args, Unset):
            args = UNSET
        else:
            args = RunDynamicSelectJsonBodyArgs.from_dict(_args)

        run_dynamic_select_json_body = cls(
            entrypoint_function=entrypoint_function,
            runnable_ref=runnable_ref,
            args=args,
        )

        run_dynamic_select_json_body.additional_properties = d
        return run_dynamic_select_json_body

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
