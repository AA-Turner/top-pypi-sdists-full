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
    from ..models.string_to_value_label_map import StringToValueLabelMap


T = TypeVar("T", bound="GetPermissionsResponse200")


@attr.s(auto_attribs=True)
class GetPermissionsResponse200:
    """
    ### Attributes:
    * `status (Union[Unset, str])`: None
    * `data (Union[Unset, StringToValueLabelMap])`:
    """

    status: Union[Unset, str] = UNSET
    data: Union[Unset, "StringToValueLabelMap"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.string_to_value_label_map import StringToValueLabelMap

        status = self.status
        data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.string_to_value_label_map import StringToValueLabelMap

        d = src_dict.copy()
        status = d.pop("status", UNSET)

        _data = d.pop("data", UNSET)
        data: Union[Unset, StringToValueLabelMap]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = StringToValueLabelMap.from_dict(_data)

        get_permissions_response_200 = cls(
            status=status,
            data=data,
        )

        get_permissions_response_200.additional_properties = d
        return get_permissions_response_200

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
