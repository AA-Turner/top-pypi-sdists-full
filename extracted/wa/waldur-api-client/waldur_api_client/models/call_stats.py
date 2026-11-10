from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.call_stats_block import CallStatsBlock
    from ..models.call_stats_round import CallStatsRound


T = TypeVar("T", bound="CallStats")


@_attrs_define
class CallStats:
    """
    Attributes:
        call (CallStatsBlock):
        rounds (list['CallStatsRound']):
    """

    call: "CallStatsBlock"
    rounds: list["CallStatsRound"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        call = self.call.to_dict()

        rounds = []
        for rounds_item_data in self.rounds:
            rounds_item = rounds_item_data.to_dict()
            rounds.append(rounds_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "call": call,
                "rounds": rounds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.call_stats_block import CallStatsBlock
        from ..models.call_stats_round import CallStatsRound

        d = dict(src_dict)
        call = CallStatsBlock.from_dict(d.pop("call"))

        rounds = []
        _rounds = d.pop("rounds")
        for rounds_item_data in _rounds:
            rounds_item = CallStatsRound.from_dict(rounds_item_data)

            rounds.append(rounds_item)

        call_stats = cls(
            call=call,
            rounds=rounds,
        )

        call_stats.additional_properties = d
        return call_stats

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
