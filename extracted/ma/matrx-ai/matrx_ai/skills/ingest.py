"""Filesystem → DB ingestion (Phase 2).

Walks a directory of SKILL.md files (Claude Code / Cursor layout) and
upserts them into ``skill.definition`` with ``is_system=true``. Supports
two layouts:

  layout A:  <root>/<skill_id>/SKILL.md        (folder + optional resources)
  layout B:  <root>/<skill_id>.md              (flat single file)

Idempotency:
  * Skills are keyed on ``skill_id`` (= folder name or filename stem).
  * The body's SHA-256 hash is stored in ``config['source_hash']``; an
    unchanged body at an unchanged path on an active row skips the UPDATE.
  * Skills present in the DB but not on disk are LEFT ALONE unless the
    caller passes ``prune_scopes`` — then a vanished mirror *inside those
    scopes* is DEACTIVATED (``is_active=False`` + ``config.pruned_at``),
    never hard-deleted. See THE OWNERSHIP GUARD below.

Ownership: this ingest writes ONLY rows it created (``config.ingested_from``).
``skill.definition`` also holds 143 DB-native ``render_block`` rows and a
handful of hand-authored ``reference``/``workflow`` rows; a repo folder sharing
one of those names is reported as ``skipped_foreign`` and nothing is written.

YAML frontmatter (between `---` fences) supplies metadata:

    ---
    name: my-skill              # business-key override (defaults to filename)
    description: One-liner.     # required
    skill_type: convention      # optional; defaults to 'reference'
    category: persistence       # optional; matches platform.categories.slug (dimension="skill")
    allowed_tools: []           # optional; list of tool UUIDs or names
    trigger_patterns: []        # optional
    disable_auto_invocation: false
    version: '1.0.0'
    ---

    # Markdown body
    ...
"""

from __future__ import annotations

import asyncio
import hashlib
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID

from matrx_utils import vcprint

_YAML_FENCE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def _parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Split YAML frontmatter from body. Returns ``({}, content)`` when
    no frontmatter fence is found."""
    m = _YAML_FENCE.match(content)
    if not m:
        return {}, content

    fm_raw = m.group(1)
    body = content[m.end() :]

    fm: Any = None
    try:
        import yaml  # type: ignore[import-not-found]

        try:
            fm = yaml.safe_load(fm_raw) or {}
        except yaml.YAMLError:
            # SKILL.md descriptions frequently contain unquoted colons,
            # semicolons, and other YAML-significant chars that a strict
            # parser rejects. Fall back to our line-oriented minimal parser
            # so dev skills authored for Claude Code / Cursor still ingest.
            fm = _minimal_yaml(fm_raw)
    except ImportError:
        fm = _minimal_yaml(fm_raw)

    if not isinstance(fm, dict):
        fm = {}
    return fm, body


def _minimal_yaml(text: str) -> dict[str, Any]:
    """Tiny key: value parser for the handful of fields we care about.
    Supports strings, bools, ints, and simple flow-style lists ([a, b]).
    Multi-line values aren't supported — install PyYAML if you need them.
    """
    out: dict[str, Any] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if not value:
            out[key] = ""
            continue
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            out[key] = [v.strip().strip("'\"") for v in inner.split(",") if v.strip()]
            continue
        if value.lower() in {"true", "false"}:
            out[key] = value.lower() == "true"
            continue
        if value.isdigit():
            out[key] = int(value)
            continue
        out[key] = value.strip("'\"")
    return out


def _hash(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# The live `skl_skill_type` enum. Kept here so a bad frontmatter value is
# rejected at parse time instead of surfacing as a per-row DB error.
_VALID_SKILL_TYPES = frozenset(
    {
        "render_block",
        "convention",
        "workflow",
        "task",
        "reference",
        "mode",
        "agent_behavior",
    }
)


# THE FLAT-FILE GUARD (2026-09-11). A bare ``<name>.md`` sitting in a skills
# directory is a skill ONLY when it declares itself one (frontmatter carrying
# both an id-ish key and a description — what every Claude/Cursor skill has).
# Plain directory docs that live beside skills are NOT skills: the 2026-07-16
# import ingested ``common-docs/skills/index.md`` (the bundle's listing) and
# ``matrx-frontend/features/skills/FEATURE.md`` (a React feature's doc) as the
# live platform skills "index" and "FEATURE". Folder layout
# (``<skill_id>/SKILL.md``) is unaffected — the folder IS the declaration.
_RESERVED_FLAT_STEMS = frozenset(
    {
        "readme",
        "index",
        "feature",
        "claude",
        "agent",
        "agents",
        "changelog",
        "module_readme",
        "state",
        "decisions",
        "plan",
        "vision",
        "notes",
        "todo",
        "contributing",
        "license",
    }
)


def _flat_md_is_skill(file_name: str, content: str) -> bool:
    """Is this bare ``<name>.md`` in a skills dir actually a skill?"""
    stem = file_name[:-3] if file_name.lower().endswith(".md") else file_name
    if stem.strip().lower().replace("-", "_") in _RESERVED_FLAT_STEMS:
        return False
    fm, _ = _parse_frontmatter(content)
    has_id = bool(_first_present(fm, "name", "skill_id", "id", "slug"))
    has_description = bool(_first_present(fm, "description", "desc", "summary", "about"))
    return has_id and has_description


# ---------------------------------------------------------------------------
# Filesystem walk
# ---------------------------------------------------------------------------


class ParsedSkill:
    """In-memory representation of one parsed SKILL.md."""

    __slots__ = (
        "skill_id",
        "label",
        "description",
        "skill_type",
        "declared_skill_type",
        "body",
        "category",
        "allowed_tools",
        "trigger_patterns",
        "disable_auto_invocation",
        "version",
        "source_hash",
        "source_path",
    )

    def __init__(
        self,
        *,
        skill_id: str,
        label: str,
        description: str,
        skill_type: str,
        declared_skill_type: bool,
        body: str,
        category: str | None,
        allowed_tools: list[str],
        trigger_patterns: list[str],
        disable_auto_invocation: bool,
        version: str | None,
        source_hash: str,
        source_path: str,
    ) -> None:
        self.skill_id = skill_id
        self.label = label
        self.description = description
        self.skill_type = skill_type
        self.declared_skill_type = declared_skill_type
        self.body = body
        self.category = category
        self.allowed_tools = allowed_tools
        self.trigger_patterns = trigger_patterns
        self.disable_auto_invocation = disable_auto_invocation
        self.version = version
        self.source_hash = source_hash
        self.source_path = source_path


def _first_present(fm: dict[str, Any], *keys: str) -> Any:
    """Return the value of the first frontmatter key that's present + truthy."""
    for k in keys:
        v = fm.get(k)
        if v not in (None, "", []):
            return v
    return None


