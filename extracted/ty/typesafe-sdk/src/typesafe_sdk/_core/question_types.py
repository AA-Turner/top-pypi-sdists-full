"""Question objects and raw input models."""

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, Literal, TypeAlias, overload

from pydantic import BaseModel, ConfigDict, Field, model_serializer
from pydantic.functional_serializers import SerializerFunctionWrapHandler
from typing_extensions import NotRequired, TypedDict

from typesafe_sdk._core.json_types import JSONContent
from typesafe_sdk._schemas import models as wire


class NoulCriteria(TypedDict, total=False, closed=True):
    """Optional descriptions of the yes and no outcomes.

    See the [noul primitive](https://docs.typesafe.ai/primitives/noul) for details.
    """

    true: JSONContent | None
    """Description of the yes outcome as text, a JSON object, or an array; `None` leaves it undescribed."""
    false: JSONContent | None
    """Description of the no outcome as text, a JSON object, or an array; `None` leaves it undescribed."""


class _DescribedTrue(TypedDict, closed=True):
    true: JSONContent
    false: NotRequired[JSONContent | None]


class _DescribedFalse(TypedDict, closed=True):
    true: NotRequired[JSONContent | None]
    false: JSONContent


class NoulModel(TypedDict, closed=True):
    """A yes/no question dictionary with `type="noul"`.

    See the [noul primitive](https://docs.typesafe.ai/primitives/noul) for details.
    """

    type: Literal["noul"]
    instructions: NotRequired[JSONContent | None]
    """The question to ask, expressed as text, a JSON object, or an array; optional when `criteria` describes an outcome."""
    criteria: NotRequired[NoulCriteria | None]
    """Optional descriptions of the yes and no outcomes; required when `instructions` is `None`."""


class ChoiceModel(TypedDict, closed=True):
    """A choice question dictionary with `type="choice"`.

    See the [choice primitive](https://docs.typesafe.ai/primitives/choice) for details.
    """

    type: Literal["choice"]
    instructions: NotRequired[JSONContent | None]
    """The question to ask, expressed as text, a JSON object, or an array; optional."""
    criteria: Mapping[str, JSONContent | None]
    """A nonempty mapping of labels to text, object, or array descriptions, or `None` for undescribed labels."""


class ScoreModel(TypedDict, closed=True):
    """A score question dictionary with `type="score"`.

    See the [score primitive](https://docs.typesafe.ai/primitives/score) for details.
    """

    type: Literal["score"]
    instructions: NotRequired[JSONContent | None]
    """The question to ask, expressed as text, a JSON object, or an array; optional."""
    criteria: Sequence[JSONContent]
    """A nonempty, ordered list of text, object, or array descriptions, one per score from zero."""


class _Question(BaseModel):
    """Reject unknown fields and omit optional fields left at their default from the wire form."""

    model_config = ConfigDict(extra="forbid")

    @model_serializer(mode="wrap")
    def _omit_none(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        # An unset optional field (`None`) is left off the wire, while user-supplied `None` values
        # nested inside `criteria`/`instructions` are preserved.
        return {key: value for key, value in handler(self).items() if value is not None}


class Noul(_Question, wire.NoulQuestion):
    """A yes/no question with optional descriptions for either outcome.

    See the [noul primitive](https://docs.typesafe.ai/primitives/noul) for details.
    """

    type: Literal["noul"] = "noul"
    instructions: JSONContent | None = None  # pyrefly: ignore[bad-override-mutable-attribute]
    """The question to ask, expressed as text, a JSON object, or an array; optional when `criteria` describes an outcome."""
    criteria: NoulCriteria | None = None  # pyrefly: ignore[bad-override-mutable-attribute]
    """Optional descriptions of the yes and no outcomes; required when `instructions` is `None`."""

    if TYPE_CHECKING:
        # Require instructions or at least one described outcome.
        @overload
        def __init__(self, *, type: Literal["noul"] = ..., instructions: JSONContent, criteria: NoulCriteria | None = ...) -> None: ...
        @overload
        def __init__(self, *, type: Literal["noul"] = ..., instructions: None = ..., criteria: _DescribedTrue | _DescribedFalse) -> None: ...
        def __init__(self, **data: Any) -> None: ...


class Choice(_Question, wire.ChoiceQuestion):
    """A question that selects between named alternatives.

    See the [choice primitive](https://docs.typesafe.ai/primitives/choice) for details.
    """

    type: Literal["choice"] = "choice"
    criteria: Mapping[str, JSONContent | None]  # pyrefly: ignore[bad-override-mutable-attribute]
    """A nonempty mapping of labels to text, object, or array descriptions, or `None` for undescribed labels."""
    instructions: JSONContent | None = None  # pyrefly: ignore[bad-override-mutable-attribute]
    """The question to ask, expressed as text, a JSON object, or an array; optional."""


class Score(_Question, wire.ScoreQuestion):
    """A question that assigns a score using an ordered rubric.

    See the [score primitive](https://docs.typesafe.ai/primitives/score) for details.
    """

    type: Literal["score"] = "score"
    criteria: Sequence[JSONContent] = Field(min_length=1)  # pyrefly: ignore[bad-override-mutable-attribute]
    """A nonempty, ordered list of text, object, or array descriptions, one per score from zero."""
    instructions: JSONContent | None = None  # pyrefly: ignore[bad-override-mutable-attribute]
    """The question to ask, expressed as text, a JSON object, or an array; optional."""


QuestionModel: TypeAlias = NoulModel | ChoiceModel | ScoreModel
"""A question dictionary identified by its `type` key."""
Question: TypeAlias = Noul | Choice | Score | QuestionModel
"""A question object or question dictionary."""
Questions: TypeAlias = Mapping[str, Question]
"""Question inputs keyed by the names used to identify their answers."""
