from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SetOnboardingProfileJsonBodyProfile")


@_attrs_define
class SetOnboardingProfileJsonBodyProfile:
    """free-form context from the invite, every key optional. The frontend reads `touch_point` (answers onboarding's source
    question), `company` and `workspace_name` (prefill the first workspace's name), `hub_projects` (slugs surfaced first
    on an empty workspace), `tools` (integrations, used to pick hub projects when none are named) and `starter_prompts`
    (`[{label, prompt}]`, replacing the home page's example prompts); unknown keys are kept and ignored

    """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        set_onboarding_profile_json_body_profile = cls()

        set_onboarding_profile_json_body_profile.additional_properties = d
        return set_onboarding_profile_json_body_profile

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
