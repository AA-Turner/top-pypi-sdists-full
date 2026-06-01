"""GitHub PIY SDLC security-gates (KSI-PIY-RSD) detector package.

Importing this package registers the detector with the global registry
via the `@detector` decorator in `detector.py`.
"""

from __future__ import annotations

from efterlev.detectors.github.piy_sdlc_security_gates import detector  # noqa: F401
