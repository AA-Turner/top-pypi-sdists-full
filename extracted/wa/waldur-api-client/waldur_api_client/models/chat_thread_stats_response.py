from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ChatThreadStatsResponse")


@_attrs_define
class ChatThreadStatsResponse:
    """
    Attributes:
        threads_total (int):
        sessions_total (int):
        users_total (int): Distinct owners of the threads in the filtered window.
        messages_total (int):
        input_tokens_total (int):
        output_tokens_total (int):
        total_tokens (int):
        flagged_total (int): Threads carrying at least one flagged message.
        feedback_positive (int):
        feedback_negative (int):
        satisfaction_rate (Union[None, float]): positive / (positive + negative); null when no human feedback.
    """

    threads_total: int
    sessions_total: int
    users_total: int
    messages_total: int
    input_tokens_total: int
    output_tokens_total: int
    total_tokens: int
    flagged_total: int
    feedback_positive: int
    feedback_negative: int
    satisfaction_rate: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        threads_total = self.threads_total

        sessions_total = self.sessions_total

        users_total = self.users_total

        messages_total = self.messages_total

        input_tokens_total = self.input_tokens_total

        output_tokens_total = self.output_tokens_total

        total_tokens = self.total_tokens

        flagged_total = self.flagged_total

        feedback_positive = self.feedback_positive

        feedback_negative = self.feedback_negative

        satisfaction_rate: Union[None, float]
        satisfaction_rate = self.satisfaction_rate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "threads_total": threads_total,
                "sessions_total": sessions_total,
                "users_total": users_total,
                "messages_total": messages_total,
                "input_tokens_total": input_tokens_total,
                "output_tokens_total": output_tokens_total,
                "total_tokens": total_tokens,
                "flagged_total": flagged_total,
                "feedback_positive": feedback_positive,
                "feedback_negative": feedback_negative,
                "satisfaction_rate": satisfaction_rate,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        threads_total = d.pop("threads_total")

        sessions_total = d.pop("sessions_total")

        users_total = d.pop("users_total")

        messages_total = d.pop("messages_total")

        input_tokens_total = d.pop("input_tokens_total")

        output_tokens_total = d.pop("output_tokens_total")

        total_tokens = d.pop("total_tokens")

        flagged_total = d.pop("flagged_total")

        feedback_positive = d.pop("feedback_positive")

        feedback_negative = d.pop("feedback_negative")

        def _parse_satisfaction_rate(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        satisfaction_rate = _parse_satisfaction_rate(d.pop("satisfaction_rate"))

        chat_thread_stats_response = cls(
            threads_total=threads_total,
            sessions_total=sessions_total,
            users_total=users_total,
            messages_total=messages_total,
            input_tokens_total=input_tokens_total,
            output_tokens_total=output_tokens_total,
            total_tokens=total_tokens,
            flagged_total=flagged_total,
            feedback_positive=feedback_positive,
            feedback_negative=feedback_negative,
            satisfaction_rate=satisfaction_rate,
        )

        chat_thread_stats_response.additional_properties = d
        return chat_thread_stats_response

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
