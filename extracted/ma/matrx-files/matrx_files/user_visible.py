"""THE user-visibility rule — declared ONCE, in code, and generated everywhere else.

Folder sync's core promise is that the browser tree and a device's disk replica
can never disagree about which files a user has (SPEC-SERVER §1, D16). That only
holds if there is ONE declaration of "user-visible", so this module holds it and
emits every other shape from it:

* :func:`sql_is_user_visible_path_body` / :func:`sql_is_user_visible_row_body` —
  the bodies migration 025 pastes into ``files.is_user_visible_path(text)`` and
  ``files.is_user_visible(files.files)``. A test asserts the live
  ``pg_proc.prosrc`` still equals the generated text.
* :func:`user_visible_filters` — the matrx-orm ``Q``/filter kwargs the change
  feed applies. A parity test runs both over the same corpus and asserts
  identical row-id sets.

🚨 ONE EXPRESSION, NOT MERELY ONE RULE. The path half is spelled as the single
call ``files.is_user_visible_path(file_path)`` -- via matrx-orm's ``__user_visible``
lookup on the ORM side -- and never as ``NOT LIKE`` conjuncts. Postgres's
predicate-implication prover matches a partial index whose predicate contains a
function call only against the SAME expression, so expanding the conjuncts loses
both partial indexes (measured live 2026-09-13: cost 11,177 with a Sort and a
three-conjunct Filter, against 13.83 for an Index Only Scan when the identical
predicate is spelled as the function call).

What the rule is NOT:

* ``files.is_crawl_artifact(id)`` is NOT part of it (S2). It reads
  ``files.files.metadata``, ``web.snapshot`` and ``web.screenshot`` -- three
  cross-schema subqueries per row -- and it is a provenance test, not a
  access shape. Consumers add it as a separate conjunct.
* ``files.folders.is_system`` is NOT read or written (D16). The live
  ``folders_set_is_system()`` trigger makes it exactly
  ``is_system_path(folder_path)``, so the path predicate selects the same set
  while staying IMMUTABLE and index-usable.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Final


@dataclass(frozen=True)
class VisibilityConjunct:
    """One clause of the rule, in the order it is evaluated."""

    name: str
    sql: str
    """SQL text; ``%(alias)s`` is substituted with a dot-terminated row alias
    (``"f."``) or the empty string for an unqualified (index-predicate) spelling."""
    why: str


#: Top-level path segments reserved for machine writers — the ``not_machine_namespace``
#: conjunct spells exactly these. A machine writer that must write into a person's
#: storage registers its namespace HERE (or sets ``artifact_kind``), BEFORE its first
#: write (common-docs systems/files/file-service/USER_FILES_VS_MACHINE_FILES.md).
MACHINE_NAMESPACES: Final[tuple[str, ...]] = ("coding-sessions", "tool-images")

#: The path half — every clause here is IMMUTABLE, so it can live in an index
#: predicate. ``p`` is the path argument of ``files.is_user_visible_path``.
PATH_CONJUNCTS: Final[tuple[VisibilityConjunct, ...]] = (
    VisibilityConjunct(
        name="path_present",
        sql="p_file_path IS NOT NULL",
        why="file_path is NOT NULL on the table; a NULL argument is never visible.",
    ),
    VisibilityConjunct(
        name="not_system_path",
        sql="NOT files.is_system_path(p_file_path)",
        why=(
            "generations/ and system-files/ are app-managed. Identical to "
            "'not under an is_system folder', because folders_set_is_system() "
            "derives is_system from folder_path by trigger."
        ),
    ),
    VisibilityConjunct(
        name="not_temp",
        sql="split_part(ltrim(p_file_path,'/'),'/',1) <> '.matrx-tmp'",
        why=(
            "The temporary-file retention scope (matrx_files/retention.py and "
            "idx_files_tmp_retention_created). Never a user's file."
        ),
    ),
    VisibilityConjunct(
        name="not_machine_namespace",
        sql=(
            "split_part(ltrim(p_file_path,'/'),'/',1) NOT IN ("
            + ", ".join(f"'{ns}'" for ns in MACHINE_NAMESPACES)
            + ")"
        ),
        why=(
            "Top-level namespaces only machines write into a person's storage: "
            "coding-sessions/ (the desktop coding-session recorder) and tool-images/ "
            "(AI tool screenshots). Never the person's files, in the tree, the sync "
            "feed or Recents (Arman, 2026-09-24; folder-sync DECISIONS R3/R5)."
        ),
    ),
)

#: The row half — not derived. Both columns, because 824 alive rows carry
#: derivation_kind='variant' with parent_file_id IS NULL, so neither column
#: alone excludes derivatives.
ROW_CONJUNCTS: Final[tuple[VisibilityConjunct, ...]] = (
    VisibilityConjunct(
        name="not_child",
        sql="%(alias)sparent_file_id IS NULL",
        why="A derived row belongs to its master, not to the user's tree.",
    ),
    VisibilityConjunct(
        name="not_derivation",
        sql="%(alias)sderivation_kind IS NULL",
        why="824 alive rows are parentless variants; parent_file_id alone misses them.",
    ),
    VisibilityConjunct(
        name="not_produced_artifact",
        sql="%(alias)sartifact_kind IS NULL",
        why=(
            "artifact_kind marks a row a machine PRODUCED and filed on the person's "
            "behalf (today 'coding_session_artifact'). The class rule: whatever path "
            "such a row lands at, it is never the person's file (Arman, 2026-09-24)."
        ),
    ),
)

#: The FOLDER rule — the path conjuncts that apply to a folder path. Deliberately
#: not ``.matrx-tmp`` (folders there stay in scope, unchanged since 026).
FOLDER_CONJUNCTS: Final[tuple[VisibilityConjunct, ...]] = (
    VisibilityConjunct(
        name="path_present",
        sql="p_folder_path IS NOT NULL",
        why="A NULL folder path is never visible.",
    ),
    VisibilityConjunct(
        name="not_system_path",
        sql="NOT files.is_system_path(p_folder_path)",
        why="generations/ and system-files/ folders are app-managed.",
    ),
    VisibilityConjunct(
        name="not_machine_namespace",
        sql=(
            "split_part(ltrim(p_folder_path,'/'),'/',1) NOT IN ("
            + ", ".join(f"'{ns}'" for ns in MACHINE_NAMESPACES)
            + ")"
        ),
        why="The same machine namespaces the file rule hides.",
    ),
)

# ---------------------------------------------------------------------------
# RECENTS — "recent activity by the person". A strict SUBSET of the visible set.
# ---------------------------------------------------------------------------

#: Roots under the person's own tree whose contents a machine produced on the
#: person's behalf. They stay browsable in the tree but are never the person's
#: recent activity. Relocated here from matrx-frontend's former client-side
#: ``isGeneratedContentPath`` / ``isSystemManagedContentPath`` so Recents has ONE
#: declaration (2026-09-24). Exact root or anything beneath it; case-sensitive.
RECENT_EXCLUDED_ROOTS: Final[tuple[str, ...]] = (
    "Images/Generated",
    "Generated",
    "Agent Apps/blocks",
    "Images/agent-blocks",
    "Transcripts/Recordings",
    "FastFire/sessions",
    "FastFire/responses",
)

#: The roots a SERVICE writes into when it carries a file FOR an organization
#: (``FileService.upload_for_organization``, FILES-FOLDER-ORG 2026-09-25): key = the stable path
#: segment, suffixed on disk with the organization id (``page-captures-<org uuid>/...``); value =
#: the name a person reads in that organization's file tree. Declared HERE, once, because the
#: Recents rule below is spelled from it; ``FileService.CARRIED_ROOTS`` is this same dict.
#: Carried files stay browsable in the tree (the FILES-FOLDER-ORG product change) but are machine
#: output, never the person's recent activity: on 2026-09-26 one owner's Recents were topped by 38
#: gzipped page originals and 6 SEO provider payloads he never uploaded.
CARRIED_ROOTS: Final[dict[str, str]] = {
    "record-store": "Record store",
    "web-crawls": "Web crawls",
    "seo-data": "SEO data",
    "login-captures": "Login captures",
    "payroll-exports": "Payroll exports",
    "timesheet-reports": "Timesheet reports",
    "hr-letters": "Employment letters",
    "page-captures": "Captured pages",
    "text-messages": "Text messages",
    # The opt-in full-transcript backup of a Claude Code / Codex session
    # (aidream coding_session_bridge/raw_backup.py; knob
    # coding_session_bridge.raw_transcript_backup, default off — Arman 2026-09-28).
    "coding-transcripts": "Coding transcripts",
    # An e-signature envelope's own files — each signer's drawn signature and the signed copy —
    # filed in the ENVELOPE's organization (aidream services/esign/filing.py, 2026-10-04). The
    # signed copy opens from its envelope page; neither is the person's own recent activity.
    "e-signatures": "E-Signatures",
    # Social Intelligence's landed post / profile / ad media (aidream services/social/media.py,
    # 2026-10-09): vendor CDN URLs expire, so every fetched video and image is filed at once in the
    # matrx-system organization's private tree and linked to its social row by an association.
    "social-media": "Social media",
    # Model presentation media (aidream services/ai_catalog/local_models/discovery.py, 2026-10-15):
    # every image discovery proposes for a model (maker logo, model-card images) is copied here as a
    # PUBLIC file in the system organization and addressed by cdn_url — never hot-linked.
    "model-media": "Model media",
    # Watch AI raw captures (aidream services/ai_watch/raw_capture_sink.py, 2026-10-22): a step's
    # outside answer exactly as received (a vendor body, a tool's whole result before a cut), filed
    # in the run's organization when it is too large to sit inline on the step's own row.
    "run-captures": "Run captures",
}

#: ``<carried root>-<organization uuid>`` as the first path segment — anchored, lowercase uuid
#: (``ensure_organization_folder_async`` writes ``str(organization_id)``).
CARRIED_ROOT_SEGMENT_PATTERN: Final[str] = (
    "^(" + "|".join(CARRIED_ROOTS) + ")-"
    "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)

# ---------------------------------------------------------------------------
# THE MACHINE-ARTIFACT MARKER — stamped at the one upload door, from the path.
# ---------------------------------------------------------------------------
#
# The person's pick lists ("Use existing → Files", the organization inventory) read ONE database
# filter, ``platform._inventory_filter``, and it hides a file whose metadata carries
# ``{"system_artifact": true}`` (any ``artifact_domain``). On 2026-09-29 those lists were flooded by
# ``page-captures-<org>/…/*.json.gz`` page originals and ``coding-sessions/…`` files because their
# writers never stamped it. The class fix: the marker is derived HERE from the path the file lands
# at, and the upload door (``cloud_sync.sync_engine`` + the TUS row builder) stamps it on every
# write, so no writer has to remember. A marker whose domain is not ``web_crawl`` carries no access
# meaning (``files.has_access_for`` / ``_is_contextual_system_artifact`` key on web_crawl only);
# the tree still shows these files — the marker only keeps them out of the pick lists.

#: The artifact_domain a file under each machine namespace carries. Keys == MACHINE_NAMESPACES.
MACHINE_NAMESPACE_DOMAINS: Final[dict[str, str]] = {
    "coding-sessions": "coding_session",
    "tool-images": "tool_image",
}

#: Carried roots whose files are MACHINE OUTPUT (value = the artifact_domain stamped when the
#: writer names none; ``None`` = the writer names its own domain because that domain carries
#: access meaning — web crawls' ``web_crawl``, SEO's provider-payload domains).
MACHINE_CARRIED_ROOTS: Final[dict[str, str | None]] = {
    "record-store": "record_store_value",
    "web-crawls": None,
    "seo-data": None,
    "login-captures": "login_capture",
    "page-captures": "page_capture",
    "coding-transcripts": "coding_transcript",
    # An envelope's drawn signatures and signed copies: filed by the e-signature service and opened
    # from their envelope page; a signer's drawn signature is never a file to pick and attach.
    "e-signatures": "e_signature",
    # Cached provider media belongs to its social row, not a person's file pick list.
    "social-media": "social_media",
    # A model's logo and card images belong to its catalog presentation, not a person's pick list.
    "model-media": "model_media",
    # A run's raw capture belongs to its step in Watch AI, never a person's pick list.
    "run-captures": "run_raw_capture",
}

#: Carried roots whose files are a DELIVERABLE a person asked for (a letter, an export, a texted
#: attachment) — pickable like anything the person uploaded. Every CARRIED_ROOTS key is in exactly
#: one of these two declarations (a test holds the partition), so a new root must choose.
PERSON_CARRIED_ROOTS: Final[frozenset[str]] = frozenset(
    {"payroll-exports", "timesheet-reports", "hr-letters", "text-messages"}
)

_CARRIED_ROOT_PREFIX_RE: Final = re.compile(CARRIED_ROOT_SEGMENT_PATTERN)


def machine_artifact_marker(file_path: str | None) -> dict[str, Any]:
    """The marker keys a file at ``file_path`` must carry — ``{}`` for a person's file."""
    if not file_path:
        return {}
    first = file_path.lstrip("/").split("/", 1)[0]
    domain = MACHINE_NAMESPACE_DOMAINS.get(first)
    if domain is not None:
        return {"system_artifact": True, "artifact_domain": domain}
    match = _CARRIED_ROOT_PREFIX_RE.match(first)
    if match is None or match.group(1) not in MACHINE_CARRIED_ROOTS:
        return {}
    carried_domain = MACHINE_CARRIED_ROOTS[match.group(1)]
    if carried_domain is None:
        return {"system_artifact": True}
    return {"system_artifact": True, "artifact_domain": carried_domain}


