from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.ai_agent_tool_inputs_additional_property_additional_property_type_0 import (
        AiAgentToolInputsAdditionalPropertyAdditionalPropertyType0,
    )
    from ..models.ai_agent_tool_inputs_additional_property_additional_property_type_1 import (
        AiAgentToolInputsAdditionalPropertyAdditionalPropertyType1,
    )
    from ..models.ai_agent_tool_inputs_additional_property_additional_property_type_2 import (
        AiAgentToolInputsAdditionalPropertyAdditionalPropertyType2,
    )


T = TypeVar("T", bound="AiAgentToolInputsAdditionalProperty")


@_attrs_define
class AiAgentToolInputsAdditionalProperty:
    """ """

    additional_properties: Dict[
        str,
        Union[
            "AiAgentToolInputsAdditionalPropertyAdditionalPropertyType0",
            "AiAgentToolInputsAdditionalPropertyAdditionalPropertyType1",
            "AiAgentToolInputsAdditionalPropertyAdditionalPropertyType2",
        ],
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.ai_agent_tool_inputs_additional_property_additional_property_type_0 import (
            AiAgentToolInputsAdditionalPropertyAdditionalPropertyType0,
        )
        from ..models.ai_agent_tool_inputs_additional_property_additional_property_type_1 import (
            AiAgentToolInputsAdditionalPropertyAdditionalPropertyType1,
        )

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, AiAgentToolInputsAdditionalPropertyAdditionalPropertyType0):
                field_dict[prop_name] = prop.to_dict()

            elif isinstance(prop, AiAgentToolInputsAdditionalPropertyAdditionalPropertyType1):
                field_dict[prop_name] = prop.to_dict()

            else:
                field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_agent_tool_inputs_additional_property_additional_property_type_0 import (
            AiAgentToolInputsAdditionalPropertyAdditionalPropertyType0,
        )
        from ..models.ai_agent_tool_inputs_additional_property_additional_property_type_1 import (
            AiAgentToolInputsAdditionalPropertyAdditionalPropertyType1,
        )
        from ..models.ai_agent_tool_inputs_additional_property_additional_property_type_2 import (
            AiAgentToolInputsAdditionalPropertyAdditionalPropertyType2,
        )

        d = src_dict.copy()
        ai_agent_tool_inputs_additional_property = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> Union[
                "AiAgentToolInputsAdditionalPropertyAdditionalPropertyType0",
                "AiAgentToolInputsAdditionalPropertyAdditionalPropertyType1",
                "AiAgentToolInputsAdditionalPropertyAdditionalPropertyType2",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_0 = AiAgentToolInputsAdditionalPropertyAdditionalPropertyType0.from_dict(
                        data
                    )

                    return additional_property_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_1 = AiAgentToolInputsAdditionalPropertyAdditionalPropertyType1.from_dict(
                        data
                    )

                    return additional_property_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                additional_property_type_2 = AiAgentToolInputsAdditionalPropertyAdditionalPropertyType2.from_dict(data)

                return additional_property_type_2

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        ai_agent_tool_inputs_additional_property.additional_properties = additional_properties
        return ai_agent_tool_inputs_additional_property

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> Union[
        "AiAgentToolInputsAdditionalPropertyAdditionalPropertyType0",
        "AiAgentToolInputsAdditionalPropertyAdditionalPropertyType1",
        "AiAgentToolInputsAdditionalPropertyAdditionalPropertyType2",
    ]:
        return self.additional_properties[key]

    def __setitem__(
        self,
        key: str,
        value: Union[
            "AiAgentToolInputsAdditionalPropertyAdditionalPropertyType0",
            "AiAgentToolInputsAdditionalPropertyAdditionalPropertyType1",
            "AiAgentToolInputsAdditionalPropertyAdditionalPropertyType2",
        ],
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
