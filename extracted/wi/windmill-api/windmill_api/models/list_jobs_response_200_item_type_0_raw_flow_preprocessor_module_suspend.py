from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_jobs_response_200_item_type_0_raw_flow_preprocessor_module_suspend_resume_form import (
        ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendResumeForm,
    )
    from ..models.list_jobs_response_200_item_type_0_raw_flow_preprocessor_module_suspend_user_groups_required_type_0 import (
        ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType0,
    )
    from ..models.list_jobs_response_200_item_type_0_raw_flow_preprocessor_module_suspend_user_groups_required_type_1 import (
        ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType1,
    )


T = TypeVar("T", bound="ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspend")


@_attrs_define
class ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspend:
    """
    Attributes:
        required_events (Union[Unset, int]):
        timeout (Union[Unset, int]):
        resume_form (Union[Unset, ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendResumeForm]):
        user_auth_required (Union[Unset, bool]):
        user_groups_required
            (Union['ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType0',
            'ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType1', Unset]):
        self_approval_disabled (Union[Unset, bool]):
        hide_cancel (Union[Unset, bool]):
        continue_on_disapprove_timeout (Union[Unset, bool]):
    """

    required_events: Union[Unset, int] = UNSET
    timeout: Union[Unset, int] = UNSET
    resume_form: Union[Unset, "ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendResumeForm"] = UNSET
    user_auth_required: Union[Unset, bool] = UNSET
    user_groups_required: Union[
        "ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType0",
        "ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType1",
        Unset,
    ] = UNSET
    self_approval_disabled: Union[Unset, bool] = UNSET
    hide_cancel: Union[Unset, bool] = UNSET
    continue_on_disapprove_timeout: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_jobs_response_200_item_type_0_raw_flow_preprocessor_module_suspend_user_groups_required_type_0 import (
            ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType0,
        )

        required_events = self.required_events
        timeout = self.timeout
        resume_form: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resume_form, Unset):
            resume_form = self.resume_form.to_dict()

        user_auth_required = self.user_auth_required
        user_groups_required: Union[Dict[str, Any], Unset]
        if isinstance(self.user_groups_required, Unset):
            user_groups_required = UNSET

        elif isinstance(
            self.user_groups_required,
            ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType0,
        ):
            user_groups_required = UNSET
            if not isinstance(self.user_groups_required, Unset):
                user_groups_required = self.user_groups_required.to_dict()

        else:
            user_groups_required = UNSET
            if not isinstance(self.user_groups_required, Unset):
                user_groups_required = self.user_groups_required.to_dict()

        self_approval_disabled = self.self_approval_disabled
        hide_cancel = self.hide_cancel
        continue_on_disapprove_timeout = self.continue_on_disapprove_timeout

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if required_events is not UNSET:
            field_dict["required_events"] = required_events
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if resume_form is not UNSET:
            field_dict["resume_form"] = resume_form
        if user_auth_required is not UNSET:
            field_dict["user_auth_required"] = user_auth_required
        if user_groups_required is not UNSET:
            field_dict["user_groups_required"] = user_groups_required
        if self_approval_disabled is not UNSET:
            field_dict["self_approval_disabled"] = self_approval_disabled
        if hide_cancel is not UNSET:
            field_dict["hide_cancel"] = hide_cancel
        if continue_on_disapprove_timeout is not UNSET:
            field_dict["continue_on_disapprove_timeout"] = continue_on_disapprove_timeout

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_jobs_response_200_item_type_0_raw_flow_preprocessor_module_suspend_resume_form import (
            ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendResumeForm,
        )
        from ..models.list_jobs_response_200_item_type_0_raw_flow_preprocessor_module_suspend_user_groups_required_type_0 import (
            ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType0,
        )
        from ..models.list_jobs_response_200_item_type_0_raw_flow_preprocessor_module_suspend_user_groups_required_type_1 import (
            ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType1,
        )

        d = src_dict.copy()
        required_events = d.pop("required_events", UNSET)

        timeout = d.pop("timeout", UNSET)

        _resume_form = d.pop("resume_form", UNSET)
        resume_form: Union[Unset, ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendResumeForm]
        if isinstance(_resume_form, Unset):
            resume_form = UNSET
        else:
            resume_form = ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendResumeForm.from_dict(_resume_form)

        user_auth_required = d.pop("user_auth_required", UNSET)

        def _parse_user_groups_required(
            data: object,
        ) -> Union[
            "ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType0",
            "ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType1",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _user_groups_required_type_0 = data
                user_groups_required_type_0: Union[
                    Unset, ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType0
                ]
                if isinstance(_user_groups_required_type_0, Unset):
                    user_groups_required_type_0 = UNSET
                else:
                    user_groups_required_type_0 = (
                        ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType0.from_dict(
                            _user_groups_required_type_0
                        )
                    )

                return user_groups_required_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _user_groups_required_type_1 = data
            user_groups_required_type_1: Union[
                Unset, ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType1
            ]
            if isinstance(_user_groups_required_type_1, Unset):
                user_groups_required_type_1 = UNSET
            else:
                user_groups_required_type_1 = (
                    ListJobsResponse200ItemType0RawFlowPreprocessorModuleSuspendUserGroupsRequiredType1.from_dict(
                        _user_groups_required_type_1
                    )
                )

            return user_groups_required_type_1

        user_groups_required = _parse_user_groups_required(d.pop("user_groups_required", UNSET))

        self_approval_disabled = d.pop("self_approval_disabled", UNSET)

        hide_cancel = d.pop("hide_cancel", UNSET)

        continue_on_disapprove_timeout = d.pop("continue_on_disapprove_timeout", UNSET)

        list_jobs_response_200_item_type_0_raw_flow_preprocessor_module_suspend = cls(
            required_events=required_events,
            timeout=timeout,
            resume_form=resume_form,
            user_auth_required=user_auth_required,
            user_groups_required=user_groups_required,
            self_approval_disabled=self_approval_disabled,
            hide_cancel=hide_cancel,
            continue_on_disapprove_timeout=continue_on_disapprove_timeout,
        )

        list_jobs_response_200_item_type_0_raw_flow_preprocessor_module_suspend.additional_properties = d
        return list_jobs_response_200_item_type_0_raw_flow_preprocessor_module_suspend

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
