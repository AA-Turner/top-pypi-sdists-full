"""Pure validation rejects inconsistent or incomplete claims without normalization."""

from dataclasses import replace

import pytest

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import (
    ReconciliationCriterionVerdict,
    ReconciliationFileVerdict,
    ReconciliationValidationError,
    validate_reconciliation_attestation,
)


class TupleSubclass(tuple):
    pass


def test_valid_claim_is_not_authentication(attestation):
    assert attestation.repair_output_sha != attestation.reviewed_head_sha
    assert validate_reconciliation_attestation(attestation) is None
    invented = replace(
        attestation,
        configured_approver_login="invented-reviewer",
        reviewer_login="invented-reviewer",
        repair_writer_login="invented-writer",
        criteria_source_sha256="0" * 64,
    )
    assert validate_reconciliation_attestation(invented) is None


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("schema_version", True, "unsupported_schema_version"),
        ("schema_version", 2, "unsupported_schema_version"),
        ("schema_version", "1", "unsupported_schema_version"),
        ("repository", None, "invalid_repository"),
        ("repository", "Owner/repo", "invalid_repository"),
        ("repository", "owner//repo", "invalid_repository"),
        ("repository", "/repo", "invalid_repository"),
        ("repository", "owner/", "invalid_repository"),
        ("repository", "owner/repo ", "invalid_repository"),
        ("repository", "-owner/repo", "invalid_repository"),
        ("repository", "own--er/repo", "invalid_repository"),
        ("repository", "a" * 40 + "/repo", "invalid_repository"),
        ("repository", "owner/" + "a" * 101, "invalid_repository"),
        ("repository", "owner/répo", "invalid_repository"),
        ("pr_number", True, "invalid_pr_number"),
        ("pr_number", 0, "invalid_pr_number"),
        ("pr_number", -1, "invalid_pr_number"),
        ("pr_number", "42", "invalid_pr_number"),
        ("pr_number", 1.0, "invalid_pr_number"),
        ("criteria_source", "https://example.com/criteria", "criterion_coverage_mismatch"),
        ("criteria_source", None, "criterion_coverage_mismatch"),
        ("criteria_source_sha256", "A" * 64, "invalid_sha256"),
        ("criteria_source_sha256", None, "invalid_sha256"),
        ("provider_evidence_ref", "", "invalid_provider_evidence_ref"),
        ("provider_evidence_ref", "github://other/repo/pull/42/reviews", "invalid_provider_evidence_ref"),
        ("provider_evidence_ref", "github://example-owner/repo/pull/43/reviews", "invalid_provider_evidence_ref"),
        ("provider_evidence_ref", "github://example-owner/repo/pull/42/reviews/1", "invalid_provider_evidence_ref"),
        ("reviewer_login", "someone-else", "reviewer_not_configured_approver"),
        ("repair_writer_login", "approver", "reviewer_is_repair_writer"),
        ("changed_files", (), "file_inventory_empty"),
        ("changed_files", ("a.py", "a.py"), "duplicate_file"),
        ("changed_files", ("src/b.py", "a.py"), "noncanonical_order"),
        ("changed_files", ("a.py",), "file_verdict_coverage_mismatch"),
    ],
)
def test_invalid_scalar_or_inventory(attestation, field, value, reason):
    with pytest.raises(ReconciliationValidationError) as error:
        validate_reconciliation_attestation(replace(attestation, **{field: value}))
    assert error.value.reason == reason


@pytest.mark.parametrize("field", ["pre_repair_sha", "pinned_base_sha", "repair_output_sha", "reviewed_head_sha"])
@pytest.mark.parametrize("value", [None, "", "a" * 39, "a" * 41, "A" * 40, "g" * 40, "a" * 40 + "\n"])
def test_commit_ids(attestation, field, value):
    with pytest.raises(ReconciliationValidationError) as error:
        validate_reconciliation_attestation(replace(attestation, **{field: value}))
    assert error.value.reason == "invalid_commit_sha"


@pytest.mark.parametrize("field", ["configured_approver_login", "reviewer_login", "repair_writer_login"])
@pytest.mark.parametrize("value", [None, "", "Uppercase", "-a", "a-", "a--b", "a_b", "é", "a" * 40, "a\n"])
def test_login_grammar(attestation, field, value):
    with pytest.raises(ReconciliationValidationError) as error:
        validate_reconciliation_attestation(replace(attestation, **{field: value}))
    assert error.value.reason == "invalid_login"


@pytest.mark.parametrize("field", ["changed_files", "file_verdicts", "criterion_verdicts"])
@pytest.mark.parametrize("factory", [list, set, TupleSubclass])
def test_mutable_and_subclass_collections_are_not_coerced(attestation, field, factory):
    value = factory(getattr(attestation, field))
    invalid = replace(attestation, **{field: value})
    with pytest.raises(ReconciliationValidationError) as error:
        validate_reconciliation_attestation(invalid)
    assert error.value.reason == "invalid_collection_type"
    assert getattr(invalid, field) is value
    assert type(value) is factory


@pytest.mark.parametrize("field", ["file_verdicts", "criterion_verdicts"])
@pytest.mark.parametrize("value", [None, {}, "accepted"])
def test_wrong_records(attestation, field, value):
    with pytest.raises(ReconciliationValidationError) as error:
        validate_reconciliation_attestation(replace(attestation, **{field: (value,)}))
    assert error.value.reason == "invalid_record_type"


