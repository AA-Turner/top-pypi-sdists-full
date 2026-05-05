# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "OpenAITypesResponsesResponseInputItemFunctionCallOutput",
    "OutputOutputContentList",
    "OutputOutputContentListResponseInputTextContent",
    "OutputOutputContentListResponseInputImageContent",
    "OutputOutputContentListResponseInputFileContent",
]


class OutputOutputContentListResponseInputTextContent(BaseModel):
    """A text input to the model."""

    text: str

    type: Literal["input_text"]

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class OutputOutputContentListResponseInputImageContent(BaseModel):
    """An image input to the model.

    Learn about [image inputs](https://platform.openai.com/docs/guides/vision)
    """

    type: Literal["input_image"]

    detail: Optional[Literal["low", "high", "auto"]] = None

    file_id: Optional[str] = None

    image_url: Optional[str] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class OutputOutputContentListResponseInputFileContent(BaseModel):
    """A file input to the model."""

    type: Literal["input_file"]

    file_data: Optional[str] = None

    file_id: Optional[str] = None

    file_url: Optional[str] = None

    filename: Optional[str] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


OutputOutputContentList: TypeAlias = Union[
    OutputOutputContentListResponseInputTextContent,
    OutputOutputContentListResponseInputImageContent,
    OutputOutputContentListResponseInputFileContent,
]


class OpenAITypesResponsesResponseInputItemFunctionCallOutput(BaseModel):
    """The output of a function tool call."""

    call_id: str

    output: Union[str, List[OutputOutputContentList]]

    type: Literal["function_call_output"]

    id: Optional[str] = None

    status: Optional[Literal["in_progress", "completed", "incomplete"]] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]
