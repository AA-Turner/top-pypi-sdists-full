from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_onboarding_profile_response_200_profile import GetOnboardingProfileResponse200Profile


T = TypeVar("T", bound="GetOnboardingProfileResponse200")


@_attrs_define
class GetOnboardingProfileResponse200:
    """
    Attributes:
        profile (Union[Unset, None, GetOnboardingProfileResponse200Profile]):
    """

    profile: Union[Unset, None, "GetOnboardingProfileResponse200Profile"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        profile: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict() if self.profile else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if profile is not UNSET:
            field_dict["profile"] = profile

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_onboarding_profile_response_200_profile import GetOnboardingProfileResponse200Profile

        d = src_dict.copy()
        _profile = d.pop("profile", UNSET)
        profile: Union[Unset, None, GetOnboardingProfileResponse200Profile]
        if _profile is None:
            profile = None
        elif isinstance(_profile, Unset):
            profile = UNSET
        else:
            profile = GetOnboardingProfileResponse200Profile.from_dict(_profile)

        get_onboarding_profile_response_200 = cls(
            profile=profile,
        )

        get_onboarding_profile_response_200.additional_properties = d
        return get_onboarding_profile_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