def _coerce_list(value: Any) -> list[str]:
    """Tolerate scalar strings, comma-separated strings, and real lists."""
    if value in (None, "", []):
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        # ``"a, b , c"`` → ``["a", "b", "c"]``; single value just becomes [value]
        if "," in value:
            return [s.strip() for s in value.split(",") if s.strip()]
        return [value.strip()] if value.strip() else []
    return [str(value)]


def _parse_content(content: str, *, skill_id: str, source_path: str) -> ParsedSkill | None:
    """Parse SKILL.md content (already-loaded string) into a ParsedSkill.

    The pure-content variant of :func:`_parse_file` — used by the sandbox
    proxy walker, which streams content over HTTP rather than reading from
    the local filesystem. Both entry points share identical semantics from
    here on.
    """
    fm, body = _parse_frontmatter(content)

    fm_id = _first_present(fm, "name", "skill_id", "id", "slug")
    if isinstance(fm_id, str) and fm_id:
        # Normalise: spaces → dashes, lowercase. Most authors expect this.
        skill_id = fm_id.strip().replace(" ", "-")

    # Description
    description = _first_present(fm, "description", "desc", "summary", "about") or ""
    description = str(description).strip()
    if not description:
        # Fallback chain: first non-heading paragraph in the body.
        for line in body.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            description = stripped[:300]
            break
    if not description:
        # Last resort: use the first heading text.
        for line in body.splitlines():
            stripped = line.strip().lstrip("#").strip()
            if stripped:
                description = stripped[:300]
                break
    if not description:
        description = skill_id

    # Label — explicit field, else first H1 in body, else titleized id.
    label = _first_present(fm, "label", "title")
    if not label:
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                label = stripped.lstrip("#").strip()
                break
    if not label:
        label = skill_id.replace("-", " ").replace("_", " ").title()

    # A frontmatter key we do not own can carry anything. `type: Skill` — the
    # Claude/Cursor DOCUMENT-type marker on all 45 common-docs skills — is not a
    # `skl_skill_type` value, and feeding it through cost 29 rows their update
    # with `Input should be 'render_block', 'convention', …`. So a declared type
    # counts only when it IS one of the enum's values; anything else is treated
    # as "not declared" (default for a new row, existing type kept for an old one).
    declared_raw = _first_present(fm, "skill_type", "type", "kind", "category_type")
    declared_type = None
    if isinstance(declared_raw, str):
        normalized = declared_raw.strip().lower().replace("-", "_").replace(" ", "_")
        if normalized in _VALID_SKILL_TYPES:
            declared_type = normalized
    skill_type = declared_type or "reference"

    # Category can be a single string or (less commonly) a list.
    category_raw = _first_present(fm, "category", "categories", "group")
    if isinstance(category_raw, list) and category_raw:
        category = str(category_raw[0])
    elif isinstance(category_raw, str):
        category = category_raw
    else:
        category = None

    triggers = _coerce_list(_first_present(fm, "trigger_patterns", "triggers", "when_to_use"))
    tools = _coerce_list(_first_present(fm, "allowed_tools", "tools", "required_tools"))

    version_raw = _first_present(fm, "version", "v", "semver")
    version = str(version_raw) if version_raw else None

    disable_auto = bool(_first_present(fm, "disable_auto_invocation", "no_auto_invoke") or False)

    return ParsedSkill(
        skill_id=skill_id,
        label=str(label)[:300],
        description=str(description)[:2000],
        skill_type=str(skill_type),
        declared_skill_type=bool(declared_type),
        body=body.strip(),
        category=category,
        allowed_tools=tools,
        trigger_patterns=triggers,
        disable_auto_invocation=disable_auto,
        version=version,
        source_hash=_hash(body),
        source_path=source_path,
    )


