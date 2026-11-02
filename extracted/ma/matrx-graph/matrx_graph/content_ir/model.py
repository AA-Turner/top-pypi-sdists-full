"""``KindModel`` — the base class that makes a pydantic model a kind instance.

THE LAW (Arman, 2026-08-20 — plan of record:
``common-docs/systems/architecture/content-ir/FEATURE.md``):

    Every value that crosses a named boundary is a kind instance, and it says
    so ITSELF. The discriminator is part of the data — a DECLARED FIELD on the
    model, exactly as ``"object": "charge"`` is part of every Stripe payload.

This is the reversal of the old doctrine (``matrx_graph.contract_kinds``'s
original docstring: "must not inject ``__kind`` into business payloads"). That
doctrine produced payloads whose identity evaporated the moment they left their
row, 986 machine-minted fingerprint kinds standing in for real declarations,
and a workflow engine that stripped the platform's own language out of
everything it touched.

WHY A DECLARED FIELD AND NOT AN INJECTED MARKER
-----------------------------------------------
An injected marker must be stamped on the way out and stripped on the way in,
so every boundary needs two pieces of ceremony and every strict model
(``extra="forbid"``) is one missed strip away from a fatal. A DECLARED field
needs neither: the schema knows about it, validation accepts it, pydantic
coerces it, and ``Literal`` typing turns it into a free discriminator for
tagged unions — a consumer annotated ``Website | Article | Video`` dispatches
on ``__kind`` natively, with no isinstance ladder and no custom parsing.

``strip_kind_markers`` (``matrx_graph.content_ir.markers``) therefore survives
at exactly two doors — serialization into an agent PROMPT (external minds) and
egress to an EXTERNAL system — plus a shrinking legacy shim for models that
have not been converted yet. It is no longer part of the interior path.

WIRE FORM
---------
The field is named ``kind_`` in Python (``kind`` is too useful a business field
name to reserve, and a leading-underscore attribute cannot be a pydantic field)
and serializes as ``__kind`` — the platform-wide wire key that chat, the
frontend detection pipeline, and the render registry already speak
(``KIND_KEY`` in ``matrx_graph.content_ir.envelope``). The base owns BOTH
directions of that alias — ``populate_by_name`` so ``Model(**payload)`` accepts
a payload that already carries ``__kind``, and ``serialize_by_alias`` so every
dump emits ``__kind`` at every depth, nested inside another model included.

USAGE
-----
    class Website(KindModel, kind="website"):
        url: str
        title: str
        snippet: str = ""

    Website(url="https://x.com", title="X").model_dump()
    # {"__kind": "website", "url": "https://x.com", "title": "X", "snippet": ""}

Nesting needs no ceremony: a field typed as another ``KindModel`` carries its
own discriminator, so a whole tree is self-describing at every level — which is
what lets one registry entry render a nested structure on every surface.

The ``@kind`` decorator (``matrx_graph.content_ir.sdk``) is the fuller entry
point — it wraps this base and adds registry publication, ``kind_edge`` rows,
and example capture. Use ``KindModel`` directly when a model must be a kind but
its registration is owned elsewhere (already-registered curated kinds, or
models declared inside a package that does not publish).
"""

from __future__ import annotations

from typing import Annotated, Any, ClassVar

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field
from pydantic.fields import FieldInfo

from matrx_graph.content_ir.envelope import KIND_KEY

__all__ = [
    "KindModel",
    "KindSubModel",
    "NON_IDENTITY_KIND",
    "NoKindMarker",
    "no_kind_marker",
    "kind_of",
    "is_kind_instance",
    "pin_kind_discriminator",
]


