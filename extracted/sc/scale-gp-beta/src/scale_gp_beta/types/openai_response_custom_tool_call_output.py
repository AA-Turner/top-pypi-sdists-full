# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .openai_response_input_file import OpenAIResponseInputFile
from .openai_response_input_text import OpenAIResponseInputText
from .openai_response_input_image import OpenAIResponseInputImage

__all__ = ["OpenAIResponseCustomToolCallOutput", "OutputOutputContentList"]

OutputOutputContentList: TypeAlias = Union[OpenAIResponseInputText, OpenAIResponseInputImage, OpenAIResponseInputFile]


class OpenAIResponseCustomToolCallOutput(BaseModel):
    """The output of a custom tool call from your code, being sent back to the model."""

    call_id: str

    output: Union[str, List[OutputOutputContentList]]

    type: Literal["custom_tool_call_output"]

    id: Optional[str] = None

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
