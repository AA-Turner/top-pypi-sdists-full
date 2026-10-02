from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsAcceleratorProviderEvidence")



@_attrs_define
class ManagedAgentsAcceleratorProviderEvidence:
    """ One provider's evidence for an accelerator model, kept in separate signals: quota is an administrative ceiling, warm
    slots are scheduler telemetry, and a recent launch is historical. None of them is physical GPU stock; only
    allocation proves that.

        Example:
            {'capacity_confidence': 'example', 'observed_at': '2026-02-18T09:30:00Z', 'provider': 'example',
                'quota_headroom': 1, 'quota_limit': 1, 'quota_usage': 1, 'recent_launch_at': '2026-02-18T09:30:00Z', 'region':
                'example', 'telemetry_stale': True, 'warm_allocatable_slots': 1}

        Attributes:
            capacity_confidence (str): fresh_count, advisory, or probe_on_launch. probe_on_launch means physical capacity is
                proven only by allocation.
            provider (str): Configured or reporting compute provider.
            telemetry_stale (bool): Whether live provider telemetry is known to be stale.
            observed_at (datetime.datetime | Unset): When quota or scheduler telemetry was observed.
            quota_headroom (int | Unset): quota_limit minus quota_usage when both are known. Administrative headroom only.
            quota_limit (int | Unset): Provider quota limit. Absent means unknown. Positive headroom does not prove physical
                capacity.
            quota_usage (int | Unset): Current provider quota allocation usage. Absent means unknown. This is not physical
                GPU stock.
            recent_launch_at (datetime.datetime | Unset): Most recent successful launch known to this deployment. Historical
                evidence only.
            region (str | Unset): Provider region this evidence covers. Empty when configuration is provider-wide.
            warm_allocatable_slots (int | Unset): Warm GPU slots upstream reports allocatable now. Absent means unreported;
                zero is a measured zero.
     """

    capacity_confidence: str
    provider: str
    telemetry_stale: bool
    observed_at: datetime.datetime | Unset = UNSET
    quota_headroom: int | Unset = UNSET
    quota_limit: int | Unset = UNSET
    quota_usage: int | Unset = UNSET
    recent_launch_at: datetime.datetime | Unset = UNSET
    region: str | Unset = UNSET
    warm_allocatable_slots: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        capacity_confidence = self.capacity_confidence

        provider = self.provider

        telemetry_stale = self.telemetry_stale

        observed_at: str | Unset = UNSET
        if not isinstance(self.observed_at, Unset):
            observed_at = self.observed_at.isoformat()

        quota_headroom = self.quota_headroom

        quota_limit = self.quota_limit

        quota_usage = self.quota_usage

        recent_launch_at: str | Unset = UNSET
        if not isinstance(self.recent_launch_at, Unset):
            recent_launch_at = self.recent_launch_at.isoformat()

        region = self.region

        warm_allocatable_slots = self.warm_allocatable_slots


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "capacity_confidence": capacity_confidence,
            "provider": provider,
            "telemetry_stale": telemetry_stale,
        })
        if observed_at is not UNSET:
            field_dict["observed_at"] = observed_at
        if quota_headroom is not UNSET:
            field_dict["quota_headroom"] = quota_headroom
        if quota_limit is not UNSET:
            field_dict["quota_limit"] = quota_limit
        if quota_usage is not UNSET:
            field_dict["quota_usage"] = quota_usage
        if recent_launch_at is not UNSET:
            field_dict["recent_launch_at"] = recent_launch_at
        if region is not UNSET:
            field_dict["region"] = region
        if warm_allocatable_slots is not UNSET:
            field_dict["warm_allocatable_slots"] = warm_allocatable_slots

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        capacity_confidence = d.pop("capacity_confidence")

        provider = d.pop("provider")

        telemetry_stale = d.pop("telemetry_stale")

        _observed_at = d.pop("observed_at", UNSET)
        observed_at: datetime.datetime | Unset
        if isinstance(_observed_at,  Unset):
            observed_at = UNSET
        else:
            observed_at = datetime.datetime.fromisoformat(_observed_at)




        quota_headroom = d.pop("quota_headroom", UNSET)

        quota_limit = d.pop("quota_limit", UNSET)

        quota_usage = d.pop("quota_usage", UNSET)

        _recent_launch_at = d.pop("recent_launch_at", UNSET)
        recent_launch_at: datetime.datetime | Unset
        if isinstance(_recent_launch_at,  Unset):
            recent_launch_at = UNSET
        else:
            recent_launch_at = datetime.datetime.fromisoformat(_recent_launch_at)




        region = d.pop("region", UNSET)

        warm_allocatable_slots = d.pop("warm_allocatable_slots", UNSET)

        managed_agents_accelerator_provider_evidence = cls(
            capacity_confidence=capacity_confidence,
            provider=provider,
            telemetry_stale=telemetry_stale,
            observed_at=observed_at,
            quota_headroom=quota_headroom,
            quota_limit=quota_limit,
            quota_usage=quota_usage,
            recent_launch_at=recent_launch_at,
            region=region,
            warm_allocatable_slots=warm_allocatable_slots,
        )


        managed_agents_accelerator_provider_evidence.additional_properties = d
        return managed_agents_accelerator_provider_evidence

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
