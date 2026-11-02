from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="ManagedModelProvider")


@_attrs_define
class ManagedModelProvider:
    """
    Attributes:
        id (str):
        secret_id (str):
        display_name (str):
        protocol (str):
        base_url (str):
        default_model (None | str):
        header_name (str):
        value_template (str):
    """

    id: str
    secret_id: str
    display_name: str
    protocol: str
    base_url: str
    default_model: None | str
    header_name: str
    value_template: str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        secret_id = self.secret_id

        display_name = self.display_name

        protocol = self.protocol

        base_url = self.base_url

        default_model: None | str
        default_model = self.default_model

        header_name = self.header_name

        value_template = self.value_template

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "secret_id": secret_id,
                "display_name": display_name,
                "protocol": protocol,
                "base_url": base_url,
                "default_model": default_model,
                "header_name": header_name,
                "value_template": value_template,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        secret_id = d.pop("secret_id")

        display_name = d.pop("display_name")

        protocol = d.pop("protocol")

        base_url = d.pop("base_url")

        def _parse_default_model(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        default_model = _parse_default_model(d.pop("default_model"))

        header_name = d.pop("header_name")

        value_template = d.pop("value_template")

        managed_model_provider = cls(
            id=id,
            secret_id=secret_id,
            display_name=display_name,
            protocol=protocol,
            base_url=base_url,
            default_model=default_model,
            header_name=header_name,
            value_template=value_template,
        )

        return managed_model_provider
