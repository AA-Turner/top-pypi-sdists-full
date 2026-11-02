"""Runtime contracts retained by post-generation compatibility fixes."""

from __future__ import annotations

import json

import pytest
from pydantic import BaseModel, ValidationError


def test_response_dispatch_omits_newer_pydantic_keywords_at_their_defaults() -> None:
    from adcp.types.response_dispatch import _model_validate_json_kwargs, _model_validate_kwargs

    assert _model_validate_kwargs(
        strict=None,
        extra=None,
        from_attributes=None,
        context=None,
        by_alias=None,
        by_name=None,
    ) == {"strict": None, "from_attributes": None, "context": None}
    assert _model_validate_kwargs(
        strict=True,
        extra="forbid",
        from_attributes=True,
        context={"trace_id": "trace_1"},
        by_alias=True,
        by_name=False,
    ) == {
        "strict": True,
        "extra": "forbid",
        "from_attributes": True,
        "context": {"trace_id": "trace_1"},
        "by_alias": True,
        "by_name": False,
    }
    assert _model_validate_json_kwargs(
        strict=None,
        extra=None,
        context=None,
        by_alias=None,
        by_name=None,
    ) == {"strict": None, "context": None}


def test_product_signal_targeting_option_keeps_discriminated_signal_ref() -> None:
    from typing import get_args

    from adcp import ProductSignalTargetingOption
    from adcp.types.domains.core.signal_ref import SignalRef

    # SignalRef is Annotated[SignalRef1 | SignalRef2 | SignalRef3, Field(...)];
    # Pydantic lifts the metadata into FieldInfo and keeps the union.
    arms, metadata = get_args(SignalRef)
    assert ProductSignalTargetingOption.model_fields["signal_ref"].annotation is arms
    assert metadata.discriminator == "scope"
    assert ProductSignalTargetingOption.model_json_schema()["properties"]["signal_ref"][
        "description"
    ].startswith("Canonical signal reference.")

    option = ProductSignalTargetingOption.model_validate(
        {"signal_ref": {"scope": "product", "signal_id": "signal_1"}}
    )
    assert isinstance(option.signal_ref, get_args(arms))
    assert option.signal_ref.scope == "product"

    with pytest.raises(ValidationError) as unknown_scope:
        ProductSignalTargetingOption.model_validate(
            {"signal_ref": {"scope": "unknown", "signal_id": "signal_1"}}
        )
    assert [error["type"] for error in unknown_scope.value.errors()] == ["union_tag_invalid"]

    with pytest.raises(ValidationError):
        ProductSignalTargetingOption.model_validate({"signal_ref": "signal_1"})


