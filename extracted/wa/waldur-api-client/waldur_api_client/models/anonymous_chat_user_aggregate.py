import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="AnonymousChatUserAggregate")


@_attrs_define
class AnonymousChatUserAggregate:
    """
    Attributes:
        user_slug (str):
        last_seen (Union[None, datetime.datetime]):
        total_interactions (int):
        session_count (int):
        positive_feedback (int):
        negative_feedback (int):
        no_feedback (int):
        injection_strikes (int):
    """

    user_slug: str
    last_seen: Union[None, datetime.datetime]
    total_interactions: int
    session_count: int
    positive_feedback: int
    negative_feedback: int
    no_feedback: int
    injection_strikes: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_slug = self.user_slug

        last_seen: Union[None, str]
        if isinstance(self.last_seen, datetime.datetime):
            last_seen = self.last_seen.isoformat()
        else:
            last_seen = self.last_seen

        total_interactions = self.total_interactions

        session_count = self.session_count

        positive_feedback = self.positive_feedback

        negative_feedback = self.negative_feedback

        no_feedback = self.no_feedback

        injection_strikes = self.injection_strikes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_slug": user_slug,
                "last_seen": last_seen,
                "total_interactions": total_interactions,
                "session_count": session_count,
                "positive_feedback": positive_feedback,
                "negative_feedback": negative_feedback,
                "no_feedback": no_feedback,
                "injection_strikes": injection_strikes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_slug = d.pop("user_slug")

        def _parse_last_seen(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_seen_type_0 = isoparse(data)

                return last_seen_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_seen = _parse_last_seen(d.pop("last_seen"))

        total_interactions = d.pop("total_interactions")

        session_count = d.pop("session_count")

        positive_feedback = d.pop("positive_feedback")

        negative_feedback = d.pop("negative_feedback")

        no_feedback = d.pop("no_feedback")

        injection_strikes = d.pop("injection_strikes")

        anonymous_chat_user_aggregate = cls(
            user_slug=user_slug,
            last_seen=last_seen,
            total_interactions=total_interactions,
            session_count=session_count,
            positive_feedback=positive_feedback,
            negative_feedback=negative_feedback,
            no_feedback=no_feedback,
            injection_strikes=injection_strikes,
        )

        anonymous_chat_user_aggregate.additional_properties = d
        return anonymous_chat_user_aggregate

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
