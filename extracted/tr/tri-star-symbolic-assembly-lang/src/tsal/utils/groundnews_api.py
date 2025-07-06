"""Placeholder for GroundNews integration."""

class GroundNewsAPIError(RuntimeError):
    pass


def fetch_news(*_args, **_kwargs):
    """GroundNews has no public API."""
    raise GroundNewsAPIError("No public API available")
