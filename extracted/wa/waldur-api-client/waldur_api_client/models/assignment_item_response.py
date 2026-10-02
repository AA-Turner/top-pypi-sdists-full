from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AssignmentItemResponse")


@_attrs_define
class AssignmentItemResponse:
    """
    Attributes:
        detail (str):
        review_uuid (Union[None, UUID, Unset]): UUID of created review (only on accept)
    """

    detail: str
    review_uuid: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail = self.detail

        review_uuid: Union[None, Unset, str]
        if isinstance(self.review_uuid, Unset):
            review_uuid = UNSET
        elif isinstance(self.review_uuid, UUID):
            review_uuid = str(self.review_uuid)
        else:
            review_uuid = self.review_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "detail": detail,
            }
        )
        if review_uuid is not UNSET:
            field_dict["review_uuid"] = review_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        detail = d.pop("detail")

        def _parse_review_uuid(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                review_uuid_type_0 = UUID(data)

                return review_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        review_uuid = _parse_review_uuid(d.pop("review_uuid", UNSET))

        assignment_item_response = cls(
            detail=detail,
            review_uuid=review_uuid,
        )

        assignment_item_response.additional_properties = d
        return assignment_item_response

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
