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

from typing import Union
from typing import cast
from typing import Dict
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.string_to_value_label_map_data import StringToValueLabelMapData


T = TypeVar("T", bound="StringToValueLabelMap")


@attr.s(auto_attribs=True)
class StringToValueLabelMap:
    """
    ### Attributes:
    * `data (Union[Unset, StringToValueLabelMapData])`:
    * `status (Union[Unset, str])`: None
    """

    data: Union[Unset, "StringToValueLabelMapData"] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.string_to_value_label_map_data import StringToValueLabelMapData

        data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.string_to_value_label_map_data import StringToValueLabelMapData

        d = src_dict.copy()
        _data = d.pop("data", UNSET)
        data: Union[Unset, StringToValueLabelMapData]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = StringToValueLabelMapData.from_dict(_data)

        status = d.pop("status", UNSET)

        string_to_value_label_map = cls(
            data=data,
            status=status,
        )

        string_to_value_label_map.additional_properties = d
        return string_to_value_label_map

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
