from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_jobs_response_200_item_type_0_raw_flow_modules_item_retry_constant import (
        ListJobsResponse200ItemType0RawFlowModulesItemRetryConstant,
    )
    from ..models.list_jobs_response_200_item_type_0_raw_flow_modules_item_retry_exponential import (
        ListJobsResponse200ItemType0RawFlowModulesItemRetryExponential,
    )
    from ..models.list_jobs_response_200_item_type_0_raw_flow_modules_item_retry_retry_if import (
        ListJobsResponse200ItemType0RawFlowModulesItemRetryRetryIf,
    )


T = TypeVar("T", bound="ListJobsResponse200ItemType0RawFlowModulesItemRetry")


@_attrs_define
class ListJobsResponse200ItemType0RawFlowModulesItemRetry:
    """
    Attributes:
        constant (Union[Unset, ListJobsResponse200ItemType0RawFlowModulesItemRetryConstant]):
        exponential (Union[Unset, ListJobsResponse200ItemType0RawFlowModulesItemRetryExponential]):
        retry_if (Union[Unset, ListJobsResponse200ItemType0RawFlowModulesItemRetryRetryIf]):
    """

    constant: Union[Unset, "ListJobsResponse200ItemType0RawFlowModulesItemRetryConstant"] = UNSET
    exponential: Union[Unset, "ListJobsResponse200ItemType0RawFlowModulesItemRetryExponential"] = UNSET
    retry_if: Union[Unset, "ListJobsResponse200ItemType0RawFlowModulesItemRetryRetryIf"] = UNSET
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
        from ..models.list_jobs_response_200_item_type_0_raw_flow_modules_item_retry_constant import (
            ListJobsResponse200ItemType0RawFlowModulesItemRetryConstant,
        )
        from ..models.list_jobs_response_200_item_type_0_raw_flow_modules_item_retry_exponential import (
            ListJobsResponse200ItemType0RawFlowModulesItemRetryExponential,
        )
        from ..models.list_jobs_response_200_item_type_0_raw_flow_modules_item_retry_retry_if import (
            ListJobsResponse200ItemType0RawFlowModulesItemRetryRetryIf,
        )

        d = src_dict.copy()
        _constant = d.pop("constant", UNSET)
        constant: Union[Unset, ListJobsResponse200ItemType0RawFlowModulesItemRetryConstant]
        if isinstance(_constant, Unset):
            constant = UNSET
        else:
            constant = ListJobsResponse200ItemType0RawFlowModulesItemRetryConstant.from_dict(_constant)

        _exponential = d.pop("exponential", UNSET)
        exponential: Union[Unset, ListJobsResponse200ItemType0RawFlowModulesItemRetryExponential]
        if isinstance(_exponential, Unset):
            exponential = UNSET
        else:
            exponential = ListJobsResponse200ItemType0RawFlowModulesItemRetryExponential.from_dict(_exponential)

        _retry_if = d.pop("retry_if", UNSET)
        retry_if: Union[Unset, ListJobsResponse200ItemType0RawFlowModulesItemRetryRetryIf]
        if isinstance(_retry_if, Unset):
            retry_if = UNSET
        else:
            retry_if = ListJobsResponse200ItemType0RawFlowModulesItemRetryRetryIf.from_dict(_retry_if)

        list_jobs_response_200_item_type_0_raw_flow_modules_item_retry = cls(
            constant=constant,
            exponential=exponential,
            retry_if=retry_if,
        )

        list_jobs_response_200_item_type_0_raw_flow_modules_item_retry.additional_properties = d
        return list_jobs_response_200_item_type_0_raw_flow_modules_item_retry

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
