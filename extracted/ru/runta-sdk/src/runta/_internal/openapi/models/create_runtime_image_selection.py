from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateRuntimeImageSelection")


@_attrs_define
class CreateRuntimeImageSelection:
    """
    Attributes:
        id (str):
        model_provider_protocol (None | str | Unset):
        runtime_sign_in (bool | Unset):  Default: False.
        model_provider_base_url (None | str | Unset): HTTPS endpoint the agent is configured against. Omit to use the
            image's default. Only images advertising allow_custom_base_url accept another endpoint.
        model_provider_model (None | str | Unset): Model the agent is configured to use. Omit to use the image's
            default.
    """

    id: str
    model_provider_protocol: None | str | Unset = UNSET
    runtime_sign_in: bool | Unset = False
    model_provider_base_url: None | str | Unset = UNSET
    model_provider_model: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        model_provider_protocol: None | str | Unset
        if isinstance(self.model_provider_protocol, Unset):
            model_provider_protocol = UNSET
        else:
            model_provider_protocol = self.model_provider_protocol

        runtime_sign_in = self.runtime_sign_in

        model_provider_base_url: None | str | Unset
        if isinstance(self.model_provider_base_url, Unset):
            model_provider_base_url = UNSET
        else:
            model_provider_base_url = self.model_provider_base_url

        model_provider_model: None | str | Unset
        if isinstance(self.model_provider_model, Unset):
            model_provider_model = UNSET
        else:
            model_provider_model = self.model_provider_model

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
            }
        )
        if model_provider_protocol is not UNSET:
            field_dict["model_provider_protocol"] = model_provider_protocol
        if runtime_sign_in is not UNSET:
            field_dict["runtime_sign_in"] = runtime_sign_in
        if model_provider_base_url is not UNSET:
            field_dict["model_provider_base_url"] = model_provider_base_url
        if model_provider_model is not UNSET:
            field_dict["model_provider_model"] = model_provider_model

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_model_provider_protocol(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_provider_protocol = _parse_model_provider_protocol(
            d.pop("model_provider_protocol", UNSET)
        )

        runtime_sign_in = d.pop("runtime_sign_in", UNSET)

        def _parse_model_provider_base_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_provider_base_url = _parse_model_provider_base_url(
            d.pop("model_provider_base_url", UNSET)
        )

        def _parse_model_provider_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_provider_model = _parse_model_provider_model(
            d.pop("model_provider_model", UNSET)
        )

        create_runtime_image_selection = cls(
            id=id,
            model_provider_protocol=model_provider_protocol,
            runtime_sign_in=runtime_sign_in,
            model_provider_base_url=model_provider_base_url,
            model_provider_model=model_provider_model,
        )

        return create_runtime_image_selection
