from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CompleteRoundRefusal")


@_attrs_define
class CompleteRoundRefusal:
    """
    Attributes:
        detail (str):
        held_decisions_count (int): Decisions of the round whose release failed at publication and that were never
            announced. Present when completing is refused because of them; publish the results again to retry them.
        undecided_count (int): Proposals of the round without a decision. Present when completing is refused because of
            them under the refuse rule.
    """

    detail: str
    held_decisions_count: int
    undecided_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail = self.detail

        held_decisions_count = self.held_decisions_count

        undecided_count = self.undecided_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "detail": detail,
                "held_decisions_count": held_decisions_count,
                "undecided_count": undecided_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        detail = d.pop("detail")

        held_decisions_count = d.pop("held_decisions_count")

        undecided_count = d.pop("undecided_count")

        complete_round_refusal = cls(
            detail=detail,
            held_decisions_count=held_decisions_count,
            undecided_count=undecided_count,
        )

        complete_round_refusal.additional_properties = d
        return complete_round_refusal

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
