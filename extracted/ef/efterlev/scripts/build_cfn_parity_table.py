"""Build CFN→TF parity matrix by introspecting:
1. property_mapping._MAPPINGS — registered CFN types
2. each mapping function's tf_type override (default = cfn_type_to_tf_type)
3. each detector's r.type == filters

Adds a manual-review classification layer that handles:
- TF type aliases (aws_alb ↔ aws_lb, etc.)
- TF data sources (aws_iam_policy_document — no CFN concept)
- TF sub-resources CFN bundles inline but we haven't synthesized
- Genuinely unmappable types (aws_iam_account_password_policy)

Run: `uv run python scripts/build_cfn_parity_table.py`
Outputs: docs/cfn-detector-parity.csv
See docs/cfn-detector-parity.md for the full explanation of the matrix.
"""

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, "src")
from efterlev.cloudformation.adapter import cfn_type_to_tf_type
from efterlev.cloudformation.property_mapping import _MAPPINGS

# Probe inputs to trigger synthesis paths so we capture all emitted tf_types.
PROBES = {
    "AWS::S3::Bucket": {"PublicAccessBlockConfiguration": {}},
    "AWS::IAM::Role": {
        "ManagedPolicyArns": ["arn:probe"],
        "Policies": [{"PolicyName": "p", "PolicyDocument": {"X": 1}}],
    },
    "AWS::IAM::User": {
        "ManagedPolicyArns": ["arn:probe"],
        "Policies": [{"PolicyName": "p", "PolicyDocument": {"X": 1}}],
    },
    "AWS::IAM::Group": {
        "ManagedPolicyArns": ["arn:probe"],
        "Policies": [{"PolicyName": "p", "PolicyDocument": {"X": 1}}],
    },
    "AWS::Events::Rule": {"Targets": [{"Id": "t", "Arn": "arn:probe"}]},
    "AWS::EC2::SecurityGroup": {
        "SecurityGroupIngress": [{"IpProtocol": "-1"}],
        "SecurityGroupEgress": [{"IpProtocol": "-1"}],
    },
}

# TF type aliases — same AWS resource, different TF type names. Treated as
# equivalent for coverage purposes.
TF_ALIASES = {
    "aws_alb": "aws_lb",
    "aws_alb_listener": "aws_lb_listener",
}

# TF types that are DATA SOURCES (kind="data") not resources. CFN has no
# data-source concept; these detectors are TF-only by design.
TF_DATA_SOURCES = {"aws_iam_policy_document"}

# TF types that DON'T HAVE A CFN COUNTERPART at all (account-level settings,
# TF-side conveniences, etc.). These are TF-only by reality.
TF_NO_CFN_EQUIVALENT = {
    "aws_iam_account_password_policy",  # account-level setting; CFN has no resource
    "aws_iam_user_login_profile",  # IAM API only; no CFN resource type
    "aws_db_instance_automated_backups_replication",  # TF-only; no CFN resource
    "aws_iam_",  # wildcard from iam_managed_via_terraform meta-detector
}

# TF sub-resources that CFN bundles into a parent resource. Format:
# tf_subresource → (parent_cfn_type_or_None, short_note).
# parent_cfn_type=None means "CFN-mappable but not yet shipped" or
# "genuinely TF-only despite the AWS-side concept existing."
# Detail explanations live in docs/cfn-detector-parity.md.
TF_SUBRESOURCES_BUNDLED_IN_CFN: dict[str, tuple[str | None, str]] = {
    "aws_s3_bucket_versioning": (
        "AWS::S3::Bucket",
        "bundled in parent VersioningConfiguration; not synthesized",
    ),
    "aws_s3_bucket_acl": (
        "AWS::S3::Bucket",
        "bundled in parent AccessControl; not synthesized",
    ),
    "aws_s3_bucket_server_side_encryption_configuration": (
        "AWS::S3::Bucket",
        "bundled in parent BucketEncryption; not synthesized",
    ),
    "aws_s3_bucket_lifecycle_configuration": (
        "AWS::S3::Bucket",
        "bundled in parent LifecycleConfiguration; not synthesized",
    ),
    "aws_s3_bucket_public_access_block": (
        "AWS::S3::Bucket",
        "ALREADY SYNTHESIZED via 1→1+N from batch 1; fires on CFN",
    ),
    "aws_s3_bucket_replication_configuration": (
        "AWS::S3::Bucket",
        "bundled in parent ReplicationConfiguration; not synthesized",
    ),
    "aws_rds_cluster_instance": (
        "AWS::RDS::DBCluster",
        "CFN clusters bundle members via DBInstance+DBClusterIdentifier; not synthesized",
    ),
}


def normalize_tf(tf: str) -> str:
    """Apply aliases (e.g. aws_alb → aws_lb)."""
    return TF_ALIASES.get(tf, tf)


def build_tf_to_cfn() -> dict[str, list[str]]:
    """Invert _MAPPINGS to TF type → list of CFN types that produce it."""
    cfn_to_tf: dict[str, set[str]] = {}
    for cfn_type, fn in _MAPPINGS.items():
        probe = PROBES.get(cfn_type, {})
        try:
            out = fn(probe)
        except Exception:
            out = []
        tf_types: set[str] = set()
        for m in out:
            tf_types.add(m.tf_type if m.tf_type else cfn_type_to_tf_type(cfn_type))
        if not tf_types:
            tf_types.add(cfn_type_to_tf_type(cfn_type))
        cfn_to_tf[cfn_type] = tf_types

    inverted: dict[str, list[str]] = {}
    for cfn, tfs in cfn_to_tf.items():
        for tf in tfs:
            inverted.setdefault(normalize_tf(tf), []).append(cfn)
    return inverted


