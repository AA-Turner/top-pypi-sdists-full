"""Canonical phase definitions for agdt-setup.

The ``PHASES`` tuple defines the ordered sequence of phases that ``setup_cmd``
executes.  The sync-gate validator (``expectations_validator.py``) imports this
tuple as the source of truth for phase names — no AST scraping required.
"""

from __future__ import annotations

AUTORUN_SETUP_PHASE = "autorun_setup"

PHASES: tuple[str, ...] = (
    "version_check",
    "certificate_prefetch",
    "cli_installation",
    "dependency_check",
    "environment_persistence",
    "file_modifications",
    AUTORUN_SETUP_PHASE,
)
