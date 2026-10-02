from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="IngestRunConfigFileFromUrlDto")



@_attrs_define
class IngestRunConfigFileFromUrlDto:
    """ Input for ingesting a file from a remote https URL: the backend streams it into storage and returns the (unattached)
    file. The caller attaches it to a draft run-config version in a separate step.

        Attributes:
            url (str): Remote https URL the backend fetches and stores its own copy of.
            filename (str | Unset): Filename to store the fetched object as. Derived from the URL path when omitted.
     """

    url: str
    filename: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        url = self.url

        filename = self.filename


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "url": url,
        })
        if filename is not UNSET:
            field_dict["filename"] = filename

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        filename = d.pop("filename", UNSET)

        ingest_run_config_file_from_url_dto = cls(
            url=url,
            filename=filename,
        )


        ingest_run_config_file_from_url_dto.additional_properties = d
        return ingest_run_config_file_from_url_dto

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
