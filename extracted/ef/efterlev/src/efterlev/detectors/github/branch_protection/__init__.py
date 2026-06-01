"""GitHub branch_protection detector package.

Importing this package registers the detector with the global registry via
the `@detector` decorator in `detector.py`.
"""

from __future__ import annotations

from efterlev.detectors.github.branch_protection import detector  # noqa: F401
