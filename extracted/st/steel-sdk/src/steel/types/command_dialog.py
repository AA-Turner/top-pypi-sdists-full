# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["CommandDialog"]


class CommandDialog(BaseModel):
    """A JavaScript dialog: alert, confirm, prompt, or beforeunload."""

    id: str

    message: str

    tab: str

    type: Literal["alert", "confirm", "prompt", "beforeunload"]

    default_prompt: Optional[str] = FieldInfo(alias="defaultPrompt", default=None)
