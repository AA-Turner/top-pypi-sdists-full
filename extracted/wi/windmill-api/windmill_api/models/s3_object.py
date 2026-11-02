from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="S3Object")


@_attrs_define
class S3Object:
    """
    Attributes:
        s3 (str):
        filename (Union[Unset, str]):
        storage (Union[Unset, str]):
        presigned (Union[Unset, str]):
    """

    s3: str
    filename: Union[Unset, str] = UNSET
    storage: Union[Unset, str] = UNSET
    presigned: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        s3 = self.s3
        filename = self.filename
        storage = self.storage
        presigned = self.presigned

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "s3": s3,
            }
        )
        if filename is not UNSET:
            field_dict["filename"] = filename
        if storage is not UNSET:
            field_dict["storage"] = storage
        if presigned is not UNSET:
            field_dict["presigned"] = presigned

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        s3 = d.pop("s3")

        filename = d.pop("filename", UNSET)

        storage = d.pop("storage", UNSET)

        presigned = d.pop("presigned", UNSET)

        s3_object = cls(
            s3=s3,
            filename=filename,
            storage=storage,
            presigned=presigned,
        )

        s3_object.additional_properties = d
        return s3_object

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
