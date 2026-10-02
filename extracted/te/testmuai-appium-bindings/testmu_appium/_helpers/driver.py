"""Driver registry.

Verbs receive the driver explicitly from the generated test.py, so the registry is
not the primary access path — it exists for helpers reached from a value expression
(assertions, variable resolution) that have no driver argument to thread.
"""
_drivers: dict[str, object] = {}


def _set_driver(profile: str, driver) -> None:
    _drivers[profile] = driver


def get_driver(profile: str = "default"):
    """The live driver for a profile, or None outside a session."""
    return _drivers.get(profile)


def _clear_drivers() -> None:
    _drivers.clear()