def stamp_machine_artifact(file_path: str | None, metadata: dict | None) -> dict | None:
    """``metadata`` with the path's marker applied; unchanged (same object) for a person's file.

    ``system_artifact`` is forced true on a machine path; ``artifact_domain`` is only filled when
    the writer named none (a writer's own domain may carry access meaning and always wins).
    """
    marker = machine_artifact_marker(file_path)
    if not marker:
        return metadata
    out = dict(metadata or {})
    out["system_artifact"] = True
    if "artifact_domain" in marker:
        out.setdefault("artifact_domain", marker["artifact_domain"])
    return out


# ---------------------------------------------------------------------------
# SYSTEM FOLDERS — the folder half of the marker (V5-B, 2026-09-30).
# ---------------------------------------------------------------------------
#
# "Use existing → Folders" read 56,037 folders for the test account, led by system-files/variants/<id>
# folders and page-captures-<org>/<site> captures, because nothing marked a folder as the system's
# own. A folder is a SYSTEM FOLDER when:
#   * the platform owns its whole tree (``files.folders.is_system``: system-files/, generations/ —
#     derived by trigger ``folders_set_is_system``; never stamped, never shown), or
#   * it carries ``metadata.system_artifact = true``, stamped HERE from its path at the one folder
#     door (``CloudSyncDB.create_folder*``): every path :func:`machine_artifact_marker` marks for a
#     file, plus a variant folder (``<master dir>/v`` and ``<master dir>/v/<master file id>``,
#     cloud_sync/variants.py), which holds nothing but derived copies.
# ``platform._inventory_filter`` lists a stamped folder only while the Feature Knob
# ``files.show_system_files`` (default off) is on — the same rule as a system file. The browser
# mirror is matrx-frontend features/files/utils/user-visible.ts (isSystemFolder).