def list_detectors() -> list[dict]:
    """Walk detector source files, extract id + tf_types_read."""
    detectors_dir = Path("src/efterlev/detectors/aws")
    id_re = re.compile(r'@detector\s*\(\s*\n?\s*id\s*=\s*"([^"]+)"', re.MULTILINE)

    out = []
    for det_dir in sorted(detectors_dir.iterdir()):
        if not det_dir.is_dir() or det_dir.name.startswith("_"):
            continue
        detfile = det_dir / "detector.py"
        if not detfile.exists():
            continue
        text = detfile.read_text()
        m = id_re.search(text)
        det_id = m.group(1) if m else f"aws.{det_dir.name}"
        tf_types_read = sorted(
            {t for t in re.findall(r'"(aws_[a-z0-9_]+)"', text) if not t.startswith("aws_managed")}
        )
        out.append({"id": det_id, "name": det_dir.name, "tf_types_read": tf_types_read})
    return out


def classify(
    tf_types_read: list[str], tf_to_cfn: dict[str, list[str]]
) -> tuple[str, list[str], str]:
    """Return (status, cfn_types_supporting, notes)."""
    cfn_set: set[str] = set()
    truly_unmapped: list[str] = []
    bundled_with_parent: list[tuple[str, str]] = []
    bundled_no_parent: list[tuple[str, str]] = []
    data_sources: list[str] = []
    no_cfn_equiv: list[str] = []

    for tf_raw in tf_types_read:
        tf = normalize_tf(tf_raw)
        cfns = tf_to_cfn.get(tf, [])
        if cfns:
            cfn_set.update(cfns)
            continue
        if tf in TF_DATA_SOURCES:
            data_sources.append(tf)
            continue
        if tf in TF_NO_CFN_EQUIVALENT:
            no_cfn_equiv.append(tf)
            continue
        if tf in TF_SUBRESOURCES_BUNDLED_IN_CFN:
            parent_type, note = TF_SUBRESOURCES_BUNDLED_IN_CFN[tf]
            if parent_type:
                cfn_set.add(parent_type)
                bundled_with_parent.append((tf, note))
            else:
                bundled_no_parent.append((tf, note))
            continue
        truly_unmapped.append(tf)

    sorted_cfn = sorted(cfn_set)
    notes_parts: list[str] = []
    if data_sources:
        notes_parts.append(f"TF data source (no CFN equivalent): {', '.join(data_sources)}")
    if no_cfn_equiv:
        notes_parts.append(f"No CFN counterpart in AWS: {', '.join(no_cfn_equiv)}")
    for tf, note in bundled_with_parent:
        notes_parts.append(f"{tf}: {note}")
    if bundled_no_parent:
        bundled_list = ", ".join(tf for tf, _ in bundled_no_parent)
        notes_parts.append(f"CFN-mappable but not yet shipped: {bundled_list}")
        for tf, note in bundled_no_parent:
            notes_parts.append(f"  - {tf}: {note}")
    if truly_unmapped:
        notes_parts.append(f"Truly unmapped: {', '.join(truly_unmapped)}")

    notes = "; ".join(notes_parts)

    has_real_gap = bool(truly_unmapped or bundled_no_parent)
    has_design_gap = bool(data_sources or no_cfn_equiv or bundled_with_parent)

    if not (has_real_gap or has_design_gap):
        return ("full", sorted_cfn, notes)
    if sorted_cfn and has_real_gap:
        return ("partial", sorted_cfn, notes)
    if sorted_cfn and has_design_gap:
        return ("partial-by-design", sorted_cfn, notes)
    if data_sources or no_cfn_equiv:
        return ("TF-only-by-design", sorted_cfn, notes)
    return ("TF-only-missing-mapping", sorted_cfn, notes)


def main() -> None:
    tf_to_cfn = build_tf_to_cfn()
    detectors = list_detectors()

    out = Path("docs/cfn-detector-parity.csv")
    # CSV-injection rule (=/+/-/@ -> Excel formula) doesn't apply: all data
    # comes from project source code (detector IDs, TF/CFN type names from
    # _MAPPINGS keys + r.type filters). No untrusted-input path exists.
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)  # nosemgrep
        w.writerow(
            [
                "detector_id",
                "tf_types_read",
                "cfn_types_mapped_or_bundled_into",
                "cfn_status",
                "notes",
            ]
        )
        for d in sorted(detectors, key=lambda x: x["id"]):
            status, cfns, notes = classify(d["tf_types_read"], tf_to_cfn)
            w.writerow([d["id"], ";".join(d["tf_types_read"]), ";".join(cfns), status, notes])

    counts: dict[str, int] = {}
    for d in detectors:
        status, _, _ = classify(d["tf_types_read"], tf_to_cfn)
        counts[status] = counts.get(status, 0) + 1
    print(f"Generated docs/cfn-detector-parity.csv with {len(detectors)} detectors")
    for status, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {status}: {count}")


if __name__ == "__main__":
    main()
