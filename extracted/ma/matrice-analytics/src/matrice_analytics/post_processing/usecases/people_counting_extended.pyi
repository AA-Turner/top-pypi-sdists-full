"""Auto-generated stub for module: people_counting_extended."""
from typing import Any, Dict, Optional

from ..core.base import ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import PeopleCountingConfig, PeopleCountingExtendedConfig
from .people_counting import PeopleCountingUseCase
from .reid.gallery import ReIDGallery
from .reid.model import EMBEDDING_DIM, get_shared_embedder
from .reid.worker import EmbedWorker

# Constants
logger: Any

# Classes
class PeopleCountingExtendedUseCase:
    # ``people_counting`` plus long-horizon person re-identification.

    def __init__(self: Any) -> None: ...

    def process(self: Any, data: Any, config: Any, input_bytes: Optional[Any] = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def reid_stats(self: Any) -> Dict[str, Any]: ...

    def reset(self: Any) -> None:
        """
        Release ReID resources. Safe to call repeatedly.
        """
        ...

