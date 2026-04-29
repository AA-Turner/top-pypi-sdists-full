from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TDeploymentFileItem")


@_attrs_define
class TDeploymentFileItem:
    """
    Attributes:
        relative_path (str):
        sha3_256 (str):
        size_in_bytes (int):
        linkname (Union[Unset, str]):
    """

    relative_path: str
    sha3_256: str
    size_in_bytes: int
    linkname: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        relative_path = self.relative_path

        sha3_256 = self.sha3_256

        size_in_bytes = self.size_in_bytes

        linkname = self.linkname

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "relative_path": relative_path,
                "sha3_256": sha3_256,
                "size_in_bytes": size_in_bytes,
            }
        )
        if linkname is not UNSET:
            field_dict["linkname"] = linkname

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        relative_path = d.pop("relative_path")

        sha3_256 = d.pop("sha3_256")

        size_in_bytes = d.pop("size_in_bytes")

        linkname = d.pop("linkname", UNSET)

        t_deployment_file_item = cls(
            relative_path=relative_path,
            sha3_256=sha3_256,
            size_in_bytes=size_in_bytes,
            linkname=linkname,
        )

        t_deployment_file_item.additional_properties = d
        return t_deployment_file_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
