r"""Define the state object."""

from __future__ import annotations

__all__ = ["ApplyState"]

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from batchtensor.recursive import BaseApplier


@dataclass
class ApplyState:
    r"""Store the current state."""

    applier: BaseApplier
    depth: int = 0

    def increment_depth(self, increment: int = 1) -> ApplyState:
        return ApplyState(applier=self.applier, depth=self.depth + increment)
