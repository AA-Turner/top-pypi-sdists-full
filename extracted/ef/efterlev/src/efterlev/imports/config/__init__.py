"""AWS Config evaluations ingestion (v0.1.114 M1 Stage 3).

AWS Config produces evaluations of resources against Config Rules. The
JSON shape is `aws configservice get-compliance-details-by-config-rule
--config-rule-name <name>`. Many rules map directly to NIST 800-53
controls + FRMR KSIs, similar to Security Hub's ASFF generator-id
mapping pattern.

Mirrors `efterlev.imports.security_hub`: parser → mapping → ingest →
Evidence record. Same architecture, different input shape.
"""

from __future__ import annotations

from efterlev.imports.config.ingest import (
    IngestConfigInput,
    IngestConfigOutput,
    ingest_config,
)
from efterlev.imports.config.mapping import (
    ConfigMapping,
    load_config_mapping,
)
from efterlev.imports.config.parser import (
    ConfigComplianceType,
    ConfigEvaluation,
    parse_config_document,
)

__all__ = [
    "ConfigComplianceType",
    "ConfigEvaluation",
    "ConfigMapping",
    "IngestConfigInput",
    "IngestConfigOutput",
    "ingest_config",
    "load_config_mapping",
    "parse_config_document",
]
