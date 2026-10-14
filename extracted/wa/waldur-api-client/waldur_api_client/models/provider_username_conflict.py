from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.provider_username_candidate import ProviderUsernameCandidate


T = TypeVar("T", bound="ProviderUsernameConflict")


@_attrs_define
class ProviderUsernameConflict:
    """
    Attributes:
        user_uuid (str):
        user_username (str):
        user_full_name (str):
        candidates (list['ProviderUsernameCandidate']):
    """

    user_uuid: str
    user_username: str
    user_full_name: str
    candidates: list["ProviderUsernameCandidate"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_uuid = self.user_uuid

        user_username = self.user_username

        user_full_name = self.user_full_name

        candidates = []
        for candidates_item_data in self.candidates:
            candidates_item = candidates_item_data.to_dict()
            candidates.append(candidates_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_uuid": user_uuid,
                "user_username": user_username,
                "user_full_name": user_full_name,
                "candidates": candidates,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provider_username_candidate import ProviderUsernameCandidate

        d = dict(src_dict)
        user_uuid = d.pop("user_uuid")

        user_username = d.pop("user_username")

        user_full_name = d.pop("user_full_name")

        candidates = []
        _candidates = d.pop("candidates")
        for candidates_item_data in _candidates:
            candidates_item = ProviderUsernameCandidate.from_dict(candidates_item_data)

            candidates.append(candidates_item)

        provider_username_conflict = cls(
            user_uuid=user_uuid,
            user_username=user_username,
            user_full_name=user_full_name,
            candidates=candidates,
        )

        provider_username_conflict.additional_properties = d
        return provider_username_conflict

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
