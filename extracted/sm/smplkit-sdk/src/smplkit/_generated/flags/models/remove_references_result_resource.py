from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Literal

if TYPE_CHECKING:
    from ..models.remove_references_attributes import RemoveReferencesAttributes


T = TypeVar("T", bound="RemoveReferencesResultResource")


@_attrs_define
class RemoveReferencesResultResource:
    """JSON:API resource envelope for the remove-references result.

    Example:
        {'attributes': {'flags_modified': ['checkout-v2', 'banner-color'], 'rules_needing_manual_review':
            [{'environment': 'production', 'flag': 'pricing-tier', 'reason': 'Context reference inside an AND expression —
            removing would broaden the rule', 'rule_index': 2}], 'rules_removed': 3}, 'type': 'remove_references_result'}

    Attributes:
        attributes (RemoveReferencesAttributes): Counts and follow-ups returned by the remove-references action.
        type_ (Literal['remove_references_result'] | Unset):  Default: 'remove_references_result'.
    """

    attributes: RemoveReferencesAttributes
    type_: Literal["remove_references_result"] | Unset = "remove_references_result"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attributes = self.attributes.to_dict()

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attributes": attributes,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.remove_references_attributes import RemoveReferencesAttributes

        d = dict(src_dict)
        attributes = RemoveReferencesAttributes.from_dict(d.pop("attributes"))

        type_ = cast(Literal["remove_references_result"] | Unset, d.pop("type", UNSET))
        if type_ != "remove_references_result" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'remove_references_result', got '{type_}'")

        remove_references_result_resource = cls(
            attributes=attributes,
            type_=type_,
        )

        remove_references_result_resource.additional_properties = d
        return remove_references_result_resource

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
