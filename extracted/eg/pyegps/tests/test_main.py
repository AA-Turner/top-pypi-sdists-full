"""Test main functionality."""

from pyegps import DEVICE_IMPLEMENTATIONS


def test_implementations_have_unique_ids():
    """Test that all device implementations have their unique implementation id."""
    unique_ids = []
    for impl in DEVICE_IMPLEMENTATIONS:
        assert (impl_id := impl.get_implementation_id()) is not unique_ids
        unique_ids.append(impl_id)
