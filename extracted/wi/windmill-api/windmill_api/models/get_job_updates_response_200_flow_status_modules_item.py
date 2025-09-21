from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_job_updates_response_200_flow_status_modules_item_type import (
    GetJobUpdatesResponse200FlowStatusModulesItemType,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_job_updates_response_200_flow_status_modules_item_agent_actions_item_type_0 import (
        GetJobUpdatesResponse200FlowStatusModulesItemAgentActionsItemType0,
    )
    from ..models.get_job_updates_response_200_flow_status_modules_item_agent_actions_item_type_1 import (
        GetJobUpdatesResponse200FlowStatusModulesItemAgentActionsItemType1,
    )
    from ..models.get_job_updates_response_200_flow_status_modules_item_approvers_item import (
        GetJobUpdatesResponse200FlowStatusModulesItemApproversItem,
    )
    from ..models.get_job_updates_response_200_flow_status_modules_item_branch_chosen import (
        GetJobUpdatesResponse200FlowStatusModulesItemBranchChosen,
    )
    from ..models.get_job_updates_response_200_flow_status_modules_item_branchall import (
        GetJobUpdatesResponse200FlowStatusModulesItemBranchall,
    )
    from ..models.get_job_updates_response_200_flow_status_modules_item_flow_jobs_duration import (
        GetJobUpdatesResponse200FlowStatusModulesItemFlowJobsDuration,
    )
    from ..models.get_job_updates_response_200_flow_status_modules_item_iterator import (
        GetJobUpdatesResponse200FlowStatusModulesItemIterator,
    )


T = TypeVar("T", bound="GetJobUpdatesResponse200FlowStatusModulesItem")


@_attrs_define
class GetJobUpdatesResponse200FlowStatusModulesItem:
    """
    Attributes:
        type (GetJobUpdatesResponse200FlowStatusModulesItemType):
        id (Union[Unset, str]):
        job (Union[Unset, str]):
        count (Union[Unset, int]):
        progress (Union[Unset, int]):
        iterator (Union[Unset, GetJobUpdatesResponse200FlowStatusModulesItemIterator]):
        flow_jobs (Union[Unset, List[str]]):
        flow_jobs_success (Union[Unset, List[bool]]):
        flow_jobs_duration (Union[Unset, GetJobUpdatesResponse200FlowStatusModulesItemFlowJobsDuration]):
        branch_chosen (Union[Unset, GetJobUpdatesResponse200FlowStatusModulesItemBranchChosen]):
        branchall (Union[Unset, GetJobUpdatesResponse200FlowStatusModulesItemBranchall]):
        approvers (Union[Unset, List['GetJobUpdatesResponse200FlowStatusModulesItemApproversItem']]):
        failed_retries (Union[Unset, List[str]]):
        skipped (Union[Unset, bool]):
        agent_actions (Union[Unset, List[Union['GetJobUpdatesResponse200FlowStatusModulesItemAgentActionsItemType0',
            'GetJobUpdatesResponse200FlowStatusModulesItemAgentActionsItemType1']]]):
        agent_actions_success (Union[Unset, List[bool]]):
    """

    type: GetJobUpdatesResponse200FlowStatusModulesItemType
    id: Union[Unset, str] = UNSET
    job: Union[Unset, str] = UNSET
    count: Union[Unset, int] = UNSET
    progress: Union[Unset, int] = UNSET
    iterator: Union[Unset, "GetJobUpdatesResponse200FlowStatusModulesItemIterator"] = UNSET
    flow_jobs: Union[Unset, List[str]] = UNSET
    flow_jobs_success: Union[Unset, List[bool]] = UNSET
    flow_jobs_duration: Union[Unset, "GetJobUpdatesResponse200FlowStatusModulesItemFlowJobsDuration"] = UNSET
    branch_chosen: Union[Unset, "GetJobUpdatesResponse200FlowStatusModulesItemBranchChosen"] = UNSET
    branchall: Union[Unset, "GetJobUpdatesResponse200FlowStatusModulesItemBranchall"] = UNSET
    approvers: Union[Unset, List["GetJobUpdatesResponse200FlowStatusModulesItemApproversItem"]] = UNSET
    failed_retries: Union[Unset, List[str]] = UNSET
    skipped: Union[Unset, bool] = UNSET
    agent_actions: Union[
        Unset,
        List[
            Union[
                "GetJobUpdatesResponse200FlowStatusModulesItemAgentActionsItemType0",
                "GetJobUpdatesResponse200FlowStatusModulesItemAgentActionsItemType1",
            ]
        ],
    ] = UNSET
    agent_actions_success: Union[Unset, List[bool]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.get_job_updates_response_200_flow_status_modules_item_agent_actions_item_type_0 import (
            GetJobUpdatesResponse200FlowStatusModulesItemAgentActionsItemType0,
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
                    agent_actions_item_data, GetJobUpdatesResponse200FlowStatusModulesItemAgentActionsItemType0
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
        from ..models.get_job_updates_response_200_flow_status_modules_item_agent_actions_item_type_0 import (
            GetJobUpdatesResponse200FlowStatusModulesItemAgentActionsItemType0,
        )
        from ..models.get_job_updates_response_200_flow_status_modules_item_agent_actions_item_type_1 import (
            GetJobUpdatesResponse200FlowStatusModulesItemAgentActionsItemType1,
        )
        from ..models.get_job_updates_response_200_flow_status_modules_item_approvers_item import (
            GetJobUpdatesResponse200FlowStatusModulesItemApproversItem,
        )
        from ..models.get_job_updates_response_200_flow_status_modules_item_branch_chosen import (
            GetJobUpdatesResponse200FlowStatusModulesItemBranchChosen,
        )
        from ..models.get_job_updates_response_200_flow_status_modules_item_branchall import (
            GetJobUpdatesResponse200FlowStatusModulesItemBranchall,
        )
        from ..models.get_job_updates_response_200_flow_status_modules_item_flow_jobs_duration import (
            GetJobUpdatesResponse200FlowStatusModulesItemFlowJobsDuration,
        )
        from ..models.get_job_updates_response_200_flow_status_modules_item_iterator import (
            GetJobUpdatesResponse200FlowStatusModulesItemIterator,
        )

        d = src_dict.copy()
        type = GetJobUpdatesResponse200FlowStatusModulesItemType(d.pop("type"))

        id = d.pop("id", UNSET)

        job = d.pop("job", UNSET)

        count = d.pop("count", UNSET)

        progress = d.pop("progress", UNSET)

        _iterator = d.pop("iterator", UNSET)
        iterator: Union[Unset, GetJobUpdatesResponse200FlowStatusModulesItemIterator]
        if isinstance(_iterator, Unset):
            iterator = UNSET
        else:
            iterator = GetJobUpdatesResponse200FlowStatusModulesItemIterator.from_dict(_iterator)

        flow_jobs = cast(List[str], d.pop("flow_jobs", UNSET))

        flow_jobs_success = cast(List[bool], d.pop("flow_jobs_success", UNSET))

        _flow_jobs_duration = d.pop("flow_jobs_duration", UNSET)
        flow_jobs_duration: Union[Unset, GetJobUpdatesResponse200FlowStatusModulesItemFlowJobsDuration]
        if isinstance(_flow_jobs_duration, Unset):
            flow_jobs_duration = UNSET
        else:
            flow_jobs_duration = GetJobUpdatesResponse200FlowStatusModulesItemFlowJobsDuration.from_dict(
                _flow_jobs_duration
            )

        _branch_chosen = d.pop("branch_chosen", UNSET)
        branch_chosen: Union[Unset, GetJobUpdatesResponse200FlowStatusModulesItemBranchChosen]
        if isinstance(_branch_chosen, Unset):
            branch_chosen = UNSET
        else:
            branch_chosen = GetJobUpdatesResponse200FlowStatusModulesItemBranchChosen.from_dict(_branch_chosen)

        _branchall = d.pop("branchall", UNSET)
        branchall: Union[Unset, GetJobUpdatesResponse200FlowStatusModulesItemBranchall]
        if isinstance(_branchall, Unset):
            branchall = UNSET
        else:
            branchall = GetJobUpdatesResponse200FlowStatusModulesItemBranchall.from_dict(_branchall)

        approvers = []
        _approvers = d.pop("approvers", UNSET)
        for approvers_item_data in _approvers or []:
            approvers_item = GetJobUpdatesResponse200FlowStatusModulesItemApproversItem.from_dict(approvers_item_data)

            approvers.append(approvers_item)

        failed_retries = cast(List[str], d.pop("failed_retries", UNSET))

        skipped = d.pop("skipped", UNSET)

        agent_actions = []
        _agent_actions = d.pop("agent_actions", UNSET)
        for agent_actions_item_data in _agent_actions or []:

            def _parse_agent_actions_item(
                data: object,
            ) -> Union[
                "GetJobUpdatesResponse200FlowStatusModulesItemAgentActionsItemType0",
                "GetJobUpdatesResponse200FlowStatusModulesItemAgentActionsItemType1",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    agent_actions_item_type_0 = (
                        GetJobUpdatesResponse200FlowStatusModulesItemAgentActionsItemType0.from_dict(data)
                    )

                    return agent_actions_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                agent_actions_item_type_1 = (
                    GetJobUpdatesResponse200FlowStatusModulesItemAgentActionsItemType1.from_dict(data)
                )

                return agent_actions_item_type_1

            agent_actions_item = _parse_agent_actions_item(agent_actions_item_data)

            agent_actions.append(agent_actions_item)

        agent_actions_success = cast(List[bool], d.pop("agent_actions_success", UNSET))

        get_job_updates_response_200_flow_status_modules_item = cls(
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

        get_job_updates_response_200_flow_status_modules_item.additional_properties = d
        return get_job_updates_response_200_flow_status_modules_item

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
