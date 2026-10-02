from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_session_hour_estimate_unit import ManagedAgentsSessionHourEstimateUnit
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_band import ManagedAgentsBand
  from ..models.managed_agents_compute_rate import ManagedAgentsComputeRate
  from ..models.managed_agents_model_active_rate import ManagedAgentsModelActiveRate
  from ..models.managed_agents_utilization import ManagedAgentsUtilization





T = TypeVar("T", bound="ManagedAgentsSessionHourEstimate")



@_attrs_define
class ManagedAgentsSessionHourEstimate:
    """ What one session hour is likely to cost the calling organization, at its billed rates.

        Example:
            {'asOf': '2026-02-18T09:30:00Z', 'compute': {'perHourUsd': 1.5, 'source': 'agent_service_rate_table'},
                'modelActiveRate': {'basis': 'observed', 'basisModel': 'example', 'billedToProvider': True, 'perHourUsd':
                {'high': 1.5, 'low': 1.5, 'typical': 1.5}, 'scaleFactor': 1.5, 'sessions': 1}, 'perSessionHourUsd': {'high':
                1.5, 'low': 1.5, 'typical': 1.5}, 'unit': 'session_hour', 'utilization': {'basis': 'agent_history',
                'sessionHours': {'high': 1.5, 'low': 1.5, 'typical': 1.5}, 'sessions': 1, 'share': {'high': 1.5, 'low': 1.5,
                'typical': 1.5}, 'workload': 'interactive'}, 'whileActivePerHourUsd': 1.5, 'windowDays': 1}

        Attributes:
            as_of (datetime.datetime): When the history behind the estimate was last refreshed.
            compute (ManagedAgentsComputeRate): Billed price of the requested compute shape. Example: {'perHourUsd': 1.5,
                'source': 'agent_service_rate_table'}.
            model_active_rate (ManagedAgentsModelActiveRate): Billed model spend per hour while the model is generating.
                Example: {'basis': 'observed', 'basisModel': 'example', 'billedToProvider': True, 'perHourUsd': {'high': 1.5,
                'low': 1.5, 'typical': 1.5}, 'scaleFactor': 1.5, 'sessions': 1}.
            per_session_hour_usd (ManagedAgentsBand): Low, typical and high values: the 25th, 50th and 75th percentiles.
                Example: {'high': 1.5, 'low': 1.5, 'typical': 1.5}.
            unit (ManagedAgentsSessionHourEstimateUnit): Unit every amount is quoted in.
            utilization (ManagedAgentsUtilization): How much of a session hour the agent spends generating. Example:
                {'basis': 'agent_history', 'sessionHours': {'high': 1.5, 'low': 1.5, 'typical': 1.5}, 'sessions': 1, 'share':
                {'high': 1.5, 'low': 1.5, 'typical': 1.5}, 'workload': 'interactive'}.
            while_active_per_hour_usd (float): Billed cost per hour while the agent is working the whole hour, in USD.
            window_days (int): Days of completed sessions the history covers.
     """

    as_of: datetime.datetime
    compute: ManagedAgentsComputeRate
    model_active_rate: ManagedAgentsModelActiveRate
    per_session_hour_usd: ManagedAgentsBand
    unit: ManagedAgentsSessionHourEstimateUnit
    utilization: ManagedAgentsUtilization
    while_active_per_hour_usd: float
    window_days: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_band import ManagedAgentsBand # noqa: PLC0415
        from ..models.managed_agents_compute_rate import ManagedAgentsComputeRate # noqa: PLC0415
        from ..models.managed_agents_model_active_rate import ManagedAgentsModelActiveRate # noqa: PLC0415
        from ..models.managed_agents_utilization import ManagedAgentsUtilization # noqa: PLC0415
        as_of = self.as_of.isoformat()

        compute = self.compute.to_dict()

        model_active_rate = self.model_active_rate.to_dict()

        per_session_hour_usd = self.per_session_hour_usd.to_dict()

        unit = self.unit.value

        utilization = self.utilization.to_dict()

        while_active_per_hour_usd = self.while_active_per_hour_usd

        window_days = self.window_days


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "asOf": as_of,
            "compute": compute,
            "modelActiveRate": model_active_rate,
            "perSessionHourUsd": per_session_hour_usd,
            "unit": unit,
            "utilization": utilization,
            "whileActivePerHourUsd": while_active_per_hour_usd,
            "windowDays": window_days,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_band import ManagedAgentsBand # noqa: PLC0415
        from ..models.managed_agents_compute_rate import ManagedAgentsComputeRate # noqa: PLC0415
        from ..models.managed_agents_model_active_rate import ManagedAgentsModelActiveRate # noqa: PLC0415
        from ..models.managed_agents_utilization import ManagedAgentsUtilization # noqa: PLC0415
        d = dict(src_dict)
        as_of = datetime.datetime.fromisoformat(d.pop("asOf"))




        compute = ManagedAgentsComputeRate.from_dict(d.pop("compute"))




        model_active_rate = ManagedAgentsModelActiveRate.from_dict(d.pop("modelActiveRate"))




        per_session_hour_usd = ManagedAgentsBand.from_dict(d.pop("perSessionHourUsd"))




        unit = ManagedAgentsSessionHourEstimateUnit(d.pop("unit"))




        utilization = ManagedAgentsUtilization.from_dict(d.pop("utilization"))




        while_active_per_hour_usd = d.pop("whileActivePerHourUsd")

        window_days = d.pop("windowDays")

        managed_agents_session_hour_estimate = cls(
            as_of=as_of,
            compute=compute,
            model_active_rate=model_active_rate,
            per_session_hour_usd=per_session_hour_usd,
            unit=unit,
            utilization=utilization,
            while_active_per_hour_usd=while_active_per_hour_usd,
            window_days=window_days,
        )


        managed_agents_session_hour_estimate.additional_properties = d
        return managed_agents_session_hour_estimate

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
