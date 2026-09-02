"""Shared helpers for the kind-registry authoring toolsets (``kind_*`` +
``kindcomp_*``).

Not a tool module — no tool functions live here. The two agent-facing modules
(``kind_authoring.py`` — the ``kind_*`` kind/schema/example/skill tools, and
``kind_component.py`` — the ``kindcomp_*`` component-code tools) both import
from here so resolution, authorization mirroring, schema inference, and
validation stay one implementation.

Authorization model
-------------------
These tools execute server-side through matrx-orm (a privileged connection —
Postgres RLS does NOT apply on this path), so every read AND write is gated in
code through the ONE live policy function: ``iam.has_access_for(user,
'content_ir_kind', kind_id, level)`` via ``matrx_orm.call_function`` (the
notes.py pattern — never a hand-rolled replica, which is exactly how a
private-kind over-grant slipped in once: org membership alone does NOT confer
access to a ``visibility='personal'`` kind). Owner (``created_by``) passes on a
fast-path without a DB round-trip; everyone else resolves through the
SECURITY DEFINER body (public/internal visibility, org membership, explicit
iam grants, reachability). Fail-closed: any error in the check reads as no
access. Levels mirror the canonical RLS policies — reads = ``viewer``, writes
= ``editor``. Never widen this by writing rows with fabricated ``created_by``
/ ``organization_id`` values.
"""

from __future__ import annotations

import asyncio
import copy
import logging
import os
import re
import shutil
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

# ── The component props contract (verified against the frontend mount site,
#    features/content-ir/react/db-component/DbKindComponentImpl.tsx:
#    `<Component data={data} kind={kind} config={resolution.config} />`).
#    This is THE #1 silent-failure class for authored components: a component
#    reading flat props (props.wine_name) renders empty with no crash and no
#    incident. Stated in every authoring tool's docstring, returned by
#    kindcomp_get_context, and enforced by component_source_lint at write time.
PROPS_CONTRACT: dict[str, str] = {
    "component_receives": (
        "The frontend mounts your component as <Component data={value} kind={kind} "
        "config={config} />. The kind instance arrives as props.data — read every field "
        "from it (e.g. `function Card({ data }) { return <div>{data.title}</div>; }`). "
        "Flat props (props.title) are NEVER provided; reading them renders empty with no "
        "error."
    ),
    "props_transform": (
        "props_transform reshapes the raw kind value BEFORE mounting, but its output "
        "STILL arrives as props.data — it never spreads keys into flat props. Your "
        "component always destructures { data }."
    ),
    "input_component_key": (
        f"'{GENERIC_INPUT_COMPONENT_KEY}' is the only routable input-role component key. "
        "kind_create seeds it automatically; never create custom input-role components."
    ),
}

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
        "@/components/kind-kit/KindHeaderBar",
        "@/components/kind-kit/StreamingSkeleton",
        "@/components/kind-kit/TagList",
    }
    | {
        f"@/components/ui/{name}"
        for name in (
            "button", "input", "textarea", "card", "label", "select", "slider",
            "switch", "tabs", "badge", "tooltip", "accordion", "collapsible",
            "progress", "separator", "scroll-area", "dialog", "sheet",
            "dropdown-menu", "table", "checkbox", "radio-group", "popover",
            "avatar", "alert", "skeleton",
        )
    }
)

