"""The naming plan behind ``kind_create`` — every kind in a composed shape,
innermost first, resolved to the ONE name the caller must use, before anything
is written.

Each kind position (the root and every ``__kind``-marked nested object) goes
through the same steps (Arman, 2026-10-31):

1. A junk name (``kind_name_problem``) is a problem, with a real name offered.
2. The same SHAPE already exists (``schema_structure``, any name) → reuse it.
   Shapes of two fields or fewer must also share the name, so a tiny
   ``{name, url}`` never merges two unrelated concepts — unless the schema is
   byte-identical, which the frontend's fingerprint index treats as one kind
   anyway (``_duplicate_shape_refusal``).
3. The requested name exists and the caller's example fits its schema → reuse.
4. The name is taken by a different shape → REFUSED, naming the field
   difference and the two lawful doors: match the named kind, or evolve it
   (``kind_update_schema`` with a change note) and send again. A near-duplicate
   is never minted beside a named kind (Arman, 2026-11-02 — 55 ``<name>_2`` /
   ``<container>_<name>`` twins born in one day, each drifting from the kind
   its mandate binds). Only an explicit ``new_kind_reasons[name]`` mints a
   variant: a nested kind qualified by its container (``brand_profile`` +
   ``person`` → ``brand_profile_person``), then ``_2``, ``_3`` …, with the
   reason and the kind it varies stored on the new row's metadata.
   A requested name that IS such a variant of a live kind (``invoice_2``,
   ``<container>_<live kind>``) needs the same reason.
5. Otherwise the kind is new under the requested name.

A nested kind's final name is written into its container's markers before the
container is matched, so an outer shape built from existing parts can itself
be recognized as existing. Every problem is collected — one refusal lists them
all — and the plan writes nothing; ``kind_create`` writes it.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Literal

from matrx_graph.content_ir.sdk import disposition_refusal

from matrx_ai.tools.implementations import kind_shared
from matrx_ai.tools.implementations.kind_shared import (
    KIND_KEY,
    RESERVED_KIND_SLUGS,
    can_access_kind,
    collect_child_kind_fields,
    ensure_root_marker,
    infer_schema_from_sample,
    inject_kind_markers_into_schema,
    kind_name_problem,
    normalize_kind_slug,
    schema_fingerprint,
    schema_structure_key,
    suggested_kind_name,
    validate_against_schema,
)
from matrx_ai.tools.models import ToolContext

MAX_CHILD_DEPTH = 3
_MIN_FIELDS_FOR_NAME_FREE_MATCH = 3
_MAX_NUMBERED_SUFFIX = 50

NameStatus = Literal["created", "reused", "renamed"]

# What an example cannot say about a field and its kind's caller can: allowed
# values, a format, bounds, a description. Applied on top of the inferred (or
# written) schema; anything else is the shape itself and comes from the example.
FIELD_RULE_KEYWORDS = frozenset(
    {
        "description",
        "enum",
        "format",
        "pattern",
        "minLength",
        "maxLength",
        "minimum",
        "maximum",
        "minItems",
        "maxItems",
    }
)
_ITEM_RULE_KEYWORDS = frozenset(
    {"enum", "format", "pattern", "minLength", "maxLength", "minimum", "maximum"}
)


def _example_kind_names(node: Any) -> set[str]:
    names: set[str] = set()
    if isinstance(node, dict):
        if isinstance(node.get(KIND_KEY), str):
            names.add(normalize_kind_slug(node[KIND_KEY]))
        for value in node.values():
            names |= _example_kind_names(value)
    elif isinstance(node, list):
        for value in node:
            names |= _example_kind_names(value)
    return names


def apply_field_rules(wire: dict[str, Any], rules: dict[str, Any], *, where: str) -> list[str]:
    """Write ``{field: {keyword: value}}`` into ``wire``'s properties in place.
    A nullable field gets the rule on its non-null branch; an array of plain
    values gets value rules (enum, format, bounds) on its items. Returns every
    problem; applies nothing it refuses."""
    problems: list[str] = []
    props = wire.get("properties") if isinstance(wire.get("properties"), dict) else {}
    if not isinstance(rules, dict):
        return [f"{where}: field_rules must map each field name to its rules."]
    for fname, rule in rules.items():
        if fname not in props:
            problems.append(
                f"{where}.{fname}: field_rules names a field this kind does not have "
                f"(it has: {', '.join(sorted(props)) or 'no fields'})."
            )
            continue
        if not isinstance(rule, dict) or not rule:
            problems.append(
                f'{where}.{fname}: a field rule is an object such as {{"enum": [...]}}.'
            )
            continue
        unknown = sorted(set(rule) - FIELD_RULE_KEYWORDS)
        if unknown:
            problems.append(
                f"{where}.{fname}: {', '.join(unknown)} cannot be set here; field_rules takes "
                f"{', '.join(sorted(FIELD_RULE_KEYWORDS))}."
            )
            continue
        node = props[fname]
        target = node
        if isinstance(node.get("anyOf"), list):
            real = [b for b in node["anyOf"] if isinstance(b, dict) and b.get("type") != "null"]
            target = real[0] if len(real) == 1 else node
        elif isinstance(node.get("type"), list) and "null" in node["type"] and "enum" in rule:
            # A nullable enum still allows null.
            rule = {
                **rule,
                "enum": [*rule["enum"], None] if None not in rule["enum"] else rule["enum"],
            }
        for key, value in rule.items():
            if key == "description":
                node["description"] = value
                continue
            items = target.get("items")
            if (
                target.get("type") == "array"
                and key in _ITEM_RULE_KEYWORDS
                and isinstance(items, dict)
                and items.get("type") not in ("object", "array")
            ):
                items[key] = value
            elif key in ("properties", "items"):
                continue
            else:
                target[key] = value
    return problems


@dataclass
class PlannedKind:
    """One kind position's resolution. ``row`` is the existing kind when reused."""

    requested: str
    final: str
    status: NameStatus
    path: str
    marked: dict[str, Any]
    wire_schema: dict[str, Any] | None = None
    block_schema: dict[str, Any] | None = None
    row: Any | None = None
    disposition: str | None = None
    note: str | None = None
    children: list[tuple[str, PlannedKind, bool]] = field(default_factory=list)
    # A deliberate variant of a live kind: which one, and the caller's stated reason.
    variant_of: str | None = None
    new_kind_reason: str | None = None

    @property
    def writes(self) -> bool:
        return self.status != "reused"


