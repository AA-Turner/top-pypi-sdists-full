"""The ingestion gate — the audit's hard problem 2, closed by construction.

Self-described payloads (``__kind`` in the data) flow into node inputs. The
law (plan §4, workflow design station 3): identity TRAVELS by default; the
marker is removed only at positions where the receiving schema would fatally
reject it — an explicitly closed object (``extra="forbid"``) that does not
declare the discriminator. So a legacy strict model can never fatal on the
platform's own marker, and a kind-aware receiver keeps the identity.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from matrx_graph.content_ir.markers import reduce_for_ingestion
from matrx_graph.content_ir.model import KindModel


class Rating(KindModel, kind="rating"):
    value: float


class LegacyStrictInput(BaseModel):
    """The pre-kinds world: extra='forbid', no discriminator declared."""

    model_config = ConfigDict(extra="forbid")

    text: str
    score: float = 0.0


class KindAwareInput(BaseModel):
    """A receiver with a KindModel arg — the discriminator is declared there."""

    model_config = ConfigDict(extra="forbid")

    rating: Rating


class OpenInput(BaseModel):
    """A generic receiver: dict arg, schema open at that position."""

    payload: dict


def test_marker_never_fatals_a_legacy_strict_model() -> None:
    # The exact fatal-at-the-door case: upstream settled a self-described
    # payload; the receiver is closed and knows nothing of kinds.
    incoming = {"text": "hello", "score": 1.0, "__kind": "note"}
    reduced = reduce_for_ingestion(incoming, LegacyStrictInput.model_json_schema())
    model = LegacyStrictInput.model_validate(reduced)  # would raise pre-gate
    assert model.text == "hello"
    assert "__kind" not in reduced


def test_kind_model_arg_keeps_its_identity() -> None:
    incoming = {"rating": {"__kind": "rating", "value": 4.5}}
    reduced = reduce_for_ingestion(incoming, KindAwareInput.model_json_schema())
    model = KindAwareInput.model_validate(reduced)
    assert model.rating.kind_slug == "rating"
    assert reduced["rating"]["__kind"] == "rating"


def test_open_positions_pass_identity_through_untouched() -> None:
    # A generic dict arg (and anything schema-unknown) is OPEN: the marker is
    # harmless there and identity must travel — the kind-filtered-edge case.
    incoming = {
        "payload": {
            "__kind": "web_search_results",
            "web": [{"__kind": "web_result", "url": "https://a"}],
        }
    }
    reduced = reduce_for_ingestion(incoming, OpenInput.model_json_schema())
    assert reduced["payload"]["__kind"] == "web_search_results"
    assert reduced["payload"]["web"][0]["__kind"] == "web_result"
    OpenInput.model_validate(reduced)


def test_schema_free_reduction_keeps_everything() -> None:
    # No schema at all = no forbidding position = nothing removed. The
    # one-shape default, and the opposite of strip_kind_markers' doctrine.
    incoming = {"__kind": "rating", "value": 4.0}
    assert reduce_for_ingestion(incoming, None) == incoming


def test_nested_forbidding_position_is_reduced_only_there() -> None:
    class Inner(BaseModel):
        model_config = ConfigDict(extra="forbid")
        name: str

    class Mixed(BaseModel):
        inner: Inner
        blob: dict

    incoming = {
        "inner": {"name": "x", "__kind": "person"},
        "blob": {"__kind": "person", "name": "y"},
    }
    reduced = reduce_for_ingestion(incoming, Mixed.model_json_schema())
    assert "__kind" not in reduced["inner"]  # closed, undeclared → reduced
    assert reduced["blob"]["__kind"] == "person"  # open → identity travels
    Mixed.model_validate(reduced)


def test_idempotent() -> None:
    incoming = {"text": "t", "__kind": "note"}
    schema = LegacyStrictInput.model_json_schema()
    once = reduce_for_ingestion(incoming, schema)
    assert reduce_for_ingestion(once, schema) == once
