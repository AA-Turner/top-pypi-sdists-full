from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.token_saving_event import TokenSavingEvent
    from ..models.token_savings_summary import TokenSavingsSummary


T = TypeVar("T", bound="TokenSavingsList")


@_attrs_define
class TokenSavingsList:
    """
    Attributes:
        events (list[TokenSavingEvent]):
        summary (TokenSavingsSummary): Totals over everything the filter selects, not merely the page returned.
        next_page_token (None | str):
    """

    events: list[TokenSavingEvent]
    summary: TokenSavingsSummary
    next_page_token: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        events = []
        for events_item_data in self.events:
            events_item = events_item_data.to_dict()
            events.append(events_item)

        summary = self.summary.to_dict()

        next_page_token: None | str
        next_page_token = self.next_page_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "events": events,
                "summary": summary,
                "next_page_token": next_page_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.token_saving_event import TokenSavingEvent
        from ..models.token_savings_summary import TokenSavingsSummary

        d = dict(src_dict)
        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = TokenSavingEvent.from_dict(events_item_data)

            events.append(events_item)

        summary = TokenSavingsSummary.from_dict(d.pop("summary"))

        def _parse_next_page_token(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_page_token = _parse_next_page_token(d.pop("next_page_token"))

        token_savings_list = cls(
            events=events,
            summary=summary,
            next_page_token=next_page_token,
        )

        token_savings_list.additional_properties = d
        return token_savings_list

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
