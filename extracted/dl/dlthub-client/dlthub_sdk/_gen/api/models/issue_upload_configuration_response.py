from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="IssueUploadConfigurationResponse")


@_attrs_define
class IssueUploadConfigurationResponse:
    """
    Attributes:
        configuration_id (UUID): ID the uploaded configuration will be created under
        upload_token (str): DataplaneUserJwt to attach as Bearer on the upload POST
        upload_url (str): Absolute URL on the data plane where bytes must be posted
    """

    configuration_id: UUID
    upload_token: str
    upload_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        configuration_id = str(self.configuration_id)

        upload_token = self.upload_token

        upload_url = self.upload_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "configuration_id": configuration_id,
                "upload_token": upload_token,
                "upload_url": upload_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        configuration_id = UUID(d.pop("configuration_id"))

        upload_token = d.pop("upload_token")

        upload_url = d.pop("upload_url")

        issue_upload_configuration_response = cls(
            configuration_id=configuration_id,
            upload_token=upload_token,
            upload_url=upload_url,
        )

        issue_upload_configuration_response.additional_properties = d
        return issue_upload_configuration_response

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
