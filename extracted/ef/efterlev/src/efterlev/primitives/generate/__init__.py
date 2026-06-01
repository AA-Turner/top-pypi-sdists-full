"""Generate primitives — produce FRMR / HTML / (v1) OSCAL output artifacts.

Importing this package triggers `@primitive` registration for every
module below. The Documentation Agent (Phase 3) composes these primitives
with LLM narrative-fill to produce agent-drafted attestations; the same
primitives used standalone produce scanner-only artifacts with no LLM
involvement (DECISIONS 2026-04-21 design call #2).
"""

from __future__ import annotations

from efterlev.primitives.generate.generate_component_definition_oscal import (
    GenerateComponentDefinitionOscalInput,
    GenerateComponentDefinitionOscalOutput,
    generate_component_definition_oscal,
)
from efterlev.primitives.generate.generate_frmr_attestation import (
    GenerateFrmrAttestationInput,
    GenerateFrmrAttestationOutput,
    generate_frmr_attestation,
)
from efterlev.primitives.generate.generate_frmr_skeleton import (
    GenerateFrmrSkeletonInput,
    GenerateFrmrSkeletonOutput,
    generate_frmr_skeleton,
)
from efterlev.primitives.generate.generate_inventory import (
    INVENTORY_SCHEMA_VERSION,
    GenerateInventoryInput,
    GenerateInventoryOutput,
    InventoryEntry,
    InventorySourceFile,
    generate_inventory,
)
from efterlev.primitives.generate.generate_poam_markdown import (
    GeneratePoamMarkdownInput,
    GeneratePoamMarkdownOutput,
    PoamClassificationInput,
    generate_poam_markdown,
)
from efterlev.primitives.generate.generate_poam_oscal import (
    GeneratePoamOscalInput,
    GeneratePoamOscalOutput,
    generate_poam_oscal,
)
from efterlev.primitives.generate.generate_vdr_report import (
    VDR_SCHEMA_VERSION,
    GenerateVdrReportInput,
    GenerateVdrReportOutput,
    VdrClassificationInput,
    VdrEntry,
    generate_vdr_report,
)

__all__ = [
    "INVENTORY_SCHEMA_VERSION",
    "VDR_SCHEMA_VERSION",
    "GenerateComponentDefinitionOscalInput",
    "GenerateComponentDefinitionOscalOutput",
    "GenerateFrmrAttestationInput",
    "GenerateFrmrAttestationOutput",
    "GenerateFrmrSkeletonInput",
    "GenerateFrmrSkeletonOutput",
    "GenerateInventoryInput",
    "GenerateInventoryOutput",
    "GeneratePoamMarkdownInput",
    "GeneratePoamMarkdownOutput",
    "GeneratePoamOscalInput",
    "GeneratePoamOscalOutput",
    "GenerateVdrReportInput",
    "GenerateVdrReportOutput",
    "InventoryEntry",
    "InventorySourceFile",
    "PoamClassificationInput",
    "VdrClassificationInput",
    "VdrEntry",
    "generate_component_definition_oscal",
    "generate_frmr_attestation",
    "generate_frmr_skeleton",
    "generate_inventory",
    "generate_poam_markdown",
    "generate_poam_oscal",
    "generate_vdr_report",
]
