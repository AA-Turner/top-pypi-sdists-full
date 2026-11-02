"""A public canonical model enforces every validator its generated source declares.

The canonical models are real subclasses of the generated classes they refine, so a
validator declared on the generated class body — the root-level required groups
``enforce_root_required_groups`` emits (#1361), the uniqueness and pairing checks other
post-generation fixes inject — reaches the public name by inheritance. These tests hold
the consequence: a document the generated class refuses, the public name refuses too.

They used to hold the same obligation over a different mechanism. The canonical models
were built with ``create_model`` over a copy of the source's fields, which left the
generated class out of the MRO, so each validator had to be re-decorated onto the copy
and any validator touching a dropped field was skipped and recorded. Both the carrying
and the skip list are gone: there is one mechanism, and nothing to forget. The tests
below are the same obligations re-pointed at it, and two of them are strictly stronger
for it — ``test_no_generated_validator_is_skipped`` admits no exceptions where the skip
list was an allowed set, and
``test_canonical_manifest_enforces_its_required_group_through_format_kind`` asserts a
refusal where the clone accepted the document.
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

import adcp
from adcp.types import canonical_creative

_REQUIRED_GROUP_VALIDATOR = "_require_schema_required_group"


def _generated_ancestors(model: type[BaseModel]) -> list[type[BaseModel]]:
    """The generated classes ``model`` descends from, nearest first."""
    return [
        base
        for base in model.__mro__[1:]
        if isinstance(base, type)
        and issubclass(base, BaseModel)
        and base.__module__.startswith("adcp.types.domains")
    ]


def _canonical_models() -> dict[str, type[BaseModel]]:
    """Every model in ``canonical_creative`` that refines a generated class.

    Broader than ``PRIMARY_CANONICAL_MODELS`` in
    ``tests/test_canonical_models_are_subclasses.py``, which is the 31 publicly bound
    models: this population also carries the private ``_Legacy*`` and ``_Delivery*``
    refinements, because a validator dropped on one of those is just as silent.
    """
    return {
        name: obj
        for name, obj in vars(canonical_creative).items()
        if isinstance(obj, type) and issubclass(obj, BaseModel) and _generated_ancestors(obj)
    }


def _own_validators(model: type[BaseModel]) -> set[str]:
    """Validators ``model`` declares on its own body, both decorator kinds.

    Only own-body validators are interesting: an inherited one reaches the public model
    through the same MRO this file is about.
    """
    decorators = model.__pydantic_decorators__
    own = vars(model)
    return {
        name for name in (*decorators.model_validators, *decorators.field_validators) if name in own
    }


def _all_validators(model: type[BaseModel]) -> set[str]:
    decorators = model.__pydantic_decorators__
    return {*decorators.model_validators, *decorators.field_validators}


def test_the_canonical_model_population_is_not_empty() -> None:
    """Anti-vacuity floor: every loop below is over this mapping."""
    models = _canonical_models()
    assert len(models) >= 31, len(models)
    assert "CreateMediaBuyRequest" in models
    assert "CreativeManifest" in models


def test_every_generated_validator_reaches_the_public_model() -> None:
    """Both decorator kinds, over every refinement, with no exceptions permitted.

    Field validators are included deliberately even though no generated ancestor
    declares one today: the clone mechanism would have had to carry them too, and an
    assertion that only covers the kind that currently exists stops grading the moment
    a post-generation fix emits the other.
    """
    missing: dict[str, set[str]] = {}
    for name, model in _canonical_models().items():
        wanted: set[str] = set()
        for ancestor in _generated_ancestors(model):
            wanted |= _own_validators(ancestor)
        absent = wanted - _all_validators(model)
        if absent:
            missing[name] = absent
    assert not missing, f"public canonical models do not carry generated validators: {missing}"


def test_no_generated_validator_is_skipped() -> None:
    """There is no skip list, and a validator reading a removed field is why there was one.

    A canonical model drops the legacy creative identity fields, so a rule written
    against ``format_id`` inherits down onto a class that does not declare it. The
    removal rule binds each removed name to ``None`` after class creation, so the read
    resolves and the rule reduces rather than being skipped — which is what lets this
    test admit no exceptions at all.
    """
    for name, model in _canonical_models().items():
        for ancestor in _generated_ancestors(model):
            for validator in _own_validators(ancestor):
                assert validator in _all_validators(model), (name, ancestor.__name__, validator)


def test_canonical_manifest_enforces_its_required_group_through_format_kind() -> None:
    """``format_id | format_kind`` reaches the public manifest, satisfied by the surviving arm.

    ``core/creative-manifest.json`` declares the group, and the canonical boundary has
    no ``format_id`` to satisfy it with. Under the clone this validator was skipped and
    ``{"assets": {}}`` validated; it is now inherited, so the public name refuses the
    document its generated source refuses and accepts it through ``format_kind``.
    """
    manifest = canonical_creative.CreativeManifest
    assert _REQUIRED_GROUP_VALIDATOR in manifest.__pydantic_decorators__.model_validators
    assert "format_id" not in manifest.model_fields

    with pytest.raises(ValidationError, match="at least one of these field groups"):
        manifest.model_validate({"assets": {}})

    accepted = manifest.model_validate({"assets": {}, "format_kind": "image"})
    assert accepted.format_kind is not None


def test_before_validators_keep_their_classmethod_binding() -> None:
    """A ``before`` validator is stored as a classmethod and must stay one.

    The clone re-decorated the class namespace rather than ``Decorator.func`` because
    the unwrapped function has already lost its ``cls`` binding; inheritance has no
    such hazard, and this holds that the binding survives on both classes.
    """
    from adcp.types import Product
    from adcp.types.domains.core.product import Product as Generated

    assert "_coerce_publisher_property_models" in Product.__pydantic_decorators__.model_validators
    assert "_coerce_publisher_property_models" in Generated.__pydantic_decorators__.model_validators


def test_required_group_validators_reach_the_canonical_names() -> None:
    """The gap #1368 documented: the generated class rejected, the public name accepted."""
    with_groups = {
        name: model
        for name, model in _canonical_models().items()
        if any(
            _REQUIRED_GROUP_VALIDATOR in _own_validators(ancestor)
            for ancestor in _generated_ancestors(model)
        )
    }
    assert "CreateMediaBuyRequest" in with_groups
    for name, model in with_groups.items():
        assert _REQUIRED_GROUP_VALIDATOR in model.__pydantic_decorators__.model_validators, name


