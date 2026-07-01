# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .last_k_memory_strategy_params import LastKMemoryStrategyParams

__all__ = ["MemoryStrategy"]


class MemoryStrategy(BaseModel):
    params: LastKMemoryStrategyParams
    """Configuration parameters for the memory strategy."""

    name: Optional[Literal["last_k"]] = None
    """Name of the memory strategy. Must be `last_k`.

    This strategy truncates the message history to the last `k` messages. It is the
    simplest way to prevent the model's context limit from being exceeded. However,
    this strategy only allows the model to have short term memory. For longer term
    memory, please use one of the other strategies.
    """
