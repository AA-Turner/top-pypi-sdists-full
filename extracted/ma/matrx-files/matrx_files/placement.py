"""THE placement registry — one declaration of where every file goes and what it is called.

Every writer that files bytes is a **pathway** (``chat.attachment``, ``media.image_generation``,
``web.crawl``…). A pathway declares, once, in code:

* whose output it is — ``audience``: ``person`` (the person caused it: their Files tree AND Recents)
  or ``automated`` (the platform did it on its own, or it is a side effect of something the person
  did: the one **System** folder, ``system-files/``, never Recents, always in search);
* whether the person picks the folder (``mode="person_chooses"``: a chosen folder is used unchanged,
  the registry only supplies the default) or the registry decides (``mode="registry"``);
* the destination — one CORE ROOT plus a subfolder pattern with tokens;
* how a file with no name of its own is named (:data:`NAMING_STRATEGIES`).

The declared values are DEFAULTS. The live values are rows of ``files.file_pathway`` (admin-editable at
manage.aimatrx.com › Utilities › File placement). A host injects a loader with
:func:`configure_pathway_rows`; with no loader (bare-venv, tests) the declared default is used and that
use is announced (``on_row_missing``). Only ``subfolder``, ``naming``, ``naming_pattern``,
``description`` and ``retention_policy`` are live-editable; ``audience``, ``root`` and ``file_access``
decide path predicates and existing rows, so they change only by a migration + mover run.

Plan and rulings: common-docs systems/files/file-service/projects/placement-registry/PLAN.md.
"""

from __future__ import annotations

import logging

import re
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any, Final, Literal

from .naming import slugify_prompt
from .system_paths import get_system_folder

Audience = Literal["person", "automated"]
Mode = Literal["person_chooses", "registry"]
Naming = Literal[
    "keep_original", "prompt_slug_hash", "timestamp", "source_timestamp", "id_only", "ai_title"
]
FileAccess = Literal["personal", "internal", "public"]
RootKind = Literal["person", "system", "temp"]

AUDIENCES: Final[tuple[str, ...]] = ("person", "automated")
MODES: Final[tuple[str, ...]] = ("person_chooses", "registry")
NAMING_STRATEGIES: Final[tuple[str, ...]] = (
    "keep_original",
    "prompt_slug_hash",
    "timestamp",
    "source_timestamp",
    "id_only",
    "ai_title",
)
FILE_ACCESS_LEVELS: Final[tuple[str, ...]] = ("personal", "internal", "public")

#: Fields an admin may change on a live row without a deploy. Everything else is a migration.
LIVE_EDITABLE_FIELDS: Final[frozenset[str]] = frozenset(
    {"subfolder", "naming", "naming_pattern", "description", "retention_policy"}
)

#: Tokens a subfolder or naming pattern may use. ``{org}`` and ``{owner}`` are deliberately absent:
#: both are columns on the row, never path text.
TOKENS: Final[frozenset[str]] = frozenset(
    {
        "yyyy", "mm", "dd", "HH", "MI", "SS",
        "conversation", "source", "record", "record_type", "run", "master", "session",
        "file_id", "pathway",
    }
)
_DATE_TOKENS: Final[frozenset[str]] = frozenset({"yyyy", "mm", "dd", "HH", "MI", "SS"})
_TOKEN_RE: Final = re.compile(r"\{([A-Za-z_]+)\}")


@dataclass(frozen=True)
class CoreRoot:
    """One of the few known top-level directories."""

    key: str
    path: str
    label: str
    kind: RootKind
    description: str


