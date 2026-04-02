import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.affiliation_type_enum import AffiliationTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewerAffiliationRequest")


@_attrs_define
class ReviewerAffiliationRequest:
    """
    Attributes:
        organization_name (str): Organization name (used when not linked to Waldur org)
        organization (Union[None, UUID, Unset]):
        organization_identifier (Union[Unset, str]): ROR, GRID, or other external identifier
        department (Union[Unset, str]):
        position_title (Union[Unset, str]):
        start_date (Union[None, Unset, datetime.date]):
        end_date (Union[None, Unset, datetime.date]): Leave empty for current affiliation
        is_primary (Union[Unset, bool]):
        affiliation_type (Union[Unset, AffiliationTypeEnum]):
    """

    organization_name: str
    organization: Union[None, UUID, Unset] = UNSET
    organization_identifier: Union[Unset, str] = UNSET
    department: Union[Unset, str] = UNSET
    position_title: Union[Unset, str] = UNSET
    start_date: Union[None, Unset, datetime.date] = UNSET
    end_date: Union[None, Unset, datetime.date] = UNSET
    is_primary: Union[Unset, bool] = UNSET
    affiliation_type: Union[Unset, AffiliationTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        organization_name = self.organization_name

        organization: Union[None, Unset, str]
        if isinstance(self.organization, Unset):
            organization = UNSET
        elif isinstance(self.organization, UUID):
            organization = str(self.organization)
        else:
            organization = self.organization

        organization_identifier = self.organization_identifier

        department = self.department

        position_title = self.position_title

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

        is_primary = self.is_primary

        affiliation_type: Union[Unset, str] = UNSET
        if not isinstance(self.affiliation_type, Unset):
            affiliation_type = self.affiliation_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "organization_name": organization_name,
            }
        )
        if organization is not UNSET:
            field_dict["organization"] = organization
        if organization_identifier is not UNSET:
            field_dict["organization_identifier"] = organization_identifier
        if department is not UNSET:
            field_dict["department"] = department
        if position_title is not UNSET:
            field_dict["position_title"] = position_title
        if start_date is not UNSET:
            field_dict["start_date"] = start_date
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if is_primary is not UNSET:
            field_dict["is_primary"] = is_primary
        if affiliation_type is not UNSET:
            field_dict["affiliation_type"] = affiliation_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        organization_name = d.pop("organization_name")

        def _parse_organization(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                organization_type_0 = UUID(data)

                return organization_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        organization = _parse_organization(d.pop("organization", UNSET))

        organization_identifier = d.pop("organization_identifier", UNSET)

        department = d.pop("department", UNSET)

        position_title = d.pop("position_title", UNSET)

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

        is_primary = d.pop("is_primary", UNSET)

        _affiliation_type = d.pop("affiliation_type", UNSET)
        affiliation_type: Union[Unset, AffiliationTypeEnum]
        if isinstance(_affiliation_type, Unset):
            affiliation_type = UNSET
        else:
            affiliation_type = AffiliationTypeEnum(_affiliation_type)

        reviewer_affiliation_request = cls(
            organization_name=organization_name,
            organization=organization,
            organization_identifier=organization_identifier,
            department=department,
            position_title=position_title,
            start_date=start_date,
            end_date=end_date,
            is_primary=is_primary,
            affiliation_type=affiliation_type,
        )

        reviewer_affiliation_request.additional_properties = d
        return reviewer_affiliation_request

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
