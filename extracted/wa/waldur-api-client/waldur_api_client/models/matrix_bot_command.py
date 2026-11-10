from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MatrixBotCommand")


@_attrs_define
class MatrixBotCommand:
    """
    Attributes:
        name (str): As typed after `!`, e.g. `ticket send`.
        description (str):
        hint (str): Arguments: `[optional]`, `<required>`.
        available (bool):
        reason (str): Why the command is not available; blank if it is.
    """

    name: str
    description: str
    hint: str
    available: bool
    reason: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        hint = self.hint

        available = self.available

        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "hint": hint,
                "available": available,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        hint = d.pop("hint")

        available = d.pop("available")

        reason = d.pop("reason")

        matrix_bot_command = cls(
            name=name,
            description=description,
            hint=hint,
            available=available,
            reason=reason,
        )

        matrix_bot_command.additional_properties = d
        return matrix_bot_command

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
