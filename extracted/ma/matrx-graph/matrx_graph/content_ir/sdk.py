"""The kind SDK — ``@kind``: one decorator, the whole ceremony.

THE EFFORT INVERSION (plan of record
``common-docs/systems/architecture/content-ir/FEATURE.md`` §4.3).
Arman's diagnosis of why the platform drifted: registering a kind cost ~7
ceremony steps (schema dump → seed SQL → apply → ledger → cache invalidation →
live verify → component wiring) while an anonymous dict cost zero, and
engineers — human and agent — follow the gradient. His requirement:

    "When is our own code base doing it? It's the easiest thing in the world.
    The function just spits out the object exactly at the shape we want."

So:

    @kind("web_result", disposition="record", label="Web Result", family="search")
    class WebResult(KindModel):
        url: str
        title: str
        snippet: str = ""

That is the entire producer-side ceremony. The decorator:

* pins the discriminator (``__kind`` as a declared ``Literal`` field — the
  same pinning the ``kind="…"`` class keyword performs, one shared helper);
* records the class in the process-wide ``kind_catalog()`` with its
  registration metadata (label, family, category, canonical example);
* derives everything publication needs FROM THE MODEL — the JSON Schema (which
  carries ``__kind`` because it is a declared field: wire IS block for
  new-world kinds, the one-shape doctrine) and the nested-kind edges (walked
  from field annotations, so ``kind_edge`` rows can never drift from the
  types).

PUBLICATION IS A SEPARATE, DELIBERATE STEP — and never a silent overwrite.
``publication_plan()`` is the pure core: given the catalog and the live
registry rows, it computes exactly what a sync would do — ``create`` for a
missing kind, ``match`` for an identical one, and **``drift`` for a registered
kind whose live schema differs from the model**. Drift is REPORTED, never
auto-applied: schema evolution goes through the compatibility gate (plan §3,
Confluent semantics), because "the model changed so overwrite the registry" is
exactly the unpoliced mutation the gate exists to prevent. The applying halves
(DB writes through the host's registered managers, the shared migration
ledger, cache invalidation) live host-side where the managers are wired.

The decorator itself performs NO I/O — importing a module that declares kinds
must stay free of side effects beyond the in-process catalog, or every import
becomes a network call and tests become integration tests.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict

from matrx_graph.content_ir.envelope import KIND_KEY
from matrx_graph.content_ir.markers import strip_optional_schema_kind_stamps
from matrx_graph.content_ir.model import KindModel, pin_kind_discriminator

__all__ = [
    "kind",
    "KIND_DISPOSITIONS",
    "KindDispositionMissing",
    "DERIVED_DISPOSITION_RULES",
    "derived_disposition",
    "disposition_of",
    "disposition_refusal",
    "TABLE_KIND_DISPOSITION",
    "require_disposition",
    "KindRegistration",
    "kind_catalog",
    "clear_kind_catalog",
    "aliases_of",
    "alias_target",
    "nested_kind_slugs",
    "PublicationAction",
    "publication_plan",
    "CompatibilityVerdict",
    "compatibility_verdict",
]


#: What a kind's output IS — the one storage question, answered at birth (KINDS-DESIGN-V2
#: §1.1, Arman's K2). The closed set the kind store (``kind_records.store``) and the
#: activation gate (``content_ir.evaluate_kind_activation``'s disposition leg) read:
#:
#: * ``record``   — structured output with keys a person filters by; stored as a record.
#: * ``envelope`` — a wrapper whose keys differ every call; keeps the run store.
#: * ``receipt``  — says a write already happened and names what it wrote.
#: * ``proposal`` — an offer against rows that exist; lives in review-and-apply.
#: * ``prose``    — one text body (K15); stays where prose lives.
#:
#: A kind born without one is refused at storage time and every user output it carries is
#: lost (``kind_disposition_undeclared``), so ``@kind`` refuses to declare a kind without it.
KIND_DISPOSITIONS: tuple[str, ...] = ("record", "envelope", "receipt", "proposal", "prose")


def disposition_refusal(slug: str, disposition: object) -> str | None:
    """The plain sentence refusing ``disposition`` for ``slug``, or None when it is valid.

    THE ONE VALIDATOR for every path that creates a kind (KINDS-GLUE wave 1b): the ``@kind``
    decorator, the publisher, the agent ``kind_create`` tool, the provision offer sync and
    every ``seed_*_kinds.py`` script call this — never a second list or a second check.
    """
    if disposition is None or (isinstance(disposition, str) and not disposition.strip()):
        return (
            f"The kind {slug!r} does not say what its output is. Declare "
            f"disposition= one of {', '.join(KIND_DISPOSITIONS)} — without it every "
            f"verified emission of this kind is refused storage and the user's output is lost."
        )
    if disposition not in KIND_DISPOSITIONS:
        return (
            f"The kind {slug!r} declares disposition={disposition!r}, which is not one of "
            f"{', '.join(KIND_DISPOSITIONS)}."
        )
    return None


#: Kept for the wave-1 call sites; new code calls ``disposition_refusal``.
_disposition_refusal = disposition_refusal


#: Dispositions decided by what a kind IS by construction, never by judgment — THE ONE place
#: these rules live (KINDS-GLUE manager ruling 2026-10-02). Every writer that mints such kinds
#: (the provision offer sync) and the wave-1 reclassification read ``derived_disposition``;
#: nobody re-states a rule. Ordered; first match wins.
#:
#: * ``<provision_key>.offer`` — the derived INPUT kind of a provision: a wrapper whose keys
#:   differ per provision -> ``envelope``.
#:
#: The ``agent_input_*`` prefix rule was retired 2026-10-25 with the kinds it described:
#: those were minted from an agent's first four field names (content-ir rule 28, NO FAKE
#: KINDS). An agent's variables are its input form; they are not a kind.
DERIVED_DISPOSITION_RULES: tuple[tuple[str, str, str, str], ...] = (
    ("suffix", ".offer", "envelope", "a provision's derived input kind"),
)


def derived_disposition(slug: str) -> str | None:
    """The disposition ``DERIVED_DISPOSITION_RULES`` assign to ``slug``, or None (no rule)."""
    for match, token, disposition, _why in DERIVED_DISPOSITION_RULES:
        if (match == "suffix" and slug.endswith(token)) or (
            match == "prefix" and slug.startswith(token)
        ):
            return disposition
    return None


#: A Table's records are records (KINDS-GLUE wave 3 ruling D): ``table:<uuid>`` is never a
#: registry row, so it can never declare a disposition — it has one by construction.
TABLE_KIND_DISPOSITION = "record"


def disposition_of(slug: str, definition_metadata: Mapping[str, Any] | None) -> str | None:
    """What an emission of ``slug`` IS — THE ONE read the kind store and wave 2's router make.

    * ``table:<uuid>`` -> ``record``, by code rule, with no registry row (wave 3 §6.2 item 1).
    * every other slug -> its registry row's declared ``metadata.disposition`` when that is one
      of ``KIND_DISPOSITIONS``, else ``None`` (undeclared — the store refuses it loudly). Wave
      1's rule is unchanged: nothing here defaults, derives or guesses a registry kind's answer.

    Nobody in ``kind_records`` reads ``metadata["disposition"]`` except through this function.
    """
    from matrx_graph.table_kinds import is_table_kind

    if is_table_kind(slug):
        return TABLE_KIND_DISPOSITION
    disposition = (definition_metadata or {}).get("disposition")
    if disposition_refusal(slug, disposition) is not None:
        return None
    return str(disposition)


class KindDispositionMissing(ValueError):
    """A kind was about to be written without a valid ``metadata.disposition``."""


def require_disposition(slug: str, metadata: Mapping[str, Any] | None) -> str:
    """Return ``metadata['disposition']`` or raise ``KindDispositionMissing`` with the sentence.

    Writers that build a ``kind_definition`` row call this on the exact metadata they are about
    to write, immediately before the insert/update.
    """
    disposition = (metadata or {}).get("disposition")
    refusal = disposition_refusal(slug, disposition)
    if refusal:
        raise KindDispositionMissing(refusal)
    return str(disposition)


class KindRegistration(BaseModel):
    """Everything the publisher needs about one decorated kind."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    slug: str
    model: type[KindModel]
    label: str
    #: What this kind's output IS (``KIND_DISPOSITIONS``) — required, never defaulted.
    disposition: str
    #: Registry ``metadata.family`` (e.g. ``search``, ``primitive``). Optional
    #: because not every kind belongs to a named family; NEVER defaulted to a
    #: guess.
    family: str | None = None
    #: ``data`` (portable payload) or ``runtime`` (wrapper) — the layer model.
    category: str = "data"
    #: Field names an AI-facing projection of this kind keeps. Empty/None means
    #: "the whole payload" — the historical behavior. See ``kind(ai_view=...)``.
    ai_view: tuple[str, ...] | None = None
    #: Canonical example, validated against the model at decoration time so a
    #: broken example fails at import in the author's face, not at publish time
    #: in nobody's face.
    example: dict[str, Any] | None = None
    #: How far this kind has been taken (Arman, 2026-08-20 — the tracking that
    #: stops a fast-fire stub from masquerading as the real deal):
    #: ``placeholder`` — outer structure captured honestly, data NOT studied
    #:   (the army's fast-fire tier; the DEFAULT, because claiming more must be
    #:   deliberate);
    #: ``distilled`` — the real data was studied and the shape designed, the
    #:   web-search treatment (nested kinds, keep/drop decisions, merge
    #:   analysis where relevant);
    #: ``verified`` — distilled AND proven end-to-end (registered → generated
    #:   types → component → real payload rendered). Set by the verification
    #:   pass, never self-award it at declaration time.
    maturity: str = "placeholder"
    #: Older slugs this kind is ALSO read as (KINDS-GLUE wave 4 §A.3.2, the one alias mechanism;
    #: TS twin: ``KindDefinition.discriminatorAliases``). Stored messages keep the old slug, so an
    #: alias is read forever; the publisher writes it to ``metadata.aliases``.
    aliases: tuple[str, ...] = ()

    def model_post_init(self, __context: Any) -> None:
        # Round-1 F12: the model enforces the tier vocabulary itself — the
        # decorator's check must not be the only gate when registrations are
        # constructed directly. The disposition likewise.
        refusal = _disposition_refusal(self.slug, self.disposition)
        if refusal:
            raise ValueError(refusal)
        if self.maturity not in ("placeholder", "distilled", "verified"):
            raise ValueError(
                f"KindRegistration({self.slug!r}): maturity must be "
                f"placeholder|distilled|verified, got {self.maturity!r}."
            )

    def json_schema(self) -> dict[str, Any]:
        """The model's schema — carries ``__kind`` (one-shape doctrine)."""
        return self.model.model_json_schema()

    def nested_slugs(self) -> tuple[str, ...]:
        """Kinds nested inside this one — the ``kind_edge`` rows, from types."""
        return nested_kind_slugs(self.model)


