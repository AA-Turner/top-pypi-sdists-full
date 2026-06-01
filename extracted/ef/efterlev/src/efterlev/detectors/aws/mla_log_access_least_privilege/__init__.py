"""AWS MLA "Authorizing Log Access" — least-privilege detector package.

Importing this package registers the detector with the global registry
via the `@detector` decorator in `detector.py`.
"""

from __future__ import annotations

from efterlev.detectors.aws.mla_log_access_least_privilege import detector  # noqa: F401
