from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_model_cost_attempt_response_completeness import ManagedAgentsModelCostAttemptResponseCompleteness
from ..models.managed_agents_model_cost_attempt_response_kind import ManagedAgentsModelCostAttemptResponseKind
from ..models.managed_agents_model_cost_attempt_response_state import ManagedAgentsModelCostAttemptResponseState
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_model_cost_charge_response import ManagedAgentsModelCostChargeResponse





T = TypeVar("T", bound="ManagedAgentsModelCostAttemptResponse")



@_attrs_define
class ManagedAgentsModelCostAttemptResponse:
    """ One provider call the ledger is accountable for, billed or not. An attempt is reserved before the request is
    dispatched, so a call that failed, was never charged, or left billing unknown stays visible in the accounting
    instead of disappearing from it.

        Example:
            {'attempt_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'catalog_version': 'example', 'charge': {'adjustments':
                [{'adjustment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at': '2026-02-18T09:30:00Z', 'created_by':
                'example', 'kind': 'provider_authority', 'model_cost_usd': 'example', 'reason': 'example'}], 'charge_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'completeness': 'complete', 'components': [{'cache_state': 'none',
                'category': 'input', 'component_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'dimension': 'example', 'modality':
                'text', 'model_cost_usd': 'example', 'price': {'catalog_version': 'example', 'currency': 'USD',
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
                'example', 'recorded_at': '2026-02-18T09:30:00Z'}, 'completeness': 'complete', 'created_at':
                '2026-02-18T09:30:00Z', 'kind': 'model', 'model': 'example', 'model_ref_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'parent_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'provider':
                'example', 'root_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_path': 'example', 'state': 'prepared', 'thread_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at': '2026-02-18T09:30:00Z'}

        Attributes:
            attempt_id (str): Identifier for this attempt (UUID). Derived deterministically from the work that issued the
                call, so a retried dispatch reuses it instead of billing twice; a retry after a dispatch that provably never
                reached billing gets its own derived child id.
            completeness (ManagedAgentsModelCostAttemptResponseCompleteness): Accounting confidence for this attempt: the
                charge's own completeness when a charge exists, otherwise pending while the outcome is still unknown, complete
                for a not_charged attempt that cost nothing, and indeterminate when the call may have been billed without a
                receipt.
            created_at (datetime.datetime): RFC 3339 timestamp of when the attempt was reserved, before the provider request
                was sent. Attempts page in this order.
            kind (ManagedAgentsModelCostAttemptResponseKind): model for inference, provider_tool for a metered provider-side
                tool, or sandbox_compute for elapsed sandbox runtime.
            provider (str): Provider the call was dispatched to, e.g. anthropic, openai, gemini, or litellm for a gateway-
                routed call.
            root_session_id (str): Root session of the tree this attempt belongs to (UUID).
            session_id (str): Session the call is attributed to (UUID).
            session_path (str): Position of that session within its tree, as a slash-delimited path of session ids. "/" for
                a root session.
            state (ManagedAgentsModelCostAttemptResponseState): Ledger lifecycle: prepared once the attempt was reserved,
                dispatched once the request was sent, charged once a receipt was persisted, not_charged when the call provably
                never reached billing, and indeterminate when it may have been billed but no usable receipt exists.
            updated_at (datetime.datetime): RFC 3339 timestamp of the attempt's last state change.
            catalog_version (str | Unset): Pricing catalog version pinned when the attempt was reserved. A receipt priced
                against another version is rejected rather than mixed. Empty when the attempt was reserved without a pricing
                catalog.
            charge (ManagedAgentsModelCostChargeResponse | Unset): The billed result of one attempt: the provider receipt,
                the components it was priced into, every adjustment since, and the amounts those produce. A charge is written
                once and never rewritten, so a later correction arrives as an adjustment rather than as an edit. Customers
                receive every amount as billed to their organization, with price snapshots and provider-reported totals
                redacted; only trusted internal callers receive raw ledger amounts. Example: {'adjustments': [{'adjustment_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at': '2026-02-18T09:30:00Z', 'created_by': 'example', 'kind':
                'provider_authority', 'model_cost_usd': 'example', 'reason': 'example'}], 'charge_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'completeness': 'complete', 'components': [{'cache_state': 'none',
                'category': 'input', 'component_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'dimension': 'example', 'modality':
                'text', 'model_cost_usd': 'example', 'price': {'catalog_version': 'example', 'currency': 'USD',
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
                'example', 'recorded_at': '2026-02-18T09:30:00Z'}.
            model (str | Unset): Model id the call requested, as sent on the wire.
            model_ref_id (str | Unset): Model reference in the catalog the model was resolved from (UUID). Empty when the
                session named a gateway model id instead of a catalog entry.
            parent_session_id (str | Unset): Parent of the session the call is attributed to (UUID). Empty when that session
                is the root.
            thread_id (str | Unset): Thread within a multi-agent session the call belongs to. Empty when the attempt was
                recorded without thread attribution.
     """

    attempt_id: str
    completeness: ManagedAgentsModelCostAttemptResponseCompleteness
    created_at: datetime.datetime
    kind: ManagedAgentsModelCostAttemptResponseKind
    provider: str
    root_session_id: str
    session_id: str
    session_path: str
    state: ManagedAgentsModelCostAttemptResponseState
    updated_at: datetime.datetime
    catalog_version: str | Unset = UNSET
    charge: ManagedAgentsModelCostChargeResponse | Unset = UNSET
    model: str | Unset = UNSET
    model_ref_id: str | Unset = UNSET
    parent_session_id: str | Unset = UNSET
    thread_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_model_cost_charge_response import ManagedAgentsModelCostChargeResponse # noqa: PLC0415
        attempt_id = self.attempt_id

        completeness = self.completeness.value

        created_at = self.created_at.isoformat()

        kind = self.kind.value

        provider = self.provider

        root_session_id = self.root_session_id

        session_id = self.session_id

        session_path = self.session_path

        state = self.state.value

        updated_at = self.updated_at.isoformat()

        catalog_version = self.catalog_version

        charge: dict[str, Any] | Unset = UNSET
        if not isinstance(self.charge, Unset):
            charge = self.charge.to_dict()

        model = self.model

        model_ref_id = self.model_ref_id

        parent_session_id = self.parent_session_id

        thread_id = self.thread_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "attempt_id": attempt_id,
            "completeness": completeness,
            "created_at": created_at,
            "kind": kind,
            "provider": provider,
            "root_session_id": root_session_id,
            "session_id": session_id,
            "session_path": session_path,
            "state": state,
            "updated_at": updated_at,
        })
        if catalog_version is not UNSET:
            field_dict["catalog_version"] = catalog_version
        if charge is not UNSET:
            field_dict["charge"] = charge
        if model is not UNSET:
            field_dict["model"] = model
        if model_ref_id is not UNSET:
            field_dict["model_ref_id"] = model_ref_id
        if parent_session_id is not UNSET:
            field_dict["parent_session_id"] = parent_session_id
        if thread_id is not UNSET:
            field_dict["thread_id"] = thread_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_model_cost_charge_response import ManagedAgentsModelCostChargeResponse # noqa: PLC0415
        d = dict(src_dict)
        attempt_id = d.pop("attempt_id")

        completeness = ManagedAgentsModelCostAttemptResponseCompleteness(d.pop("completeness"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        kind = ManagedAgentsModelCostAttemptResponseKind(d.pop("kind"))




        provider = d.pop("provider")

        root_session_id = d.pop("root_session_id")

        session_id = d.pop("session_id")

        session_path = d.pop("session_path")

        state = ManagedAgentsModelCostAttemptResponseState(d.pop("state"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        catalog_version = d.pop("catalog_version", UNSET)

        _charge = d.pop("charge", UNSET)
        charge: ManagedAgentsModelCostChargeResponse | Unset
        if isinstance(_charge,  Unset):
            charge = UNSET
        else:
            charge = ManagedAgentsModelCostChargeResponse.from_dict(_charge)




        model = d.pop("model", UNSET)

        model_ref_id = d.pop("model_ref_id", UNSET)

        parent_session_id = d.pop("parent_session_id", UNSET)

        thread_id = d.pop("thread_id", UNSET)

        managed_agents_model_cost_attempt_response = cls(
            attempt_id=attempt_id,
            completeness=completeness,
            created_at=created_at,
            kind=kind,
            provider=provider,
            root_session_id=root_session_id,
            session_id=session_id,
            session_path=session_path,
            state=state,
            updated_at=updated_at,
            catalog_version=catalog_version,
            charge=charge,
            model=model,
            model_ref_id=model_ref_id,
            parent_session_id=parent_session_id,
            thread_id=thread_id,
        )


        managed_agents_model_cost_attempt_response.additional_properties = d
        return managed_agents_model_cost_attempt_response

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
