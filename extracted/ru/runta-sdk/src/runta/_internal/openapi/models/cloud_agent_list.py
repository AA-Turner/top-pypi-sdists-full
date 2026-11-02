from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.cloud_agent import CloudAgent


T = TypeVar("T", bound="CloudAgentList")


@_attrs_define
class CloudAgentList:
    """
    Attributes:
        agents (list[CloudAgent]):
        next_cursor (None | str):
    """

    agents: list[CloudAgent]
    next_cursor: None | str

    def to_dict(self) -> dict[str, Any]:
        agents = []
        for agents_item_data in self.agents:
            agents_item = agents_item_data.to_dict()
            agents.append(agents_item)

        next_cursor: None | str
        next_cursor = self.next_cursor

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "agents": agents,
                "next_cursor": next_cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cloud_agent import CloudAgent

        d = dict(src_dict)
        agents = []
        _agents = d.pop("agents")
        for agents_item_data in _agents:
            agents_item = CloudAgent.from_dict(agents_item_data)

            agents.append(agents_item)

        def _parse_next_cursor(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_cursor = _parse_next_cursor(d.pop("next_cursor"))

        cloud_agent_list = cls(
            agents=agents,
            next_cursor=next_cursor,
        )

        return cloud_agent_list