_UUID: Final[str] = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

#: ``<master dir>/v`` or ``<master dir>/v/<master file id>`` — never a top-level ``v``.
VARIANT_FOLDER_PATTERN: Final[str] = rf"^.+/v(/{_UUID})?$"
_VARIANT_FOLDER_RE: Final = re.compile(VARIANT_FOLDER_PATTERN)


def system_folder_marker(folder_path: str | None) -> dict[str, Any]:
    """The marker keys a folder at ``folder_path`` must carry — ``{}`` for a person's folder."""
    if not folder_path:
        return {}
    marker = machine_artifact_marker(folder_path)
    if marker:
        return marker
    if _VARIANT_FOLDER_RE.match(folder_path.strip("/")):
        return {"system_artifact": True, "artifact_domain": "file_variant"}
    return {}


def stamp_system_folder(folder_path: str | None, metadata: dict | None) -> dict | None:
    """``metadata`` with the folder's marker applied; unchanged (same object) for a person's folder."""
    marker = system_folder_marker(folder_path)
    if not marker:
        return metadata
    out = dict(metadata or {})
    out["system_artifact"] = True
    if "artifact_domain" in marker:
        out.setdefault("artifact_domain", marker["artifact_domain"])
    return out


RECENT_PATH_CONJUNCTS: Final[tuple[VisibilityConjunct, ...]] = (
    VisibilityConjunct(
        name="user_visible",
        sql="files.is_user_visible_path(p_file_path)",
        why="Recents is a subset of the person's visible files.",
    ),
    VisibilityConjunct(
        name="not_produced_on_behalf",
        sql=(
            "NOT (ltrim(p_file_path,'/') = ANY (ARRAY["
            + ", ".join(f"'{r}'" for r in RECENT_EXCLUDED_ROOTS)
            + "]) OR ltrim(p_file_path,'/') LIKE ANY (ARRAY["
            + ", ".join(f"'{r}/%'" for r in RECENT_EXCLUDED_ROOTS)
            + "]))"
        ),
        why="Machine output filed under the person's roots (see RECENT_EXCLUDED_ROOTS).",
    ),
    VisibilityConjunct(
        name="not_carried_for_an_organization",
        sql=(
            "split_part(ltrim(p_file_path,'/'),'/',1) !~ '"
            + CARRIED_ROOT_SEGMENT_PATTERN
            + "'"
        ),
        why=(
            "A file a service carried for an organization (see CARRIED_ROOTS) is browsable in "
            "that organization's tree but is never the person's recent activity (2026-09-26)."
        ),
    ),
)

