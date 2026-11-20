from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_extended_jobs_response_200_jobs_item_type_0_flow_status_continued_on_error_item import (
        ListExtendedJobsResponse200JobsItemType0FlowStatusContinuedOnErrorItem,
    )
    from ..models.list_extended_jobs_response_200_jobs_item_type_0_flow_status_failure_module import (
        ListExtendedJobsResponse200JobsItemType0FlowStatusFailureModule,
    )
    from ..models.list_extended_jobs_response_200_jobs_item_type_0_flow_status_modules_item import (
        ListExtendedJobsResponse200JobsItemType0FlowStatusModulesItem,
    )
    from ..models.list_extended_jobs_response_200_jobs_item_type_0_flow_status_preprocessor_module import (
        ListExtendedJobsResponse200JobsItemType0FlowStatusPreprocessorModule,
    )
    from ..models.list_extended_jobs_response_200_jobs_item_type_0_flow_status_retry import (
        ListExtendedJobsResponse200JobsItemType0FlowStatusRetry,
    )
    from ..models.list_extended_jobs_response_200_jobs_item_type_0_flow_status_test_subflows import (
        ListExtendedJobsResponse200JobsItemType0FlowStatusTestSubflows,
    )


T = TypeVar("T", bound="ListExtendedJobsResponse200JobsItemType0FlowStatus")


