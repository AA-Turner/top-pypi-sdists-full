from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_type import (
    ListJobsResponse200ItemType1FlowStatusModulesItemType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_agent_actions_item_type_0 import (
        ListJobsResponse200ItemType1FlowStatusModulesItemAgentActionsItemType0,
    )
    from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_agent_actions_item_type_1 import (
        ListJobsResponse200ItemType1FlowStatusModulesItemAgentActionsItemType1,
    )
    from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_approvers_item import (
        ListJobsResponse200ItemType1FlowStatusModulesItemApproversItem,
    )
    from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_branch_chosen import (
        ListJobsResponse200ItemType1FlowStatusModulesItemBranchChosen,
    )
    from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_branchall import (
        ListJobsResponse200ItemType1FlowStatusModulesItemBranchall,
    )
    from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_flow_jobs_duration import (
        ListJobsResponse200ItemType1FlowStatusModulesItemFlowJobsDuration,
    )
    from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_iterator import (
        ListJobsResponse200ItemType1FlowStatusModulesItemIterator,
    )


T = TypeVar("T", bound="ListJobsResponse200ItemType1FlowStatusModulesItem")


@_attrs_define
class ListJobsResponse200ItemType1FlowStatusModulesItem:
    """
    Attributes:
        type (ListJobsResponse200ItemType1FlowStatusModulesItemType):
        id (Union[Unset, str]):
        job (Union[Unset, str]):
        count (Union[Unset, int]):
        progress (Union[Unset, int]):
        iterator (Union[Unset, ListJobsResponse200ItemType1FlowStatusModulesItemIterator]):
        flow_jobs (Union[Unset, List[str]]):
        flow_jobs_success (Union[Unset, List[bool]]):
        flow_jobs_duration (Union[Unset, ListJobsResponse200ItemType1FlowStatusModulesItemFlowJobsDuration]):
        branch_chosen (Union[Unset, ListJobsResponse200ItemType1FlowStatusModulesItemBranchChosen]):
        branchall (Union[Unset, ListJobsResponse200ItemType1FlowStatusModulesItemBranchall]):
        approvers (Union[Unset, List['ListJobsResponse200ItemType1FlowStatusModulesItemApproversItem']]):
        failed_retries (Union[Unset, List[str]]):
        skipped (Union[Unset, bool]):
        agent_actions (Union[Unset, List[Union['ListJobsResponse200ItemType1FlowStatusModulesItemAgentActionsItemType0',
            'ListJobsResponse200ItemType1FlowStatusModulesItemAgentActionsItemType1']]]):
        agent_actions_success (Union[Unset, List[bool]]):
    """

    type: ListJobsResponse200ItemType1FlowStatusModulesItemType
    id: Union[Unset, str] = UNSET
    job: Union[Unset, str] = UNSET
    count: Union[Unset, int] = UNSET
    progress: Union[Unset, int] = UNSET
    iterator: Union[Unset, "ListJobsResponse200ItemType1FlowStatusModulesItemIterator"] = UNSET
    flow_jobs: Union[Unset, List[str]] = UNSET
    flow_jobs_success: Union[Unset, List[bool]] = UNSET
    flow_jobs_duration: Union[Unset, "ListJobsResponse200ItemType1FlowStatusModulesItemFlowJobsDuration"] = UNSET
    branch_chosen: Union[Unset, "ListJobsResponse200ItemType1FlowStatusModulesItemBranchChosen"] = UNSET
    branchall: Union[Unset, "ListJobsResponse200ItemType1FlowStatusModulesItemBranchall"] = UNSET
    approvers: Union[Unset, List["ListJobsResponse200ItemType1FlowStatusModulesItemApproversItem"]] = UNSET
    failed_retries: Union[Unset, List[str]] = UNSET
    skipped: Union[Unset, bool] = UNSET
    agent_actions: Union[
        Unset,
        List[
            Union[
                "ListJobsResponse200ItemType1FlowStatusModulesItemAgentActionsItemType0",
                "ListJobsResponse200ItemType1FlowStatusModulesItemAgentActionsItemType1",
            ]
        ],
    ] = UNSET
    agent_actions_success: Union[Unset, List[bool]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_agent_actions_item_type_0 import (
            ListJobsResponse200ItemType1FlowStatusModulesItemAgentActionsItemType0,
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
                    agent_actions_item_data, ListJobsResponse200ItemType1FlowStatusModulesItemAgentActionsItemType0
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
        from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_agent_actions_item_type_0 import (
            ListJobsResponse200ItemType1FlowStatusModulesItemAgentActionsItemType0,
        )
        from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_agent_actions_item_type_1 import (
            ListJobsResponse200ItemType1FlowStatusModulesItemAgentActionsItemType1,
        )
        from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_approvers_item import (
            ListJobsResponse200ItemType1FlowStatusModulesItemApproversItem,
        )
        from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_branch_chosen import (
            ListJobsResponse200ItemType1FlowStatusModulesItemBranchChosen,
        )
        from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_branchall import (
            ListJobsResponse200ItemType1FlowStatusModulesItemBranchall,
        )
        from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_flow_jobs_duration import (
            ListJobsResponse200ItemType1FlowStatusModulesItemFlowJobsDuration,
        )
        from ..models.list_jobs_response_200_item_type_1_flow_status_modules_item_iterator import (
            ListJobsResponse200ItemType1FlowStatusModulesItemIterator,
        )

        d = src_dict.copy()
        type = ListJobsResponse200ItemType1FlowStatusModulesItemType(d.pop("type"))

        id = d.pop("id", UNSET)

        job = d.pop("job", UNSET)

        count = d.pop("count", UNSET)

        progress = d.pop("progress", UNSET)

        _iterator = d.pop("iterator", UNSET)
        iterator: Union[Unset, ListJobsResponse200ItemType1FlowStatusModulesItemIterator]
        if isinstance(_iterator, Unset):
            iterator = UNSET
        else:
            iterator = ListJobsResponse200ItemType1FlowStatusModulesItemIterator.from_dict(_iterator)

        flow_jobs = cast(List[str], d.pop("flow_jobs", UNSET))

        flow_jobs_success = cast(List[bool], d.pop("flow_jobs_success", UNSET))

        _flow_jobs_duration = d.pop("flow_jobs_duration", UNSET)
        flow_jobs_duration: Union[Unset, ListJobsResponse200ItemType1FlowStatusModulesItemFlowJobsDuration]
        if isinstance(_flow_jobs_duration, Unset):
            flow_jobs_duration = UNSET
        else:
            flow_jobs_duration = ListJobsResponse200ItemType1FlowStatusModulesItemFlowJobsDuration.from_dict(
                _flow_jobs_duration
            )

        _branch_chosen = d.pop("branch_chosen", UNSET)
        branch_chosen: Union[Unset, ListJobsResponse200ItemType1FlowStatusModulesItemBranchChosen]
        if isinstance(_branch_chosen, Unset):
            branch_chosen = UNSET
        else:
            branch_chosen = ListJobsResponse200ItemType1FlowStatusModulesItemBranchChosen.from_dict(_branch_chosen)

        _branchall = d.pop("branchall", UNSET)
        branchall: Union[Unset, ListJobsResponse200ItemType1FlowStatusModulesItemBranchall]
        if isinstance(_branchall, Unset):
            branchall = UNSET
        else:
            branchall = ListJobsResponse200ItemType1FlowStatusModulesItemBranchall.from_dict(_branchall)

        approvers = []
        _approvers = d.pop("approvers", UNSET)
        for approvers_item_data in _approvers or []:
            approvers_item = ListJobsResponse200ItemType1FlowStatusModulesItemApproversItem.from_dict(
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
                "ListJobsResponse200ItemType1FlowStatusModulesItemAgentActionsItemType0",
                "ListJobsResponse200ItemType1FlowStatusModulesItemAgentActionsItemType1",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    agent_actions_item_type_0 = (
                        ListJobsResponse200ItemType1FlowStatusModulesItemAgentActionsItemType0.from_dict(data)
                    )

                    return agent_actions_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                agent_actions_item_type_1 = (
                    ListJobsResponse200ItemType1FlowStatusModulesItemAgentActionsItemType1.from_dict(data)
                )

                return agent_actions_item_type_1

            agent_actions_item = _parse_agent_actions_item(agent_actions_item_data)

            agent_actions.append(agent_actions_item)

        agent_actions_success = cast(List[bool], d.pop("agent_actions_success", UNSET))

        list_jobs_response_200_item_type_1_flow_status_modules_item = cls(
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

        list_jobs_response_200_item_type_1_flow_status_modules_item.additional_properties = d
        return list_jobs_response_200_item_type_1_flow_status_modules_item

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
