"""The new analytics engine package.

Sub-packages are built independently:

* :mod:`matrice_analytics.engine.contract` -- the wire format (S1/S2/S3/S4),
  the single build+validate+publish path, and the conformance checks.
* ``matrice_analytics.engine.manifest`` -- app manifest loading/validation.

Nothing in :mod:`matrice_analytics.engine` may import from
``matrice_analytics.post_processing`` or ``matrice_analytics.analytics``.
"""

from __future__ import annotations

__all__: list[str] = []
