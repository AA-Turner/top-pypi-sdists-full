from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.instance_set_metadata_request_metadata import InstanceSetMetadataRequestMetadata


T = TypeVar("T", bound="InstanceSetMetadataRequest")


@_attrs_define
class InstanceSetMetadataRequest:
    """
    Attributes:
        metadata (InstanceSetMetadataRequestMetadata): Nova instance metadata as string-to-string pairs. At most 128
            entries; keys and values up to 255 characters.
    """

    metadata: "InstanceSetMetadataRequestMetadata"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.instance_set_metadata_request_metadata import InstanceSetMetadataRequestMetadata

        d = dict(src_dict)
        metadata = InstanceSetMetadataRequestMetadata.from_dict(d.pop("metadata"))

        instance_set_metadata_request = cls(
            metadata=metadata,
        )

        instance_set_metadata_request.additional_properties = d
        return instance_set_metadata_request

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