_MEDIA_BUY_UNCONDITIONAL_FIELDS: dict[str, Any] = {
    "idempotency_key": "idem-key-0123456789",
    "account": {"account_id": "acct_1"},
    "brand": {"brand_id": "brand_1", "domain": "example.com"},
    "start_time": "2026-11-01T00:00:00Z",
    "end_time": "2026-11-30T00:00:00Z",
}


@pytest.mark.parametrize(
    "model",
    [adcp.CreateMediaBuyRequest, canonical_creative.CreateMediaBuyRequest],
    ids=["adcp", "canonical_creative"],
)
def test_canonical_create_media_buy_request_requires_one_root_anyof_group(
    model: type[BaseModel],
) -> None:
    """A media buy with no packages, no budget and no proposal is refused on every path.

    ``create-media-buy-request.json`` declares the three ways to be a media buy as a
    root ``anyOf``. The generated class gained the rule in #1368; this is the controlled
    probe that showed the public canonical name still accepted the document, held green.
    """
    ancestors = _generated_ancestors(model)
    assert ancestors, model.__name__
    source = ancestors[0]
    with pytest.raises(ValidationError, match="at least one of these field groups"):
        source.model_validate(dict(_MEDIA_BUY_UNCONDITIONAL_FIELDS))
    with pytest.raises(ValidationError, match="at least one of these field groups"):
        model.model_validate(dict(_MEDIA_BUY_UNCONDITIONAL_FIELDS))

    committed = model.model_validate(
        {
            **_MEDIA_BUY_UNCONDITIONAL_FIELDS,
            "proposal_id": "prop_1",
            "total_budget": {"amount": 1000.0, "currency": "USD"},
        }
    )
    assert committed.proposal_id == "prop_1"  # type: ignore[attr-defined]
    assert committed.packages is None  # type: ignore[attr-defined]


def test_canonical_model_keeps_the_boundary_validator_alongside_the_inherited_ones() -> None:
    """Inheriting source validators must not displace the boundary's own."""
    model = canonical_creative.CreateMediaBuyRequest
    validators = model.__pydantic_decorators__.model_validators
    assert "_reject_legacy_creative_identity" in validators
    assert _REQUIRED_GROUP_VALIDATOR in validators
    with pytest.raises(ValidationError, match="legacy creative identity"):
        model.model_validate(
            {
                **_MEDIA_BUY_UNCONDITIONAL_FIELDS,
                "packages": [
                    {
                        "buyer_ref": "pkg_1",
                        "product_id": "prod_1",
                        "format_ids": [{"agent_url": "https://x.example", "id": "f"}],
                    }
                ],
            }
        )