_catalog: dict[str, KindRegistration] = {}


def kind(
    slug: str,
    *,
    disposition: str | None = None,
    label: str | None = None,
    family: str | None = None,
    category: str = "data",
    example: dict[str, Any] | None = None,
    maturity: str = "placeholder",
    ai_view: Sequence[str] | None = None,
    aliases: Sequence[str] = (),
) -> Callable[[type[KindModel]], type[KindModel]]:
    """Declare a ``KindModel`` subclass as the kind ``slug``. See module doc.

    ``ai_view`` names the fields an AI-facing projection of this kind keeps.

    THE PROBLEM IT SOLVES (Arman, 2026-08-24): a workflow step emits a kind and
    the author binds it to an agent variable. Today the model receives the
    ENTIRE payload — for ``scraped_page`` that is the markdown AND two other
    full-text renderings AND 1,473 link records AND 158 content blocks AND a
    minhash vector. *"If you overdo it, then you're killing the model's context
    window."* But the answer is not a second kind per family: it is the kind
    saying, once, which of its own fields matter to a model.

    Declared here, published to ``kind_definition.metadata.ai_view``, and
    applied at the ONE prompt door (``matrx_ai.config.prompt_values``), so no
    workflow author has to know and no call site has to remember.

    Omit it and nothing changes — the whole payload travels, exactly as before.

    ``disposition`` is REQUIRED: what this kind's output is (``KIND_DISPOSITIONS``). A kind
    without one used to be born, published and activated, and then every verified emission
    of it was refused storage — the user's output lost, one kind at a time (KINDS-GLUE
    wave 1). Omitting it fails at import, in the author's face.
    """
    if not isinstance(slug, str) or not slug.strip():
        raise TypeError(f"@kind requires a non-empty slug, got {slug!r}.")
    refusal = _disposition_refusal(slug, disposition)
    if refusal:
        raise ValueError(f"@kind({slug!r}): {refusal}")
    if category not in ("data", "runtime"):
        raise ValueError(
            f"@kind({slug!r}): category must be 'data' or 'runtime', got {category!r} "
            f"(the layer model admits no third category)."
        )
    if ai_view is not None:
        ai_view = tuple(ai_view)
        if not ai_view:
            raise ValueError(
                f"@kind({slug!r}): ai_view was given but empty. Omit it to send the "
                f"whole payload; an empty tuple would send a model nothing at all."
            )
        unknown = [f for f in ai_view if not isinstance(f, str) or not f.strip()]
        if unknown:
            raise ValueError(f"@kind({slug!r}): ai_view entries must be field names, got {unknown!r}.")
    aliases = tuple(aliases)
    if slug in aliases or any(not isinstance(a, str) or not a.strip() for a in aliases):
        raise ValueError(f"@kind({slug!r}): aliases must be other, non-empty slugs, got {aliases!r}.")
    if maturity not in ("placeholder", "distilled"):
        raise ValueError(
            f"@kind({slug!r}): maturity must be 'placeholder' or 'distilled', got "
            f"{maturity!r}. 'verified' is earned through the verification pass, "
            f"never declared."
        )

    def decorate(cls: type[KindModel]) -> type[KindModel]:
        if not (isinstance(cls, type) and issubclass(cls, KindModel)):
            raise TypeError(
                f"@kind({slug!r}) requires a KindModel subclass; {cls!r} is not one. "
                f"Inherit KindModel — the discriminator must be a declared field."
            )
        if cls.kind_slug and cls.kind_slug != slug:
            raise ValueError(
                f"{cls.__name__} already declares kind {cls.kind_slug!r}; "
                f"@kind({slug!r}) contradicts it. One class, one kind."
            )
        pin_kind_discriminator(cls, slug)

        if ai_view is not None:
            # A projection naming a field the model does not have is a silent
            # hole in what a model receives — fail at import, in the author's
            # face, exactly as a bad `example` does.
            missing = [f for f in ai_view if f not in cls.model_fields]
            if missing:
                raise ValueError(
                    f"@kind({slug!r}): ai_view names field(s) {missing!r} that "
                    f"{cls.__name__} does not declare. A projection cannot keep a "
                    f"field that does not exist."
                )

        if example is not None:
            # Fail at import, in the author's face. An example that does not
            # satisfy its own model is a lie the registry would then certify.
            cls.model_validate(example)

        for alias in aliases:
            owner = alias_target(alias)
            if owner is not None and owner != slug:
                raise ValueError(f"@kind({slug!r}): {alias!r} is already an alias of {owner!r}.")
        existing = _catalog.get(slug)
        if existing is not None and existing.model is not cls:
            raise ValueError(
                f"Kind {slug!r} is already declared by "
                f"{existing.model.__module__}.{existing.model.__qualname__}; "
                f"{cls.__module__}.{cls.__qualname__} redeclares it. One kind, one model."
            )
        _catalog[slug] = KindRegistration(
            slug=slug,
            model=cls,
            label=label or _default_label(cls.__name__),
            disposition=disposition,
            family=family,
            category=category,
            example=example,
            maturity=maturity,
            ai_view=ai_view,
            aliases=aliases,
        )
        return cls

    return decorate


