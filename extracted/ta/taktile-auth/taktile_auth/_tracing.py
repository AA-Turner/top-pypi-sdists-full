import hashlib

from taktile_auth._logging import get_logger
from taktile_auth.settings import settings

logger = get_logger()


def is_session_sampled(session_prefix: str) -> bool:
    """Whether ``session_prefix`` falls in the ``SESSION_SAMPLE_PERCENT`` sample.

    Every hop of one session makes the same decision, so a sampled
    session is logged at every hop it reaches.
    """
    # hash() is salted per process; a digest gives every service the same bucket.
    bucket = int.from_bytes(hashlib.sha256(session_prefix.encode()).digest()[:8], "big") % 100
    percent: int = settings.SESSION_SAMPLE_PERCENT
    return bucket < percent


def log_session_hop(session_prefix: str, weight: int, success: bool) -> None:
    """Log one line for this hop when its session is sampled."""
    if is_session_sampled(session_prefix):
        logger.info(
            "call_graph_hop",
            extra={"session_prefix": session_prefix, "weight": weight, "success": success},
        )
