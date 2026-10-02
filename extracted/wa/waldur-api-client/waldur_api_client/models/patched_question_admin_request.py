from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blank_enum import BlankEnum
from ..models.checklist_operators import ChecklistOperators
from ..models.dependency_logic_operator_enum import DependencyLogicOperatorEnum
from ..models.likert_scale_length_enum import LikertScaleLengthEnum
from ..models.question_type_enum import QuestionTypeEnum
from ..models.rich_text_toolbar_level_enum import RichTextToolbarLevelEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patched_question_admin_request_guidance_answer_value_type_0 import (
        PatchedQuestionAdminRequestGuidanceAnswerValueType0,
    )


T = TypeVar("T", bound="PatchedQuestionAdminRequest")


@_attrs_define
class PatchedQuestionAdminRequest:
    """
    Attributes:
        required (Union[Unset, bool]):
        description (Union[Unset, str]):
        user_guidance (Union[Unset, str]): Additional guidance text visible to users when answering and reviewing
        question_type (Union[Unset, QuestionTypeEnum]):
        order (Union[Unset, int]):
        min_value (Union[None, Unset, str]): Minimum value allowed for NUMBER, YEAR, and RATING type questions
        max_value (Union[None, Unset, str]): Maximum value allowed for NUMBER, YEAR, and RATING type questions
        allowed_file_types (Union[Unset, list[str]]):
        allowed_mime_types (Union[Unset, list[str]]):
        max_file_size_mb (Union[None, Unset, int]): Maximum file size in megabytes. If not set, no size limit is
            enforced.
        max_files_count (Union[None, Unset, int]): Maximum number of files allowed for MULTIPLE_FILES type questions. If
            not set, no count limit is enforced.
        likert_scale_length (Union[LikertScaleLengthEnum, None, Unset]): Number of points on the Likert scale (3, 5, or
            7). Required for LIKERT type questions.
        likert_low_label (Union[Unset, str]): Label for the lowest point on the Likert scale (e.g. 'Strongly disagree').
            Optional.
        likert_high_label (Union[Unset, str]): Label for the highest point on the Likert scale (e.g. 'Strongly agree').
            Optional.
        likert_allow_na (Union[Unset, bool]): Allow respondents to choose 'N/A' as an answer for LIKERT type questions.
        rich_text_char_limit (Union[None, Unset, int]): Maximum number of characters allowed in RICH_TEXT type answers.
            If not set, no limit is enforced.
        rich_text_toolbar_level (Union[BlankEnum, RichTextToolbarLevelEnum, Unset]): Toolbar level for the rich text
            editor: 'minimal', 'standard', or 'extended'.
        operator (Union[BlankEnum, ChecklistOperators, Unset]):
        review_answer_value (Union[Unset, Any]):
        always_requires_review (Union[Unset, bool]): This question always requires review regardless of answer
        guidance_answer_value (Union['PatchedQuestionAdminRequestGuidanceAnswerValueType0', None, Unset]): Answer value
            that triggers display of user guidance.
        guidance_operator (Union[BlankEnum, ChecklistOperators, Unset]): Operator to use when comparing answer with
            guidance_answer_value
        always_show_guidance (Union[Unset, bool]): Show user guidance always, regardless of answer. If False, guidance
            is conditional on answer matching guidance_answer_value with guidance_operator
        dependency_logic_operator (Union[Unset, DependencyLogicOperatorEnum]):
        checklist (Union[Unset, str]):
    """

    required: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    user_guidance: Union[Unset, str] = UNSET
    question_type: Union[Unset, QuestionTypeEnum] = UNSET
    order: Union[Unset, int] = UNSET
    min_value: Union[None, Unset, str] = UNSET
    max_value: Union[None, Unset, str] = UNSET
    allowed_file_types: Union[Unset, list[str]] = UNSET
    allowed_mime_types: Union[Unset, list[str]] = UNSET
    max_file_size_mb: Union[None, Unset, int] = UNSET
    max_files_count: Union[None, Unset, int] = UNSET
    likert_scale_length: Union[LikertScaleLengthEnum, None, Unset] = UNSET
    likert_low_label: Union[Unset, str] = UNSET
    likert_high_label: Union[Unset, str] = UNSET
    likert_allow_na: Union[Unset, bool] = UNSET
    rich_text_char_limit: Union[None, Unset, int] = UNSET
    rich_text_toolbar_level: Union[BlankEnum, RichTextToolbarLevelEnum, Unset] = UNSET
    operator: Union[BlankEnum, ChecklistOperators, Unset] = UNSET
    review_answer_value: Union[Unset, Any] = UNSET
    always_requires_review: Union[Unset, bool] = UNSET
    guidance_answer_value: Union["PatchedQuestionAdminRequestGuidanceAnswerValueType0", None, Unset] = UNSET
    guidance_operator: Union[BlankEnum, ChecklistOperators, Unset] = UNSET
    always_show_guidance: Union[Unset, bool] = UNSET
    dependency_logic_operator: Union[Unset, DependencyLogicOperatorEnum] = UNSET
    checklist: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.patched_question_admin_request_guidance_answer_value_type_0 import (
            PatchedQuestionAdminRequestGuidanceAnswerValueType0,
        )

        required = self.required

        description = self.description

        user_guidance = self.user_guidance

        question_type: Union[Unset, str] = UNSET
        if not isinstance(self.question_type, Unset):
            question_type = self.question_type.value

        order = self.order

        min_value: Union[None, Unset, str]
        if isinstance(self.min_value, Unset):
            min_value = UNSET
        else:
            min_value = self.min_value

        max_value: Union[None, Unset, str]
        if isinstance(self.max_value, Unset):
            max_value = UNSET
        else:
            max_value = self.max_value

        allowed_file_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_file_types, Unset):
            allowed_file_types = self.allowed_file_types

        allowed_mime_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_mime_types, Unset):
            allowed_mime_types = self.allowed_mime_types

        max_file_size_mb: Union[None, Unset, int]
        if isinstance(self.max_file_size_mb, Unset):
            max_file_size_mb = UNSET
        else:
            max_file_size_mb = self.max_file_size_mb

        max_files_count: Union[None, Unset, int]
        if isinstance(self.max_files_count, Unset):
            max_files_count = UNSET
        else:
            max_files_count = self.max_files_count

        likert_scale_length: Union[None, Unset, int]
        if isinstance(self.likert_scale_length, Unset):
            likert_scale_length = UNSET
        elif isinstance(self.likert_scale_length, LikertScaleLengthEnum):
            likert_scale_length = self.likert_scale_length.value
        else:
            likert_scale_length = self.likert_scale_length

        likert_low_label = self.likert_low_label

        likert_high_label = self.likert_high_label

        likert_allow_na = self.likert_allow_na

        rich_text_char_limit: Union[None, Unset, int]
        if isinstance(self.rich_text_char_limit, Unset):
            rich_text_char_limit = UNSET
        else:
            rich_text_char_limit = self.rich_text_char_limit

        rich_text_toolbar_level: Union[Unset, str]
        if isinstance(self.rich_text_toolbar_level, Unset):
            rich_text_toolbar_level = UNSET
        elif isinstance(self.rich_text_toolbar_level, RichTextToolbarLevelEnum):
            rich_text_toolbar_level = self.rich_text_toolbar_level.value
        else:
            rich_text_toolbar_level = self.rich_text_toolbar_level.value

        operator: Union[Unset, str]
        if isinstance(self.operator, Unset):
            operator = UNSET
        elif isinstance(self.operator, ChecklistOperators):
            operator = self.operator.value
        else:
            operator = self.operator.value

        review_answer_value = self.review_answer_value

        always_requires_review = self.always_requires_review

        guidance_answer_value: Union[None, Unset, dict[str, Any]]
        if isinstance(self.guidance_answer_value, Unset):
            guidance_answer_value = UNSET
        elif isinstance(self.guidance_answer_value, PatchedQuestionAdminRequestGuidanceAnswerValueType0):
            guidance_answer_value = self.guidance_answer_value.to_dict()
        else:
            guidance_answer_value = self.guidance_answer_value

        guidance_operator: Union[Unset, str]
        if isinstance(self.guidance_operator, Unset):
            guidance_operator = UNSET
        elif isinstance(self.guidance_operator, ChecklistOperators):
            guidance_operator = self.guidance_operator.value
        else:
            guidance_operator = self.guidance_operator.value

        always_show_guidance = self.always_show_guidance

        dependency_logic_operator: Union[Unset, str] = UNSET
        if not isinstance(self.dependency_logic_operator, Unset):
            dependency_logic_operator = self.dependency_logic_operator.value

        checklist = self.checklist

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if required is not UNSET:
            field_dict["required"] = required
        if description is not UNSET:
            field_dict["description"] = description
        if user_guidance is not UNSET:
            field_dict["user_guidance"] = user_guidance
        if question_type is not UNSET:
            field_dict["question_type"] = question_type
        if order is not UNSET:
            field_dict["order"] = order
        if min_value is not UNSET:
            field_dict["min_value"] = min_value
        if max_value is not UNSET:
            field_dict["max_value"] = max_value
        if allowed_file_types is not UNSET:
            field_dict["allowed_file_types"] = allowed_file_types
        if allowed_mime_types is not UNSET:
            field_dict["allowed_mime_types"] = allowed_mime_types
        if max_file_size_mb is not UNSET:
            field_dict["max_file_size_mb"] = max_file_size_mb
        if max_files_count is not UNSET:
            field_dict["max_files_count"] = max_files_count
        if likert_scale_length is not UNSET:
            field_dict["likert_scale_length"] = likert_scale_length
        if likert_low_label is not UNSET:
            field_dict["likert_low_label"] = likert_low_label
        if likert_high_label is not UNSET:
            field_dict["likert_high_label"] = likert_high_label
        if likert_allow_na is not UNSET:
            field_dict["likert_allow_na"] = likert_allow_na
        if rich_text_char_limit is not UNSET:
            field_dict["rich_text_char_limit"] = rich_text_char_limit
        if rich_text_toolbar_level is not UNSET:
            field_dict["rich_text_toolbar_level"] = rich_text_toolbar_level
        if operator is not UNSET:
            field_dict["operator"] = operator
        if review_answer_value is not UNSET:
            field_dict["review_answer_value"] = review_answer_value
        if always_requires_review is not UNSET:
            field_dict["always_requires_review"] = always_requires_review
        if guidance_answer_value is not UNSET:
            field_dict["guidance_answer_value"] = guidance_answer_value
        if guidance_operator is not UNSET:
            field_dict["guidance_operator"] = guidance_operator
        if always_show_guidance is not UNSET:
            field_dict["always_show_guidance"] = always_show_guidance
        if dependency_logic_operator is not UNSET:
            field_dict["dependency_logic_operator"] = dependency_logic_operator
        if checklist is not UNSET:
            field_dict["checklist"] = checklist

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.patched_question_admin_request_guidance_answer_value_type_0 import (
            PatchedQuestionAdminRequestGuidanceAnswerValueType0,
        )

        d = dict(src_dict)
        required = d.pop("required", UNSET)

        description = d.pop("description", UNSET)

        user_guidance = d.pop("user_guidance", UNSET)

        _question_type = d.pop("question_type", UNSET)
        question_type: Union[Unset, QuestionTypeEnum]
        if isinstance(_question_type, Unset):
            question_type = UNSET
        else:
            question_type = QuestionTypeEnum(_question_type)

        order = d.pop("order", UNSET)

        def _parse_min_value(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        min_value = _parse_min_value(d.pop("min_value", UNSET))

        def _parse_max_value(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        max_value = _parse_max_value(d.pop("max_value", UNSET))

        allowed_file_types = cast(list[str], d.pop("allowed_file_types", UNSET))

        allowed_mime_types = cast(list[str], d.pop("allowed_mime_types", UNSET))

        def _parse_max_file_size_mb(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_file_size_mb = _parse_max_file_size_mb(d.pop("max_file_size_mb", UNSET))

        def _parse_max_files_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_files_count = _parse_max_files_count(d.pop("max_files_count", UNSET))

        def _parse_likert_scale_length(data: object) -> Union[LikertScaleLengthEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, int):
                    raise TypeError()
                likert_scale_length_type_0 = LikertScaleLengthEnum(data)

                return likert_scale_length_type_0
            except:  # noqa: E722
                pass
            return cast(Union[LikertScaleLengthEnum, None, Unset], data)

        likert_scale_length = _parse_likert_scale_length(d.pop("likert_scale_length", UNSET))

        likert_low_label = d.pop("likert_low_label", UNSET)

        likert_high_label = d.pop("likert_high_label", UNSET)

        likert_allow_na = d.pop("likert_allow_na", UNSET)

        def _parse_rich_text_char_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        rich_text_char_limit = _parse_rich_text_char_limit(d.pop("rich_text_char_limit", UNSET))

        def _parse_rich_text_toolbar_level(data: object) -> Union[BlankEnum, RichTextToolbarLevelEnum, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                rich_text_toolbar_level_type_0 = RichTextToolbarLevelEnum(data)

                return rich_text_toolbar_level_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            rich_text_toolbar_level_type_1 = BlankEnum(data)

            return rich_text_toolbar_level_type_1

        rich_text_toolbar_level = _parse_rich_text_toolbar_level(d.pop("rich_text_toolbar_level", UNSET))

        def _parse_operator(data: object) -> Union[BlankEnum, ChecklistOperators, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                operator_type_0 = ChecklistOperators(data)

                return operator_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            operator_type_1 = BlankEnum(data)

            return operator_type_1

        operator = _parse_operator(d.pop("operator", UNSET))

        review_answer_value = d.pop("review_answer_value", UNSET)

        always_requires_review = d.pop("always_requires_review", UNSET)

        def _parse_guidance_answer_value(
            data: object,
        ) -> Union["PatchedQuestionAdminRequestGuidanceAnswerValueType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                guidance_answer_value_type_0 = PatchedQuestionAdminRequestGuidanceAnswerValueType0.from_dict(data)

                return guidance_answer_value_type_0
            except:  # noqa: E722
                pass
            return cast(Union["PatchedQuestionAdminRequestGuidanceAnswerValueType0", None, Unset], data)

        guidance_answer_value = _parse_guidance_answer_value(d.pop("guidance_answer_value", UNSET))

        def _parse_guidance_operator(data: object) -> Union[BlankEnum, ChecklistOperators, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                guidance_operator_type_0 = ChecklistOperators(data)

                return guidance_operator_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            guidance_operator_type_1 = BlankEnum(data)

            return guidance_operator_type_1

        guidance_operator = _parse_guidance_operator(d.pop("guidance_operator", UNSET))

        always_show_guidance = d.pop("always_show_guidance", UNSET)

        _dependency_logic_operator = d.pop("dependency_logic_operator", UNSET)
        dependency_logic_operator: Union[Unset, DependencyLogicOperatorEnum]
        if isinstance(_dependency_logic_operator, Unset):
            dependency_logic_operator = UNSET
        else:
            dependency_logic_operator = DependencyLogicOperatorEnum(_dependency_logic_operator)

        checklist = d.pop("checklist", UNSET)

        patched_question_admin_request = cls(
            required=required,
            description=description,
            user_guidance=user_guidance,
            question_type=question_type,
            order=order,
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
            operator=operator,
            review_answer_value=review_answer_value,
            always_requires_review=always_requires_review,
            guidance_answer_value=guidance_answer_value,
            guidance_operator=guidance_operator,
            always_show_guidance=always_show_guidance,
            dependency_logic_operator=dependency_logic_operator,
            checklist=checklist,
        )

        patched_question_admin_request.additional_properties = d
        return patched_question_admin_request

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