def test_creative_representation_keeps_canonical_format_contract() -> None:
    from adcp import LegacyBuildCreativeRequest
    from adcp.types import CanonicalFormatKind
    from adcp.types.domains.core.creative_representation import CreativeRepresentation

    # ``str``, not the enum: the vocabulary is open at every reference and
    # governed by a validator on the request models. Asserting membership of
    # the generated enum here keeps the vocabulary itself in the test.
    assert CreativeRepresentation.model_fields["format_kind"].annotation is str
    assert "image" in {kind.value for kind in CanonicalFormatKind}
    schema = CreativeRepresentation.model_json_schema()
    assert schema["properties"]["format_kind"]["description"].startswith("Canonical 3.2 path.")
    assert schema["not"] == {
        "anyOf": [
            {"required": ["format_id"]},
            {"required": ["format_option_ref"]},
            {"required": ["representation_selection"]},
        ]
    }

    representation = {
        "representation_id": "representation_1",
        "source": {"system": "test", "source_representation": "source_1"},
        "format_kind": "image",
        "assets": {},
    }
    parsed_representation = CreativeRepresentation.model_validate(representation)
    assert parsed_representation.format_kind == CanonicalFormatKind.image

    # ``CreativeRepresentation`` carries the open vocabulary, like every other
    # model in this SDK: an unknown kind is retained rather than refused, in
    # either direction. Checking the vocabulary is the caller's, through
    # ``adcp.types.is_canonical_format_kind``.
    unknown = CreativeRepresentation.model_validate({**representation, "format_kind": "unknown"})
    assert unknown.format_kind == "unknown"

    for seller_bound_field in ("format_id", "format_option_ref", "representation_selection"):
        with pytest.raises(ValidationError):
            # JSON Schema's ``required`` considers a key present even when null.
            CreativeRepresentation.model_validate({**representation, seller_bound_field: None})

    representation_set = {
        "creative_id": "creative_1",
        "revision_id": "revision_1",
        "revision_content_digest": "sha256:" + "0" * 64,
        "name": "Test creative",
        "representations": [{**representation, "format_kind": "unknown"}],
    }
    # ``LegacyBuildCreativeRequest`` is a request model and it too retains the
    # unknown kind rather than refusing it: no model in this SDK refuses a
    # format kind, because a pinned library cannot tell a kind a seller
    # invented from a kind defined after its pin. That is the one cost of the
    # open vocabulary, and it is declared
    # by name in ``tests/conformance/_schema_parity.py``'s
    # ``format_kind_is_an_open_vocabulary_by_decision`` — the bundled schema
    # still refuses this document, and the model no longer agrees. Retention is
    # asserted at the nested position so the claim is graded rather than implied.
    built = LegacyBuildCreativeRequest.model_validate(
        {
            "idempotency_key": "idem-123456789012",
            "creative_representation_set": representation_set,
        }
    )
    assert built.creative_representation_set.representations[0].format_kind == "unknown"


def test_transformer_requires_a_canonical_or_legacy_output_declaration() -> None:
    from adcp.types import ListTransformersResponse
    from adcp.types.domains.core.transformer import Transformer

    base_transformer = {"transformer_id": "transformer_1", "name": "Test transformer"}
    with pytest.raises(ValidationError):
        ListTransformersResponse.model_validate({"transformers": [base_transformer]})

    assert (
        Transformer.model_validate(
            {**base_transformer, "output_capability_ids": ["capability_1"]}
        ).output_capability_ids
        is not None
    )
    assert (
        Transformer.model_validate(
            {
                **base_transformer,
                "output_format_ids": [{"agent_url": "https://creative.example", "id": "format_1"}],
            }
        ).model_dump()["output_format_ids"]
        is not None
    )


def test_public_response_bases_remain_constructible_and_arms_remain_specific() -> None:
    from adcp.types import (
        ComplyTestControllerResponse,
        CreateContentStandardsResponse,
        ListContentStandardsResponse,
        SyncGovernanceResponse,
        UpdateContentStandardsResponse,
    )
    from adcp.types.aliases import (
        ComplyListScenariosResponse,
        CreateContentStandardsSuccessResponse,
        ListContentStandardsSuccessResponse,
        UpdateContentStandardsSuccessResponse,
    )
    from adcp.types.domains.account.sync_governance_response import SyncGovernanceResponse1
    from adcp.types.domains.compliance.comply_test_controller_response import (
        ComplyTestControllerResponse1,
    )
    from adcp.types.domains.content_standards.create_content_standards_response import (
        CreateContentStandardsResponse1,
    )
    from adcp.types.domains.content_standards.list_content_standards_response import (
        ListContentStandardsResponse1,
    )
    from adcp.types.domains.content_standards.update_content_standards_response import (
        UpdateContentStandardsResponse1,
    )
    from adcp.utils.response_parser import parse_json_or_text

    responses = (
        (
            ComplyTestControllerResponse,
            ComplyListScenariosResponse,
            ComplyTestControllerResponse1,
            {"success": True, "scenarios": []},
            {"success": True},
            {"success": "invalid"},
            {"scenarios": []},
        ),
        (
            CreateContentStandardsResponse,
            CreateContentStandardsSuccessResponse,
            CreateContentStandardsResponse1,
            {"standards_id": "standards_1"},
            {},
            {},
            {"standards_id": "standards_1"},
        ),
        (
            ListContentStandardsResponse,
            ListContentStandardsSuccessResponse,
            ListContentStandardsResponse1,
            {"standards": []},
            {},
            {},
            {"standards": []},
        ),
        (
            SyncGovernanceResponse,
            SyncGovernanceResponse1,
            SyncGovernanceResponse1,
            {"accounts": []},
            {},
            {},
            {"accounts": []},
        ),
        (
            UpdateContentStandardsResponse,
            UpdateContentStandardsSuccessResponse,
            UpdateContentStandardsResponse1,
            {"success": True, "standards_id": "standards_1"},
            {"success": False, "standards_id": "standards_1"},
            {"success": False, "standards_id": "standards_1"},
            {"standards_id": "standards_1"},
        ),
    )

    for (
        response_base,
        response_alias,
        response_arm,
        valid,
        invalid_arm,
        invalid_base,
        preserved_fields,
    ) in responses:
        assert issubclass(response_base, BaseModel)
        assert isinstance(response_base(), response_base)
        assert response_alias is response_arm
        assert issubclass(response_arm, response_base)
        assert isinstance(response_alias.model_validate(valid), response_base)

        direct = response_base.model_validate(valid)
        direct_json = response_base.model_validate_json(json.dumps(valid))
        parsed = parse_json_or_text(valid, response_base)
        for result in (direct, direct_json, parsed):
            assert type(result) is response_arm
            assert all(getattr(result, name) == value for name, value in preserved_fields.items())

        empty_base = response_base()
        assert response_base.model_validate(empty_base) is empty_base

        with pytest.raises(ValidationError):
            response_alias.model_validate(invalid_arm)
        with pytest.raises(ValidationError):
            response_base.model_validate(invalid_base)
        with pytest.raises(ValueError):
            parse_json_or_text(invalid_base, response_base)


