# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .._types import SequenceNotStr
from .command_target_param import CommandTargetParam
from .command_locator_param import CommandLocatorParam

__all__ = ["CommandFrameParam"]

CommandFrameParam: TypeAlias = Union[str, CommandLocatorParam, SequenceNotStr[CommandTargetParam]]
