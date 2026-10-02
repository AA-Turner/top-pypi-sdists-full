import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RemoteProjectUpdateRequest")


@_attrs_define
class RemoteProjectUpdateRequest:
    """
    Attributes:
        uuid (UUID):
        state (str):
        customer_name (str):
        customer_uuid (str):
        offering_name (str):
        offering_uuid (UUID):
        created (datetime.datetime):
        reviewed_at (Union[None, datetime.datetime]): Timestamp when the review was completed
        reviewed_by_full_name (str):
        reviewed_by_uuid (UUID):
        old_oecd_fos_2007_label (str):
        new_oecd_fos_2007_label (str):
        review_comment (Union[None, Unset, str]): Optional comment provided during review
        old_name (Union[Unset, str]):
        new_name (Union[Unset, str]):
        old_description (Union[Unset, str]):
        new_description (Union[Unset, str]):
        old_end_date (Union[None, Unset, datetime.date]):
        new_end_date (Union[None, Unset, datetime.date]):
        old_oecd_fos_2007_code (Union[None, Unset, str]):
        new_oecd_fos_2007_code (Union[None, Unset, str]):
        old_is_industry (Union[None, Unset, bool]):
        new_is_industry (Union[None, Unset, bool]):
        created_by (Union[None, Unset, int]):
    """

    uuid: UUID
    state: str
    customer_name: str
    customer_uuid: str
    offering_name: str
    offering_uuid: UUID
    created: datetime.datetime
    reviewed_at: Union[None, datetime.datetime]
    reviewed_by_full_name: str
    reviewed_by_uuid: UUID
    old_oecd_fos_2007_label: str
    new_oecd_fos_2007_label: str
    review_comment: Union[None, Unset, str] = UNSET
    old_name: Union[Unset, str] = UNSET
    new_name: Union[Unset, str] = UNSET
    old_description: Union[Unset, str] = UNSET
    new_description: Union[Unset, str] = UNSET
    old_end_date: Union[None, Unset, datetime.date] = UNSET
    new_end_date: Union[None, Unset, datetime.date] = UNSET
    old_oecd_fos_2007_code: Union[None, Unset, str] = UNSET
    new_oecd_fos_2007_code: Union[None, Unset, str] = UNSET
    old_is_industry: Union[None, Unset, bool] = UNSET
    new_is_industry: Union[None, Unset, bool] = UNSET
    created_by: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        state = self.state

        customer_name = self.customer_name

        customer_uuid = self.customer_uuid

        offering_name = self.offering_name

        offering_uuid = str(self.offering_uuid)

        created = self.created.isoformat()

        reviewed_at: Union[None, str]
        if isinstance(self.reviewed_at, datetime.datetime):
            reviewed_at = self.reviewed_at.isoformat()
        else:
            reviewed_at = self.reviewed_at

        reviewed_by_full_name = self.reviewed_by_full_name

        reviewed_by_uuid = str(self.reviewed_by_uuid)

        old_oecd_fos_2007_label = self.old_oecd_fos_2007_label

        new_oecd_fos_2007_label = self.new_oecd_fos_2007_label

        review_comment: Union[None, Unset, str]
        if isinstance(self.review_comment, Unset):
            review_comment = UNSET
        else:
            review_comment = self.review_comment

        old_name = self.old_name

        new_name = self.new_name

        old_description = self.old_description

        new_description = self.new_description

        old_end_date: Union[None, Unset, str]
        if isinstance(self.old_end_date, Unset):
            old_end_date = UNSET
        elif isinstance(self.old_end_date, datetime.date):
            old_end_date = self.old_end_date.isoformat()
        else:
            old_end_date = self.old_end_date

        new_end_date: Union[None, Unset, str]
        if isinstance(self.new_end_date, Unset):
            new_end_date = UNSET
        elif isinstance(self.new_end_date, datetime.date):
            new_end_date = self.new_end_date.isoformat()
        else:
            new_end_date = self.new_end_date

        old_oecd_fos_2007_code: Union[None, Unset, str]
        if isinstance(self.old_oecd_fos_2007_code, Unset):
            old_oecd_fos_2007_code = UNSET
        else:
            old_oecd_fos_2007_code = self.old_oecd_fos_2007_code

        new_oecd_fos_2007_code: Union[None, Unset, str]
        if isinstance(self.new_oecd_fos_2007_code, Unset):
            new_oecd_fos_2007_code = UNSET
        else:
            new_oecd_fos_2007_code = self.new_oecd_fos_2007_code

        old_is_industry: Union[None, Unset, bool]
        if isinstance(self.old_is_industry, Unset):
            old_is_industry = UNSET
        else:
            old_is_industry = self.old_is_industry

        new_is_industry: Union[None, Unset, bool]
        if isinstance(self.new_is_industry, Unset):
            new_is_industry = UNSET
        else:
            new_is_industry = self.new_is_industry

        created_by: Union[None, Unset, int]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "state": state,
                "customer_name": customer_name,
                "customer_uuid": customer_uuid,
                "offering_name": offering_name,
                "offering_uuid": offering_uuid,
                "created": created,
                "reviewed_at": reviewed_at,
                "reviewed_by_full_name": reviewed_by_full_name,
                "reviewed_by_uuid": reviewed_by_uuid,
                "old_oecd_fos_2007_label": old_oecd_fos_2007_label,
                "new_oecd_fos_2007_label": new_oecd_fos_2007_label,
            }
        )
        if review_comment is not UNSET:
            field_dict["review_comment"] = review_comment
        if old_name is not UNSET:
            field_dict["old_name"] = old_name
        if new_name is not UNSET:
            field_dict["new_name"] = new_name
        if old_description is not UNSET:
            field_dict["old_description"] = old_description
        if new_description is not UNSET:
            field_dict["new_description"] = new_description
        if old_end_date is not UNSET:
            field_dict["old_end_date"] = old_end_date
        if new_end_date is not UNSET:
            field_dict["new_end_date"] = new_end_date
        if old_oecd_fos_2007_code is not UNSET:
            field_dict["old_oecd_fos_2007_code"] = old_oecd_fos_2007_code
        if new_oecd_fos_2007_code is not UNSET:
            field_dict["new_oecd_fos_2007_code"] = new_oecd_fos_2007_code
        if old_is_industry is not UNSET:
            field_dict["old_is_industry"] = old_is_industry
        if new_is_industry is not UNSET:
            field_dict["new_is_industry"] = new_is_industry
        if created_by is not UNSET:
            field_dict["created_by"] = created_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        state = d.pop("state")

        customer_name = d.pop("customer_name")

        customer_uuid = d.pop("customer_uuid")

        offering_name = d.pop("offering_name")

        offering_uuid = UUID(d.pop("offering_uuid"))

        created = isoparse(d.pop("created"))

        def _parse_reviewed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reviewed_at_type_0 = isoparse(data)

                return reviewed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        reviewed_at = _parse_reviewed_at(d.pop("reviewed_at"))

        reviewed_by_full_name = d.pop("reviewed_by_full_name")

        reviewed_by_uuid = UUID(d.pop("reviewed_by_uuid"))

        old_oecd_fos_2007_label = d.pop("old_oecd_fos_2007_label")

        new_oecd_fos_2007_label = d.pop("new_oecd_fos_2007_label")

        def _parse_review_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        review_comment = _parse_review_comment(d.pop("review_comment", UNSET))

        old_name = d.pop("old_name", UNSET)

        new_name = d.pop("new_name", UNSET)

        old_description = d.pop("old_description", UNSET)

        new_description = d.pop("new_description", UNSET)

        def _parse_old_end_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                old_end_date_type_0 = isoparse(data).date()

                return old_end_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        old_end_date = _parse_old_end_date(d.pop("old_end_date", UNSET))

        def _parse_new_end_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                new_end_date_type_0 = isoparse(data).date()

                return new_end_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        new_end_date = _parse_new_end_date(d.pop("new_end_date", UNSET))

        def _parse_old_oecd_fos_2007_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        old_oecd_fos_2007_code = _parse_old_oecd_fos_2007_code(d.pop("old_oecd_fos_2007_code", UNSET))

        def _parse_new_oecd_fos_2007_code(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        new_oecd_fos_2007_code = _parse_new_oecd_fos_2007_code(d.pop("new_oecd_fos_2007_code", UNSET))

        def _parse_old_is_industry(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        old_is_industry = _parse_old_is_industry(d.pop("old_is_industry", UNSET))

        def _parse_new_is_industry(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        new_is_industry = _parse_new_is_industry(d.pop("new_is_industry", UNSET))

        def _parse_created_by(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        remote_project_update_request = cls(
            uuid=uuid,
            state=state,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            created=created,
            reviewed_at=reviewed_at,
            reviewed_by_full_name=reviewed_by_full_name,
            reviewed_by_uuid=reviewed_by_uuid,
            old_oecd_fos_2007_label=old_oecd_fos_2007_label,
            new_oecd_fos_2007_label=new_oecd_fos_2007_label,
            review_comment=review_comment,
            old_name=old_name,
            new_name=new_name,
            old_description=old_description,
            new_description=new_description,
            old_end_date=old_end_date,
            new_end_date=new_end_date,
            old_oecd_fos_2007_code=old_oecd_fos_2007_code,
            new_oecd_fos_2007_code=new_oecd_fos_2007_code,
            old_is_industry=old_is_industry,
            new_is_industry=new_is_industry,
            created_by=created_by,
        )

        remote_project_update_request.additional_properties = d
        return remote_project_update_request

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
