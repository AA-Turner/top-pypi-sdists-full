from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.context_value_resource_type import check_context_value_resource_type
from ..models.context_value_resource_type import ContextValueResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.context_value import ContextValue


T = TypeVar("T", bound="ContextValueResource")


@_attrs_define
class ContextValueResource:
    """JSON:API resource envelope for a distinct context-attribute value.

    `id` is the value itself.

        Example:
            {'attributes': {'value': 'Michael'}, 'id': 'Michael', 'type': 'context_value'}

        Attributes:
            type_ (ContextValueResourceType):
            attributes (ContextValue): A single distinct attribute value observed across context instances.

                Returned by `GET /api/v1/context_values` to power typeahead pickers in
                rule-building UIs. The set of values reflects what has been registered
                via the bulk-context endpoint — it is observational, not a customer-
                declared enumeration. Example: {'value': 'Michael'}.
            id (None | str | Unset):
    """

    type_: ContextValueResourceType
    attributes: ContextValue
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.context_value import ContextValue

        d = dict(src_dict)
        type_ = check_context_value_resource_type(d.pop("type"))

        attributes = ContextValue.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        context_value_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        context_value_resource.additional_properties = d
        return context_value_resource

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
