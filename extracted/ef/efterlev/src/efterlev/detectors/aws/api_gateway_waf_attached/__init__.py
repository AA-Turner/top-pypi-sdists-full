"""AWS API Gateway WAF-attachment detector package.

Importing this package registers the detector with the global registry via
the `@detector` decorator in `detector.py`.
"""

from __future__ import annotations

from efterlev.detectors.aws.api_gateway_waf_attached import detector  # noqa: F401
