"""AWS API Gateway custom-domain TLS minimum-version detector package.

Importing this package registers the detector with the global registry via
the `@detector` decorator in `detector.py`.
"""

from __future__ import annotations

from efterlev.detectors.aws.api_gateway_tls_min_version import detector  # noqa: F401