#: THE core directories — few, human-named. They feed IMMUTABLE SQL (path predicates and partial
#: indexes), so they are a code declaration, never an admin edit.
CORE_ROOTS: Final[tuple[CoreRoot, ...]] = (
    CoreRoot("my_files", "My Files", "My Files", "person", "Uploads with no folder chosen, and imports."),
    CoreRoot("images", "Images", "Images", "person", "Images the person made, edited, captured or uploaded."),
    CoreRoot("video", "Video", "Video", "person", "Videos the person generated, recorded or rendered."),
    CoreRoot("audio", "Audio", "Audio", "person", "Audio the person generated or recorded; podcasts."),
    CoreRoot("documents", "Documents", "Documents", "person", "Documents generated, scanned, exported or signed."),
    CoreRoot("chat_attachments", "Chat Attachments", "Chat Attachments", "person", "Files attached in chats and agent runs."),
    CoreRoot("system", "system-files", "System", "system", "Everything the platform files on its own and every side effect."),
    CoreRoot("temp", ".matrx-tmp", "Temporary", "temp", "Disposable working files, swept by retention."),
)
_ROOTS_BY_KEY: Final[dict[str, CoreRoot]] = {r.key: r for r in CORE_ROOTS}


def core_root(key: str) -> CoreRoot:
    try:
        return _ROOTS_BY_KEY[key]
    except KeyError:
        raise KeyError(f"Unknown core root {key!r}; one of {sorted(_ROOTS_BY_KEY)}") from None


@dataclass(frozen=True)
class Pathway:
    """One named file writer. Construct only through :func:`register_pathway`."""

    key: str
    owner_feature: str
    audience: Audience
    mode: Mode
    root: str
    subfolder: str
    naming: Naming
    description: str
    naming_pattern: str = ""
    file_access: FileAccess = "personal"
    retention_policy: str = ""
    system_folder: str = ""
    """The legacy ``SystemPathRegistry`` name this pathway replaces (``ai_images`` …), if any."""
    legacy_prefixes: tuple[str, ...] = field(default_factory=tuple)
    """Path prefixes existing rows of this pathway still live under — the mover's input."""

    @property
    def in_tree(self) -> bool:
        return self.audience == "person"

    @property
    def in_recents(self) -> bool:
        return self.audience == "person"

    @property
    def in_pick_lists(self) -> bool:
        return self.audience == "person"

    def declared(self) -> dict[str, Any]:
        """The values a ``files.file_pathway`` row stores as ``declared``."""
        out = asdict(self)
        out["legacy_prefixes"] = list(self.legacy_prefixes)
        return out


class PathwayError(ValueError):
    """A pathway declaration or resolution that cannot be honoured — the message says why."""


