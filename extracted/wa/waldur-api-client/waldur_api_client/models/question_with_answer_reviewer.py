from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blank_enum import BlankEnum
from ..models.checklist_operators import ChecklistOperators
from ..models.question_type_enum import QuestionTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.question_with_answer_reviewer_dependencies_info_type_0 import (
        QuestionWithAnswerReviewerDependenciesInfoType0,
    )
    from ..models.question_with_answer_reviewer_existing_answer_type_0 import (
        QuestionWithAnswerReviewerExistingAnswerType0,
    )


T = TypeVar("T", bound="QuestionWithAnswerReviewer")


@_attrs_define
class QuestionWithAnswerReviewer:
    """
    Attributes:
        uuid (UUID):
        description (str):
        user_guidance (Union[None, str]):
        question_type (QuestionTypeEnum):
        required (bool):
        order (int):
        existing_answer (Union['QuestionWithAnswerReviewerExistingAnswerType0', None]):
        question_options (Union[None, list[Any]]):
        min_value (Union[None, str]): Minimum value allowed for NUMBER, YEAR, and RATING type questions
        max_value (Union[None, str]): Maximum value allowed for NUMBER, YEAR, and RATING type questions
        allowed_file_types (Any): List of allowed file extensions (e.g., ['.pdf', '.doc', '.docx']). If empty, all file
            types are allowed.
        allowed_mime_types (Any): List of allowed MIME types (e.g., ['application/pdf', 'application/msword']). If
            empty, MIME type validation is not enforced. When both extensions and MIME types are specified, files must match
            both criteria for security.
        max_file_size_mb (Union[None, int]): Maximum file size in megabytes. If not set, no size limit is enforced.
        max_files_count (Union[None, int]): Maximum number of files allowed for MULTIPLE_FILES type questions. If not
            set, no count limit is enforced.
        dependencies_info (Union['QuestionWithAnswerReviewerDependenciesInfoType0', None]):
        operator (Union[BlankEnum, ChecklistOperators, Unset]):
        review_answer_value (Union[Unset, Any]): Answer value that trigger review.
        always_requires_review (Union[Unset, bool]): This question always requires review regardless of answer
    """

    uuid: UUID
    description: str
    user_guidance: Union[None, str]
    question_type: QuestionTypeEnum
    required: bool
    order: int
    existing_answer: Union["QuestionWithAnswerReviewerExistingAnswerType0", None]
    question_options: Union[None, list[Any]]
    min_value: Union[None, str]
    max_value: Union[None, str]
    allowed_file_types: Any
    allowed_mime_types: Any
    max_file_size_mb: Union[None, int]
    max_files_count: Union[None, int]
    dependencies_info: Union["QuestionWithAnswerReviewerDependenciesInfoType0", None]
    operator: Union[BlankEnum, ChecklistOperators, Unset] = UNSET
    review_answer_value: Union[Unset, Any] = UNSET
    always_requires_review: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.question_with_answer_reviewer_dependencies_info_type_0 import (
            QuestionWithAnswerReviewerDependenciesInfoType0,
        )
        from ..models.question_with_answer_reviewer_existing_answer_type_0 import (
            QuestionWithAnswerReviewerExistingAnswerType0,
        )

        uuid = str(self.uuid)

        description = self.description

        user_guidance: Union[None, str]
        user_guidance = self.user_guidance

        question_type = self.question_type.value

        required = self.required

        order = self.order

        existing_answer: Union[None, dict[str, Any]]
        if isinstance(self.existing_answer, QuestionWithAnswerReviewerExistingAnswerType0):
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

        allowed_file_types = self.allowed_file_types

        allowed_mime_types = self.allowed_mime_types

        max_file_size_mb: Union[None, int]
        max_file_size_mb = self.max_file_size_mb

        max_files_count: Union[None, int]
        max_files_count = self.max_files_count

        dependencies_info: Union[None, dict[str, Any]]
        if isinstance(self.dependencies_info, QuestionWithAnswerReviewerDependenciesInfoType0):
            dependencies_info = self.dependencies_info.to_dict()
        else:
            dependencies_info = self.dependencies_info

        operator: Union[Unset, str]
        if isinstance(self.operator, Unset):
            operator = UNSET
        elif isinstance(self.operator, ChecklistOperators):
            operator = self.operator.value
        else:
            operator = self.operator.value

        review_answer_value = self.review_answer_value

        always_requires_review = self.always_requires_review

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
                "dependencies_info": dependencies_info,
            }
        )
        if operator is not UNSET:
            field_dict["operator"] = operator
        if review_answer_value is not UNSET:
            field_dict["review_answer_value"] = review_answer_value
        if always_requires_review is not UNSET:
            field_dict["always_requires_review"] = always_requires_review

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.question_with_answer_reviewer_dependencies_info_type_0 import (
            QuestionWithAnswerReviewerDependenciesInfoType0,
        )
        from ..models.question_with_answer_reviewer_existing_answer_type_0 import (
            QuestionWithAnswerReviewerExistingAnswerType0,
        )

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

        def _parse_existing_answer(data: object) -> Union["QuestionWithAnswerReviewerExistingAnswerType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                existing_answer_type_0 = QuestionWithAnswerReviewerExistingAnswerType0.from_dict(data)

                return existing_answer_type_0
            except:  # noqa: E722
                pass
            return cast(Union["QuestionWithAnswerReviewerExistingAnswerType0", None], data)

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

        allowed_file_types = d.pop("allowed_file_types")

        allowed_mime_types = d.pop("allowed_mime_types")

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

        def _parse_dependencies_info(data: object) -> Union["QuestionWithAnswerReviewerDependenciesInfoType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dependencies_info_type_0 = QuestionWithAnswerReviewerDependenciesInfoType0.from_dict(data)

                return dependencies_info_type_0
            except:  # noqa: E722
                pass
            return cast(Union["QuestionWithAnswerReviewerDependenciesInfoType0", None], data)

        dependencies_info = _parse_dependencies_info(d.pop("dependencies_info"))

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

        question_with_answer_reviewer = cls(
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
            dependencies_info=dependencies_info,
            operator=operator,
            review_answer_value=review_answer_value,
            always_requires_review=always_requires_review,
        )

        question_with_answer_reviewer.additional_properties = d
        return question_with_answer_reviewer

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
