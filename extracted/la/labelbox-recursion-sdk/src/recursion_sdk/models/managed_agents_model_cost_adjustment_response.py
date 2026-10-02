from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_model_cost_adjustment_response_kind import ManagedAgentsModelCostAdjustmentResponseKind
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsModelCostAdjustmentResponse")



@_attrs_define
class ManagedAgentsModelCostAdjustmentResponse:
    """ A signed correction to one charge, recorded after the charge itself. Adjustments are append-only:
    original_model_cost_usd keeps the amount as first recorded, and model_cost_usd carries the locally priced total plus
    every adjustment.

        Example:
            {'adjustment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at': '2026-02-18T09:30:00Z', 'created_by':
                'example', 'kind': 'provider_authority', 'model_cost_usd': 'example', 'reason': 'example'}

        Attributes:
            adjustment_id (str): Identifier for this adjustment within its charge. The ledger's own reconciliation of a
                provider-reported total always uses provider-authority.
            created_at (datetime.datetime): RFC 3339 timestamp of when the adjustment was committed.
            created_by (str): Principal that recorded the adjustment. The automatic provider-total reconciliation records
                system:cost-ledger.
            kind (ManagedAgentsModelCostAdjustmentResponseKind): provider_authority reconciles the locally priced total to
                the total the provider reported for the same call; correction is an amendment recorded against an existing
                charge.
            model_cost_usd (str): Exact signed canonical decimal USD string.
            reason (str): Why the adjustment was recorded, e.g. that the provider-reported total overrides the local price
                snapshot.
     """

    adjustment_id: str
    created_at: datetime.datetime
    created_by: str
    kind: ManagedAgentsModelCostAdjustmentResponseKind
    model_cost_usd: str
    reason: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        adjustment_id = self.adjustment_id

        created_at = self.created_at.isoformat()

        created_by = self.created_by

        kind = self.kind.value

        model_cost_usd = self.model_cost_usd

        reason = self.reason


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "adjustment_id": adjustment_id,
            "created_at": created_at,
            "created_by": created_by,
            "kind": kind,
            "model_cost_usd": model_cost_usd,
            "reason": reason,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        adjustment_id = d.pop("adjustment_id")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        created_by = d.pop("created_by")

        kind = ManagedAgentsModelCostAdjustmentResponseKind(d.pop("kind"))




        model_cost_usd = d.pop("model_cost_usd")

        reason = d.pop("reason")

        managed_agents_model_cost_adjustment_response = cls(
            adjustment_id=adjustment_id,
            created_at=created_at,
            created_by=created_by,
            kind=kind,
            model_cost_usd=model_cost_usd,
            reason=reason,
        )


        managed_agents_model_cost_adjustment_response.additional_properties = d
        return managed_agents_model_cost_adjustment_response

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
