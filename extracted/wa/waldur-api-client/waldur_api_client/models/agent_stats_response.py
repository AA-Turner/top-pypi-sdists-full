from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.agent_stats_response_identities import AgentStatsResponseIdentities
    from ..models.agent_stats_response_processors import AgentStatsResponseProcessors
    from ..models.agent_stats_response_services import AgentStatsResponseServices


T = TypeVar("T", bound="AgentStatsResponse")


@_attrs_define
class AgentStatsResponse:
    """
    Attributes:
        identities (AgentStatsResponseIdentities): Statistics about agent identities
        services (AgentStatsResponseServices): Statistics about agent services
        processors (AgentStatsResponseProcessors): Statistics about agent processors
    """

    identities: "AgentStatsResponseIdentities"
    services: "AgentStatsResponseServices"
    processors: "AgentStatsResponseProcessors"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        identities = self.identities.to_dict()

        services = self.services.to_dict()

        processors = self.processors.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "identities": identities,
                "services": services,
                "processors": processors,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_stats_response_identities import AgentStatsResponseIdentities
        from ..models.agent_stats_response_processors import AgentStatsResponseProcessors
        from ..models.agent_stats_response_services import AgentStatsResponseServices

        d = dict(src_dict)
        identities = AgentStatsResponseIdentities.from_dict(d.pop("identities"))

        services = AgentStatsResponseServices.from_dict(d.pop("services"))

        processors = AgentStatsResponseProcessors.from_dict(d.pop("processors"))

        agent_stats_response = cls(
            identities=identities,
            services=services,
            processors=processors,
        )

        agent_stats_response.additional_properties = d
        return agent_stats_response

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