@_attrs_define
class ListExtendedJobsResponse200JobsItemType0FlowStatus:
    """
    Attributes:
        step (int):
        modules (List['ListExtendedJobsResponse200JobsItemType0FlowStatusModulesItem']):
        failure_module (ListExtendedJobsResponse200JobsItemType0FlowStatusFailureModule):
        user_states (Union[Unset, Any]):
        preprocessor_module (Union[Unset, ListExtendedJobsResponse200JobsItemType0FlowStatusPreprocessorModule]):
        retry (Union[Unset, ListExtendedJobsResponse200JobsItemType0FlowStatusRetry]):
        continued_on_error (Union[Unset,
            List['ListExtendedJobsResponse200JobsItemType0FlowStatusContinuedOnErrorItem']]): On a root flow, the steps at
            any depth that failed and that the flow went past because of continue_on_error (at most 100).
        test_subflows (Union[Unset, ListExtendedJobsResponse200JobsItemType0FlowStatusTestSubflows]): In a flow test
            run, deployed subflow path -> the flow value with the test's step overrides applied, run in place of the
            deployed subflow.
    """

    step: int
    modules: List["ListExtendedJobsResponse200JobsItemType0FlowStatusModulesItem"]
    failure_module: "ListExtendedJobsResponse200JobsItemType0FlowStatusFailureModule"
    user_states: Union[Unset, Any] = UNSET
    preprocessor_module: Union[Unset, "ListExtendedJobsResponse200JobsItemType0FlowStatusPreprocessorModule"] = UNSET
    retry: Union[Unset, "ListExtendedJobsResponse200JobsItemType0FlowStatusRetry"] = UNSET
    continued_on_error: Union[
        Unset, List["ListExtendedJobsResponse200JobsItemType0FlowStatusContinuedOnErrorItem"]
    ] = UNSET
    test_subflows: Union[Unset, "ListExtendedJobsResponse200JobsItemType0FlowStatusTestSubflows"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        step = self.step
        modules = []
        for modules_item_data in self.modules:
            modules_item = modules_item_data.to_dict()

            modules.append(modules_item)

        failure_module = self.failure_module.to_dict()

        user_states = self.user_states
        preprocessor_module: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.preprocessor_module, Unset):
            preprocessor_module = self.preprocessor_module.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        continued_on_error: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.continued_on_error, Unset):
            continued_on_error = []
            for continued_on_error_item_data in self.continued_on_error:
                continued_on_error_item = continued_on_error_item_data.to_dict()

                continued_on_error.append(continued_on_error_item)

        test_subflows: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.test_subflows, Unset):
            test_subflows = self.test_subflows.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "step": step,
                "modules": modules,
                "failure_module": failure_module,
            }
        )
        if user_states is not UNSET:
            field_dict["user_states"] = user_states
        if preprocessor_module is not UNSET:
            field_dict["preprocessor_module"] = preprocessor_module
        if retry is not UNSET:
            field_dict["retry"] = retry
        if continued_on_error is not UNSET:
            field_dict["continued_on_error"] = continued_on_error
        if test_subflows is not UNSET:
            field_dict["test_subflows"] = test_subflows

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_extended_jobs_response_200_jobs_item_type_0_flow_status_continued_on_error_item import (
            ListExtendedJobsResponse200JobsItemType0FlowStatusContinuedOnErrorItem,
        )
        from ..models.list_extended_jobs_response_200_jobs_item_type_0_flow_status_failure_module import (
            ListExtendedJobsResponse200JobsItemType0FlowStatusFailureModule,
        )
        from ..models.list_extended_jobs_response_200_jobs_item_type_0_flow_status_modules_item import (
            ListExtendedJobsResponse200JobsItemType0FlowStatusModulesItem,
        )
        from ..models.list_extended_jobs_response_200_jobs_item_type_0_flow_status_preprocessor_module import (
            ListExtendedJobsResponse200JobsItemType0FlowStatusPreprocessorModule,
        )
        from ..models.list_extended_jobs_response_200_jobs_item_type_0_flow_status_retry import (
            ListExtendedJobsResponse200JobsItemType0FlowStatusRetry,
        )
        from ..models.list_extended_jobs_response_200_jobs_item_type_0_flow_status_test_subflows import (
            ListExtendedJobsResponse200JobsItemType0FlowStatusTestSubflows,
        )

        d = src_dict.copy()
        step = d.pop("step")

        modules = []
        _modules = d.pop("modules")
        for modules_item_data in _modules:
            modules_item = ListExtendedJobsResponse200JobsItemType0FlowStatusModulesItem.from_dict(modules_item_data)

            modules.append(modules_item)

        failure_module = ListExtendedJobsResponse200JobsItemType0FlowStatusFailureModule.from_dict(
            d.pop("failure_module")
        )

        user_states = d.pop("user_states", UNSET)

        _preprocessor_module = d.pop("preprocessor_module", UNSET)
        preprocessor_module: Union[Unset, ListExtendedJobsResponse200JobsItemType0FlowStatusPreprocessorModule]
        if isinstance(_preprocessor_module, Unset):
            preprocessor_module = UNSET
        else:
            preprocessor_module = ListExtendedJobsResponse200JobsItemType0FlowStatusPreprocessorModule.from_dict(
                _preprocessor_module
            )

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, ListExtendedJobsResponse200JobsItemType0FlowStatusRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = ListExtendedJobsResponse200JobsItemType0FlowStatusRetry.from_dict(_retry)

        continued_on_error = []
        _continued_on_error = d.pop("continued_on_error", UNSET)
        for continued_on_error_item_data in _continued_on_error or []:
            continued_on_error_item = ListExtendedJobsResponse200JobsItemType0FlowStatusContinuedOnErrorItem.from_dict(
                continued_on_error_item_data
            )

            continued_on_error.append(continued_on_error_item)

        _test_subflows = d.pop("test_subflows", UNSET)
        test_subflows: Union[Unset, ListExtendedJobsResponse200JobsItemType0FlowStatusTestSubflows]
        if isinstance(_test_subflows, Unset):
            test_subflows = UNSET
        else:
            test_subflows = ListExtendedJobsResponse200JobsItemType0FlowStatusTestSubflows.from_dict(_test_subflows)

        list_extended_jobs_response_200_jobs_item_type_0_flow_status = cls(
            step=step,
            modules=modules,
            failure_module=failure_module,
            user_states=user_states,
            preprocessor_module=preprocessor_module,
            retry=retry,
            continued_on_error=continued_on_error,
            test_subflows=test_subflows,
        )

        list_extended_jobs_response_200_jobs_item_type_0_flow_status.additional_properties = d
        return list_extended_jobs_response_200_jobs_item_type_0_flow_status

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
