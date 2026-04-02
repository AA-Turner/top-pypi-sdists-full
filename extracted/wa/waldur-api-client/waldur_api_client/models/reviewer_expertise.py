import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.proficiency_level_enum import ProficiencyLevelEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ReviewerExpertise")


@_attrs_define
class ReviewerExpertise:
    """
    Attributes:
        uuid (UUID):
        expertise_keyword (str): Free-text keyword
        expertise_category_name (str):
        created (datetime.datetime):
        expertise_category (Union[None, UUID, Unset]):
        proficiency_level (Union[Unset, ProficiencyLevelEnum]):
        years_experience (Union[None, Unset, int]):
        last_active_date (Union[None, Unset, datetime.date]): When last worked in this area
    """

    uuid: UUID
    expertise_keyword: str
    expertise_category_name: str
    created: datetime.datetime
    expertise_category: Union[None, UUID, Unset] = UNSET
    proficiency_level: Union[Unset, ProficiencyLevelEnum] = UNSET
    years_experience: Union[None, Unset, int] = UNSET
    last_active_date: Union[None, Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        expertise_keyword = self.expertise_keyword

        expertise_category_name = self.expertise_category_name

        created = self.created.isoformat()

        expertise_category: Union[None, Unset, str]
        if isinstance(self.expertise_category, Unset):
            expertise_category = UNSET
        elif isinstance(self.expertise_category, UUID):
            expertise_category = str(self.expertise_category)
        else:
            expertise_category = self.expertise_category

        proficiency_level: Union[Unset, str] = UNSET
        if not isinstance(self.proficiency_level, Unset):
            proficiency_level = self.proficiency_level.value

        years_experience: Union[None, Unset, int]
        if isinstance(self.years_experience, Unset):
            years_experience = UNSET
        else:
            years_experience = self.years_experience

        last_active_date: Union[None, Unset, str]
        if isinstance(self.last_active_date, Unset):
            last_active_date = UNSET
        elif isinstance(self.last_active_date, datetime.date):
            last_active_date = self.last_active_date.isoformat()
        else:
            last_active_date = self.last_active_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "expertise_keyword": expertise_keyword,
                "expertise_category_name": expertise_category_name,
                "created": created,
            }
        )
        if expertise_category is not UNSET:
            field_dict["expertise_category"] = expertise_category
        if proficiency_level is not UNSET:
            field_dict["proficiency_level"] = proficiency_level
        if years_experience is not UNSET:
            field_dict["years_experience"] = years_experience
        if last_active_date is not UNSET:
            field_dict["last_active_date"] = last_active_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        expertise_keyword = d.pop("expertise_keyword")

        expertise_category_name = d.pop("expertise_category_name")

        created = isoparse(d.pop("created"))

        def _parse_expertise_category(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expertise_category_type_0 = UUID(data)

                return expertise_category_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        expertise_category = _parse_expertise_category(d.pop("expertise_category", UNSET))

        _proficiency_level = d.pop("proficiency_level", UNSET)
        proficiency_level: Union[Unset, ProficiencyLevelEnum]
        if isinstance(_proficiency_level, Unset):
            proficiency_level = UNSET
        else:
            proficiency_level = ProficiencyLevelEnum(_proficiency_level)

        def _parse_years_experience(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        years_experience = _parse_years_experience(d.pop("years_experience", UNSET))

        def _parse_last_active_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_active_date_type_0 = isoparse(data).date()

                return last_active_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        last_active_date = _parse_last_active_date(d.pop("last_active_date", UNSET))

        reviewer_expertise = cls(
            uuid=uuid,
            expertise_keyword=expertise_keyword,
            expertise_category_name=expertise_category_name,
            created=created,
            expertise_category=expertise_category,
            proficiency_level=proficiency_level,
            years_experience=years_experience,
            last_active_date=last_active_date,
        )

        reviewer_expertise.additional_properties = d
        return reviewer_expertise

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
