from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.billing_unit import BillingUnit
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_plan_component import NestedPlanComponent
    from ..models.organization_group import OrganizationGroup
    from ..models.provider_plan_details_future_prices import ProviderPlanDetailsFuturePrices
    from ..models.provider_plan_details_prices import ProviderPlanDetailsPrices
    from ..models.provider_plan_details_quotas import ProviderPlanDetailsQuotas


T = TypeVar("T", bound="ProviderPlanDetails")


@_attrs_define
class ProviderPlanDetails:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        is_active (bool):
        init_price (float):
        switch_price (float):
        organization_groups (list['OrganizationGroup']):
        components (list['NestedPlanComponent']):
        offering (str):
        prices (ProviderPlanDetailsPrices):
        future_prices (ProviderPlanDetailsFuturePrices):
        quotas (ProviderPlanDetailsQuotas):
        resources_count (int):
        plan_type (str):
        minimal_price (float):
        description (Union[Unset, str]):
        article_code (Union[Unset, str]):
        max_amount (Union[None, Unset, int]): Maximum number of plans that could be active. Plan is disabled when
            maximum amount is reached.
        archived (Union[Unset, bool]): Forbids creation of new resources.
        unit_price (Union[Unset, str]):
        unit (Union[Unset, BillingUnit]):
        backend_id (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    name: str
    is_active: bool
    init_price: float
    switch_price: float
    organization_groups: list["OrganizationGroup"]
    components: list["NestedPlanComponent"]
    offering: str
    prices: "ProviderPlanDetailsPrices"
    future_prices: "ProviderPlanDetailsFuturePrices"
    quotas: "ProviderPlanDetailsQuotas"
    resources_count: int
    plan_type: str
    minimal_price: float
    description: Union[Unset, str] = UNSET
    article_code: Union[Unset, str] = UNSET
    max_amount: Union[None, Unset, int] = UNSET
    archived: Union[Unset, bool] = UNSET
    unit_price: Union[Unset, str] = UNSET
    unit: Union[Unset, BillingUnit] = UNSET
    backend_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        is_active = self.is_active

        init_price = self.init_price

        switch_price = self.switch_price

        organization_groups = []
        for organization_groups_item_data in self.organization_groups:
            organization_groups_item = organization_groups_item_data.to_dict()
            organization_groups.append(organization_groups_item)

        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()
            components.append(components_item)

        offering = self.offering

        prices = self.prices.to_dict()

        future_prices = self.future_prices.to_dict()

        quotas = self.quotas.to_dict()

        resources_count = self.resources_count

        plan_type = self.plan_type

        minimal_price = self.minimal_price

        description = self.description

        article_code = self.article_code

        max_amount: Union[None, Unset, int]
        if isinstance(self.max_amount, Unset):
            max_amount = UNSET
        else:
            max_amount = self.max_amount

        archived = self.archived

        unit_price = self.unit_price

        unit: Union[Unset, str] = UNSET
        if not isinstance(self.unit, Unset):
            unit = self.unit.value

        backend_id = self.backend_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "is_active": is_active,
                "init_price": init_price,
                "switch_price": switch_price,
                "organization_groups": organization_groups,
                "components": components,
                "offering": offering,
                "prices": prices,
                "future_prices": future_prices,
                "quotas": quotas,
                "resources_count": resources_count,
                "plan_type": plan_type,
                "minimal_price": minimal_price,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if article_code is not UNSET:
            field_dict["article_code"] = article_code
        if max_amount is not UNSET:
            field_dict["max_amount"] = max_amount
        if archived is not UNSET:
            field_dict["archived"] = archived
        if unit_price is not UNSET:
            field_dict["unit_price"] = unit_price
        if unit is not UNSET:
            field_dict["unit"] = unit
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_plan_component import NestedPlanComponent
        from ..models.organization_group import OrganizationGroup
        from ..models.provider_plan_details_future_prices import ProviderPlanDetailsFuturePrices
        from ..models.provider_plan_details_prices import ProviderPlanDetailsPrices
        from ..models.provider_plan_details_quotas import ProviderPlanDetailsQuotas

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        is_active = d.pop("is_active")

        init_price = d.pop("init_price")

        switch_price = d.pop("switch_price")

        organization_groups = []
        _organization_groups = d.pop("organization_groups")
        for organization_groups_item_data in _organization_groups:
            organization_groups_item = OrganizationGroup.from_dict(organization_groups_item_data)

            organization_groups.append(organization_groups_item)

        components = []
        _components = d.pop("components")
        for components_item_data in _components:
            components_item = NestedPlanComponent.from_dict(components_item_data)

            components.append(components_item)

        offering = d.pop("offering")

        prices = ProviderPlanDetailsPrices.from_dict(d.pop("prices"))

        future_prices = ProviderPlanDetailsFuturePrices.from_dict(d.pop("future_prices"))

        quotas = ProviderPlanDetailsQuotas.from_dict(d.pop("quotas"))

        resources_count = d.pop("resources_count")

        plan_type = d.pop("plan_type")

        minimal_price = d.pop("minimal_price")

        description = d.pop("description", UNSET)

        article_code = d.pop("article_code", UNSET)

        def _parse_max_amount(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_amount = _parse_max_amount(d.pop("max_amount", UNSET))

        archived = d.pop("archived", UNSET)

        unit_price = d.pop("unit_price", UNSET)

        _unit = d.pop("unit", UNSET)
        unit: Union[Unset, BillingUnit]
        if isinstance(_unit, Unset):
            unit = UNSET
        else:
            unit = BillingUnit(_unit)

        backend_id = d.pop("backend_id", UNSET)

        provider_plan_details = cls(
            url=url,
            uuid=uuid,
            name=name,
            is_active=is_active,
            init_price=init_price,
            switch_price=switch_price,
            organization_groups=organization_groups,
            components=components,
            offering=offering,
            prices=prices,
            future_prices=future_prices,
            quotas=quotas,
            resources_count=resources_count,
            plan_type=plan_type,
            minimal_price=minimal_price,
            description=description,
            article_code=article_code,
            max_amount=max_amount,
            archived=archived,
            unit_price=unit_price,
            unit=unit,
            backend_id=backend_id,
        )

        provider_plan_details.additional_properties = d
        return provider_plan_details

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
