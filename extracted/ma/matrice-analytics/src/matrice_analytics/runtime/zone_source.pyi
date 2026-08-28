"""Auto-generated stub for module: zone_source."""
from typing import Any, Dict, Optional

from .app_bundle import _open_session
from .app_bundle import fetch_post_processing_config_by_camera_and_app
from .app_bundle import fetch_post_processing_configs
from .backends import _declared_resolution, normalize_zone_config

# Constants
LOOKUP_FALLBACK_ENV: str
MAX_BACKOFF_ENV: str
REFRESH_SECONDS_ENV: str
logger: Any

# Functions
def merge_zone_configs(api: Optional[Any[str, Any]], supplied: Optional[Any[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Combine the API's geometry with whatever the worker sent, **per field**.
    
        ``enrich`` fills gaps and never overwrites, which is right for identity -- the caller knows
        its own camera name better than the SDK does. It is wrong for geometry, because geometry is
        not identity: it changes after deploy, and the value the worker holds came from the
        deployment-time config blob rather than from the camera.
    
        The concrete failure this prevents: a worker whose ``camera_config`` declares only ``lines``
        suppresses the whole API lookup, so an app needing ``zones`` sees none and refuses -- with a
        ``zone_config`` present on the stream, which makes it look like geometry *was* delivered.
    
        So: each of ``zones`` and ``lines`` is taken from the API when the API declares any, and from
        the caller otherwise. A config declaring neither is treated as absent rather than as an
        authoritative "no geometry", which also closes the empty-dict trap for any producer that
        sends ``{"zones": {}, "lines": {}}``.
    """
    ...

# Classes
class ZoneAnswer:
    # What is known about one camera's geometry, and how confident we are of it.

    def fingerprint(self: Any) -> str:
        """
        Stable identity of this geometry, for deciding whether a Session must be rebuilt.
        
                Sorted, because a dict built from a JSON response has whatever key order the server sent
                and a re-fetch that reordered it must not read as a redraw.
        """
        ...

    def has_zones(self: Any) -> bool: ...

class ZoneGeometryResolver:
    # Resolves and re-resolves zone geometry for every camera in one app deployment.
    #
    #     One instance per :class:`~matrice_analytics.runtime.backends.EngineBackend`. Holds one
    #     platform session for its whole life rather than opening one per fetch: with a TTL the fetch
    #     recurs, and ``fetch_post_processing_configs`` opens a fresh session every call otherwise.

    def __init__(self: Any, app_id: str) -> None: ...

    def answer_for(self: Any, camera_id: str, deployment_id: Optional[str], application_id: Optional[str]) -> Any:
        """
        This camera's geometry, refetching when the previous answer is due for a re-check.
        """
        ...

    def diagnostics(self: Any) -> Dict[str, Any]:
        """
        Per-camera geometry state, for an operator asking "why is this camera empty?".
        """
        ...

    def fallback_enabled(self: Any) -> bool: ...

    def max_backoff(self: Any) -> float: ...

    def refresh_seconds(self: Any) -> float: ...