class KindModel(BaseModel):
    """Base class for every model that IS a registered kind.

    Subclasses declare their slug in the class definition:

        class Website(KindModel, kind="website"): ...

    The slug becomes both a ``ClassVar`` (``Website.kind_slug``) and the
    default of the declared ``kind_`` field, so an instance carries its
    identity in the data with zero effort at the construction site.

    ``extra="forbid"`` is deliberate and matches the registry's schemas: a
    kind is a CONTRACT, and a field nobody declared is a silent drift channel.
    Genuinely open-ended payloads model that explicitly (a typed ``dict`` field
    or a documented ``extras`` map), never by leaving the door open.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        serialize_by_alias=True,
        validate_assignment=True,
    )

    #: The registered kind slug. Set by ``__init_subclass__`` from the class
    #: keyword; read it without instantiating (``Website.kind_slug``).
    kind_slug: ClassVar[str] = ""

    # The discriminator, as DATA. Redeclared in each subclass by
    # ``__init_subclass__`` with a ``Literal`` type and a default, which is
    # what makes pydantic tagged unions work on ``__kind`` for free.
    kind_: str = Field(default="", alias=KIND_KEY, serialization_alias=KIND_KEY)

    def __init_subclass__(cls, kind: str | None = None, **kwargs: Any) -> None:
        # Consume the ``kind=`` class keyword before pydantic's metaclass sees
        # it, and stash it for ``__pydantic_init_subclass__`` below. The field
        # cannot be redeclared HERE: this hook runs while the class is still
        # being built, so pydantic has not collected the subclass's own fields
        # yet and any ``model_rebuild`` would freeze a half-built schema (it
        # did exactly that — every real field came back "extra_forbidden").
        if kind is not None:
            if not isinstance(kind, str) or not kind.strip():
                raise TypeError(
                    f"{cls.__name__}: kind must be a non-empty slug string, got {kind!r}."
                )
            cls.kind_slug = kind
        super().__init_subclass__(**kwargs)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        """Pin the discriminator AFTER pydantic has built the subclass.

        An intermediate base may omit the slug and let its own subclasses
        declare it; only a class that actually carries one gets its
        discriminator pinned. ``Literal`` + default is what gives pydantic a
        free tagged-union discriminator on ``__kind`` and a JSON Schema that
        states what the payload IS.
        """
        super().__pydantic_init_subclass__(**kwargs)
        slug = cls.__dict__.get("kind_slug") or ""
        if slug:
            pin_kind_discriminator(cls, slug)

    def model_copy(self, *, update: Any = None, deep: bool = False) -> Any:
        """Copy with the discriminator PINNED (round-1 adversarial F9).

        ``model_copy`` bypasses validation by pydantic design, so
        ``update={"kind_": "evil"}`` could forge an instance that serializes
        a ``__kind`` its class does not own while ``kind_of()`` still reports
        the class slug — two answers for one identity. The discriminator is
        CLASS identity, not instance data: any attempt to update it is
        overwritten with the class's own slug.
        """
        if update and "kind_" in update and self.kind_slug:
            update = {**update, "kind_": self.kind_slug}
        return super().model_copy(update=update, deep=deep)

    # THE WIRE KEY IS OWNED BY ``serialize_by_alias=True`` ABOVE, NOT BY AN
    # OVERRIDE. ``model_dump``/``model_dump_json`` overrides that defaulted
    # ``by_alias=True`` used to live here, and they were only half the rule: an
    # override fires only when a caller dumps THIS model directly. A kind
    # NESTED inside another model is serialized by pydantic-core, which never
    # calls it — so the top level said ``__kind`` while one level down said
    # ``kind_``, and the registry (additionalProperties:false, ``__kind``
    # declared) rejected the payload. The config setting applies at every
    # depth. Pass ``by_alias=False`` deliberately when a caller genuinely wants
    # Python field names (rare; usually a sign the value should not be leaving
    # at all).


#: The ``__kind`` value of a plain sub-structure: it has no kind of its own.
#: Declared as ``const`` in every sub-structure schema so a model bound to the
#: schema cannot invent one (``markers.normalize_nonidentity_markers``).
NON_IDENTITY_KIND = ""


def _ignore_sub_marker(_value: Any) -> str:
    """Accept-and-ignore: whatever a payload carries here, a sub-structure has
    no identity, so the stored value is always ``NON_IDENTITY_KIND``."""
    return NON_IDENTITY_KIND


#: The ``__kind`` slot of a model that is NOT a kind (Content IR rule 28): any value
#: an old row or a payload carries is read as ``NON_IDENTITY_KIND``, never refused.
NoKindMarker = Annotated[str, BeforeValidator(_ignore_sub_marker)]


def no_kind_marker() -> Any:
    """The field for a ``NoKindMarker`` slot — ``kind: NoKindMarker = no_kind_marker()``.

    For a model that used to stamp an invented ``__kind`` on itself: stored rows keep
    parsing (accept-and-ignore), and nothing it writes claims a kind (excluded from
    every dump), exactly like ``KindSubModel``'s own marker.
    """
    return Field(
        default=NON_IDENTITY_KIND,
        alias=KIND_KEY,
        serialization_alias=KIND_KEY,
        exclude=True,
        json_schema_extra={"const": NON_IDENTITY_KIND},
        description="Not a kind: no kind of its own. Always empty.",
    )


class KindSubModel(BaseModel):
    """Base for plain sub-structure INSIDE a kind — shape without identity.

    A ``SiteLink`` or a ``DayHours`` is not a kind: it has no independent
    meaning outside the kind that holds it, so it gets no slug, no registry
    row, and emits no ``__kind``. Giving every nested object a slug is how a
    family ends up with 100 kinds, which is the same as no kinds.

    But it must still ACCEPT the marker. THE ``__kind`` LAW's consumer clause
    (``KINDS_EVERYWHERE_PLAN.md`` §4.2a) is that a consumer which chokes on the
    marker gets FIXED to accept-and-ignore — never fed stripped data. A plain
    ``BaseModel`` with ``extra="forbid"`` chokes: one producer stamping
    ``__kind`` on a sub-object turns into a validation fatal far from the cause.

    That is not hypothetical. The live registry rows already declare an
    optional ``__kind`` on every nested ``$def`` (the schema-law campaign
    patched them there), so a model whose sub-structures REFUSE it is strictly
    stricter than the contract it claims to implement — and the compatibility
    gate reads the missing property as "a field disappeared" and refuses the
    whole distillation as breaking. Measured 2026-08-24 on the search family:
    six kinds were refused for exactly this and nothing else.

    So: declared, optional, ignored, and ``exclude``-d from every dump, because
    a sub-structure that is not a kind must never claim to be one.

    THE MARKER IS A CONST, NEVER A FREE STRING (2026-10-24). A sub-structure's
    own declared kind name is EMPTY — it has no identity — so its schema says
    exactly that: ``{"type": "string", "const": ""}``, optional, default
    ``""``. It used to say ``{"type": "string"}``, and a free string in a
    response schema is an invitation: agents bound to these schemas filled it
    with junk (``"x"``, ``"grew_from"``, ``"option_flag"``,
    ``"ElementOption_placeholder"``) on 859 nested definitions across 345 live
    kinds. Reading stays accept-and-ignore: ANY value arriving here (an old
    stored row, a provider that ignored the const) is normalized to ``""`` by
    the before-validator, never refused. Guard:
    ``tests/test_nested_kind_marker_const.py``.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        serialize_by_alias=True,
    )

    kind_: Annotated[str, BeforeValidator(_ignore_sub_marker)] = Field(
        default=NON_IDENTITY_KIND,
        alias=KIND_KEY,
        serialization_alias=KIND_KEY,
        exclude=True,
        json_schema_extra={"const": NON_IDENTITY_KIND},
        description="Plain sub-structure: no kind of its own. Always empty.",
    )


