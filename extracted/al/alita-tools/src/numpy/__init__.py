"""
Stub for numpy module to avoid importing the real numpy in tests.
"""
# Minimal stub for numpy to avoid import errors and segmentation faults in tests.
__all__ = []
def __getattr__(name):
    raise ImportError(f"numpy stub does not provide {name}")