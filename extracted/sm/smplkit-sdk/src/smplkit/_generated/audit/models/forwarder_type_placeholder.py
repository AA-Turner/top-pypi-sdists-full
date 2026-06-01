from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="ForwarderTypePlaceholder")


@_attrs_define
class ForwarderTypePlaceholder:
    """UI metadata for one ``{name}`` placeholder in the configuration.

    Attributes:
        label (str): Human-readable label for the input.
        secret (bool | Unset): If true, mask the value in the UI and treat as a credential. Default: False.
        enum (list[str] | None | Unset): If set, the value must be one of the listed strings — render as a dropdown.
        default (None | str | Unset): Pre-selected value when `enum` is set, or the default for a free-text field.
        placeholder (None | str | Unset): HTML-input hint text shown when the field is empty.
    """

    label: str
    secret: bool | Unset = False
    enum: list[str] | None | Unset = UNSET
    default: None | str | Unset = UNSET
    placeholder: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        secret = self.secret

        enum: list[str] | None | Unset
        if isinstance(self.enum, Unset):
            enum = UNSET
        elif isinstance(self.enum, list):
            enum = self.enum

        else:
            enum = self.enum

        default: None | str | Unset
        if isinstance(self.default, Unset):
            default = UNSET
        else:
            default = self.default

        placeholder: None | str | Unset
        if isinstance(self.placeholder, Unset):
            placeholder = UNSET
        else:
            placeholder = self.placeholder

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "label": label,
            }
        )
        if secret is not UNSET:
            field_dict["secret"] = secret
        if enum is not UNSET:
            field_dict["enum"] = enum
        if default is not UNSET:
            field_dict["default"] = default
        if placeholder is not UNSET:
            field_dict["placeholder"] = placeholder

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        secret = d.pop("secret", UNSET)

        def _parse_enum(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                enum_type_0 = cast(list[str], data)

                return enum_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        enum = _parse_enum(d.pop("enum", UNSET))

        def _parse_default(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        default = _parse_default(d.pop("default", UNSET))

        def _parse_placeholder(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        placeholder = _parse_placeholder(d.pop("placeholder", UNSET))

        forwarder_type_placeholder = cls(
            label=label,
            secret=secret,
            enum=enum,
            default=default,
            placeholder=placeholder,
        )

        return forwarder_type_placeholder
