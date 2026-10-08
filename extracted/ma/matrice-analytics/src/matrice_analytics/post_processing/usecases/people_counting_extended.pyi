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

    def drain_reid(self: Any, timeout_s: float = 2.0) -> bool:
        """
        Wait for every queued embedding to be applied. Offline use only.
        
                Re-identification runs on a background thread, so the frame a
                verdict lands on -- and therefore the gallery state it is matched
                against -- depends on thread scheduling. Replaying one clip twice
                can give different unique counts for that reason alone.
        
                Calling this after each :meth:`process` pins the schedule and makes
                the count repeatable, which is what threshold calibration and
                regression tests need. It blocks on the embedder, so it must not be
                used on a live realtime stream.
        """
        ...

    def interval_counts(self: Any) -> Dict[str, int]:
        """
        Distinct people this window, and how many were never seen before.
        
                Read by the analytics bridge once per publish; see
                :meth:`reset_interval`, which the bridge calls immediately after.
        """
        ...

    def process(self: Any, data: Any, config: Any, input_bytes: Optional[Any] = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def reid_stats(self: Any) -> Dict[str, Any]: ...

    def reset(self: Any) -> None:
        """
        Release ReID resources. Safe to call repeatedly.
        """
        ...

    def reset_interval(self: Any) -> None:
        """
        Start a new publish window. Lifetime identities are kept.
        
                Keeping ``_lifetime_identities`` is the whole point: it is what makes
                a returning person count toward "total" but never again toward "new".
                It grows with distinct people, not with time, and is bounded in
                practice by the gallery capacity that mints the ids.
        """
        ...

