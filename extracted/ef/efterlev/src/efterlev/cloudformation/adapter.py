"""Convert CFN resources to `TerraformResource`-shaped objects.

Per DECISIONS 2026-05-12 (Tier 5 #1, Decision #2): the adapter shim
approach lets existing detectors filter by `r.type == "aws_s3_bucket"`
against CFN resources whose CFN-native type is `AWS::S3::Bucket`.

**Updated scope as of v0.1.73 (PR gamma).** v0.1.72 (PR beta) shipped
type-name translation only; this release adds the property-mapping
table that translates CFN's `Properties` structure into TF body shape
for registered resource types. Coverage at v0.1.73 is intentionally
narrow (3 resource types — `AWS::S3::Bucket`, `AWS::S3::BucketPolicy`,
`AWS::ElasticLoadBalancingV2::Listener`) to validate the mapping shape
against the three sample detectors named in DECISIONS 2026-05-12
(`aws.encryption_s3_at_rest`, `aws.s3_public_access_block`,
`aws.tls_on_lb_listeners`). PR gamma.2 expands coverage.

The adapter signature also changed from 1→1 to 1→N: a single CFN
resource may yield multiple TF resources when the CFN structure folds
multiple TF concerns together (notably `AWS::S3::Bucket`'s
`PublicAccessBlockConfiguration`, which becomes a separate
`aws_s3_bucket_public_access_block`).

**Two paths through the adapter:**

- Registered CFN type (`property_mapping.has_mapping()` True): the
  registered mapping function emits a list of `MappedResource`s; each
  becomes a `TerraformResource` with TF-shape body.
- Unregistered CFN type (fallback): shallow snake_case mirror of
  top-level property keys, values unchanged. Detectors filtering on
  these types pass the type filter but read no meaningful body data —
  honest "we see this resource exists, but can't yet read into its
  properties."

Detectors don't need to change — they continue to filter by
`r.type == "aws_s3_bucket"` and read `r.body[...]` as they always have.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from efterlev.cloudformation.parser import CfnResource
from efterlev.cloudformation.property_mapping import apply_mapping, has_mapping
from efterlev.models import SourceRef, TerraformResource

_CAMEL_TO_SNAKE_RE = re.compile(r"(?<!^)(?=[A-Z])")


def _camel_to_snake(name: str) -> str:
    """`BucketName` → `bucket_name`; naive single-pass.

    Used for the unregistered-CFN-type fallback path only. Registered
    types go through the property-mapping table which uses explicit
    per-key renames.
    """
    return _CAMEL_TO_SNAKE_RE.sub("_", name).lower()


def cfn_type_to_tf_type(cfn_type: str) -> str:
    """`AWS::S3::Bucket` → `aws_s3_bucket`.

    Lower-cases each `::`-separated segment whole (no internal
    underscoring) and joins with `_`. Matches the dominant TF
    convention for `aws_<service>_<resource>` types.

    Limitation: multi-CamelCase Resource segments (`WebACL` in
    `AWS::WAFv2::WebACL`) lose word boundaries — yields
    `aws_wafv2_webacl` not the TF-canonical `aws_wafv2_web_acl`.
    Per-resource overrides land via the property-mapping table when
    those resource types ship.
    """
    parts = cfn_type.split("::")
    return "_".join(p.lower() for p in parts)


def adapt_cfn_to_terraform(
    cfn: CfnResource, *, scan_root: Path | None = None
) -> list[TerraformResource]:
    """Convert one `CfnResource` to one or more `TerraformResource`s.

    Returns a list because a single CFN resource may yield multiple TF
    resources (sub-resource synthesis — see module docstring). Most
    resources yield a single-element list.
    """
    if scan_root is not None:
        try:
            rel_file = cfn.file.relative_to(scan_root)
        except ValueError:
            rel_file = cfn.file
    else:
        rel_file = cfn.file

    # SourceRef line numbers null per DECISIONS 2026-05-12 #4
    # (file-level only at v1).
    source_ref = SourceRef(file=rel_file, line_start=None, line_end=None)

    default_tf_type = cfn_type_to_tf_type(cfn.type)

    if has_mapping(cfn.type):
        mapped = apply_mapping(cfn.type, cfn.properties)
        return [
            TerraformResource(
                type=m.tf_type if m.tf_type is not None else default_tf_type,
                name=cfn.logical_id + m.name_suffix,
                body=m.body,
                source_ref=source_ref,
                kind="resource",
            )
            for m in mapped
        ]

    # Fallback for unmapped types: shallow snake_case mirror.
    fallback_body: dict[str, Any] = {_camel_to_snake(k): v for k, v in cfn.properties.items()}
    return [
        TerraformResource(
            type=default_tf_type,
            name=cfn.logical_id,
            body=fallback_body,
            source_ref=source_ref,
            kind="resource",
        )
    ]


def adapt_cfn_resources(
    resources: list[CfnResource], *, scan_root: Path | None = None
) -> list[TerraformResource]:
    """Adapt a batch of `CfnResource` records to `TerraformResource`s.

    Flattens the per-resource 1→N expansion into a single list. The
    output length may exceed the input length (sub-resource synthesis).
    """
    out: list[TerraformResource] = []
    for r in resources:
        out.extend(adapt_cfn_to_terraform(r, scan_root=scan_root))
    return out
