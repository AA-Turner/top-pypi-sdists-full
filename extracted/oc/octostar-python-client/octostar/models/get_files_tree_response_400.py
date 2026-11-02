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

from ..models.get_files_tree_response_400_status import GetFilesTreeResponse400Status
from ..types import UNSET, Unset
from typing import Union
from typing import cast
from typing import Dict

if TYPE_CHECKING:
    from ..models.get_files_tree_response_400_data import GetFilesTreeResponse400Data


T = TypeVar("T", bound="GetFilesTreeResponse400")


@attr.s(auto_attribs=True)
class GetFilesTreeResponse400:
    """
    ### Attributes:
    * `status (Union[Unset, GetFilesTreeResponse400Status])`: None
    * `data (Union[Unset, GetFilesTreeResponse400Data])`:
    """

    status: Union[Unset, GetFilesTreeResponse400Status] = UNSET
    data: Union[Unset, "GetFilesTreeResponse400Data"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.get_files_tree_response_400_data import (
            GetFilesTreeResponse400Data,
        )

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

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
        from ..models.get_files_tree_response_400_data import (
            GetFilesTreeResponse400Data,
        )

        d = src_dict.copy()
        _status = d.pop("status", UNSET)
        status: Union[Unset, GetFilesTreeResponse400Status]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = GetFilesTreeResponse400Status(_status)

        _data = d.pop("data", UNSET)
        data: Union[Unset, GetFilesTreeResponse400Data]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = GetFilesTreeResponse400Data.from_dict(_data)

        get_files_tree_response_400 = cls(
            status=status,
            data=data,
        )

        get_files_tree_response_400.additional_properties = d
        return get_files_tree_response_400

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
