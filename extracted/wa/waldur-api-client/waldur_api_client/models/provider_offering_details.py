import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.blank_enum import BlankEnum
from ..models.core_states import CoreStates
from ..models.country_enum import CountryEnum
from ..models.offering_state import OfferingState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_provider_plan import BaseProviderPlan
    from ..models.integration_status import IntegrationStatus
    from ..models.merged_plugin_options import MergedPluginOptions
    from ..models.merged_secret_options import MergedSecretOptions
    from ..models.nested_endpoint import NestedEndpoint
    from ..models.nested_offering_file import NestedOfferingFile
    from ..models.nested_partition import NestedPartition
    from ..models.nested_role import NestedRole
    from ..models.nested_screenshot import NestedScreenshot
    from ..models.nested_software_catalog import NestedSoftwareCatalog
    from ..models.nested_tag import NestedTag
    from ..models.offering_component import OfferingComponent
    from ..models.offering_options import OfferingOptions
    from ..models.organization_group import OrganizationGroup
    from ..models.provider_offering_details_attributes import ProviderOfferingDetailsAttributes
    from ..models.provider_offering_details_service_attributes import ProviderOfferingDetailsServiceAttributes
    from ..models.quota import Quota


T = TypeVar("T", bound="ProviderOfferingDetails")


