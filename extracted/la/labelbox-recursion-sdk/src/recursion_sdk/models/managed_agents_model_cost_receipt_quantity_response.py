from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_model_cost_receipt_quantity_response_cache_state import ManagedAgentsModelCostReceiptQuantityResponseCacheState
from ..models.managed_agents_model_cost_receipt_quantity_response_category import ManagedAgentsModelCostReceiptQuantityResponseCategory
from ..models.managed_agents_model_cost_receipt_quantity_response_modality import ManagedAgentsModelCostReceiptQuantityResponseModality
from ..models.managed_agents_model_cost_receipt_quantity_response_unit import ManagedAgentsModelCostReceiptQuantityResponseUnit






T = TypeVar("T", bound="ManagedAgentsModelCostReceiptQuantityResponse")



@_attrs_define
class ManagedAgentsModelCostReceiptQuantityResponse:
    """ One billable quantity exactly as the provider reported it, before any pricing. Receipt quantities are the audit
    trail behind a charge: each priced component reconciles to exactly one quantity of the same dimension, with the same
    category, modality, cache state, unit, and count.

        Example:
            {'cache_state': 'none', 'category': 'input', 'dimension': 'example', 'modality': 'text', 'quantity': 'example',
                'unit': 'token'}

        Attributes:
            cache_state (ManagedAgentsModelCostReceiptQuantityResponseCacheState): Prompt-cache disposition: none for
                uncached tokens, read for a cache hit, and write_5m or write_1h for tokens written into the provider's cache at
                that time to live.
            category (ManagedAgentsModelCostReceiptQuantityResponseCategory): What the quantity was consumed for: model
                input or output, provider-side tools, or compute runtime.
            dimension (str): Field path in the provider's usage body this quantity was read from, e.g. input_tokens,
                cache_creation.ephemeral_5m_input_tokens, or output.reasoning. Unique within a receipt, and the key its priced
                component joins on. A dimension containing .unsupported is a provider aggregate that cannot be attributed to a
                rate, and is never priced.
            modality (ManagedAgentsModelCostReceiptQuantityResponseModality): Content or resource type measured. compute
                marks sandbox runtime rather than model content.
            quantity (str): Exact base-10 integer string.
            unit (ManagedAgentsModelCostReceiptQuantityResponseUnit): What quantity counts: tokens, requests, or elapsed
                compute milliseconds.
     """

    cache_state: ManagedAgentsModelCostReceiptQuantityResponseCacheState
    category: ManagedAgentsModelCostReceiptQuantityResponseCategory
    dimension: str
    modality: ManagedAgentsModelCostReceiptQuantityResponseModality
    quantity: str
    unit: ManagedAgentsModelCostReceiptQuantityResponseUnit
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        cache_state = self.cache_state.value

        category = self.category.value

        dimension = self.dimension

        modality = self.modality.value

        quantity = self.quantity

        unit = self.unit.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "cache_state": cache_state,
            "category": category,
            "dimension": dimension,
            "modality": modality,
            "quantity": quantity,
            "unit": unit,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cache_state = ManagedAgentsModelCostReceiptQuantityResponseCacheState(d.pop("cache_state"))




        category = ManagedAgentsModelCostReceiptQuantityResponseCategory(d.pop("category"))




        dimension = d.pop("dimension")

        modality = ManagedAgentsModelCostReceiptQuantityResponseModality(d.pop("modality"))




        quantity = d.pop("quantity")

        unit = ManagedAgentsModelCostReceiptQuantityResponseUnit(d.pop("unit"))




        managed_agents_model_cost_receipt_quantity_response = cls(
            cache_state=cache_state,
            category=category,
            dimension=dimension,
            modality=modality,
            quantity=quantity,
            unit=unit,
        )


        managed_agents_model_cost_receipt_quantity_response.additional_properties = d
        return managed_agents_model_cost_receipt_quantity_response

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
