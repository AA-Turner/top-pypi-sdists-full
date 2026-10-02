import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="CustomerPermissionReview")


@_attrs_define
class CustomerPermissionReview:
    """
    Attributes:
        url (str):
        uuid (UUID):
        reviewer_full_name (Union[None, str]):
        reviewer_uuid (Union[None, UUID]):
        is_pending (bool):
        created (datetime.datetime):
        closed (Union[None, datetime.datetime]):
        customer_uuid (UUID):
        customer_name (str):
    """

    url: str
    uuid: UUID
    reviewer_full_name: Union[None, str]
    reviewer_uuid: Union[None, UUID]
    is_pending: bool
    created: datetime.datetime
    closed: Union[None, datetime.datetime]
    customer_uuid: UUID
    customer_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        reviewer_full_name: Union[None, str]
        reviewer_full_name = self.reviewer_full_name

        reviewer_uuid: Union[None, str]
        if isinstance(self.reviewer_uuid, UUID):
            reviewer_uuid = str(self.reviewer_uuid)
        else:
            reviewer_uuid = self.reviewer_uuid

        is_pending = self.is_pending

        created = self.created.isoformat()

        closed: Union[None, str]
        if isinstance(self.closed, datetime.datetime):
            closed = self.closed.isoformat()
        else:
            closed = self.closed

        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "reviewer_full_name": reviewer_full_name,
                "reviewer_uuid": reviewer_uuid,
                "is_pending": is_pending,
                "created": created,
                "closed": closed,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        def _parse_reviewer_full_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        reviewer_full_name = _parse_reviewer_full_name(d.pop("reviewer_full_name"))

        def _parse_reviewer_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reviewer_uuid_type_0 = UUID(data)

                return reviewer_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        reviewer_uuid = _parse_reviewer_uuid(d.pop("reviewer_uuid"))

        is_pending = d.pop("is_pending")

        created = isoparse(d.pop("created"))

        def _parse_closed(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                closed_type_0 = isoparse(data)

                return closed_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        closed = _parse_closed(d.pop("closed"))

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        customer_permission_review = cls(
            url=url,
            uuid=uuid,
            reviewer_full_name=reviewer_full_name,
            reviewer_uuid=reviewer_uuid,
            is_pending=is_pending,
            created=created,
            closed=closed,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
        )

        customer_permission_review.additional_properties = d
        return customer_permission_review

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
