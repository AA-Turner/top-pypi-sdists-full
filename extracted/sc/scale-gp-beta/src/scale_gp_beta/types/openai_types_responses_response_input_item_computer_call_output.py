# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .response_computer_tool_call_output_screenshot import ResponseComputerToolCallOutputScreenshot

__all__ = ["OpenAITypesResponsesResponseInputItemComputerCallOutput", "AcknowledgedSafetyCheck"]


class AcknowledgedSafetyCheck(BaseModel):
    """A pending safety check for the computer call."""

    id: str

    code: Optional[str] = None

    message: Optional[str] = None

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


class OpenAITypesResponsesResponseInputItemComputerCallOutput(BaseModel):
    """The output of a computer tool call."""

    call_id: str

    output: ResponseComputerToolCallOutputScreenshot
    """A computer screenshot image used with the computer use tool."""

    type: Literal["computer_call_output"]

    id: Optional[str] = None

    acknowledged_safety_checks: Optional[List[AcknowledgedSafetyCheck]] = None

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
