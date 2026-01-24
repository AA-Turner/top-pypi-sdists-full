from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, StringConstraints
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
