"""AWS Lambda environment-variable KMS-encryption detector package.

Importing this package registers the detector with the global registry via
the `@detector` decorator in `detector.py`.
"""

from __future__ import annotations

from efterlev.detectors.aws.lambda_env_kms_encryption import detector  # noqa: F401
