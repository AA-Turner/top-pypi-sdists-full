from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedReviewerProfileRequest")


@_attrs_define
class PatchedReviewerProfileRequest:
    """
    Attributes:
        orcid_id (Union[None, Unset, str]): ORCID identifier (format: 0000-0000-0000-0000)
        biography (Union[Unset, str]): Professional biography / summary
        alternative_names (Union[Unset, Any]): List of name variants used in publications
        available_for_reviews (Union[Unset, bool]): Whether reviewer is currently accepting review requests
    """

    orcid_id: Union[None, Unset, str] = UNSET
    biography: Union[Unset, str] = UNSET
    alternative_names: Union[Unset, Any] = UNSET
    available_for_reviews: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        orcid_id: Union[None, Unset, str]
        if isinstance(self.orcid_id, Unset):
            orcid_id = UNSET
        else:
            orcid_id = self.orcid_id

        biography = self.biography

        alternative_names = self.alternative_names

        available_for_reviews = self.available_for_reviews

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if orcid_id is not UNSET:
            field_dict["orcid_id"] = orcid_id
        if biography is not UNSET:
            field_dict["biography"] = biography
        if alternative_names is not UNSET:
            field_dict["alternative_names"] = alternative_names
        if available_for_reviews is not UNSET:
            field_dict["available_for_reviews"] = available_for_reviews

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_orcid_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        orcid_id = _parse_orcid_id(d.pop("orcid_id", UNSET))

        biography = d.pop("biography", UNSET)

        alternative_names = d.pop("alternative_names", UNSET)

        available_for_reviews = d.pop("available_for_reviews", UNSET)

        patched_reviewer_profile_request = cls(
            orcid_id=orcid_id,
            biography=biography,
            alternative_names=alternative_names,
            available_for_reviews=available_for_reviews,
        )

        patched_reviewer_profile_request.additional_properties = d
        return patched_reviewer_profile_request

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
