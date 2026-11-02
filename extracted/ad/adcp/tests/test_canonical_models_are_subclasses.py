"""A canonical public model is a SUBCLASS of the generated wire model (#1368).

The canonical layer used to build its 32 public classes with ``create_model``,
copying ``model_fields`` off the generated model and inheriting nothing from it.
That is why PR #1368's injected ``enforce_root_required_groups`` validator
reached the generated class and never the public one — the blocking review
finding on that PR. ARCH-ONE-SURFACE §6 refuses a second injection mechanism
for the copy layer ("it fixes the finding by doubling the thing that caused
it"), so the copy is gone instead.

These tests grade the replacement as a property rather than as a diff:

* every public canonical model descends from a generated wire model;
* every ``model_validator`` the generated model declares is present on the
  public model — which is the #1368 contract, stated for ALL validators rather
  than for one;
* the two concerns the copy had to re-attach per class (the boundary's
  ``extra="allow"`` and the legacy-identity strip) still hold.

Reverting any canonical model to a copy fails the first test, because
``create_model`` stamps the calling module onto what it builds and the copy has
no generated ancestor at all.
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel

from adcp.types import canonical_creative
from adcp.types.canonical_creative import (
    PRIMARY_CANONICAL_MODELS,
    CanonicalBoundaryModel,
    is_legacy_creative_identity_key,
)

_GENERATED_PREFIX = "adcp.types.domains."

#: ``Format`` is the one canonical model with no generated counterpart: it is
#: hand-written from the canonical format declaration and declares its own
#: fields. Everything else refines a generated wire model.
_HAND_WRITTEN = {"Format"}


def _generated_ancestors(model: type[BaseModel]) -> list[type[BaseModel]]:
    return [
        base
        for base in model.__mro__
        if base.__module__.startswith(_GENERATED_PREFIX) and issubclass(base, BaseModel)
    ]


def _ids(models: tuple[type[BaseModel], ...]) -> list[str]:
    return [model.__name__ for model in models]


def test_the_canonical_model_list_is_not_empty() -> None:
    """A later refactor must not satisfy these tests by emptying the list."""
    assert len(PRIMARY_CANONICAL_MODELS) == 31


@pytest.mark.parametrize("model", PRIMARY_CANONICAL_MODELS, ids=_ids(PRIMARY_CANONICAL_MODELS))
def test_every_canonical_model_descends_from_a_generated_model(model: type[BaseModel]) -> None:
    """The anti-copy property, stated structurally."""
    if model.__name__ in _HAND_WRITTEN:
        pytest.skip(f"{model.__name__} has no generated counterpart")
    ancestors = _generated_ancestors(model)
    assert ancestors, (
        f"{model.__name__} has no generated ancestor — it is a copy, not a "
        f"refinement. MRO: {[base.__name__ for base in model.__mro__]}"
    )


@pytest.mark.parametrize("model", PRIMARY_CANONICAL_MODELS, ids=_ids(PRIMARY_CANONICAL_MODELS))
def test_every_generated_validator_reaches_the_public_model(model: type[BaseModel]) -> None:
    """#1368's contract, for every validator rather than for one.

    A validator injected into a generated class by a generation pass — which is
    what ``enforce_root_required_groups`` is — must be live on the public model
    an adopter imports. Pydantic carries inherited decorators on the subclass's
    ``__pydantic_decorators__``, so the subclass's validator set is a superset
    of each generated ancestor's. A copy's is disjoint.
    """
    if model.__name__ in _HAND_WRITTEN:
        pytest.skip(f"{model.__name__} has no generated counterpart")
    public = set(model.__pydantic_decorators__.model_validators)
    for ancestor in _generated_ancestors(model):
        inherited = set(ancestor.__pydantic_decorators__.model_validators)
        assert inherited <= public, (
            f"{model.__name__} lost {sorted(inherited - public)} declared on its "
            f"generated ancestor {ancestor.__name__}"
        )


@pytest.mark.parametrize("model", PRIMARY_CANONICAL_MODELS, ids=_ids(PRIMARY_CANONICAL_MODELS))
def test_every_canonical_model_declares_no_legacy_identity(model: type[BaseModel]) -> None:
    """Inheritance brings the legacy fields along; the one declared rule removes them."""
    leaked = [name for name in model.model_fields if is_legacy_creative_identity_key(name)]
    assert leaked == [], f"{model.__name__} declares legacy creative identity: {leaked}"


@pytest.mark.parametrize("model", PRIMARY_CANONICAL_MODELS, ids=_ids(PRIMARY_CANONICAL_MODELS))
def test_every_canonical_model_keeps_the_boundary_policy(model: type[BaseModel]) -> None:
    """``CanonicalBoundaryModel`` is the LAST base, so its config wins the merge."""
    assert issubclass(model, CanonicalBoundaryModel), model.__name__
    assert model.model_config["extra"] == "allow", model.__name__


@pytest.mark.parametrize("model", PRIMARY_CANONICAL_MODELS, ids=_ids(PRIMARY_CANONICAL_MODELS))
def test_every_canonical_model_runs_the_wrap_serializer(model: type[BaseModel]) -> None:
    """The strip serializer is declared once on the boundary and inherited.

    It used to be re-attached per class through ``create_model``'s
    ``__validators__``; a class the copy helper missed would serialize legacy
    identity from a nested ``TypeAdapter`` path.
    """
    serializers = model.__pydantic_decorators__.model_serializers
    assert "_serialize_canonical" in serializers, model.__name__


def test_the_removal_rule_is_declared_once_and_derived() -> None:
    """The strip predicate has one owner, and the rule reads it.

    Four behaviors strip legacy identity — input rejection, JSON-schema
    sanitation, serialization, and now the declared-field removal — and all
    four call ``is_legacy_creative_identity_key``. A second spelling of the
    key list is the drift channel this asserts shut.
    """

    class Probe(canonical_creative.Package):
        pass

    assert "format_ids" not in Probe.model_fields
    assert "format_ids" in _generated_ancestors(Probe)[0].model_fields


def test_an_inherited_validator_that_reads_a_removed_field_still_works() -> None:
    """The one interaction between inheritance and the removal rule.

    ``list-creatives-response.json`` carries an injected
    ``_validate_format_reference_xor`` that reads ``self.format_id``. Inheritance
    is the point of this layer, so that validator now runs on the canonical
    model — and with the field merely deleted it raised ``AttributeError``
    instead of validating. The removal binds the name to ``None``, which is the
    removal's own truth, and the XOR then reduces to the invariant the canonical
    model should hold: ``format_kind`` must be set.

    Both directions are graded, because a reduced invariant that accepts
    everything is not an invariant.
    """
    import pytest as _pytest
    from pydantic import ValidationError

    from adcp.types import CanonicalFormatKind

    row = {
        "creative_id": "creative-1",
        "name": "Image",
        "format_kind": "image",
        "status": "approved",
        "created_date": "2026-09-01T00:00:00Z",
        "updated_date": "2026-09-01T00:00:00Z",
    }
    accepted = canonical_creative.Creative.model_validate(row)
    assert accepted.format_kind == CanonicalFormatKind.image
    assert "format_id" not in canonical_creative.Creative.model_fields
    assert accepted.format_id is None

    with _pytest.raises(ValidationError):
        canonical_creative.Creative.model_validate(
            {k: v for k, v in row.items() if k != "format_kind"}
        )
