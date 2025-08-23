from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ai_agent_input_transforms_additional_property_type_0 import (
        AiAgentInputTransformsAdditionalPropertyType0,
    )
    from ..models.ai_agent_input_transforms_additional_property_type_1 import (
        AiAgentInputTransformsAdditionalPropertyType1,
    )


T = TypeVar("T", bound="AiAgentInputTransforms")


@_attrs_define
class AiAgentInputTransforms:
    """ """

    additional_properties: Dict[
        str, Union["AiAgentInputTransformsAdditionalPropertyType0", "AiAgentInputTransformsAdditionalPropertyType1"]
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.ai_agent_input_transforms_additional_property_type_0 import (
            AiAgentInputTransformsAdditionalPropertyType0,
        )

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, AiAgentInputTransformsAdditionalPropertyType0):
                field_dict[prop_name] = prop.to_dict()

            else:
                field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_agent_input_transforms_additional_property_type_0 import (
            AiAgentInputTransformsAdditionalPropertyType0,
        )
        from ..models.ai_agent_input_transforms_additional_property_type_1 import (
            AiAgentInputTransformsAdditionalPropertyType1,
        )

        d = src_dict.copy()
        ai_agent_input_transforms = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> Union[
                "AiAgentInputTransformsAdditionalPropertyType0", "AiAgentInputTransformsAdditionalPropertyType1"
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_0 = AiAgentInputTransformsAdditionalPropertyType0.from_dict(data)

                    return additional_property_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                additional_property_type_1 = AiAgentInputTransformsAdditionalPropertyType1.from_dict(data)

                return additional_property_type_1

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        ai_agent_input_transforms.additional_properties = additional_properties
        return ai_agent_input_transforms

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> Union["AiAgentInputTransformsAdditionalPropertyType0", "AiAgentInputTransformsAdditionalPropertyType1"]:
        return self.additional_properties[key]

    def __setitem__(
        self,
        key: str,
        value: Union["AiAgentInputTransformsAdditionalPropertyType0", "AiAgentInputTransformsAdditionalPropertyType1"],
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