RECENT_ROW_CONJUNCTS: Final[tuple[VisibilityConjunct, ...]] = (
    VisibilityConjunct(
        name="visible",
        sql="files.is_user_visible(%(row)s)",
        why="Recents is a subset of the person's visible files.",
    ),
    VisibilityConjunct(
        name="not_device_written",
        sql="%(row)s.origin_device_id IS NULL",
        why=(
            "A row a registered device wrote (a desktop sync client) is the person's "
            "file, but its arrival is not the person's recent activity in the app "
            "(folder-sync DECISIONS R3)."
        ),
    ),
    VisibilityConjunct(
        name="recent_path",
        sql="files.is_recent_activity_path(%(row)s.file_path)",
        why="The path half of Recents.",
    ),
    VisibilityConjunct(
        name="not_a_system_file",
        sql="NOT (%(row)s.metadata @> '{\"system_artifact\": true}'::jsonb)",
        why=(
            "A file the system marked as its own (metadata.system_artifact, stamped by "
            "machine_artifact_marker / stamp_machine_artifact) is never Recents, wherever it lives "
            "(Arman 2026-09-29: system files 'should never show in recents anyways')."
        ),
    ),
)

#: The one expression every consumer spells for the path half.
PATH_PREDICATE_FUNCTION: Final[str] = "files.is_user_visible_path"
ROW_PREDICATE_FUNCTION: Final[str] = "files.is_user_visible"
FOLDER_PREDICATE_FUNCTION: Final[str] = "files.is_user_visible_folder_path"
RECENT_PATH_FUNCTION: Final[str] = "files.is_recent_activity_path"
RECENT_ROW_FUNCTION: Final[str] = "files.is_recent_activity"

