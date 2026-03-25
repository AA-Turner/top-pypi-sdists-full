from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CompletedJobRawFlowPreprocessorModuleDebouncing")


@_attrs_define
class CompletedJobRawFlowPreprocessorModuleDebouncing:
    """Debounce configuration for this step (EE only)

    Attributes:
        debounce_delay_s (Union[Unset, int]): Delay in seconds to debounce this step's executions across flow runs
        debounce_key (Union[Unset, str]): Expression to group debounced executions. Supports $workspace and $args[name].
            Default: $workspace/flow/<flow_path>-<step_id>
        debounce_args_to_accumulate (Union[Unset, List[str]]): Array-type arguments to accumulate across debounced
            executions
        max_total_debouncing_time (Union[Unset, int]): Maximum total time in seconds before forced execution
        max_total_debounces_amount (Union[Unset, int]): Maximum number of debounces before forced execution
    """

    debounce_delay_s: Union[Unset, int] = UNSET
    debounce_key: Union[Unset, str] = UNSET
    debounce_args_to_accumulate: Union[Unset, List[str]] = UNSET
    max_total_debouncing_time: Union[Unset, int] = UNSET
    max_total_debounces_amount: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        debounce_delay_s = self.debounce_delay_s
        debounce_key = self.debounce_key
        debounce_args_to_accumulate: Union[Unset, List[str]] = UNSET
        if not isinstance(self.debounce_args_to_accumulate, Unset):
            debounce_args_to_accumulate = self.debounce_args_to_accumulate

        max_total_debouncing_time = self.max_total_debouncing_time
        max_total_debounces_amount = self.max_total_debounces_amount

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if debounce_delay_s is not UNSET:
            field_dict["debounce_delay_s"] = debounce_delay_s
        if debounce_key is not UNSET:
            field_dict["debounce_key"] = debounce_key
        if debounce_args_to_accumulate is not UNSET:
            field_dict["debounce_args_to_accumulate"] = debounce_args_to_accumulate
        if max_total_debouncing_time is not UNSET:
            field_dict["max_total_debouncing_time"] = max_total_debouncing_time
        if max_total_debounces_amount is not UNSET:
            field_dict["max_total_debounces_amount"] = max_total_debounces_amount

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        debounce_delay_s = d.pop("debounce_delay_s", UNSET)

        debounce_key = d.pop("debounce_key", UNSET)

        debounce_args_to_accumulate = cast(List[str], d.pop("debounce_args_to_accumulate", UNSET))

        max_total_debouncing_time = d.pop("max_total_debouncing_time", UNSET)

        max_total_debounces_amount = d.pop("max_total_debounces_amount", UNSET)

        completed_job_raw_flow_preprocessor_module_debouncing = cls(
            debounce_delay_s=debounce_delay_s,
            debounce_key=debounce_key,
            debounce_args_to_accumulate=debounce_args_to_accumulate,
            max_total_debouncing_time=max_total_debouncing_time,
            max_total_debounces_amount=max_total_debounces_amount,
        )

        completed_job_raw_flow_preprocessor_module_debouncing.additional_properties = d
        return completed_job_raw_flow_preprocessor_module_debouncing

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
