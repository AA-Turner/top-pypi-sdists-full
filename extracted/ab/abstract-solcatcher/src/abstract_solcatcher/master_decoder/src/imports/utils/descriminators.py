from .imports import *
# ============================================================================
# DISCRIMINATOR HELPERS
# ============================================================================

def event_discriminator(name: str) -> bytes:
    """Anchor-style: sha256('event:{name}')[:8]"""
    return hashlib.sha256(f"event:{name}".encode()).digest()[:8]


def disc_hex(name: str) -> str:
    """Get hex string for an event discriminator"""
    return event_discriminator(name).hex()

