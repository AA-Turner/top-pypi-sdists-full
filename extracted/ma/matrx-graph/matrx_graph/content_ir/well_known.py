"""The well-known kinds the ENGINE itself produces — declared once, reused.

THE RULE (KINDS_EVERYWHERE_PLAN §4.4): well-known kinds are seeded first so
shapes get REUSED, never re-minted under five names. Reinvention is a review
failure, not a style preference.

This module holds the tiny, universal shapes that more than one built-in node
answers with. Before it existed, ``text.join`` and ``data.stringify_json`` each
carried their own private ``{text: str}`` class while a THIRD hand-written copy
sat in the host's registry module under the slug they both declared — three
classes for one shape, and nothing keeping them equal.

WHY HERE AND NOT IN THE HOST. matrx-graph must stay importable on a bare
Postgres with nothing wired (package doctrine), so the MODEL lives with the
engine that constructs it and PUBLICATION stays host-side, where the DB
managers are. The host applies ``@kind`` to these classes rather than
redeclaring them — the split ``aidream/kinds/runtime.py`` established for the
runtime wrappers, for exactly the same reason.

Keep this set SMALL and closed. A shape belongs here only when several
built-ins genuinely produce the same thing; a node with a shape of its own
declares its own kind beside its executor, where its field descriptions can
say what that node means.
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field, JsonValue

from matrx_graph.content_ir.model import KindModel

__all__ = ["ItemsValue", "SingleValue", "TextValue"]


class TextValue(KindModel, kind="text"):
    """Plain text — the generic prose kind. One block, no rendering promise.

    Registered as ``text`` (family ``workflow_io``). Deliberately NOT
    ``markdown``: that slug promises a renderer a markdown document, and a
    joined list of parts or a JSON string is not one.
    """

    text: str


class ItemsValue(KindModel, kind="items"):
    """A list of things — THE input every generic list node consumes.

    Registered as ``items`` (family ``workflow_io``) since ``wf_013`` as a
    hand-seeded archetype row with no model in code, so the seven list nodes
    that declare ``input_kind="items"`` (``data.filter``, ``data.flatten``,
    ``data.dedupe``, ``data.sort``, ``data.limit``, ``data.batch``,
    ``data.aggregate``) could not be graded against it. This is that row's
    shape, field for field: ``archetype`` and ``count`` stay because the
    canonical ``Items`` payload (``matrx_graph.types.canonical_payloads``)
    emits them, and a consumer must accept what its producer sends.
    """

    archetype: Literal["items"] = "items"
    items: list[JsonValue] = Field(description="The elements, in order.")
    count: int = Field(
        default=-1,
        description="len(items); auto-derived when not provided.",
    )


class SingleValue(KindModel, kind="value"):
    """One JSON value — what ``data.parse_json``, ``data.parse_yaml`` and
    ``math.evaluate`` produce and what ``data.stringify_json`` and
    ``text.json_path`` consume.

    Registered as ``value`` (family ``workflow_io``) since ``wf_013``; this is
    that row's shape, and the canonical ``Value`` payload's.
    """

    archetype: Literal["value"] = Field(
        default="value",
        description="Canonical payload discriminator for a single computed value.",
    )
    value: JsonValue = Field(description="The computed value produced by the node.")