#: The ORM column the path half is applied to on ``files.files``.
PATH_COLUMN: Final[str] = "file_path"


def sql_is_user_visible_path_body() -> str:
    """The exact body of ``files.is_user_visible_path(text)`` (migration 025)."""
    clauses = "\n     AND ".join(c.sql for c in PATH_CONJUNCTS)
    return f"\n  SELECT {clauses};\n"


def sql_is_user_visible_row_body(alias: str = "p_row") -> str:
    """The exact body of ``files.is_user_visible(files.files)`` (migration 025)."""
    row = "\n     AND ".join(c.sql % {"alias": f"{alias}."} for c in ROW_CONJUNCTS)
    return f"\n  SELECT {row}\n     AND {PATH_PREDICATE_FUNCTION}({alias}.file_path);\n"


def sql_is_user_visible_folder_path_body() -> str:
    """The exact body of ``files.is_user_visible_folder_path(text)`` (migration 046)."""
    clauses = "\n     AND ".join(c.sql for c in FOLDER_CONJUNCTS)
    return f"\n  SELECT {clauses};\n"


def sql_is_recent_activity_path_body() -> str:
    """The exact body of ``files.is_recent_activity_path(text)`` (migration 046)."""
    clauses = "\n     AND ".join(c.sql for c in RECENT_PATH_CONJUNCTS)
    return f"\n  SELECT {clauses};\n"


