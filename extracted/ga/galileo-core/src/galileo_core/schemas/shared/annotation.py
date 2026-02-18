from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field, StringConstraints
from typing_extensions import Annotated

AnnotationTagType = Annotated[str, StringConstraints(min_length=1, max_length=255, strip_whitespace=True)]


class AnnotationType(str, Enum):
    like_dislike = "like_dislike"
    star = "star"
    score = "score"
    tags = "tags"
    text = "text"


class AnnotationRatingInfo(BaseModel):
    annotation_type: AnnotationType
    value: Union[bool, int, str, List[AnnotationTagType]]
    explanation: Optional[str]


class LikeDislikeAggregate(BaseModel):
    annotation_type: Literal[AnnotationType.like_dislike] = AnnotationType.like_dislike
    like_count: int
    dislike_count: int
    unrated_count: int

    def sortable_value(self) -> float:
        return (
            self.like_count / (self.like_count + self.dislike_count + self.unrated_count)
            if self.like_count + self.dislike_count > 0
            else 0.0
        )


class StarAggregate(BaseModel):
    annotation_type: Literal[AnnotationType.star] = AnnotationType.star
    average: float
    counts: dict[int, int]
    unrated_count: int

    def sortable_value(self) -> float:
        return self.average


class ScoreAggregate(BaseModel):
    annotation_type: Literal[AnnotationType.score] = AnnotationType.score
    average: float
    unrated_count: int

    def sortable_value(self) -> float:
        return self.average


class TagsAggregate(BaseModel):
    annotation_type: Literal[AnnotationType.tags] = AnnotationType.tags
    counts: dict[str, int]
    unrated_count: int

    def sortable_value(self) -> float:
        return max(self.counts.values(), default=0)


class TextAggregate(BaseModel):
    annotation_type: Literal[AnnotationType.text] = AnnotationType.text
    count: int
    unrated_count: int

    def sortable_value(self) -> float:
        return float(self.count)


class AnnotationAggregate(BaseModel):
    aggregate: Annotated[
        LikeDislikeAggregate | StarAggregate | ScoreAggregate | TagsAggregate | TextAggregate,
        Field(discriminator="annotation_type"),
    ]

    @property
    def sortable_value(self) -> float:
        """Returns a value that can be used for sorting annotation aggregates."""
        return self.aggregate.sortable_value()
