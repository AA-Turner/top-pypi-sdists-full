from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_model_active_rate_basis import ManagedAgentsModelActiveRateBasis
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_band import ManagedAgentsBand





T = TypeVar("T", bound="ManagedAgentsModelActiveRate")



@_attrs_define
class ManagedAgentsModelActiveRate:
    """ Billed model spend per hour while the model is generating.

        Example:
            {'basis': 'observed', 'basisModel': 'example', 'billedToProvider': True, 'perHourUsd': {'high': 1.5, 'low': 1.5,
                'typical': 1.5}, 'scaleFactor': 1.5, 'sessions': 1}

        Attributes:
            basis (ManagedAgentsModelActiveRateBasis): Where the rate comes from: recent sessions of this model, a platform
                baseline, a similar model scaled by list price, or unknown when neither exists.
            billed_to_provider (bool): True when the model runs on the organization's own provider account, so its spend is
                billed there rather than by this platform and perHourUsd is zero.
            per_hour_usd (ManagedAgentsBand): Low, typical and high values: the 25th, 50th and 75th percentiles. Example:
                {'high': 1.5, 'low': 1.5, 'typical': 1.5}.
            sessions (int): Recent sessions behind an observed rate; zero otherwise.
            basis_model (str | Unset): Model the rate was scaled from, when basis is scaled_list_price.
            scale_factor (float | Unset): Ratio applied to the basis model's rate, when basis is scaled_list_price.
     """

    basis: ManagedAgentsModelActiveRateBasis
    billed_to_provider: bool
    per_hour_usd: ManagedAgentsBand
    sessions: int
    basis_model: str | Unset = UNSET
    scale_factor: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_band import ManagedAgentsBand # noqa: PLC0415
        basis = self.basis.value

        billed_to_provider = self.billed_to_provider

        per_hour_usd = self.per_hour_usd.to_dict()

        sessions = self.sessions

        basis_model = self.basis_model

        scale_factor = self.scale_factor


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "basis": basis,
            "billedToProvider": billed_to_provider,
            "perHourUsd": per_hour_usd,
            "sessions": sessions,
        })
        if basis_model is not UNSET:
            field_dict["basisModel"] = basis_model
        if scale_factor is not UNSET:
            field_dict["scaleFactor"] = scale_factor

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_band import ManagedAgentsBand # noqa: PLC0415
        d = dict(src_dict)
        basis = ManagedAgentsModelActiveRateBasis(d.pop("basis"))




        billed_to_provider = d.pop("billedToProvider")

        per_hour_usd = ManagedAgentsBand.from_dict(d.pop("perHourUsd"))




        sessions = d.pop("sessions")

        basis_model = d.pop("basisModel", UNSET)

        scale_factor = d.pop("scaleFactor", UNSET)

        managed_agents_model_active_rate = cls(
            basis=basis,
            billed_to_provider=billed_to_provider,
            per_hour_usd=per_hour_usd,
            sessions=sessions,
            basis_model=basis_model,
            scale_factor=scale_factor,
        )


        managed_agents_model_active_rate.additional_properties = d
        return managed_agents_model_active_rate

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
