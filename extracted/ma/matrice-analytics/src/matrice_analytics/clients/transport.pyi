"""Auto-generated stub for module: transport."""
from typing import Any, Optional, Tuple

from .response import CallFailure

# Constants
ENV_API_BASE: str
LOCAL_AUTHORITY_PREFIXES: Tuple[Any, ...]
logger: Any

# Functions
def backend_base_url(env: Optional[Any[str, str]] = None) -> str:
    """
    The backend's own address, for a route the session's base URL will not serve.
    
        Deployments set ``MATRICE_BASE_URL`` to a local gateway (``http://localhost``). That gateway
        proxies the route prefixes it knows -- ``/v1/inference/*`` among them, which is why
        ``PostProcessingConfigClient`` has always worked -- and 302s anything else out to the real
        backend. ``matrice_common``'s client has ``follow_redirects=True``, and httpx drops the
        ``Authorization`` header when a redirect crosses origin, so a redirected call arrives
        unauthenticated and be-application answers 404. Observed in production on 0.1.428:
        ``http://localhost/v1/applications/.../usecase/download`` -> 302 -> prod -> 404, while the same
        path with a direct base URL returns 200.
    
        Derived the same way ``matrice_common`` derives its own default, so an on-prem or non-prod
        deployment still lands on its own backend; ``$MATRICE_APP_BUNDLE_API_BASE`` overrides it.
    """
    ...
