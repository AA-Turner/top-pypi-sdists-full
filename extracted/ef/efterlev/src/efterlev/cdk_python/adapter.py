"""Adapt parsed `CdkConstruct` records to `TerraformResource` shape.

Python CDK kwargs are already snake_case (e.g. `bucket_name=`,
`versioned=`), which matches Terraform's HCL key convention directly.
That's why CDK Python is the right Stage 1 starting point: the kwargs
flow into a `TerraformResource.body` with no rename step. (TS CDK,
Stage 2+, will need camelCase→snake_case.)

The TF type comes from `cfn_type_to_tf_type` reused from the CFN
adapter, so the existing detector library sees CDK constructs as
`aws_s3_bucket` and friends — same filter pass as Terraform-source
scans.

The source-mode value proposition lands in `SourceRef.line_start`:
unlike the CFN adapter (which sets line_start=None per DECISIONS
2026-05-12 #4), the CDK adapter populates the line number from the
parsed AST so Evidence records cite the .py file:line directly.

Stage 1 scope (v0.1.126): no property-shape translation. Detectors
that read deep nested HCL block syntax (`server_side_encryption_configuration`
etc.) won't fire on raw CDK kwargs (`encryption=...`). That gap is
intentional — Stage 1 validates the architecture; property-mapping
expansion comes in Stage 2+ batches that mirror the v0.1.74-93 CFN
property-mapping arc.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.cdk_python.parser import CdkConstruct
from efterlev.cloudformation.adapter import cfn_type_to_tf_type
from efterlev.models import TerraformResource
from efterlev.models.source_ref import SourceRef


def adapt_cdk_construct_to_terraform(
    construct: CdkConstruct, *, scan_root: Path | None = None
) -> TerraformResource:
    """Convert one parsed CDK construct invocation to a `TerraformResource`.

    Single-resource translation only at Stage 1 (no sub-resource
    synthesis like the CFN IAM::Role-with-inline-policies pattern).
    """
    if scan_root is not None:
        try:
            rel_file = construct.source_file.relative_to(scan_root)
        except ValueError:
            rel_file = construct.source_file
    else:
        rel_file = construct.source_file

    return TerraformResource(
        type=cfn_type_to_tf_type(construct.cfn_type),
        name=construct.construct_id,
        body=dict(construct.kwargs),
        source_ref=SourceRef(
            file=rel_file,
            line_start=construct.source_line,
            line_end=construct.source_line,
        ),
        kind="resource",
    )


def adapt_cdk_constructs(
    constructs: list[CdkConstruct], *, scan_root: Path | None = None
) -> list[TerraformResource]:
    """Adapt a batch of CDK constructs to `TerraformResource` records."""
    return [adapt_cdk_construct_to_terraform(c, scan_root=scan_root) for c in constructs]
