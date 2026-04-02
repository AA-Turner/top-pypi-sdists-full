import datetime
from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from .. import types
from ..models.blank_enum import BlankEnum
from ..models.kind_enum import KindEnum
from ..models.oecd_fos_2007_code_enum import OecdFos2007CodeEnum
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="PatchedProjectRequestMultipart")


@_attrs_define
class PatchedProjectRequestMultipart:
    """
    Attributes:
        name (Union[Unset, str]):
        slug (Union[Unset, str]): URL-friendly identifier. Only editable by staff users.
        customer (Union[Unset, str]):
        description (Union[Unset, str]): Project description (HTML content will be sanitized)
        type_ (Union[None, Unset, str]):
        backend_id (Union[Unset, str]):
        start_date (Union[None, Unset, datetime.date]): Project start date. Cannot be edited after the start date has
            arrived.
        end_date (Union[None, Unset, datetime.date]): Project end date. Setting this field requires DELETE_PROJECT
            permission.
        oecd_fos_2007_code (Union[BlankEnum, None, OecdFos2007CodeEnum, Unset]):
        is_industry (Union[Unset, bool]):
        image (Union[File, None, Unset]):
        kind (Union[Unset, KindEnum]):
        staff_notes (Union[Unset, str]): Internal notes visible only to staff and support users (HTML content will be
            sanitized)
        grace_period_days (Union[None, Unset, int]): Number of extra days after project end date before resources are
            terminated. Overrides customer-level setting.
        user_email_patterns (Union[Unset, Any]):
        user_affiliations (Union[Unset, Any]):
        user_identity_sources (Union[Unset, Any]): List of allowed identity sources (identity providers).
    """

    name: Union[Unset, str] = UNSET
    slug: Union[Unset, str] = UNSET
    customer: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    type_: Union[None, Unset, str] = UNSET
    backend_id: Union[Unset, str] = UNSET
    start_date: Union[None, Unset, datetime.date] = UNSET
    end_date: Union[None, Unset, datetime.date] = UNSET
    oecd_fos_2007_code: Union[BlankEnum, None, OecdFos2007CodeEnum, Unset] = UNSET
    is_industry: Union[Unset, bool] = UNSET
    image: Union[File, None, Unset] = UNSET
    kind: Union[Unset, KindEnum] = UNSET
    staff_notes: Union[Unset, str] = UNSET
    grace_period_days: Union[None, Unset, int] = UNSET
    user_email_patterns: Union[Unset, Any] = UNSET
    user_affiliations: Union[Unset, Any] = UNSET
    user_identity_sources: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        slug = self.slug

        customer = self.customer

        description = self.description

        type_: Union[None, Unset, str]
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

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

        oecd_fos_2007_code: Union[None, Unset, str]
        if isinstance(self.oecd_fos_2007_code, Unset):
            oecd_fos_2007_code = UNSET
        elif isinstance(self.oecd_fos_2007_code, OecdFos2007CodeEnum):
            oecd_fos_2007_code = self.oecd_fos_2007_code.value
        elif isinstance(self.oecd_fos_2007_code, BlankEnum):
            oecd_fos_2007_code = self.oecd_fos_2007_code.value
        else:
            oecd_fos_2007_code = self.oecd_fos_2007_code

        is_industry = self.is_industry

        image: Union[None, Unset, types.FileTypes]
        if isinstance(self.image, Unset):
            image = UNSET
        elif isinstance(self.image, File):
            image = self.image.to_tuple()

        else:
            image = self.image

        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        staff_notes = self.staff_notes

        grace_period_days: Union[None, Unset, int]
        if isinstance(self.grace_period_days, Unset):
            grace_period_days = UNSET
        else:
            grace_period_days = self.grace_period_days

        user_email_patterns = self.user_email_patterns

        user_affiliations = self.user_affiliations

        user_identity_sources = self.user_identity_sources

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if slug is not UNSET:
            field_dict["slug"] = slug
        if customer is not UNSET:
            field_dict["customer"] = customer
        if description is not UNSET:
            field_dict["description"] = description
        if type_ is not UNSET:
            field_dict["type"] = type_
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if oecd_fos_2007_code is not UNSET:
            field_dict["oecd_fos_2007_code"] = oecd_fos_2007_code
        if is_industry is not UNSET:
            field_dict["is_industry"] = is_industry
        if image is not UNSET:
            field_dict["image"] = image
        if kind is not UNSET:
            field_dict["kind"] = kind
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

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if not isinstance(self.name, Unset):
            files.append(("name", (None, str(self.name).encode(), "text/plain")))

        if not isinstance(self.slug, Unset):
            files.append(("slug", (None, str(self.slug).encode(), "text/plain")))

        if not isinstance(self.customer, Unset):
            files.append(("customer", (None, str(self.customer).encode(), "text/plain")))

        if not isinstance(self.description, Unset):
            files.append(("description", (None, str(self.description).encode(), "text/plain")))

        if not isinstance(self.type_, Unset):
            if isinstance(self.type_, str):
                files.append(("type", (None, str(self.type_).encode(), "text/plain")))
            else:
                files.append(("type", (None, str(self.type_).encode(), "text/plain")))

        if not isinstance(self.backend_id, Unset):
            files.append(("backend_id", (None, str(self.backend_id).encode(), "text/plain")))

        if not isinstance(self.start_date, Unset):
            if isinstance(self.start_date, datetime.date):
                files.append(("start_date", (None, self.start_date.isoformat().encode(), "text/plain")))
            else:
                files.append(("start_date", (None, str(self.start_date).encode(), "text/plain")))

        if not isinstance(self.end_date, Unset):
            if isinstance(self.end_date, datetime.date):
                files.append(("end_date", (None, self.end_date.isoformat().encode(), "text/plain")))
            else:
                files.append(("end_date", (None, str(self.end_date).encode(), "text/plain")))

        if not isinstance(self.oecd_fos_2007_code, Unset):
            if isinstance(self.oecd_fos_2007_code, OecdFos2007CodeEnum):
                files.append(("oecd_fos_2007_code", (None, str(self.oecd_fos_2007_code.value).encode(), "text/plain")))
            elif isinstance(self.oecd_fos_2007_code, BlankEnum):
                files.append(("oecd_fos_2007_code", (None, str(self.oecd_fos_2007_code.value).encode(), "text/plain")))
            elif self.oecd_fos_2007_code is None:
                files.append(("oecd_fos_2007_code", (None, str(self.oecd_fos_2007_code).encode(), "text/plain")))
            else:
                files.append(("oecd_fos_2007_code", (None, str(self.oecd_fos_2007_code).encode(), "text/plain")))

        if not isinstance(self.is_industry, Unset):
            files.append(("is_industry", (None, str(self.is_industry).encode(), "text/plain")))

        if not isinstance(self.image, Unset):
            if isinstance(self.image, File):
                files.append(("image", self.image.to_tuple()))
            else:
                files.append(("image", (None, str(self.image).encode(), "text/plain")))

        if not isinstance(self.kind, Unset):
            files.append(("kind", (None, str(self.kind.value).encode(), "text/plain")))

        if not isinstance(self.staff_notes, Unset):
            files.append(("staff_notes", (None, str(self.staff_notes).encode(), "text/plain")))

        if not isinstance(self.grace_period_days, Unset):
            if isinstance(self.grace_period_days, int):
                files.append(("grace_period_days", (None, str(self.grace_period_days).encode(), "text/plain")))
            else:
                files.append(("grace_period_days", (None, str(self.grace_period_days).encode(), "text/plain")))

        if not isinstance(self.user_email_patterns, Unset):
            files.append(("user_email_patterns", (None, str(self.user_email_patterns).encode(), "text/plain")))

        if not isinstance(self.user_affiliations, Unset):
            files.append(("user_affiliations", (None, str(self.user_affiliations).encode(), "text/plain")))

        if not isinstance(self.user_identity_sources, Unset):
            files.append(("user_identity_sources", (None, str(self.user_identity_sources).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        slug = d.pop("slug", UNSET)

        customer = d.pop("customer", UNSET)

        description = d.pop("description", UNSET)

        def _parse_type_(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        type_ = _parse_type_(d.pop("type", UNSET))

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

        is_industry = d.pop("is_industry", UNSET)

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

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, KindEnum]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = KindEnum(_kind)

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

        patched_project_request_multipart = cls(
            name=name,
            slug=slug,
            customer=customer,
            description=description,
            type_=type_,
            backend_id=backend_id,
            start_date=start_date,
            end_date=end_date,
            oecd_fos_2007_code=oecd_fos_2007_code,
            is_industry=is_industry,
            image=image,
            kind=kind,
            staff_notes=staff_notes,
            grace_period_days=grace_period_days,
            user_email_patterns=user_email_patterns,
            user_affiliations=user_affiliations,
            user_identity_sources=user_identity_sources,
        )

        patched_project_request_multipart.additional_properties = d
        return patched_project_request_multipart

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
