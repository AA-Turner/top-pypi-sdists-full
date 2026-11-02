from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.create_app_raw_multipart_data_app_policy_triggerables_additional_property import (
        CreateAppRawMultipartDataAppPolicyTriggerablesAdditionalProperty,
    )


T = TypeVar("T", bound="CreateAppRawMultipartDataAppPolicyTriggerables")


@_attrs_define
class CreateAppRawMultipartDataAppPolicyTriggerables:
    """ """

    additional_properties: Dict[str, "CreateAppRawMultipartDataAppPolicyTriggerablesAdditionalProperty"] = _attrs_field(
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
        from ..models.create_app_raw_multipart_data_app_policy_triggerables_additional_property import (
            CreateAppRawMultipartDataAppPolicyTriggerablesAdditionalProperty,
        )

        d = src_dict.copy()
        create_app_raw_multipart_data_app_policy_triggerables = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = CreateAppRawMultipartDataAppPolicyTriggerablesAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        create_app_raw_multipart_data_app_policy_triggerables.additional_properties = additional_properties
        return create_app_raw_multipart_data_app_policy_triggerables

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "CreateAppRawMultipartDataAppPolicyTriggerablesAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "CreateAppRawMultipartDataAppPolicyTriggerablesAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
