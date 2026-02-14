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


class FeedbackRatingInfo(BaseModel):
    feedback_type: FeedbackType
    value: Union[bool, int, str, List[FeedbackTagType]]
    explanation: Optional[str]


class LikeDislikeAggregate(BaseModel):
    feedback_type: Literal[FeedbackType.like_dislike] = FeedbackType.like_dislike
    like_count: int
    dislike_count: int
    unrated_count: int


class StarAggregate(BaseModel):
    feedback_type: Literal[FeedbackType.star] = FeedbackType.star
    average: float
    counts: dict[int, int]
    unrated_count: int


class ScoreAggregate(BaseModel):
    feedback_type: Literal[FeedbackType.score] = FeedbackType.score
    average: float
    unrated_count: int


class TagsAggregate(BaseModel):
    feedback_type: Literal[FeedbackType.tags] = FeedbackType.tags
    counts: dict[str, int]
    unrated_count: int


class TextAggregate(BaseModel):
    feedback_type: Literal[FeedbackType.text] = FeedbackType.text
    count: int
    unrated_count: int


class FeedbackAggregate(BaseModel):
    aggregate: Annotated[
        LikeDislikeAggregate | StarAggregate | ScoreAggregate | TagsAggregate | TextAggregate,
        Field(discriminator="feedback_type"),
    ]