def kind_catalog() -> dict[str, KindRegistration]:
    """The process-wide catalog of decorated kinds (slug → registration)."""
    return dict(_catalog)


def aliases_of(slug: str) -> frozenset[str]:
    """The older slugs ``slug`` is also read as — THE ONE alias read (never a hand list)."""
    registration = _catalog.get(slug)
    return frozenset(registration.aliases) if registration is not None else frozenset()


def alias_target(slug: str) -> str | None:
    """The kind an alias ``slug`` resolves to, or None when no declared kind claims it."""
    for registration in _catalog.values():
        if slug in registration.aliases:
            return registration.slug
    return None


def clear_kind_catalog() -> None:
    """Test isolation only."""
    _catalog.clear()


def _default_label(class_name: str) -> str:
    # WebResult -> "Web Result"; keeps runs of capitals together (AIAnswer ->
    # "AI Answer").
    out: list[str] = []
    for i, ch in enumerate(class_name):
        if (
            ch.isupper()
            and i > 0
            and (
                not class_name[i - 1].isupper()
                or (i + 1 < len(class_name) and class_name[i + 1].islower())
            )
        ):
            out.append(" ")
        out.append(ch)
    return "".join(out)


def nested_kind_slugs(model: type[KindModel]) -> tuple[str, ...]:
    """The kind slugs nested anywhere in ``model``'s schema, deduplicated.

    Read from the generated schema rather than annotations: the schema is what
    the registry stores and what the availability index walks, so edges derived
    here can never disagree with what a consumer of the registry would see.
    """
    schema = model.model_json_schema()
    found: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            properties = node.get("properties")
            if isinstance(properties, dict):
                marker = properties.get(KIND_KEY)
                if isinstance(marker, dict):
                    const = marker.get("const")
                    if isinstance(const, str) and const and const != model.kind_slug:
                        if const not in found:
                            found.append(const)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(schema)
    return tuple(found)


