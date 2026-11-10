# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .command_locator_param import CommandLocatorParam

__all__ = ["CommandTargetParam"]

CommandTargetParam: TypeAlias = Union[str, CommandLocatorParam]
