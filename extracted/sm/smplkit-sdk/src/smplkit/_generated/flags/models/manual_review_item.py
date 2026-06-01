from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="ManualReviewItem")


@_attrs_define
class ManualReviewItem:
    """A flag rule that could not be safely modified by the bulk
    remove-references action.

        Attributes:
            flag (str): Key of the flag containing the rule.
            environment (str): Environment containing the rule.
            rule_index (int): Position of the rule within the environment's `rules` array.
            reason (str): Why the rule needs manual review.
    """

    flag: str
    environment: str
    rule_index: int
    reason: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flag = self.flag

        environment = self.environment

        rule_index = self.rule_index

        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "flag": flag,
                "environment": environment,
                "rule_index": rule_index,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        flag = d.pop("flag")

        environment = d.pop("environment")

        rule_index = d.pop("rule_index")

        reason = d.pop("reason")

        manual_review_item = cls(
            flag=flag,
            environment=environment,
            rule_index=rule_index,
            reason=reason,
        )

        manual_review_item.additional_properties = d
        return manual_review_item

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