class PublicationAction(BaseModel):
    """One row of a publication plan."""

    model_config = ConfigDict(frozen=True)

    slug: str
    #: ``create`` (not in the registry) · ``match`` (registered, identical
    #: schema) · ``drift`` (registered, DIFFERENT schema — needs the
    #: compatibility gate, never an auto-overwrite).
    action: str
    label: str
    #: The declared disposition (``KIND_DISPOSITIONS``) the publisher writes.
    disposition: str
    family: str | None = None
    category: str = "data"
    json_schema: dict[str, Any]
    #: ``kind_edge`` rows this kind implies (parent = this slug).
    nested: tuple[str, ...] = ()
    #: For ``drift``: a compact description of what differs, for the report.
    drift_summary: str | None = None


def publication_plan(
    registrations: dict[str, KindRegistration],
    resolve_live_schema: Callable[[str], dict[str, Any] | None],
) -> list[PublicationAction]:
    """Compute what a registry sync WOULD do — pure, no I/O.

    ``resolve_live_schema`` maps a slug to the registry's current
    ``emitted_json_schema`` (``None`` = unregistered). Comparison ignores the
    volatile ``description``/``title`` decorations pydantic emits and compares
    structure — a cosmetic docstring edit is not schema drift.
    """
    plan: list[PublicationAction] = []
    for slug in sorted(registrations):
        registration = registrations[slug]
        model_schema = registration.json_schema()
        live = resolve_live_schema(slug)
        if live is None:
            action, summary = "create", None
        elif _structurally_equal(model_schema, live):
            action, summary = "match", None
        else:
            action = "drift"
            summary = _drift_summary(model_schema, live)
        plan.append(
            PublicationAction(
                slug=slug,
                action=action,
                label=registration.label,
                disposition=registration.disposition,
                family=registration.family,
                category=registration.category,
                json_schema=model_schema,
                nested=registration.nested_slugs(),
                drift_summary=summary,
            )
        )
    return plan


_COSMETIC_KEYS = frozenset({"description", "title", "examples"})

# Dict-valued schema keywords whose KEYS are data (property names, def names),
# not schema keywords. Cosmetic stripping must never apply at these key levels
# — a kind with a real field named ``title`` or ``description`` would otherwise
# have changes to that field be INVISIBLE to drift detection (caught by
# test_publication_plan_create_match_drift).
_KEYED_MAPS = frozenset({"properties", "$defs", "patternProperties"})

#: Keywords that are pure ANNOTATIONS — JSON Schema 2020-12 §9.2 says they do
#: not participate in validation at all. They are NOT cosmetic (a ``default``
#: is real, meaningful data that generators and forms read), so they are
#: stripped for exactly ONE question: Confluent BACKWARD compatibility, "can a
#: reader built for the NEW schema still read data written under the OLD one".
#: An annotation cannot make an old payload stop validating in either
#: direction, so a field whose only difference is the presence of a ``default``
#: has NOT changed type or constraints.
#:
#: Why this matters: every ``@kind`` model emits
#: ``{"type": "string", "const": <slug>, "title": …, "default": <slug>,
#: "description": …}`` for ``__kind``, while live rows patched by hand during
#: the ``__kind`` schema-law campaign carry the same const with NO ``default``.
#: Comparing those literally reported "changes the type/constraints of field
#: '__kind'" — a BREAKING verdict for a change that never happened, which
#: forced every distillation of such a slug through ``--breaking`` and hid any
#: REAL break in the same run behind a flag the author already had to pass
#: (reproduced live 2026-08-23 on ``scraped_page``).
#:
#: Deliberately NOT folded into ``_COSMETIC_KEYS``: drift detection
#: (``_structurally_equal`` → the publication plan) must still SEE a changed
#: default, so the update is planned and never silent.
_ANNOTATION_KEYS = frozenset({"default"})


def _normalize(node: Any, *, keys_are_data: bool = False, drop_annotations: bool = False) -> Any:
    if isinstance(node, dict):
        out = {}
        for key, value in sorted(node.items()):
            if not keys_are_data and key in _COSMETIC_KEYS:
                continue
            if not keys_are_data and drop_annotations and key in _ANNOTATION_KEYS:
                continue
            out[key] = _normalize(
                value,
                keys_are_data=(not keys_are_data and key in _KEYED_MAPS),
                drop_annotations=drop_annotations,
            )
        return out
    if isinstance(node, list):
        return [_normalize(item, drop_annotations=drop_annotations) for item in node]
    return node


def _compat_normalize(node: Any) -> Any:
    """``_normalize`` for the COMPATIBILITY gate: annotations are not contract."""
    return _normalize(node, drop_annotations=True)


def _json_value_equal(left: Any, right: Any) -> bool:
    """JSON-value equality without Python's ``True == 1`` coercion.

    Enum membership is a validation rule, so its comparison must use JSON's
    value domains.  Python considers booleans integers for equality; JSON
    Schema does not.  Keeping this recursive also makes a future compound enum
    value unambiguous rather than quietly relying on host-language equality.
    """
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(
            _json_value_equal(value, right[key]) for key, value in left.items()
        )
    if isinstance(left, list):
        return len(left) == len(right) and all(
            _json_value_equal(value, candidate) for value, candidate in zip(left, right, strict=True)
        )
    return left == right


def _structurally_equal(a: dict[str, Any], b: dict[str, Any]) -> bool:
    return strip_optional_schema_kind_stamps(_normalize(a)) == strip_optional_schema_kind_stamps(
        _normalize(b)
    )


