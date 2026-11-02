from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    Tuple,
    Optional,
    BinaryIO,
    TextIO,
    TYPE_CHECKING,
)

from typing import List


import attr

from ..types import UNSET, Unset

from typing import cast
from typing import Dict

if TYPE_CHECKING:
    from ..models.string_to_value_label_map_data_additional_property import (
        StringToValueLabelMapDataAdditionalProperty,
    )


T = TypeVar("T", bound="StringToValueLabelMapData")


@attr.s(auto_attribs=True)
class StringToValueLabelMapData:
    """ """

    additional_properties: Dict[str, "StringToValueLabelMapDataAdditionalProperty"] = (
        attr.ib(init=False, factory=dict)
    )

    def to_dict(self) -> Dict[str, Any]:
        from ..models.string_to_value_label_map_data_additional_property import (
            StringToValueLabelMapDataAdditionalProperty,
        )

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.string_to_value_label_map_data_additional_property import (
            StringToValueLabelMapDataAdditionalProperty,
        )

        d = src_dict.copy()
        string_to_value_label_map_data = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = StringToValueLabelMapDataAdditionalProperty.from_dict(
                prop_dict
            )

            additional_properties[prop_name] = additional_property

        string_to_value_label_map_data.additional_properties = additional_properties
        return string_to_value_label_map_data

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "StringToValueLabelMapDataAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(
        self, key: str, value: "StringToValueLabelMapDataAdditionalProperty"
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
