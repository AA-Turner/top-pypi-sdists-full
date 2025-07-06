"""Core constants and axis validation."""

class UndefinedPhaseError(Exception):
    """Raised when an object lacks the spin axis."""

AXIS_ZERO = "spin"

def ensure_spin_axis(obj) -> None:
    """Raise ``UndefinedPhaseError`` if ``obj`` lacks a ``spin`` attribute."""
    has_spin = False
    if isinstance(obj, dict):
        has_spin = "spin" in obj
    else:
        has_spin = hasattr(obj, "spin")
    if not has_spin:
        raise UndefinedPhaseError("System operating without spin axis.")

__all__ = ["AXIS_ZERO", "ensure_spin_axis", "UndefinedPhaseError"]