# ── The component design bar (Arman, 2026-08-22). Returned to the authoring
#    agent beside the props contract; the reference implementation is the
#    keyword-research component family. This is the QUALITY floor, not a
#    suggestion.
COMPONENT_DESIGN_DOCTRINE = (
    "Design bar for every kind component — modern, professional, delicate:\n"
    "- KIT FIRST: the registered kind-kit primitives (SortableList, KindPanelGrid, "
    "KindPanel, KindHeaderBar, StreamingSkeleton/useStreamingValue, TagList/"
    "KeywordChip — contracts in platform_components) are the ONLY way to build "
    "lists, panels, grids, headers, chips, and skeletons. Hand-rolling any of "
    "them is a defect; they are what make every component correct and consistent "
    "by construction.\n"
    "- DENSE, never cramped: minimal outer padding, tight internal spacing, "
    "use the full width; the layout should feel open while wasting no space.\n"
    "- A compact header: the instance's primary identity (title_key) plus "
    "at-a-glance counts/stats — one line, no hero banners.\n"
    "- INTERACTIVE everywhere the data invites it: lists support reordering "
    "(drag handles), inline editing, add/remove; sections have one-click "
    "copy; the header carries a delicate copy bar (JSON / Markdown / CSV / "
    "TXT / XML-for-AI) using CopyButtons/CopyForAiButton.\n"
    "- DRAG FEEDBACK IS MANDATORY (Arman, 2026-08-22): while an item is "
    "dragged over a slot, the displaced item must visibly move aside "
    "(translate in the drop direction) and a shadowed drop placeholder must "
    "show exactly where the dragged item will land — without this the user "
    "cannot tell where the item ends up. Implement on dragOver: give the "
    "hovered row a transform (e.g. translate-y) plus an insertion indicator "
    "with shadow (border/gap + shadow-md), cleared on dragLeave/drop.\n"
    "- Subtle motion and a touch of color (Tailwind semantic tokens only: "
    "bg-card, text-foreground, text-muted-foreground, border-border and "
    "variants — no arbitrary values, no emojis).\n"
    "- Fully responsive and mobile-friendly; long content collapses or "
    "scrolls within the component — NEVER a raw JSON dump.\n"
    "- Null-guard every optional field; a partial payload must render "
    "gracefully, never crash, never show 'undefined' or [object Object].\n"
    "- Images are welcome when the shape carries them (render <img> with "
    "max-width, rounded corners, and an alt).\n"
    "- THE LAYOUT LAW (Arman, 2026-08-23 — after a four-panel keyword map that "
    "truncated every keyword to three characters): budget WIDTH from the "
    "CONTENT, never from the count of things you want side by side. Text-bearing "
    "panels need ~280px minimum each; use an auto-fit grid (repeat(auto-fit, "
    "minmax(280px, 1fr))) so four panels become 2x2 or a single column when "
    "space is short — never four cramped columns. A keyword, phrase, or chip "
    "WRAPS; it is never truncated with an ellipsis. A subline (rationale, "
    "description) spans the FULL panel width under the header — never squeezed "
    "beside the title. A header row carries the title, ONE count/badge, and at "
    "most two controls; every further control collapses into an overflow menu. "
    "Per-row actions appear on hover/focus, not permanently. Side-by-side panels "
    "are equal height (flex column) with footer actions (Add, Copy) PINNED to "
    "the bottom (mt-auto) so they align across panels. Long lists scroll inside "
    "the panel (max-h + overflow-y) rather than stretching the page. Prefer "
    "one excellent column over four unreadable ones.\n"
    "- STREAMING IS A REQUIREMENT, not a feature (Arman, 2026-08-22): the "
    "value arrives PROGRESSIVELY during the LLM stream, so the component must "
    "render its full layout immediately and fill in as data lands. Ship its "
    "own brief skeleton state that MIMICS the finished layout (never the "
    "generic fallback, never a spinner-until-complete), render list items the "
    "moment each one parses (stable keys — no flicker, no reordering jumps), "
    "let true prose fields grow as text streams in, and reveal structured "
    "details in chunks as they complete. A component that waits for the "
    "complete object before rendering is broken by definition — every field "
    "access must tolerate absence mid-stream."
)

