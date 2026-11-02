"""Source evidence binds the same trusted owner as its ledger obligation."""

from dataclasses import replace
from datetime import timedelta

import pytest
from pydantic import ValidationError

from adcp.reporting.conformance import (
    ReportingSourceConformanceError,
    validate_reporting_revision_sequence,
    validate_reporting_source_execution,
)
from adcp.reporting.fixtures import (
    redacted_capabilities,
    redacted_completed_result,
    redacted_snapshot_request,
)
from adcp.reporting.ledger import ReportingStatusCaller
from adcp.reporting.ledger.provisional import ProvisionalAcquisition, ProvisionalPolicy
from adcp.reporting.ledger.store import LedgerConflictError
from adcp.reporting.source import (
    ReportingSourceIdentityV1,
    SourceBatchManifestV1,
    encode_source_batch_manifest_v1,
    publication_content_fingerprint_v1,
)
from tests.test_reporting_settling import _capabilities, _harness, _only_obligation


@pytest.mark.parametrize("consumer", ["buyer-a", "https://buyer.example/" + "a" * 300])
def test_source_owner_accepts_trusted_principals_and_full_buyer_urls(consumer):
    request = redacted_snapshot_request(consumer_id=consumer)
    assert request.identity.consumer_id == consumer
    assert (
        ReportingSourceIdentityV1.model_validate_json(request.identity.model_dump_json())
        == request.identity
    )


@pytest.mark.parametrize("consumer", ["", "https://user:password@buyer.example", "a" * 2049])
def test_source_owner_uses_reporting_identity_validation(consumer):
    with pytest.raises(ValidationError):
        redacted_snapshot_request(consumer_id=consumer)


def test_legacy_manifest_still_parses_with_identical_bytes_and_content_fingerprint():
    _, manifest, _ = redacted_completed_result(redacted_snapshot_request())
    original = encode_source_batch_manifest_v1(manifest)
    assert b'"consumer_id"' not in original
    retained = SourceBatchManifestV1.model_validate_json(original)
    assert retained.identity.consumer_id is None
    assert encode_source_batch_manifest_v1(retained) == original
    assert publication_content_fingerprint_v1(retained) == manifest.content_fingerprint


async def test_owner_changes_content_and_cannot_cross_an_execution_or_revision_sequence():
    first = redacted_snapshot_request(consumer_id="buyer-a")
    second = redacted_snapshot_request(consumer_id="buyer-b")
    first_result, first_manifest, reader = redacted_completed_result(first)
    _, second_manifest, _ = redacted_completed_result(second)
    assert first_manifest.content_fingerprint != second_manifest.content_fingerprint
    with pytest.raises(ReportingSourceConformanceError, match="identity"):
        await validate_reporting_source_execution(
            capabilities=redacted_capabilities(),
            request=second,
            result=first_result,
            object_reader=reader,
        )
    with pytest.raises(ReportingSourceConformanceError):
        validate_reporting_revision_sequence([first_manifest, second_manifest])


async def test_same_config_and_period_have_consumer_specific_logical_slices_and_bindings():
    producer, store, _, clock = await _harness(_capabilities(restatement_window="P3D"))
    await producer.run_worker()
    obligation = await _only_obligation(store)
    configurations = await store.list_configurations(
        caller=ReportingStatusCaller(obligation.account_id, obligation.consumer_id)
    )
    configuration = configurations[0]
    other = replace(obligation, consumer_id="buyer-other")
    other_configuration = replace(configuration, consumer_id=other.consumer_id)
    requests = [
        producer._build_slice(
            config, record, producer._offerings.snapshot_offering_id, now=clock[0]
        )
        for config, record in [(configuration, obligation), (other_configuration, other)]
    ]
    assert requests[0].identity.consumer_id == obligation.consumer_id
    assert (
        requests[0].identity.logical_slice_fingerprint
        != requests[1].identity.logical_slice_fingerprint
    )
    acquisition = ProvisionalAcquisition(
        requests[0].model_dump_json(),
        0,
        ProvisionalPolicy(timedelta(days=3), timedelta(hours=1)),
    )
    assert acquisition.binds(obligation)
    assert not acquisition.binds(other)
    for owner in ["buyer-other", None]:
        request = requests[0].model_copy(
            update={"identity": requests[0].identity.model_copy(update={"consumer_id": owner})}
        )
        _, manifest, _ = redacted_completed_result(request)
        with pytest.raises(LedgerConflictError, match="manifest does not bind"):
            producer._validate_manifest_currency(obligation, manifest)
