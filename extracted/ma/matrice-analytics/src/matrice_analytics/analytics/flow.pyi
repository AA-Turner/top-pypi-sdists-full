"""Auto-generated stub for module: flow."""
from typing import Any, Dict, Optional, Set

from .engine_session import normalize_index_to_category

# Constants
ALLOWED_CATEGORIES: Set[Any]
FLOW_ENV_VAR: str
NEW_FLOW_DENYLIST: Set[Any]
NEW_FLOW_HARNESS_DENYLIST: Set[Any]
logger: Any

# Functions
def load_manifest_index_to_category(manifest_name: str) -> Optional[Dict[int, str]]:
    """
    Return ``index_to_category`` from a bundled manifest, if present.
    """
    ...
def resolve_manifest_for_app(app_name: Optional[str]) -> Optional[str]:
    """
    Return the new-flow manifest name for ``app_name``, or None for legacy.
    
        A non-None return is a bare manifest name guaranteed to exist under
        ``analytics/config/`` and loadable by ``AnalyticsEngine(manifest_name)``.
    """
    ...