_PATHWAYS: dict[str, Pathway] = {}
_KEY_RE: Final = re.compile(r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$")


def _check_tokens(pattern: str, *, where: str, key: str) -> None:
    unknown = set(_TOKEN_RE.findall(pattern)) - TOKENS
    if unknown:
        raise PathwayError(f"Pathway {key!r} {where} uses unknown token(s) {sorted(unknown)}; allowed: {sorted(TOKENS)}")


def validate_pathway(p: Pathway) -> None:
    """Every rule a pathway (declared or live row) must satisfy."""
    if not _KEY_RE.match(p.key):
        raise PathwayError(f"Pathway key {p.key!r} must be '<domain>.<use>' in lower snake case")
    if p.audience not in AUDIENCES:
        raise PathwayError(f"Pathway {p.key!r}: audience must be one of {AUDIENCES}")
    if p.mode not in MODES:
        raise PathwayError(f"Pathway {p.key!r}: mode must be one of {MODES}")
    if p.naming not in NAMING_STRATEGIES:
        raise PathwayError(f"Pathway {p.key!r}: naming must be one of {NAMING_STRATEGIES}")
    if p.file_access not in FILE_ACCESS_LEVELS:
        raise PathwayError(f"Pathway {p.key!r}: file_access must be one of {FILE_ACCESS_LEVELS}")
    root = core_root(p.root)
    if p.audience == "person" and root.kind != "person":
        raise PathwayError(
            f"Pathway {p.key!r} is the person's output but its root {root.label!r} is not a person "
            f"root — it would be hidden from their Files and Recents."
        )
    if p.audience == "automated" and root.kind == "person":
        raise PathwayError(
            f"Pathway {p.key!r} is automated but its root {root.label!r} is a person root — automated "
            f"output and side effects live in System (system-files/) or Temporary."
        )
    if p.audience == "automated" and p.file_access == "personal":
        raise PathwayError(f"Pathway {p.key!r}: automated output is 'internal' or 'public', never 'personal'")
    if p.mode == "person_chooses" and p.audience != "person":
        raise PathwayError(f"Pathway {p.key!r}: only a person pathway lets the person choose the folder")
    if p.naming in ("timestamp", "source_timestamp") and not p.naming_pattern:
        raise PathwayError(f"Pathway {p.key!r}: naming {p.naming!r} needs a naming_pattern")
    _check_tokens(p.subfolder, where="subfolder", key=p.key)
    _check_tokens(p.naming_pattern, where="naming_pattern", key=p.key)
    if ".." in p.subfolder.split("/"):
        raise PathwayError(f"Pathway {p.key!r}: subfolder may not contain '..'")


def register_pathway(
    key: str,
    *,
    owner_feature: str,
    audience: Audience,
    root: str,
    subfolder: str = "",
    naming: Naming,
    description: str,
    mode: Mode = "registry",
    naming_pattern: str = "",
    file_access: FileAccess | None = None,
    retention_policy: str = "",
    system_folder: str = "",
    legacy_prefixes: tuple[str, ...] = (),
) -> Pathway:
    """Declare a pathway at import time. Re-registering the same key with other values raises."""
    p = Pathway(
        key=key,
        owner_feature=owner_feature,
        audience=audience,
        mode=mode,
        root=root,
        subfolder=subfolder.strip("/"),
        naming=naming,
        description=description,
        naming_pattern=naming_pattern,
        file_access=file_access or ("personal" if audience == "person" else "internal"),
        retention_policy=retention_policy,
        system_folder=system_folder,
        legacy_prefixes=tuple(legacy_prefixes),
    )
    validate_pathway(p)
    if system_folder:
        folder = get_system_folder(system_folder)  # raises on an unknown name
        base = "/".join(x for x in (core_root(root).path, p.subfolder.split("{", 1)[0].rstrip("/")) if x)
        if folder.root != base and not folder.root.startswith(base + "/"):
            raise PathwayError(
                f"Pathway {key!r} replaces system folder {system_folder!r} at {folder.root!r} but resolves "
                f"under {base!r}; keep them the same until the mover runs."
            )
    existing = _PATHWAYS.get(key)
    if existing is not None and existing != p:
        raise PathwayError(f"Pathway {key!r} is already registered with different values")
    _PATHWAYS[key] = p
    return p


def get_pathway(key: str) -> Pathway:
    try:
        return _PATHWAYS[key]
    except KeyError:
        raise PathwayError(
            f"Unknown pathway {key!r}. Register it with register_pathway(...) before its first write."
        ) from None


def list_pathways() -> list[Pathway]:
    return sorted(_PATHWAYS.values(), key=lambda p: p.key)


def declared_payload() -> list[dict[str, Any]]:
    """Every declared pathway as the rows ``files.file_pathway_declare(p_rows)`` takes.

    The pathway's access level is named ``file_access`` here and in the database alike.
    """
    return [p.declared() for p in list_pathways()]


def pathway_for_system_folder(name: str) -> Pathway | None:
    """The pathway that replaces a legacy ``SystemPathRegistry`` folder name, if declared."""
    for p in _PATHWAYS.values():
        if p.system_folder == name:
            return p
    return None


# ---------------------------------------------------------------------------
# Live rows (host-injected). Only LIVE_EDITABLE_FIELDS are taken from a row.
# ---------------------------------------------------------------------------

RowLoader = Callable[[str], Mapping[str, Any] | None]
_row_loader: RowLoader | None = None
_on_row_missing: Callable[[str, str], None] | None = None


def configure_pathway_rows(
    loader: RowLoader | None,
    *,
    on_row_missing: Callable[[str, str], None] | None = None,
) -> None:
    """Install the host's live-row reader and the loud notice for a missing row."""
    global _row_loader, _on_row_missing
    _row_loader = loader
    _on_row_missing = on_row_missing


def effective_pathway(key: str, row: Mapping[str, Any] | None = None) -> Pathway:
    """The declared pathway with the live row's editable fields applied (and re-validated)."""
    declared = get_pathway(key)
    if row is None and _row_loader is not None:
        row = _row_loader(key)
        if row is None and _on_row_missing is not None:
            _on_row_missing(key, "no files.file_pathway row; using the declared default")
    if not row:
        return declared
    patch = {f: row[f] for f in LIVE_EDITABLE_FIELDS if f in row and row[f] is not None}
    if not patch:
        return declared
    merged = Pathway(**{**asdict(declared), **patch, "legacy_prefixes": declared.legacy_prefixes})
    validate_pathway(merged)
    return merged


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Placement:
    """Where one write lands, and what the door stamps on the row."""

    pathway: str
    audience: Audience
    folder_path: str
    file_name: str
    file_access: FileAccess
    ai_naming_pending: bool = False

    @property
    def file_path(self) -> str:
        return f"{self.folder_path}/{self.file_name}" if self.folder_path else self.file_name

    def metadata_stamp(self) -> dict[str, Any]:
        """Metadata keys the upload door writes for this pathway."""
        if self.audience == "automated":
            return {"system_artifact": True, "artifact_domain": self.pathway}
        return {}


_UNSAFE_NAME_RE: Final = re.compile(r"[\x00-\x1f\x7f/\\‪-‮⁦-⁩]")


def sanitize_file_name(name: str) -> str:
    """One path segment: no separators, control or Bidi characters, never empty, never '.'/'..'."""
    cleaned = _UNSAFE_NAME_RE.sub("-", (name or "").strip()).strip(" .")
    return cleaned[:200] or "file"


def _fill(pattern: str, tokens: Mapping[str, str], *, key: str, where: str) -> str:
    def rep(m: re.Match[str]) -> str:
        name = m.group(1)
        value = tokens.get(name)
        if value is None or str(value) == "":
            raise PathwayError(f"Pathway {key!r} {where} needs token {{{name}}}; the writer did not supply it")
        return sanitize_file_name(str(value)) if where == "subfolder" else str(value)

    return _TOKEN_RE.sub(rep, pattern)


def _ext(original_name: str | None, extension: str | None) -> str:
    if extension:
        return extension if extension.startswith(".") else f".{extension}"
    if original_name and "." in original_name.rsplit("/", 1)[-1]:
        return "." + original_name.rsplit(".", 1)[-1].lower()
    return ""


def resolve(
    key: str,
    *,
    tokens: Mapping[str, Any] | None = None,
    original_name: str | None = None,
    extension: str | None = None,
    content: bytes | None = None,
    prompt: str | None = None,
    chosen_folder: str | None = None,
    now: datetime | None = None,
    row: Mapping[str, Any] | None = None,
) -> Placement:
    """Resolve one write of ``key`` to a folder and a file name.

    ``chosen_folder`` is the person's own pick; it is honoured unchanged for a ``person_chooses``
    pathway and refused for a ``registry`` pathway (a writer may not pick its own destination).
    """
    p = effective_pathway(key, row)
    moment = now or datetime.now(UTC)
    tok: dict[str, str] = {k: str(v) for k, v in (tokens or {}).items() if v is not None}
    tok.setdefault("yyyy", f"{moment.year:04d}")
    tok.setdefault("mm", f"{moment.month:02d}")
    tok.setdefault("dd", f"{moment.day:02d}")
    tok.setdefault("HH", f"{moment.hour:02d}")
    tok.setdefault("MI", f"{moment.minute:02d}")
    tok.setdefault("SS", f"{moment.second:02d}")
    tok.setdefault("pathway", p.key)

    if chosen_folder is not None and chosen_folder.strip("/"):
        if p.mode != "person_chooses":
            raise PathwayError(f"Pathway {key!r} decides its own folder; a writer may not choose one")
        folder = chosen_folder.strip("/")
    else:
        sub = _fill(p.subfolder, tok, key=key, where="subfolder") if p.subfolder else ""
        folder = "/".join(x for x in (core_root(p.root).path, sub) if x)

    ext = _ext(original_name, extension)
    pending = False
    naming = p.naming
    if naming == "ai_title":
        # The mandate renames after the write; the file is born with a deterministic name.
        pending = True
        naming = "prompt_slug_hash" if prompt else ("timestamp" if p.naming_pattern else "keep_original")
    if naming == "keep_original":
        if not original_name:
            raise PathwayError(f"Pathway {key!r} keeps the original name, but the writer supplied none")
        name = sanitize_file_name(original_name.rsplit("/", 1)[-1])
    elif naming == "prompt_slug_hash":
        name = slugify_prompt(prompt, content_bytes=content, fallback=p.key.split(".", 1)[1].replace("_", "-")) + ext
    elif naming in ("timestamp", "source_timestamp"):
        name = sanitize_file_name(_fill(p.naming_pattern, tok, key=key, where="naming_pattern")) + ext
    elif naming == "id_only":
        fid = tok.get("file_id")
        if not fid:
            raise PathwayError(f"Pathway {key!r} names files by id; the writer supplied no file_id token")
        name = f"{fid}{ext}"
    else:  # pragma: no cover - validate_pathway guards the enum
        raise PathwayError(f"Pathway {key!r}: unknown naming {naming!r}")
    return Placement(
        pathway=p.key,
        audience=p.audience,
        folder_path=folder,
        file_name=name,
        file_access=p.file_access,
        ai_naming_pending=pending,
    )


def pathway_for_path(file_path: str | None) -> Pathway | None:
    """The declared pathway whose CURRENT destination prefix holds ``file_path`` (longest match)."""
    if not file_path:
        return None
    path = file_path.lstrip("/")
    best: tuple[int, Pathway] | None = None
    for p in _PATHWAYS.values():
        base = "/".join(x for x in (core_root(p.root).path, p.subfolder.split("{", 1)[0].rstrip("/")) if x)
        if path == base or path.startswith(base + "/"):
            if p.mode == "person_chooses" and p.subfolder == "":
                continue  # a bare person root is a choice, not this pathway's signature
            if best is None or len(base) > best[0]:
                best = (len(base), p)
    return best[1] if best else None




# ---------------------------------------------------------------------------
# CARRIED ROOTS (PLAN § 7, Lane 5) — a service writing FOR an organization files under the pathway.
# ---------------------------------------------------------------------------


def pathway_for_carried_root(root: str) -> Pathway | None:
    """The pathway that took over the old ``<root>-<organization uuid>`` tree (its ``legacy_prefixes``
    name ``"<root>-"``), or ``None`` when no declared pathway claims it. The registry is the one map;
    there is no second root→pathway table."""
    hits = sorted(
        (p for p in _PATHWAYS.values() if f"{root}-" in p.legacy_prefixes), key=lambda p: p.key
    )
    return hits[0] if hits else None


def pathway_base_folder(key: str) -> str:
    """The fixed part of a pathway's destination: the core root plus its subfolder up to the first
    ``{token}`` (``system-files/runs`` for ``runs/{run}``). Live subfolder edits apply."""
    p = effective_pathway(key)
    sub = p.subfolder.split("{", 1)[0].rstrip("/")
    return "/".join(x for x in (core_root(p.root).path, sub) if x)


def carried_folder_segments(key: str, source_key: str, source_label: str) -> list[tuple[str, str]]:
    """``[(path segment, folder name), ...]`` for one organization's carried files under pathway
    ``key``: the pathway's base folder, then the source (a table, provider or scope id, named for a
    person) unless the base already ends with it (``system-files/diagram-checks`` + ``diagram-checks``).
    This is the same layout the mover gave existing rows (old tail kept under the base, org dropped
    from the path — the organization is the row's column, never path text)."""
    base = pathway_base_folder(key)
    parts = [x for x in base.split("/") if x]
    root = core_root(effective_pathway(key).root)
    segments = [(seg, root.label if i == 0 else seg) for i, seg in enumerate(parts)]
    if not parts or parts[-1] != str(source_key):
        segments.append((str(source_key), source_label))
    return segments


def org_suffixed_name(file_name: str, organization_id: str) -> str:
    """``name (<org8>).ext`` — the ONE cross-organization collision rule, shared with the mover
    (``files.file_pathway_relocate``): the person's path key is unique across organizations, so a
    second organization's file at the same path gets this deterministic name, never the first one's row."""
    stem, dot, ext = file_name.rpartition(".")
    tag = f" ({str(organization_id)[:8]})"
    return f"{stem}{tag}.{ext}" if dot else f"{file_name}{tag}"

# ---------------------------------------------------------------------------
# THE STAMP POINT (PLAN § 4.2a) — the one upload door calls this for every row it writes.
# ---------------------------------------------------------------------------

_unregistered_logger = logging.getLogger("matrx_files.placement.unregistered")
_UNREGISTERED_SEEN: set[str] = set()


def _caller_outside_package() -> str:
    """``module:line`` of the first frame outside matrx_files — the writer that named no pathway."""
    import sys

    frame = sys._getframe(2)
    while frame is not None:
        mod = frame.f_globals.get("__name__", "")
        if not mod.startswith("matrx_files"):
            return f"{mod}:{frame.f_lineno}"
        frame = frame.f_back
    return "matrx_files:?"


def stamp_for_write(
    pathway: str | None, file_path: str | None, metadata: dict | None
) -> tuple[dict | None, str | None]:
    """``(metadata, file_pathway)`` for one row written at the upload door.

    A named pathway must be declared (``PathwayError`` otherwise); an AUTOMATED pathway stamps the
    system marker (``system_artifact`` + ``artifact_domain`` defaulting to the key), a person
    pathway stamps nothing. The database guard ``files.file_pathway_guard`` checks the same.
    With no pathway the legacy path marker applies (``user_visible.stamp_machine_artifact``) and the
    writer is reported once per process as UNREGISTERED (``file-placement-unregistered``) — the
    admin page's Unregistered tab; knob ``files.placement_enforce`` turns system rows with no
    pathway into a refusal in the database.
    """
    from .user_visible import stamp_machine_artifact

    if pathway:
        p = get_pathway(pathway)
        if p.audience == "automated":
            out = dict(metadata or {})
            out["system_artifact"] = True
            out.setdefault("artifact_domain", p.key)
            return out, p.key
        return metadata, p.key
    caller = _caller_outside_package()
    if caller not in _UNREGISTERED_SEEN:
        _UNREGISTERED_SEEN.add(caller)
        _unregistered_logger.warning(
            "file-placement-unregistered: %s wrote %r without a pathway (placement registry § 4.3)",
            caller,
            file_path,
            extra={"feature": "file-placement-unregistered", "writer": caller, "file_path": file_path},
        )
    return stamp_machine_artifact(file_path, metadata), None

def client_person_pathway(metadata: dict | None) -> str | None:
    """The PERSON pathway a client upload named (``file_pathway`` in its metadata), popped off the row
    metadata. ``None`` for no name, an undeclared one, or an automated one — automated pathways are
    server-only, so a client naming one is dropped loudly, never stamped. Both client upload doors
    (resumable TUS and the buffered ``POST /files/upload``) call this, so they cannot disagree."""
    if not metadata or "file_pathway" not in metadata:
        return None
    name = metadata.pop("file_pathway")
    try:
        p = get_pathway(str(name))
    except Exception:
        _unregistered_logger.warning("client upload named undeclared file pathway %r — dropped (placement § 4.2)", name)
        return None
    if p.audience != "person":
        _unregistered_logger.warning("client upload named automated file pathway %r — server-only, dropped (§ 4.2)", name)
        return None
    return p.key


def _prefix_holds(prefix: str, path: str) -> bool:
    """A legacy prefix ending in ``-`` names a carried root (``seo-data-`` holds
    ``seo-data-<org>/…``); any other prefix is a folder (``coding-sessions`` holds
    ``coding-sessions/…``)."""
    prefix = prefix.strip("/")
    if not prefix:
        return False
    if prefix.endswith("-"):
        head = path.split("/", 1)[0]
        return head.startswith(prefix) and len(head) > len(prefix)
    return path == prefix or path.startswith(prefix + "/")


def automated_pathway_for_path(file_path: str | None) -> Pathway | None:
    """The AUTOMATED pathway whose destination or one of whose ``legacy_prefixes`` holds
    ``file_path`` (longest prefix wins, then key). ``None`` for a person path or a path no
    automated pathway claims."""
    if not file_path:
        return None
    path = file_path.lstrip("/")
    best: tuple[int, str, Pathway] | None = None
    for p in _PATHWAYS.values():
        if p.audience != "automated":
            continue
        base = "/".join(x for x in (core_root(p.root).path, p.subfolder.split("{", 1)[0].rstrip("/")) if x)
        for prefix in (base, *p.legacy_prefixes):
            if prefix == core_root(p.root).path:
                continue  # the bare System root is every automated pathway's, so no one's signature
            if _prefix_holds(prefix, path):
                cand = (len(prefix.strip("/")), p.key, p)
                if best is None or cand[0] > best[0] or (cand[0] == best[0] and cand[1] < best[1]):
                    best = cand
    return best[2] if best else None


def client_upload_pathway(metadata: dict | None, file_path: str | None) -> str | None:
    """The pathway a CLIENT upload is stamped with — the one rule both client doors (resumable TUS
    and the buffered ``POST /files/upload``) share.

    1. The PERSON pathway the client named (:func:`client_person_pathway`; an automated name is
       dropped — a client never chooses an automated pathway).
    2. Else the AUTOMATED pathway the registry places at this path (:func:`automated_pathway_for_path`):
       an out-of-repo machine writer (the desktop coding-session recorder at ``coding-sessions/…``, a
       device mirror re-uploading ``seo-data-<org>/…`` or ``page-captures-<org>/…``) cannot name a
       pathway, but its path is the registry's own declaration, so the SERVER decides from it — the
       same decision the path marker (``user_visible.stamp_machine_artifact``) already makes, now
       with a name, so ``files.placement_enforce`` never refuses such a write.
    """
    named = client_person_pathway(metadata)
    if named:
        return named
    claimed = automated_pathway_for_path(file_path)
    return claimed.key if claimed else None


from . import _builtin_pathways  # noqa: E402,F401  (registers the package's own pathways)

__all__ = [
    "AUDIENCES",
    "CORE_ROOTS",
    "LIVE_EDITABLE_FIELDS",
    "MODES",
    "NAMING_STRATEGIES",
    "TOKENS",
    "FILE_ACCESS_LEVELS",
    "CoreRoot",
    "Pathway",
    "PathwayError",
    "Placement",
    "carried_folder_segments",
    "automated_pathway_for_path",
    "client_person_pathway",
    "client_upload_pathway",
    "configure_pathway_rows",
    "core_root",
    "declared_payload",
    "effective_pathway",
    "get_pathway",
    "list_pathways",
    "org_suffixed_name",
    "pathway_base_folder",
    "pathway_for_carried_root",
    "pathway_for_path",
    "pathway_for_system_folder",
    "register_pathway",
    "stamp_for_write",
    "resolve",
    "sanitize_file_name",
    "validate_pathway",
]
