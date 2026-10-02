"""VLM alert verification -- the worker the ``verification`` primitive submits to.

Normative source: ``VLM-VERIFY-INTERFACES.md`` §2.  Importing this package starts nothing:
no thread, no socket, no environment read.  :func:`worker_for` builds the process-wide
worker lazily, on first use, from the ``MATRICE_VERIFY_*`` / ``MATRICE_VSS_VERIFY_*``
environment; :func:`close_all_workers` stops it (also registered with :mod:`atexit`).

See :mod:`matrice_analytics.engine.verify.worker` for the threading model and retry table.
"""

from __future__ import annotations

from matrice_analytics.engine.verify.worker import (
    Verdict,
    VerificationWorker,
    VerifyJob,
    close_all_workers,
    worker_for,
)

__all__ = ["Verdict", "VerificationWorker", "VerifyJob", "close_all_workers", "worker_for"]
