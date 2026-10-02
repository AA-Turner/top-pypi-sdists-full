from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.resource_demand_stat_total_approved_limits import ResourceDemandStatTotalApprovedLimits
    from ..models.resource_demand_stat_total_requested_limits import ResourceDemandStatTotalRequestedLimits


T = TypeVar("T", bound="ResourceDemandStat")


@_attrs_define
class ResourceDemandStat:
    """
    Attributes:
        offering_uuid (UUID):
        offering_name (str):
        offering_type (str):
        provider_name (str):
        proposal_count (int):
        request_count (int):
        approved_count (int):
        pending_count (int):
        total_requested_limits (ResourceDemandStatTotalRequestedLimits):
        total_approved_limits (ResourceDemandStatTotalApprovedLimits):
    """

    offering_uuid: UUID
    offering_name: str
    offering_type: str
    provider_name: str
    proposal_count: int
    request_count: int
    approved_count: int
    pending_count: int
    total_requested_limits: "ResourceDemandStatTotalRequestedLimits"
    total_approved_limits: "ResourceDemandStatTotalApprovedLimits"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        offering_type = self.offering_type

        provider_name = self.provider_name

        proposal_count = self.proposal_count

        request_count = self.request_count

        approved_count = self.approved_count

        pending_count = self.pending_count

        total_requested_limits = self.total_requested_limits.to_dict()

        total_approved_limits = self.total_approved_limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "offering_type": offering_type,
                "provider_name": provider_name,
                "proposal_count": proposal_count,
                "request_count": request_count,
                "approved_count": approved_count,
                "pending_count": pending_count,
                "total_requested_limits": total_requested_limits,
                "total_approved_limits": total_approved_limits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_demand_stat_total_approved_limits import ResourceDemandStatTotalApprovedLimits
        from ..models.resource_demand_stat_total_requested_limits import ResourceDemandStatTotalRequestedLimits

        d = dict(src_dict)
        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        offering_type = d.pop("offering_type")

        provider_name = d.pop("provider_name")

        proposal_count = d.pop("proposal_count")

        request_count = d.pop("request_count")

        approved_count = d.pop("approved_count")

        pending_count = d.pop("pending_count")

        total_requested_limits = ResourceDemandStatTotalRequestedLimits.from_dict(d.pop("total_requested_limits"))

        total_approved_limits = ResourceDemandStatTotalApprovedLimits.from_dict(d.pop("total_approved_limits"))

        resource_demand_stat = cls(
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            offering_type=offering_type,
            provider_name=provider_name,
            proposal_count=proposal_count,
            request_count=request_count,
            approved_count=approved_count,
            pending_count=pending_count,
            total_requested_limits=total_requested_limits,
            total_approved_limits=total_approved_limits,
        )

        resource_demand_stat.additional_properties = d
        return resource_demand_stat

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
