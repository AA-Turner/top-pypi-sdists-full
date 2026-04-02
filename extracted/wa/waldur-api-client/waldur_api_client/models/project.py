import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.blank_enum import BlankEnum
from ..models.kind_enum import KindEnum
from ..models.oecd_fos_2007_code_enum import OecdFos2007CodeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_price_estimate import NestedPriceEstimate
    from ..models.project_marketplace_resource_count import ProjectMarketplaceResourceCount


T = TypeVar("T", bound="Project")


@_attrs_define
class Project:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        slug (Union[Unset, str]): URL-friendly identifier. Only editable by staff users.
        customer (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        customer_name (Union[Unset, str]):
        customer_slug (Union[Unset, str]):
        customer_native_name (Union[Unset, str]):
        customer_abbreviation (Union[Unset, str]):
        description (Union[Unset, str]): Project description (HTML content will be sanitized)
        customer_display_billing_info_in_projects (Union[Unset, bool]):
        created (Union[Unset, datetime.datetime]):
        type_ (Union[None, Unset, str]):
        type_name (Union[None, Unset, str]):
        type_uuid (Union[None, UUID, Unset]):
        backend_id (Union[Unset, str]):
        start_date (Union[None, Unset, datetime.date]): Project start date. Cannot be edited after the start date has
            arrived.
        end_date (Union[None, Unset, datetime.date]): Project end date. Setting this field requires DELETE_PROJECT
            permission.
        end_date_requested_by (Union[None, Unset, str]):
        oecd_fos_2007_code (Union[BlankEnum, None, OecdFos2007CodeEnum, Unset]):
        oecd_fos_2007_label (Union[Unset, str]): Human-readable label for the OECD FOS 2007 classification code
        is_industry (Union[Unset, bool]):
        image (Union[None, Unset, str]):
        resources_count (Union[Unset, int]): Number of active resources in this project
        max_service_accounts (Union[None, Unset, int]): Maximum number of service accounts allowed
        kind (Union[Unset, KindEnum]):
        is_removed (Union[Unset, bool]):
        termination_metadata (Union[Unset, Any]): Metadata about project termination (read-only)
        staff_notes (Union[Unset, str]): Internal notes visible only to staff and support users (HTML content will be
            sanitized)
        grace_period_days (Union[None, Unset, int]): Number of extra days after project end date before resources are
            terminated. Overrides customer-level setting.
        user_email_patterns (Union[Unset, Any]):
        user_affiliations (Union[Unset, Any]):
        user_identity_sources (Union[Unset, Any]): List of allowed identity sources (identity providers).
        project_credit (Union[None, Unset, float]):
        marketplace_resource_count (Union[Unset, ProjectMarketplaceResourceCount]):
        billing_price_estimate (Union[Unset, NestedPriceEstimate]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    slug: Union[Unset, str] = UNSET
    customer: Union[Unset, str] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    customer_name: Union[Unset, str] = UNSET
    customer_slug: Union[Unset, str] = UNSET
    customer_native_name: Union[Unset, str] = UNSET
    customer_abbreviation: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    customer_display_billing_info_in_projects: Union[Unset, bool] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    type_: Union[None, Unset, str] = UNSET
    type_name: Union[None, Unset, str] = UNSET
    type_uuid: Union[None, UUID, Unset] = UNSET
    backend_id: Union[Unset, str] = UNSET
    start_date: Union[None, Unset, datetime.date] = UNSET
    end_date: Union[None, Unset, datetime.date] = UNSET
    end_date_requested_by: Union[None, Unset, str] = UNSET
    oecd_fos_2007_code: Union[BlankEnum, None, OecdFos2007CodeEnum, Unset] = UNSET
    oecd_fos_2007_label: Union[Unset, str] = UNSET
    is_industry: Union[Unset, bool] = UNSET
    image: Union[None, Unset, str] = UNSET
    resources_count: Union[Unset, int] = UNSET
    max_service_accounts: Union[None, Unset, int] = UNSET
    kind: Union[Unset, KindEnum] = UNSET
    is_removed: Union[Unset, bool] = UNSET
    termination_metadata: Union[Unset, Any] = UNSET
    staff_notes: Union[Unset, str] = UNSET
    grace_period_days: Union[None, Unset, int] = UNSET
    user_email_patterns: Union[Unset, Any] = UNSET
    user_affiliations: Union[Unset, Any] = UNSET
    user_identity_sources: Union[Unset, Any] = UNSET
    project_credit: Union[None, Unset, float] = UNSET
    marketplace_resource_count: Union[Unset, "ProjectMarketplaceResourceCount"] = UNSET
    billing_price_estimate: Union[Unset, "NestedPriceEstimate"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        slug = self.slug

        customer = self.customer

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        customer_slug = self.customer_slug

        customer_native_name = self.customer_native_name

        customer_abbreviation = self.customer_abbreviation

        description = self.description

        customer_display_billing_info_in_projects = self.customer_display_billing_info_in_projects

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        type_: Union[None, Unset, str]
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

        type_name: Union[None, Unset, str]
        if isinstance(self.type_name, Unset):
            type_name = UNSET
        else:
            type_name = self.type_name

        type_uuid: Union[None, Unset, str]
        if isinstance(self.type_uuid, Unset):
            type_uuid = UNSET
        elif isinstance(self.type_uuid, UUID):
            type_uuid = str(self.type_uuid)
        else:
            type_uuid = self.type_uuid

        backend_id = self.backend_id

        start_date: Union[None, Unset, str]
        if isinstance(self.start_date, Unset):
            start_date = UNSET
        elif isinstance(self.start_date, datetime.date):
            start_date = self.start_date.isoformat()
        else:
            start_date = self.start_date

        end_date: Union[None, Unset, str]
        if isinstance(self.end_date, Unset):
            end_date = UNSET
        elif isinstance(self.end_date, datetime.date):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        end_date_requested_by: Union[None, Unset, str]
        if isinstance(self.end_date_requested_by, Unset):
            end_date_requested_by = UNSET
        else:
            end_date_requested_by = self.end_date_requested_by

        oecd_fos_2007_code: Union[None, Unset, str]
        if isinstance(self.oecd_fos_2007_code, Unset):
            oecd_fos_2007_code = UNSET
        elif isinstance(self.oecd_fos_2007_code, OecdFos2007CodeEnum):
            oecd_fos_2007_code = self.oecd_fos_2007_code.value
        elif isinstance(self.oecd_fos_2007_code, BlankEnum):
            oecd_fos_2007_code = self.oecd_fos_2007_code.value
        else:
            oecd_fos_2007_code = self.oecd_fos_2007_code

        oecd_fos_2007_label = self.oecd_fos_2007_label

        is_industry = self.is_industry

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        resources_count = self.resources_count

        max_service_accounts: Union[None, Unset, int]
        if isinstance(self.max_service_accounts, Unset):
            max_service_accounts = UNSET
        else:
            max_service_accounts = self.max_service_accounts

        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        is_removed = self.is_removed

        termination_metadata = self.termination_metadata

        staff_notes = self.staff_notes

        grace_period_days: Union[None, Unset, int]
        if isinstance(self.grace_period_days, Unset):
            grace_period_days = UNSET
        else:
            grace_period_days = self.grace_period_days

        user_email_patterns = self.user_email_patterns

        user_affiliations = self.user_affiliations

        user_identity_sources = self.user_identity_sources

        project_credit: Union[None, Unset, float]
        if isinstance(self.project_credit, Unset):
            project_credit = UNSET
        else:
            project_credit = self.project_credit

        marketplace_resource_count: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.marketplace_resource_count, Unset):
            marketplace_resource_count = self.marketplace_resource_count.to_dict()

        billing_price_estimate: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.billing_price_estimate, Unset):
            billing_price_estimate = self.billing_price_estimate.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if slug is not UNSET:
            field_dict["slug"] = slug
        if customer is not UNSET:
            field_dict["customer"] = customer
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if customer_slug is not UNSET:
            field_dict["customer_slug"] = customer_slug
        if customer_native_name is not UNSET:
            field_dict["customer_native_name"] = customer_native_name
        if customer_abbreviation is not UNSET:
            field_dict["customer_abbreviation"] = customer_abbreviation
        if description is not UNSET:
            field_dict["description"] = description
        if customer_display_billing_info_in_projects is not UNSET:
            field_dict["customer_display_billing_info_in_projects"] = customer_display_billing_info_in_projects
        if created is not UNSET:
            field_dict["created"] = created
        if type_ is not UNSET:
            field_dict["type"] = type_
        if type_name is not UNSET:
            field_dict["type_name"] = type_name
        if type_uuid is not UNSET:
            field_dict["type_uuid"] = type_uuid
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if end_date_requested_by is not UNSET:
            field_dict["end_date_requested_by"] = end_date_requested_by
        if oecd_fos_2007_code is not UNSET:
            field_dict["oecd_fos_2007_code"] = oecd_fos_2007_code
        if oecd_fos_2007_label is not UNSET:
            field_dict["oecd_fos_2007_label"] = oecd_fos_2007_label
        if is_industry is not UNSET:
            field_dict["is_industry"] = is_industry
        if image is not UNSET:
            field_dict["image"] = image
        if resources_count is not UNSET:
            field_dict["resources_count"] = resources_count
        if max_service_accounts is not UNSET:
            field_dict["max_service_accounts"] = max_service_accounts
        if kind is not UNSET:
            field_dict["kind"] = kind
        if is_removed is not UNSET:
            field_dict["is_removed"] = is_removed
        if termination_metadata is not UNSET:
            field_dict["termination_metadata"] = termination_metadata
        if staff_notes is not UNSET:
            field_dict["staff_notes"] = staff_notes
        if grace_period_days is not UNSET:
            field_dict["grace_period_days"] = grace_period_days
        if user_email_patterns is not UNSET:
            field_dict["user_email_patterns"] = user_email_patterns
        if user_affiliations is not UNSET:
            field_dict["user_affiliations"] = user_affiliations
        if user_identity_sources is not UNSET:
            field_dict["user_identity_sources"] = user_identity_sources
        if project_credit is not UNSET:
            field_dict["project_credit"] = project_credit
        if marketplace_resource_count is not UNSET:
            field_dict["marketplace_resource_count"] = marketplace_resource_count
        if billing_price_estimate is not UNSET:
            field_dict["billing_price_estimate"] = billing_price_estimate

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_price_estimate import NestedPriceEstimate
        from ..models.project_marketplace_resource_count import ProjectMarketplaceResourceCount

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        name = d.pop("name", UNSET)

        slug = d.pop("slug", UNSET)

        customer = d.pop("customer", UNSET)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        customer_name = d.pop("customer_name", UNSET)

        customer_slug = d.pop("customer_slug", UNSET)

        customer_native_name = d.pop("customer_native_name", UNSET)

        customer_abbreviation = d.pop("customer_abbreviation", UNSET)

        description = d.pop("description", UNSET)

        customer_display_billing_info_in_projects = d.pop("customer_display_billing_info_in_projects", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        def _parse_type_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        type_ = _parse_type_(d.pop("type", UNSET))

        def _parse_type_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        type_name = _parse_type_name(d.pop("type_name", UNSET))

        def _parse_type_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                type_uuid_type_0 = UUID(data)

                return type_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        type_uuid = _parse_type_uuid(d.pop("type_uuid", UNSET))

        backend_id = d.pop("backend_id", UNSET)

        def _parse_start_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_date_type_0 = isoparse(data).date()

                return start_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        start_date = _parse_start_date(d.pop("start_date", UNSET))

        def _parse_end_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = isoparse(data).date()

                return end_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        end_date = _parse_end_date(d.pop("end_date", UNSET))

        def _parse_end_date_requested_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        end_date_requested_by = _parse_end_date_requested_by(d.pop("end_date_requested_by", UNSET))

        def _parse_oecd_fos_2007_code(data: object) -> Union[BlankEnum, None, OecdFos2007CodeEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                oecd_fos_2007_code_type_0 = OecdFos2007CodeEnum(data)

                return oecd_fos_2007_code_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                oecd_fos_2007_code_type_1 = BlankEnum(data)

                return oecd_fos_2007_code_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BlankEnum, None, OecdFos2007CodeEnum, Unset], data)

        oecd_fos_2007_code = _parse_oecd_fos_2007_code(d.pop("oecd_fos_2007_code", UNSET))

        oecd_fos_2007_label = d.pop("oecd_fos_2007_label", UNSET)

        is_industry = d.pop("is_industry", UNSET)

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        resources_count = d.pop("resources_count", UNSET)

        def _parse_max_service_accounts(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_service_accounts = _parse_max_service_accounts(d.pop("max_service_accounts", UNSET))

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, KindEnum]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = KindEnum(_kind)

        is_removed = d.pop("is_removed", UNSET)

        termination_metadata = d.pop("termination_metadata", UNSET)

        staff_notes = d.pop("staff_notes", UNSET)

        def _parse_grace_period_days(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        grace_period_days = _parse_grace_period_days(d.pop("grace_period_days", UNSET))

        user_email_patterns = d.pop("user_email_patterns", UNSET)

        user_affiliations = d.pop("user_affiliations", UNSET)

        user_identity_sources = d.pop("user_identity_sources", UNSET)

        def _parse_project_credit(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        project_credit = _parse_project_credit(d.pop("project_credit", UNSET))

        _marketplace_resource_count = d.pop("marketplace_resource_count", UNSET)
        marketplace_resource_count: Union[Unset, ProjectMarketplaceResourceCount]
        if isinstance(_marketplace_resource_count, Unset):
            marketplace_resource_count = UNSET
        else:
            marketplace_resource_count = ProjectMarketplaceResourceCount.from_dict(_marketplace_resource_count)

        _billing_price_estimate = d.pop("billing_price_estimate", UNSET)
        billing_price_estimate: Union[Unset, NestedPriceEstimate]
        if isinstance(_billing_price_estimate, Unset):
            billing_price_estimate = UNSET
        else:
            billing_price_estimate = NestedPriceEstimate.from_dict(_billing_price_estimate)

        project = cls(
            url=url,
            uuid=uuid,
            name=name,
            slug=slug,
            customer=customer,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            customer_slug=customer_slug,
            customer_native_name=customer_native_name,
            customer_abbreviation=customer_abbreviation,
            description=description,
            customer_display_billing_info_in_projects=customer_display_billing_info_in_projects,
            created=created,
            type_=type_,
            type_name=type_name,
            type_uuid=type_uuid,
            backend_id=backend_id,
            start_date=start_date,
            end_date=end_date,
            end_date_requested_by=end_date_requested_by,
            oecd_fos_2007_code=oecd_fos_2007_code,
            oecd_fos_2007_label=oecd_fos_2007_label,
            is_industry=is_industry,
            image=image,
            resources_count=resources_count,
            max_service_accounts=max_service_accounts,
            kind=kind,
            is_removed=is_removed,
            termination_metadata=termination_metadata,
            staff_notes=staff_notes,
            grace_period_days=grace_period_days,
            user_email_patterns=user_email_patterns,
            user_affiliations=user_affiliations,
            user_identity_sources=user_identity_sources,
            project_credit=project_credit,
            marketplace_resource_count=marketplace_resource_count,
            billing_price_estimate=billing_price_estimate,
        )

        project.additional_properties = d
        return project

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
