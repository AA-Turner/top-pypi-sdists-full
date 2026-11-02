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


T = TypeVar("T", bound="SuccessfulInsertion")


@attr.s(auto_attribs=True)
class SuccessfulInsertion:
    """
    ### Attributes:
    * `status (Union[Unset, str])`: None Example: successful
    * `records_updated (Union[Unset, int])`: None
    * `records_created (Union[Unset, int])`: None
    * `relations_created (Union[Unset, int])`: None
    """

    status: Union[Unset, str] = UNSET
    records_updated: Union[Unset, int] = UNSET
    records_created: Union[Unset, int] = UNSET
    relations_created: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        records_updated = self.records_updated
        records_created = self.records_created
        relations_created = self.relations_created

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if records_updated is not UNSET:
            field_dict["records_updated"] = records_updated
        if records_created is not UNSET:
            field_dict["records_created"] = records_created
        if relations_created is not UNSET:
            field_dict["relations_created"] = relations_created

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = d.pop("status", UNSET)

        records_updated = d.pop("records_updated", UNSET)

        records_created = d.pop("records_created", UNSET)

        relations_created = d.pop("relations_created", UNSET)

        successful_insertion = cls(
            status=status,
            records_updated=records_updated,
            records_created=records_created,
            relations_created=relations_created,
        )

        successful_insertion.additional_properties = d
        return successful_insertion

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
