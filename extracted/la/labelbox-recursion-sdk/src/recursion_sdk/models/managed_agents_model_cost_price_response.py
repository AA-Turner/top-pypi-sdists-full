from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_model_cost_price_response_currency import ManagedAgentsModelCostPriceResponseCurrency
from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsModelCostPriceResponse")



@_attrs_define
class ManagedAgentsModelCostPriceResponse:
    """ Price one component was charged at, snapshotted from the pricing catalog when the charge was recorded so the amount
    stays reproducible after the catalog changes. The rate is numerator_nano_usd per denominator_units of quantity, in
    nano-USD (1,000,000,000 nano-USD = 1 USD), and a component's amount is quantity * numerator / denominator rounded
    half to even exactly once. Returned only to trusted internal callers that read raw cost.

        Example:
            {'catalog_version': 'example', 'currency': 'USD', 'denominator_units': 'example', 'model': 'example',
                'numerator_nano_usd': 'example', 'provider': 'example', 'region': 'example', 'rule_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'service_tier': 'example'}

        Attributes:
            catalog_version (str): Pricing catalog version this snapshot was taken from, always the version pinned on the
                attempt. A receipt priced against a different version is rejected rather than mixed.
            currency (ManagedAgentsModelCostPriceResponseCurrency): Currency of the rate. Always USD; the ledger holds no
                other currency.
            denominator_units (str): Exact base-10 integer string.
            numerator_nano_usd (str): Exact base-10 integer string.
            provider (str): Provider this rate priced, always the attempt's own provider.
            rule_id (str): Rule within that catalog version that matched this component. The most specific matching rule
                wins, and an ambiguous tie is rejected rather than guessed.
            model (str | Unset): Model id the rate was applied to: the receipt's resolved model, or the requested model when
                the provider reported no resolution. Empty only when neither recorded one.
            region (str | Unset): Region the rate was applied at, always equal to the receipt's region. Empty when the
                provider reported none.
            service_tier (str | Unset): Service tier the rate was applied at, always equal to the receipt's service_tier.
                Empty when the provider reported no tier.
     """

    catalog_version: str
    currency: ManagedAgentsModelCostPriceResponseCurrency
    denominator_units: str
    numerator_nano_usd: str
    provider: str
    rule_id: str
    model: str | Unset = UNSET
    region: str | Unset = UNSET
    service_tier: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        catalog_version = self.catalog_version

        currency = self.currency.value

        denominator_units = self.denominator_units

        numerator_nano_usd = self.numerator_nano_usd

        provider = self.provider

        rule_id = self.rule_id

        model = self.model

        region = self.region

        service_tier = self.service_tier


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "catalog_version": catalog_version,
            "currency": currency,
            "denominator_units": denominator_units,
            "numerator_nano_usd": numerator_nano_usd,
            "provider": provider,
            "rule_id": rule_id,
        })
        if model is not UNSET:
            field_dict["model"] = model
        if region is not UNSET:
            field_dict["region"] = region
        if service_tier is not UNSET:
            field_dict["service_tier"] = service_tier

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        catalog_version = d.pop("catalog_version")

        currency = ManagedAgentsModelCostPriceResponseCurrency(d.pop("currency"))




        denominator_units = d.pop("denominator_units")

        numerator_nano_usd = d.pop("numerator_nano_usd")

        provider = d.pop("provider")

        rule_id = d.pop("rule_id")

        model = d.pop("model", UNSET)

        region = d.pop("region", UNSET)

        service_tier = d.pop("service_tier", UNSET)

        managed_agents_model_cost_price_response = cls(
            catalog_version=catalog_version,
            currency=currency,
            denominator_units=denominator_units,
            numerator_nano_usd=numerator_nano_usd,
            provider=provider,
            rule_id=rule_id,
            model=model,
            region=region,
            service_tier=service_tier,
        )


        managed_agents_model_cost_price_response.additional_properties = d
        return managed_agents_model_cost_price_response

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