# ── Platform component contracts the allowlist exposes.
#    CROSS-REPO MIRROR of matrx-frontend components/agent-copy/
#    {CopyButtons,CopyForAiButton}.tsx + buildAgentPayload.ts. The Artisan's
#    first live build (2026-08-22) had to GUESS these props (it passed
#    `content=` / `data=`, which do not exist) and honestly flagged it — the
#    copy bar would have rendered and silently done nothing. Exact contracts
#    ride the authoring bundle so no component author ever guesses again.
#    Change BOTH sides together.
PLATFORM_COMPONENT_CONTRACTS: dict[str, str] = {
    "CopyButtons": (
        "import { CopyButtons } from \"@/components/agent-copy/CopyButtons\" — the "
        "copy / copy-for-AI (+ optional download) pair. REQUIRED prop `label: string` "
        "(toast + tooltip text). `human?: string | (() => string)` — the plain-text "
        "copy; `agent?: AgentPayloadInput | string | (() => AgentPayloadInput | string)` "
        "— the Copy-for-AI payload (see AgentPayloadInput); `json?: unknown | (() => "
        "unknown)` — adds a pretty-printed JSON entry to the AI dropdown; `size?: "
        "'xs' | 'icon' | 'sm'` (xs = dense list items, icon = rows/cards, sm = "
        "header); `export?: { items, sheetRows }` — a download dropdown (CSV/MD/TXT "
        "etc.); `hide?: ('copy'|'ai'|'export')[]`; `stopPropagation` defaults true. "
        "There is NO `content` prop and NO format map — build the markdown/CSV/TXT "
        "strings yourself and pass them via `human` (one format) or `export` items."
    ),
    "CopyForAiButton": (
        "import { CopyForAiButton } from \"@/components/agent-copy/CopyForAiButton\" — "
        "the single Copy-for-AI action. REQUIRED `label: string` and REQUIRED "
        "`agent: AgentPayloadInput | string | (() => …)`; optional `size?: 'icon' | "
        "'sm'`, `compact?: boolean` (icon-only h-6 for headers), `showLabel`, "
        "`disabled`, `className`. There is NO `data` prop — wrap your value in an "
        "AgentPayloadInput."
    ),
    "AgentPayloadInput": (
        "{ kind: string (stable slug, e.g. 'reading-list'), location: string (where the "
        "user is, in words), description: string (one line: what was copied), data: "
        "unknown (the raw object/array — dumped as JSON in full), summary?: string, "
        "attributes?: Record<string, string | number> }. Prefer passing a builder "
        "FUNCTION so URL/timestamp are captured at click time."
    ),
    "KIND_KIT": (
        "THE KIT COMES FIRST (Arman, 2026-08-23): these registered, tested primitives "
        "(matrx-frontend components/kind-kit) exist so every component gets the same "
        "correct drag feedback, content-aware grids, pinned footers, wrapping chips, "
        "and streaming skeletons. Never hand-roll what the kit provides. Import each "
        "by its exact path with the named export."
    ),
    "SortableList": (
        "import { SortableList } from \"@/components/kind-kit/SortableList\" — "
        "drag-to-reorder list: rows DISPLACE and a shadowed dashed placeholder marks "
        "the landing slot; grip handle; arrow buttons as keyboard/touch fallback. Props: "
        "items: readonly T[] (required; never mutated), onReorder(items: T[]) "
        "(required; full new order), getKey?(item, index) => string (default id/key/"
        "index), renderItem?(item, {index, isDragging}) => ReactNode (default "
        "label/title/name/text), onRemove?(item, index) (adds inline X), disabled?, "
        "hideArrows?, emptyState?, className?, itemClassName?, ariaLabel?."
    ),
    "KindPanelGrid": (
        "import { KindPanelGrid } from \"@/components/kind-kit/KindPanelGrid\" — "
        "content-aware auto-fit grid with EQUAL-HEIGHT panels. Props: children "
        "(required), minColumnWidth?: number px (default 280 — never smaller for "
        "text panels), maxColumns?, gap?: 'sm'|'md'|'lg' (default md), fill?: "
        "'auto-fit'|'auto-fill', className?."
    ),
    "KindPanel": (
        "import { KindPanel } from \"@/components/kind-kit/KindPanel\" — header (icon "
        "· wrapping title · count · badge · spinner · at most 2 `actions` · overflow "
        "menu) → FULL-WIDTH `subline` → body → `footer` PINNED to the bottom (mt-auto) "
        "so Add/Copy align across sibling panels. Props: title (required), icon? "
        "accepts `Icon` or `<Icon />`, "
        "count?: number|string, badge?, streaming?, actions? (≤2 controls), "
        "menuItems?: [{label, onSelect, icon?, disabled?, destructive?, "
        "separatorBefore?}], subline?, children?, footer?, variant?: 'card'|'bare', "
        "dense?, className?, bodyClassName?."
    ),
    "KindHeaderBar": (
        "import { KindHeaderBar } from \"@/components/kind-kit/KindHeaderBar\" — the "
        "standard compact kind header: title (title_key) · stats · streaming indicator "
        "· copy bar. Props: title (required), icon? accepts `Icon` or `<Icon />`, "
        "subtitle?, stats?: [{label, value, icon? accepts either form, title?}], "
        "streaming?, streamingLabel?, copy?: CopyButtonsProps "
        "minus size/className (label REQUIRED; human?, agent?, json?, export?, hide?), "
        "actions?, size?: 'sm'|'md', className?."
    ),
    "StreamingSkeleton": (
        "import { StreamingSkeleton, useStreamingValue, streamList, streamText } from "
        "\"@/components/kind-kit/StreamingSkeleton\" — <StreamingSkeleton layout="
        "'list'|'cards'|'table'|'text' rows={3} columns={} header label /> mimics the "
        "finished layout before data lands. useStreamingValue(value, fallback) → "
        "{value, arrived} keeps the latest DEFINED value sticky during the stream "
        "(call unconditionally with a field read like data?.summary — never a fresh "
        "per-render expression; use streamList(value) for arrays and "
        "streamText(value, fallback) for strings)."
    ),
    "TagList": (
        "import { KeywordChip, TagList } from \"@/components/kind-kit/TagList\" — chips "
        "that WRAP and never truncate. KeywordChip: label (required), meta?, icon?, "
        "selected?, onSelect?(next), onRemove?(), onEdit?(next), disabled?, tone?: "
        "'default'|'primary'|'muted', size?: 'sm'|'md'. TagList: items (required; "
        "strings or {label, key?, meta?, disabled?}), selected?, onToggle?(key, next), "
        "onRemove?(key, index), onEdit?(key, index, next), onAdd?(label) (renders the "
        "add input), addPlaceholder?, emptyState?, tone?, size?, disabled?."
    ),
    "kit_usage": (
        "Four keyword lists, correctly: <KindHeaderBar title={data.primary_keyword} "
        "stats={[{label:'lists', value: lists.length}, {label:'keywords', value: total}]} "
        "copy={{ label: 'Keyword map', human: () => markdownText, json: () => data, "
        "agent: () => ({ kind: 'keyword-map', location: 'Chat', description: 'Keyword "
        "relationship map', data }) }} /> then <KindPanelGrid minColumnWidth={300}> "
        "{lists.map(list => <KindPanel key={list.label} title={list.label} count={list."
        "keywords.length} subline={list.rationale} actions={<CopyButtons label={list."
        "label} size=\"xs\" human={() => list.keywords.join('\\n')} hide={['export']} />} "
        "footer={<TagList items={[]} onAdd={add} addPlaceholder=\"Add keyword\" />}> "
        "<SortableList items={list.keywords} onReorder={reorder} onRemove={remove} "
        "renderItem={(k) => <KeywordChip label={k} />} /></KindPanel>)}</KindPanelGrid>."
    ),
    "usage": (
        "Header: <CopyButtons label=\"Reading list\" size=\"sm\" human={() => markdownText} "
        "json={() => exportObject} agent={() => ({ kind: 'reading-list', location: "
        "'Chat', description: 'A curated reading list', data: exportObject })} "
        "export={{ items: [{ id: 'csv', label: 'CSV', filename: 'list.csv', "
        "content: () => csvText }, { id: 'md', label: 'Markdown', filename: 'list.md', "
        "content: () => markdownText }] }} />. Per row: <CopyButtons label={book.title} "
        "size=\"xs\" human={() => rowText} agent={() => ({ kind: 'book', location: "
        "'Chat', description: 'One book', data: book })} hide={['export']} />."
    ),
}

