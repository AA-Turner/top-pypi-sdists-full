"""AWS SVC at-rest encryption coverage (KSI-SVC-PRR) detector package.

Importing this package registers the detector with the global registry
via the `@detector` decorator in `detector.py`.
"""

from __future__ import annotations

from efterlev.detectors.aws.svc_at_rest_encryption_coverage import detector  # noqa: F401
