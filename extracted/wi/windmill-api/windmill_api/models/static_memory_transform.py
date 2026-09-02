from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.static_memory_transform_type import StaticMemoryTransformType

if TYPE_CHECKING:
    from ..models.static_memory_transform_value_type_0 import StaticMemoryTransformValueType0
    from ..models.static_memory_transform_value_type_1 import StaticMemoryTransformValueType1
    from ..models.static_memory_transform_value_type_2 import StaticMemoryTransformValueType2


T = TypeVar("T", bound="StaticMemoryTransform")


@_attrs_define
class StaticMemoryTransform:
    """Static memory configuration passed directly to the AI agent

    Attributes:
        value (Union['StaticMemoryTransformValueType0', 'StaticMemoryTransformValueType1',
            'StaticMemoryTransformValueType2']): Conversation memory configuration
        type (StaticMemoryTransformType):
    """

    value: Union[
        "StaticMemoryTransformValueType0", "StaticMemoryTransformValueType1", "StaticMemoryTransformValueType2"
    ]
    type: StaticMemoryTransformType
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.static_memory_transform_value_type_0 import StaticMemoryTransformValueType0
        from ..models.static_memory_transform_value_type_1 import StaticMemoryTransformValueType1

        value: Dict[str, Any]

        if isinstance(self.value, StaticMemoryTransformValueType0):
            value = self.value.to_dict()

        elif isinstance(self.value, StaticMemoryTransformValueType1):
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
        from ..models.static_memory_transform_value_type_0 import StaticMemoryTransformValueType0
        from ..models.static_memory_transform_value_type_1 import StaticMemoryTransformValueType1
        from ..models.static_memory_transform_value_type_2 import StaticMemoryTransformValueType2

        d = src_dict.copy()

        def _parse_value(
            data: object,
        ) -> Union[
            "StaticMemoryTransformValueType0", "StaticMemoryTransformValueType1", "StaticMemoryTransformValueType2"
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_0 = StaticMemoryTransformValueType0.from_dict(data)

                return value_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_1 = StaticMemoryTransformValueType1.from_dict(data)

                return value_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            value_type_2 = StaticMemoryTransformValueType2.from_dict(data)

            return value_type_2

        value = _parse_value(d.pop("value"))

        type = StaticMemoryTransformType(d.pop("type"))

        static_memory_transform = cls(
            value=value,
            type=type,
        )

        static_memory_transform.additional_properties = d
        return static_memory_transform

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