def _drift_summary(model_schema: dict[str, Any], live: dict[str, Any]) -> str:
    def keys(schema: dict[str, Any]) -> set[str]:
        properties = schema.get("properties")
        if not isinstance(properties, dict) and isinstance(schema.get("$defs"), dict):
            ref = schema.get("$ref", "")
            root = schema["$defs"].get(str(ref).rsplit("/", 1)[-1], {})
            properties = root.get("properties")
        return set(properties or {})

    model_keys, live_keys = keys(model_schema), keys(live)
    added = sorted(model_keys - live_keys)
    removed = sorted(live_keys - model_keys)
    parts = []
    if added:
        parts.append(f"model adds {added}")
    if removed:
        parts.append(f"model removes {removed}")
    if not parts:
        parts.append("field-level constraints differ (same key set)")
    return "; ".join(parts)


class CompatibilityVerdict(BaseModel):
    """Whether a model's schema may replace a registered kind's live schema.

    Confluent BACKWARD semantics, the only direction that matters here: a
    reader built for the NEW schema must still read data written under the OLD
    one. Adding an OPTIONAL field is safe (old payloads simply lack it);
    adding a REQUIRED field, removing a field, or changing a field's type is
    not — old rows in ``workflow.node_outcome`` would stop validating.

    Pure and I/O-free so the gate is testable without a registry, and so the
    publisher can never "decide" compatibility on its own.
    """

    model_config = ConfigDict(frozen=True)

    compatible: bool
    #: Human-readable reasons a replacement is refused. Empty when compatible.
    breaking: tuple[str, ...] = ()
    #: Safe changes, for the report (so an evolution is never silent).
    additive: tuple[str, ...] = ()


def _resolve(node: Any, defs: dict[str, Any]) -> Any:
    """Follow a ``$ref`` into ``defs`` (one hop; refs to refs are rare).

    SIBLINGS SURVIVE THE HOP. JSON Schema 2020-12 lets ``$ref`` sit beside
    ordinary keywords, and pydantic uses that constantly: a
    ``JsonValue``-typed field with a default emits
    ``{"$ref": "#/$defs/JsonValue", "default": null, "description": …}``.
    Returning the bare target discarded the ``default``, so the resolved model
    field compared as ``{}`` against a live field that still said
    ``{"default": null}`` — a spurious "changes the type/constraints" verdict
    that refused an evolution where NOTHING about the field had changed
    (found 2026-08-23 on ``regex_extract_result.first``, whose live row was
    published by an older dump that inlined the same empty definition).

    Dropping keywords in the other direction is just as wrong: a real
    tightening carried on a sibling would have been invisible to the gate.
    Merging siblings over the target is the faithful view — this makes the
    comparison MORE accurate, never more permissive.
    """
    if isinstance(node, dict) and "$ref" in node and isinstance(defs, dict):
        target = defs.get(str(node["$ref"]).rsplit("/", 1)[-1])
        if isinstance(target, dict):
            siblings = {k: v for k, v in node.items() if k != "$ref"}
            return {**target, **siblings} if siblings else target
    return node


def _root_properties(schema: dict[str, Any]) -> tuple[dict[str, Any], set[str]]:
    """(properties, required) for a schema, following a root ``$ref``."""
    defs = schema.get("$defs") if isinstance(schema.get("$defs"), dict) else {}
    node = schema
    if not isinstance(node.get("properties"), dict) and defs:
        node = _resolve(node, defs)
    properties = node.get("properties")
    required = node.get("required")
    return (
        properties if isinstance(properties, dict) else {},
        set(required) if isinstance(required, list) else set(),
    )


def _is_unconstrained_schema(
    node: Any,
    defs: dict[str, Any],
    _depth: int = 0,
    _seen: frozenset[str] = frozenset(),
) -> bool:
    """Whether a schema accepts every value, following only empty local refs.

    JSON Schema's boolean ``true`` schema and the empty schema ``{}`` have the
    same meaning. Pydantic's ``JsonValue`` definition is the latter, so a
    dictionary whose additionalProperties is a ref to that definition is no
    narrower than legacy ``additionalProperties: true``. Ref siblings are
    retained as constraints/metadata by the normal comparator and therefore
    are deliberately excluded from this alias-only normalization.
    """
    if node is True or node == {}:
        return True
    if not isinstance(node, dict) or set(node) != {"$ref"}:
        return False
    ref = node.get("$ref")
    if not isinstance(ref, str) or not ref.startswith("#/$defs/"):
        return False
    if _depth >= _MAX_COMPAT_DEPTH or ref in _seen:
        return False
    name = ref[len("#/$defs/"):].replace("~1", "/").replace("~0", "~")
    target = defs.get(name)
    if not isinstance(target, dict):
        return False
    return _is_unconstrained_schema(target, defs, _depth + 1, _seen | {ref})


def _same_object_schema_ignoring_empty_properties(model: Any, live: Any) -> bool:
    """Compare object shells, treating only an empty/missing properties map alike."""
    if not (isinstance(model, dict) and isinstance(live, dict)):
        return _compat_normalize(model) == _compat_normalize(live)
    if model.get("type") == live.get("type") == "object":
        model_properties = model.get("properties")
        live_properties = live.get("properties")
        if (model_properties == {} and "properties" not in live) or (
            live_properties == {} and "properties" not in model
        ):
            model = {key: value for key, value in model.items() if key != "properties"}
            live = {key: value for key, value in live.items() if key != "properties"}
    return _compat_normalize(model) == _compat_normalize(live)


