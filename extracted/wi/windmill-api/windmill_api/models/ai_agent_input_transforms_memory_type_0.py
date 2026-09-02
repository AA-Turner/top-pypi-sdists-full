from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ai_agent_input_transforms_memory_type_0_type import AiAgentInputTransformsMemoryType0Type

if TYPE_CHECKING:
    from ..models.ai_agent_input_transforms_memory_type_0_value_type_0 import (
        AiAgentInputTransformsMemoryType0ValueType0,
    )
    from ..models.ai_agent_input_transforms_memory_type_0_value_type_1 import (
        AiAgentInputTransformsMemoryType0ValueType1,
    )
    from ..models.ai_agent_input_transforms_memory_type_0_value_type_2 import (
        AiAgentInputTransformsMemoryType0ValueType2,
    )


T = TypeVar("T", bound="AiAgentInputTransformsMemoryType0")


@_attrs_define
class AiAgentInputTransformsMemoryType0:
    """Static memory configuration passed directly to the AI agent

    Attributes:
        value (Union['AiAgentInputTransformsMemoryType0ValueType0', 'AiAgentInputTransformsMemoryType0ValueType1',
            'AiAgentInputTransformsMemoryType0ValueType2']): Conversation memory configuration
        type (AiAgentInputTransformsMemoryType0Type):
    """

    value: Union[
        "AiAgentInputTransformsMemoryType0ValueType0",
        "AiAgentInputTransformsMemoryType0ValueType1",
        "AiAgentInputTransformsMemoryType0ValueType2",
    ]
    type: AiAgentInputTransformsMemoryType0Type
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.ai_agent_input_transforms_memory_type_0_value_type_0 import (
            AiAgentInputTransformsMemoryType0ValueType0,
        )
        from ..models.ai_agent_input_transforms_memory_type_0_value_type_1 import (
            AiAgentInputTransformsMemoryType0ValueType1,
        )

        value: Dict[str, Any]

        if isinstance(self.value, AiAgentInputTransformsMemoryType0ValueType0):
            value = self.value.to_dict()

        elif isinstance(self.value, AiAgentInputTransformsMemoryType0ValueType1):
            value = self.value.to_dict()

        else:
            value = self.value.to_dict()

        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.ai_agent_input_transforms_memory_type_0_value_type_0 import (
            AiAgentInputTransformsMemoryType0ValueType0,
        )
        from ..models.ai_agent_input_transforms_memory_type_0_value_type_1 import (
            AiAgentInputTransformsMemoryType0ValueType1,
        )
        from ..models.ai_agent_input_transforms_memory_type_0_value_type_2 import (
            AiAgentInputTransformsMemoryType0ValueType2,
        )

        d = src_dict.copy()

        def _parse_value(
            data: object,
        ) -> Union[
            "AiAgentInputTransformsMemoryType0ValueType0",
            "AiAgentInputTransformsMemoryType0ValueType1",
            "AiAgentInputTransformsMemoryType0ValueType2",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_0 = AiAgentInputTransformsMemoryType0ValueType0.from_dict(data)

                return value_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_1 = AiAgentInputTransformsMemoryType0ValueType1.from_dict(data)

                return value_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            value_type_2 = AiAgentInputTransformsMemoryType0ValueType2.from_dict(data)

            return value_type_2

        value = _parse_value(d.pop("value"))

        type = AiAgentInputTransformsMemoryType0Type(d.pop("type"))

        ai_agent_input_transforms_memory_type_0 = cls(
            value=value,
            type=type,
        )

        ai_agent_input_transforms_memory_type_0.additional_properties = d
        return ai_agent_input_transforms_memory_type_0

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
