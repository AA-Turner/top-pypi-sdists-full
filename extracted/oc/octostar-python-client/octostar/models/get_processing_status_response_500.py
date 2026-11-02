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
from ..types import UNSET, Unset


T = TypeVar("T", bound="GetProcessingStatusResponse500")


@attr.s(auto_attribs=True)
class GetProcessingStatusResponse500:
    """
    ### Attributes:
    * `status (Union[Unset, str])`: None Example: failure
    * `message (Union[Unset, str])`: None Example: Failed to retrieve processing status
    """

    status: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = d.pop("status", UNSET)

        message = d.pop("message", UNSET)

        get_processing_status_response_500 = cls(
            status=status,
            message=message,
        )

        get_processing_status_response_500.additional_properties = d
        return get_processing_status_response_500

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
