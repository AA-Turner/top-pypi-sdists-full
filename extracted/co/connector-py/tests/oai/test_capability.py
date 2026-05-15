"""Tests for ``connector.oai.capability`` module.

Todo
----
* generate_capability_schema
"""

import typing as t

import pytest
import pytest_cases
from connector.oai.capability import (
    _STANDARD_CAPABILITY_SIGNATURES,
    CapabilityCallableProto,
    CustomRequest,
    CustomResponse,
    Request,
    Response,
    StandardCapabilityName,
    get_capability_annotations,
    validate_capability,
)
from connector_sdk_types.generated import (
    ExecutionSummary,
)
from connector_sdk_types.generated.models.updated_effect import UpdatedEffect

from .shared_types import SampleRequest, SampleResponse

Case: t.TypeAlias = tuple[
    CapabilityCallableProto[t.Any],
    tuple[type[Request], type[Response]],
]


@pytest_cases.parametrize_with_cases(
    ["capability", "expected_annotations"],
    cases=[
        "tests.oai.test_get_capability_annotations_cases",
    ],
    has_tag="correct",
)
async def test_get_capability_annotations(
    capability: CapabilityCallableProto[t.Any],
    expected_annotations: tuple[Request, Response],
) -> None:
    """Test if annotations are correctly get from capability."""
    actual_annotations = get_capability_annotations(capability)
    assert actual_annotations == expected_annotations


@pytest_cases.parametrize_with_cases(
    ["capability"],
    cases=[
        "tests.oai.test_get_capability_annotations_cases",
    ],
    has_tag="missing_annotation",
)
async def test_get_capability_annotations_type_error(
    capability: CapabilityCallableProto[t.Any],
) -> None:
    """Test if incorrectly typed capability raises error."""
    with pytest.raises(TypeError):
        get_capability_annotations(capability)


@pytest_cases.parametrize_with_cases(
    ["capability_name", "capability"],
    cases=[
        "tests.oai.test_validate_capability_cases",
    ],
    has_tag="valid",
)
async def test_validate_capability(
    capability_name: StandardCapabilityName,
    capability: CapabilityCallableProto[t.Any],
) -> None:
    """Test if valid capability is marked as valid."""
    validate_capability(capability_name, capability)


@pytest_cases.parametrize_with_cases(
    ["capability_name", "capability"],
    cases=[
        "tests.oai.test_validate_capability_cases",
    ],
    has_tag="invalid",
)
async def test_validate_capability_invalid(
    capability_name: StandardCapabilityName,
    capability: CapabilityCallableProto[t.Any],
) -> None:
    """Test if an invalid capability is marked as valid."""
    with pytest.raises(TypeError):
        validate_capability(capability_name, capability)


@pytest_cases.parametrize_with_cases(
    ["capability"],
    cases=[
        "tests.oai.test_get_capability_annotations_cases",
    ],
    has_tag="missing_annotation",
)
async def test_validate_capability_missing_annotation(
    capability: CapabilityCallableProto[t.Any],
) -> None:
    """Test if valid capability is marked as valid.

    We just pass any capability_name just to make function happy,
    however, ``validate_capability`` should raise before it touches the
    name.
    """
    capability_name = StandardCapabilityName.VALIDATE_CREDENTIALS
    with pytest.raises(TypeError):
        validate_capability(capability_name, capability)


async def test_standard_capability_signatures_exhaustive() -> None:
    """
    Test if all standard capability signatures are exhaustively
    covered in _STANDARD_CAPABILITY_SIGNATURES
    """
    for capability_name in StandardCapabilityName:
        if capability_name == StandardCapabilityName.INFO:
            # INFO is a special case as it is not manually registered
            continue
        if capability_name == StandardCapabilityName.CONNECTED_INFO:
            # CONNECTED_INFO is a special case as it is not manually registered
            continue
        if capability_name == StandardCapabilityName.APP_INFO:
            # APP_INFO is a special case as it is not manually registered
            continue
        signature = _STANDARD_CAPABILITY_SIGNATURES.get(capability_name)
        assert (
            signature is not None
        ), f"Standard capability signature for {capability_name} is not found"


def test_custom_response_execution_summary_defaults_to_none() -> None:
    """execution_summary should be optional and default to None"""
    response = CustomResponse(response=SampleResponse(success=True))
    assert response.execution_summary is None


def test_custom_response_execution_summary_can_be_set() -> None:
    """execution_summary should be settable with an ExecutionSummary object"""
    summary = ExecutionSummary(
        effect=UpdatedEffect(),
        is_idempotent=True,
        request_fingerprint="abc123",
    )
    response = CustomResponse(response=SampleResponse(success=True), execution_summary=summary)
    assert response.execution_summary == summary


def test_custom_request_fingerprint_only_encodes_request() -> None:
    """fingerprint only works for the request, other parameters do not affect it"""
    request_1 = CustomRequest(
        request=SampleRequest(account_id="123"), settings={"domain": "example.com"}
    )
    request_2 = CustomRequest(
        request=SampleRequest(account_id="123"), settings={"domain": "other.com"}
    )
    assert request_1.fingerprint() == request_2.fingerprint()


def test_custom_request_fingerprint_differs_for_different_requests() -> None:
    """different request payloads should produce different fingerprints"""
    request_1 = CustomRequest(request=SampleRequest(account_id="123"), settings={})
    request_2 = CustomRequest(request=SampleRequest(account_id="456"), settings={})
    assert request_1.fingerprint() != request_2.fingerprint()
