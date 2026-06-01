"""CFN ↔ TF parity tests for the 3 sample detectors (v0.1.73 PR gamma).

Each test constructs an equivalent CFN resource and TF resource, runs
the same detector against both, and asserts the emitted Evidence
content matches (modulo source_ref details — file path differs).

This is the validation that the property-mapping table produces TF
shapes detectors can actually consume; without it, the v0.1.72 plumbing
work was hypothetical. Per DECISIONS 2026-05-12 amendment (PR gamma
follow-on entry): if all 3 detectors emit equivalent Evidence for
parallel inputs, the mapping shape is validated against the architecture
plan.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from efterlev.cloudformation import adapt_cfn_resources, parse_cfn_file
from efterlev.detectors.aws.encryption_s3_at_rest import detector as encryption_detector
from efterlev.detectors.aws.s3_public_access_block import detector as pab_detector
from efterlev.detectors.aws.tls_on_lb_listeners import detector as tls_detector
from efterlev.models import SourceRef, TerraformResource


def _content_minus_source(evidence_list: list) -> list[dict[str, Any]]:
    """Strip source_ref/timestamp from Evidence for parity comparison.

    source_ref.file legitimately differs between the CFN .yaml input and
    the in-memory TF construction; we compare on the evidence *content*.
    timestamp varies on every run; we compare the rest.
    """
    return [
        {
            "detector_id": e.detector_id,
            "ksis_evidenced": e.ksis_evidenced,
            "controls_evidenced": e.controls_evidenced,
            "content": e.content,
        }
        for e in evidence_list
    ]


# --- aws.encryption_s3_at_rest -----------------------------------------------


def test_encryption_s3_at_rest_parity_encrypted(tmp_path: Path) -> None:
    """An encrypted CFN S3 bucket emits the same Evidence as the TF equivalent."""
    cfn_path = tmp_path / "stack.yaml"
    cfn_path.write_text(
        "Resources:\n"
        "  EncryptedBucket:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties:\n"
        "      BucketName: encrypted-bucket\n"
        "      BucketEncryption:\n"
        "        ServerSideEncryptionConfiguration:\n"
        "          - ServerSideEncryptionByDefault:\n"
        "              SSEAlgorithm: AES256\n"
    )
    cfn_resources = parse_cfn_file(cfn_path)
    cfn_tf_resources = adapt_cfn_resources(cfn_resources, scan_root=tmp_path)

    tf_equivalent = [
        TerraformResource(
            type="aws_s3_bucket",
            name="EncryptedBucket",
            body={
                "bucket": "encrypted-bucket",
                "server_side_encryption_configuration": [
                    {
                        "rule": [
                            {
                                "apply_server_side_encryption_by_default": [
                                    {"sse_algorithm": "AES256"}
                                ]
                            }
                        ]
                    }
                ],
            },
            source_ref=SourceRef(file=Path("stack.tf"), line_start=None, line_end=None),
            kind="resource",
        )
    ]

    cfn_ev = _content_minus_source(encryption_detector.detect(cfn_tf_resources))
    tf_ev = _content_minus_source(encryption_detector.detect(tf_equivalent))

    assert cfn_ev == tf_ev
    assert len(cfn_ev) == 1
    assert cfn_ev[0]["content"]["encryption_state"] == "present"
    assert cfn_ev[0]["content"]["algorithm"] == "AES256"
    assert "SC-28(1)" in cfn_ev[0]["controls_evidenced"]


def test_encryption_s3_at_rest_parity_unencrypted(tmp_path: Path) -> None:
    """An unencrypted CFN S3 bucket emits the gap-evidence equivalent to TF."""
    cfn_path = tmp_path / "stack.yaml"
    cfn_path.write_text(
        "Resources:\n"
        "  PlainBucket:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties:\n"
        "      BucketName: plain-bucket\n"
    )
    cfn_resources = parse_cfn_file(cfn_path)
    cfn_tf_resources = adapt_cfn_resources(cfn_resources, scan_root=tmp_path)

    tf_equivalent = [
        TerraformResource(
            type="aws_s3_bucket",
            name="PlainBucket",
            body={"bucket": "plain-bucket"},
            source_ref=SourceRef(file=Path("stack.tf"), line_start=None, line_end=None),
            kind="resource",
        )
    ]

    cfn_ev = _content_minus_source(encryption_detector.detect(cfn_tf_resources))
    tf_ev = _content_minus_source(encryption_detector.detect(tf_equivalent))

    assert cfn_ev == tf_ev
    assert cfn_ev[0]["content"]["encryption_state"] == "absent"


# --- aws.s3_public_access_block ----------------------------------------------


def test_s3_pab_parity_fully_blocked(tmp_path: Path) -> None:
    """CFN bucket with all 4 PAB flags → same Evidence as TF separate-resource."""
    cfn_path = tmp_path / "stack.yaml"
    cfn_path.write_text(
        "Resources:\n"
        "  LockedBucket:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties:\n"
        "      PublicAccessBlockConfiguration:\n"
        "        BlockPublicAcls: true\n"
        "        IgnorePublicAcls: true\n"
        "        BlockPublicPolicy: true\n"
        "        RestrictPublicBuckets: true\n"
    )
    cfn_resources = parse_cfn_file(cfn_path)
    cfn_tf_resources = adapt_cfn_resources(cfn_resources, scan_root=tmp_path)

    tf_equivalent = [
        TerraformResource(
            type="aws_s3_bucket_public_access_block",
            name="LockedBucket_pab",
            body={
                "block_public_acls": True,
                "ignore_public_acls": True,
                "block_public_policy": True,
                "restrict_public_buckets": True,
            },
            source_ref=SourceRef(file=Path("stack.tf"), line_start=None, line_end=None),
            kind="resource",
        )
    ]

    cfn_ev = _content_minus_source(pab_detector.detect(cfn_tf_resources))
    tf_ev = _content_minus_source(pab_detector.detect(tf_equivalent))

    assert cfn_ev == tf_ev
    assert len(cfn_ev) == 1
    assert cfn_ev[0]["content"]["posture"] == "fully_blocked"


def test_s3_pab_parity_partial(tmp_path: Path) -> None:
    """Partial PAB → same partial-posture Evidence + gap content."""
    cfn_path = tmp_path / "stack.yaml"
    cfn_path.write_text(
        "Resources:\n"
        "  HalfBlocked:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties:\n"
        "      PublicAccessBlockConfiguration:\n"
        "        BlockPublicAcls: true\n"
        "        BlockPublicPolicy: false\n"
    )
    cfn_resources = parse_cfn_file(cfn_path)
    cfn_tf_resources = adapt_cfn_resources(cfn_resources, scan_root=tmp_path)

    tf_equivalent = [
        TerraformResource(
            type="aws_s3_bucket_public_access_block",
            name="HalfBlocked_pab",
            body={
                "block_public_acls": True,
                "block_public_policy": False,
            },
            source_ref=SourceRef(file=Path("stack.tf"), line_start=None, line_end=None),
            kind="resource",
        )
    ]

    cfn_ev = _content_minus_source(pab_detector.detect(cfn_tf_resources))
    tf_ev = _content_minus_source(pab_detector.detect(tf_equivalent))

    assert cfn_ev == tf_ev
    assert cfn_ev[0]["content"]["posture"] == "partial"


# --- aws.tls_on_lb_listeners -------------------------------------------------


def test_tls_on_lb_listener_parity_https(tmp_path: Path) -> None:
    """HTTPS CFN listener → same Evidence as TF equivalent."""
    cfn_path = tmp_path / "stack.yaml"
    cfn_path.write_text(
        "Resources:\n"
        "  SecureListener:\n"
        "    Type: AWS::ElasticLoadBalancingV2::Listener\n"
        "    Properties:\n"
        "      Protocol: HTTPS\n"
        "      Port: 443\n"
        "      SslPolicy: ELBSecurityPolicy-TLS-1-2-2017-01\n"
        "      Certificates:\n"
        "        - CertificateArn: arn:aws:acm:us-east-1:123:certificate/abc\n"
    )
    cfn_resources = parse_cfn_file(cfn_path)
    cfn_tf_resources = adapt_cfn_resources(cfn_resources, scan_root=tmp_path)

    tf_equivalent = [
        TerraformResource(
            type="aws_lb_listener",
            name="SecureListener",
            body={
                "protocol": "HTTPS",
                "port": 443,
                "ssl_policy": "ELBSecurityPolicy-TLS-1-2-2017-01",
                "certificate_arn": "arn:aws:acm:us-east-1:123:certificate/abc",
            },
            source_ref=SourceRef(file=Path("stack.tf"), line_start=None, line_end=None),
            kind="resource",
        )
    ]

    cfn_ev = _content_minus_source(tls_detector.detect(cfn_tf_resources))
    tf_ev = _content_minus_source(tls_detector.detect(tf_equivalent))

    assert cfn_ev == tf_ev
    assert len(cfn_ev) == 1
    assert cfn_ev[0]["content"]["tls_state"] == "present"
    assert cfn_ev[0]["content"]["certificate_arn_present"] is True
    assert cfn_ev[0]["content"]["ssl_policy"] == "ELBSecurityPolicy-TLS-1-2-2017-01"


def test_tls_on_lb_listener_parity_http(tmp_path: Path) -> None:
    """Plain HTTP CFN listener → same absent-Evidence as TF equivalent."""
    cfn_path = tmp_path / "stack.yaml"
    cfn_path.write_text(
        "Resources:\n"
        "  PlainListener:\n"
        "    Type: AWS::ElasticLoadBalancingV2::Listener\n"
        "    Properties:\n"
        "      Protocol: HTTP\n"
        "      Port: 80\n"
    )
    cfn_resources = parse_cfn_file(cfn_path)
    cfn_tf_resources = adapt_cfn_resources(cfn_resources, scan_root=tmp_path)

    tf_equivalent = [
        TerraformResource(
            type="aws_lb_listener",
            name="PlainListener",
            body={"protocol": "HTTP", "port": 80},
            source_ref=SourceRef(file=Path("stack.tf"), line_start=None, line_end=None),
            kind="resource",
        )
    ]

    cfn_ev = _content_minus_source(tls_detector.detect(cfn_tf_resources))
    tf_ev = _content_minus_source(tls_detector.detect(tf_equivalent))

    assert cfn_ev == tf_ev
    assert cfn_ev[0]["content"]["tls_state"] == "absent"


# --- Sub-resource synthesis end-to-end --------------------------------------


def test_single_cfn_bucket_emits_evidence_to_two_detectors(tmp_path: Path) -> None:
    """One CFN bucket with both encryption + PAB feeds two different detectors.

    Validates the 1→N expansion at the per-detector level: the synthesized
    PAB resource is visible to `aws.s3_public_access_block`, and the bucket
    itself is visible to `aws.encryption_s3_at_rest`.
    """
    cfn_path = tmp_path / "stack.yaml"
    cfn_path.write_text(
        "Resources:\n"
        "  HardenedBucket:\n"
        "    Type: AWS::S3::Bucket\n"
        "    Properties:\n"
        "      BucketName: hardened\n"
        "      BucketEncryption:\n"
        "        ServerSideEncryptionConfiguration:\n"
        "          - ServerSideEncryptionByDefault:\n"
        "              SSEAlgorithm: aws:kms\n"
        "      PublicAccessBlockConfiguration:\n"
        "        BlockPublicAcls: true\n"
        "        IgnorePublicAcls: true\n"
        "        BlockPublicPolicy: true\n"
        "        RestrictPublicBuckets: true\n"
    )
    cfn_resources = parse_cfn_file(cfn_path)
    tf_resources = adapt_cfn_resources(cfn_resources, scan_root=tmp_path)

    assert len(tf_resources) == 2

    enc_ev = encryption_detector.detect(tf_resources)
    assert len(enc_ev) == 1
    assert enc_ev[0].content["encryption_state"] == "present"
    assert enc_ev[0].content["algorithm"] == "aws:kms"

    pab_ev = pab_detector.detect(tf_resources)
    assert len(pab_ev) == 1
    assert pab_ev[0].content["posture"] == "fully_blocked"


# --- BucketPolicy parity (no detector touches it yet; structural test only) -


def test_s3_bucket_policy_translated_with_canonical_tf_type() -> None:
    """AWS::S3::BucketPolicy → aws_s3_bucket_policy (not the default broken translation)."""
    from efterlev.cloudformation.parser import CfnResource

    cfn = CfnResource(
        logical_id="MyPolicy",
        type="AWS::S3::BucketPolicy",
        properties={
            "Bucket": "my-bucket",
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [{"Effect": "Deny", "Action": "*", "Resource": "*"}],
            },
        },
        file=Path("stack.yaml"),
    )
    tf_resources = adapt_cfn_resources([cfn])
    assert len(tf_resources) == 1
    assert tf_resources[0].type == "aws_s3_bucket_policy"
    assert "Statement" in tf_resources[0].body["policy"]  # JSON-stringified


# --- Coverage list assertion (architectural pin) ----------------------------


def test_v0_1_73_coverage_subset_still_present() -> None:
    """The 3 PR gamma resource types must remain in the registry across batches.

    The full coverage list grows with each PR gamma.N batch — pinned in
    the batch-N test file. This test ensures the original 3 stay covered.
    """
    from efterlev.cloudformation.property_mapping import mapped_cfn_types

    coverage = set(mapped_cfn_types())
    assert {
        "AWS::ElasticLoadBalancingV2::Listener",
        "AWS::S3::Bucket",
        "AWS::S3::BucketPolicy",
    }.issubset(coverage)


# --- Reject "no mapping" cleanly --------------------------------------------


def test_unmapped_type_raises_on_apply_mapping() -> None:
    """`apply_mapping` raises KeyError for unmapped types; adapter should NOT call it."""
    from efterlev.cloudformation.property_mapping import apply_mapping

    with pytest.raises(KeyError, match="no property mapping"):
        # Use a CFN type with no detector reads (Athena WorkGroup) — guaranteed
        # unmapped. CloudFront::Distribution was used here pre-v0.1.93 but is
        # now explicitly mapped per PR gamma.2 batch 8 (the finishing batch).
        apply_mapping("AWS::Athena::WorkGroup", {})
