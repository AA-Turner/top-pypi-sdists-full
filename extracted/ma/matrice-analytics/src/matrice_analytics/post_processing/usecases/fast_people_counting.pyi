"""Auto-generated stub for module: fast_people_counting."""
from typing import Any, Dict, Optional

from ..core.base import ConfigProtocol, ProcessingContext, ProcessingResult
from .people_counting import PeopleCountingUseCase

# Classes
class FastPeopleCountingUseCase:
    # Trackerless, debug-free people counter for high-throughput pipelines.

    def __init__(self: Any) -> None: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