_MEDIA_BUY_UNCONDITIONAL_FIELDS = {
    "idempotency_key": "idem-key-0123456789",
    "account": {"account_id": "acct_1"},
    "brand": {"brand_id": "brand_1", "domain": "example.com"},
    "start_time": "2026-11-01T00:00:00Z",
    "end_time": "2026-11-30T00:00:00Z",
}


def test_create_media_buy_request_requires_one_root_anyof_group() -> None:
    """``create-media-buy-request.json`` declares three ways to be a media buy.

    Root ``required`` names the five fields every arm shares; the root ``anyOf``
    names the three groups, one of which a request has to carry. A document with
    the five and none of the three is a media buy with no packages, no budget and
    no proposal.
    """
    from adcp.types.domains.media_buy.create_media_buy_request import CreateMediaBuyRequest

    with pytest.raises(ValidationError, match="at least one of these field groups"):
        CreateMediaBuyRequest.model_validate(dict(_MEDIA_BUY_UNCONDITIONAL_FIELDS))

    committed = CreateMediaBuyRequest.model_validate(
        {
            **_MEDIA_BUY_UNCONDITIONAL_FIELDS,
            "proposal_id": "prop_1",
            "total_budget": {"amount": 1000.0, "currency": "USD"},
        }
    )
    assert committed.proposal_id == "prop_1"
    assert committed.packages is None


def test_sync_creatives_request_takes_assignment_operations_without_creatives() -> None:
    """``creatives`` is one arm of a root ``anyOf``, not an unconditional field.

    AdCP 3.2 moved ``creatives`` out of root ``required`` into a group alongside
    ``assignments`` and ``assignment_operations``, so a request that traffics
    existing creative IDs carries no ``creatives`` at all.
    """
    from adcp.types.domains.creative.sync_creatives_request import SyncCreativesRequest

    base = {"idempotency_key": "idem-key-0123456789", "account": {"account_id": "acct_1"}}

    with pytest.raises(ValidationError, match="at least one of these field groups"):
        SyncCreativesRequest.model_validate(dict(base))

    assignments_only = SyncCreativesRequest.model_validate(
        {
            **base,
            "assignment_operations": [
                {"operation": "assign", "creative_id": "creative_1", "package_id": "package_1"}
            ],
        }
    )
    assert assignments_only.creatives is None
    assert assignments_only.assignment_operations is not None