def _parse_file(path: Path, skill_id: str) -> ParsedSkill | None:
    """Parse one SKILL.md / .md file on the local filesystem.

    Tolerates the same format drift documented on :func:`_parse_content`;
    only difference is the I/O wrapper that reads bytes off disk.
    """
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as exc:
        vcprint(f"[skills.ingest] read failed {path}: {exc}", color="red")
        return None
    return _parse_content(content, skill_id=skill_id, source_path=str(path))


def walk_filesystem(root: Path | str) -> list[ParsedSkill]:
    """Walk a *single* skills directory, return every parsed SKILL.md.

    Treats ``root`` as a leaf skills directory — direct children are
    expected to be ``<skill_id>/SKILL.md`` folders OR ``<skill_id>.md``
    files. Use :func:`discover_and_walk` to auto-find skill directories
    inside a repo / parent path.
    """
    root_path = Path(root)
    if not root_path.exists() or not root_path.is_dir():
        vcprint(f"[skills.ingest] root not found: {root_path}", color="yellow")
        return []

    skills: list[ParsedSkill] = []
    for child in sorted(root_path.iterdir()):
        if child.is_dir():
            skill_md = child / "SKILL.md"
            if skill_md.exists():
                parsed = _parse_file(skill_md, skill_id=child.name)
                if parsed:
                    skills.append(parsed)
        elif child.suffix.lower() == ".md":
            try:
                content = child.read_text(encoding="utf-8")
            except Exception as exc:
                vcprint(f"[skills.ingest] read failed {child}: {exc}", color="yellow")
                continue
            if not _flat_md_is_skill(child.name, content):
                continue
            parsed = _parse_content(content, skill_id=child.stem, source_path=str(child))
            if parsed:
                skills.append(parsed)

    return skills


# ---------------------------------------------------------------------------
# Discovery — find every conventional skill directory inside a repo / parent
# ---------------------------------------------------------------------------

# The conventions we recognize. Order matters only for stable reporting; the
# walker dedups by skill_id later, with later sources overriding earlier ones.
# Add a new convention here when a new client / tool ships one.
_SKILL_DIR_CONVENTIONS: tuple[str, ...] = (
    ".claude/skills",
    ".cursor/skills",
    ".agent/skills",
    ".agents/skills",
    ".matrx/skills",
    "skills",
)


def _looks_like_skills_dir(path: Path) -> bool:
    """Return True if ``path`` itself is a *recognized* skills directory.

    A directory qualifies only when:

      1. Its path ends with one of ``_SKILL_DIR_CONVENTIONS``
         (e.g. ``.../.cursor/skills``, ``.../skills``) AND it has at
         least one plausible child (``<name>/SKILL.md`` or a non-README
         ``<name>.md``), OR
      2. Its basename is exactly ``skills`` AND it contains at least one
         ``<name>/SKILL.md`` folder (a custom skills leaf passed
         explicitly).

    Never treat an arbitrary parent (``$HOME``, a repo root, ``~/code``)
    as a skills leaf just because one child happens to carry a
    ``SKILL.md`` — that short-circuits recursive discovery and skips
    ``~/.claude/skills`` / ``~/.cursor/skills``. Real incident: home
    matched via ``~/Downloads/SKILL.md`` and ingested only that one.
    """
    if not path.is_dir():
        return False
    try:
        children = list(path.iterdir())
    except PermissionError:
        return False

    # A directory with __init__.py is a Python package, not a skills dir,
    # even if its name happens to be ``skills``. Bail early.
    if (path / "__init__.py").exists():
        return False

    has_skill_md_folder = any(
        child.is_dir() and (child / "SKILL.md").exists() for child in children
    )
    def _is_flat_skill(child: Path) -> bool:
        if not (child.is_file() and child.suffix.lower() == ".md"):
            return False
        try:
            return _flat_md_is_skill(child.name, child.read_text(encoding="utf-8"))
        except Exception:
            return False

    has_md = any(_is_flat_skill(child) for child in children)

    resolved_str = str(path)
    matches_convention = any(
        resolved_str.endswith(f"/{conv}") or resolved_str.endswith(f"{os.sep}{conv}")
        for conv in _SKILL_DIR_CONVENTIONS
    )
    if matches_convention:
        return has_skill_md_folder or has_md

    # Custom leaf: basename "skills" + folder/SKILL.md children only.
    return path.name == "skills" and has_skill_md_folder


