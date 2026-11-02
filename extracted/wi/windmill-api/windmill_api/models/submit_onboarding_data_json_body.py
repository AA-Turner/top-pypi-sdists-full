from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SubmitOnboardingDataJsonBody")


@_attrs_define
class SubmitOnboardingDataJsonBody:
    """
    Attributes:
        touch_point (Union[Unset, str]):
        use_case (Union[Unset, str]):
    """

    touch_point: Union[Unset, str] = UNSET
    use_case: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        touch_point = self.touch_point
        use_case = self.use_case

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if touch_point is not UNSET:
            field_dict["touch_point"] = touch_point
        if use_case is not UNSET:
            field_dict["use_case"] = use_case

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        touch_point = d.pop("touch_point", UNSET)

        use_case = d.pop("use_case", UNSET)

        submit_onboarding_data_json_body = cls(
            touch_point=touch_point,
            use_case=use_case,
        )

        submit_onboarding_data_json_body.additional_properties = d
        return submit_onboarding_data_json_body

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
