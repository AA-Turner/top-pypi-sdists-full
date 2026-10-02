from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_limit_change_request_request_requested_limits import (
        ResourceLimitChangeRequestRequestRequestedLimits,
    )


T = TypeVar("T", bound="ResourceLimitChangeRequestRequest")


@_attrs_define
class ResourceLimitChangeRequestRequest:
    """
    Attributes:
        resource (str):
        requested_limits (ResourceLimitChangeRequestRequestRequestedLimits):
        review_comment (Union[None, Unset, str]): Optional comment provided during review
    """

    resource: str
    requested_limits: "ResourceLimitChangeRequestRequestRequestedLimits"
    review_comment: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource = self.resource

        requested_limits = self.requested_limits.to_dict()

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
                "requested_limits": requested_limits,
            }
        )
        if review_comment is not UNSET:
            field_dict["review_comment"] = review_comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_limit_change_request_request_requested_limits import (
            ResourceLimitChangeRequestRequestRequestedLimits,
        )

        d = dict(src_dict)
        resource = d.pop("resource")

        requested_limits = ResourceLimitChangeRequestRequestRequestedLimits.from_dict(d.pop("requested_limits"))

        def _parse_review_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        review_comment = _parse_review_comment(d.pop("review_comment", UNSET))

        resource_limit_change_request_request = cls(
            resource=resource,
            requested_limits=requested_limits,
            review_comment=review_comment,
        )

        resource_limit_change_request_request.additional_properties = d
        return resource_limit_change_request_request

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