def discover_skill_roots(
    start: Path | str,
    *,
    max_depth: int = 4,
) -> list[Path]:
    """Find every skills directory at or under ``start``.

    Strategy:
        1. If ``start`` is itself a leaf skills dir → return [start].
        2. Otherwise walk subdirectories looking for any of the
           conventional locations (``.claude/skills``, ``.cursor/skills``,
           ``.agent[s]/skills``, ``.matrx/skills``, ``skills``).
        3. Avoid descending into noisy / huge trees (``node_modules``,
           ``.git``, ``.venv``, ``__pycache__``, ``dist``, ``build``).

    ``max_depth`` caps how deep we recurse from ``start``. Default 4 is
    enough for a typical layout like ``~/code/<repo>/.cursor/skills``.
    """
    start_path = Path(start).expanduser().resolve()
    if not start_path.exists() or not start_path.is_dir():
        return []

    # Step 1: passed a leaf skills dir directly.
    if _looks_like_skills_dir(start_path):
        return [start_path]

    excluded_names = {
        "node_modules",
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "dist",
        "build",
        ".next",
        ".turbo",
        ".cache",
        "target",
        ".terraform",
        "vendor",
        # macOS / home-dir noise — walking these from $HOME burns seconds
        # and never holds skills. Convention probes still hit
        # ~/.claude/skills etc. at depth 0 before descent. Pass
        # ~/Documents or ~/Desktop explicitly if a project lives there.
        "Library",
        "Applications",
        "Pictures",
        "Movies",
        "Music",
        "Public",
        "Downloads",
        ".Trash",
        ".npm",
        ".nvm",
        ".local",
        ".docker",
        ".rustup",
        ".cargo",
        ".pyenv",
        ".vscode",
        ".idea",
    }

    # Path-segment exclusions: any directory whose RESOLVED path contains
    # one of these segments is skipped entirely. ``.claude/worktrees`` is
    # the canonical case — Claude Code creates per-branch worktree clones
    # of the parent repo there, each with its own ``.claude/skills``. We
    # never want to ingest those duplicates. Same idea for any other
    # ``worktrees`` convention. Extension/plugin caches ship their own
    # ``skills/`` trees that are not user-authored Matrx skills.
    excluded_segments = (
        "/.claude/worktrees/",
        "/.cursor/worktrees/",
        "/.agent/worktrees/",
        "/.agents/worktrees/",
        "/.matrx/worktrees/",
        "/worktrees/",
        "/extensions/",
        "/.claude/plugins/",
        "/.codex/",
        "/.tmp/",
        "/.antigravity/",
        "/node_modules/",
        "/.venv/",
    )
    found: list[Path] = []
    seen: set[Path] = set()

    def _is_in_excluded_segment(p: Path) -> bool:
        s = str(p.resolve())
        # Normalise Windows separators to forward slashes for the check.
        s_norm = s.replace(os.sep, "/")
        return any(seg in s_norm for seg in excluded_segments)

    def _walk(current: Path, depth: int) -> None:
        if depth > max_depth:
            return
        if _is_in_excluded_segment(current):
            return
        # Probe every convention at this level before descending.
        for convention in _SKILL_DIR_CONVENTIONS:
            candidate = current / convention
            if candidate.exists() and candidate.is_dir():
                if _is_in_excluded_segment(candidate):
                    continue
                resolved = candidate.resolve()
                if resolved in seen:
                    continue
                if _looks_like_skills_dir(candidate):
                    seen.add(resolved)
                    found.append(candidate)
        # Descend into subdirectories that AREN'T themselves skill
        # conventions (we already probed those at this level).
        try:
            children = list(current.iterdir())
        except PermissionError:
            return
        for child in children:
            if not child.is_dir():
                continue
            if child.name in excluded_names or child.name.startswith(".git"):
                continue
            # If the child IS one of our conventions, we already probed
            # for it above — skip the descent (we don't want to recurse
            # into .cursor/skills again).
            if any(str(child.resolve()).endswith(conv) for conv in _SKILL_DIR_CONVENTIONS):
                continue
            _walk(child, depth + 1)

    _walk(start_path, 0)
    return found


# ---------------------------------------------------------------------------
# Sandbox-proxy walk — discover skills inside a remote sandbox / local-PC
# binding via the fs_list / fs_read HTTP proxy. Same parsing semantics as the
# local walker; the only difference is where the bytes come from.
# ---------------------------------------------------------------------------

# Path-segment exclusions reused from the local walker — the sandbox's repo
# tree can contain worktree clones too.
_PROXY_EXCLUDED_SEGMENTS = (
    "/.claude/worktrees/",
    "/.cursor/worktrees/",
    "/.agent/worktrees/",
    "/.agents/worktrees/",
    "/.matrx/worktrees/",
    "/worktrees/",
)


