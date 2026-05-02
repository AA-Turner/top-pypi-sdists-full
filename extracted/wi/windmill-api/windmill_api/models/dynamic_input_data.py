from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dynamic_input_data_args import DynamicInputDataArgs
    from ..models.dynamic_input_data_runnable_ref_type_0 import DynamicInputDataRunnableRefType0
    from ..models.dynamic_input_data_runnable_ref_type_1 import DynamicInputDataRunnableRefType1


T = TypeVar("T", bound="DynamicInputData")


@_attrs_define
class DynamicInputData:
    """
    Attributes:
        entrypoint_function (str): Name of the function to execute for dynamic select
        runnable_ref (Union['DynamicInputDataRunnableRefType0', 'DynamicInputDataRunnableRefType1']):
        args (Union[Unset, DynamicInputDataArgs]): Arguments to pass to the function
    """

    entrypoint_function: str
    runnable_ref: Union["DynamicInputDataRunnableRefType0", "DynamicInputDataRunnableRefType1"]
    args: Union[Unset, "DynamicInputDataArgs"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.dynamic_input_data_runnable_ref_type_0 import DynamicInputDataRunnableRefType0

        entrypoint_function = self.entrypoint_function
        runnable_ref: Dict[str, Any]

        if isinstance(self.runnable_ref, DynamicInputDataRunnableRefType0):
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
        from ..models.dynamic_input_data_args import DynamicInputDataArgs
        from ..models.dynamic_input_data_runnable_ref_type_0 import DynamicInputDataRunnableRefType0
        from ..models.dynamic_input_data_runnable_ref_type_1 import DynamicInputDataRunnableRefType1

        d = src_dict.copy()
        entrypoint_function = d.pop("entrypoint_function")

        def _parse_runnable_ref(
            data: object,
        ) -> Union["DynamicInputDataRunnableRefType0", "DynamicInputDataRunnableRefType1"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                runnable_ref_type_0 = DynamicInputDataRunnableRefType0.from_dict(data)

                return runnable_ref_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            runnable_ref_type_1 = DynamicInputDataRunnableRefType1.from_dict(data)

            return runnable_ref_type_1

        runnable_ref = _parse_runnable_ref(d.pop("runnable_ref"))

        _args = d.pop("args", UNSET)
        args: Union[Unset, DynamicInputDataArgs]
        if isinstance(_args, Unset):
            args = UNSET
        else:
            args = DynamicInputDataArgs.from_dict(_args)

        dynamic_input_data = cls(
            entrypoint_function=entrypoint_function,
            runnable_ref=runnable_ref,
            args=args,
        )

        dynamic_input_data.additional_properties = d
        return dynamic_input_data

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
