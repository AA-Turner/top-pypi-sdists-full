from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.likert_scale_length_enum import LikertScaleLengthEnum
from ..models.question_type_enum import QuestionTypeEnum
from ..models.rich_text_toolbar_level_enum import RichTextToolbarLevelEnum

if TYPE_CHECKING:
    from ..models.answer import Answer
    from ..models.question_dependency_info import QuestionDependencyInfo
    from ..models.question_with_answer_allowed_file_types import QuestionWithAnswerAllowedFileTypes
    from ..models.question_with_answer_allowed_mime_types import QuestionWithAnswerAllowedMimeTypes


T = TypeVar("T", bound="QuestionWithAnswer")


@_attrs_define
class QuestionWithAnswer:
    """
    Attributes:
        uuid (UUID):
        description (str):
        user_guidance (Union[None, str]):
        question_type (QuestionTypeEnum):
        required (bool):
        order (int):
        existing_answer (Union['Answer', None]):
        question_options (Union[None, list[Any]]):
        min_value (Union[None, str]): Minimum value allowed for NUMBER, YEAR, and RATING type questions
        max_value (Union[None, str]): Maximum value allowed for NUMBER, YEAR, and RATING type questions
        allowed_file_types (QuestionWithAnswerAllowedFileTypes): List of allowed file extensions (e.g., ['.pdf', '.doc',
            '.docx']). If empty, all file types are allowed.
        allowed_mime_types (QuestionWithAnswerAllowedMimeTypes): List of allowed MIME types (e.g., ['application/pdf',
            'application/msword']). If empty, MIME type validation is not enforced. When both extensions and MIME types are
            specified, files must match both criteria for security.
        max_file_size_mb (Union[None, int]): Maximum file size in megabytes. If not set, no size limit is enforced.
        max_files_count (Union[None, int]): Maximum number of files allowed for MULTIPLE_FILES type questions. If not
            set, no count limit is enforced.
        likert_scale_length (Union[LikertScaleLengthEnum, None]): Number of points on the Likert scale (3, 5, or 7).
            Required for LIKERT type questions.
        likert_low_label (str): Label for the lowest point on the Likert scale (e.g. 'Strongly disagree'). Optional.
        likert_high_label (str): Label for the highest point on the Likert scale (e.g. 'Strongly agree'). Optional.
        likert_allow_na (bool): Allow respondents to choose 'N/A' as an answer for LIKERT type questions.
        rich_text_char_limit (Union[None, int]): Maximum number of characters allowed in RICH_TEXT type answers. If not
            set, no limit is enforced.
        rich_text_toolbar_level (RichTextToolbarLevelEnum):
        dependencies_info (Union['QuestionDependencyInfo', None]):
    """

    uuid: UUID
    description: str
    user_guidance: Union[None, str]
    question_type: QuestionTypeEnum
    required: bool
    order: int
    existing_answer: Union["Answer", None]
    question_options: Union[None, list[Any]]
    min_value: Union[None, str]
    max_value: Union[None, str]
    allowed_file_types: "QuestionWithAnswerAllowedFileTypes"
    allowed_mime_types: "QuestionWithAnswerAllowedMimeTypes"
    max_file_size_mb: Union[None, int]
    max_files_count: Union[None, int]
    likert_scale_length: Union[LikertScaleLengthEnum, None]
    likert_low_label: str
    likert_high_label: str
    likert_allow_na: bool
    rich_text_char_limit: Union[None, int]
    rich_text_toolbar_level: RichTextToolbarLevelEnum
    dependencies_info: Union["QuestionDependencyInfo", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.answer import Answer
        from ..models.question_dependency_info import QuestionDependencyInfo

        uuid = str(self.uuid)

        description = self.description

        user_guidance: Union[None, str]
        user_guidance = self.user_guidance

        question_type = self.question_type.value

        required = self.required

        order = self.order

        existing_answer: Union[None, dict[str, Any]]
        if isinstance(self.existing_answer, Answer):
            existing_answer = self.existing_answer.to_dict()
        else:
            existing_answer = self.existing_answer

        question_options: Union[None, list[Any]]
        if isinstance(self.question_options, list):
            question_options = self.question_options

        else:
            question_options = self.question_options

        min_value: Union[None, str]
        min_value = self.min_value

        max_value: Union[None, str]
        max_value = self.max_value

        allowed_file_types = self.allowed_file_types.to_dict()

        allowed_mime_types = self.allowed_mime_types.to_dict()

        max_file_size_mb: Union[None, int]
        max_file_size_mb = self.max_file_size_mb

        max_files_count: Union[None, int]
        max_files_count = self.max_files_count

        likert_scale_length: Union[None, int]
        if isinstance(self.likert_scale_length, LikertScaleLengthEnum):
            likert_scale_length = self.likert_scale_length.value
        else:
            likert_scale_length = self.likert_scale_length

        likert_low_label = self.likert_low_label

        likert_high_label = self.likert_high_label

        likert_allow_na = self.likert_allow_na

        rich_text_char_limit: Union[None, int]
        rich_text_char_limit = self.rich_text_char_limit

        rich_text_toolbar_level = self.rich_text_toolbar_level.value

        dependencies_info: Union[None, dict[str, Any]]
        if isinstance(self.dependencies_info, QuestionDependencyInfo):
            dependencies_info = self.dependencies_info.to_dict()
        else:
            dependencies_info = self.dependencies_info

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "description": description,
                "user_guidance": user_guidance,
                "question_type": question_type,
                "required": required,
                "order": order,
                "existing_answer": existing_answer,
                "question_options": question_options,
                "min_value": min_value,
                "max_value": max_value,
                "allowed_file_types": allowed_file_types,
                "allowed_mime_types": allowed_mime_types,
                "max_file_size_mb": max_file_size_mb,
                "max_files_count": max_files_count,
                "likert_scale_length": likert_scale_length,
                "likert_low_label": likert_low_label,
                "likert_high_label": likert_high_label,
                "likert_allow_na": likert_allow_na,
                "rich_text_char_limit": rich_text_char_limit,
                "rich_text_toolbar_level": rich_text_toolbar_level,
                "dependencies_info": dependencies_info,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.answer import Answer
        from ..models.question_dependency_info import QuestionDependencyInfo
        from ..models.question_with_answer_allowed_file_types import QuestionWithAnswerAllowedFileTypes
        from ..models.question_with_answer_allowed_mime_types import QuestionWithAnswerAllowedMimeTypes

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        description = d.pop("description")

        def _parse_user_guidance(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        user_guidance = _parse_user_guidance(d.pop("user_guidance"))

        question_type = QuestionTypeEnum(d.pop("question_type"))

        required = d.pop("required")

        order = d.pop("order")

        def _parse_existing_answer(data: object) -> Union["Answer", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                existing_answer_type_1 = Answer.from_dict(data)

                return existing_answer_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Answer", None], data)

        existing_answer = _parse_existing_answer(d.pop("existing_answer"))

        def _parse_question_options(data: object) -> Union[None, list[Any]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                question_options_type_0 = cast(list[Any], data)

                return question_options_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[Any]], data)

        question_options = _parse_question_options(d.pop("question_options"))

        def _parse_min_value(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        min_value = _parse_min_value(d.pop("min_value"))

        def _parse_max_value(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        max_value = _parse_max_value(d.pop("max_value"))

        allowed_file_types = QuestionWithAnswerAllowedFileTypes.from_dict(d.pop("allowed_file_types"))

        allowed_mime_types = QuestionWithAnswerAllowedMimeTypes.from_dict(d.pop("allowed_mime_types"))

        def _parse_max_file_size_mb(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_file_size_mb = _parse_max_file_size_mb(d.pop("max_file_size_mb"))

        def _parse_max_files_count(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_files_count = _parse_max_files_count(d.pop("max_files_count"))

        def _parse_likert_scale_length(data: object) -> Union[LikertScaleLengthEnum, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, int):
                    raise TypeError()
                likert_scale_length_type_0 = LikertScaleLengthEnum(data)

                return likert_scale_length_type_0
            except:  # noqa: E722
                pass
            return cast(Union[LikertScaleLengthEnum, None], data)

        likert_scale_length = _parse_likert_scale_length(d.pop("likert_scale_length"))

        likert_low_label = d.pop("likert_low_label")

        likert_high_label = d.pop("likert_high_label")

        likert_allow_na = d.pop("likert_allow_na")

        def _parse_rich_text_char_limit(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        rich_text_char_limit = _parse_rich_text_char_limit(d.pop("rich_text_char_limit"))

        rich_text_toolbar_level = RichTextToolbarLevelEnum(d.pop("rich_text_toolbar_level"))

        def _parse_dependencies_info(data: object) -> Union["QuestionDependencyInfo", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dependencies_info_type_1 = QuestionDependencyInfo.from_dict(data)

                return dependencies_info_type_1
            except:  # noqa: E722
                pass
            return cast(Union["QuestionDependencyInfo", None], data)

        dependencies_info = _parse_dependencies_info(d.pop("dependencies_info"))

        question_with_answer = cls(
            uuid=uuid,
            description=description,
            user_guidance=user_guidance,
            question_type=question_type,
            required=required,
            order=order,
            existing_answer=existing_answer,
            question_options=question_options,
            min_value=min_value,
            max_value=max_value,
            allowed_file_types=allowed_file_types,
            allowed_mime_types=allowed_mime_types,
            max_file_size_mb=max_file_size_mb,
            max_files_count=max_files_count,
            likert_scale_length=likert_scale_length,
            likert_low_label=likert_low_label,
            likert_high_label=likert_high_label,
            likert_allow_na=likert_allow_na,
            rich_text_char_limit=rich_text_char_limit,
            rich_text_toolbar_level=rich_text_toolbar_level,
            dependencies_info=dependencies_info,
        )

        question_with_answer.additional_properties = d
        return question_with_answer

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
