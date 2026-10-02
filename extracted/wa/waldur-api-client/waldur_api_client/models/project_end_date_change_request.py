import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectEndDateChangeRequest")


@_attrs_define
class ProjectEndDateChangeRequest:
    """
    Attributes:
        url (str):
        uuid (UUID):
        state (str):
        project (str):
        project_uuid (UUID):
        project_name (str):
        customer_uuid (UUID):
        customer_name (str):
        requested_end_date (datetime.date): The requested new end date for the project
        created (datetime.datetime):
        created_by_uuid (Union[None, UUID]):
        created_by_full_name (Union[None, str]):
        reviewed_at (Union[None, datetime.datetime]): Timestamp when the review was completed
        reviewed_by_uuid (Union[None, UUID]):
        reviewed_by_full_name (Union[None, str]):
        comment (Union[None, Unset, str]): Optional comment from the requester
        review_comment (Union[None, Unset, str]): Optional comment provided during review
    """

    url: str
    uuid: UUID
    state: str
    project: str
    project_uuid: UUID
    project_name: str
    customer_uuid: UUID
    customer_name: str
    requested_end_date: datetime.date
    created: datetime.datetime
    created_by_uuid: Union[None, UUID]
    created_by_full_name: Union[None, str]
    reviewed_at: Union[None, datetime.datetime]
    reviewed_by_uuid: Union[None, UUID]
    reviewed_by_full_name: Union[None, str]
    comment: Union[None, Unset, str] = UNSET
    review_comment: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        state = self.state

        project = self.project

        project_uuid = str(self.project_uuid)

        project_name = self.project_name

        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        requested_end_date = self.requested_end_date.isoformat()

        created = self.created.isoformat()

        created_by_uuid: Union[None, str]
        if isinstance(self.created_by_uuid, UUID):
            created_by_uuid = str(self.created_by_uuid)
        else:
            created_by_uuid = self.created_by_uuid

        created_by_full_name: Union[None, str]
        created_by_full_name = self.created_by_full_name

        reviewed_at: Union[None, str]
        if isinstance(self.reviewed_at, datetime.datetime):
            reviewed_at = self.reviewed_at.isoformat()
        else:
            reviewed_at = self.reviewed_at

        reviewed_by_uuid: Union[None, str]
        if isinstance(self.reviewed_by_uuid, UUID):
            reviewed_by_uuid = str(self.reviewed_by_uuid)
        else:
            reviewed_by_uuid = self.reviewed_by_uuid

        reviewed_by_full_name: Union[None, str]
        reviewed_by_full_name = self.reviewed_by_full_name

        comment: Union[None, Unset, str]
        if isinstance(self.comment, Unset):
            comment = UNSET
        else:
            comment = self.comment

        review_comment: Union[None, Unset, str]
        if isinstance(self.review_comment, Unset):
            review_comment = UNSET
        else:
            review_comment = self.review_comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "state": state,
                "project": project,
                "project_uuid": project_uuid,
                "project_name": project_name,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "requested_end_date": requested_end_date,
                "created": created,
                "created_by_uuid": created_by_uuid,
                "created_by_full_name": created_by_full_name,
                "reviewed_at": reviewed_at,
                "reviewed_by_uuid": reviewed_by_uuid,
                "reviewed_by_full_name": reviewed_by_full_name,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment
        if review_comment is not UNSET:
            field_dict["review_comment"] = review_comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        state = d.pop("state")

        project = d.pop("project")

        project_uuid = UUID(d.pop("project_uuid"))

        project_name = d.pop("project_name")

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        requested_end_date = isoparse(d.pop("requested_end_date")).date()

        created = isoparse(d.pop("created"))

        def _parse_created_by_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_by_uuid_type_0 = UUID(data)

                return created_by_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        created_by_uuid = _parse_created_by_uuid(d.pop("created_by_uuid"))

        def _parse_created_by_full_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        created_by_full_name = _parse_created_by_full_name(d.pop("created_by_full_name"))

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

        def _parse_reviewed_by_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reviewed_by_uuid_type_0 = UUID(data)

                return reviewed_by_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        reviewed_by_uuid = _parse_reviewed_by_uuid(d.pop("reviewed_by_uuid"))

        def _parse_reviewed_by_full_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reviewed_by_full_name = _parse_reviewed_by_full_name(d.pop("reviewed_by_full_name"))

        def _parse_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment = _parse_comment(d.pop("comment", UNSET))

        def _parse_review_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        review_comment = _parse_review_comment(d.pop("review_comment", UNSET))

        project_end_date_change_request = cls(
            url=url,
            uuid=uuid,
            state=state,
            project=project,
            project_uuid=project_uuid,
            project_name=project_name,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            requested_end_date=requested_end_date,
            created=created,
            created_by_uuid=created_by_uuid,
            created_by_full_name=created_by_full_name,
            reviewed_at=reviewed_at,
            reviewed_by_uuid=reviewed_by_uuid,
            reviewed_by_full_name=reviewed_by_full_name,
            comment=comment,
            review_comment=review_comment,
        )

        project_end_date_change_request.additional_properties = d
        return project_end_date_change_request

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
