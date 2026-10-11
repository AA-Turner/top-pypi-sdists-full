"""Legacy path: a pip too old for PEP 517 runs this instead of the backend."""
import sys

sys.path.insert(0, ".")
import bithuman_platform_guard as _g  # noqa: E402

_g._refuse()
