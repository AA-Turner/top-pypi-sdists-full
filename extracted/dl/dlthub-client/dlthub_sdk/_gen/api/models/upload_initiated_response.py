from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UploadInitiatedResponse")


@_attrs_define
class UploadInitiatedResponse:
    """
    Attributes:
        upload_token (str): DataplaneUserJwt to attach as Bearer on the upload POST
        upload_url (str): Absolute URL on the data plane where bytes must be posted
        configuration_id (None | Unset | UUID): ID of the freshly-created configuration row (configuration flow)
        deployment_id (None | Unset | UUID): ID of the freshly-created deployment row (deployment flow)
    """

    upload_token: str
    upload_url: str
    configuration_id: None | Unset | UUID = UNSET
    deployment_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        upload_token = self.upload_token

        upload_url = self.upload_url

        configuration_id: None | str | Unset
        if isinstance(self.configuration_id, Unset):
            configuration_id = UNSET
        elif isinstance(self.configuration_id, UUID):
            configuration_id = str(self.configuration_id)
        else:
            configuration_id = self.configuration_id

        deployment_id: None | str | Unset
        if isinstance(self.deployment_id, Unset):
            deployment_id = UNSET
        elif isinstance(self.deployment_id, UUID):
            deployment_id = str(self.deployment_id)
        else:
            deployment_id = self.deployment_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "upload_token": upload_token,
                "upload_url": upload_url,
            }
        )
        if configuration_id is not UNSET:
            field_dict["configuration_id"] = configuration_id
        if deployment_id is not UNSET:
            field_dict["deployment_id"] = deployment_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        upload_token = d.pop("upload_token")

        upload_url = d.pop("upload_url")

        def _parse_configuration_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                configuration_id_type_0 = UUID(data)

                return configuration_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        configuration_id = _parse_configuration_id(d.pop("configuration_id", UNSET))

        def _parse_deployment_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deployment_id_type_0 = UUID(data)

                return deployment_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        deployment_id = _parse_deployment_id(d.pop("deployment_id", UNSET))

        upload_initiated_response = cls(
            upload_token=upload_token,
            upload_url=upload_url,
            configuration_id=configuration_id,
            deployment_id=deployment_id,
        )

        upload_initiated_response.additional_properties = d
        return upload_initiated_response

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