def _forgive_nonidentity_marker(model: Any, live: Any) -> tuple[Any, Any]:
    """Pinning a sub-structure's ``__kind`` to the non-identity ``const ""`` is
    BACKWARD COMPATIBLE, whatever the live declaration was (free string,
    ``string | null``, the registry stamp): every reader normalizes an old
    value there to ``""`` (``markers.normalize_nonidentity_markers`` at kind
    validation and at the agent-output parse funnel; ``KindSubModel``'s
    before-validator in Python). So when the MODEL side declares it optional
    ``const ""`` and neither side requires it, the marker leaves the
    comparison on both sides. Drift detection is untouched (it compares
    structure, not compatibility), so the change is still published.
    """
    if not (isinstance(model, dict) and isinstance(live, dict)):
        return model, live
    model_props, live_props = model.get("properties"), live.get("properties")
    if not (isinstance(model_props, dict) and isinstance(model_props.get(KIND_KEY), dict)):
        return model, live
    if model_props[KIND_KEY].get("const") != "":
        return model, live
    if KIND_KEY in (model.get("required") or ()) or KIND_KEY in (live.get("required") or ()):
        return model, live

    live_marker = live_props.get(KIND_KEY) if isinstance(live_props, dict) else None
    branches = live_marker.get("anyOf") if isinstance(live_marker, dict) else None
    legacy_nullable = (
        isinstance(branches, list)
        and len(branches) == 2
        and {branch.get("type") for branch in branches if isinstance(branch, dict)}
        == {"string", "null"}
        and all(isinstance(branch, dict) and set(branch) == {"type"} for branch in branches)
    )
    if live_marker is not None and live_marker not in (
        {"type": "string"},
        {"type": "string", "const": ""},
    ) and not legacy_nullable:
        # A non-empty const or enum is identity, not an old spelling of the
        # non-identity slot. It remains a real compatibility constraint.
        return model, live

    def _without(node: dict[str, Any]) -> dict[str, Any]:
        props = node.get("properties")
        if not isinstance(props, dict) or KIND_KEY not in props:
            return node
        rest = {k: v for k, v in props.items() if k != KIND_KEY}
        out = {k: v for k, v in node.items() if k != "properties"}
        if rest:
            out["properties"] = rest
        return out

    return _without(model), _without(live) if isinstance(live_props, dict) else live