async def walk_via_proxy(
    binding: Any,
    *,
    root_path: str | None = None,
    timeout: float = 30.0,
) -> tuple[list[ParsedSkill], list[str]]:
    """Discover SKILL.md files inside a remote sandbox via the fs proxy.

    Walks ``<root_path>/<convention>`` for each of the recognized skill
    conventions (``.claude/skills``, ``.cursor/skills`` …). Reads each
    SKILL.md over HTTP and runs the same parser the local walker uses.

    Args:
        binding: A ``SandboxBinding`` (the dataclass from
            ``matrx_ai.tools._sandbox_proxy``) OR an object with the same
            shape — ``sandbox_id, base_url, access_token, root_path``.
            The ``SandboxBindingRequest`` Pydantic model from
            ``aidream.api.sandbox_binding`` is duck-compatible.
        root_path: Override the binding's default ``root_path``. Most
            callers leave this ``None`` and use the binding's value.
        timeout: HTTP timeout per fs call.

    Returns:
        ``(skills, roots)`` — the parsed skills (deduped by ``skill_id``;
        later root wins on conflict, matching the local walker) and the
        list of skill directories that were actually discovered.

    Never raises: any proxy error short-circuits the affected directory
    and logs via ``vcprint``. The auto-discovery hook depends on this —
    a misbehaving sandbox must not break the agent's first turn.
    """
    # Lazy import — keeps the package importable in environments that don't
    # have httpx (tests / type-only consumers).
    try:
        from matrx_ai.tools._sandbox_proxy import (
            SandboxBinding,
            SandboxProxyError,
            fs_list,
            fs_read,
        )
    except Exception as exc:
        vcprint(
            f"[skills.ingest] sandbox proxy unavailable: {exc!r}",
            color="yellow",
        )
        return [], []

    # Coerce the input to the proxy's dataclass shape. Accepts either the
    # frozen dataclass or any pydantic-style object with the same fields.
    if isinstance(binding, SandboxBinding):
        b: SandboxBinding = binding
    else:
        try:
            b = SandboxBinding(
                sandbox_id=getattr(binding, "sandbox_id"),
                base_url=getattr(binding, "base_url"),
                access_token=getattr(binding, "access_token"),
                root_path=getattr(binding, "root_path", None) or "/home/agent",
            )
        except AttributeError as exc:
            vcprint(
                f"[skills.ingest] walk_via_proxy bad binding: {exc!r}",
                color="red",
            )
            return [], []

    effective_root = (root_path or b.root_path or "/home/agent").rstrip("/")

    discovered_roots: list[str] = []
    by_id: dict[str, ParsedSkill] = {}

    for convention in _SKILL_DIR_CONVENTIONS:
        candidate = f"{effective_root}/{convention}"
        if any(seg in f"{candidate}/" for seg in _PROXY_EXCLUDED_SEGMENTS):
            continue
        try:
            top = await fs_list(b, candidate, recursive=False, depth=1)
        except SandboxProxyError as exc:
            # 404 just means this convention isn't present — common case.
            if getattr(exc, "status", None) != 404:
                vcprint(
                    f"[skills.ingest] proxy fs_list {candidate} failed: {exc}",
                    color="yellow",
                )
            continue
        except Exception as exc:
            vcprint(
                f"[skills.ingest] proxy fs_list {candidate} unexpected error: {exc!r}",
                color="yellow",
            )
            continue

        entries = top.get("entries") or []
        if not entries:
            continue
        discovered_roots.append(candidate)

        for entry in entries:
            name = entry.get("name") or ""
            kind = entry.get("kind") or ""
            path = entry.get("path") or f"{candidate}/{name}"
            if not name:
                continue

            if kind in ("dir", "directory"):
                # layout A: <skill_id>/SKILL.md
                skill_md_path = f"{path.rstrip('/')}/SKILL.md"
                try:
                    content = await fs_read(b, skill_md_path, encoding="utf8")
                except SandboxProxyError as exc:
                    if getattr(exc, "status", None) != 404:
                        vcprint(
                            f"[skills.ingest] proxy fs_read {skill_md_path} failed: {exc}",
                            color="yellow",
                        )
                    continue
                except Exception as exc:
                    vcprint(
                        f"[skills.ingest] proxy fs_read {skill_md_path} unexpected error: {exc!r}",
                        color="yellow",
                    )
                    continue
                parsed = _parse_content(
                    content,
                    skill_id=name,
                    source_path=f"sandbox://{b.sandbox_id}{skill_md_path}",
                )
                if parsed:
                    by_id[parsed.skill_id] = parsed

            elif kind in ("file", "regular_file"):
                # layout B: <skill_id>.md
                if not name.lower().endswith(".md"):
                    continue
                stem = name[:-3]
                try:
                    content = await fs_read(b, path, encoding="utf8")
                except Exception as exc:
                    vcprint(
                        f"[skills.ingest] proxy fs_read {path} failed: {exc!r}",
                        color="yellow",
                    )
                    continue
                # Same flat-file guard as the local walker — a README/index/
                # FEATURE doc beside skills is not a skill.
                if not _flat_md_is_skill(name, content):
                    continue
                parsed = _parse_content(
                    content,
                    skill_id=stem,
                    source_path=f"sandbox://{b.sandbox_id}{path}",
                )
                if parsed:
                    by_id[parsed.skill_id] = parsed

    return list(by_id.values()), discovered_roots


def walk_paths(
    paths: list[Path | str],
) -> tuple[list[ParsedSkill], list[Path], list[str]]:
    """Discover + walk one or many paths.

    Each path can be a leaf skills directory OR a repo / parent dir; we
    use :func:`discover_skill_roots` to expand the latter. Returns the
    full parsed-skill list (deduped by skill_id — later wins), the list of
    skill directories actually visited, and a list of human-readable
    COLLISION notes.

    Collisions are reported, never silent (2026-09-11): the same skill_id
    lives in four repos at once (``create-agent`` is synced into aidream,
    matrx-frontend, matrx-extend AND common-docs by
    ``common-docs/meta/scripts/sync_skills.py``). "Later root wins" is the
    right rule for byte-identical synced copies, but when the bodies DIFFER
    the loser is silently discarded — that is a drift report the operator
    must see, not an implementation detail.
    """
    roots: list[Path] = []
    seen_roots: set[Path] = set()
    for entry in paths:
        for r in discover_skill_roots(entry):
            if r in seen_roots:
                continue
            seen_roots.add(r)
            roots.append(r)

    by_id: dict[str, ParsedSkill] = {}
    collisions: list[str] = []
    for root in roots:
        for parsed in walk_filesystem(root):
            prior = by_id.get(parsed.skill_id)
            if prior is not None and prior.source_hash != parsed.source_hash:
                collisions.append(
                    f"{parsed.skill_id}: differing copies — using {parsed.source_path}, "
                    f"discarding {prior.source_path}"
                )
            by_id[parsed.skill_id] = parsed  # later root wins on conflict
    return list(by_id.values()), roots, collisions