def sql_is_recent_activity_row_body(alias: str = "p_row") -> str:
    """The exact body of ``files.is_recent_activity(files.files)`` (migration 046)."""
    clauses = "\n     AND ".join(c.sql % {"row": alias} for c in RECENT_ROW_CONJUNCTS)
    return f"\n  SELECT {clauses};\n"


def sql_row_conjuncts(alias: str) -> str:
    """The inline conjunct list a SQL consumer (``get_user_file_tree``) pastes.

    Returns the row half AND the single path-predicate call — the same
    expression the index predicates carry, so the planner can match them.
    """
    row = "\n          AND ".join(c.sql % {"alias": f"{alias}."} for c in ROW_CONJUNCTS)
    return f"{row}\n          AND {PATH_PREDICATE_FUNCTION}({alias}.file_path)"


def sql_index_predicate() -> str:
    """The partial-index predicate shared by §1.3's tree index and §2.5's feed index."""
    row = " AND ".join(c.sql % {"alias": ""} for c in ROW_CONJUNCTS)
    return f"{row} AND {PATH_PREDICATE_FUNCTION}({PATH_COLUMN})"


def row_visible_filters() -> dict[str, Any]:
    """The "not derived" half as matrx-orm filter kwargs.

    Applied unconditionally by the feed: ``include_system=true`` means "ignore
    the path half", and it must never re-admit derivative rows.
    """
    return {
        "parent_file_id__isnull": True,
        "derivation_kind__isnull": True,
        "artifact_kind__isnull": True,
    }


def path_visible_filters() -> dict[str, Any]:
    """The path half as matrx-orm filter kwargs.

    ``__user_visible`` is matrx-orm's registered path-family lookup; it emits
    ``files.is_user_visible_path(file_path) = $n`` verbatim, which is what makes
    the partial index matchable.
    """
    return {f"{PATH_COLUMN}__user_visible": True}


def user_visible_filters() -> dict[str, Any]:
    """Both halves — the full rule, as matrx-orm filter kwargs."""
    return {**row_visible_filters(), **path_visible_filters()}


def explain_rule() -> str:
    """Human-readable statement of the rule, for error messages and docs."""
    parts = [f"- {c.name}: {c.why}" for c in (*ROW_CONJUNCTS, *PATH_CONJUNCTS)]
    return "A file is user-visible when all of:\n" + "\n".join(parts)