def _field_compatible(
    model_field: Any,
    live_field: Any,
    model_defs: dict[str, Any],
    live_defs: dict[str, Any],
    _depth: int = 0,
) -> bool:
    """Is ``model_field`` a backward-compatible replacement for ``live_field``?

    Identical structure is compatible. So is a field whose type moved to a
    SUPERSET object — a ``$ref`` swapped from ``AiUsage`` to a subclass that
    only adds optional fields is exactly the change a distillation makes when
    it declares the richer model a node was already emitting, and refusing it
    would force every such upgrade into a hand-written breaking change.
    Comparing the ``$ref`` NAMES would call that a type change; comparing what
    the names point AT does not.
    """
    # The registry write trigger adds this optional marker to every object.
    # Compare the producer's real constraints, not that storage normalization;
    # a declared/required discriminator survives this helper unchanged.
    model_field = _compat_normalize(model_field)
    live_field = _compat_normalize(live_field)
    model_field, live_field = _forgive_nonidentity_marker(model_field, live_field)
    model_field = strip_optional_schema_kind_stamps(model_field)
    live_field = strip_optional_schema_kind_stamps(live_field)

    if _is_unconstrained_schema(model_field, model_defs) and _is_unconstrained_schema(
        live_field, live_defs
    ):
        return True

    if _is_optional_marker_widening(model_field, live_field, model_defs, live_defs):
        return True

    # ``anyOf`` is a union.  Backward compatibility is set inclusion: every
    # old branch must still be accepted by at least one new branch.  Branch
    # order is presentation only, so a positional comparison both rejects a
    # real widening (the authored message-part union) and misclassifies a
    # harmless reorder.  Do not apply this rule to ``oneOf``: exclusivity can
    # make a superficially broader branch reject a previously valid payload.
    model_any_of = model_field.get("anyOf") if isinstance(model_field, dict) else None
    live_any_of = live_field.get("anyOf") if isinstance(live_field, dict) else None
    if isinstance(model_any_of, list):
        # Siblings constrain the whole union, not a branch.  Ignoring them
        # would incorrectly accept ``anyOf: [...]`` tightened by a sibling
        # ``additionalProperties: false``.
        model_siblings = {key: value for key, value in model_field.items() if key != "anyOf"}
        live_siblings = (
            {key: value for key, value in live_field.items() if key != "anyOf"}
            if isinstance(live_any_of, list)
            else {}
        )
        if _compat_normalize(model_siblings) != _compat_normalize(live_siblings):
            return False
        live_branches = live_any_of if isinstance(live_any_of, list) else [live_field]
        return all(
            any(
                _field_compatible(model_branch, live_branch, model_defs, live_defs, _depth + 1)
                for model_branch in model_any_of
            )
            for live_branch in live_branches
        )
    if isinstance(live_any_of, list):
        return all(
            _field_compatible(model_field, live_branch, model_defs, live_defs, _depth + 1)
            for live_branch in live_any_of
        )

    has_ref = isinstance(model_field, dict) and "$ref" in model_field
    has_ref = has_ref or (isinstance(live_field, dict) and "$ref" in live_field)
    if not has_ref:
        # A CONTAINER hides its ``$ref`` one level down: ``dict[str, X]`` puts
        # it under ``additionalProperties``, ``list[X]`` under ``items``. Those
        # must resolve too, or the same ref-name trap this function exists to
        # avoid simply moves inside the container — ``dict[str, AssetVariant]``
        # → ``dict[str, AssetVariantKind]`` was refused as a type change while
        # the two definitions were structurally identical (found 2026-08-21,
        # minting ``asset_variant``).
        if isinstance(model_field, dict) and isinstance(live_field, dict):
            resolved_containers: list[str] = []
            for container in ("additionalProperties", "items"):
                inner_model = model_field.get(container)
                inner_live = live_field.get(container)
                if not isinstance(inner_model, (bool, dict)) or not isinstance(
                    inner_live, (bool, dict)
                ):
                    continue
                contains_ref = any(
                    isinstance(inner, dict) and "$ref" in inner
                    for inner in (inner_model, inner_live)
                )
                same_open_schema = _is_unconstrained_schema(
                    inner_model, model_defs
                ) and _is_unconstrained_schema(inner_live, live_defs)
                if not contains_ref and not same_open_schema:
                    continue
                if not _field_compatible(
                    inner_model, inner_live, model_defs, live_defs, _depth + 1
                ):
                    return False
                resolved_containers.append(container)
            if resolved_containers:
                # The container's own keywords still have to match literally —
                # only schema-valued children were allowed to resolve.
                model_rest = {k: v for k, v in model_field.items() if k not in resolved_containers}
                live_rest = {k: v for k, v in live_field.items() if k not in resolved_containers}
                return _same_object_schema_ignoring_empty_properties(model_rest, live_rest)
        # Enum ordering is not validation semantics.  A new enum is compatible
        # only when it retains every old value; this intentionally keeps a
        # dropped value as a hard failure.
        if isinstance(model_field, dict) and isinstance(live_field, dict):
            model_enum = model_field.get("enum")
            live_enum = live_field.get("enum")
            if isinstance(model_enum, list) and isinstance(live_enum, list):
                model_rest = {key: value for key, value in model_field.items() if key != "enum"}
                live_rest = {key: value for key, value in live_field.items() if key != "enum"}
                return (
                    _compat_normalize(model_rest) == _compat_normalize(live_rest)
                    and all(
                        any(_json_value_equal(value, candidate) for candidate in model_enum)
                        for value in live_enum
                    )
                )
        # Pydantic's ``dict`` has both spellings.  They validate the same open
        # object language; a schema-valued ``additionalProperties`` remains a
        # real constraint and deliberately does not reach this branch.
        open_object_spellings = (
            {"type": "object"},
            {"type": "object", "additionalProperties": True},
        )
        if model_field in open_object_spellings and live_field in open_object_spellings:
            return True
        # No indirection — literal equality is the whole question.
        return _same_object_schema_ignoring_empty_properties(model_field, live_field)
    if _depth >= _MAX_COMPAT_DEPTH:
        return False

    # NEVER short-circuit on equal ``$ref`` STRINGS: the same "#/$defs/U" can
    # point at two different definitions across the two schemas, which is
    # precisely how a nested field silently becomes required.
    model_target = _compat_normalize(_resolve(model_field, model_defs))
    live_target = _compat_normalize(_resolve(live_field, live_defs))
    if not (isinstance(model_target, dict) and isinstance(live_target, dict)):
        return False
    model_target, live_target = _forgive_nonidentity_marker(model_target, live_target)
    model_target = strip_optional_schema_kind_stamps(model_target)
    live_target = strip_optional_schema_kind_stamps(live_target)
    # An UNCHANGED target is compatible whatever it is. Without this, any
    # ``$ref`` to a non-object definition — an enum, most commonly — was judged
    # a type change even when the two definitions were byte-identical, which
    # made every kind carrying a nested enum permanently un-evolvable
    # (``agent_assignment_batch_result`` was refused over its unchanged
    # ``AssignmentSessionStatus``, found 2026-08-20).
    if _json_value_equal(model_target, live_target):
        return True
    if model_target.get("type") != "object" or live_target.get("type") != "object":
        return False

    # An empty ``properties`` map and an omitted one are equivalent only when
    # every other object keyword is exactly the same. In particular, required,
    # additionalProperties, and size/conditional constraints remain visible.
    model_properties = model_target.get("properties")
    live_properties = live_target.get("properties")
    if (model_properties == {} and "properties" not in live_target) or (
        live_properties == {} and "properties" not in model_target
    ):
        model_other_constraints = {
            key: value
            for key, value in model_target.items()
            if key not in {"properties", "required", "additionalProperties"}
        }
        live_other_constraints = {
            key: value
            for key, value in live_target.items()
            if key not in {"properties", "required", "additionalProperties"}
        }
        if _compat_normalize(model_other_constraints) != _compat_normalize(
            live_other_constraints
        ):
            return False
        # Continue through the ordinary required/property and AP compatibility
        # checks below; empty properties must not bypass those constraints.
        if model_properties == {}:
            model_target = {key: value for key, value in model_target.items() if key != "properties"}
        if live_properties == {}:
            live_target = {key: value for key, value in live_target.items() if key != "properties"}

    model_props = model_target.get("properties") or {}
    live_props = live_target.get("properties") or {}
    model_required = set(model_target.get("required") or ())
    live_required = set(live_target.get("required") or ())

    # Following a reference must not erase the object's extra-key contract.
    # An old open object can carry fields the new closed object rejects; this
    # remains a real narrowing even when their named properties are identical.
    model_ap = model_target.get("additionalProperties", True)
    live_ap = live_target.get("additionalProperties", True)
    if live_ap is not False and model_ap is False:
        return False
    if _is_unconstrained_schema(live_ap, live_defs) and not _is_unconstrained_schema(
        model_ap, model_defs
    ):
        return False
    if isinstance(live_ap, dict):
        if model_ap is False or (
            isinstance(model_ap, dict)
            and not _field_compatible(model_ap, live_ap, model_defs, live_defs, _depth + 1)
        ):
            return False

    # Superset only: nothing removed, nothing newly required, every shared
    # field still compatible.
    if set(live_props) - set(model_props):
        return False  # a field disappeared
    if model_required - live_required:
        return False  # something became required — old payloads may lack it
    return all(
        _field_compatible(model_props[name], live_props[name], model_defs, live_defs, _depth + 1)
        for name in live_props
    )


