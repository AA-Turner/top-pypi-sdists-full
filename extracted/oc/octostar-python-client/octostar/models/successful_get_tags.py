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

from typing import cast, List
from ..types import UNSET, Unset
from typing import Union
from typing import cast
from typing import Dict

if TYPE_CHECKING:
    from ..models.upsert_entity import UpsertEntity


T = TypeVar("T", bound="SuccessfulGetTags")


@attr.s(auto_attribs=True)
class SuccessfulGetTags:
    """
    ### Attributes:
    * `status (Union[Unset, str])`: None Example: success
    * `data (Union[Unset, List['UpsertEntity']])`: None
    """

    status: Union[Unset, str] = UNSET
    data: Union[Unset, List["UpsertEntity"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.upsert_entity import UpsertEntity

        status = self.status
        data: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()

                data.append(data_item)

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
        from ..models.upsert_entity import UpsertEntity

        d = src_dict.copy()
        status = d.pop("status", UNSET)

        data = []
        _data = d.pop("data", UNSET)
        for data_item_data in _data or []:
            data_item = UpsertEntity.from_dict(data_item_data)

            data.append(data_item)

        successful_get_tags = cls(
            status=status,
            data=data,
        )

        successful_get_tags.additional_properties = d
        return successful_get_tags

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
