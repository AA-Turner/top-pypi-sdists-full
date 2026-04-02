from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ResourceProvisioningStats")


@_attrs_define
class ResourceProvisioningStats:
    """
    Attributes:
        offering_uuid (UUID): UUID of the offering
        offering_name (str): Name of the offering
        service_provider_uuid (UUID): UUID of the service provider
        service_provider_name (str): Name of the service provider
        provisioning_count (int): Total finished provisioning attempts (DONE + ERRED)
        provisioning_success_count (int): Total successful provisioning attempts (DONE)
        provisioning_error_count (int): Total failed provisioning attempts (ERRED)
        provisioning_in_progress_count (int): Total currently in-progress provisioning attempts
        provisioning_success_rate (float): Rate of successful provisioning (0.0 to 1.0)
        avg_provisioning_duration (float): Average duration in seconds from Executing to Terminal state
        avg_pending_duration (float): Average duration in seconds from Creation to Executing state
    """

    offering_uuid: UUID
    offering_name: str
    service_provider_uuid: UUID
    service_provider_name: str
    provisioning_count: int
    provisioning_success_count: int
    provisioning_error_count: int
    provisioning_in_progress_count: int
    provisioning_success_rate: float
    avg_provisioning_duration: float
    avg_pending_duration: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        service_provider_uuid = str(self.service_provider_uuid)

        service_provider_name = self.service_provider_name

        provisioning_count = self.provisioning_count

        provisioning_success_count = self.provisioning_success_count

        provisioning_error_count = self.provisioning_error_count

        provisioning_in_progress_count = self.provisioning_in_progress_count

        provisioning_success_rate = self.provisioning_success_rate

        avg_provisioning_duration = self.avg_provisioning_duration

        avg_pending_duration = self.avg_pending_duration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "service_provider_uuid": service_provider_uuid,
                "service_provider_name": service_provider_name,
                "provisioning_count": provisioning_count,
                "provisioning_success_count": provisioning_success_count,
                "provisioning_error_count": provisioning_error_count,
                "provisioning_in_progress_count": provisioning_in_progress_count,
                "provisioning_success_rate": provisioning_success_rate,
                "avg_provisioning_duration": avg_provisioning_duration,
                "avg_pending_duration": avg_pending_duration,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        service_provider_uuid = UUID(d.pop("service_provider_uuid"))

        service_provider_name = d.pop("service_provider_name")

        provisioning_count = d.pop("provisioning_count")

        provisioning_success_count = d.pop("provisioning_success_count")

        provisioning_error_count = d.pop("provisioning_error_count")

        provisioning_in_progress_count = d.pop("provisioning_in_progress_count")

        provisioning_success_rate = d.pop("provisioning_success_rate")

        avg_provisioning_duration = d.pop("avg_provisioning_duration")

        avg_pending_duration = d.pop("avg_pending_duration")

        resource_provisioning_stats = cls(
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            service_provider_uuid=service_provider_uuid,
            service_provider_name=service_provider_name,
            provisioning_count=provisioning_count,
            provisioning_success_count=provisioning_success_count,
            provisioning_error_count=provisioning_error_count,
            provisioning_in_progress_count=provisioning_in_progress_count,
            provisioning_success_rate=provisioning_success_rate,
            avg_provisioning_duration=avg_provisioning_duration,
            avg_pending_duration=avg_pending_duration,
        )

        resource_provisioning_stats.additional_properties = d
        return resource_provisioning_stats

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
