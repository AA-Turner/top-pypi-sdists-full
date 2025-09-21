from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_type import (
    ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_agent_actions_item_type_0 import (
        ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType0,
    )
    from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_agent_actions_item_type_1 import (
        ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType1,
    )
    from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_approvers_item import (
        ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleApproversItem,
    )
    from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_branch_chosen import (
        ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleBranchChosen,
    )
    from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_branchall import (
        ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleBranchall,
    )
    from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_flow_jobs_duration import (
        ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleFlowJobsDuration,
    )
    from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_iterator import (
        ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleIterator,
    )


T = TypeVar("T", bound="ExtendedJobsJobsItemType1FlowStatusPreprocessorModule")


@_attrs_define
class ExtendedJobsJobsItemType1FlowStatusPreprocessorModule:
    """
    Attributes:
        type (ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleType):
        id (Union[Unset, str]):
        job (Union[Unset, str]):
        count (Union[Unset, int]):
        progress (Union[Unset, int]):
        iterator (Union[Unset, ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleIterator]):
        flow_jobs (Union[Unset, List[str]]):
        flow_jobs_success (Union[Unset, List[bool]]):
        flow_jobs_duration (Union[Unset, ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleFlowJobsDuration]):
        branch_chosen (Union[Unset, ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleBranchChosen]):
        branchall (Union[Unset, ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleBranchall]):
        approvers (Union[Unset, List['ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleApproversItem']]):
        failed_retries (Union[Unset, List[str]]):
        skipped (Union[Unset, bool]):
        agent_actions (Union[Unset,
            List[Union['ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType0',
            'ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType1']]]):
        agent_actions_success (Union[Unset, List[bool]]):
    """

    type: ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleType
    id: Union[Unset, str] = UNSET
    job: Union[Unset, str] = UNSET
    count: Union[Unset, int] = UNSET
    progress: Union[Unset, int] = UNSET
    iterator: Union[Unset, "ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleIterator"] = UNSET
    flow_jobs: Union[Unset, List[str]] = UNSET
    flow_jobs_success: Union[Unset, List[bool]] = UNSET
    flow_jobs_duration: Union[Unset, "ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleFlowJobsDuration"] = UNSET
    branch_chosen: Union[Unset, "ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleBranchChosen"] = UNSET
    branchall: Union[Unset, "ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleBranchall"] = UNSET
    approvers: Union[Unset, List["ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleApproversItem"]] = UNSET
    failed_retries: Union[Unset, List[str]] = UNSET
    skipped: Union[Unset, bool] = UNSET
    agent_actions: Union[
        Unset,
        List[
            Union[
                "ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType0",
                "ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType1",
            ]
        ],
    ] = UNSET
    agent_actions_success: Union[Unset, List[bool]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_agent_actions_item_type_0 import (
            ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType0,
        )

        type = self.type.value

        id = self.id
        job = self.job
        count = self.count
        progress = self.progress
        iterator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.iterator, Unset):
            iterator = self.iterator.to_dict()

        flow_jobs: Union[Unset, List[str]] = UNSET
        if not isinstance(self.flow_jobs, Unset):
            flow_jobs = self.flow_jobs

        flow_jobs_success: Union[Unset, List[bool]] = UNSET
        if not isinstance(self.flow_jobs_success, Unset):
            flow_jobs_success = self.flow_jobs_success

        flow_jobs_duration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flow_jobs_duration, Unset):
            flow_jobs_duration = self.flow_jobs_duration.to_dict()

        branch_chosen: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.branch_chosen, Unset):
            branch_chosen = self.branch_chosen.to_dict()

        branchall: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.branchall, Unset):
            branchall = self.branchall.to_dict()

        approvers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.approvers, Unset):
            approvers = []
            for approvers_item_data in self.approvers:
                approvers_item = approvers_item_data.to_dict()

                approvers.append(approvers_item)

        failed_retries: Union[Unset, List[str]] = UNSET
        if not isinstance(self.failed_retries, Unset):
            failed_retries = self.failed_retries

        skipped = self.skipped
        agent_actions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.agent_actions, Unset):
            agent_actions = []
            for agent_actions_item_data in self.agent_actions:
                agent_actions_item: Dict[str, Any]

                if isinstance(
                    agent_actions_item_data, ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType0
                ):
                    agent_actions_item = agent_actions_item_data.to_dict()

                else:
                    agent_actions_item = agent_actions_item_data.to_dict()

                agent_actions.append(agent_actions_item)

        agent_actions_success: Union[Unset, List[bool]] = UNSET
        if not isinstance(self.agent_actions_success, Unset):
            agent_actions_success = self.agent_actions_success

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if job is not UNSET:
            field_dict["job"] = job
        if count is not UNSET:
            field_dict["count"] = count
        if progress is not UNSET:
            field_dict["progress"] = progress
        if iterator is not UNSET:
            field_dict["iterator"] = iterator
        if flow_jobs is not UNSET:
            field_dict["flow_jobs"] = flow_jobs
        if flow_jobs_success is not UNSET:
            field_dict["flow_jobs_success"] = flow_jobs_success
        if flow_jobs_duration is not UNSET:
            field_dict["flow_jobs_duration"] = flow_jobs_duration
        if branch_chosen is not UNSET:
            field_dict["branch_chosen"] = branch_chosen
        if branchall is not UNSET:
            field_dict["branchall"] = branchall
        if approvers is not UNSET:
            field_dict["approvers"] = approvers
        if failed_retries is not UNSET:
            field_dict["failed_retries"] = failed_retries
        if skipped is not UNSET:
            field_dict["skipped"] = skipped
        if agent_actions is not UNSET:
            field_dict["agent_actions"] = agent_actions
        if agent_actions_success is not UNSET:
            field_dict["agent_actions_success"] = agent_actions_success

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_agent_actions_item_type_0 import (
            ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType0,
        )
        from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_agent_actions_item_type_1 import (
            ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType1,
        )
        from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_approvers_item import (
            ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleApproversItem,
        )
        from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_branch_chosen import (
            ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleBranchChosen,
        )
        from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_branchall import (
            ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleBranchall,
        )
        from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_flow_jobs_duration import (
            ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleFlowJobsDuration,
        )
        from ..models.extended_jobs_jobs_item_type_1_flow_status_preprocessor_module_iterator import (
            ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleIterator,
        )

        d = src_dict.copy()
        type = ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleType(d.pop("type"))

        id = d.pop("id", UNSET)

        job = d.pop("job", UNSET)

        count = d.pop("count", UNSET)

        progress = d.pop("progress", UNSET)

        _iterator = d.pop("iterator", UNSET)
        iterator: Union[Unset, ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleIterator]
        if isinstance(_iterator, Unset):
            iterator = UNSET
        else:
            iterator = ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleIterator.from_dict(_iterator)

        flow_jobs = cast(List[str], d.pop("flow_jobs", UNSET))

        flow_jobs_success = cast(List[bool], d.pop("flow_jobs_success", UNSET))

        _flow_jobs_duration = d.pop("flow_jobs_duration", UNSET)
        flow_jobs_duration: Union[Unset, ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleFlowJobsDuration]
        if isinstance(_flow_jobs_duration, Unset):
            flow_jobs_duration = UNSET
        else:
            flow_jobs_duration = ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleFlowJobsDuration.from_dict(
                _flow_jobs_duration
            )

        _branch_chosen = d.pop("branch_chosen", UNSET)
        branch_chosen: Union[Unset, ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleBranchChosen]
        if isinstance(_branch_chosen, Unset):
            branch_chosen = UNSET
        else:
            branch_chosen = ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleBranchChosen.from_dict(_branch_chosen)

        _branchall = d.pop("branchall", UNSET)
        branchall: Union[Unset, ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleBranchall]
        if isinstance(_branchall, Unset):
            branchall = UNSET
        else:
            branchall = ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleBranchall.from_dict(_branchall)

        approvers = []
        _approvers = d.pop("approvers", UNSET)
        for approvers_item_data in _approvers or []:
            approvers_item = ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleApproversItem.from_dict(
                approvers_item_data
            )

            approvers.append(approvers_item)

        failed_retries = cast(List[str], d.pop("failed_retries", UNSET))

        skipped = d.pop("skipped", UNSET)

        agent_actions = []
        _agent_actions = d.pop("agent_actions", UNSET)
        for agent_actions_item_data in _agent_actions or []:

            def _parse_agent_actions_item(
                data: object,
            ) -> Union[
                "ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType0",
                "ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType1",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    agent_actions_item_type_0 = (
                        ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType0.from_dict(data)
                    )

                    return agent_actions_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                agent_actions_item_type_1 = (
                    ExtendedJobsJobsItemType1FlowStatusPreprocessorModuleAgentActionsItemType1.from_dict(data)
                )

                return agent_actions_item_type_1

            agent_actions_item = _parse_agent_actions_item(agent_actions_item_data)

            agent_actions.append(agent_actions_item)

        agent_actions_success = cast(List[bool], d.pop("agent_actions_success", UNSET))

        extended_jobs_jobs_item_type_1_flow_status_preprocessor_module = cls(
            type=type,
            id=id,
            job=job,
            count=count,
            progress=progress,
            iterator=iterator,
            flow_jobs=flow_jobs,
            flow_jobs_success=flow_jobs_success,
            flow_jobs_duration=flow_jobs_duration,
            branch_chosen=branch_chosen,
            branchall=branchall,
            approvers=approvers,
            failed_retries=failed_retries,
            skipped=skipped,
            agent_actions=agent_actions,
            agent_actions_success=agent_actions_success,
        )

        extended_jobs_jobs_item_type_1_flow_status_preprocessor_module.additional_properties = d
        return extended_jobs_jobs_item_type_1_flow_status_preprocessor_module

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
