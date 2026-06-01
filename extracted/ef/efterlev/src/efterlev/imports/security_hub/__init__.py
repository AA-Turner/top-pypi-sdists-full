"""AWS Security Hub ASFF ingestion (v0.1.113 M1 Stage 1).

ASFF (AWS Security Finding Format) is the canonical Security Hub
findings shape. `aws securityhub get-findings` produces it; many
third-party tools also emit it (Prowler can target ASFF format too,
which is the v0.1.114+ Prowler-ingestion shortcut).
"""

from __future__ import annotations

from efterlev.imports.security_hub.ingest import (
    IngestSecurityHubInput,
    IngestSecurityHubOutput,
    ingest_security_hub,
)
from efterlev.imports.security_hub.mapping import (
    AsffMapping,
    load_asff_mapping,
)
from efterlev.imports.security_hub.parser import (
    AsffComplianceStatus,
    AsffFinding,
    parse_asff_document,
)

__all__ = [
    "AsffComplianceStatus",
    "AsffFinding",
    "AsffMapping",
    "IngestSecurityHubInput",
    "IngestSecurityHubOutput",
    "ingest_security_hub",
    "load_asff_mapping",
    "parse_asff_document",
]
