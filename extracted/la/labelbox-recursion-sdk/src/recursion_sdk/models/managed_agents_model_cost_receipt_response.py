from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_cost_gateway_evidence import ManagedAgentsCostGatewayEvidence
  from ..models.managed_agents_cost_receipt_recovery import ManagedAgentsCostReceiptRecovery
  from ..models.managed_agents_model_cost_receipt_quantity_response import ManagedAgentsModelCostReceiptQuantityResponse





T = TypeVar("T", bound="ManagedAgentsModelCostReceiptResponse")



@_attrs_define
class ManagedAgentsModelCostReceiptResponse:
    """ Immutable provider evidence behind one charge: what the provider says it served, and how much of it. Amounts are
    never read from here directly; the components carry the priced result, and receipt_sha256 on the charge covers this
    evidence together with the provider's raw usage body.

        Example:
            {'gateway': {'call_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'discount_amount_usd': 'example',
                'margin_amount_usd': 'example', 'margin_percent': 'example', 'original_total_usd': 'example',
                'reported_total_usd': 'example', 'selected_deployment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'selected_model_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'total_state': 'example'}, 'provider_request_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'quantities': [{'cache_state': 'none', 'category': 'input', 'dimension':
                'example', 'modality': 'text', 'quantity': 'example', 'unit': 'token'}], 'recovery': {'method': 'example',
                'recovered_at': '2026-02-18T09:30:00Z', 'reference': 'example'}, 'redacted_fields': ['example'], 'region':
                'example', 'requested_model_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'resolved_model_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'service_tier': 'example', 'source': 'example'}

        Attributes:
            quantities (list[ManagedAgentsModelCostReceiptQuantityResponse] | None): Every billable quantity the provider
                reported, one per dimension. A charge's components reconcile exactly to these. Empty for customer callers, which
                see quantities named in redacted_fields.
            source (str): Provider that authored this usage body, always the attempt's own provider, e.g. anthropic, openai,
                gemini, or litellm.
            gateway (ManagedAgentsCostGatewayEvidence | Unset): Transport-level evidence from the LiteLLM gateway for one
                attempt, read from response headers rather than from the provider usage body. The gateway's own total is the
                authoritative amount for a gateway-routed call, so it is kept here exactly as sent alongside the fields needed
                to audit it. Recorded only when the attempt's provider is litellm, where it is required. Example: {'call_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'discount_amount_usd': 'example', 'margin_amount_usd': 'example',
                'margin_percent': 'example', 'original_total_usd': 'example', 'reported_total_usd': 'example',
                'selected_deployment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'selected_model_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'total_state': 'example'}.
            provider_request_id (str | Unset): Provider's own id for the request, which is how the call is found in provider
                logs. Empty when the provider returned none. Withheld from callers without RL_DATA_READ, which instead see it
                named in redacted_fields.
            recovery (ManagedAgentsCostReceiptRecovery | Unset): How a provider receipt was obtained after the original
                response was lost, so a charge settled out of band is still auditable back to the provider. Example: {'method':
                'example', 'recovered_at': '2026-02-18T09:30:00Z', 'reference': 'example'}.
            redacted_fields (list[str] | Unset): Paths withheld from this receipt, e.g. provider_request_id,
                resolved_model_id, components[].price, or gateway.call_id. Also carries invalid_header:<name> markers for
                gateway headers that failed validation and were dropped from evidence rather than trusted.
            region (str | Unset): Provider region or inference geography the call was served from, when reported. Part of
                the pricing-rule match.
            requested_model_id (str | Unset): Model id the request asked for, as sent on the wire.
            resolved_model_id (str | Unset): Model id the provider reports it actually served, and the id the components
                were priced against. Empty when the provider returned none, and withheld from callers without RL_DATA_READ.
            service_tier (str | Unset): Provider service tier the call was served at, when the provider reports one. Part of
                the pricing-rule match.
     """

    quantities: list[ManagedAgentsModelCostReceiptQuantityResponse] | None
    source: str
    gateway: ManagedAgentsCostGatewayEvidence | Unset = UNSET
    provider_request_id: str | Unset = UNSET
    recovery: ManagedAgentsCostReceiptRecovery | Unset = UNSET
    redacted_fields: list[str] | Unset = UNSET
    region: str | Unset = UNSET
    requested_model_id: str | Unset = UNSET
    resolved_model_id: str | Unset = UNSET
    service_tier: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_cost_gateway_evidence import ManagedAgentsCostGatewayEvidence # noqa: PLC0415
        from ..models.managed_agents_cost_receipt_recovery import ManagedAgentsCostReceiptRecovery # noqa: PLC0415
        from ..models.managed_agents_model_cost_receipt_quantity_response import ManagedAgentsModelCostReceiptQuantityResponse # noqa: PLC0415
        quantities: list[dict[str, Any]] | None
        if isinstance(self.quantities, list):
            quantities = []
            for quantities_type_0_item_data in self.quantities:
                quantities_type_0_item = quantities_type_0_item_data.to_dict()
                quantities.append(quantities_type_0_item)


        else:
            quantities = self.quantities

        source = self.source

        gateway: dict[str, Any] | Unset = UNSET
        if not isinstance(self.gateway, Unset):
            gateway = self.gateway.to_dict()

        provider_request_id = self.provider_request_id

        recovery: dict[str, Any] | Unset = UNSET
        if not isinstance(self.recovery, Unset):
            recovery = self.recovery.to_dict()

        redacted_fields: list[str] | Unset = UNSET
        if not isinstance(self.redacted_fields, Unset):
            redacted_fields = self.redacted_fields



        region = self.region

        requested_model_id = self.requested_model_id

        resolved_model_id = self.resolved_model_id

        service_tier = self.service_tier


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "quantities": quantities,
            "source": source,
        })
        if gateway is not UNSET:
            field_dict["gateway"] = gateway
        if provider_request_id is not UNSET:
            field_dict["provider_request_id"] = provider_request_id
        if recovery is not UNSET:
            field_dict["recovery"] = recovery
        if redacted_fields is not UNSET:
            field_dict["redacted_fields"] = redacted_fields
        if region is not UNSET:
            field_dict["region"] = region
        if requested_model_id is not UNSET:
            field_dict["requested_model_id"] = requested_model_id
        if resolved_model_id is not UNSET:
            field_dict["resolved_model_id"] = resolved_model_id
        if service_tier is not UNSET:
            field_dict["service_tier"] = service_tier

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_cost_gateway_evidence import ManagedAgentsCostGatewayEvidence # noqa: PLC0415
        from ..models.managed_agents_cost_receipt_recovery import ManagedAgentsCostReceiptRecovery # noqa: PLC0415
        from ..models.managed_agents_model_cost_receipt_quantity_response import ManagedAgentsModelCostReceiptQuantityResponse # noqa: PLC0415
        d = dict(src_dict)
        def _parse_quantities(data: object) -> list[ManagedAgentsModelCostReceiptQuantityResponse] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                quantities_type_0 = []
                _quantities_type_0 = data
                for quantities_type_0_item_data in (_quantities_type_0):
                    quantities_type_0_item = ManagedAgentsModelCostReceiptQuantityResponse.from_dict(quantities_type_0_item_data)



                    quantities_type_0.append(quantities_type_0_item)

                return quantities_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsModelCostReceiptQuantityResponse] | None, data)

        quantities = _parse_quantities(d.pop("quantities"))


        source = d.pop("source")

        _gateway = d.pop("gateway", UNSET)
        gateway: ManagedAgentsCostGatewayEvidence | Unset
        if isinstance(_gateway,  Unset):
            gateway = UNSET
        else:
            gateway = ManagedAgentsCostGatewayEvidence.from_dict(_gateway)




        provider_request_id = d.pop("provider_request_id", UNSET)

        _recovery = d.pop("recovery", UNSET)
        recovery: ManagedAgentsCostReceiptRecovery | Unset
        if isinstance(_recovery,  Unset):
            recovery = UNSET
        else:
            recovery = ManagedAgentsCostReceiptRecovery.from_dict(_recovery)




        redacted_fields = cast(list[str], d.pop("redacted_fields", UNSET))


        region = d.pop("region", UNSET)

        requested_model_id = d.pop("requested_model_id", UNSET)

        resolved_model_id = d.pop("resolved_model_id", UNSET)

        service_tier = d.pop("service_tier", UNSET)

        managed_agents_model_cost_receipt_response = cls(
            quantities=quantities,
            source=source,
            gateway=gateway,
            provider_request_id=provider_request_id,
            recovery=recovery,
            redacted_fields=redacted_fields,
            region=region,
            requested_model_id=requested_model_id,
            resolved_model_id=resolved_model_id,
            service_tier=service_tier,
        )


        managed_agents_model_cost_receipt_response.additional_properties = d
        return managed_agents_model_cost_receipt_response

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
