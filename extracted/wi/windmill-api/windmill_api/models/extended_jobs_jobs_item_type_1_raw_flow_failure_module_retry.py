from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.extended_jobs_jobs_item_type_1_raw_flow_failure_module_retry_constant import (
        ExtendedJobsJobsItemType1RawFlowFailureModuleRetryConstant,
    )
    from ..models.extended_jobs_jobs_item_type_1_raw_flow_failure_module_retry_exponential import (
        ExtendedJobsJobsItemType1RawFlowFailureModuleRetryExponential,
    )
    from ..models.extended_jobs_jobs_item_type_1_raw_flow_failure_module_retry_retry_if import (
        ExtendedJobsJobsItemType1RawFlowFailureModuleRetryRetryIf,
    )


T = TypeVar("T", bound="ExtendedJobsJobsItemType1RawFlowFailureModuleRetry")


@_attrs_define
class ExtendedJobsJobsItemType1RawFlowFailureModuleRetry:
    """
    Attributes:
        constant (Union[Unset, ExtendedJobsJobsItemType1RawFlowFailureModuleRetryConstant]):
        exponential (Union[Unset, ExtendedJobsJobsItemType1RawFlowFailureModuleRetryExponential]):
        retry_if (Union[Unset, ExtendedJobsJobsItemType1RawFlowFailureModuleRetryRetryIf]):
    """

    constant: Union[Unset, "ExtendedJobsJobsItemType1RawFlowFailureModuleRetryConstant"] = UNSET
    exponential: Union[Unset, "ExtendedJobsJobsItemType1RawFlowFailureModuleRetryExponential"] = UNSET
    retry_if: Union[Unset, "ExtendedJobsJobsItemType1RawFlowFailureModuleRetryRetryIf"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        constant: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.constant, Unset):
            constant = self.constant.to_dict()

        exponential: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.exponential, Unset):
            exponential = self.exponential.to_dict()

        retry_if: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry_if, Unset):
            retry_if = self.retry_if.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if constant is not UNSET:
            field_dict["constant"] = constant
        if exponential is not UNSET:
            field_dict["exponential"] = exponential
        if retry_if is not UNSET:
            field_dict["retry_if"] = retry_if

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.extended_jobs_jobs_item_type_1_raw_flow_failure_module_retry_constant import (
            ExtendedJobsJobsItemType1RawFlowFailureModuleRetryConstant,
        )
        from ..models.extended_jobs_jobs_item_type_1_raw_flow_failure_module_retry_exponential import (
            ExtendedJobsJobsItemType1RawFlowFailureModuleRetryExponential,
        )
        from ..models.extended_jobs_jobs_item_type_1_raw_flow_failure_module_retry_retry_if import (
            ExtendedJobsJobsItemType1RawFlowFailureModuleRetryRetryIf,
        )

        d = src_dict.copy()
        _constant = d.pop("constant", UNSET)
        constant: Union[Unset, ExtendedJobsJobsItemType1RawFlowFailureModuleRetryConstant]
        if isinstance(_constant, Unset):
            constant = UNSET
        else:
            constant = ExtendedJobsJobsItemType1RawFlowFailureModuleRetryConstant.from_dict(_constant)

        _exponential = d.pop("exponential", UNSET)
        exponential: Union[Unset, ExtendedJobsJobsItemType1RawFlowFailureModuleRetryExponential]
        if isinstance(_exponential, Unset):
            exponential = UNSET
        else:
            exponential = ExtendedJobsJobsItemType1RawFlowFailureModuleRetryExponential.from_dict(_exponential)

        _retry_if = d.pop("retry_if", UNSET)
        retry_if: Union[Unset, ExtendedJobsJobsItemType1RawFlowFailureModuleRetryRetryIf]
        if isinstance(_retry_if, Unset):
            retry_if = UNSET
        else:
            retry_if = ExtendedJobsJobsItemType1RawFlowFailureModuleRetryRetryIf.from_dict(_retry_if)

        extended_jobs_jobs_item_type_1_raw_flow_failure_module_retry = cls(
            constant=constant,
            exponential=exponential,
            retry_if=retry_if,
        )

        extended_jobs_jobs_item_type_1_raw_flow_failure_module_retry.additional_properties = d
        return extended_jobs_jobs_item_type_1_raw_flow_failure_module_retry

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
