"""AWS WAFv2 Web ACL IP-set blocking detector package.

Importing this package registers the detector with the global registry via
the `@detector` decorator in `detector.py`.
"""

from __future__ import annotations

from efterlev.detectors.aws.waf_ip_set_blocking import detector  # noqa: F401