@_attrs_define
class ProviderOfferingDetails:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        slug (Union[Unset, str]): URL-friendly identifier. Only editable by staff users.
        description (Union[Unset, str]):
        full_description (Union[Unset, str]):
        privacy_policy_link (Union[Unset, str]):
        access_url (Union[Unset, str]): Publicly accessible offering access URL
        endpoints (Union[Unset, list['NestedEndpoint']]):
        software_catalogs (Union[Unset, list['NestedSoftwareCatalog']]):
        partitions (Union[Unset, list['NestedPartition']]):
        roles (Union[Unset, list['NestedRole']]):
        customer (Union[None, Unset, str]):
        customer_uuid (Union[None, UUID, Unset]):
        customer_name (Union[None, Unset, str]):
        project (Union[None, Unset, str]):
        project_uuid (Union[None, UUID, Unset]):
        project_name (Union[None, Unset, str]):
        category (Union[Unset, str]):
        category_uuid (Union[Unset, UUID]):
        category_title (Union[Unset, str]):
        attributes (Union[Unset, ProviderOfferingDetailsAttributes]):
        options (Union[Unset, OfferingOptions]):
        resource_options (Union[Unset, OfferingOptions]):
        components (Union[Unset, list['OfferingComponent']]):
        plugin_options (Union[Unset, MergedPluginOptions]):
        secret_options (Union[Unset, MergedSecretOptions]):
        service_attributes (Union[Unset, ProviderOfferingDetailsServiceAttributes]):
        state (Union[Unset, OfferingState]):
        vendor_details (Union[Unset, str]):
        getting_started (Union[Unset, str]):
        integration_guide (Union[Unset, str]):
        thumbnail (Union[None, Unset, str]):
        order_count (Union[Unset, int]):
        plans (Union[Unset, list['BaseProviderPlan']]):
        screenshots (Union[Unset, list['NestedScreenshot']]):
        type_ (Union[Unset, str]):
        shared (Union[Unset, bool]): Accessible to all customers.
        billable (Union[Unset, bool]): Purchase and usage is invoiced.
        scope (Union[Unset, str]):
        scope_uuid (Union[None, UUID, Unset]):
        scope_name (Union[None, UUID, Unset]):
        scope_state (Union[CoreStates, None, Unset]):
        scope_error_message (Union[None, Unset, str]):
        files (Union[Unset, list['NestedOfferingFile']]):
        quotas (Union[Unset, list['Quota']]):
        paused_reason (Union[Unset, str]):
        datacite_doi (Union[Unset, str]):
        citation_count (Union[Unset, int]): Number of citations of a DOI
        latitude (Union[None, Unset, float]):
        longitude (Union[None, Unset, float]):
        country (Union[BlankEnum, CountryEnum, Unset]): Country code (ISO 3166-1 alpha-2)
        backend_id (Union[Unset, str]):
        backend_id_rules (Union[Unset, Any]): Validation rules for resource backend_id: format regex and uniqueness
            scope.
        organization_groups (Union[Unset, list['OrganizationGroup']]):
        tags (Union[Unset, list['NestedTag']]):
        image (Union[None, Unset, str]):
        total_customers (Union[None, Unset, int]):
        total_cost (Union[None, Unset, int]):
        total_cost_estimated (Union[None, Unset, int]):
        parent_description (Union[None, Unset, str]):
        parent_uuid (Union[None, UUID, Unset]):
        parent_name (Union[None, Unset, str]):
        backend_metadata (Union[Unset, Any]):
        has_compliance_requirements (Union[Unset, bool]):
        billing_type_classification (Union[Unset, str]): Classify offering components by billing type.
            Returns 'limit_only', 'usage_only', or 'mixed'.
        compliance_checklist (Union[None, Unset, str]):
        integration_status (Union[None, Unset, list['IntegrationStatus']]):
        google_calendar_is_public (Union[None, Unset, bool]):
        google_calendar_link (Union[None, Unset, str]): Get the Google Calendar link for an offering.
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    slug: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    full_description: Union[Unset, str] = UNSET
    privacy_policy_link: Union[Unset, str] = UNSET
    access_url: Union[Unset, str] = UNSET
    endpoints: Union[Unset, list["NestedEndpoint"]] = UNSET
    software_catalogs: Union[Unset, list["NestedSoftwareCatalog"]] = UNSET
    partitions: Union[Unset, list["NestedPartition"]] = UNSET
    roles: Union[Unset, list["NestedRole"]] = UNSET
    customer: Union[None, Unset, str] = UNSET
    customer_uuid: Union[None, UUID, Unset] = UNSET
    customer_name: Union[None, Unset, str] = UNSET
    project: Union[None, Unset, str] = UNSET
    project_uuid: Union[None, UUID, Unset] = UNSET
    project_name: Union[None, Unset, str] = UNSET
    category: Union[Unset, str] = UNSET
    category_uuid: Union[Unset, UUID] = UNSET
    category_title: Union[Unset, str] = UNSET
    attributes: Union[Unset, "ProviderOfferingDetailsAttributes"] = UNSET
    options: Union[Unset, "OfferingOptions"] = UNSET
    resource_options: Union[Unset, "OfferingOptions"] = UNSET
    components: Union[Unset, list["OfferingComponent"]] = UNSET
    plugin_options: Union[Unset, "MergedPluginOptions"] = UNSET
    secret_options: Union[Unset, "MergedSecretOptions"] = UNSET
    service_attributes: Union[Unset, "ProviderOfferingDetailsServiceAttributes"] = UNSET
    state: Union[Unset, OfferingState] = UNSET
    vendor_details: Union[Unset, str] = UNSET
    getting_started: Union[Unset, str] = UNSET
    integration_guide: Union[Unset, str] = UNSET
    thumbnail: Union[None, Unset, str] = UNSET
    order_count: Union[Unset, int] = UNSET
    plans: Union[Unset, list["BaseProviderPlan"]] = UNSET
    screenshots: Union[Unset, list["NestedScreenshot"]] = UNSET
    type_: Union[Unset, str] = UNSET
    shared: Union[Unset, bool] = UNSET
    billable: Union[Unset, bool] = UNSET
    scope: Union[Unset, str] = UNSET
    scope_uuid: Union[None, UUID, Unset] = UNSET
    scope_name: Union[None, UUID, Unset] = UNSET
    scope_state: Union[CoreStates, None, Unset] = UNSET
    scope_error_message: Union[None, Unset, str] = UNSET
    files: Union[Unset, list["NestedOfferingFile"]] = UNSET
    quotas: Union[Unset, list["Quota"]] = UNSET
    paused_reason: Union[Unset, str] = UNSET
    datacite_doi: Union[Unset, str] = UNSET
    citation_count: Union[Unset, int] = UNSET
    latitude: Union[None, Unset, float] = UNSET
    longitude: Union[None, Unset, float] = UNSET
    country: Union[BlankEnum, CountryEnum, Unset] = UNSET
    backend_id: Union[Unset, str] = UNSET
    backend_id_rules: Union[Unset, Any] = UNSET
    organization_groups: Union[Unset, list["OrganizationGroup"]] = UNSET
    tags: Union[Unset, list["NestedTag"]] = UNSET
    image: Union[None, Unset, str] = UNSET
    total_customers: Union[None, Unset, int] = UNSET
    total_cost: Union[None, Unset, int] = UNSET
    total_cost_estimated: Union[None, Unset, int] = UNSET
    parent_description: Union[None, Unset, str] = UNSET
    parent_uuid: Union[None, UUID, Unset] = UNSET
    parent_name: Union[None, Unset, str] = UNSET
    backend_metadata: Union[Unset, Any] = UNSET
    has_compliance_requirements: Union[Unset, bool] = UNSET
    billing_type_classification: Union[Unset, str] = UNSET
    compliance_checklist: Union[None, Unset, str] = UNSET
    integration_status: Union[None, Unset, list["IntegrationStatus"]] = UNSET
    google_calendar_is_public: Union[None, Unset, bool] = UNSET
    google_calendar_link: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        name = self.name

        slug = self.slug

        description = self.description

        full_description = self.full_description

        privacy_policy_link = self.privacy_policy_link

        access_url = self.access_url

        endpoints: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.endpoints, Unset):
            endpoints = []
            for endpoints_item_data in self.endpoints:
                endpoints_item = endpoints_item_data.to_dict()
                endpoints.append(endpoints_item)

        software_catalogs: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.software_catalogs, Unset):
            software_catalogs = []
            for software_catalogs_item_data in self.software_catalogs:
                software_catalogs_item = software_catalogs_item_data.to_dict()
                software_catalogs.append(software_catalogs_item)

        partitions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.partitions, Unset):
            partitions = []
            for partitions_item_data in self.partitions:
                partitions_item = partitions_item_data.to_dict()
                partitions.append(partitions_item)

        roles: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = []
            for roles_item_data in self.roles:
                roles_item = roles_item_data.to_dict()
                roles.append(roles_item)

        customer: Union[None, Unset, str]
        if isinstance(self.customer, Unset):
            customer = UNSET
        else:
            customer = self.customer

        customer_uuid: Union[None, Unset, str]
        if isinstance(self.customer_uuid, Unset):
            customer_uuid = UNSET
        elif isinstance(self.customer_uuid, UUID):
            customer_uuid = str(self.customer_uuid)
        else:
            customer_uuid = self.customer_uuid

        customer_name: Union[None, Unset, str]
        if isinstance(self.customer_name, Unset):
            customer_name = UNSET
        else:
            customer_name = self.customer_name

        project: Union[None, Unset, str]
        if isinstance(self.project, Unset):
            project = UNSET
        else:
            project = self.project

        project_uuid: Union[None, Unset, str]
        if isinstance(self.project_uuid, Unset):
            project_uuid = UNSET
        elif isinstance(self.project_uuid, UUID):
            project_uuid = str(self.project_uuid)
        else:
            project_uuid = self.project_uuid

        project_name: Union[None, Unset, str]
        if isinstance(self.project_name, Unset):
            project_name = UNSET
        else:
            project_name = self.project_name

        category = self.category

        category_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.category_uuid, Unset):
            category_uuid = str(self.category_uuid)

        category_title = self.category_title

        attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

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

        secret_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.secret_options, Unset):
            secret_options = self.secret_options.to_dict()

        service_attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.service_attributes, Unset):
            service_attributes = self.service_attributes.to_dict()

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        vendor_details = self.vendor_details

        getting_started = self.getting_started

        integration_guide = self.integration_guide

        thumbnail: Union[None, Unset, str]
        if isinstance(self.thumbnail, Unset):
            thumbnail = UNSET
        else:
            thumbnail = self.thumbnail

        order_count = self.order_count

        plans: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.plans, Unset):
            plans = []
            for plans_item_data in self.plans:
                plans_item = plans_item_data.to_dict()
                plans.append(plans_item)

        screenshots: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.screenshots, Unset):
            screenshots = []
            for screenshots_item_data in self.screenshots:
                screenshots_item = screenshots_item_data.to_dict()
                screenshots.append(screenshots_item)

        type_ = self.type_

        shared = self.shared

        billable = self.billable

        scope = self.scope

        scope_uuid: Union[None, Unset, str]
        if isinstance(self.scope_uuid, Unset):
            scope_uuid = UNSET
        elif isinstance(self.scope_uuid, UUID):
            scope_uuid = str(self.scope_uuid)
        else:
            scope_uuid = self.scope_uuid

        scope_name: Union[None, Unset, str]
        if isinstance(self.scope_name, Unset):
            scope_name = UNSET
        elif isinstance(self.scope_name, UUID):
            scope_name = str(self.scope_name)
        else:
            scope_name = self.scope_name

        scope_state: Union[None, Unset, str]
        if isinstance(self.scope_state, Unset):
            scope_state = UNSET
        elif isinstance(self.scope_state, CoreStates):
            scope_state = self.scope_state.value
        else:
            scope_state = self.scope_state

        scope_error_message: Union[None, Unset, str]
        if isinstance(self.scope_error_message, Unset):
            scope_error_message = UNSET
        else:
            scope_error_message = self.scope_error_message

        files: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)

        quotas: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.quotas, Unset):
            quotas = []
            for quotas_item_data in self.quotas:
                quotas_item = quotas_item_data.to_dict()
                quotas.append(quotas_item)

        paused_reason = self.paused_reason

        datacite_doi = self.datacite_doi

        citation_count = self.citation_count

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

        organization_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.organization_groups, Unset):
            organization_groups = []
            for organization_groups_item_data in self.organization_groups:
                organization_groups_item = organization_groups_item_data.to_dict()
                organization_groups.append(organization_groups_item)

        tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.to_dict()
                tags.append(tags_item)

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        total_customers: Union[None, Unset, int]
        if isinstance(self.total_customers, Unset):
            total_customers = UNSET
        else:
            total_customers = self.total_customers

        total_cost: Union[None, Unset, int]
        if isinstance(self.total_cost, Unset):
            total_cost = UNSET
        else:
            total_cost = self.total_cost

        total_cost_estimated: Union[None, Unset, int]
        if isinstance(self.total_cost_estimated, Unset):
            total_cost_estimated = UNSET
        else:
            total_cost_estimated = self.total_cost_estimated

        parent_description: Union[None, Unset, str]
        if isinstance(self.parent_description, Unset):
            parent_description = UNSET
        else:
            parent_description = self.parent_description

        parent_uuid: Union[None, Unset, str]
        if isinstance(self.parent_uuid, Unset):
            parent_uuid = UNSET
        elif isinstance(self.parent_uuid, UUID):
            parent_uuid = str(self.parent_uuid)
        else:
            parent_uuid = self.parent_uuid

        parent_name: Union[None, Unset, str]
        if isinstance(self.parent_name, Unset):
            parent_name = UNSET
        else:
            parent_name = self.parent_name

        backend_metadata = self.backend_metadata

        has_compliance_requirements = self.has_compliance_requirements

        billing_type_classification = self.billing_type_classification

        compliance_checklist: Union[None, Unset, str]
        if isinstance(self.compliance_checklist, Unset):
            compliance_checklist = UNSET
        else:
            compliance_checklist = self.compliance_checklist

        integration_status: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.integration_status, Unset):
            integration_status = UNSET
        elif isinstance(self.integration_status, list):
            integration_status = []
            for integration_status_type_0_item_data in self.integration_status:
                integration_status_type_0_item = integration_status_type_0_item_data.to_dict()
                integration_status.append(integration_status_type_0_item)

        else:
            integration_status = self.integration_status

        google_calendar_is_public: Union[None, Unset, bool]
        if isinstance(self.google_calendar_is_public, Unset):
            google_calendar_is_public = UNSET
        else:
            google_calendar_is_public = self.google_calendar_is_public

        google_calendar_link: Union[None, Unset, str]
        if isinstance(self.google_calendar_link, Unset):
            google_calendar_link = UNSET
        else:
            google_calendar_link = self.google_calendar_link

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if created is not UNSET:
            field_dict["created"] = created
        if name is not UNSET:
            field_dict["name"] = name
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
        if endpoints is not UNSET:
            field_dict["endpoints"] = endpoints
        if software_catalogs is not UNSET:
            field_dict["software_catalogs"] = software_catalogs
        if partitions is not UNSET:
            field_dict["partitions"] = partitions
        if roles is not UNSET:
            field_dict["roles"] = roles
        if customer is not UNSET:
            field_dict["customer"] = customer
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if project is not UNSET:
            field_dict["project"] = project
        if project_uuid is not UNSET:
            field_dict["project_uuid"] = project_uuid
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if category is not UNSET:
            field_dict["category"] = category
        if category_uuid is not UNSET:
            field_dict["category_uuid"] = category_uuid
        if category_title is not UNSET:
            field_dict["category_title"] = category_title
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
        if secret_options is not UNSET:
            field_dict["secret_options"] = secret_options
        if service_attributes is not UNSET:
            field_dict["service_attributes"] = service_attributes
        if state is not UNSET:
            field_dict["state"] = state
        if vendor_details is not UNSET:
            field_dict["vendor_details"] = vendor_details
        if getting_started is not UNSET:
            field_dict["getting_started"] = getting_started
        if integration_guide is not UNSET:
            field_dict["integration_guide"] = integration_guide
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail
        if order_count is not UNSET:
            field_dict["order_count"] = order_count
        if plans is not UNSET:
            field_dict["plans"] = plans
        if screenshots is not UNSET:
            field_dict["screenshots"] = screenshots
        if type_ is not UNSET:
            field_dict["type"] = type_
        if shared is not UNSET:
            field_dict["shared"] = shared
        if billable is not UNSET:
            field_dict["billable"] = billable
        if scope is not UNSET:
            field_dict["scope"] = scope
        if scope_uuid is not UNSET:
            field_dict["scope_uuid"] = scope_uuid
        if scope_name is not UNSET:
            field_dict["scope_name"] = scope_name
        if scope_state is not UNSET:
            field_dict["scope_state"] = scope_state
        if scope_error_message is not UNSET:
            field_dict["scope_error_message"] = scope_error_message
        if files is not UNSET:
            field_dict["files"] = files
        if quotas is not UNSET:
            field_dict["quotas"] = quotas
        if paused_reason is not UNSET:
            field_dict["paused_reason"] = paused_reason
        if datacite_doi is not UNSET:
            field_dict["datacite_doi"] = datacite_doi
        if citation_count is not UNSET:
            field_dict["citation_count"] = citation_count
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
        if organization_groups is not UNSET:
            field_dict["organization_groups"] = organization_groups
        if tags is not UNSET:
            field_dict["tags"] = tags
        if image is not UNSET:
            field_dict["image"] = image
        if total_customers is not UNSET:
            field_dict["total_customers"] = total_customers
        if total_cost is not UNSET:
            field_dict["total_cost"] = total_cost
        if total_cost_estimated is not UNSET:
            field_dict["total_cost_estimated"] = total_cost_estimated
        if parent_description is not UNSET:
            field_dict["parent_description"] = parent_description
        if parent_uuid is not UNSET:
            field_dict["parent_uuid"] = parent_uuid
        if parent_name is not UNSET:
            field_dict["parent_name"] = parent_name
        if backend_metadata is not UNSET:
            field_dict["backend_metadata"] = backend_metadata
        if has_compliance_requirements is not UNSET:
            field_dict["has_compliance_requirements"] = has_compliance_requirements
        if billing_type_classification is not UNSET:
            field_dict["billing_type_classification"] = billing_type_classification
        if compliance_checklist is not UNSET:
            field_dict["compliance_checklist"] = compliance_checklist
        if integration_status is not UNSET:
            field_dict["integration_status"] = integration_status
        if google_calendar_is_public is not UNSET:
            field_dict["google_calendar_is_public"] = google_calendar_is_public
        if google_calendar_link is not UNSET:
            field_dict["google_calendar_link"] = google_calendar_link

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_provider_plan import BaseProviderPlan
        from ..models.integration_status import IntegrationStatus
        from ..models.merged_plugin_options import MergedPluginOptions
        from ..models.merged_secret_options import MergedSecretOptions
        from ..models.nested_endpoint import NestedEndpoint
        from ..models.nested_offering_file import NestedOfferingFile
        from ..models.nested_partition import NestedPartition
        from ..models.nested_role import NestedRole
        from ..models.nested_screenshot import NestedScreenshot
        from ..models.nested_software_catalog import NestedSoftwareCatalog
        from ..models.nested_tag import NestedTag
        from ..models.offering_component import OfferingComponent
        from ..models.offering_options import OfferingOptions
        from ..models.organization_group import OrganizationGroup
        from ..models.provider_offering_details_attributes import ProviderOfferingDetailsAttributes
        from ..models.provider_offering_details_service_attributes import ProviderOfferingDetailsServiceAttributes
        from ..models.quota import Quota

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        name = d.pop("name", UNSET)

        slug = d.pop("slug", UNSET)

        description = d.pop("description", UNSET)

        full_description = d.pop("full_description", UNSET)

        privacy_policy_link = d.pop("privacy_policy_link", UNSET)

        access_url = d.pop("access_url", UNSET)

        endpoints = []
        _endpoints = d.pop("endpoints", UNSET)
        for endpoints_item_data in _endpoints or []:
            endpoints_item = NestedEndpoint.from_dict(endpoints_item_data)

            endpoints.append(endpoints_item)

        software_catalogs = []
        _software_catalogs = d.pop("software_catalogs", UNSET)
        for software_catalogs_item_data in _software_catalogs or []:
            software_catalogs_item = NestedSoftwareCatalog.from_dict(software_catalogs_item_data)

            software_catalogs.append(software_catalogs_item)

        partitions = []
        _partitions = d.pop("partitions", UNSET)
        for partitions_item_data in _partitions or []:
            partitions_item = NestedPartition.from_dict(partitions_item_data)

            partitions.append(partitions_item)

        roles = []
        _roles = d.pop("roles", UNSET)
        for roles_item_data in _roles or []:
            roles_item = NestedRole.from_dict(roles_item_data)

            roles.append(roles_item)

        def _parse_customer(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        customer = _parse_customer(d.pop("customer", UNSET))

        def _parse_customer_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                customer_uuid_type_0 = UUID(data)

                return customer_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        customer_uuid = _parse_customer_uuid(d.pop("customer_uuid", UNSET))

        def _parse_customer_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        customer_name = _parse_customer_name(d.pop("customer_name", UNSET))

        def _parse_project(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project = _parse_project(d.pop("project", UNSET))

        def _parse_project_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_uuid_type_0 = UUID(data)

                return project_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        project_uuid = _parse_project_uuid(d.pop("project_uuid", UNSET))

        def _parse_project_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_name = _parse_project_name(d.pop("project_name", UNSET))

        category = d.pop("category", UNSET)

        _category_uuid = d.pop("category_uuid", UNSET)
        category_uuid: Union[Unset, UUID]
        if isinstance(_category_uuid, Unset):
            category_uuid = UNSET
        else:
            category_uuid = UUID(_category_uuid)

        category_title = d.pop("category_title", UNSET)

        _attributes = d.pop("attributes", UNSET)
        attributes: Union[Unset, ProviderOfferingDetailsAttributes]
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = ProviderOfferingDetailsAttributes.from_dict(_attributes)

        _options = d.pop("options", UNSET)
        options: Union[Unset, OfferingOptions]
        if isinstance(_options, Unset):
            options = UNSET
        else:
            options = OfferingOptions.from_dict(_options)

        _resource_options = d.pop("resource_options", UNSET)
        resource_options: Union[Unset, OfferingOptions]
        if isinstance(_resource_options, Unset):
            resource_options = UNSET
        else:
            resource_options = OfferingOptions.from_dict(_resource_options)

        components = []
        _components = d.pop("components", UNSET)
        for components_item_data in _components or []:
            components_item = OfferingComponent.from_dict(components_item_data)

            components.append(components_item)

        _plugin_options = d.pop("plugin_options", UNSET)
        plugin_options: Union[Unset, MergedPluginOptions]
        if isinstance(_plugin_options, Unset):
            plugin_options = UNSET
        else:
            plugin_options = MergedPluginOptions.from_dict(_plugin_options)

        _secret_options = d.pop("secret_options", UNSET)
        secret_options: Union[Unset, MergedSecretOptions]
        if isinstance(_secret_options, Unset):
            secret_options = UNSET
        else:
            secret_options = MergedSecretOptions.from_dict(_secret_options)

        _service_attributes = d.pop("service_attributes", UNSET)
        service_attributes: Union[Unset, ProviderOfferingDetailsServiceAttributes]
        if isinstance(_service_attributes, Unset):
            service_attributes = UNSET
        else:
            service_attributes = ProviderOfferingDetailsServiceAttributes.from_dict(_service_attributes)

        _state = d.pop("state", UNSET)
        state: Union[Unset, OfferingState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = OfferingState(_state)

        vendor_details = d.pop("vendor_details", UNSET)

        getting_started = d.pop("getting_started", UNSET)

        integration_guide = d.pop("integration_guide", UNSET)

        def _parse_thumbnail(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        thumbnail = _parse_thumbnail(d.pop("thumbnail", UNSET))

        order_count = d.pop("order_count", UNSET)

        plans = []
        _plans = d.pop("plans", UNSET)
        for plans_item_data in _plans or []:
            plans_item = BaseProviderPlan.from_dict(plans_item_data)

            plans.append(plans_item)

        screenshots = []
        _screenshots = d.pop("screenshots", UNSET)
        for screenshots_item_data in _screenshots or []:
            screenshots_item = NestedScreenshot.from_dict(screenshots_item_data)

            screenshots.append(screenshots_item)

        type_ = d.pop("type", UNSET)

        shared = d.pop("shared", UNSET)

        billable = d.pop("billable", UNSET)

        scope = d.pop("scope", UNSET)

        def _parse_scope_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scope_uuid_type_0 = UUID(data)

                return scope_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        scope_uuid = _parse_scope_uuid(d.pop("scope_uuid", UNSET))

        def _parse_scope_name(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scope_name_type_0 = UUID(data)

                return scope_name_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        scope_name = _parse_scope_name(d.pop("scope_name", UNSET))

        def _parse_scope_state(data: object) -> Union[CoreStates, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scope_state_type_0 = CoreStates(data)

                return scope_state_type_0
            except:  # noqa: E722
                pass
            return cast(Union[CoreStates, None, Unset], data)

        scope_state = _parse_scope_state(d.pop("scope_state", UNSET))

        def _parse_scope_error_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        scope_error_message = _parse_scope_error_message(d.pop("scope_error_message", UNSET))

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = NestedOfferingFile.from_dict(files_item_data)

            files.append(files_item)

        quotas = []
        _quotas = d.pop("quotas", UNSET)
        for quotas_item_data in _quotas or []:
            quotas_item = Quota.from_dict(quotas_item_data)

            quotas.append(quotas_item)

        paused_reason = d.pop("paused_reason", UNSET)

        datacite_doi = d.pop("datacite_doi", UNSET)

        citation_count = d.pop("citation_count", UNSET)

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

        organization_groups = []
        _organization_groups = d.pop("organization_groups", UNSET)
        for organization_groups_item_data in _organization_groups or []:
            organization_groups_item = OrganizationGroup.from_dict(organization_groups_item_data)

            organization_groups.append(organization_groups_item)

        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in _tags or []:
            tags_item = NestedTag.from_dict(tags_item_data)

            tags.append(tags_item)

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        def _parse_total_customers(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        total_customers = _parse_total_customers(d.pop("total_customers", UNSET))

        def _parse_total_cost(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        total_cost = _parse_total_cost(d.pop("total_cost", UNSET))

        def _parse_total_cost_estimated(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        total_cost_estimated = _parse_total_cost_estimated(d.pop("total_cost_estimated", UNSET))

        def _parse_parent_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parent_description = _parse_parent_description(d.pop("parent_description", UNSET))

        def _parse_parent_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                parent_uuid_type_0 = UUID(data)

                return parent_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        parent_uuid = _parse_parent_uuid(d.pop("parent_uuid", UNSET))

        def _parse_parent_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parent_name = _parse_parent_name(d.pop("parent_name", UNSET))

        backend_metadata = d.pop("backend_metadata", UNSET)

        has_compliance_requirements = d.pop("has_compliance_requirements", UNSET)

        billing_type_classification = d.pop("billing_type_classification", UNSET)

        def _parse_compliance_checklist(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        compliance_checklist = _parse_compliance_checklist(d.pop("compliance_checklist", UNSET))

        def _parse_integration_status(data: object) -> Union[None, Unset, list["IntegrationStatus"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                integration_status_type_0 = []
                _integration_status_type_0 = data
                for integration_status_type_0_item_data in _integration_status_type_0:
                    integration_status_type_0_item = IntegrationStatus.from_dict(integration_status_type_0_item_data)

                    integration_status_type_0.append(integration_status_type_0_item)

                return integration_status_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["IntegrationStatus"]], data)

        integration_status = _parse_integration_status(d.pop("integration_status", UNSET))

        def _parse_google_calendar_is_public(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        google_calendar_is_public = _parse_google_calendar_is_public(d.pop("google_calendar_is_public", UNSET))

        def _parse_google_calendar_link(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        google_calendar_link = _parse_google_calendar_link(d.pop("google_calendar_link", UNSET))

        provider_offering_details = cls(
            url=url,
            uuid=uuid,
            created=created,
            name=name,
            slug=slug,
            description=description,
            full_description=full_description,
            privacy_policy_link=privacy_policy_link,
            access_url=access_url,
            endpoints=endpoints,
            software_catalogs=software_catalogs,
            partitions=partitions,
            roles=roles,
            customer=customer,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            project=project,
            project_uuid=project_uuid,
            project_name=project_name,
            category=category,
            category_uuid=category_uuid,
            category_title=category_title,
            attributes=attributes,
            options=options,
            resource_options=resource_options,
            components=components,
            plugin_options=plugin_options,
            secret_options=secret_options,
            service_attributes=service_attributes,
            state=state,
            vendor_details=vendor_details,
            getting_started=getting_started,
            integration_guide=integration_guide,
            thumbnail=thumbnail,
            order_count=order_count,
            plans=plans,
            screenshots=screenshots,
            type_=type_,
            shared=shared,
            billable=billable,
            scope=scope,
            scope_uuid=scope_uuid,
            scope_name=scope_name,
            scope_state=scope_state,
            scope_error_message=scope_error_message,
            files=files,
            quotas=quotas,
            paused_reason=paused_reason,
            datacite_doi=datacite_doi,
            citation_count=citation_count,
            latitude=latitude,
            longitude=longitude,
            country=country,
            backend_id=backend_id,
            backend_id_rules=backend_id_rules,
            organization_groups=organization_groups,
            tags=tags,
            image=image,
            total_customers=total_customers,
            total_cost=total_cost,
            total_cost_estimated=total_cost_estimated,
            parent_description=parent_description,
            parent_uuid=parent_uuid,
            parent_name=parent_name,
            backend_metadata=backend_metadata,
            has_compliance_requirements=has_compliance_requirements,
            billing_type_classification=billing_type_classification,
            compliance_checklist=compliance_checklist,
            integration_status=integration_status,
            google_calendar_is_public=google_calendar_is_public,
            google_calendar_link=google_calendar_link,
        )

        provider_offering_details.additional_properties = d
        return provider_offering_details

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
