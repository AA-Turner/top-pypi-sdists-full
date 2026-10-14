import datetime
from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="RoundAdoptionRequest")


@_attrs_define
class RoundAdoptionRequest:
    """
    Attributes:
        adopted_at (Union[None, datetime.date]): When the round's results were adopted.
        adoption_note (Union[Unset, str]):
        adoption_document (Union[File, None, Unset]):
    """

    adopted_at: Union[None, datetime.date]
    adoption_note: Union[Unset, str] = UNSET
    adoption_document: Union[File, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        adopted_at: Union[None, str]
        if isinstance(self.adopted_at, datetime.date):
            adopted_at = self.adopted_at.isoformat()
        else:
            adopted_at = self.adopted_at

        adoption_note = self.adoption_note

        adoption_document: Union[None, Unset, types.FileTypes]
        if isinstance(self.adoption_document, Unset):
            adoption_document = UNSET
        elif isinstance(self.adoption_document, File):
            adoption_document = self.adoption_document.to_tuple()

        else:
            adoption_document = self.adoption_document

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "adopted_at": adopted_at,
            }
        )
        if adoption_note is not UNSET:
            field_dict["adoption_note"] = adoption_note
        if adoption_document is not UNSET:
            field_dict["adoption_document"] = adoption_document

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        if isinstance(self.adopted_at, datetime.date):
            files.append(("adopted_at", (None, self.adopted_at.isoformat().encode(), "text/plain")))
        else:
            files.append(("adopted_at", (None, str(self.adopted_at).encode(), "text/plain")))

        if not isinstance(self.adoption_note, Unset):
            files.append(("adoption_note", (None, str(self.adoption_note).encode(), "text/plain")))

        if not isinstance(self.adoption_document, Unset):
            if isinstance(self.adoption_document, File):
                files.append(("adoption_document", self.adoption_document.to_tuple()))
            else:
                files.append(("adoption_document", (None, str(self.adoption_document).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_adopted_at(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                adopted_at_type_0 = isoparse(data).date()

                return adopted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        adopted_at = _parse_adopted_at(d.pop("adopted_at"))

        adoption_note = d.pop("adoption_note", UNSET)

        def _parse_adoption_document(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                adoption_document_type_0 = File(payload=BytesIO(data))

                return adoption_document_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        adoption_document = _parse_adoption_document(d.pop("adoption_document", UNSET))

        round_adoption_request = cls(
            adopted_at=adopted_at,
            adoption_note=adoption_note,
            adoption_document=adoption_document,
        )

        round_adoption_request.additional_properties = d
        return round_adoption_request

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
