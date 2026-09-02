"""The drift-detection engine.

Pure logic: it takes the *code* registry (:func:`matrx_ai.tools.declared.declared_tools`)
and a list of *database* rows (``tool_def`` joined to ``tool_binding``), and
returns a :class:`ValidationReport` describing every divergence. It performs no
I/O — the CLI and the admin API do the fetching and the printing — so it is
trivially testable and stays package-independent.

It enforces:

* **R2 — arguments.** The Pydantic args model and ``tool_def.parameters`` must
  describe the identical set of parameters (name, type, required, default, and
  per-field enum members). For multi-action *dispatcher* tools this is checked
  per action: a code discriminated-union RootModel vs the DB ``$variants`` map,
  plus the discriminator's enum members. Per-field enum drift is ERROR when
  both sides constrain but disagree, WARNING when only one side constrains
  (non-breaking, but the code model should be tightened to a Literal so the
  executor enforces what the DB advertises).
* **R3 — ownership, both directions.** Every code tool must exist in the DB
  (``MISSING_IN_DB``) and every locally-owned DB tool must exist in code
  (``MISSING_IN_CODE``). ``source_kind`` and the executor binding must agree.

Location drift (the old R1) is no longer checked — the schema's
``function_path`` column was dropped. The @tool decorator records the
function's location in-memory only; the DB does not store it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from matrx_ai.tools.declared import DeclaredFamily, DeclaredTool
from matrx_ai.tools.validation.schema import (
    CanonParam,
    canon_db_params,
    canon_db_variants,
    canon_model_params,
    canon_model_variant,
    db_discriminator_enum,
    discriminated_union_members,
)


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class FindingKind(str, Enum):
    MISSING_IN_DB = "missing_in_db"  # R3: code has it, DB doesn't
    MISSING_IN_CODE = "missing_in_code"  # R3: DB has it, code doesn't
    OWNER_DRIFT = "owner_drift"  # R3: source_kind differs
    EXECUTOR_DRIFT = "executor_drift"  # R3: executor binding differs
    ARG_DRIFT = "arg_drift"  # R2: params differ (type/required/default/set)
    DEPRECATED_ACTIVE = "deprecated_active"  # code says deprecated, DB still active
    INACTIVE_IN_DB = "inactive_in_db"  # code declares it, DB row is inactive


@dataclass(frozen=True)
class Finding:
    kind: FindingKind
    severity: Severity
    tool_name: str
    message: str
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "severity": self.severity.value,
            "tool_name": self.tool_name,
            "message": self.message,
            "detail": self.detail,
        }


@dataclass
class ValidationReport:
    findings: list[Finding] = field(default_factory=list)
    code_count: int = 0
    db_count: int = 0
    external_count: int = 0
    exempt: list[str] = field(default_factory=list)
    checked: list[str] = field(default_factory=list)
    # Tools whose function does NOT actually use its registered args model — i.e.
    # the model is a DB-shaped mirror the code ignores, so diffing it against the DB
    # is circular and proves nothing. Populated by the runner (needs code reflection).
    # Each entry: {tool_name, model, function_path}.
    unverified: list[dict[str, Any]] = field(default_factory=list)

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity is Severity.ERROR]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity is Severity.WARNING]

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def fully_verified(self) -> bool:
        """True only when there is no drift AND every owned tool's real code is
        actually bound to a checkable contract. A green result REQUIRES this — a
        check that cannot fail (circular DB-mirror models) is not a pass."""
        return self.ok and not self.unverified

    def for_tool(self, name: str) -> list[Finding]:
        return [f for f in self.findings if f.tool_name == name]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "summary": {
                "code_count": self.code_count,
                "db_count": self.db_count,
                "external_count": self.external_count,
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "exempt": len(self.exempt),
            },
            "findings": [f.to_dict() for f in self.findings],
        }


@dataclass(frozen=True)
class DbTool:
    """Normalised view of a ``tool_def`` row + its executor bindings."""

    name: str
    source_kind: str
    parameters: Any
    description: str
    is_active: bool
    validation_exempt: bool
    executors: tuple[str, ...]

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> DbTool:
        raw_executors = row.get("executors")
        if isinstance(raw_executors, str):
            executors = tuple(s for s in (x.strip() for x in raw_executors.split(",")) if s)
        elif isinstance(raw_executors, (list, tuple)):
            executors = tuple(str(s) for s in raw_executors)
        else:
            executors = ()
        return cls(
            name=row["name"],
            source_kind=row.get("source_kind") or "",
            parameters=row.get("parameters"),
            description=row.get("description") or "",
            is_active=bool(row.get("is_active", True)),
            validation_exempt=bool(row.get("validation_exempt", False)),
            executors=executors,
        )


def _match_family(name: str, families: list[DeclaredFamily]) -> DeclaredFamily | None:
    """Longest-prefix family match for ``name`` (deterministic), or None."""
    best: DeclaredFamily | None = None
    for fam in families:
        if name.startswith(fam.name_prefix) and (
            best is None or len(fam.name_prefix) > len(best.name_prefix)
        ):
            best = fam
    return best


def validate(
    code: dict[str, DeclaredTool],
    db_rows: list[dict[str, Any]],
    *,
    owner_executors: set[str],
    families: list[DeclaredFamily] | None = None,
) -> ValidationReport:
    """Diff the code registry against DB rows for the executor(s) that THIS repo owns.

    Per the two-input rule (common-docs/systems/agents/agent-tools/DECISIONS.md Part 1), ownership
    is derived from executor BINDING — not from ``source_kind``, which is too
    coarse to distinguish "implemented in this repo" from "implemented in another
    repo's runtime" (matrx-local, matrx-extend, matrx-frontend).

    Args:
        code: ``{name: DeclaredTool}`` — the code source of truth.
        db_rows: ``tool_def`` rows (each a dict, with an ``executors`` key
            carrying the tool's ``tool_binding.executor_name`` values).
        owner_executors: executor names whose DB rows are expected to have
            backing @tool code in THIS repo (typically
            ``{"matrx-ai-core", "aidream"}``). A DB row whose bindings don't
            intersect this set is reported as ``external`` and never flagged
            as ``missing_in_code``.

    Descriptions are intentionally NOT compared: descriptions are not code,
    they live only in the DB (``tool_def.description``). The gate checks only
    the elements code depends on — identity, ownership (via binding), and the
    argument contract. The schema's ``function_path`` column was dropped, so
    location drift is no longer a check — the @tool decorator records the
    function's location in-memory only.
    """
    families = families or []
    report = ValidationReport()
    db_by_name: dict[str, DbTool] = {}
    for row in db_rows:
        try:
            dt = DbTool.from_row(row)
        except KeyError:
            continue
        db_by_name[dt.name] = dt

    def _is_owned(db: DbTool) -> bool:
        return bool(set(db.executors) & owner_executors)

    report.db_count = sum(1 for d in db_by_name.values() if _is_owned(d))
    report.external_count = sum(1 for d in db_by_name.values() if not _is_owned(d))
    report.code_count = len(code)

    # ── Direction 1: every code tool must have a matching, correct DB row ──
    for name, ct in code.items():
        if not ct.validate or ct.deprecated:
            report.exempt.append(name)
            db = db_by_name.get(name)
            if ct.deprecated and db is not None and db.is_active:
                report.findings.append(
                    Finding(
                        FindingKind.DEPRECATED_ACTIVE,
                        Severity.WARNING,
                        name,
                        "Tool is marked deprecated in code but is still is_active=true in the DB.",
                    )
                )
            continue

        # Only validate code declarations whose declared executor is one we own.
        # An external @tool (e.g. an aidream-side declaration that registers a
        # matrx-local tool placeholder) would otherwise spuriously fail.
        if ct.executor is not None and ct.executor not in owner_executors:
            continue

        report.checked.append(name)
        db = db_by_name.get(name)
        if db is None:
            report.findings.append(
                Finding(
                    FindingKind.MISSING_IN_DB,
                    Severity.ERROR,
                    name,
                    f"Declared in code ({ct.function_path}) but no tool_def row exists.",
                    {"function_path": ct.function_path, "source_kind": ct.source_kind},
                )
            )
            continue

        if db.validation_exempt:
            report.exempt.append(name)
            continue

        if not db.is_active:
            report.findings.append(
                Finding(
                    FindingKind.INACTIVE_IN_DB,
                    Severity.WARNING,
                    name,
                    "Tool is declared & active in code but is_active=false in the DB.",
                )
            )

        # R3 — ownership (source_kind). Now an advisory check — we still flag
        # divergence because someone is wrong, but it's not the primary
        # ownership signal anymore.
        if ct.source_kind != db.source_kind:
            report.findings.append(
                Finding(
                    FindingKind.OWNER_DRIFT,
                    Severity.WARNING,
                    name,
                    f"source_kind differs: code={ct.source_kind!r} db={db.source_kind!r}",
                    {"code": ct.source_kind, "db": db.source_kind},
                )
            )

        # R3 — executor binding. THE primary ownership signal.
        if ct.executor is not None and db.executors and ct.executor not in db.executors:
            report.findings.append(
                Finding(
                    FindingKind.EXECUTOR_DRIFT,
                    Severity.ERROR,
                    name,
                    f"executor {ct.executor!r} not among tool_binding executors {list(db.executors)}",
                    {"code": ct.executor, "db": list(db.executors)},
                )
            )

        # R2 — arguments
        _diff_args(name, ct, db, report)

    # ── Direction 2: every locally-owned DB tool must have code ──
    for name, db in db_by_name.items():
        if not _is_owned(db):
            continue
        if db.validation_exempt or not db.is_active:
            if db.validation_exempt:
                report.exempt.append(name)
            continue
        if name in code:
            continue  # already checked in Direction 1

        # A generic family (e.g. ``bundle:list_*``) backs this row with ONE shared
        # implementation — there is no per-member @tool declaration by design.
        # Materialise the family for this name and check it exactly like a
        # singly-declared tool (executor binding + argument contract), so the
        # row is genuinely verified, not merely silenced.
        fam = _match_family(name, families)
        if fam is not None:
            ct = fam.as_declared(name)
            if not ct.validate or ct.deprecated:
                report.exempt.append(name)
                continue
            report.checked.append(name)
            if ct.executor is not None and db.executors and ct.executor not in db.executors:
                report.findings.append(
                    Finding(
                        FindingKind.EXECUTOR_DRIFT,
                        Severity.ERROR,
                        name,
                        f"executor {ct.executor!r} not among tool_binding executors "
                        f"{list(db.executors)}",
                        {"code": ct.executor, "db": list(db.executors)},
                    )
                )
            _diff_args(name, ct, db, report)
            continue

        report.findings.append(
            Finding(
                FindingKind.MISSING_IN_CODE,
                Severity.ERROR,
                name,
                f"tool_def row bound to {list(db.executors)} has no @tool declaration in code.",
                {"executors": list(db.executors), "source_kind": db.source_kind},
            )
        )

    return report


def _diff_args(
    name: str,
    ct: DeclaredTool,
    db: DbTool,
    report: ValidationReport,
) -> None:
    # Multi-action dispatchers carry a per-action contract on BOTH sides (a code
    # discriminated-union RootModel and a DB ``$variants`` map). If either side is
    # dispatcher-shaped, diff per action; otherwise take the ordinary flat path.
    union = discriminated_union_members(ct.args_model)
    db_variants = canon_db_variants(db.parameters)
    if union is not None or db_variants is not None:
        _diff_args_dispatcher(name, ct, db, report, union, db_variants)
        return

    _diff_param_maps(
        name,
        canon_model_params(ct.args_model),
        canon_db_params(db.parameters),
        report,
    )


def _diff_param_maps(
    name: str,
    code_params: dict[str, CanonParam],
    db_params: dict[str, CanonParam],
    report: ValidationReport,
    *,
    scope: str | None = None,
) -> None:
    """Diff two canonical param maps. ``scope`` (an action tag) prefixes messages
    for the per-action dispatcher path; when ``None`` the messages match the
    original flat-tool wording exactly."""
    prefix = f"[{scope}] " if scope else ""
    detail_scope = {"action": scope} if scope else {}

    only_code = sorted(set(code_params) - set(db_params))
    only_db = sorted(set(db_params) - set(code_params))
    if only_code or only_db:
        report.findings.append(
            Finding(
                FindingKind.ARG_DRIFT,
                Severity.ERROR,
                name,
                f"{prefix}argument set differs — only in code: {only_code or '∅'}; "
                f"only in DB: {only_db or '∅'}",
                {**detail_scope, "only_in_code": only_code, "only_in_db": only_db},
            )
        )

    for pname in sorted(set(code_params) & set(db_params)):
        c, d = code_params[pname], db_params[pname]
        if c.identity() != d.identity():
            report.findings.append(
                Finding(
                    FindingKind.ARG_DRIFT,
                    Severity.ERROR,
                    name,
                    f"{prefix}argument {pname!r} differs — "
                    f"code(type={c.type}, optional={c.optional}) vs "
                    f"db(type={d.type}, optional={d.optional})",
                    {
                        **detail_scope,
                        "param": pname,
                        "code": {"type": c.type, "optional": c.optional},
                        "db": {"type": d.type, "optional": d.optional},
                    },
                )
            )
        elif c.enum != d.enum:
            # Per-field enum drift — the counterpart to the dispatcher
            # discriminator's enum check ("enum values" in the match spec,
            # common-docs/systems/agents/agent-tools/STATE.md). Severity splits by how it actually bites:
            #   • BOTH sides declare an enum but members differ  → ERROR. The model
            #     is shown one set (DB → provider schema) while the executor enforces
            #     another (code model) — a guaranteed model_error on a value the
            #     model was told is valid.
            #   • One-sided (DB constrains, code open — or the reverse) → WARNING.
            #     Non-breaking today (the open side accepts the constrained side's
            #     values); the fix is to tighten the code model to a Literal[...] so
            #     the executor enforces exactly what the DB advertises.
            one_sided = c.enum is None or d.enum is None
            report.findings.append(
                Finding(
                    FindingKind.ARG_DRIFT,
                    Severity.WARNING if one_sided else Severity.ERROR,
                    name,
                    f"{prefix}argument {pname!r} "
                    + (
                        "is enum-constrained on only one side"
                        if one_sided
                        else "enum members differ"
                    )
                    + f" — code={sorted(c.enum) if c.enum else '∅'} vs "
                    f"db={sorted(d.enum) if d.enum else '∅'}"
                    + (
                        "  (tighten the code model to Literal[...] so the executor "
                        "enforces the values the DB advertises)"
                        if one_sided
                        else ""
                    ),
                    {
                        **detail_scope,
                        "param": pname,
                        "one_sided": one_sided,
                        "code_enum": sorted(c.enum) if c.enum else None,
                        "db_enum": sorted(d.enum) if d.enum else None,
                    },
                )
            )
        elif c.has_default and d.has_default and c.default_key() != d.default_key():
            report.findings.append(
                Finding(
                    FindingKind.ARG_DRIFT,
                    Severity.ERROR,
                    name,
                    f"{prefix}argument {pname!r} default differs — "
                    f"code={c.default!r} vs db={d.default!r}",
                    {
                        **detail_scope,
                        "param": pname,
                        "code_default": c.default,
                        "db_default": d.default,
                    },
                )
            )


def _diff_args_dispatcher(
    name: str,
    ct: DeclaredTool,
    db: DbTool,
    report: ValidationReport,
    union: tuple[str, dict[str, Any]] | None,
    db_variants: dict[str, dict[str, CanonParam]] | None,
) -> None:
    """Diff a multi-action dispatcher per action. Both sides must declare the
    per-action contract; a one-sided declaration is itself drift (the whole point
    of GAP 1 — the real contract must not escape the DB diff)."""
    if union is None:
        report.findings.append(
            Finding(
                FindingKind.ARG_DRIFT,
                Severity.ERROR,
                name,
                "tool_def.parameters declares a per-action contract ($variants) but the code "
                "args model is not a discriminated RootModel union — the executor would only "
                "enforce the loose outer model. Register "
                "RootModel[Annotated[Union[...], Field(discriminator=...)]].",
                {"db_actions": sorted(db_variants or {})},
            )
        )
        return
    if db_variants is None:
        report.findings.append(
            Finding(
                FindingKind.ARG_DRIFT,
                Severity.ERROR,
                name,
                "code registers a discriminated-union (per-action) args model but "
                "tool_def.parameters has no $variants — the per-action contract cannot be "
                "verified against the DB. Add $variants to the tool_def row.",
                {"code_actions": sorted(union[1])},
            )
        )
        return

    disc, members = union
    code_actions = set(members)
    db_actions = set(db_variants)
    if code_actions != db_actions:
        report.findings.append(
            Finding(
                FindingKind.ARG_DRIFT,
                Severity.ERROR,
                name,
                f"action set differs — code={sorted(code_actions)} db={sorted(db_actions)}",
                {
                    "only_in_code": sorted(code_actions - db_actions),
                    "only_in_db": sorted(db_actions - code_actions),
                },
            )
        )

    # The discriminator's own enum members (the one place we DO compare enum values).
    db_enum = db_discriminator_enum(db.parameters, disc)
    if db_enum is not None and db_enum != code_actions:
        report.findings.append(
            Finding(
                FindingKind.ARG_DRIFT,
                Severity.ERROR,
                name,
                f"discriminator {disc!r} enum differs — code={sorted(code_actions)} "
                f"db.{disc}.enum={sorted(db_enum)}",
                {"discriminator": disc, "code": sorted(code_actions), "db": sorted(db_enum)},
            )
        )

    for action in sorted(code_actions & db_actions):
        _diff_param_maps(
            name,
            canon_model_variant(members[action], disc),
            db_variants[action],
            report,
            scope=action,
        )
