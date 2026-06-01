from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.remove_references_result_resource import RemoveReferencesResultResource


T = TypeVar("T", bound="RemoveReferencesResultEnvelope")


@_attrs_define
class RemoveReferencesResultEnvelope:
    """JSON:API single-resource response envelope for the
    remove-references action.

        Attributes:
            data (RemoveReferencesResultResource): JSON:API resource envelope for the remove-references result. Example:
                {'attributes': {'flags_modified': ['checkout-v2', 'banner-color'], 'rules_needing_manual_review':
                [{'environment': 'production', 'flag': 'pricing-tier', 'reason': 'Context reference inside an AND expression —
                removing would broaden the rule', 'rule_index': 2}], 'rules_removed': 3}, 'type': 'remove_references_result'}.
    """

    data: RemoveReferencesResultResource
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
        from ..models.remove_references_result_resource import RemoveReferencesResultResource

        d = dict(src_dict)
        data = RemoveReferencesResultResource.from_dict(d.pop("data"))

        remove_references_result_envelope = cls(
            data=data,
        )

        remove_references_result_envelope.additional_properties = d
        return remove_references_result_envelope

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