def _is_optional_marker_widening(
    model_field: Any,
    live_field: Any,
    model_defs: dict[str, Any],
    live_defs: dict[str, Any],
) -> bool:
    """Recognize a deep-marker sweep on an otherwise untyped object.

    ``dict`` accepts every object, including the optional ``__kind`` injected
    into stored schemas by the marker-law sweep.  That stored marker is not a
    narrowing the Python producer needs to reproduce, so it must not force a
    fictional breaking evolution.  This deliberately covers only the exact
    marker-only object shape; real object constraints still use the ordinary
    compatibility comparison below.
    """
    if not isinstance(model_field, dict) or not isinstance(live_field, dict):
        return False
    model = _compat_normalize(model_field)
    live = _compat_normalize(live_field)
    model_any_of = model.get("anyOf")
    live_any_of = live.get("anyOf")
    if isinstance(model_any_of, list) and isinstance(live_any_of, list):
        model_siblings = {key: value for key, value in model.items() if key != "anyOf"}
        live_siblings = {key: value for key, value in live.items() if key != "anyOf"}
        return model_siblings == live_siblings and len(model_any_of) == len(live_any_of) and all(
            _is_optional_marker_widening(candidate, stored, model_defs, live_defs)
            or _compat_normalize(candidate) == _compat_normalize(stored)
            for candidate, stored in zip(model_any_of, live_any_of, strict=True)
        )
    # 🚨 An open object has TWO spellings and pydantic emits the one this
    # recognizer originally did not accept. ``dict``/``dict[str, Any]`` →
    # ``{"type": "object", "additionalProperties": true}``; a hand-written or
    # ``JsonValue``-derived schema → bare ``{"type": "object"}``. Both mean "any
    # object, no constraint", so both must be recognized — matching only the
    # bare spelling reported ``file_write_result`` as INCOMPATIBLE on
    # 2026-09-13 for a change nobody made and left the publisher with no way
    # out. ``additionalProperties`` carrying a SCHEMA is a real constraint and
    # is deliberately NOT folded in here.
    model_is_open = (
        isinstance(model, dict)
        and model.get("type") == "object"
        and set(model) <= {"type", "properties", "required", "additionalProperties"}
        and set(model.get("properties") or {}) <= {"__kind"}
        and set(model.get("required") or ()) <= {"__kind"}
        and "__kind" not in set(model.get("required") or ())
        and _is_unconstrained_schema(model.get("additionalProperties", True), model_defs)
    )
    if not model_is_open:
        return False
    properties = live.get("properties")
    return (
        live.get("type") == "object"
        and isinstance(properties, dict)
        and set(properties) == {"__kind"}
        and "__kind" not in set(live.get("required") or ())
        and live.get("additionalProperties", True) is True
        and set(live) <= {"type", "properties", "required", "additionalProperties"}
    )


#: Recursion bound for the structural comparison — deep enough for real kind
#: nesting, shallow enough that a cyclic schema cannot hang the gate.
_MAX_COMPAT_DEPTH = 6


def compatibility_verdict(
    model_schema: dict[str, Any], live_schema: dict[str, Any]
) -> CompatibilityVerdict:
    """Judge a proposed schema replacement against the live one."""
    model_props, model_required = _root_properties(model_schema)
    live_props, live_required = _root_properties(live_schema)

    breaking: list[str] = []
    additive: list[str] = []

    # Round-1 F8: the ROOT itself is part of the contract. A property walk
    # alone is blind to non-object roots ({"type":"string"} → integer read as
    # "compatible"), to map-rooted kinds whose value shape changes, and to
    # the textbook Confluent break of tightening an open root to
    # additionalProperties:false.
    def _root_of(schema: dict[str, Any]) -> dict[str, Any]:
        defs = schema.get("$defs")
        ref = schema.get("$ref")
        if isinstance(ref, str) and isinstance(defs, dict):
            target = defs.get(ref.rsplit("/", 1)[-1])
            if isinstance(target, dict):
                return target
        return schema

    model_root, live_root = _root_of(model_schema), _root_of(live_schema)
    model_type, live_type = model_root.get("type"), live_root.get("type")
    if live_type is not None and model_type != live_type:
        breaking.append(f"changes the ROOT type from {live_type!r} to {model_type!r}")
    model_ap, live_ap = (
        model_root.get("additionalProperties"),
        live_root.get("additionalProperties"),
    )
    if live_ap is not False and model_ap is False:
        breaking.append(
            "tightens the root to additionalProperties:false "
            "(old payloads with extra keys stop validating)"
        )
    if isinstance(live_ap, dict) and isinstance(model_ap, dict):
        if _compat_normalize(model_ap) != _compat_normalize(live_ap) and not _field_compatible(
            model_ap,
            live_ap,
            model_schema.get("$defs") or {},
            live_schema.get("$defs") or {},
        ):
            breaking.append("changes the map-value schema (additionalProperties)")

    for name in sorted(set(model_props) - set(live_props)):
        if name in model_required:
            breaking.append(f"adds REQUIRED field {name!r} (old payloads lack it)")
        else:
            additive.append(f"adds optional field {name!r}")

    for name in sorted(set(live_props) - set(model_props)):
        breaking.append(f"removes field {name!r}")

    model_defs = model_schema.get("$defs") if isinstance(model_schema.get("$defs"), dict) else {}
    live_defs = live_schema.get("$defs") if isinstance(live_schema.get("$defs"), dict) else {}
    for name in sorted(set(model_props) & set(live_props)):
        if not _field_compatible(model_props[name], live_props[name], model_defs, live_defs):
            breaking.append(f"changes the type/constraints of field {name!r}")
        elif _compat_normalize(model_props[name]) != _compat_normalize(live_props[name]):
            additive.append(f"widens field {name!r} to a superset shape")
        if name in model_required and name not in live_required:
            breaking.append(f"makes existing field {name!r} REQUIRED")

    return CompatibilityVerdict(
        compatible=not breaking,
        breaking=tuple(breaking),
        additive=tuple(additive),
    )
