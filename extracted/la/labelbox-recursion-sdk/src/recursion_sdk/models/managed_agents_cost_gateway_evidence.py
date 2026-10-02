from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsCostGatewayEvidence")



@_attrs_define
class ManagedAgentsCostGatewayEvidence:
    """ Transport-level evidence from the LiteLLM gateway for one attempt, read from response headers rather than from the
    provider usage body. The gateway's own total is the authoritative amount for a gateway-routed call, so it is kept
    here exactly as sent alongside the fields needed to audit it. Recorded only when the attempt's provider is litellm,
    where it is required.

        Example:
            {'call_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'discount_amount_usd': 'example', 'margin_amount_usd':
                'example', 'margin_percent': 'example', 'original_total_usd': 'example', 'reported_total_usd': 'example',
                'selected_deployment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'selected_model_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'total_state': 'example'}

        Attributes:
            total_state (str): Whether the gateway's cost header can be trusted as this attempt's total: authoritative when
                an exact total arrived bound to a call id, missing when no header was sent, and invalid when one was sent but
                could not be parsed, exceeded the evidence size bound, or arrived without a call id. Anything other than
                authoritative forces the charge to partial.
            call_id (str | Unset): Gateway's own call id from x-litellm-call-id, which names the same round trip in gateway
                logs and must equal the receipt's provider_request_id. Required before a reported total is treated as
                authoritative, and withheld from callers without RL_DATA_READ.
            discount_amount_usd (str | Unset): Discount the gateway applied, from x-litellm-response-cost-discount-amount,
                as a signed lexical decimal USD string. Audit evidence only. Absent when not sent or dropped as invalid, and
                withheld from callers that do not read raw cost.
            margin_amount_usd (str | Unset): Gateway margin on this call, from x-litellm-response-cost-margin-amount, as a
                signed lexical decimal USD string. Audit evidence only. Absent when not sent or dropped as invalid, and withheld
                from callers that do not read raw cost.
            margin_percent (str | Unset): Gateway margin as a percentage, from x-litellm-response-cost-margin-percent, as a
                signed lexical decimal. Audit evidence only. Absent when not sent or dropped as invalid, and withheld from
                callers that do not read raw cost.
            original_total_usd (str | Unset): Pre-discount gateway total from x-litellm-response-cost-original, as a lexical
                decimal USD string. Audit evidence only; it never becomes the ledger amount. Absent when not sent or dropped as
                invalid, and withheld from callers that do not read raw cost.
            reported_total_usd (str | Unset): Exact lexical value of the gateway's x-litellm-response-cost header, preserved
                character for character including scientific notation, and reconciled into the charge's
                provider_reported_model_cost_usd. Replaced with sha256:<digest> when the header exceeded the 128-byte evidence
                bound. Absent when total_state is missing.
            selected_deployment_id (str | Unset): Gateway deployment the call landed on, from x-litellm-model-id, used to
                match deployment-specific pricing rules. Withheld from callers without RL_DATA_READ.
            selected_model_id (str | Unset): Upstream model the gateway routed to, from x-litellm-model-name. This is the
                model the components were priced against, not the alias the request asked for. Withheld from callers without
                RL_DATA_READ.
     """

    total_state: str
    call_id: str | Unset = UNSET
    discount_amount_usd: str | Unset = UNSET
    margin_amount_usd: str | Unset = UNSET
    margin_percent: str | Unset = UNSET
    original_total_usd: str | Unset = UNSET
    reported_total_usd: str | Unset = UNSET
    selected_deployment_id: str | Unset = UNSET
    selected_model_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        total_state = self.total_state

        call_id = self.call_id

        discount_amount_usd = self.discount_amount_usd

        margin_amount_usd = self.margin_amount_usd

        margin_percent = self.margin_percent

        original_total_usd = self.original_total_usd

        reported_total_usd = self.reported_total_usd

        selected_deployment_id = self.selected_deployment_id

        selected_model_id = self.selected_model_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "total_state": total_state,
        })
        if call_id is not UNSET:
            field_dict["call_id"] = call_id
        if discount_amount_usd is not UNSET:
            field_dict["discount_amount_usd"] = discount_amount_usd
        if margin_amount_usd is not UNSET:
            field_dict["margin_amount_usd"] = margin_amount_usd
        if margin_percent is not UNSET:
            field_dict["margin_percent"] = margin_percent
        if original_total_usd is not UNSET:
            field_dict["original_total_usd"] = original_total_usd
        if reported_total_usd is not UNSET:
            field_dict["reported_total_usd"] = reported_total_usd
        if selected_deployment_id is not UNSET:
            field_dict["selected_deployment_id"] = selected_deployment_id
        if selected_model_id is not UNSET:
            field_dict["selected_model_id"] = selected_model_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_state = d.pop("total_state")

        call_id = d.pop("call_id", UNSET)

        discount_amount_usd = d.pop("discount_amount_usd", UNSET)

        margin_amount_usd = d.pop("margin_amount_usd", UNSET)

        margin_percent = d.pop("margin_percent", UNSET)

        original_total_usd = d.pop("original_total_usd", UNSET)

        reported_total_usd = d.pop("reported_total_usd", UNSET)

        selected_deployment_id = d.pop("selected_deployment_id", UNSET)

        selected_model_id = d.pop("selected_model_id", UNSET)

        managed_agents_cost_gateway_evidence = cls(
            total_state=total_state,
            call_id=call_id,
            discount_amount_usd=discount_amount_usd,
            margin_amount_usd=margin_amount_usd,
            margin_percent=margin_percent,
            original_total_usd=original_total_usd,
            reported_total_usd=reported_total_usd,
            selected_deployment_id=selected_deployment_id,
            selected_model_id=selected_model_id,
        )


        managed_agents_cost_gateway_evidence.additional_properties = d
        return managed_agents_cost_gateway_evidence

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
