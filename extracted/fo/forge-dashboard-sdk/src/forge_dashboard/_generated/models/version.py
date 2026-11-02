from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="Version")



@_attrs_define
class Version:
    """ 
        Attributes:
            api_version (str): The API's current major version, such as v1: the path segment
                the versioned operations live under. It is one value, not a list.
            version (str): The release tag this binary was built from, with no leading
                "v" — or "dev" for a build outside the release pipeline.
     """

    api_version: str
    version: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        api_version = self.api_version

        version = self.version


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "apiVersion": api_version,
            "version": version,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        api_version = d.pop("apiVersion")

        version = d.pop("version")

        version = cls(
            api_version=api_version,
            version=version,
        )


        version.additional_properties = d
        return version

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
