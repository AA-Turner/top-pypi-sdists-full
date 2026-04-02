import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.coi_disclosure_financial_interest import COIDisclosureFinancialInterest


T = TypeVar("T", bound="COIDisclosureForm")


@_attrs_define
class COIDisclosureForm:
    """
    Attributes:
        url (str):
        uuid (UUID):
        reviewer (str):
        reviewer_uuid (UUID):
        reviewer_name (str):
        call_uuid (UUID):
        call_name (str):
        certification_date (Union[None, datetime.datetime]):
        financial_interests (list['COIDisclosureFinancialInterest']):
        valid_until (datetime.date): Typically 1 year from certification
        is_current (bool):
        created (datetime.datetime):
        call (Union[None, Unset, str]): Null for general annual disclosure
        certified (Union[Unset, bool]):
        certification_statement (Union[Unset, str]): Legal text they agreed to
        has_financial_interests (Union[Unset, bool]):
        has_personal_relationships (Union[Unset, bool]):
        personal_relationships (Union[Unset, Any]):
        has_other_conflicts (Union[Unset, bool]):
        other_conflicts_description (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    reviewer: str
    reviewer_uuid: UUID
    reviewer_name: str
    call_uuid: UUID
    call_name: str
    certification_date: Union[None, datetime.datetime]
    financial_interests: list["COIDisclosureFinancialInterest"]
    valid_until: datetime.date
    is_current: bool
    created: datetime.datetime
    call: Union[None, Unset, str] = UNSET
    certified: Union[Unset, bool] = UNSET
    certification_statement: Union[Unset, str] = UNSET
    has_financial_interests: Union[Unset, bool] = UNSET
    has_personal_relationships: Union[Unset, bool] = UNSET
    personal_relationships: Union[Unset, Any] = UNSET
    has_other_conflicts: Union[Unset, bool] = UNSET
    other_conflicts_description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        reviewer = self.reviewer

        reviewer_uuid = str(self.reviewer_uuid)

        reviewer_name = self.reviewer_name

        call_uuid = str(self.call_uuid)

        call_name = self.call_name

        certification_date: Union[None, str]
        if isinstance(self.certification_date, datetime.datetime):
            certification_date = self.certification_date.isoformat()
        else:
            certification_date = self.certification_date

        financial_interests = []
        for financial_interests_item_data in self.financial_interests:
            financial_interests_item = financial_interests_item_data.to_dict()
            financial_interests.append(financial_interests_item)

        valid_until = self.valid_until.isoformat()

        is_current = self.is_current

        created = self.created.isoformat()

        call: Union[None, Unset, str]
        if isinstance(self.call, Unset):
            call = UNSET
        else:
            call = self.call

        certified = self.certified

        certification_statement = self.certification_statement

        has_financial_interests = self.has_financial_interests

        has_personal_relationships = self.has_personal_relationships

        personal_relationships = self.personal_relationships

        has_other_conflicts = self.has_other_conflicts

        other_conflicts_description = self.other_conflicts_description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "reviewer": reviewer,
                "reviewer_uuid": reviewer_uuid,
                "reviewer_name": reviewer_name,
                "call_uuid": call_uuid,
                "call_name": call_name,
                "certification_date": certification_date,
                "financial_interests": financial_interests,
                "valid_until": valid_until,
                "is_current": is_current,
                "created": created,
            }
        )
        if call is not UNSET:
            field_dict["call"] = call
        if certified is not UNSET:
            field_dict["certified"] = certified
        if certification_statement is not UNSET:
            field_dict["certification_statement"] = certification_statement
        if has_financial_interests is not UNSET:
            field_dict["has_financial_interests"] = has_financial_interests
        if has_personal_relationships is not UNSET:
            field_dict["has_personal_relationships"] = has_personal_relationships
        if personal_relationships is not UNSET:
            field_dict["personal_relationships"] = personal_relationships
        if has_other_conflicts is not UNSET:
            field_dict["has_other_conflicts"] = has_other_conflicts
        if other_conflicts_description is not UNSET:
            field_dict["other_conflicts_description"] = other_conflicts_description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.coi_disclosure_financial_interest import COIDisclosureFinancialInterest

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        reviewer = d.pop("reviewer")

        reviewer_uuid = UUID(d.pop("reviewer_uuid"))

        reviewer_name = d.pop("reviewer_name")

        call_uuid = UUID(d.pop("call_uuid"))

        call_name = d.pop("call_name")

        def _parse_certification_date(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                certification_date_type_0 = isoparse(data)

                return certification_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        certification_date = _parse_certification_date(d.pop("certification_date"))

        financial_interests = []
        _financial_interests = d.pop("financial_interests")
        for financial_interests_item_data in _financial_interests:
            financial_interests_item = COIDisclosureFinancialInterest.from_dict(financial_interests_item_data)

            financial_interests.append(financial_interests_item)

        valid_until = isoparse(d.pop("valid_until")).date()

        is_current = d.pop("is_current")

        created = isoparse(d.pop("created"))

        def _parse_call(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        call = _parse_call(d.pop("call", UNSET))

        certified = d.pop("certified", UNSET)

        certification_statement = d.pop("certification_statement", UNSET)

        has_financial_interests = d.pop("has_financial_interests", UNSET)

        has_personal_relationships = d.pop("has_personal_relationships", UNSET)

        personal_relationships = d.pop("personal_relationships", UNSET)

        has_other_conflicts = d.pop("has_other_conflicts", UNSET)

        other_conflicts_description = d.pop("other_conflicts_description", UNSET)

        coi_disclosure_form = cls(
            url=url,
            uuid=uuid,
            reviewer=reviewer,
            reviewer_uuid=reviewer_uuid,
            reviewer_name=reviewer_name,
            call_uuid=call_uuid,
            call_name=call_name,
            certification_date=certification_date,
            financial_interests=financial_interests,
            valid_until=valid_until,
            is_current=is_current,
            created=created,
            call=call,
            certified=certified,
            certification_statement=certification_statement,
            has_financial_interests=has_financial_interests,
            has_personal_relationships=has_personal_relationships,
            personal_relationships=personal_relationships,
            has_other_conflicts=has_other_conflicts,
            other_conflicts_description=other_conflicts_description,
        )

        coi_disclosure_form.additional_properties = d
        return coi_disclosure_form

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
