from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_model_cost_component_response_cache_state import ManagedAgentsModelCostComponentResponseCacheState
from ..models.managed_agents_model_cost_component_response_category import ManagedAgentsModelCostComponentResponseCategory
from ..models.managed_agents_model_cost_component_response_modality import ManagedAgentsModelCostComponentResponseModality
from ..models.managed_agents_model_cost_component_response_unit import ManagedAgentsModelCostComponentResponseUnit
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_model_cost_price_response import ManagedAgentsModelCostPriceResponse





T = TypeVar("T", bound="ManagedAgentsModelCostComponentResponse")



@_attrs_define
class ManagedAgentsModelCostComponentResponse:
    """ One priced line of a charge: a receipt quantity joined to the rate it was charged at, and the exact amount that
    produced. Components sum to locally_priced_model_cost_usd, and an unpriced component contributes nothing to it.

        Example:
            {'cache_state': 'none', 'category': 'input', 'component_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'dimension': 'example', 'modality': 'text', 'model_cost_usd': 'example', 'price': {'catalog_version': 'example',
                'currency': 'USD', 'denominator_units': 'example', 'model': 'example', 'numerator_nano_usd': 'example',
                'provider': 'example', 'region': 'example', 'rule_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'service_tier':
                'example'}, 'price_redacted': True, 'quantity': 'example', 'unit': 'token'}

        Attributes:
            cache_state (ManagedAgentsModelCostComponentResponseCacheState): Prompt-cache disposition: none for uncached
                tokens, read for a cache hit, and write_5m or write_1h for tokens written into the provider's cache at that time
                to live.
            category (ManagedAgentsModelCostComponentResponseCategory): What the quantity was consumed for: model input or
                output, provider-side tools, or compute runtime.
            component_id (str): Identifier for this component within its charge. Equal to the dimension it prices, and
                unique per charge.
            dimension (str): Provider usage field this component prices, matching exactly one receipt quantity of the same
                dimension.
            modality (ManagedAgentsModelCostComponentResponseModality): Content or resource type measured. compute marks
                sandbox runtime rather than model content.
            model_cost_usd (str): Exact canonical decimal USD string.
            unit (ManagedAgentsModelCostComponentResponseUnit): What quantity counts: tokens, requests, or elapsed compute
                milliseconds.
            price (ManagedAgentsModelCostPriceResponse | Unset): Price one component was charged at, snapshotted from the
                pricing catalog when the charge was recorded so the amount stays reproducible after the catalog changes. The
                rate is numerator_nano_usd per denominator_units of quantity, in nano-USD (1,000,000,000 nano-USD = 1 USD), and
                a component's amount is quantity * numerator / denominator rounded half to even exactly once. Returned only to
                trusted internal callers that read raw cost. Example: {'catalog_version': 'example', 'currency': 'USD',
                'denominator_units': 'example', 'model': 'example', 'numerator_nano_usd': 'example', 'provider': 'example',
                'region': 'example', 'rule_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'service_tier': 'example'}.
            price_redacted (bool | Unset): True when this component was priced but its private price snapshot was omitted.
            quantity (str | Unset): Exact base-10 integer string. Withheld from customer callers, which see it named in the
                receipt's redacted_fields.
     """

    cache_state: ManagedAgentsModelCostComponentResponseCacheState
    category: ManagedAgentsModelCostComponentResponseCategory
    component_id: str
    dimension: str
    modality: ManagedAgentsModelCostComponentResponseModality
    model_cost_usd: str
    unit: ManagedAgentsModelCostComponentResponseUnit
    price: ManagedAgentsModelCostPriceResponse | Unset = UNSET
    price_redacted: bool | Unset = UNSET
    quantity: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_model_cost_price_response import ManagedAgentsModelCostPriceResponse # noqa: PLC0415
        cache_state = self.cache_state.value

        category = self.category.value

        component_id = self.component_id

        dimension = self.dimension

        modality = self.modality.value

        model_cost_usd = self.model_cost_usd

        unit = self.unit.value

        price: dict[str, Any] | Unset = UNSET
        if not isinstance(self.price, Unset):
            price = self.price.to_dict()

        price_redacted = self.price_redacted

        quantity = self.quantity


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "cache_state": cache_state,
            "category": category,
            "component_id": component_id,
            "dimension": dimension,
            "modality": modality,
            "model_cost_usd": model_cost_usd,
            "unit": unit,
        })
        if price is not UNSET:
            field_dict["price"] = price
        if price_redacted is not UNSET:
            field_dict["price_redacted"] = price_redacted
        if quantity is not UNSET:
            field_dict["quantity"] = quantity

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_model_cost_price_response import ManagedAgentsModelCostPriceResponse # noqa: PLC0415
        d = dict(src_dict)
        cache_state = ManagedAgentsModelCostComponentResponseCacheState(d.pop("cache_state"))




        category = ManagedAgentsModelCostComponentResponseCategory(d.pop("category"))




        component_id = d.pop("component_id")

        dimension = d.pop("dimension")

        modality = ManagedAgentsModelCostComponentResponseModality(d.pop("modality"))




        model_cost_usd = d.pop("model_cost_usd")

        unit = ManagedAgentsModelCostComponentResponseUnit(d.pop("unit"))




        _price = d.pop("price", UNSET)
        price: ManagedAgentsModelCostPriceResponse | Unset
        if isinstance(_price,  Unset):
            price = UNSET
        else:
            price = ManagedAgentsModelCostPriceResponse.from_dict(_price)




        price_redacted = d.pop("price_redacted", UNSET)

        quantity = d.pop("quantity", UNSET)

        managed_agents_model_cost_component_response = cls(
            cache_state=cache_state,
            category=category,
            component_id=component_id,
            dimension=dimension,
            modality=modality,
            model_cost_usd=model_cost_usd,
            unit=unit,
            price=price,
            price_redacted=price_redacted,
            quantity=quantity,
        )


        managed_agents_model_cost_component_response.additional_properties = d
        return managed_agents_model_cost_component_response

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
