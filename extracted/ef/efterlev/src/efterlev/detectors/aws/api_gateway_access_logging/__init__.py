"""AWS API Gateway access-logging configuration detector package.

Importing this package registers the detector with the global registry via
the `@detector` decorator in `detector.py`.
"""

from __future__ import annotations

from efterlev.detectors.aws.api_gateway_access_logging import detector  # noqa: F401