# ---------------------------------------------------------------------------
# DB upsert
# ---------------------------------------------------------------------------


# THE OWNERSHIP GUARD (2026-09-11). ``skill.definition`` is ONE table holding
# several populations that this ingest did not author and must never touch:
#
#   * 143 ``render_block`` rows (the kind/content-IR catalog, DB-native).
#   * hand-authored ``reference`` rows the platform serves to agents —
#     ``credential-login`` (the canonical Vault sign-in flow, visibility=public),
#     ``cms-authoring``, ``content-plan-actions``, ``pronunciation-authoring``,
#     ``flashcard-generation``, ``matrx-db-canonical-data-model``.
#   * ``workflow`` rows authored in the skill editor.
#
# A repo folder can carry the SAME skill_id as one of those rows —
# ``aidream/.claude/skills/credential-login/`` is exactly that case. Before this
# guard, ingesting it would have overwritten the live row's body, replaced its
# whole ``config``, and flipped visibility public → internal, because the only
# lookup key was ``skill_id``.
#
# So: a row is ingest-owned ONLY when it already carries ``config.ingested_from``.
# Anything else is reported as ``skipped_foreign`` and left byte-for-byte alone.
# Adopting a DB-native row into the mirror is a deliberate act (``--adopt``),
# never a side effect of a name collision.
_OWNED_SOURCES = frozenset({"filesystem", "sandbox"})


def _row_config(row: Any) -> dict[str, Any]:
    cfg = getattr(row, "config", None)
    return cfg if isinstance(cfg, dict) else {}


def _is_ingest_owned(row: Any) -> bool:
    """True when this row was created by a previous ingest run."""
    return _row_config(row).get("ingested_from") in _OWNED_SOURCES


def _source_repo(source_path: str) -> str | None:
    """Best-effort ``<repo>`` label for a source path, for row provenance.

    ``/Users/x/code/matrx-frontend/.claude/skills/foo/SKILL.md`` → ``matrx-frontend``.
    Anything that doesn't sit under a recognized skills convention returns None
    rather than guessing.
    """
    norm = source_path.replace(os.sep, "/")
    for conv in _SKILL_DIR_CONVENTIONS:
        marker = f"/{conv}/"
        idx = norm.find(marker)
        if idx == -1:
            continue
        head = norm[:idx]
        return head.rsplit("/", 1)[-1] or None
    return None


def _looks_like_sandbox_binding(obj: Any) -> bool:
    """Duck-type check — anything with sandbox_id+base_url+access_token is
    treated as a sandbox binding (vs. a host path)."""
    if obj is None or isinstance(obj, (str, Path)):
        return False
    return hasattr(obj, "sandbox_id") and hasattr(obj, "base_url") and hasattr(obj, "access_token")