_DATA_REFERENCE_RE = re.compile(r"\bdata\b")
_IMPORT_RE = re.compile(
    r"""^\s*import\s+(?:[^'"]*?\s+from\s+)?['"]([^'"]+)['"]""", re.MULTILINE
)


def component_import_lint(source: str) -> str | None:
    """Refuse imports outside the frontend compiler's allowlist.

    The in-page compiler SKIPS unknown imports (console.warn) instead of
    failing, so the component mounts with undefined identifiers and breaks at
    runtime with no incident. Returns the refusal message, or None when every
    import is allowlisted."""
    unknown = sorted(
        {m for m in _IMPORT_RE.findall(source or "") if m not in COMPONENT_ALLOWED_IMPORTS}
    )
    if not unknown:
        return None
    return (
        f"Component imports modules outside the sandbox allowlist: {unknown}. "
        "The browser compiler skips unknown imports silently, so these would be "
        "undefined at runtime and the component would break with no error. "
        f"Allowed imports: {sorted(COMPONENT_ALLOWED_IMPORTS)}. Rewrite using "
        "only allowlisted modules (lucide-react icons, @/components/ui/* "
        "shadcn primitives, recharts, CopyButtons/CopyForAiButton, Markdown)."
    )


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
        _, stderr = await asyncio.wait_for(
            proc.communicate((source or "").encode()), timeout=15
        )
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
        "Component source never references `data`, so it cannot render the kind "
        "instance and would mount as a silent empty component. The frontend mounts "
        "DB components as <Component data={value} kind={kind} config={config} /> — "
        "read every field from props.data (e.g. `function Card({ data }) { ... "
        "data.title ... }`). props_transform output ALSO arrives as props.data; "
        "flat props are never provided. Rewrite the component to destructure "
        "{ data } and resubmit."
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


