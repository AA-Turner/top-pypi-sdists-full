from collections.abc import Mapping
from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..models.blank_enum import BlankEnum
from ..models.country_enum import CountryEnum
from ..types import UNSET, File, Unset

if TYPE_CHECKING:
    from ..models.base_provider_plan_request import BaseProviderPlanRequest
    from ..models.merged_plugin_options_request import MergedPluginOptionsRequest
    from ..models.offering_component_request import OfferingComponentRequest
    from ..models.offering_create_request_form_limits import OfferingCreateRequestFormLimits
    from ..models.offering_options_request import OfferingOptionsRequest


T = TypeVar("T", bound="OfferingCreateRequestForm")


@_attrs_define
class OfferingCreateRequestForm:
    """
    Attributes:
        name (str):
        category (str):
        type_ (str):
        slug (Union[Unset, str]): URL-friendly identifier. Only editable by staff users.
        description (Union[Unset, str]):
        full_description (Union[Unset, str]):
        privacy_policy_link (Union[Unset, str]):
        access_url (Union[Unset, str]): Publicly accessible offering access URL
        customer (Union[None, Unset, str]):
        attributes (Union[Unset, Any]):
        options (Union[Unset, OfferingOptionsRequest]):
        resource_options (Union[Unset, OfferingOptionsRequest]):
        components (Union[Unset, list['OfferingComponentRequest']]):
        plugin_options (Union[Unset, MergedPluginOptionsRequest]):
        vendor_details (Union[Unset, str]):
        getting_started (Union[Unset, str]):
        integration_guide (Union[Unset, str]):
        thumbnail (Union[File, None, Unset]):
        plans (Union[Unset, list['BaseProviderPlanRequest']]):
        shared (Union[Unset, bool]): Accessible to all customers.
        billable (Union[Unset, bool]): Purchase and usage is invoiced.
        datacite_doi (Union[Unset, str]):
        latitude (Union[None, Unset, float]):
        longitude (Union[None, Unset, float]):
        country (Union[BlankEnum, CountryEnum, Unset]): Country code (ISO 3166-1 alpha-2)
        backend_id (Union[Unset, str]):
        backend_id_rules (Union[Unset, Any]): Validation rules for resource backend_id: format regex and uniqueness
            scope.
        image (Union[File, None, Unset]):
        backend_metadata (Union[Unset, Any]):
        compliance_checklist (Union[None, Unset, str]):
        limits (Union[Unset, OfferingCreateRequestFormLimits]):
    """

    name: str
    category: str
    type_: str
    slug: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    full_description: Union[Unset, str] = UNSET
    privacy_policy_link: Union[Unset, str] = UNSET
    access_url: Union[Unset, str] = UNSET
    customer: Union[None, Unset, str] = UNSET
    attributes: Union[Unset, Any] = UNSET
    options: Union[Unset, "OfferingOptionsRequest"] = UNSET
    resource_options: Union[Unset, "OfferingOptionsRequest"] = UNSET
    components: Union[Unset, list["OfferingComponentRequest"]] = UNSET
    plugin_options: Union[Unset, "MergedPluginOptionsRequest"] = UNSET
    vendor_details: Union[Unset, str] = UNSET
    getting_started: Union[Unset, str] = UNSET
    integration_guide: Union[Unset, str] = UNSET
    thumbnail: Union[File, None, Unset] = UNSET
    plans: Union[Unset, list["BaseProviderPlanRequest"]] = UNSET
    shared: Union[Unset, bool] = UNSET
    billable: Union[Unset, bool] = UNSET
    datacite_doi: Union[Unset, str] = UNSET
    latitude: Union[None, Unset, float] = UNSET
    longitude: Union[None, Unset, float] = UNSET
    country: Union[BlankEnum, CountryEnum, Unset] = UNSET
    backend_id: Union[Unset, str] = UNSET
    backend_id_rules: Union[Unset, Any] = UNSET
    image: Union[File, None, Unset] = UNSET
    backend_metadata: Union[Unset, Any] = UNSET
    compliance_checklist: Union[None, Unset, str] = UNSET
    limits: Union[Unset, "OfferingCreateRequestFormLimits"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        category = self.category

        type_ = self.type_

        slug = self.slug

        description = self.description

        full_description = self.full_description

        privacy_policy_link = self.privacy_policy_link

        access_url = self.access_url

        customer: Union[None, Unset, str]
        if isinstance(self.customer, Unset):
            customer = UNSET
        else:
            customer = self.customer

        attributes = self.attributes

        options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.options, Unset):
            options = self.options.to_dict()

        resource_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.resource_options, Unset):
            resource_options = self.resource_options.to_dict()

        components: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.components, Unset):
            components = []
            for components_item_data in self.components:
                components_item = components_item_data.to_dict()
                components.append(components_item)

        plugin_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.plugin_options, Unset):
            plugin_options = self.plugin_options.to_dict()

        vendor_details = self.vendor_details

        getting_started = self.getting_started

        integration_guide = self.integration_guide

        thumbnail: Union[None, Unset, types.FileTypes]
        if isinstance(self.thumbnail, Unset):
            thumbnail = UNSET
        elif isinstance(self.thumbnail, File):
            thumbnail = self.thumbnail.to_tuple()

        else:
            thumbnail = self.thumbnail

        plans: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.plans, Unset):
            plans = []
            for plans_item_data in self.plans:
                plans_item = plans_item_data.to_dict()
                plans.append(plans_item)

        shared = self.shared

        billable = self.billable

        datacite_doi = self.datacite_doi

        latitude: Union[None, Unset, float]
        if isinstance(self.latitude, Unset):
            latitude = UNSET
        else:
            latitude = self.latitude

        longitude: Union[None, Unset, float]
        if isinstance(self.longitude, Unset):
            longitude = UNSET
        else:
            longitude = self.longitude

        country: Union[Unset, str]
        if isinstance(self.country, Unset):
            country = UNSET
        elif isinstance(self.country, CountryEnum):
            country = self.country.value
        else:
            country = self.country.value

        backend_id = self.backend_id

        backend_id_rules = self.backend_id_rules

        image: Union[None, Unset, types.FileTypes]
        if isinstance(self.image, Unset):
            image = UNSET
        elif isinstance(self.image, File):
            image = self.image.to_tuple()

        else:
            image = self.image

        backend_metadata = self.backend_metadata

        compliance_checklist: Union[None, Unset, str]
        if isinstance(self.compliance_checklist, Unset):
            compliance_checklist = UNSET
        else:
            compliance_checklist = self.compliance_checklist

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "category": category,
                "type": type_,
            }
        )
        if slug is not UNSET:
            field_dict["slug"] = slug
        if description is not UNSET:
            field_dict["description"] = description
        if full_description is not UNSET:
            field_dict["full_description"] = full_description
        if privacy_policy_link is not UNSET:
            field_dict["privacy_policy_link"] = privacy_policy_link
        if access_url is not UNSET:
            field_dict["access_url"] = access_url
        if customer is not UNSET:
            field_dict["customer"] = customer
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if options is not UNSET:
            field_dict["options"] = options
        if resource_options is not UNSET:
            field_dict["resource_options"] = resource_options
        if components is not UNSET:
            field_dict["components"] = components
        if plugin_options is not UNSET:
            field_dict["plugin_options"] = plugin_options
        if vendor_details is not UNSET:
            field_dict["vendor_details"] = vendor_details
        if getting_started is not UNSET:
            field_dict["getting_started"] = getting_started
        if integration_guide is not UNSET:
            field_dict["integration_guide"] = integration_guide
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail
        if plans is not UNSET:
            field_dict["plans"] = plans
        if shared is not UNSET:
            field_dict["shared"] = shared
        if billable is not UNSET:
            field_dict["billable"] = billable
        if datacite_doi is not UNSET:
            field_dict["datacite_doi"] = datacite_doi
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if country is not UNSET:
            field_dict["country"] = country
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if backend_id_rules is not UNSET:
            field_dict["backend_id_rules"] = backend_id_rules
        if image is not UNSET:
            field_dict["image"] = image
        if backend_metadata is not UNSET:
            field_dict["backend_metadata"] = backend_metadata
        if compliance_checklist is not UNSET:
            field_dict["compliance_checklist"] = compliance_checklist
        if limits is not UNSET:
            field_dict["limits"] = limits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_provider_plan_request import BaseProviderPlanRequest
        from ..models.merged_plugin_options_request import MergedPluginOptionsRequest
        from ..models.offering_component_request import OfferingComponentRequest
        from ..models.offering_create_request_form_limits import OfferingCreateRequestFormLimits
        from ..models.offering_options_request import OfferingOptionsRequest

        d = dict(src_dict)
        name = d.pop("name")

        category = d.pop("category")

        type_ = d.pop("type")

        slug = d.pop("slug", UNSET)

        description = d.pop("description", UNSET)

        full_description = d.pop("full_description", UNSET)

        privacy_policy_link = d.pop("privacy_policy_link", UNSET)

        access_url = d.pop("access_url", UNSET)

        def _parse_customer(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        customer = _parse_customer(d.pop("customer", UNSET))

        attributes = d.pop("attributes", UNSET)

        _options = d.pop("options", UNSET)
        options: Union[Unset, OfferingOptionsRequest]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = OfferingOptionsRequest.from_dict(_options)

        _resource_options = d.pop("resource_options", UNSET)
        resource_options: Union[Unset, OfferingOptionsRequest]
        if isinstance(_resource_options, Unset):
            resource_options = UNSET
        else:
            resource_options = OfferingOptionsRequest.from_dict(_resource_options)

        components = []
        _components = d.pop("components", UNSET)
        for components_item_data in _components or []:
            components_item = OfferingComponentRequest.from_dict(components_item_data)

            components.append(components_item)

        _plugin_options = d.pop("plugin_options", UNSET)
        plugin_options: Union[Unset, MergedPluginOptionsRequest]
        if isinstance(_plugin_options, Unset):
            plugin_options = UNSET
        else:
            plugin_options = MergedPluginOptionsRequest.from_dict(_plugin_options)

        vendor_details = d.pop("vendor_details", UNSET)

        getting_started = d.pop("getting_started", UNSET)

        integration_guide = d.pop("integration_guide", UNSET)

        def _parse_thumbnail(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                thumbnail_type_0 = File(payload=BytesIO(data))

                return thumbnail_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        thumbnail = _parse_thumbnail(d.pop("thumbnail", UNSET))

        plans = []
        _plans = d.pop("plans", UNSET)
        for plans_item_data in _plans or []:
            plans_item = BaseProviderPlanRequest.from_dict(plans_item_data)

            plans.append(plans_item)

        shared = d.pop("shared", UNSET)

        billable = d.pop("billable", UNSET)

        datacite_doi = d.pop("datacite_doi", UNSET)

        def _parse_latitude(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        latitude = _parse_latitude(d.pop("latitude", UNSET))

        def _parse_longitude(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        longitude = _parse_longitude(d.pop("longitude", UNSET))

        def _parse_country(data: object) -> Union[BlankEnum, CountryEnum, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                country_type_0 = CountryEnum(data)

                return country_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            country_type_1 = BlankEnum(data)

            return country_type_1

        country = _parse_country(d.pop("country", UNSET))

        backend_id = d.pop("backend_id", UNSET)

        backend_id_rules = d.pop("backend_id_rules", UNSET)

        def _parse_image(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                image_type_0 = File(payload=BytesIO(data))

                return image_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        image = _parse_image(d.pop("image", UNSET))

        backend_metadata = d.pop("backend_metadata", UNSET)

        def _parse_compliance_checklist(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        compliance_checklist = _parse_compliance_checklist(d.pop("compliance_checklist", UNSET))

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, OfferingCreateRequestFormLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = OfferingCreateRequestFormLimits.from_dict(_limits)

        offering_create_request_form = cls(
            name=name,
            category=category,
            type_=type_,
            slug=slug,
            description=description,
            full_description=full_description,
            privacy_policy_link=privacy_policy_link,
            access_url=access_url,
            customer=customer,
            attributes=attributes,
            options=options,
            resource_options=resource_options,
            components=components,
            plugin_options=plugin_options,
            vendor_details=vendor_details,
            getting_started=getting_started,
            integration_guide=integration_guide,
            thumbnail=thumbnail,
            plans=plans,
            shared=shared,
            billable=billable,
            datacite_doi=datacite_doi,
            latitude=latitude,
            longitude=longitude,
            country=country,
            backend_id=backend_id,
            backend_id_rules=backend_id_rules,
            image=image,
            backend_metadata=backend_metadata,
            compliance_checklist=compliance_checklist,
            limits=limits,
        )

        offering_create_request_form.additional_properties = d
        return offering_create_request_form

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
