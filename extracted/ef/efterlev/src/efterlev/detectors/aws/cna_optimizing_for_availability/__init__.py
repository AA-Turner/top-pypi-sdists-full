"""AWS CNA "Optimizing for Availability" detector package.

Importing this package registers the detector with the global registry via
the `@detector` decorator in `detector.py`.
"""

from __future__ import annotations

from efterlev.detectors.aws.cna_optimizing_for_availability import detector  # noqa: F401
