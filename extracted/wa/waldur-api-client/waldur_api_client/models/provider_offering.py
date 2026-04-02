from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.offering_state import OfferingState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_provider_plan import BaseProviderPlan
    from ..models.merged_secret_options import MergedSecretOptions
    from ..models.nested_price_estimate import NestedPriceEstimate
    from ..models.offering_component import OfferingComponent


T = TypeVar("T", bound="ProviderOffering")


@_attrs_define
class ProviderOffering:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        slug (Union[Unset, str]): URL-friendly identifier. Only editable by staff users.
        category_title (Union[Unset, str]):
        type_ (Union[Unset, str]):
        state (Union[Unset, OfferingState]):
        resources_count (Union[Unset, int]):
        billing_price_estimate (Union[Unset, NestedPriceEstimate]):
        components (Union[Unset, list['OfferingComponent']]):
        plans (Union[Unset, list['BaseProviderPlan']]):
        options (Union[Unset, Any]): Fields describing resource provision form.
        resource_options (Union[Unset, Any]): Fields describing resource report form.
        secret_options (Union[Unset, MergedSecretOptions]):
        thumbnail (Union[None, Unset, str]):
    """

    uuid: Union[Unset, UUID] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    slug: Union[Unset, str] = UNSET
    category_title: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    state: Union[Unset, OfferingState] = UNSET
    resources_count: Union[Unset, int] = UNSET
    billing_price_estimate: Union[Unset, "NestedPriceEstimate"] = UNSET
    components: Union[Unset, list["OfferingComponent"]] = UNSET
    plans: Union[Unset, list["BaseProviderPlan"]] = UNSET
    options: Union[Unset, Any] = UNSET
    resource_options: Union[Unset, Any] = UNSET
    secret_options: Union[Unset, "MergedSecretOptions"] = UNSET
    thumbnail: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        name = self.name

        slug = self.slug

        category_title = self.category_title

        type_ = self.type_

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        resources_count = self.resources_count

        billing_price_estimate: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.billing_price_estimate, Unset):
            billing_price_estimate = self.billing_price_estimate.to_dict()

        components: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.components, Unset):
            components = []
            for components_item_data in self.components:
                components_item = components_item_data.to_dict()
                components.append(components_item)

        plans: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.plans, Unset):
            plans = []
            for plans_item_data in self.plans:
                plans_item = plans_item_data.to_dict()
                plans.append(plans_item)

        options = self.options

        resource_options = self.resource_options

        secret_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.secret_options, Unset):
            secret_options = self.secret_options.to_dict()

        thumbnail: Union[None, Unset, str]
        if isinstance(self.thumbnail, Unset):
            thumbnail = UNSET
        else:
            thumbnail = self.thumbnail

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if name is not UNSET:
            field_dict["name"] = name
        if slug is not UNSET:
            field_dict["slug"] = slug
        if category_title is not UNSET:
            field_dict["category_title"] = category_title
        if type_ is not UNSET:
            field_dict["type"] = type_
        if state is not UNSET:
            field_dict["state"] = state
        if resources_count is not UNSET:
            field_dict["resources_count"] = resources_count
        if billing_price_estimate is not UNSET:
            field_dict["billing_price_estimate"] = billing_price_estimate
        if components is not UNSET:
            field_dict["components"] = components
        if plans is not UNSET:
            field_dict["plans"] = plans
        if options is not UNSET:
            field_dict["options"] = options
        if resource_options is not UNSET:
            field_dict["resource_options"] = resource_options
        if secret_options is not UNSET:
            field_dict["secret_options"] = secret_options
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_provider_plan import BaseProviderPlan
        from ..models.merged_secret_options import MergedSecretOptions
        from ..models.nested_price_estimate import NestedPriceEstimate
        from ..models.offering_component import OfferingComponent

        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        name = d.pop("name", UNSET)

        slug = d.pop("slug", UNSET)

        category_title = d.pop("category_title", UNSET)

        type_ = d.pop("type", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, OfferingState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = OfferingState(_state)

        resources_count = d.pop("resources_count", UNSET)

        _billing_price_estimate = d.pop("billing_price_estimate", UNSET)
        billing_price_estimate: Union[Unset, NestedPriceEstimate]
        if isinstance(_billing_price_estimate, Unset):
            billing_price_estimate = UNSET
        else:
            billing_price_estimate = NestedPriceEstimate.from_dict(_billing_price_estimate)

        components = []
        _components = d.pop("components", UNSET)
        for components_item_data in _components or []:
            components_item = OfferingComponent.from_dict(components_item_data)

            components.append(components_item)

        plans = []
        _plans = d.pop("plans", UNSET)
        for plans_item_data in _plans or []:
            plans_item = BaseProviderPlan.from_dict(plans_item_data)

            plans.append(plans_item)

        options = d.pop("options", UNSET)

        resource_options = d.pop("resource_options", UNSET)

        _secret_options = d.pop("secret_options", UNSET)
        secret_options: Union[Unset, MergedSecretOptions]
        if isinstance(_secret_options, Unset):
            secret_options = UNSET
        else:
            secret_options = MergedSecretOptions.from_dict(_secret_options)

        def _parse_thumbnail(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        thumbnail = _parse_thumbnail(d.pop("thumbnail", UNSET))

        provider_offering = cls(
            uuid=uuid,
            customer_uuid=customer_uuid,
            name=name,
            slug=slug,
            category_title=category_title,
            type_=type_,
            state=state,
            resources_count=resources_count,
            billing_price_estimate=billing_price_estimate,
            components=components,
            plans=plans,
            options=options,
            resource_options=resource_options,
            secret_options=secret_options,
            thumbnail=thumbnail,
        )

        provider_offering.additional_properties = d
        return provider_offering

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
