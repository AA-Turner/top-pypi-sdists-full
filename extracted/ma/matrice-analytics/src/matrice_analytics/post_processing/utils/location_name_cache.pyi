"""Auto-generated stub for module: location_name_cache."""
from typing import Any, Optional

# Classes
class LocationNameCache:
    # Remember resolved names; let failures expire.
    #
    #     Thread-safe: ``face_recognition`` and the plate sync sender both resolve names off
    #     their own threads while the frame thread is in ``process()``.

    def __init__(self: Any, retry_after: float = RETRY_AFTER_SECONDS) -> None: ...

    def clear(self: Any) -> None:
        """
        Drop everything. For tests and for a session change.
        """
        ...

    def note_failure(self: Any, location_id: str) -> None:
        """
        Start (or restart) the cool-off after a lookup failed.
        """
        ...

    def resolved(self: Any, location_id: str) -> Optional[str]:
        """
        The cached name, or ``None`` when this id has never resolved.
        """
        ...

    def should_fetch(self: Any, location_id: str) -> bool:
        """
        Whether a caller should spend a request on this id now.
        
                ``False`` only while a recent failure is still inside its cool-off. An id that
                has never been tried, or whose last failure has aged out, is always fetchable.
        """
        ...

    def store(self: Any, location_id: str, name: str) -> None:
        """
        Record a resolved name and clear any earlier failure for it.
        """
        ...

