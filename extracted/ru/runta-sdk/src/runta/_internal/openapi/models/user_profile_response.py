from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.user_profile import UserProfile


T = TypeVar("T", bound="UserProfileResponse")


@_attrs_define
class UserProfileResponse:
    """Response envelope.

    Attributes:
        data (UserProfile): Minimal current-user identity available to user-authorized device clients.
    """

    data: UserProfile

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_profile import UserProfile

        d = dict(src_dict)
        data = UserProfile.from_dict(d.pop("data"))

        user_profile_response = cls(
            data=data,
        )

        return user_profile_response
