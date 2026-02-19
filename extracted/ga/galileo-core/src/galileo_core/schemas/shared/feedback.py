from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field, StringConstraints
from typing_extensions import Annotated

FeedbackTagType = Annotated[str, StringConstraints(min_length=1, max_length=255, strip_whitespace=True)]


class FeedbackType(str, Enum):
    like_dislike = "like_dislike"
    star = "star"
    score = "score"
    tags = "tags"
    text = "text"


class AnnotationType(str, Enum):
    like_dislike = "like_dislike"
    star = "star"
    score = "score"
    tags = "tags"
    text = "text"


class FeedbackRatingInfo(BaseModel):
    feedback_type: FeedbackType
    value: Union[bool, int, str, List[FeedbackTagType]]
    explanation: Optional[str]


class AnnotationRatingInfo(BaseModel):
    annotation_type: AnnotationType
    value: Union[bool, int, str, List[FeedbackTagType]]
    explanation: Optional[str]


class AnnotationLikeDislikeAggregate(BaseModel):
    annotation_type: Literal[AnnotationType.like_dislike] = AnnotationType.like_dislike
    like_count: int
    dislike_count: int
    unrated_count: int


class AnnotationStarAggregate(BaseModel):
    annotation_type: Literal[AnnotationType.star] = AnnotationType.star
    average: float
    counts: dict[int, int]
    unrated_count: int


class AnnotationScoreAggregate(BaseModel):
    annotation_type: Literal[AnnotationType.score] = AnnotationType.score
    average: float
    unrated_count: int


class AnnotationTagsAggregate(BaseModel):
    annotation_type: Literal[AnnotationType.tags] = AnnotationType.tags
    counts: dict[str, int]
    unrated_count: int


class AnnotationTextAggregate(BaseModel):
    annotation_type: Literal[AnnotationType.text] = AnnotationType.text
    count: int
    unrated_count: int


class AnnotationAggregate(BaseModel):
    aggregate: Annotated[
        AnnotationLikeDislikeAggregate
        | AnnotationStarAggregate
        | AnnotationScoreAggregate
        | AnnotationTagsAggregate
        | AnnotationTextAggregate,
        Field(discriminator="annotation_type"),
    ]