def pin_kind_discriminator(cls: type[KindModel], slug: str) -> None:
    """Declare ``cls``'s discriminator as ``Literal[slug]`` with the wire alias.

    Shared by the class-keyword path (``class Website(KindModel,
    kind="website")``) and the ``@kind`` decorator (``content_ir.sdk``), so the
    two entry points cannot drift. Must run AFTER pydantic has collected the
    class's own fields — rebuilding earlier freezes a half-built schema (pinned
    by ``test_declared_fields_survive_strictness``).
    """
    cls.kind_slug = slug
    cls.model_fields["kind_"] = FieldInfo.from_annotated_attribute(
        _literal_of(slug),
        Field(
            default=slug,
            alias=KIND_KEY,
            serialization_alias=KIND_KEY,
            description="The registered kind this payload is an instance of.",
        ),
    )
    cls.model_rebuild(force=True)


def _literal_of(value: str) -> Any:
    from typing import Literal

    return Literal[value]  # type: ignore[valid-type]


def kind_of(value: Any) -> str | None:
    """The kind slug of ``value``, or ``None`` when it is not a kind instance.

    Works on both halves of the boundary: a ``KindModel`` instance (read from
    the class) and an already-serialized payload (read from the wire key), so
    callers that receive "whatever flowed" — runtime kind propagation, the
    ingestion gate, the render router — have ONE way to ask.
    """
    if isinstance(value, KindModel):
        return value.kind_slug or None
    if isinstance(value, dict):
        slug = value.get(KIND_KEY)
        return slug if isinstance(slug, str) and slug else None
    return None


def is_kind_instance(value: Any) -> bool:
    """Whether ``value`` carries a kind identity (model or serialized payload)."""
    return kind_of(value) is not None