@pytest.mark.parametrize(
    ("field", "record_type"),
    [("file_verdicts", ReconciliationFileVerdict), ("criterion_verdicts", ReconciliationCriterionVerdict)],
)
def test_record_subclasses_rejected(attestation, field, record_type):
    record = getattr(attestation, field)[0]
    subclass = type("RecordSubclass", (record_type,), {})
    value = subclass(**vars(record))
    with pytest.raises(ReconciliationValidationError) as error:
        validate_reconciliation_attestation(replace(attestation, **{field: (value,)}))
    assert error.value.reason == "invalid_record_type"


@pytest.mark.parametrize("path", [None, "", "/abs", "C:/abs", "a\\b", "a//b", ".", "..", "a/./b", "a/../b", "a/", "\0"])
def test_invalid_git_paths(attestation, path):
    with pytest.raises(ReconciliationValidationError) as error:
        validate_reconciliation_attestation(replace(attestation, changed_files=(path,)))
    assert error.value.reason == "invalid_file_path"


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("content_sha256", "", "invalid_sha256"),
        ("content_sha256", "f" * 63, "invalid_sha256"),
        ("content_sha256", "G" * 64, "invalid_sha256"),
        ("behavior", "", "empty_file_behavior"),
        ("behavior", " \n\t", "empty_file_behavior"),
        ("behavior", None, "empty_file_behavior"),
        ("verdict", "rejected", "file_verdict_rejected"),
        ("verdict", "unresolved", "file_verdict_unresolved"),
        ("verdict", "invalid", "invalid_file_verdict"),
        ("verdict", None, "invalid_file_verdict"),
        ("verdict", [], "invalid_file_verdict"),
        ("path", "../a", "invalid_file_path"),
    ],
)
def test_file_record_fields(attestation, field, value, reason):
    record = replace(attestation.file_verdicts[0], **{field: value})
    with pytest.raises(ReconciliationValidationError) as error:
        validate_reconciliation_attestation(replace(attestation, file_verdicts=(record, attestation.file_verdicts[1])))
    assert error.value.reason == reason


@pytest.mark.parametrize(
    ("kind", "reason"),
    [
        ("missing", "file_verdict_coverage_mismatch"),
        ("extra", "file_verdict_coverage_mismatch"),
        ("duplicate", "duplicate_file"),
        ("order", "noncanonical_order"),
    ],
)
def test_file_coverage(attestation, kind, reason):
    a, b = attestation.file_verdicts
    records = {
        "missing": (a,),
        "extra": (a, b, replace(b, path="z.py")),
        "duplicate": (a, a, b),
        "order": (b, a),
    }[kind]
    with pytest.raises(ReconciliationValidationError) as error:
        validate_reconciliation_attestation(replace(attestation, file_verdicts=records))
    assert error.value.reason == reason


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("criterion_id", "AC8", "criterion_coverage_mismatch"),
        ("criterion_id", None, "criterion_coverage_mismatch"),
        ("criterion_id", [], "criterion_coverage_mismatch"),
        ("rationale", "", "empty_criterion_rationale"),
        ("rationale", " \n", "empty_criterion_rationale"),
        ("rationale", None, "empty_criterion_rationale"),
        ("verdict", "rejected", "criterion_verdict_rejected"),
        ("verdict", "unresolved", "criterion_verdict_unresolved"),
        ("verdict", "invalid", "invalid_criterion_verdict"),
        ("verdict", None, "invalid_criterion_verdict"),
        ("verdict", [], "invalid_criterion_verdict"),
    ],
)
def test_criterion_record_fields(attestation, field, value, reason):
    record = replace(attestation.criterion_verdicts[0], **{field: value})
    with pytest.raises(ReconciliationValidationError) as error:
        validate_reconciliation_attestation(
            replace(attestation, criterion_verdicts=(record, *attestation.criterion_verdicts[1:]))
        )
    assert error.value.reason == reason


@pytest.mark.parametrize(
    ("kind", "reason"),
    [
        ("missing", "criterion_coverage_mismatch"),
        ("extra", "criterion_coverage_mismatch"),
        ("duplicate", "duplicate_criterion"),
        ("order", "noncanonical_order"),
    ],
)
def test_criterion_coverage(attestation, kind, reason):
    records = attestation.criterion_verdicts
    records = {
        "missing": records[:-1],
        "extra": (*records, replace(records[0], criterion_id="AC8")),
        "duplicate": (*records, records[0]),
        "order": tuple(reversed(records)),
    }[kind]
    with pytest.raises(ReconciliationValidationError) as error:
        validate_reconciliation_attestation(replace(attestation, criterion_verdicts=records))
    assert error.value.reason == reason


def test_wrong_attestation_type():
    with pytest.raises(ReconciliationValidationError) as error:
        validate_reconciliation_attestation({})
    assert error.value.reason == "invalid_record_type"


def test_canonical_grammar_boundaries(attestation):
    repository = "a" * 39 + "/" + "r" * 97 + "._-"
    candidate = replace(
        attestation,
        repository=repository,
        pr_number=1,
        provider_evidence_ref=f"github://{repository}/pull/1/reviews",
        configured_approver_login="a" * 39,
        reviewer_login="a" * 39,
        repair_writer_login="0",
    )
    assert validate_reconciliation_attestation(candidate) is None
