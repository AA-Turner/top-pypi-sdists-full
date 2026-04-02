from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mapping_request import MappingRequest


T = TypeVar("T", bound="MigrationDetailsRequest")


@_attrs_define
class MigrationDetailsRequest:
    """
    Attributes:
        mappings (MappingRequest):
        error_message (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
    """

    mappings: "MappingRequest"
    error_message: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mappings = self.mappings.to_dict()

        error_message = self.error_message

        error_traceback = self.error_traceback

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mappings": mappings,
            }
        )
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mapping_request import MappingRequest

        d = dict(src_dict)
        mappings = MappingRequest.from_dict(d.pop("mappings"))

        error_message = d.pop("error_message", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        migration_details_request = cls(
            mappings=mappings,
            error_message=error_message,
            error_traceback=error_traceback,
        )

        migration_details_request.additional_properties = d
        return migration_details_request

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
