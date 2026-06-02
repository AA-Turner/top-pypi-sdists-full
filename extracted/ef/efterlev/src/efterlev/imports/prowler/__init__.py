"""Prowler ingestion (v0.1.123 M1 Stage 5).

Prowler (https://prowler.com/) is a popular open-source AWS security
scanner. It produces several output formats; this primitive consumes
its native JSON output (the default for `prowler aws -M json`).

Mirrors `efterlev.imports.security_hub` + `efterlev.imports.config` —
parser + mapping + ingest. Same architecture, different input shape:
Prowler uses `CheckID` (not ASFF `GeneratorId` or Config `ConfigRuleName`)
and a 3-state `Status` (PASS / FAIL / MANUAL) rather than ASFF's
4-state Compliance.Status.

Why we ingest Prowler natively instead of routing customers through
Prowler's ASFF output (which `import-security-hub` could already
consume):
- Prowler's native JSON has richer fields (CheckType, Severity,
  ResourceTags, Risk, Remediation) that Prowler's ASFF translation
  drops.
- Customers running Prowler in multi-tool aggregation workflows already have
  the native JSON; adding an ASFF translation step is friction.
- Native ingest path lets us evolve the Prowler-specific Evidence
  content shape independently of the ASFF mapping table.
"""

from __future__ import annotations

from efterlev.imports.prowler.ingest import (
    IngestProwlerInput,
    IngestProwlerOutput,
    ingest_prowler,
)
from efterlev.imports.prowler.mapping import (
    ProwlerMapping,
    load_prowler_mapping,
)
from efterlev.imports.prowler.parser import (
    ProwlerFinding,
    ProwlerStatus,
    parse_prowler_document,
)

__all__ = [
    "IngestProwlerInput",
    "IngestProwlerOutput",
    "ProwlerFinding",
    "ProwlerMapping",
    "ProwlerStatus",
    "ingest_prowler",
    "load_prowler_mapping",
    "parse_prowler_document",
]
