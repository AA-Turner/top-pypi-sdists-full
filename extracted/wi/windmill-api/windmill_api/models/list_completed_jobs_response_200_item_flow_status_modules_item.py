from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_type import (
    ListCompletedJobsResponse200ItemFlowStatusModulesItemType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_agent_actions_item_type_0 import (
        ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType0,
    )
    from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_agent_actions_item_type_1 import (
        ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType1,
    )
    from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_approvers_item import (
        ListCompletedJobsResponse200ItemFlowStatusModulesItemApproversItem,
    )
    from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_branch_chosen import (
        ListCompletedJobsResponse200ItemFlowStatusModulesItemBranchChosen,
    )
    from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_branchall import (
        ListCompletedJobsResponse200ItemFlowStatusModulesItemBranchall,
    )
    from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_flow_jobs_duration import (
        ListCompletedJobsResponse200ItemFlowStatusModulesItemFlowJobsDuration,
    )
    from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_iterator import (
        ListCompletedJobsResponse200ItemFlowStatusModulesItemIterator,
    )


T = TypeVar("T", bound="ListCompletedJobsResponse200ItemFlowStatusModulesItem")


@_attrs_define
class ListCompletedJobsResponse200ItemFlowStatusModulesItem:
    """
    Attributes:
        type (ListCompletedJobsResponse200ItemFlowStatusModulesItemType):
        id (Union[Unset, str]):
        job (Union[Unset, str]):
        count (Union[Unset, int]):
        progress (Union[Unset, int]):
        iterator (Union[Unset, ListCompletedJobsResponse200ItemFlowStatusModulesItemIterator]):
        flow_jobs (Union[Unset, List[str]]):
        flow_jobs_success (Union[Unset, List[bool]]):
        flow_jobs_duration (Union[Unset, ListCompletedJobsResponse200ItemFlowStatusModulesItemFlowJobsDuration]):
        branch_chosen (Union[Unset, ListCompletedJobsResponse200ItemFlowStatusModulesItemBranchChosen]):
        branchall (Union[Unset, ListCompletedJobsResponse200ItemFlowStatusModulesItemBranchall]):
        approvers (Union[Unset, List['ListCompletedJobsResponse200ItemFlowStatusModulesItemApproversItem']]):
        failed_retries (Union[Unset, List[str]]):
        skipped (Union[Unset, bool]):
        agent_actions (Union[Unset,
            List[Union['ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType0',
            'ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType1']]]):
        agent_actions_success (Union[Unset, List[bool]]):
    """

    type: ListCompletedJobsResponse200ItemFlowStatusModulesItemType
    id: Union[Unset, str] = UNSET
    job: Union[Unset, str] = UNSET
    count: Union[Unset, int] = UNSET
    progress: Union[Unset, int] = UNSET
    iterator: Union[Unset, "ListCompletedJobsResponse200ItemFlowStatusModulesItemIterator"] = UNSET
    flow_jobs: Union[Unset, List[str]] = UNSET
    flow_jobs_success: Union[Unset, List[bool]] = UNSET
    flow_jobs_duration: Union[Unset, "ListCompletedJobsResponse200ItemFlowStatusModulesItemFlowJobsDuration"] = UNSET
    branch_chosen: Union[Unset, "ListCompletedJobsResponse200ItemFlowStatusModulesItemBranchChosen"] = UNSET
    branchall: Union[Unset, "ListCompletedJobsResponse200ItemFlowStatusModulesItemBranchall"] = UNSET
    approvers: Union[Unset, List["ListCompletedJobsResponse200ItemFlowStatusModulesItemApproversItem"]] = UNSET
    failed_retries: Union[Unset, List[str]] = UNSET
    skipped: Union[Unset, bool] = UNSET
    agent_actions: Union[
        Unset,
        List[
            Union[
                "ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType0",
                "ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType1",
            ]
        ],
    ] = UNSET
    agent_actions_success: Union[Unset, List[bool]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_agent_actions_item_type_0 import (
            ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType0,
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
                    agent_actions_item_data, ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType0
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
        from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_agent_actions_item_type_0 import (
            ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType0,
        )
        from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_agent_actions_item_type_1 import (
            ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType1,
        )
        from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_approvers_item import (
            ListCompletedJobsResponse200ItemFlowStatusModulesItemApproversItem,
        )
        from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_branch_chosen import (
            ListCompletedJobsResponse200ItemFlowStatusModulesItemBranchChosen,
        )
        from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_branchall import (
            ListCompletedJobsResponse200ItemFlowStatusModulesItemBranchall,
        )
        from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_flow_jobs_duration import (
            ListCompletedJobsResponse200ItemFlowStatusModulesItemFlowJobsDuration,
        )
        from ..models.list_completed_jobs_response_200_item_flow_status_modules_item_iterator import (
            ListCompletedJobsResponse200ItemFlowStatusModulesItemIterator,
        )

        d = src_dict.copy()
        type = ListCompletedJobsResponse200ItemFlowStatusModulesItemType(d.pop("type"))

        id = d.pop("id", UNSET)

        job = d.pop("job", UNSET)

        count = d.pop("count", UNSET)

        progress = d.pop("progress", UNSET)

        _iterator = d.pop("iterator", UNSET)
        iterator: Union[Unset, ListCompletedJobsResponse200ItemFlowStatusModulesItemIterator]
        if isinstance(_iterator, Unset):
            iterator = UNSET
        else:
            iterator = ListCompletedJobsResponse200ItemFlowStatusModulesItemIterator.from_dict(_iterator)

        flow_jobs = cast(List[str], d.pop("flow_jobs", UNSET))

        flow_jobs_success = cast(List[bool], d.pop("flow_jobs_success", UNSET))

        _flow_jobs_duration = d.pop("flow_jobs_duration", UNSET)
        flow_jobs_duration: Union[Unset, ListCompletedJobsResponse200ItemFlowStatusModulesItemFlowJobsDuration]
        if isinstance(_flow_jobs_duration, Unset):
            flow_jobs_duration = UNSET
        else:
            flow_jobs_duration = ListCompletedJobsResponse200ItemFlowStatusModulesItemFlowJobsDuration.from_dict(
                _flow_jobs_duration
            )

        _branch_chosen = d.pop("branch_chosen", UNSET)
        branch_chosen: Union[Unset, ListCompletedJobsResponse200ItemFlowStatusModulesItemBranchChosen]
        if isinstance(_branch_chosen, Unset):
            branch_chosen = UNSET
        else:
            branch_chosen = ListCompletedJobsResponse200ItemFlowStatusModulesItemBranchChosen.from_dict(_branch_chosen)

        _branchall = d.pop("branchall", UNSET)
        branchall: Union[Unset, ListCompletedJobsResponse200ItemFlowStatusModulesItemBranchall]
        if isinstance(_branchall, Unset):
            branchall = UNSET
        else:
            branchall = ListCompletedJobsResponse200ItemFlowStatusModulesItemBranchall.from_dict(_branchall)

        approvers = []
        _approvers = d.pop("approvers", UNSET)
        for approvers_item_data in _approvers or []:
            approvers_item = ListCompletedJobsResponse200ItemFlowStatusModulesItemApproversItem.from_dict(
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
                "ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType0",
                "ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType1",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    agent_actions_item_type_0 = (
                        ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType0.from_dict(data)
                    )

                    return agent_actions_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                agent_actions_item_type_1 = (
                    ListCompletedJobsResponse200ItemFlowStatusModulesItemAgentActionsItemType1.from_dict(data)
                )

                return agent_actions_item_type_1

            agent_actions_item = _parse_agent_actions_item(agent_actions_item_data)

            agent_actions.append(agent_actions_item)

        agent_actions_success = cast(List[bool], d.pop("agent_actions_success", UNSET))

        list_completed_jobs_response_200_item_flow_status_modules_item = cls(
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

        list_completed_jobs_response_200_item_flow_status_modules_item.additional_properties = d
        return list_completed_jobs_response_200_item_flow_status_modules_item

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
