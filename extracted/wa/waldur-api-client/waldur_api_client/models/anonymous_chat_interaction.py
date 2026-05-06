import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.anonymous_chat_feedback import AnonymousChatFeedback


T = TypeVar("T", bound="AnonymousChatInteraction")


@_attrs_define
class AnonymousChatInteraction:
    """
    Attributes:
        uuid (UUID):
        user_slug (str):
        user_input (str):
        assistant_blocks (Any):
        offering_uuids (Any):
        result_count (int):
        is_flagged (bool):
        severity (str):
        injection_categories (Any):
        pii_categories (Any):
        action_taken (str):
        warning (str):
        ip_address (Union[None, str]): An IPv4 or IPv6 address.
        session_id (str):
        last_active_at (Union[None, datetime.datetime]):
        created (datetime.datetime):
        feedback (AnonymousChatFeedback):
    """

    uuid: UUID
    user_slug: str
    user_input: str
    assistant_blocks: Any
    offering_uuids: Any
    result_count: int
    is_flagged: bool
    severity: str
    injection_categories: Any
    pii_categories: Any
    action_taken: str
    warning: str
    ip_address: Union[None, str]
    session_id: str
    last_active_at: Union[None, datetime.datetime]
    created: datetime.datetime
    feedback: "AnonymousChatFeedback"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        user_slug = self.user_slug

        user_input = self.user_input

        assistant_blocks = self.assistant_blocks

        offering_uuids = self.offering_uuids

        result_count = self.result_count

        is_flagged = self.is_flagged

        severity = self.severity

        injection_categories = self.injection_categories

        pii_categories = self.pii_categories

        action_taken = self.action_taken

        warning = self.warning

        ip_address: Union[None, str]
        ip_address = self.ip_address

        session_id = self.session_id

        last_active_at: Union[None, str]
        if isinstance(self.last_active_at, datetime.datetime):
            last_active_at = self.last_active_at.isoformat()
        else:
            last_active_at = self.last_active_at

        created = self.created.isoformat()

        feedback = self.feedback.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "user_slug": user_slug,
                "user_input": user_input,
                "assistant_blocks": assistant_blocks,
                "offering_uuids": offering_uuids,
                "result_count": result_count,
                "is_flagged": is_flagged,
                "severity": severity,
                "injection_categories": injection_categories,
                "pii_categories": pii_categories,
                "action_taken": action_taken,
                "warning": warning,
                "ip_address": ip_address,
                "session_id": session_id,
                "last_active_at": last_active_at,
                "created": created,
                "feedback": feedback,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.anonymous_chat_feedback import AnonymousChatFeedback

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        user_slug = d.pop("user_slug")

        user_input = d.pop("user_input")

        assistant_blocks = d.pop("assistant_blocks")

        offering_uuids = d.pop("offering_uuids")

        result_count = d.pop("result_count")

        is_flagged = d.pop("is_flagged")

        severity = d.pop("severity")

        injection_categories = d.pop("injection_categories")

        pii_categories = d.pop("pii_categories")

        action_taken = d.pop("action_taken")

        warning = d.pop("warning")

        def _parse_ip_address(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        ip_address = _parse_ip_address(d.pop("ip_address"))

        session_id = d.pop("session_id")

        def _parse_last_active_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_active_at_type_0 = isoparse(data)

                return last_active_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_active_at = _parse_last_active_at(d.pop("last_active_at"))

        created = isoparse(d.pop("created"))

        feedback = AnonymousChatFeedback.from_dict(d.pop("feedback"))

        anonymous_chat_interaction = cls(
            uuid=uuid,
            user_slug=user_slug,
            user_input=user_input,
            assistant_blocks=assistant_blocks,
            offering_uuids=offering_uuids,
            result_count=result_count,
            is_flagged=is_flagged,
            severity=severity,
            injection_categories=injection_categories,
            pii_categories=pii_categories,
            action_taken=action_taken,
            warning=warning,
            ip_address=ip_address,
            session_id=session_id,
            last_active_at=last_active_at,
            created=created,
            feedback=feedback,
        )

        anonymous_chat_interaction.additional_properties = d
        return anonymous_chat_interaction

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