def ctx_is_admin(ctx: ToolContext) -> bool:
    """True only when the calling request's authenticated user is a platform
    admin (``AppContext.is_admin`` — an ``admin.admins`` row resolved at JWT
    auth, matrx-connect). Fail-closed: no context or any error reads as
    non-admin. This gates the ``platform_kind`` mint path — never widen it to
    org-admin or any softer signal."""
    try:
        from matrx_ai.context.app_context import try_get_app_context

        app_ctx = try_get_app_context()
        return bool(getattr(app_ctx, "is_admin", False))
    except Exception:  # noqa: BLE001 — fail closed
        return False


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

    if is_uuid(ref):
        row = await KindDefinition.get_or_none(use_cache=False, id=ref)
        if row is None or row.deleted_at is not None:
            return None, err("not_found", f"No kind_definition found with id '{ref}'.")
        return row, None

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


async def kind_access_allowed(kind_id: str, user_id: str, level: str) -> bool:
    """Canonical access check — ``iam.has_access_for(user, 'content_ir_kind',
    id, level)`` (the same SECURITY DEFINER body behind the RLS policies).

    ONE source of truth — never re-implement visibility/org/grant semantics
    here (org membership alone must NOT unlock a private kind). Fail-closed:
    any error reads as no access.
    """
    try:
        from matrx_orm import call_function

        database = get_db_model("KindDefinition")._database
        result = await call_function(
            database,
            "iam",
            "has_access_for",
            user_id,
            KIND_ENTITY_TOKEN,
            kind_id,
            level,
            mode="scalar",
        )
        return bool(result)
    except Exception:  # noqa: BLE001 — fail closed, never raise into the tool
        logger.warning("kind access check failed for %s (level=%s)", kind_id, level, exc_info=True)
        return False


async def can_access_kind(kind_row: Any, ctx: ToolContext, level: str) -> bool:
    """Owner fast-path, else the live ``iam.has_access_for`` at ``level``."""
    user_id = ctx_user_id(ctx)
    if not user_id:
        return False
    if str(kind_row.created_by or "") == user_id:
        return True
    return await kind_access_allowed(str(kind_row.id), user_id, level)


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
                    items = child_schema.get("items")
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


def kind_summary(kd: Any) -> dict[str, Any]:
    return {
        "id": str(kd.id),
        "kind": kd.kind,
        "label": kd.label,
        "authoring_owner": kd.authoring_owner,
        "version": kd.version,
        "is_active": kd.is_active,
        "visibility": str(getattr(kd.visibility, "value", kd.visibility)),
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
