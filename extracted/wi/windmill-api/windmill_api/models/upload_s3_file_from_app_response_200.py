from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UploadS3FileFromAppResponse200")


@_attrs_define
class UploadS3FileFromAppResponse200:
    """
    Attributes:
        file_key (str):
        delete_token (str):
    """

    file_key: str
    delete_token: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_key = self.file_key
        delete_token = self.delete_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file_key": file_key,
                "delete_token": delete_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_key = d.pop("file_key")

        delete_token = d.pop("delete_token")

        upload_s3_file_from_app_response_200 = cls(
            file_key=file_key,
            delete_token=delete_token,
        )

        upload_s3_file_from_app_response_200.additional_properties = d
        return upload_s3_file_from_app_response_200

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
