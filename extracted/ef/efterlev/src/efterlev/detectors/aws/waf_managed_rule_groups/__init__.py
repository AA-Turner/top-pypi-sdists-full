"""AWS WAFv2 Web ACL managed-rule-group detector package.

Importing this package registers the detector with the global registry via
the `@detector` decorator in `detector.py`.
"""

from __future__ import annotations

from efterlev.detectors.aws.waf_managed_rule_groups import detector  # noqa: F401
