from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, Unset

T = TypeVar("T", bound="CallAttachDocumentsRequest")


@_attrs_define
class CallAttachDocumentsRequest:
    """
    Attributes:
        documents (list[File]):
        description (Union[Unset, str]):
    """

    documents: list[File]
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        documents = []
        for documents_item_data in self.documents:
            documents_item = documents_item_data.to_tuple()

            documents.append(documents_item)

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "documents": documents,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        documents = []
        _documents = d.pop("documents")
        for documents_item_data in _documents:
            documents_item = File(payload=BytesIO(documents_item_data))

            documents.append(documents_item)

        description = d.pop("description", UNSET)

        call_attach_documents_request = cls(
            documents=documents,
            description=description,
        )

        call_attach_documents_request.additional_properties = d
        return call_attach_documents_request

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