@dataclass
class KindPlan:
    root: PlannedKind | None
    problems: list[str]

    def every_kind(self) -> list[PlannedKind]:
        """Every kind the plan reaches, innermost first, each once. A reused
        kind's own children are not reached — nothing below it is written."""
        seen: set[int] = set()
        out: list[PlannedKind] = []

        def walk(node: PlannedKind) -> None:
            if id(node) in seen:
                return
            seen.add(id(node))
            if node.writes:
                for _f, child, _l in node.children:
                    walk(child)
            out.append(node)

        if self.root is not None:
            walk(self.root)
        return out


def find_blank_markers(value: Any, path: str = "") -> list[str]:
    """Paths of every ``__kind`` marker anywhere in ``value`` that is not a
    non-empty string. ``collect_child_kind_fields`` silently treats a blank
    marker as plain data; a blank kind is refused instead."""
    found: list[str] = []
    if isinstance(value, dict):
        if KIND_KEY in value:
            marker = value[KIND_KEY]
            if not isinstance(marker, str) or not marker.strip():
                found.append(path or "(root)")
        for key, item in value.items():
            if key != KIND_KEY:
                found += find_blank_markers(item, f"{path}.{key}" if path else key)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            found += find_blank_markers(item, f"{path}[{i}]")
    return found


def _with_marker(value: Any, slug: str) -> Any:
    return ensure_root_marker(value, slug) if isinstance(value, dict) else value


def _apply_names(value: Any, node: PlannedKind) -> Any:
    """``value`` as an instance of ``node``: its marker is the final name, and
    so is every nested kind's marker below it, at every depth."""
    if not isinstance(value, dict):
        return value
    return ensure_root_marker(_rename_children(value, node.children), node.final)


