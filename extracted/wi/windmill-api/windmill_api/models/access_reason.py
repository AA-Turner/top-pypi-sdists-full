from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.access_reason_type import AccessReasonType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AccessReason")


@_attrs_define
class AccessReason:
    """
    Attributes:
        type (AccessReasonType):
        group (Union[Unset, str]):
        folder (Union[Unset, str]):
        write (Union[Unset, bool]):
    """

    type: AccessReasonType
    group: Union[Unset, str] = UNSET
    folder: Union[Unset, str] = UNSET
    write: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        group = self.group
        folder = self.folder
        write = self.write

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if group is not UNSET:
            field_dict["group"] = group
        if folder is not UNSET:
            field_dict["folder"] = folder
        if write is not UNSET:
            field_dict["write"] = write

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = AccessReasonType(d.pop("type"))

        group = d.pop("group", UNSET)

        folder = d.pop("folder", UNSET)

        write = d.pop("write", UNSET)

        access_reason = cls(
            type=type,
            group=group,
            folder=folder,
            write=write,
        )

        access_reason.additional_properties = d
        return access_reason

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
