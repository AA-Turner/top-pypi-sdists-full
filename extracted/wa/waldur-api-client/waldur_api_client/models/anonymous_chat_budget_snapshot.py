import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="AnonymousChatBudgetSnapshot")


@_attrs_define
class AnonymousChatBudgetSnapshot:
    """
    Attributes:
        tokens_today (int):
        tokens_limit (int):
        resets_at (datetime.datetime):
    """

    tokens_today: int
    tokens_limit: int
    resets_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tokens_today = self.tokens_today

        tokens_limit = self.tokens_limit

        resets_at = self.resets_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tokens_today": tokens_today,
                "tokens_limit": tokens_limit,
                "resets_at": resets_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tokens_today = d.pop("tokens_today")

        tokens_limit = d.pop("tokens_limit")

        resets_at = isoparse(d.pop("resets_at"))

        anonymous_chat_budget_snapshot = cls(
            tokens_today=tokens_today,
            tokens_limit=tokens_limit,
            resets_at=resets_at,
        )

        anonymous_chat_budget_snapshot.additional_properties = d
        return anonymous_chat_budget_snapshot

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
