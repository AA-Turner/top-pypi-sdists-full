import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.project_answer_detail_answer_data_type_0 import ProjectAnswerDetailAnswerDataType0


T = TypeVar("T", bound="ProjectAnswerDetail")


@_attrs_define
class ProjectAnswerDetail:
    """
    Attributes:
        project_uuid (UUID):
        project_name (str):
        answer_uuid (Union[None, UUID]):
        answer_data (Union['ProjectAnswerDetailAnswerDataType0', None]):
        answered_by (Union[None, str]):
        answered_at (Union[None, datetime.datetime]): When the shown answer was last saved.
        requires_review (bool):
    """

    project_uuid: UUID
    project_name: str
    answer_uuid: Union[None, UUID]
    answer_data: Union["ProjectAnswerDetailAnswerDataType0", None]
    answered_by: Union[None, str]
    answered_at: Union[None, datetime.datetime]
    requires_review: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.project_answer_detail_answer_data_type_0 import ProjectAnswerDetailAnswerDataType0

        project_uuid = str(self.project_uuid)

        project_name = self.project_name

        answer_uuid: Union[None, str]
        if isinstance(self.answer_uuid, UUID):
            answer_uuid = str(self.answer_uuid)
        else:
            answer_uuid = self.answer_uuid

        answer_data: Union[None, dict[str, Any]]
        if isinstance(self.answer_data, ProjectAnswerDetailAnswerDataType0):
            answer_data = self.answer_data.to_dict()
        else:
            answer_data = self.answer_data

        answered_by: Union[None, str]
        answered_by = self.answered_by

        answered_at: Union[None, str]
        if isinstance(self.answered_at, datetime.datetime):
            answered_at = self.answered_at.isoformat()
        else:
            answered_at = self.answered_at

        requires_review = self.requires_review

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_uuid": project_uuid,
                "project_name": project_name,
                "answer_uuid": answer_uuid,
                "answer_data": answer_data,
                "answered_by": answered_by,
                "answered_at": answered_at,
                "requires_review": requires_review,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_answer_detail_answer_data_type_0 import ProjectAnswerDetailAnswerDataType0

        d = dict(src_dict)
        project_uuid = UUID(d.pop("project_uuid"))

        project_name = d.pop("project_name")

        def _parse_answer_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                answer_uuid_type_0 = UUID(data)

                return answer_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        answer_uuid = _parse_answer_uuid(d.pop("answer_uuid"))

        def _parse_answer_data(data: object) -> Union["ProjectAnswerDetailAnswerDataType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                answer_data_type_0 = ProjectAnswerDetailAnswerDataType0.from_dict(data)

                return answer_data_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ProjectAnswerDetailAnswerDataType0", None], data)

        answer_data = _parse_answer_data(d.pop("answer_data"))

        def _parse_answered_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        answered_by = _parse_answered_by(d.pop("answered_by"))

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

        requires_review = d.pop("requires_review")

        project_answer_detail = cls(
            project_uuid=project_uuid,
            project_name=project_name,
            answer_uuid=answer_uuid,
            answer_data=answer_data,
            answered_by=answered_by,
            answered_at=answered_at,
            requires_review=requires_review,
        )

        project_answer_detail.additional_properties = d
        return project_answer_detail

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