async def ingest_filesystem(
    roots_or_binding: Any,
    *,
    admin_user_id: UUID | str,
    dry_run: bool = False,
    is_system: bool = True,
    prune_scopes: list[str] | None = None,
    adopt: bool = False,
) -> dict[str, Any]:
    """Upsert every parsed SKILL.md into ``skill.definition``.

    Two input modes:

    1. **Host paths** (existing behaviour): pass a path, a Path, or a list
       of paths. Walks the local filesystem via :func:`walk_paths`.

    2. **Sandbox binding** (new in Track 2): pass any object with
       ``sandbox_id`` / ``base_url`` / ``access_token`` attributes (the
       ``SandboxBinding`` dataclass or the ``SandboxBindingRequest``
       Pydantic model both qualify). Walks the remote sandbox's
       filesystem via :func:`walk_via_proxy`.

    Args:
        roots_or_binding: paths or a sandbox binding (see above).
        admin_user_id: User attributed as the owner of created system rows.
            In auto-discovery mode this is the sandbox owner; for the admin
            ingest endpoint it's the super-admin user. Either way every row
            ends up with a real owner per the ownership contract.
        dry_run: Parse and report without writing.
        is_system: When True (default — matches the admin ingest semantics),
            new rows land with ``is_system=true``. Auto-discovery can pass
            ``False`` if we ever want sandbox-discovered skills owned by
            the user as personal skills instead. Default stays True because
            today the user controls *what* lands in their repo's
            ``.claude/skills/`` directory; promoting those to system rows
            makes them visible to every agent the user runs.
        prune_scopes: Absolute path prefixes whose vanished mirrors should be
            DEACTIVATED (``is_active=False``) rather than left offered to
            agents forever. A row is a prune candidate ONLY when all three
            hold: it is ingest-owned, its ``config.source_path`` sits under one
            of these prefixes, and its skill_id was not seen on disk this run.
            Rows are never hard-deleted and never touched outside the scopes —
            the 2026-07-16 import swept ``~/.claude/plugins``, ``~/Downloads``
            and ``/private/tmp`` into this table, and an unscoped prune would
            mass-deactivate ~100 rows nobody asked about. Default ``None``
            prunes nothing (the sandbox auto-bind path must never prune).
        adopt: Take ownership of DB-native rows that collide with a repo skill
            by name. Off by default — see THE OWNERSHIP GUARD above.

    Returns:
        ``{'parsed': N, 'created': N, 'updated': N, 'unchanged': N,
            'skipped_foreign': N, 'deactivated': N, 'errors': [...],
            'skills': [...], 'roots': [...], 'collisions': [...],
            'prune_plan': [...]}``
    """
    collisions: list[str] = []
    if _looks_like_sandbox_binding(roots_or_binding):
        parsed, visited_root_strs = await walk_via_proxy(roots_or_binding)
        visited_roots_for_report: list[str] = list(visited_root_strs)
    else:
        if isinstance(roots_or_binding, (str, Path)):
            path_list: list[Path | str] = [roots_or_binding]
        else:
            path_list = list(roots_or_binding)
        # Discovery + SKILL.md parse are sync disk/CPU work — never on the
        # event loop (walking ~/code and hashing bodies stalled aidream-api
        # for ~1s). Offload the whole walk.
        parsed, visited_path_roots, collisions = await asyncio.to_thread(walk_paths, path_list)
        visited_roots_for_report = [str(r) for r in visited_path_roots]

    report: dict[str, Any] = {
        "parsed": len(parsed),
        "created": 0,
        "updated": 0,
        "unchanged": 0,
        "skipped_foreign": 0,
        "deactivated": 0,
        "errors": [],
        "skills": [
            {
                "skill_id": p.skill_id,
                "source_path": p.source_path,
                "category": p.category or "",
                "status": "pending",
            }
            for p in parsed
        ],
        "roots": visited_roots_for_report,
        "collisions": collisions,
        "prune_plan": [],
    }
    skills_by_id: dict[str, dict[str, str]] = {s["skill_id"]: s for s in report["skills"]}

    try:
        from matrx_ai.db._registry import get_instance

        cat_mgr = get_instance("skl_categories_manager")
        defs_mgr = get_instance("skl_definitions_manager")
    except Exception as exc:
        report["errors"].append(f"manager resolution failed: {exc!r}")
        return report

    # Resolve category slug -> id once for the whole batch. Skill categories
    # live in platform.categories (dimension="skill") since the 2026-06-28
    # canonical reorg; `slug` is the old `category_key`.
    categories = await cat_mgr.filter_items(dimension="skill")
    cat_by_key: dict[str, str] = {c.slug: str(c.id) for c in categories if getattr(c, "slug", None)}

    # ONE full read of the catalog. Used for BOTH the per-skill lookup and the
    # prune census, and — critically — it runs in dry-run too, so the plan the
    # operator reviews is the real plan (which rows are foreign, which would be
    # deactivated), not a parse count that implies every skill writes clean.
    all_rows = await defs_mgr.filter_items()
    rows_by_id: dict[str, list[Any]] = {}
    for row in all_rows:
        rows_by_id.setdefault(str(getattr(row, "skill_id", "")), []).append(row)

    admin_id = str(admin_user_id)
    parsed_ids = {p.skill_id for p in parsed}

    for p in parsed:
        try:
            # Duplicate skill_ids DO exist in this table (kind_seo_meta_options,
            # kind_keyword_relationship_research each have two rows), so prefer
            # the row this ingest already owns over whichever came back first.
            candidates = rows_by_id.get(p.skill_id, [])
            owned = [r for r in candidates if _is_ingest_owned(r)]
            row = owned[0] if owned else (candidates[0] if candidates else None)

            entry = skills_by_id[p.skill_id]

            if row is not None and not _is_ingest_owned(row) and not adopt:
                # A DB-native row wearing the same name. Report it loudly and
                # write nothing — see THE OWNERSHIP GUARD.
                report["skipped_foreign"] += 1
                entry["status"] = "skipped_foreign"
                entry["id"] = str(row.id)
                entry["reason"] = (
                    f"DB-native row (skill_type={getattr(row, 'skill_type', '?')}, "
                    f"visibility={getattr(row, 'visibility', '?')}) carries no "
                    f"config.ingested_from — not a repo mirror. Pass adopt=True to claim it."
                )
                vcprint(
                    f"[skills.ingest] SKIP FOREIGN {p.skill_id}: {entry['reason']}",
                    color="yellow",
                )
                continue

            category_id = cat_by_key.get(p.category) if p.category else None

            # A SKILL.md that declares no `skill_type` must not DOWNGRADE an
            # existing row to the 'reference' default: `create-agent` and
            # `build-matrx-workflow` are live `workflow` rows whose synced
            # SKILL.md carries only name + description. The default applies to
            # NEW rows; an existing row keeps the type an admin gave it.
            skill_type = p.skill_type
            if not p.declared_skill_type and row is not None:
                existing_type = getattr(row, "skill_type", None)
                if existing_type:
                    # The ORM hands back the `skl_skill_type` ENUM, whose
                    # `str()` is "SklSkillType.REFERENCE" — not a value the
                    # column accepts. Always round-trip through `.value`.
                    skill_type = str(getattr(existing_type, "value", existing_type))

            # Merge, never replace, `config`: other systems stamp keys here and
            # a wholesale replace silently drops them.
            merged_config = dict(_row_config(row)) if row is not None else {}
            merged_config.update(
                {
                    "source_hash": p.source_hash,
                    "source_path": p.source_path,
                    "source_repo": _source_repo(p.source_path),
                    "ingested_from": (
                        "sandbox" if p.source_path.startswith("sandbox://") else "filesystem"
                    ),
                    "ingested_at": _now_iso(),
                }
            )
            merged_config.pop("pruned_at", None)
            merged_config.pop("pruned_reason", None)

            # Canonical columns after the 2026 schema reorg: owner is
            # ``created_by`` (not user_id); product semver is ``semver``
            # (``version`` is the int row-counter).
            row_data: dict[str, Any] = {
                "label": p.label,
                "description": p.description,
                "skill_type": skill_type,
                "body": p.body,
                "allowed_tools": p.allowed_tools,
                "trigger_patterns": p.trigger_patterns,
                "disable_auto_invocation": p.disable_auto_invocation,
                "semver": p.version,
                "config": merged_config,
                "category_id": category_id,
                "is_system": is_system,
                # Filesystem-ingested skills are admin/dev tooling, never
                # the same catalog end users get — force `internal` on every
                # write (create AND update) so a row can't stay/become
                # publicly visible just because it happened to exist with
                # visibility='public' before this ingest run touched it.
                # Promoting a skill to user-facing is a deliberate, separate
                # admin action via the skill editor, not an ingest side effect.
                "visibility": "internal",
                "is_active": True,
                "created_by": admin_id,
            }
            # Drop None values that would violate FK constraints.
            row_data = {k: v for k, v in row_data.items() if v is not None}

            if row is not None:
                entry["id"] = str(row.id)
                existing_cfg = _row_config(row)
                # A reactivation is a real change even when the body matches —
                # a row pruned by an earlier run whose skill came back must not
                # sit "unchanged" and inactive.
                # ... and a row still missing the provenance stamp is NOT in
                # sync even when its body matches: `source_repo` / `ingested_at`
                # are how a later run knows which repo owns the mirror and when
                # it was last confirmed. Presence, never equality — so this
                # backfills once and then stays idempotent.
                if (
                    existing_cfg.get("source_hash") == p.source_hash
                    and getattr(row, "is_active", False)
                    and existing_cfg.get("source_path") == p.source_path
                    and existing_cfg.get("ingested_at")
                    and existing_cfg.get("source_repo")
                ):
                    report["unchanged"] += 1
                    entry["status"] = "unchanged"
                    continue
                # Count AFTER the write, never before: a run that reported
                # "updated: 89" while 89 writes raised is a lying status.
                if not dry_run:
                    await defs_mgr.update_item(str(row.id), **row_data)
                entry["status"] = "updated"
                report["updated"] += 1
            else:
                if not dry_run:
                    created = await defs_mgr.create_item(skill_id=p.skill_id, **row_data)
                    entry["id"] = str(getattr(created, "id", ""))
                entry["status"] = "created"
                report["created"] += 1

        except Exception as exc:
            skills_by_id[p.skill_id]["status"] = "error"
            report["errors"].append(f"{p.skill_id}: {exc!r}")
            vcprint(
                f"[skills.ingest] {p.skill_id}: {exc!r}",
                color="red",
            )

    # ---- Scoped prune: a repo skill that vanished (deleted or MERGED into
    # another skill) must stop being offered to agents. Deactivate, never
    # delete — the row keeps its body and its audit trail, and comes back on
    # the next run if the skill returns.
    if prune_scopes:
        norm_scopes = [str(Path(s).expanduser().resolve()) for s in prune_scopes]
        for row in all_rows:
            sid = str(getattr(row, "skill_id", ""))
            if sid in parsed_ids or not _is_ingest_owned(row):
                continue
            if not getattr(row, "is_active", False):
                continue
            sp = _row_config(row).get("source_path") or ""
            if not any(sp == s or sp.startswith(s + os.sep) for s in norm_scopes):
                continue
            plan_line = f"{sid} ← {sp}"
            report["prune_plan"].append(plan_line)
            report["deactivated"] += 1
            if not dry_run:
                try:
                    cfg = dict(_row_config(row))
                    cfg["pruned_at"] = _now_iso()
                    cfg["pruned_reason"] = "source file no longer present in the repo"
                    await defs_mgr.update_item(str(row.id), is_active=False, config=cfg)
                except Exception as exc:
                    report["deactivated"] -= 1
                    report["errors"].append(f"prune {sid}: {exc!r}")
                    vcprint(f"[skills.ingest] prune {sid}: {exc!r}", color="red")

    roots_str = ", ".join(report["roots"]) if report["roots"] else "(none)"
    vcprint(
        f"[skills.ingest] {'DRY RUN ' if dry_run else ''}roots=[{roots_str}]: "
        f"parsed={report['parsed']} created={report['created']} "
        f"updated={report['updated']} unchanged={report['unchanged']} "
        f"skipped_foreign={report['skipped_foreign']} "
        f"deactivated={report['deactivated']} errors={len(report['errors'])}",
        color="green",
    )
    return report
