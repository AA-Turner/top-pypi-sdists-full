import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceEndDateChangeRequestRequest")


@_attrs_define
class ResourceEndDateChangeRequestRequest:
    """
    Attributes:
        resource (str):
        requested_end_date (datetime.date): The requested new end date for the resource
        comment (Union[None, Unset, str]): Optional comment from the requester
        review_comment (Union[None, Unset, str]): Optional comment provided during review
    """

    resource: str
    requested_end_date: datetime.date
    comment: Union[None, Unset, str] = UNSET
    review_comment: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource = self.resource

        requested_end_date = self.requested_end_date.isoformat()

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
                "resource": resource,
                "requested_end_date": requested_end_date,
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
        resource = d.pop("resource")

        requested_end_date = isoparse(d.pop("requested_end_date")).date()

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

        resource_end_date_change_request_request = cls(
            resource=resource,
            requested_end_date=requested_end_date,
            comment=comment,
            review_comment=review_comment,
        )

        resource_end_date_change_request_request.additional_properties = d
        return resource_end_date_change_request_request

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
