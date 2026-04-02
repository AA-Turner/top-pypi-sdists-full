from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.import_publications_source_enum import ImportPublicationsSourceEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ImportPublicationsRequest")


@_attrs_define
class ImportPublicationsRequest:
    """
    Attributes:
        source (Union[Unset, ImportPublicationsSourceEnum]):  Default: ImportPublicationsSourceEnum.ORCID.
        doi (Union[Unset, str]): DOI of publication to import (required if source is 'doi')
    """

    source: Union[Unset, ImportPublicationsSourceEnum] = ImportPublicationsSourceEnum.ORCID
    doi: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source: Union[Unset, str] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        doi = self.doi

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if source is not UNSET:
            field_dict["source"] = source
        if doi is not UNSET:
            field_dict["doi"] = doi

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _source = d.pop("source", UNSET)
        source: Union[Unset, ImportPublicationsSourceEnum]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = ImportPublicationsSourceEnum(_source)

        doi = d.pop("doi", UNSET)

        import_publications_request = cls(
            source=source,
            doi=doi,
        )

        import_publications_request.additional_properties = d
        return import_publications_request

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
