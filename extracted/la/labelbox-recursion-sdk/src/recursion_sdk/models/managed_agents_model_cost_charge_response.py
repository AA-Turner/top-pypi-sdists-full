from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_model_cost_charge_response_completeness import ManagedAgentsModelCostChargeResponseCompleteness
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_model_cost_adjustment_response import ManagedAgentsModelCostAdjustmentResponse
  from ..models.managed_agents_model_cost_component_response import ManagedAgentsModelCostComponentResponse
  from ..models.managed_agents_model_cost_receipt_response import ManagedAgentsModelCostReceiptResponse





T = TypeVar("T", bound="ManagedAgentsModelCostChargeResponse")



@_attrs_define
class ManagedAgentsModelCostChargeResponse:
    """ The billed result of one attempt: the provider receipt, the components it was priced into, every adjustment since,
    and the amounts those produce. A charge is written once and never rewritten, so a later correction arrives as an
    adjustment rather than as an edit. Customers receive every amount as billed to their organization, with price
    snapshots and provider-reported totals redacted; only trusted internal callers receive raw ledger amounts.

        Example:
            {'adjustments': [{'adjustment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at': '2026-02-18T09:30:00Z',
                'created_by': 'example', 'kind': 'provider_authority', 'model_cost_usd': 'example', 'reason': 'example'}],
                'charge_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'completeness': 'complete', 'components': [{'cache_state':
                'none', 'category': 'input', 'component_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'dimension': 'example',
                'modality': 'text', 'model_cost_usd': 'example', 'price': {'catalog_version': 'example', 'currency': 'USD',
                'denominator_units': 'example', 'model': 'example', 'numerator_nano_usd': 'example', 'provider': 'example',
                'region': 'example', 'rule_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'service_tier': 'example'},
                'price_redacted': True, 'quantity': 'example', 'unit': 'token'}], 'locally_priced_model_cost_usd': 'example',
                'model_cost_usd': 'example', 'original_model_cost_usd': 'example', 'provider_reported_model_cost_usd':
                'example', 'receipt': {'gateway': {'call_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'discount_amount_usd':
                'example', 'margin_amount_usd': 'example', 'margin_percent': 'example', 'original_total_usd': 'example',
                'reported_total_usd': 'example', 'selected_deployment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'selected_model_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'total_state': 'example'}, 'provider_request_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'quantities': [{'cache_state': 'none', 'category': 'input', 'dimension':
                'example', 'modality': 'text', 'quantity': 'example', 'unit': 'token'}], 'recovery': {'method': 'example',
                'recovered_at': '2026-02-18T09:30:00Z', 'reference': 'example'}, 'redacted_fields': ['example'], 'region':
                'example', 'requested_model_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'resolved_model_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'service_tier': 'example', 'source': 'example'}, 'receipt_sha256':
                'example', 'recorded_at': '2026-02-18T09:30:00Z'}

        Attributes:
            adjustments (list[ManagedAgentsModelCostAdjustmentResponse] | None): Signed corrections applied to this charge,
                oldest first. Empty when the locally priced total was accepted as recorded.
            charge_id (str): Identifier for this charge (UUID), always the attempt_id it settles: a charged attempt has
                exactly one charge.
            completeness (ManagedAgentsModelCostChargeResponseCompleteness): Accounting confidence for this charge alone:
                complete when every component is priced, unpriced when none matched a catalog rule, partial when only some cost
                is known or a gateway total could not be trusted, and legacy_partial for charges recorded before the current
                reconciliation rules. A persisted charge is never pending or indeterminate; those states belong to an attempt
                without one.
            components (list[ManagedAgentsModelCostComponentResponse] | None): Priced lines of this charge, one per receipt
                dimension, ordered by component_id.
            locally_priced_model_cost_usd (str): Sum of the components' amounts, i.e. what the pinned price catalog says
                this call cost. Exact canonical decimal USD string.
            model_cost_usd (str): Current ledger amount for this charge, i.e. the locally priced total plus every
                adjustment. This is the amount that rolls up into the session summaries. Exact canonical decimal USD string.
            original_model_cost_usd (str): Ledger amount when this charge was first recorded: the provider-reported total
                when one was authoritative, otherwise the locally priced total. Exact canonical decimal USD string.
            receipt (ManagedAgentsModelCostReceiptResponse): Immutable provider evidence behind one charge: what the
                provider says it served, and how much of it. Amounts are never read from here directly; the components carry the
                priced result, and receipt_sha256 on the charge covers this evidence together with the provider's raw usage
                body. Example: {'gateway': {'call_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'discount_amount_usd': 'example',
                'margin_amount_usd': 'example', 'margin_percent': 'example', 'original_total_usd': 'example',
                'reported_total_usd': 'example', 'selected_deployment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'selected_model_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'total_state': 'example'}, 'provider_request_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'quantities': [{'cache_state': 'none', 'category': 'input', 'dimension':
                'example', 'modality': 'text', 'quantity': 'example', 'unit': 'token'}], 'recovery': {'method': 'example',
                'recovered_at': '2026-02-18T09:30:00Z', 'reference': 'example'}, 'redacted_fields': ['example'], 'region':
                'example', 'requested_model_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'resolved_model_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'service_tier': 'example', 'source': 'example'}.
            receipt_sha256 (str): Lowercase hex SHA-256 over the canonical receipt envelope, which is the provider's raw
                usage body together with the receipt evidence. Re-hashing the receipt proves it has not changed since the charge
                was recorded.
            recorded_at (datetime.datetime): RFC 3339 commit timestamp of when the charge was written to the ledger.
            provider_reported_model_cost_usd (str | Unset): Total the provider or gateway reported for this call, reconciled
                from its exact lexical value. Absent when none was reported or none could be trusted. When it differs from the
                locally priced total, a provider_authority adjustment reconciles the two. Exact canonical decimal USD string.
     """

    adjustments: list[ManagedAgentsModelCostAdjustmentResponse] | None
    charge_id: str
    completeness: ManagedAgentsModelCostChargeResponseCompleteness
    components: list[ManagedAgentsModelCostComponentResponse] | None
    locally_priced_model_cost_usd: str
    model_cost_usd: str
    original_model_cost_usd: str
    receipt: ManagedAgentsModelCostReceiptResponse
    receipt_sha256: str
    recorded_at: datetime.datetime
    provider_reported_model_cost_usd: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_model_cost_adjustment_response import ManagedAgentsModelCostAdjustmentResponse # noqa: PLC0415
        from ..models.managed_agents_model_cost_component_response import ManagedAgentsModelCostComponentResponse # noqa: PLC0415
        from ..models.managed_agents_model_cost_receipt_response import ManagedAgentsModelCostReceiptResponse # noqa: PLC0415
        adjustments: list[dict[str, Any]] | None
        if isinstance(self.adjustments, list):
            adjustments = []
            for adjustments_type_0_item_data in self.adjustments:
                adjustments_type_0_item = adjustments_type_0_item_data.to_dict()
                adjustments.append(adjustments_type_0_item)


        else:
            adjustments = self.adjustments

        charge_id = self.charge_id

        completeness = self.completeness.value

        components: list[dict[str, Any]] | None
        if isinstance(self.components, list):
            components = []
            for components_type_0_item_data in self.components:
                components_type_0_item = components_type_0_item_data.to_dict()
                components.append(components_type_0_item)


        else:
            components = self.components

        locally_priced_model_cost_usd = self.locally_priced_model_cost_usd

        model_cost_usd = self.model_cost_usd

        original_model_cost_usd = self.original_model_cost_usd

        receipt = self.receipt.to_dict()

        receipt_sha256 = self.receipt_sha256

        recorded_at = self.recorded_at.isoformat()

        provider_reported_model_cost_usd = self.provider_reported_model_cost_usd


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "adjustments": adjustments,
            "charge_id": charge_id,
            "completeness": completeness,
            "components": components,
            "locally_priced_model_cost_usd": locally_priced_model_cost_usd,
            "model_cost_usd": model_cost_usd,
            "original_model_cost_usd": original_model_cost_usd,
            "receipt": receipt,
            "receipt_sha256": receipt_sha256,
            "recorded_at": recorded_at,
        })
        if provider_reported_model_cost_usd is not UNSET:
            field_dict["provider_reported_model_cost_usd"] = provider_reported_model_cost_usd

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_model_cost_adjustment_response import ManagedAgentsModelCostAdjustmentResponse # noqa: PLC0415
        from ..models.managed_agents_model_cost_component_response import ManagedAgentsModelCostComponentResponse # noqa: PLC0415
        from ..models.managed_agents_model_cost_receipt_response import ManagedAgentsModelCostReceiptResponse # noqa: PLC0415
        d = dict(src_dict)
        def _parse_adjustments(data: object) -> list[ManagedAgentsModelCostAdjustmentResponse] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                adjustments_type_0 = []
                _adjustments_type_0 = data
                for adjustments_type_0_item_data in (_adjustments_type_0):
                    adjustments_type_0_item = ManagedAgentsModelCostAdjustmentResponse.from_dict(adjustments_type_0_item_data)



                    adjustments_type_0.append(adjustments_type_0_item)

                return adjustments_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsModelCostAdjustmentResponse] | None, data)

        adjustments = _parse_adjustments(d.pop("adjustments"))


        charge_id = d.pop("charge_id")

        completeness = ManagedAgentsModelCostChargeResponseCompleteness(d.pop("completeness"))




        def _parse_components(data: object) -> list[ManagedAgentsModelCostComponentResponse] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                components_type_0 = []
                _components_type_0 = data
                for components_type_0_item_data in (_components_type_0):
                    components_type_0_item = ManagedAgentsModelCostComponentResponse.from_dict(components_type_0_item_data)



                    components_type_0.append(components_type_0_item)

                return components_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsModelCostComponentResponse] | None, data)

        components = _parse_components(d.pop("components"))


        locally_priced_model_cost_usd = d.pop("locally_priced_model_cost_usd")

        model_cost_usd = d.pop("model_cost_usd")

        original_model_cost_usd = d.pop("original_model_cost_usd")

        receipt = ManagedAgentsModelCostReceiptResponse.from_dict(d.pop("receipt"))




        receipt_sha256 = d.pop("receipt_sha256")

        recorded_at = datetime.datetime.fromisoformat(d.pop("recorded_at"))




        provider_reported_model_cost_usd = d.pop("provider_reported_model_cost_usd", UNSET)

        managed_agents_model_cost_charge_response = cls(
            adjustments=adjustments,
            charge_id=charge_id,
            completeness=completeness,
            components=components,
            locally_priced_model_cost_usd=locally_priced_model_cost_usd,
            model_cost_usd=model_cost_usd,
            original_model_cost_usd=original_model_cost_usd,
            receipt=receipt,
            receipt_sha256=receipt_sha256,
            recorded_at=recorded_at,
            provider_reported_model_cost_usd=provider_reported_model_cost_usd,
        )


        managed_agents_model_cost_charge_response.additional_properties = d
        return managed_agents_model_cost_charge_response

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
