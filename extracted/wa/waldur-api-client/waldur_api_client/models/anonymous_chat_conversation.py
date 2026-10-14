import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="AnonymousChatConversation")


@_attrs_define
class AnonymousChatConversation:
    """
    Attributes:
        session_id (str):
        user_slug (str):
        message_count (int):
        is_flagged (bool):
        max_severity (str):
        max_severity_rank (int): Numeric ordinal of max_severity (0=none … 4=critical) for severity-ordered sorting.
        has_feedback (bool):
        offerings_shown (int):
        offerings_clicked (int): Click-throughs on recommended offerings; repeat clicks count separately.
        models_used (str): Comma-separated distinct LLM models across the conversation. More than one when
            AI_ASSISTANT_MODEL was switched partway through; blank for conversations predating model tracking.
        is_reviewed (bool): True once the nightly LLM judge has scored this conversation. One verdict per conversation,
            recorded on its last turn; a conversation is never re-judged.
        input_tokens (int): Prompt tokens summed over the conversation; 0 for turns predating token tracking.
        output_tokens (int): Completion tokens summed over the conversation.
        total_tokens (int): input_tokens + output_tokens. Excludes LLM judge spend, which runs on its own budget.
        started (Union[None, datetime.datetime]):
        last_active (Union[None, datetime.datetime]):
    """

    session_id: str
    user_slug: str
    message_count: int
    is_flagged: bool
    max_severity: str
    max_severity_rank: int
    has_feedback: bool
    offerings_shown: int
    offerings_clicked: int
    models_used: str
    is_reviewed: bool
    input_tokens: int
    output_tokens: int
    total_tokens: int
    started: Union[None, datetime.datetime]
    last_active: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        session_id = self.session_id

        user_slug = self.user_slug

        message_count = self.message_count

        is_flagged = self.is_flagged

        max_severity = self.max_severity

        max_severity_rank = self.max_severity_rank

        has_feedback = self.has_feedback

        offerings_shown = self.offerings_shown

        offerings_clicked = self.offerings_clicked

        models_used = self.models_used

        is_reviewed = self.is_reviewed

        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        total_tokens = self.total_tokens

        started: Union[None, str]
        if isinstance(self.started, datetime.datetime):
            started = self.started.isoformat()
        else:
            started = self.started

        last_active: Union[None, str]
        if isinstance(self.last_active, datetime.datetime):
            last_active = self.last_active.isoformat()
        else:
            last_active = self.last_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "session_id": session_id,
                "user_slug": user_slug,
                "message_count": message_count,
                "is_flagged": is_flagged,
                "max_severity": max_severity,
                "max_severity_rank": max_severity_rank,
                "has_feedback": has_feedback,
                "offerings_shown": offerings_shown,
                "offerings_clicked": offerings_clicked,
                "models_used": models_used,
                "is_reviewed": is_reviewed,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "started": started,
                "last_active": last_active,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        session_id = d.pop("session_id")

        user_slug = d.pop("user_slug")

        message_count = d.pop("message_count")

        is_flagged = d.pop("is_flagged")

        max_severity = d.pop("max_severity")

        max_severity_rank = d.pop("max_severity_rank")

        has_feedback = d.pop("has_feedback")

        offerings_shown = d.pop("offerings_shown")

        offerings_clicked = d.pop("offerings_clicked")

        models_used = d.pop("models_used")

        is_reviewed = d.pop("is_reviewed")

        input_tokens = d.pop("input_tokens")

        output_tokens = d.pop("output_tokens")

        total_tokens = d.pop("total_tokens")

        def _parse_started(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_type_0 = isoparse(data)

                return started_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        started = _parse_started(d.pop("started"))

        def _parse_last_active(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_active_type_0 = isoparse(data)

                return last_active_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_active = _parse_last_active(d.pop("last_active"))

        anonymous_chat_conversation = cls(
            session_id=session_id,
            user_slug=user_slug,
            message_count=message_count,
            is_flagged=is_flagged,
            max_severity=max_severity,
            max_severity_rank=max_severity_rank,
            has_feedback=has_feedback,
            offerings_shown=offerings_shown,
            offerings_clicked=offerings_clicked,
            models_used=models_used,
            is_reviewed=is_reviewed,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            started=started,
            last_active=last_active,
        )

        anonymous_chat_conversation.additional_properties = d
        return anonymous_chat_conversation

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
