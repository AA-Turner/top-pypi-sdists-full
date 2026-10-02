import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.technical_assessment_answer import TechnicalAssessmentAnswer


T = TypeVar("T", bound="StepChecklistResponseGroup")


@_attrs_define
class StepChecklistResponseGroup:
    """
    Attributes:
        user_uuid (Union[None, UUID]):
        user_full_name (Union[None, str]):
        user_image (Union[None, str]):
        submitted_at (Union[None, datetime.datetime]):
        answers (list['TechnicalAssessmentAnswer']):
    """

    user_uuid: Union[None, UUID]
    user_full_name: Union[None, str]
    user_image: Union[None, str]
    submitted_at: Union[None, datetime.datetime]
    answers: list["TechnicalAssessmentAnswer"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_uuid: Union[None, str]
        if isinstance(self.user_uuid, UUID):
            user_uuid = str(self.user_uuid)
        else:
            user_uuid = self.user_uuid

        user_full_name: Union[None, str]
        user_full_name = self.user_full_name

        user_image: Union[None, str]
        user_image = self.user_image

        submitted_at: Union[None, str]
        if isinstance(self.submitted_at, datetime.datetime):
            submitted_at = self.submitted_at.isoformat()
        else:
            submitted_at = self.submitted_at

        answers = []
        for answers_item_data in self.answers:
            answers_item = answers_item_data.to_dict()
            answers.append(answers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_uuid": user_uuid,
                "user_full_name": user_full_name,
                "user_image": user_image,
                "submitted_at": submitted_at,
                "answers": answers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.technical_assessment_answer import TechnicalAssessmentAnswer

        d = dict(src_dict)

        def _parse_user_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                user_uuid_type_0 = UUID(data)

                return user_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        user_uuid = _parse_user_uuid(d.pop("user_uuid"))

        def _parse_user_full_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        user_full_name = _parse_user_full_name(d.pop("user_full_name"))

        def _parse_user_image(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        user_image = _parse_user_image(d.pop("user_image"))

        def _parse_submitted_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                submitted_at_type_0 = isoparse(data)

                return submitted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        submitted_at = _parse_submitted_at(d.pop("submitted_at"))

        answers = []
        _answers = d.pop("answers")
        for answers_item_data in _answers:
            answers_item = TechnicalAssessmentAnswer.from_dict(answers_item_data)

            answers.append(answers_item)

        step_checklist_response_group = cls(
            user_uuid=user_uuid,
            user_full_name=user_full_name,
            user_image=user_image,
            submitted_at=submitted_at,
            answers=answers,
        )

        step_checklist_response_group.additional_properties = d
        return step_checklist_response_group

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
