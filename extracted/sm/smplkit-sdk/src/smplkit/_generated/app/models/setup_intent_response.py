from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.setup_intent_resource import SetupIntentResource


T = TypeVar("T", bound="SetupIntentResponse")


@_attrs_define
class SetupIntentResponse:
    """JSON:API single-resource response envelope for a setup-intent result.

    Attributes:
        data (SetupIntentResource):  Example: {'attributes': {'client_secret': 'seti_1234567890abcdef_secret_xyz'},
            'type': 'setup_intent'}.
    """

    data: SetupIntentResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.setup_intent_resource import SetupIntentResource

        d = dict(src_dict)
        data = SetupIntentResource.from_dict(d.pop("data"))

        setup_intent_response = cls(
            data=data,
        )

        setup_intent_response.additional_properties = d
        return setup_intent_response

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
