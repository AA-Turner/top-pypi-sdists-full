from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.billing_unit import BillingUnit
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_public_plan_future_prices import BasePublicPlanFuturePrices
    from ..models.base_public_plan_prices import BasePublicPlanPrices
    from ..models.base_public_plan_quotas import BasePublicPlanQuotas
    from ..models.nested_plan_component import NestedPlanComponent
    from ..models.organization_group import OrganizationGroup


T = TypeVar("T", bound="BasePublicPlan")


@_attrs_define
class BasePublicPlan:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        article_code (Union[Unset, str]):
        max_amount (Union[None, Unset, int]): Maximum number of plans that could be active. Plan is disabled when
            maximum amount is reached.
        archived (Union[Unset, bool]): Forbids creation of new resources.
        is_active (Union[Unset, bool]):
        unit_price (Union[Unset, str]):
        unit (Union[Unset, BillingUnit]):
        init_price (Union[Unset, float]):
        switch_price (Union[Unset, float]):
        backend_id (Union[Unset, str]):
        organization_groups (Union[Unset, list['OrganizationGroup']]):
        components (Union[Unset, list['NestedPlanComponent']]):
        prices (Union[Unset, BasePublicPlanPrices]):
        future_prices (Union[Unset, BasePublicPlanFuturePrices]):
        quotas (Union[Unset, BasePublicPlanQuotas]):
        resources_count (Union[Unset, int]):
        plan_type (Union[Unset, str]):
        minimal_price (Union[Unset, float]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    article_code: Union[Unset, str] = UNSET
    max_amount: Union[None, Unset, int] = UNSET
    archived: Union[Unset, bool] = UNSET
    is_active: Union[Unset, bool] = UNSET
    unit_price: Union[Unset, str] = UNSET
    unit: Union[Unset, BillingUnit] = UNSET
    init_price: Union[Unset, float] = UNSET
    switch_price: Union[Unset, float] = UNSET
    backend_id: Union[Unset, str] = UNSET
    organization_groups: Union[Unset, list["OrganizationGroup"]] = UNSET
    components: Union[Unset, list["NestedPlanComponent"]] = UNSET
    prices: Union[Unset, "BasePublicPlanPrices"] = UNSET
    future_prices: Union[Unset, "BasePublicPlanFuturePrices"] = UNSET
    quotas: Union[Unset, "BasePublicPlanQuotas"] = UNSET
    resources_count: Union[Unset, int] = UNSET
    plan_type: Union[Unset, str] = UNSET
    minimal_price: Union[Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        description = self.description

        article_code = self.article_code

        max_amount: Union[None, Unset, int]
        if isinstance(self.max_amount, Unset):
            max_amount = UNSET
        else:
            max_amount = self.max_amount

        archived = self.archived

        is_active = self.is_active

        unit_price = self.unit_price

        unit: Union[Unset, str] = UNSET
        if not isinstance(self.unit, Unset):
            unit = self.unit.value

        init_price = self.init_price

        switch_price = self.switch_price

        backend_id = self.backend_id

        organization_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.organization_groups, Unset):
            organization_groups = []
            for organization_groups_item_data in self.organization_groups:
                organization_groups_item = organization_groups_item_data.to_dict()
                organization_groups.append(organization_groups_item)

        components: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.components, Unset):
            components = []
            for components_item_data in self.components:
                components_item = components_item_data.to_dict()
                components.append(components_item)

        prices: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.prices, Unset):
            prices = self.prices.to_dict()

        future_prices: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.future_prices, Unset):
            future_prices = self.future_prices.to_dict()

        quotas: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.quotas, Unset):
            quotas = self.quotas.to_dict()

        resources_count = self.resources_count

        plan_type = self.plan_type

        minimal_price = self.minimal_price

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if article_code is not UNSET:
            field_dict["article_code"] = article_code
        if max_amount is not UNSET:
            field_dict["max_amount"] = max_amount
        if archived is not UNSET:
            field_dict["archived"] = archived
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if unit_price is not UNSET:
            field_dict["unit_price"] = unit_price
        if unit is not UNSET:
            field_dict["unit"] = unit
        if init_price is not UNSET:
            field_dict["init_price"] = init_price
        if switch_price is not UNSET:
            field_dict["switch_price"] = switch_price
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if organization_groups is not UNSET:
            field_dict["organization_groups"] = organization_groups
        if components is not UNSET:
            field_dict["components"] = components
        if prices is not UNSET:
            field_dict["prices"] = prices
        if future_prices is not UNSET:
            field_dict["future_prices"] = future_prices
        if quotas is not UNSET:
            field_dict["quotas"] = quotas
        if resources_count is not UNSET:
            field_dict["resources_count"] = resources_count
        if plan_type is not UNSET:
            field_dict["plan_type"] = plan_type
        if minimal_price is not UNSET:
            field_dict["minimal_price"] = minimal_price

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_public_plan_future_prices import BasePublicPlanFuturePrices
        from ..models.base_public_plan_prices import BasePublicPlanPrices
        from ..models.base_public_plan_quotas import BasePublicPlanQuotas
        from ..models.nested_plan_component import NestedPlanComponent
        from ..models.organization_group import OrganizationGroup

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        name = d.pop("name", UNSET)

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

        is_active = d.pop("is_active", UNSET)

        unit_price = d.pop("unit_price", UNSET)

        _unit = d.pop("unit", UNSET)
        unit: Union[Unset, BillingUnit]
        if isinstance(_unit, Unset):
            unit = UNSET
        else:
            unit = BillingUnit(_unit)

        init_price = d.pop("init_price", UNSET)

        switch_price = d.pop("switch_price", UNSET)

        backend_id = d.pop("backend_id", UNSET)

        organization_groups = []
        _organization_groups = d.pop("organization_groups", UNSET)
        for organization_groups_item_data in _organization_groups or []:
            organization_groups_item = OrganizationGroup.from_dict(organization_groups_item_data)

            organization_groups.append(organization_groups_item)

        components = []
        _components = d.pop("components", UNSET)
        for components_item_data in _components or []:
            components_item = NestedPlanComponent.from_dict(components_item_data)

            components.append(components_item)

        _prices = d.pop("prices", UNSET)
        prices: Union[Unset, BasePublicPlanPrices]
        if isinstance(_prices, Unset):
            prices = UNSET
        else:
            prices = BasePublicPlanPrices.from_dict(_prices)

        _future_prices = d.pop("future_prices", UNSET)
        future_prices: Union[Unset, BasePublicPlanFuturePrices]
        if isinstance(_future_prices, Unset):
            future_prices = UNSET
        else:
            future_prices = BasePublicPlanFuturePrices.from_dict(_future_prices)

        _quotas = d.pop("quotas", UNSET)
        quotas: Union[Unset, BasePublicPlanQuotas]
        if isinstance(_quotas, Unset):
            quotas = UNSET
        else:
            quotas = BasePublicPlanQuotas.from_dict(_quotas)

        resources_count = d.pop("resources_count", UNSET)

        plan_type = d.pop("plan_type", UNSET)

        minimal_price = d.pop("minimal_price", UNSET)

        base_public_plan = cls(
            url=url,
            uuid=uuid,
            name=name,
            description=description,
            article_code=article_code,
            max_amount=max_amount,
            archived=archived,
            is_active=is_active,
            unit_price=unit_price,
            unit=unit,
            init_price=init_price,
            switch_price=switch_price,
            backend_id=backend_id,
            organization_groups=organization_groups,
            components=components,
            prices=prices,
            future_prices=future_prices,
            quotas=quotas,
            resources_count=resources_count,
            plan_type=plan_type,
            minimal_price=minimal_price,
        )

        base_public_plan.additional_properties = d
        return base_public_plan

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
