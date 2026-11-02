"""Kind Directives — the grammar, the shell, and the position law.

ONE system (Arman, 2026-08-23): the Matrx Envelope/Directive protocol and the
Content IR kind system were *"always meant to be just one system"* and the split
was a terminology accident. This module is where the merge is structural. It is
PURE — no I/O, no DB, no aidream import — so the grammar can be parsed anywhere
a kind can, including inside matrx-graph's own engine.

Source of record: ``docs/protocol/KIND_DIRECTIVES.md``; doctrine:
``common-docs/policies/strictness-law.md``.
Protocol doc: aidream ``docs/protocol/KIND_DIRECTIVES.md``.

THE WIRE SHAPE
--------------
::

    { "__kind": "directive_v1_create_task", "items": [ { ...one item... } ] }

Two keys, and ``__kind`` is the FIRST one. That is not cosmetic: an unfenced
JSON document is typed early by its first key alone
(``block_detector._extract_first_json_key``), so a directive with ``__kind``
first routes through the SAME skeleton→fill→component path as every other kind
instance. The retired 4-key shell (``matrx_version``/``kind``/``type``/``items``)
announced itself with a version integer that nothing ever compared, and it took
a second detector, a second registry axis, and a second render dispatch to
carry it. ``items`` stays because batch semantics are load-bearing — the
per-item ledger, the per-item receipt, and partial-batch retry all key on it.

THE SLUG GRAMMAR — a routing language
-------------------------------------
``directive_v<version>_<class>_<noun>``

* ``directive_v`` is a RESERVED prefix. A hand-authored or user-created kind may
  never start with it (enforced in ``@kind``, in kind authoring, in the FE shape
  creator, and by the collision guard). Under this rule the whole namespace
  collision class the old registry lived with dissolves structurally: the kind
  ``transcript`` and the directive ``directive_v1_reference_transcript`` cannot
  be the same string, so there is nothing left to grandfather.
* ``<class>`` comes from a CLOSED vocabulary (:data:`CLASSES`), which is what
  makes parsing unambiguous even though nouns contain underscores: the class is
  always the first ``_``-delimited token after the prefix, so
  ``directive_v1_reference_create_task`` is unambiguously
  ``(reference, "create_task")`` and never ``(create, ...)``. The mapping
  ``(class, noun) → slug`` is injective for the same reason.
* ``<noun>`` is an enrolled ``platform.entity_types`` token (``task``,
  ``note``, …) or a declared name. Kind Actions carry class ``action``
  (``directive_v1_action_plan_tree``); validators class ``validation``
  (``directive_v1_validation_regex``); secrets class ``secret``.
* CAPABILITY IS DERIVED FROM THE CLASS, never stored twice
  (:data:`CAPABILITY_BY_CLASS`), and the position law keys on the class.
* ``v1`` replaces the old ``matrx_version`` field. Bump only on a breaking
  change to the shell-or-item contract of that shape.

THE POSITION LAW LIVES HERE, ONCE
---------------------------------
Before the merge the same law was written in FOUR places over THREE different
kind sets (the output dispatcher's ``_EXECUTING_KINDS``, the reference
substituter's ``IN_CONTENT_KINDS``, the confirm endpoint's tuple, and the
grooming gate's tuple) — three chances to disagree about what a position means.
Now there are exactly two predicates, :func:`executes_at_output_root` and
:func:`resolves_in_content`, and every caller asks one of them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.content_ir.envelope import KIND_KEY

__all__ = [
    "CAPABILITY_BY_CLASS",
    "CLASSES",
    "DIRECTIVE_VERSION",
    "IN_CONTENT_CLASSES",
    "KIND_KEY",
    "KindDirective",
    "RESERVED_PREFIX",
    "SIDE_EFFECT_CLASSES",
    "SLUG_PREFIX",
    "DirectiveClass",
    "DirectiveSlug",
    "build_directive_slug",
    "capability_of",
    "directive_slug_of",
    "executes_at_output_root",
    "is_kind_directive",
    "is_reserved_directive_slug",
    "parse_directive_slug",
    "resolves_in_content",
]

#: The reserved slug prefix. ANY kind slug starting with this belongs to the
#: Kind Directives protocol; nothing else may claim one.
RESERVED_PREFIX = "directive_v"

#: Current directive grammar version.
DIRECTIVE_VERSION = 1

#: The full prefix of a v1 directive slug.
SLUG_PREFIX = f"{RESERVED_PREFIX}{DIRECTIVE_VERSION}_"

DirectiveClass = Literal[
    "reference", "view", "create", "update", "delete", "action", "validation", "secret"
]

#: The CLOSED class vocabulary. Closed is what makes the grammar parseable.
CLASSES: tuple[str, ...] = (
    "reference",
    "view",
    "create",
    "update",
    "delete",
    "action",
    "validation",
    "secret",
)

#: class → capability (the safety/lifecycle contract). DERIVED, never stored on
#: a shape: a shape's capability is a fact about its class, and a second copy is
#: a second thing to drift.
CAPABILITY_BY_CLASS: dict[str, str] = {
    "reference": "pure",  # resolve/render on read; mutates nothing
    "view": "pure",  # an open-this affordance; a read, resolved by the client
    "validation": "pure",  # returns a verdict; mutates nothing
    "secret": "sensitive",  # resolved only for the model; redacted on store
    "create": "side_effect",  # executes once, server-side; auth + idempotency
    "update": "side_effect",
    "delete": "side_effect",
    "action": "side_effect",  # a named, registered procedure (a Kind Action)
}

#: The classes that EXECUTE at an agent's output root — a durable side effect.
SIDE_EFFECT_CLASSES: frozenset[str] = frozenset(
    c for c, cap in CAPABILITY_BY_CLASS.items() if cap == "side_effect"
)

#: The classes that resolve to a LIVE VALUE inside content (prose / a ```matrx
#: fence) — a pointer or a sensitive value.
#:
#: STRICT BY CHOICE (2026-08-23): this is exactly the pre-merge in-content set
#: (``reference``, ``secret``). ``view`` is pure and could plausibly be read as
#: in-content, but nothing registers a ``view`` shape today and widening a
#: position gate that no caller needs is the "little bit of breathing room" the
#: Strictness Law forbids. A ``view`` shape that ever earns in-content
#: resolution adds itself here, deliberately, with a consumer.
IN_CONTENT_CLASSES: frozenset[str] = frozenset({"reference", "secret"})


@dataclass(frozen=True)
class DirectiveSlug:
    """A parsed directive slug. ``slug`` round-trips: ``build_directive_slug(
    parsed.directive_class, parsed.noun) == parsed.slug``."""

    slug: str
    version: int
    directive_class: str
    noun: str

    @property
    def capability(self) -> str:
        return CAPABILITY_BY_CLASS[self.directive_class]

    @property
    def executes(self) -> bool:
        return executes_at_output_root(self.directive_class)

    @property
    def in_content(self) -> bool:
        return resolves_in_content(self.directive_class)


def is_reserved_directive_slug(slug: object) -> bool:
    """Whether ``slug`` sits in the reserved Kind Directives namespace.

    Deliberately broader than :func:`parse_directive_slug`: a MALFORMED
    ``directive_v…`` slug is still reserved, so authoring gates reject it
    instead of letting a near-miss through as an ordinary kind."""
    return isinstance(slug, str) and slug.startswith(RESERVED_PREFIX)


def build_directive_slug(directive_class: str, noun: str, *, version: int = DIRECTIVE_VERSION) -> str:
    """``("create", "task") → "directive_v1_create_task"``. Raises on a class
    outside the closed vocabulary or an empty/ill-formed noun — a slug that
    cannot be parsed back must never be mintable."""
    if directive_class not in CAPABILITY_BY_CLASS:
        raise ValueError(
            f"unknown directive class {directive_class!r}; the vocabulary is CLOSED: "
            f"{', '.join(CLASSES)}."
        )
    if not isinstance(noun, str) or not noun or not _is_token(noun):
        raise ValueError(
            f"invalid directive noun {noun!r} for class {directive_class!r}: a noun is "
            f"lowercase [a-z0-9_], starts with a letter, and is non-empty."
        )
    return f"{RESERVED_PREFIX}{version}_{directive_class}_{noun}"


def parse_directive_slug(slug: object) -> DirectiveSlug | None:
    """Parse a directive slug, or ``None`` when ``slug`` is not one.

    ``None`` means "not a directive at all". A slug that IS in the reserved
    namespace but does not parse returns ``None`` too — callers pair this with
    :func:`is_reserved_directive_slug` when they need to tell "ordinary kind"
    apart from "malformed directive", and every such caller in the protocol
    treats the malformed case as an ERROR, never as an ordinary kind.
    """
    if not isinstance(slug, str) or not slug.startswith(RESERVED_PREFIX):
        return None
    rest = slug[len(RESERVED_PREFIX) :]
    version_digits, sep, remainder = rest.partition("_")
    if not sep or not version_digits.isdigit():
        return None
    directive_class, sep, noun = remainder.partition("_")
    if not sep or directive_class not in CAPABILITY_BY_CLASS or not _is_token(noun):
        return None
    return DirectiveSlug(
        slug=slug, version=int(version_digits), directive_class=directive_class, noun=noun
    )


def _is_token(value: str) -> bool:
    """A noun/token: starts with a lowercase letter, then ``[a-z0-9_]``."""
    if not value or not ("a" <= value[0] <= "z"):
        return False
    return all(("a" <= ch <= "z") or ("0" <= ch <= "9") or ch == "_" for ch in value)


def capability_of(directive_class: str) -> str:
    return CAPABILITY_BY_CLASS[directive_class]


def executes_at_output_root(directive_class: str) -> bool:
    """THE position law, half one: only a side-effect class executes at an
    agent's output root. A reference or a secret there is inert data."""
    return directive_class in SIDE_EFFECT_CLASSES


