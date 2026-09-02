from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.create_app_raw_source_json_body_policy_triggerables_v2_additional_property import (
        CreateAppRawSourceJsonBodyPolicyTriggerablesV2AdditionalProperty,
    )


T = TypeVar("T", bound="CreateAppRawSourceJsonBodyPolicyTriggerablesV2")


@_attrs_define
class CreateAppRawSourceJsonBodyPolicyTriggerablesV2:
    """ """

    additional_properties: Dict[str, "CreateAppRawSourceJsonBodyPolicyTriggerablesV2AdditionalProperty"] = _attrs_field(
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
        from ..models.create_app_raw_source_json_body_policy_triggerables_v2_additional_property import (
            CreateAppRawSourceJsonBodyPolicyTriggerablesV2AdditionalProperty,
        )

        d = src_dict.copy()
        create_app_raw_source_json_body_policy_triggerables_v2 = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = CreateAppRawSourceJsonBodyPolicyTriggerablesV2AdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        create_app_raw_source_json_body_policy_triggerables_v2.additional_properties = additional_properties
        return create_app_raw_source_json_body_policy_triggerables_v2

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "CreateAppRawSourceJsonBodyPolicyTriggerablesV2AdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "CreateAppRawSourceJsonBodyPolicyTriggerablesV2AdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