def _rename_children(
    value: dict[str, Any], children: list[tuple[str, PlannedKind, bool]]
) -> dict[str, Any]:
    if not children:
        return value
    out = dict(value)
    for fname, child, is_list in children:
        item = out.get(fname)
        names = {child.requested, child.final}
        if is_list and isinstance(item, list):
            out[fname] = [
                _apply_names(i, child) if isinstance(i, dict) and i.get(KIND_KEY) in names else i
                for i in item
            ]
        elif isinstance(item, dict):
            out[fname] = _apply_names(item, child)
    return out


def _field_names(schema: Any) -> list[str]:
    props = schema.get("properties") if isinstance(schema, dict) else None
    return sorted(k for k in (props or {}) if k != KIND_KEY)


class KindPlanner:
    def __init__(
        self,
        ctx: ToolContext,
        *,
        child_dispositions: dict[str, str] | None = None,
        platform: bool = False,
        field_rules: dict[str, Any] | None = None,
        new_kind_reasons: dict[str, str] | None = None,
    ) -> None:
        self.ctx = ctx
        self.child_dispositions = dict(child_dispositions or {})
        # Keyed by the kind name as the caller wrote it in the example.
        self.field_rules = {normalize_kind_slug(k): v for k, v in (field_rules or {}).items()}
        # Keyed like field_rules: the name the caller wrote → why it is NOT the live kind of
        # that name. The only door to a suffixed/qualified variant of an existing kind.
        self.new_kind_reasons = {
            normalize_kind_slug(k): v.strip()
            for k, v in (new_kind_reasons or {}).items()
            if isinstance(v, str) and v.strip()
        }

        # A platform mint is published to the web; it may only reuse kinds that are too,
        # or a public kind would point at an organization's private one.
        self.platform = platform
        self.problems: list[str] = []
        self.undeclared: list[str] = []
        self._claimed: set[str] = set()
        self._memo: dict[tuple[str, str], PlannedKind] = {}
        self._by_structure: dict[str, list[Any]] | None = None
        # Active hand-authored kinds by wire fingerprint: the rows the database's
        # `guard_kind_shape_uniqueness` refuses a byte-identical new kind against,
        # whoever can see them.
        self._blocking: dict[str, list[Any]] = {}
        self._planned_by_fingerprint: dict[str, PlannedKind] = {}
        self._live_by_slug: dict[str, list[Any]] = {}
        self._viewable: dict[str, bool] = {}

    # -- registry reads ----------------------------------------------------

    async def _structure_index(self) -> dict[str, list[Any]]:
        if self._by_structure is None:
            KindDefinition = kind_shared.get_db_model("KindDefinition")
            index: dict[str, list[Any]] = {}
            for row in await KindDefinition.filter(is_active=True).all():
                if row.deleted_at is not None or getattr(row, "is_contract_artifact", False):
                    continue
                if not isinstance(row.emitted_json_schema, dict):
                    continue
                key, _fields = schema_structure_key(row.emitted_json_schema)
                index.setdefault(key, []).append(row)
                if (
                    row.emitted_fingerprint
                    and (row.metadata or {}).get("family") == "user_authored"
                ):
                    self._blocking.setdefault(row.emitted_fingerprint, []).append(row)
            self._by_structure = index
        return self._by_structure

    async def _live(self, slug: str) -> list[Any]:
        """Live rows holding ``slug`` — slugs are global, so this is NOT scoped
        to the caller (``kind_definition_global_slug_unique``)."""
        if slug not in self._live_by_slug:
            KindDefinition = kind_shared.get_db_model("KindDefinition")
            self._live_by_slug[slug] = [
                r for r in await KindDefinition.filter(kind=slug).all() if r.deleted_at is None
            ]
        return self._live_by_slug[slug]

    async def _can_reuse(self, row: Any, *, as_child: bool = False) -> bool:
        if self.platform and not getattr(row, "published_to_web", False):
            return False
        if as_child and not self._parent_audience_reads(row):
            return False
        return await self._can_view(row)

    def _parent_audience_reads(self, row: Any) -> bool:
        """Whether everyone who can read the kind being WRITTEN can read ``row`` as its child.

        The caller seeing a kind is not enough: the parent's edge is read by the parent's
        audience. A parent written into the System organization (a caller whose active org is
        the platform tenant) reused a child private to another organization, and every catalog
        reader then met an edge to a child it could not see (kind_edge 221e5eed, app_log
        a9c125af). A child is reusable when it is published, in the System organization, or in
        the organization the parent is written into; otherwise a kind of its own is planned."""
        if getattr(row, "published_to_web", False):
            return True
        child_org = str(getattr(row, "organization_id", "") or "")
        system_org = kind_shared.system_organization_id()
        target_org = system_org if self.platform else (kind_shared.ctx_org_id(self.ctx) or "")
        return child_org in {system_org, target_org}

    async def _can_view(self, row: Any) -> bool:
        key = str(row.id)
        if key not in self._viewable:
            self._viewable[key] = await can_access_kind(row, self.ctx, "viewer")
        return self._viewable[key]

    async def _name_is_free(self, slug: str) -> bool:
        return (
            slug not in self._claimed
            and slug not in RESERVED_KIND_SLUGS
            and kind_name_problem(slug) is None
            and not await self._live(slug)
        )

    # -- matching ------------------------------------------------------------

    @staticmethod
    def _fits(row: Any, instances: list[dict[str, Any]]) -> bool:
        schema = row.emitted_json_schema
        if not isinstance(schema, dict):
            return False
        return all(
            not validate_against_schema(_with_marker(i, row.kind), schema) for i in instances
        )

    async def _existing_by_shape(
        self,
        requested: str,
        block_schema: dict[str, Any],
        fingerprint: str,
        instances: list[dict[str, Any]],
        strict: bool,
        *,
        as_child: bool = False,
    ) -> Any | None:
        """``strict``: the caller wrote the schema itself, so its enums, required
        fields and bounds are part of what it asked for — only a byte-identical
        schema may stand in for it."""
        key, fields = schema_structure_key(block_schema)
        candidates = (await self._structure_index()).get(key, [])

        def rank(row: Any) -> tuple[int, int, str]:
            return (
                0 if row.kind == requested else 1,
                0 if (row.metadata or {}).get("family") == "user_authored" else 1,
                str(getattr(row, "created_at", "") or ""),
            )

        for row in sorted(candidates, key=rank):
            same_name = row.kind == requested
            identical = row.emitted_fingerprint == fingerprint
            if strict and not identical:
                continue
            if fields < _MIN_FIELDS_FOR_NAME_FREE_MATCH and not (same_name or identical):
                continue
            if await self._can_reuse(row, as_child=as_child) and self._fits(row, instances):
                return row
        return None

    async def _new_name(self, requested: str, parent: str | None) -> str | None:
        bases = []
        if parent and not requested.startswith(f"{parent}_"):
            bases.append(normalize_kind_slug(f"{parent}_{requested}"))
        bases.append(requested)
        for base in bases:
            if await self._name_is_free(base):
                return base
        base = bases[0]
        for n in range(2, _MAX_NUMBERED_SUFFIX + 1):
            candidate = f"{base}_{n}"
            if await self._name_is_free(candidate):
                return candidate
        return None

    async def _variant_base(self, slug: str, parent: str | None) -> str | None:
        """The live kind ``slug`` is a suffixed or container-qualified variant of
        (``invoice_2`` → ``invoice``; ``brand_profile_person`` under
        ``brand_profile`` → ``person``), else None."""
        stem, sep, tail = slug.rpartition("_")
        if sep and tail.isdigit() and stem and await self._live(stem):
            return stem
        if parent and slug.startswith(f"{parent}_"):
            inner = slug[len(parent) + 1 :]
            if inner and inner != parent and await self._live(inner):
                return inner
        return None

    def _reason_for(self, requested: str) -> str | None:
        return self.new_kind_reasons.get(requested)

    async def _taken_problem(
        self, path: str, requested: str, wire: dict[str, Any], *, variant: str | None = None
    ) -> str:
        """Why a near-duplicate of a named kind is not minted, and the doors that are open."""
        name = variant or requested
        doors = (
            f"Use '{name}' — match its schema — or evolve it first with "
            f"kind_update_schema(kind='{name}', json_schema=…, change_note='what changed and "
            "why') so it holds your fields, then send this again"
        )
        escape = (
            f". Only if this is genuinely not a '{name}', give it a name that says how it "
            f"differs, or pass new_kind_reasons={{'{requested}': '<why it is not {name}>'}}."
        )
        if variant:
            return (
                f"{path}: '{requested}' is a numbered or container-qualified copy of the "
                f"existing kind '{variant}' — a second kind beside a named one is never "
                f"minted without a stated reason. {doors}{escape}"
            )
        if requested in self._claimed:
            return (
                f"{path}: '{requested}' names two different shapes in this one call. Mark "
                "both with the same fields, or give one of them a name that says how it "
                "differs."
            )
        if requested in RESERVED_KIND_SLUGS:
            return f"{path}: '{requested}' is a reserved name — name the kind for what it holds."
        holders = await self._live(requested)
        if not holders or not await self._can_view(holders[0]):
            return (
                f"{path}: '{requested}' is held by a kind you cannot see. Give this one a "
                "name that says what it is" + escape
            )
        held = holders[0]
        theirs, mine = set(_field_names(held.emitted_json_schema)), set(_field_names(wire))
        diff = []
        if mine - theirs:
            diff.append(f"yours adds {', '.join(sorted(mine - theirs))}")
        if theirs - mine:
            diff.append(f"yours lacks {', '.join(sorted(theirs - mine))}")
        if not diff:
            diff.append("same fields, different types, required fields or rules")
        owner = (held.metadata or {}).get("family")
        if owner and owner != "user_authored":
            doors += f" ('{name}' is published from code, family '{owner}': evolve its model there)"
        return (
            f"{path}: '{requested}' already exists with a different shape "
            f"({'; '.join(diff)}). A near-duplicate is never minted beside a named kind. "
            f"{doors}{escape}"
        )

    # -- the plan ------------------------------------------------------------

    async def plan(
        self,
        *,
        name: str,
        sample: dict[str, Any],
        json_schema: dict[str, Any] | None,
        required_fields: list[str] | None,
        disposition: str | None,
    ) -> KindPlan:
        for path in find_blank_markers(sample):
            self.problems.append(
                f"{path}: '__kind' is empty — every kind marker must name the shape it marks."
            )
        root = None
        if not self.problems:
            root = await self._plan_position(
                raw_name=name,
                sample=sample,
                instances=[sample],
                depth=0,
                parent=None,
                field_name=None,
                path=normalize_kind_slug(name) or "(root)",
                json_schema=json_schema,
                required_fields=required_fields,
                disposition=disposition,
            )
        unused = sorted(
            set(self.field_rules) - _example_kind_names(sample) - {normalize_kind_slug(name)}
        )
        if unused:
            self.problems.append(
                "field_rules names kinds that are not in the example: "
                + ", ".join(repr(n) for n in unused)
                + ". Key field_rules by the __kind names the example uses."
            )
        if self.undeclared:
            self.problems.append(
                "These new kinds do not say what their output is: "
                + ", ".join(repr(n) for n in sorted(set(self.undeclared)))
                + ". Pass disposition for the root and child_dispositions "
                "{name: record|prose|proposal|receipt|envelope} for each nested one."
            )
        return KindPlan(root=root if not self.problems else None, problems=self.problems)

    async def _plan_position(
        self,
        *,
        raw_name: str,
        sample: dict[str, Any],
        instances: list[dict[str, Any]],
        depth: int,
        parent: str | None,
        field_name: str | None,
        path: str,
        json_schema: dict[str, Any] | None = None,
        required_fields: list[str] | None = None,
        disposition: str | None = None,
    ) -> PlannedKind | None:
        requested = normalize_kind_slug(raw_name)
        problem = kind_name_problem(requested)
        if problem:
            hint = suggested_kind_name(parent, field_name)
            self.problems.append(
                f"{path}: '{raw_name}' is not a usable kind name ({problem})."
                + (
                    f" Use a name that says what it is, e.g. '{hint}'."
                    if hint
                    else " Use a name that says what the shape is."
                )
            )
            return None
        if depth > MAX_CHILD_DEPTH:
            self.problems.append(
                f"{path}: nested kinds go at most {MAX_CHILD_DEPTH} levels deep — "
                "flatten this branch or build it as its own kind first."
            )
            return None

        marked = ensure_root_marker(sample, requested)
        try:
            child_fields = collect_child_kind_fields(marked, requested)
        except ValueError as exc:
            self.problems.append(f"{path}: {exc}")
            return None

        children: list[tuple[str, PlannedKind, bool]] = []
        failed = False
        for fname, info in child_fields.items():
            value = marked[fname]
            child_instances = (
                [i for i in value if isinstance(i, dict) and i.get(KIND_KEY) == info["slug"]]
                if info["is_list"]
                else [value]
            )
            child = await self._plan_position(
                raw_name=info["slug"],
                sample=info["sample"],
                instances=child_instances,
                depth=depth + 1,
                parent=requested,
                field_name=fname,
                path=f"{path}.{fname}" + ("[]" if info["is_list"] else ""),
            )
            if child is None:
                failed = True
                continue
            children.append((fname, child, info["is_list"]))
        marked = _rename_children(marked, children)
        if failed:
            # Still name a rule for a field this kind lacks, so one refusal lists everything.
            rules = self.field_rules.get(requested)
            if isinstance(rules, dict):
                fields = {k for k in marked if k != KIND_KEY}
                self.problems.extend(
                    f"{path}.{f}: field_rules names a field this kind does not have "
                    f"(it has: {', '.join(sorted(fields))})."
                    for f in rules
                    if f not in fields
                )
            return None

        try:
            wire = (
                copy.deepcopy(json_schema)
                if json_schema is not None
                else (infer_schema_from_sample(marked, required_fields=required_fields))
            )
        except ValueError as exc:
            self.problems.append(f"{path}: {exc}")
            return None
        rules = self.field_rules.get(requested)
        if rules is not None:
            rule_problems = apply_field_rules(wire, rules, where=path)
            if not rule_problems:
                for instance in instances:
                    rule_problems.extend(
                        f"{path}: the example breaks field_rules — {e}"
                        for e in validate_against_schema(_rename_children(instance, children), wire)
                    )
            if rule_problems:
                self.problems.extend(rule_problems)
                return None
        block = inject_kind_markers_into_schema(wire, marked, requested)
        fingerprint = schema_fingerprint(wire)
        structure, _fields = schema_structure_key(block)
        memo_key = (requested, structure)
        if memo_key in self._memo:
            return self._memo[memo_key]

        # The caller's instances, carrying the final child names, to fit-test against.
        fit_instances = (
            [marked] if depth == 0 else [_rename_children(i, children) for i in instances]
        )

        node: PlannedKind
        # Stated rules are part of what was asked for, like a written schema.
        strict = json_schema is not None or rules is not None
        existing = await self._existing_by_shape(
            requested, block, fingerprint, fit_instances, strict, as_child=depth > 0
        )
        if existing is None:
            for row in await self._live(requested):
                if strict and row.emitted_fingerprint != fingerprint:
                    continue
                if await self._can_reuse(row, as_child=depth > 0) and self._fits(row, fit_instances):
                    existing = row
                    break
        if existing is not None:
            note = None
            if existing.kind != requested:
                note = f"An existing kind '{existing.kind}' already has this shape; use it."
            node = PlannedKind(
                requested=requested,
                final=existing.kind,
                status="reused",
                path=path,
                marked=ensure_root_marker(marked, existing.kind),
                row=existing,
                note=note,
                children=children,
            )
        else:
            # Two names for one byte-identical shape are refused by the database, so a
            # shape already planned in this call is the same kind, and one already
            # registered (but not reusable here) is a problem stated now, never a
            # failed write after a green plan.
            twin = self._planned_by_fingerprint.get(fingerprint)
            if twin is not None:
                if schema_structure_key(twin.block_schema or {})[0] == structure:
                    self._memo[memo_key] = twin
                    return twin
                self.problems.append(
                    f"{path}: has exactly the fields of {twin.path} but different nested "
                    "kinds — two kinds cannot share one set of fields. Add or rename a "
                    "field so the shapes differ, or mark both with the same nested kinds."
                )
                return None
            await self._structure_index()
            holders = self._blocking.get(fingerprint, [])
            if holders:
                seen = holders[0]
                if depth > 0 and not self._parent_audience_reads(seen) and await self._can_view(seen):
                    self.problems.append(
                        f"{path}: has exactly the fields of the kind '{seen.kind}', which belongs "
                        "to another organization and is not published, so readers of the kind "
                        f"you are creating could not open it. Publish '{seen.kind}', or add a "
                        "field that makes this shape different."
                    )
                elif await self._can_view(seen):
                    self.problems.append(
                        f"{path}: has exactly the fields of the existing kind '{seen.kind}', "
                        "which this example does not fit (or nests different kinds). Use "
                        f"'{seen.kind}' and match its schema, or add a field that makes "
                        "this shape different."
                    )
                else:
                    self.problems.append(
                        f"{path}: a kind you cannot see already has exactly these fields. "
                        "Add a field that makes this shape different, or ask for access."
                    )
                return None
            final = requested
            status: NameStatus = "created"
            note = None
            variant_of: str | None = None
            reason: str | None = None
            if not await self._name_is_free(requested):
                # A name held by a different shape is the named kind's to evolve, never a
                # reason to mint `<name>_2` / `<container>_<name>` beside it.
                reason = self._reason_for(requested)
                if reason is None:
                    self.problems.append(await self._taken_problem(path, requested, wire))
                    return None
                variant_of = requested
                renamed = await self._new_name(requested, parent)
                if renamed is None:
                    self.problems.append(
                        f"{path}: every name built from '{requested}' is taken — "
                        "pick a name that says what makes this shape different."
                    )
                    return None
                final, status = renamed, "renamed"
                holders = await self._live(requested)
                if holders and await self._can_view(holders[0]):
                    theirs = _field_names(holders[0].emitted_json_schema)
                    mine = _field_names(wire)
                    note = (
                        f"'{requested}' is already a different kind (fields: "
                        f"{', '.join(theirs) or 'none'}; yours: {', '.join(mine) or 'none'}), "
                        f"so this one is '{final}'."
                    )
                else:
                    note = f"'{requested}' is already taken, so this one is '{final}'."
                note += f" Reason given: {reason}"
            else:
                variant_of = await self._variant_base(requested, parent)
                if variant_of is not None:
                    reason = self._reason_for(requested)
                    if reason is None:
                        self.problems.append(
                            await self._taken_problem(path, requested, wire, variant=variant_of)
                        )
                        return None
            self._claimed.add(final)
            final_marked = ensure_root_marker(marked, final)
            final_block = inject_kind_markers_into_schema(wire, final_marked, final)
            errors = validate_against_schema(final_marked, final_block)
            if errors:
                self.problems.append(
                    f"{path}: the example does not validate against the schema: {errors[:6]}"
                )
                return None
            stated = (
                disposition
                if depth == 0
                else (self.child_dispositions.get(requested) or self.child_dispositions.get(final))
            )
            if disposition_refusal(final, stated):
                self.undeclared.append(requested)
            node = PlannedKind(
                requested=requested,
                final=final,
                status=status,
                path=path,
                marked=final_marked,
                wire_schema=wire,
                block_schema=final_block,
                disposition=stated,
                note=note,
                children=children,
                variant_of=variant_of,
                new_kind_reason=reason,
            )
        if node.writes:
            self._planned_by_fingerprint[fingerprint] = node
        self._memo[memo_key] = node
        return node
