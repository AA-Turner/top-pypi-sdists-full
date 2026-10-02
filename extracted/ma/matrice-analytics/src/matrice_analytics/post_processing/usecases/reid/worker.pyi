"""Auto-generated stub for module: worker."""
from typing import Any, Callable, Dict, List, Optional

# Constants
logger: Any

# Classes
class EmbedWorker:
    # Single daemon thread turning person crops into embeddings.
    #
    #     One worker per use-case instance (i.e. per stream). The embedder it
    #     calls is process-wide and shared, so N streams still cost one model.

    def __init__(self: Any, embed_fn: Callable[[List[Any.Any]], Optional[Any.Any]], max_pending: int = 64, batch_size: int = 8, idle_sleep_s: float = 0.002, name: str = 'reid-embed') -> None: ...

    def alive(self: Any) -> bool: ...

    def forget(self: Any, track_ids: Any) -> None:
        """
        Drop state for tracks the caller no longer cares about.
        """
        ...

    def get_result(self: Any, track_id: Any) -> Optional[Any.Any]: ...

    def has_pending(self: Any, track_id: Any) -> bool: ...

    def offer(self: Any, track_id: Any, crop: Any.Any) -> str:
        """
        Queue ``crop`` for ``track_id``. Never blocks. Returns a disposition.
        """
        ...

    def pop_result(self: Any, track_id: Any) -> Optional[Any.Any]: ...

    def starving(self: Any, grace_s: float = 2.0) -> bool:
        """
        True when work has been queued for ``grace_s`` with nothing completed.
        
                The frame path calls the use case synchronously, and torch inference
                holds the GIL in bursts, so a caller that never yields between frames
                can starve this thread. Frame-count budgets do not help there: the
                frames tick by while no wall-clock time is given to the worker. This
                is the wall-clock escape hatch -- the caller releases deferred tracks
                under their raw ids rather than holding a count hostage.
        """
        ...

    def stats(self: Any) -> Dict[str, Any]: ...

    def stop(self: Any, timeout: float = 2.0) -> None: ...

