from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_task_stats_response_active_tasks_item import AgentTaskStatsResponseActiveTasksItem
    from ..models.agent_task_stats_response_reserved_tasks_item import AgentTaskStatsResponseReservedTasksItem
    from ..models.agent_task_stats_response_scheduled_tasks_item import AgentTaskStatsResponseScheduledTasksItem


T = TypeVar("T", bound="AgentTaskStatsResponse")


@_attrs_define
class AgentTaskStatsResponse:
    """
    Attributes:
        active_tasks (list['AgentTaskStatsResponseActiveTasksItem']): Currently running agent-related tasks
        scheduled_tasks (list['AgentTaskStatsResponseScheduledTasksItem']): Scheduled agent-related tasks
        reserved_tasks (list['AgentTaskStatsResponseReservedTasksItem']): Reserved agent-related tasks
        error (Union[Unset, str]): Error message if task inspection failed
    """

    active_tasks: list["AgentTaskStatsResponseActiveTasksItem"]
    scheduled_tasks: list["AgentTaskStatsResponseScheduledTasksItem"]
    reserved_tasks: list["AgentTaskStatsResponseReservedTasksItem"]
    error: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active_tasks = []
        for active_tasks_item_data in self.active_tasks:
            active_tasks_item = active_tasks_item_data.to_dict()
            active_tasks.append(active_tasks_item)

        scheduled_tasks = []
        for scheduled_tasks_item_data in self.scheduled_tasks:
            scheduled_tasks_item = scheduled_tasks_item_data.to_dict()
            scheduled_tasks.append(scheduled_tasks_item)

        reserved_tasks = []
        for reserved_tasks_item_data in self.reserved_tasks:
            reserved_tasks_item = reserved_tasks_item_data.to_dict()
            reserved_tasks.append(reserved_tasks_item)

        error = self.error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active_tasks": active_tasks,
                "scheduled_tasks": scheduled_tasks,
                "reserved_tasks": reserved_tasks,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_task_stats_response_active_tasks_item import AgentTaskStatsResponseActiveTasksItem
        from ..models.agent_task_stats_response_reserved_tasks_item import AgentTaskStatsResponseReservedTasksItem
        from ..models.agent_task_stats_response_scheduled_tasks_item import AgentTaskStatsResponseScheduledTasksItem

        d = dict(src_dict)
        active_tasks = []
        _active_tasks = d.pop("active_tasks")
        for active_tasks_item_data in _active_tasks:
            active_tasks_item = AgentTaskStatsResponseActiveTasksItem.from_dict(active_tasks_item_data)

            active_tasks.append(active_tasks_item)

        scheduled_tasks = []
        _scheduled_tasks = d.pop("scheduled_tasks")
        for scheduled_tasks_item_data in _scheduled_tasks:
            scheduled_tasks_item = AgentTaskStatsResponseScheduledTasksItem.from_dict(scheduled_tasks_item_data)

            scheduled_tasks.append(scheduled_tasks_item)

        reserved_tasks = []
        _reserved_tasks = d.pop("reserved_tasks")
        for reserved_tasks_item_data in _reserved_tasks:
            reserved_tasks_item = AgentTaskStatsResponseReservedTasksItem.from_dict(reserved_tasks_item_data)

            reserved_tasks.append(reserved_tasks_item)

        error = d.pop("error", UNSET)

        agent_task_stats_response = cls(
            active_tasks=active_tasks,
            scheduled_tasks=scheduled_tasks,
            reserved_tasks=reserved_tasks,
            error=error,
        )

        agent_task_stats_response.additional_properties = d
        return agent_task_stats_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
