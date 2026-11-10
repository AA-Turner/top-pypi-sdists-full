import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.feedback_state_enum import FeedbackStateEnum

if TYPE_CHECKING:
    from ..models.project_metadata_answer import ProjectMetadataAnswer


T = TypeVar("T", bound="FeedbackRequest")


@_attrs_define
class FeedbackRequest:
    """
    Attributes:
        uuid (UUID):
        created (datetime.datetime):
        survey_uuid (UUID):
        survey_name (str):
        user_uuid (UUID):
        user_full_name (str):
        user_username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_ characters
        user_email (str):
        organization_names (list[str]):
        state (FeedbackStateEnum):
        prompt_count (int):
        snoozed_until (Union[None, datetime.datetime]):
        answered_at (Union[None, datetime.datetime]):
        answers (list['ProjectMetadataAnswer']):
    """

    uuid: UUID
    created: datetime.datetime
    survey_uuid: UUID
    survey_name: str
    user_uuid: UUID
    user_full_name: str
    user_username: str
    user_email: str
    organization_names: list[str]
    state: FeedbackStateEnum
    prompt_count: int
    snoozed_until: Union[None, datetime.datetime]
    answered_at: Union[None, datetime.datetime]
    answers: list["ProjectMetadataAnswer"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        created = self.created.isoformat()

        survey_uuid = str(self.survey_uuid)

        survey_name = self.survey_name

        user_uuid = str(self.user_uuid)

        user_full_name = self.user_full_name

        user_username = self.user_username

        user_email = self.user_email

        organization_names = self.organization_names

        state = self.state.value

        prompt_count = self.prompt_count

        snoozed_until: Union[None, str]
        if isinstance(self.snoozed_until, datetime.datetime):
            snoozed_until = self.snoozed_until.isoformat()
        else:
            snoozed_until = self.snoozed_until

        answered_at: Union[None, str]
        if isinstance(self.answered_at, datetime.datetime):
            answered_at = self.answered_at.isoformat()
        else:
            answered_at = self.answered_at

        answers = []
        for answers_item_data in self.answers:
            answers_item = answers_item_data.to_dict()
            answers.append(answers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "created": created,
                "survey_uuid": survey_uuid,
                "survey_name": survey_name,
                "user_uuid": user_uuid,
                "user_full_name": user_full_name,
                "user_username": user_username,
                "user_email": user_email,
                "organization_names": organization_names,
                "state": state,
                "prompt_count": prompt_count,
                "snoozed_until": snoozed_until,
                "answered_at": answered_at,
                "answers": answers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_metadata_answer import ProjectMetadataAnswer

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        survey_uuid = UUID(d.pop("survey_uuid"))

        survey_name = d.pop("survey_name")

        user_uuid = UUID(d.pop("user_uuid"))

        user_full_name = d.pop("user_full_name")

        user_username = d.pop("user_username")

        user_email = d.pop("user_email")

        organization_names = cast(list[str], d.pop("organization_names"))

        state = FeedbackStateEnum(d.pop("state"))

        prompt_count = d.pop("prompt_count")

        def _parse_snoozed_until(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                snoozed_until_type_0 = isoparse(data)

                return snoozed_until_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        snoozed_until = _parse_snoozed_until(d.pop("snoozed_until"))

        def _parse_answered_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                answered_at_type_0 = isoparse(data)

                return answered_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        answered_at = _parse_answered_at(d.pop("answered_at"))

        answers = []
        _answers = d.pop("answers")
        for answers_item_data in _answers:
            answers_item = ProjectMetadataAnswer.from_dict(answers_item_data)

            answers.append(answers_item)

        feedback_request = cls(
            uuid=uuid,
            created=created,
            survey_uuid=survey_uuid,
            survey_name=survey_name,
            user_uuid=user_uuid,
            user_full_name=user_full_name,
            user_username=user_username,
            user_email=user_email,
            organization_names=organization_names,
            state=state,
            prompt_count=prompt_count,
            snoozed_until=snoozed_until,
            answered_at=answered_at,
            answers=answers,
        )

        feedback_request.additional_properties = d
        return feedback_request

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
