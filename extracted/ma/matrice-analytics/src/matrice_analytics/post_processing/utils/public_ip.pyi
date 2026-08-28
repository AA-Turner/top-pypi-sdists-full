"""Auto-generated stub for module: public_ip."""
from typing import Any, Optional

# Constants
ENV_SKIP_PUBLIC_IP: str

# Functions
def reset_cache() -> None:
    """
    Forget the resolved value so the next call looks it up again.
    
        Test support. Production never calls this: the whole point of the module is
        that the answer is decided once, and re-deciding it re-introduces the
        per-frame stall this replaced.
    """
    ...
def resolve_public_ip_once(logger: Optional[Any.Any] = None) -> str:
    """
    This host's public IP, resolved at most once per process.
    
        Returns ``"localhost"`` when the lookup is disabled or fails. The lock is
        held across the request so N first-frame initialisers racing on startup make
        one lookup between them rather than N.
    """
    ...
