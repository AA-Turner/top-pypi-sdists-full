"""CloudFormation parsing + adapter — Tier 5 #1 plumbing layer.

Per DECISIONS 2026-05-12 (Tier 5 #1, "CloudFormation/CDK synth-mode
support"). v0.1.72 (PR beta) shipped the parser + type-translation
adapter + scan integration. v0.1.73 (PR gamma) adds the
property-mapping table for 3 resource types (architecture validation;
bulk sweep deferred to PR gamma.2).
"""

from __future__ import annotations

from efterlev.cloudformation.adapter import (
    adapt_cfn_resources,
    adapt_cfn_to_terraform,
    cfn_type_to_tf_type,
)
from efterlev.cloudformation.parser import (
    CfnParseFailure,
    CfnParseResult,
    CfnResource,
    parse_cfn_file,
    parse_cfn_tree,
)
from efterlev.cloudformation.property_mapping import (
    MappedResource,
    apply_mapping,
    has_mapping,
    mapped_cfn_types,
)

__all__ = [
    "CfnParseFailure",
    "CfnParseResult",
    "CfnResource",
    "MappedResource",
    "adapt_cfn_resources",
    "adapt_cfn_to_terraform",
    "apply_mapping",
    "cfn_type_to_tf_type",
    "has_mapping",
    "mapped_cfn_types",
    "parse_cfn_file",
    "parse_cfn_tree",
]
