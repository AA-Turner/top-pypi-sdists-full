import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.action_taken_enum import ActionTakenEnum
from ..models.feedback_category_enum import FeedbackCategoryEnum
from ..models.injection_severity_enum import InjectionSeverityEnum
from ..models.message_role_enum import MessageRoleEnum

if TYPE_CHECKING:
    from ..models.message_blocks_item import MessageBlocksItem


T = TypeVar("T", bound="Message")


@_attrs_define
class Message:
    """
    Attributes:
        uuid (UUID):
        thread (UUID):
        role (MessageRoleEnum):
        blocks (list['MessageBlocksItem']):
        warning (str):
        sequence_index (int):
        replaces (Union[None, UUID]):
        created (datetime.datetime):
        input_tokens (Union[None, int]):
        output_tokens (Union[None, int]):
        is_flagged (bool):
        severity (InjectionSeverityEnum):
        injection_categories (Any):
        pii_categories (Any):
        action_taken (ActionTakenEnum):
        feedback_score (Union[None, bool]): User feedback: True=thumbs up, False=thumbs down, None=no feedback.
        feedback_comment (Union[None, str]): Optional user comment accompanying feedback.
        feedback_category (Union[FeedbackCategoryEnum, None]): Category tag when feedback_score is False (thumbs down);
            null otherwise.
        feedback_submitted_at (Union[None, datetime.datetime]): Timestamp of the most recent feedback submission;
            overwritten on resubmit.
    """

    uuid: UUID
    thread: UUID
    role: MessageRoleEnum
    blocks: list["MessageBlocksItem"]
    warning: str
    sequence_index: int
    replaces: Union[None, UUID]
    created: datetime.datetime
    input_tokens: Union[None, int]
    output_tokens: Union[None, int]
    is_flagged: bool
    severity: InjectionSeverityEnum
    injection_categories: Any
    pii_categories: Any
    action_taken: ActionTakenEnum
    feedback_score: Union[None, bool]
    feedback_comment: Union[None, str]
    feedback_category: Union[FeedbackCategoryEnum, None]
    feedback_submitted_at: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        thread = str(self.thread)

        role = self.role.value

        blocks = []
        for blocks_item_data in self.blocks:
            blocks_item = blocks_item_data.to_dict()
            blocks.append(blocks_item)

        warning = self.warning

        sequence_index = self.sequence_index

        replaces: Union[None, str]
        if isinstance(self.replaces, UUID):
            replaces = str(self.replaces)
        else:
            replaces = self.replaces

        created = self.created.isoformat()

        input_tokens: Union[None, int]
        input_tokens = self.input_tokens

        output_tokens: Union[None, int]
        output_tokens = self.output_tokens

        is_flagged = self.is_flagged

        severity = self.severity.value

        injection_categories = self.injection_categories

        pii_categories = self.pii_categories

        action_taken = self.action_taken.value

        feedback_score: Union[None, bool]
        feedback_score = self.feedback_score

        feedback_comment: Union[None, str]
        feedback_comment = self.feedback_comment

        feedback_category: Union[None, str]
        if isinstance(self.feedback_category, FeedbackCategoryEnum):
            feedback_category = self.feedback_category.value
        else:
            feedback_category = self.feedback_category

        feedback_submitted_at: Union[None, str]
        if isinstance(self.feedback_submitted_at, datetime.datetime):
            feedback_submitted_at = self.feedback_submitted_at.isoformat()
        else:
            feedback_submitted_at = self.feedback_submitted_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "thread": thread,
                "role": role,
                "blocks": blocks,
                "warning": warning,
                "sequence_index": sequence_index,
                "replaces": replaces,
                "created": created,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "is_flagged": is_flagged,
                "severity": severity,
                "injection_categories": injection_categories,
                "pii_categories": pii_categories,
                "action_taken": action_taken,
                "feedback_score": feedback_score,
                "feedback_comment": feedback_comment,
                "feedback_category": feedback_category,
                "feedback_submitted_at": feedback_submitted_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.message_blocks_item import MessageBlocksItem

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        thread = UUID(d.pop("thread"))

        role = MessageRoleEnum(d.pop("role"))

        blocks = []
        _blocks = d.pop("blocks")
        for blocks_item_data in _blocks:
            blocks_item = MessageBlocksItem.from_dict(blocks_item_data)

            blocks.append(blocks_item)

        warning = d.pop("warning")

        sequence_index = d.pop("sequence_index")

        def _parse_replaces(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                replaces_type_0 = UUID(data)

                return replaces_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        replaces = _parse_replaces(d.pop("replaces"))

        created = isoparse(d.pop("created"))

        def _parse_input_tokens(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        input_tokens = _parse_input_tokens(d.pop("input_tokens"))

        def _parse_output_tokens(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        output_tokens = _parse_output_tokens(d.pop("output_tokens"))

        is_flagged = d.pop("is_flagged")

        severity = InjectionSeverityEnum(d.pop("severity"))

        injection_categories = d.pop("injection_categories")

        pii_categories = d.pop("pii_categories")

        action_taken = ActionTakenEnum(d.pop("action_taken"))

        def _parse_feedback_score(data: object) -> Union[None, bool]:
            if data is None:
                return data
            return cast(Union[None, bool], data)

        feedback_score = _parse_feedback_score(d.pop("feedback_score"))

        def _parse_feedback_comment(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        feedback_comment = _parse_feedback_comment(d.pop("feedback_comment"))

        def _parse_feedback_category(data: object) -> Union[FeedbackCategoryEnum, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                feedback_category_type_0 = FeedbackCategoryEnum(data)

                return feedback_category_type_0
            except:  # noqa: E722
                pass
            return cast(Union[FeedbackCategoryEnum, None], data)

        feedback_category = _parse_feedback_category(d.pop("feedback_category"))

        def _parse_feedback_submitted_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                feedback_submitted_at_type_0 = isoparse(data)

                return feedback_submitted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        feedback_submitted_at = _parse_feedback_submitted_at(d.pop("feedback_submitted_at"))

        message = cls(
            uuid=uuid,
            thread=thread,
            role=role,
            blocks=blocks,
            warning=warning,
            sequence_index=sequence_index,
            replaces=replaces,
            created=created,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            is_flagged=is_flagged,
            severity=severity,
            injection_categories=injection_categories,
            pii_categories=pii_categories,
            action_taken=action_taken,
            feedback_score=feedback_score,
            feedback_comment=feedback_comment,
            feedback_category=feedback_category,
            feedback_submitted_at=feedback_submitted_at,
        )

        message.additional_properties = d
        return message

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