def resolves_in_content(directive_class: str) -> bool:
    """THE position law, half two: only a pointer or a sensitive value resolves
    to a live value inside content. A side effect in prose is never executed."""
    return directive_class in IN_CONTENT_CLASSES


def directive_slug_of(obj: object) -> str | None:
    """The ``__kind`` of ``obj`` when it is in the reserved namespace, else None.

    Reads the RESERVED namespace, not the parsed grammar, so a malformed
    directive is still recognized as a directive (and rejected downstream with
    a real message) rather than silently mistaken for an ordinary kind."""
    if not isinstance(obj, dict):
        return None
    slug = obj.get(KIND_KEY)
    return slug if is_reserved_directive_slug(slug) else None


def is_kind_directive(obj: object) -> bool:
    """THE detector — a dict whose ``__kind`` is in the reserved namespace.

    Replaces ``is_matrx_envelope`` (presence of ``matrx_version``). One
    discriminator, one namespace, and it is the same key every other kind
    instance already carries."""
    return directive_slug_of(obj) is not None


class KindDirective(BaseModel):
    """The two-key shell. ``items`` are raw dicts here — the host decoder then
    validates each against the item model registered for the slug.

    ``extra='forbid'`` is load-bearing: it makes "everything lives inside
    ``items``" structurally true, so a stray top-level key is a hard error and
    never a silent passthrough. The Python attribute is ``kind_`` and the wire
    key is ``__kind`` — the same alias discipline
    ``matrx_graph.content_ir.model.KindModel`` uses, so a directive is a kind
    instance in the ordinary sense and not a special case."""

    model_config = ConfigDict(
        extra="forbid", populate_by_name=True, serialize_by_alias=True
    )

    kind_: str = Field(alias=KIND_KEY, serialization_alias=KIND_KEY)
    items: list[dict[str, Any]] = Field(default_factory=list)

    @property
    def slug(self) -> str:
        return self.kind_
