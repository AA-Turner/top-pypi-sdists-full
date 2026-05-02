from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_app_by_path_response_200_policy_triggerables_v2_additional_property import (
        GetAppByPathResponse200PolicyTriggerablesV2AdditionalProperty,
    )


T = TypeVar("T", bound="GetAppByPathResponse200PolicyTriggerablesV2")


@_attrs_define
class GetAppByPathResponse200PolicyTriggerablesV2:
    """ """

    additional_properties: Dict[str, "GetAppByPathResponse200PolicyTriggerablesV2AdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_app_by_path_response_200_policy_triggerables_v2_additional_property import (
            GetAppByPathResponse200PolicyTriggerablesV2AdditionalProperty,
        )

        d = src_dict.copy()
        get_app_by_path_response_200_policy_triggerables_v2 = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = GetAppByPathResponse200PolicyTriggerablesV2AdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        get_app_by_path_response_200_policy_triggerables_v2.additional_properties = additional_properties
        return get_app_by_path_response_200_policy_triggerables_v2

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "GetAppByPathResponse200PolicyTriggerablesV2AdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "GetAppByPathResponse200PolicyTriggerablesV2AdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
