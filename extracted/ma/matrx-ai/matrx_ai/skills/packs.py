"""Outside skill packs → ``skill.definition`` (deliberate, attributed imports).

An *outside skill pack* is a set of SKILL.md files an outside expert wrote in
their own field (the first is a PR/media pack by Elvis Sun and Carly
Martinetti, MIT). Arman, 2026-09-27: take their skills "and put them into our
skills library". This module is how, and it is the OPPOSITE of the 2026-07-16
bulk import that swept random SKILL.md files into the table:

* **Declared, not discovered.** A reviewed YAML manifest (``pack_manifests/<id>.yaml``)
  names the source repo, the exact commit, the license, the authors, the
  category, the renames and the extra documents. Nothing outside the pack's
  skills directory is read, and the clone's HEAD must match the manifest's
  commit or the run refuses.
* **Complete or loud.** Every file in the skills directory is either a skill
  folder, a declared document, or explicitly ignored — anything else is an
  error, so a new upstream file can never be silently dropped. Support files
  inside a skill folder (references, evidence, scripts) are appended to that
  skill's body verbatim, fenced, so nothing is lost.
* **Faithful.** The authors' text is kept verbatim. The only edits are
  mechanical: renamed skill ids (e.g. a trademarked product name) and the
  cross-references that point at them, so references resolve inside our
  library, and an honest banner on top.
* **Honest.** The banner says it is an imported outside skill with full
  provenance, and — when the body tells the agent to use tooling that does not
  exist on this platform (the pack's CLI, its local files, its authors'
  commercial API, harness cron jobs) — says loudly that those steps are the
  spec for a native rebuild and are not runnable here. Those instructions are
  never deleted.
* **Owned by the pack.** Rows carry ``config.ingested_from = "outside_pack"``
  and ``config.pack_id``. A pack run writes only its own rows; a repo-mirror
  ingest sees them as foreign, and vice versa.
* **Re-runnable.** Bodies are deterministic (no timestamps in the text), so a
  second run over the same commit reports every row ``unchanged``.
"""

from __future__ import annotations

import asyncio
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import UUID

from matrx_ai.skills.ingest import (
    ParsedSkill,
    _hash,
    _parse_content,
    _parse_frontmatter,
    _row_config,
    ensure_skill_category,
    upsert_parsed_skills,
)

PACK_MANIFESTS_DIR = Path(__file__).parent / "pack_manifests"
OUTSIDE_PACK_SOURCE = "outside_pack"

_FENCE_LANG = {
    ".md": "markdown",
    ".json": "json",
    ".mjs": "javascript",
    ".js": "javascript",
    ".ts": "typescript",
    ".py": "python",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".sh": "bash",
    ".txt": "text",
}


class PackError(ValueError):
    """The manifest or the source tree cannot be imported faithfully."""


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------


@dataclass
class ToolingNotice:
    label: str
    pattern: re.Pattern[str]


@dataclass
class PackDocument:
    """One extra document imported as a library entry.

    ``path`` is relative to the pack's skills directory; ``repo_path`` (used
    instead) is relative to the clone root, for documents that live elsewhere
    in the source repo (e.g. a docs site). Those must sit in a declared
    ``document_dirs`` entry so completeness is still enforced there.
    ``description`` may be omitted when the file's own frontmatter carries
    one. ``note`` adds one line to this document's banner.
    """

    path: str
    skill_id: str
    label: str
    description: str
    repo_path: str = ""
    note: str = ""

    @property
    def key(self) -> str:
        return self.repo_path or self.path


@dataclass
class DocumentDir:
    """A source-repo directory (outside the skills dir) holding declared documents.

    Every top-level entry in it must be a declared document or listed in
    ``skip`` with a reason — the same complete-or-loud rule as the skills dir.
    """

    dir: str
    skip: dict[str, str] = field(default_factory=dict)


@dataclass
class ToolEquivalent:
    """A tool the source text names, and what AI Matrx offers for it today.

    ``ours`` is None when nothing equivalent exists yet. The banner is built
    from this map, so when a new tool ships, the manifest line changes and a
    re-run rewrites every affected banner — never a hand-edited body.
    """

    name: str
    ours: str | None


@dataclass
class PackManifest:
    pack_id: str
    title: str
    repo_url: str
    commit: str
    license: str
    authors: list[str]
    skills_dir: str
    imported_on: str
    visibility: str
    category: dict[str, Any]
    renames: dict[str, dict[str, str]] = field(default_factory=dict)
    documents: list[PackDocument] = field(default_factory=list)
    path_rewrites: dict[str, str] = field(default_factory=dict)
    ignore_files: list[str] = field(default_factory=list)
    tooling_notices: list[ToolingNotice] = field(default_factory=list)
    tooling_note: str = ""
    skill_type: str = "reference"
    product_name: str = ""
    skip_skills: dict[str, str] = field(default_factory=dict)
    document_dirs: list[DocumentDir] = field(default_factory=list)
    tool_equivalents: list[ToolEquivalent] = field(default_factory=list)
    tool_equivalents_note: str = ""
    edits_note: str = ""
    # Where a DOCUMENT instructs the agent (vs. merely narrates). None = the whole
    # body counts, as for a skill. See ``instruction_text``.
    document_instruction_headings: re.Pattern[str] | None = None
    document_instruction_fences: bool = False

    def pack_paths(self) -> list[str]:
        """Every source path the import reads (checked clean at the pinned commit)."""
        paths = [self.skills_dir, *(d.dir for d in self.document_dirs)]
        paths += [d.repo_path for d in self.documents if d.repo_path]
        return list(dict.fromkeys(paths))


_VISIBILITIES = frozenset({"private", "internal", "public"})


def load_manifest(path: Path | str) -> PackManifest:
    """Read and validate one pack manifest. Raises :class:`PackError`."""
    import yaml  # type: ignore[import-not-found]

    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    try:
        source = raw["source"]
        manifest = PackManifest(
            pack_id=str(raw["pack_id"]),
            title=str(raw["title"]),
            repo_url=str(source["repo_url"]),
            commit=str(source["commit"]),
            license=str(source["license"]),
            authors=[str(a) for a in source["authors"]],
            skills_dir=str(source.get("skills_dir", "skills")),
            imported_on=str(raw["imported_on"]),
            visibility=str(raw.get("visibility", "internal")),
            category=dict(raw["category"]),
            renames={str(k): dict(v) for k, v in (raw.get("renames") or {}).items()},
            documents=[
                PackDocument(
                    path=str(d.get("path") or ""),
                    skill_id=str(d["skill_id"]),
                    label=str(d["label"]),
                    description=str(d.get("description") or "").strip(),
                    repo_path=str(d.get("repo_path") or ""),
                    note=str(d.get("note") or "").strip(),
                )
                for d in (raw.get("documents") or [])
            ],
            path_rewrites={str(k): str(v) for k, v in (raw.get("path_rewrites") or {}).items()},
            ignore_files=[str(f) for f in (raw.get("ignore_files") or [])],
            tooling_notices=[
                ToolingNotice(label=str(t["label"]), pattern=re.compile(str(t["pattern"])))
                for t in (raw.get("tooling_notices") or [])
            ],
            tooling_note=str(raw.get("tooling_note") or "").strip(),
            skill_type=str(raw.get("skill_type", "reference")),
            product_name=str(source.get("product_name") or ""),
            skip_skills={str(k): str(v).strip() for k, v in (raw.get("skip_skills") or {}).items()},
            document_dirs=[
                DocumentDir(
                    dir=str(d["dir"]).strip("/"),
                    skip={str(k): str(v).strip() for k, v in (d.get("skip") or {}).items()},
                )
                for d in (raw.get("document_dirs") or [])
            ],
            tool_equivalents=[
                ToolEquivalent(name=str(name), ours=(str(ours).strip() if ours else None))
                for name, ours in (raw.get("tool_equivalents") or {}).items()
            ],
            tool_equivalents_note=str(raw.get("tool_equivalents_note") or "").strip(),
            edits_note=str(raw.get("edits_note") or "").strip(),
            document_instruction_headings=(
                re.compile(str(scope["headings"]))
                if (scope := raw.get("document_instruction_scope") or {}).get("headings")
                else None
            ),
            document_instruction_fences=bool(
                (raw.get("document_instruction_scope") or {}).get("fenced_blocks")
            ),
        )
    except KeyError as exc:
        raise PackError(f"manifest {path} is missing required key {exc}") from exc
    if manifest.visibility not in _VISIBILITIES:
        raise PackError(
            f"manifest visibility {manifest.visibility!r} is not one of {sorted(_VISIBILITIES)}"
        )
    if not manifest.category.get("slug") or not manifest.category.get("name"):
        raise PackError("manifest category needs both slug and name")
    for old, spec in manifest.renames.items():
        # A rename may change only the displayed label; the id then stays.
        spec.setdefault("skill_id", old)
        if not spec.get("skill_id"):
            raise PackError(f"rename for {old!r} needs a skill_id")
    for doc in manifest.documents:
        if bool(doc.path) == bool(doc.repo_path):
            raise PackError(f"document {doc.skill_id!r} needs exactly one of path / repo_path")
        if doc.repo_path:
            parent = doc.repo_path.rsplit("/", 1)[0] if "/" in doc.repo_path else ""
            if parent not in {d.dir for d in manifest.document_dirs}:
                raise PackError(
                    f"document {doc.repo_path!r} is outside the skills dir but its folder is not a "
                    "declared document_dirs entry (completeness could not be checked there)"
                )
    overlap = set(manifest.skip_skills) & set(manifest.renames)
    if overlap:
        raise PackError(f"skills both skipped and renamed: {sorted(overlap)}")
    missing_reason = [k for k, v in manifest.skip_skills.items() if not v]
    if missing_reason:
        raise PackError(f"skip_skills entries need a reason: {missing_reason}")
    _check_product_name(
        manifest,
        [(spec["skill_id"], spec.get("label", "")) for spec in manifest.renames.values()]
        + [(d.skill_id, d.label) for d in manifest.documents],
    )
    return manifest


def _check_product_name(manifest: PackManifest, names: list[tuple[str, str]]) -> None:
    """The source's product name is never one of OUR library names (id or label)."""
    product = manifest.product_name.strip().lower()
    if not product:
        return
    squashed = re.sub(r"[^a-z0-9]", "", product)
    for skill_id, label in names:
        for value in (skill_id, label):
            if product in value.lower() or squashed in re.sub(r"[^a-z0-9]", "", value.lower()):
                raise PackError(
                    f"library name {value!r} contains the source product name {manifest.product_name!r}; "
                    "give it a plain label/id in the manifest (provenance still names the source)"
                )


# ---------------------------------------------------------------------------
# Source verification
# ---------------------------------------------------------------------------


def verify_source_commit(
    source_root: Path, commit: str, pack_paths: list[str] | None = None
) -> str:
    """Return the clone's HEAD sha; raise unless the pack is EXACTLY ``commit``.

    The manifest pins the exact upstream commit the import was reviewed
    against. Importing a different tree under that provenance would be a lie —
    and a matching HEAD is not enough: an edited, untracked or git-ignored file
    inside the pack paths would be stored under the experts' commit and names.
    So the pack paths must also be clean (no modified, staged, untracked or
    ignored entries).
    """

    def _git(*args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(source_root), *args],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        ).stdout

    try:
        head = _git("rev-parse", "HEAD").strip()
    except (OSError, subprocess.SubprocessError) as exc:
        raise PackError(f"{source_root} is not a git checkout: {exc}") from exc
    if not head.startswith(commit.lower()) and not commit.lower().startswith(head):
        raise PackError(
            f"{source_root} is at {head[:12]}, but the manifest pins {commit}. "
            f"Check out {commit} (or review the new commit and update the manifest)."
        )
    try:
        dirty = _git(
            "status",
            "--porcelain",
            "--untracked-files=all",
            "--ignored",
            "--",
            *(pack_paths or ["."]),
        ).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        raise PackError(f"could not read the working-tree state of {source_root}: {exc}") from exc
    if dirty:
        lines = dirty.splitlines()
        shown = "; ".join(lines[:10]) + (f"; … {len(lines) - 10} more" if len(lines) > 10 else "")
        raise PackError(
            f"{source_root} has local changes inside the pack ({shown}). The import would store "
            f"them under commit {commit} and the authors' names. Use a clean checkout of "
            f"{commit} (for example a fresh clone) and re-run."
        )
    return head


# ---------------------------------------------------------------------------
# Transformations
# ---------------------------------------------------------------------------


def _fence(content: str, lang: str) -> str:
    longest = max((len(m) for m in re.findall(r"`+", content)), default=0)
    ticks = "`" * max(3, longest + 1)
    return f"{ticks}{lang}\n{content.rstrip()}\n{ticks}"


def _id_map(manifest: PackManifest, folder_ids: list[str]) -> dict[str, str]:
    mapping = {fid: manifest.renames.get(fid, {}).get("skill_id", fid) for fid in folder_ids}
    for doc in manifest.documents:
        mapping[doc.key] = doc.skill_id
    return mapping


def rewrite_references(text: str, manifest: PackManifest, id_map: dict[str, str]) -> str:
    """Point in-body references at library skill ids. Mechanical, never judgment.

    * ``skills/<folder>/SKILL.md`` → the skill's library id.
    * manifest ``path_rewrites`` (e.g. ``skills/ETHICS.md`` → ``pr-ethics-doctrine``).
    * every renamed id as a whole token → its new id.
    """
    skills_dir = manifest.skills_dir.rstrip("/")

    def _skill_path(m: re.Match[str]) -> str:
        return id_map.get(m.group(1), m.group(0))

    text = re.sub(rf"{re.escape(skills_dir)}/([A-Za-z0-9_-]+)/SKILL\.md", _skill_path, text)
    for old, new in manifest.path_rewrites.items():
        text = text.replace(old, new)
    for old, spec in manifest.renames.items():
        text = re.sub(rf"(?<![\w-]){re.escape(old)}(?![\w-])", spec["skill_id"], text)
    return text


def _rewrite_h1(body: str, label: str) -> str:
    """Replace the first H1 (the skill's displayed name) with the library label."""
    return re.sub(r"^# .*$", f"# {label}", body, count=1, flags=re.MULTILINE)


def tool_mentions(
    text: str, manifest: PackManifest
) -> tuple[list[ToolEquivalent], list[ToolEquivalent]]:
    """Source tools this text names: (those with an AI Matrx equivalent, those without)."""
    named = [
        t
        for t in manifest.tool_equivalents
        if re.search(rf"(?<![\w-]){re.escape(t.name)}(?![\w-])", text)
    ]
    return [t for t in named if t.ours], [t for t in named if not t.ours]


def _split_doc_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """A document's own YAML frontmatter (title/description), and the rest verbatim."""
    if not text.startswith("---"):
        return {}, text
    fm, body = _parse_frontmatter(text)
    return (fm or {}), body


_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_FENCE_OPEN = re.compile(r"^(`{3,}|~{3,})")


def instruction_text(text: str, manifest: PackManifest) -> str:
    """The part of a DOCUMENT that tells the agent what to do.

    A skill body is instructions end to end, so it is scanned whole. A
    document (an article, a playbook) mostly narrates: it may mention the
    source product in passing without any step depending on it, and flagging
    it "not runnable" for that would overstate. When the manifest declares a
    ``document_instruction_scope``, only these parts count: sections whose
    heading matches ``headings`` (up to the next heading of the same or a
    higher level) and, with ``fenced_blocks``, fenced blocks (ready-to-run
    prompts). No scope declared → the whole document counts (the old rule).
    """
    heads = manifest.document_instruction_headings
    fences = manifest.document_instruction_fences
    if heads is None and not fences:
        return text
    kept: list[str] = []
    in_fence: str | None = None
    section_level: int | None = None  # level of the matching heading we are inside
    for line in text.splitlines():
        fence = _FENCE_OPEN.match(line)
        if in_fence is not None:
            if fence and line.startswith(in_fence):
                in_fence = None
                continue
            if fences or section_level is not None:
                kept.append(line)
            continue
        if fence:
            in_fence = fence.group(1)
            continue
        heading = _HEADING.match(line)
        if heading:
            level = len(heading.group(1))
            if section_level is not None and level <= section_level:
                section_level = None
            if (
                heads is not None
                and section_level is None
                and heads.search(heading.group(2).strip())
            ):
                section_level = level
                kept.append(line)
                continue
        if section_level is not None:
            kept.append(line)
    return "\n".join(kept)


def tooling_hits(text: str, manifest: PackManifest) -> list[tuple[str, int]]:
    return [
        (notice.label, len(notice.pattern.findall(text)))
        for notice in manifest.tooling_notices
        if notice.pattern.search(text)
    ]


def build_banner(
    manifest: PackManifest,
    *,
    source_rel_path: str,
    original_id: str,
    library_id: str,
    hits: list[tuple[str, int]],
    is_document: bool = False,
    tools: tuple[list[ToolEquivalent], list[ToolEquivalent]] = ([], []),
    frontmatter_lifted: bool = False,
    note: str = "",
) -> str:
    authors = (
        " and ".join(manifest.authors)
        if len(manifest.authors) <= 2
        else (", ".join(manifest.authors[:-1]) + f", and {manifest.authors[-1]}")
    )
    what = "outside document" if is_document else "outside skill"
    solo = len(manifest.authors) == 1
    whose = "author's" if solo else "authors'"
    lines = [
        f"> **Imported {what} — written by {'an outside expert' if solo else 'outside experts'}, not by AI Matrx.** "
        f"Part of *{manifest.title}* by {authors} "
        f"([source]({manifest.repo_url}), commit `{manifest.commit}`, file `{source_rel_path}`), "
        f"{manifest.license} License, imported {manifest.imported_on}.",
        ">",
        f"> The text below is the {whose} own, kept verbatim. The only edits are mechanical: "
        "skill names were changed to match this library"
        + (
            f" (this one was `{original_id}`, now `{library_id}`)"
            if original_id != library_id
            else ""
        )
        + ", and references to other skills in the set use their library names. "
        "Relative file references (for example `references/…` or `evidence.md`) point to the "
        "supporting files appended at the end of the named skill."
        + (
            " The source file's title and summary are shown as its heading and first line."
            if frontmatter_lifted
            else ""
        )
        + (f" {manifest.edits_note}" if manifest.edits_note else ""),
    ]
    if note:
        lines += [">", f"> {note}"]
    with_equiv, without = tools
    if with_equiv or without:
        lines += [
            ">",
            "> **The tools this text names are the source product's own.** "
            + manifest.tool_equivalents_note,
        ]
        if with_equiv:
            lines.append("> - **Has an AI Matrx equivalent today:**")
            lines += [f">   - `{t.name}` → {t.ours}" for t in with_equiv]
        if without:
            lines.append(
                "> - **No AI Matrx equivalent yet:** "
                + ", ".join(f"`{t.name}`" for t in without)
                + ". When a step needs one of these, say plainly that it is not available here yet."
            )
    if hits:
        scoped = is_document and (
            manifest.document_instruction_headings is not None
            or manifest.document_instruction_fences
        )
        who = "Its how-to-run steps and ready-made prompts tell" if scoped else "This text tells"
        found = "; ".join(f"{label} ({n} mention{'s' if n != 1 else ''})" for label, n in hits)
        lines += [
            ">",
            f"> **Warning — not yet runnable here.** {who} the agent to use: {found}. "
            + manifest.tooling_note,
        ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Walk
# ---------------------------------------------------------------------------


@dataclass
class PackWalk:
    skills: list[ParsedSkill]
    carried_support_files: list[str]
    errors: list[str]
    head: str


def _provenance(
    manifest: PackManifest, rel_path: str, original_id: str, head: str
) -> dict[str, Any]:
    return {
        "pack_id": manifest.pack_id,
        "source_repo": manifest.repo_url,
        "source_commit": manifest.commit,
        "source_commit_full": head,
        "source_path": rel_path,
        "source_license": manifest.license,
        "source_authors": list(manifest.authors),
        "original_skill_id": original_id,
        "imported_on": manifest.imported_on,
    }


def walk_pack(manifest: PackManifest, source_root: Path | str) -> PackWalk:
    """Build every ParsedSkill the pack declares. Pure: reads files, writes nothing."""
    root = Path(source_root).expanduser().resolve()
    head = verify_source_commit(root, manifest.commit, manifest.pack_paths())
    skills_root = root / manifest.skills_dir
    if not skills_root.is_dir():
        raise PackError(f"{skills_root} does not exist")

    errors: list[str] = []
    ignored = set(manifest.ignore_files)
    skipped = set(manifest.skip_skills)
    all_folders = sorted(
        child.name
        for child in skills_root.iterdir()
        if child.is_dir() and (child / "SKILL.md").exists()
    )
    # A skipped (or ignored) skill folder is accounted for but never imported.
    folder_ids = [f for f in all_folders if f not in skipped and f not in ignored]
    declared_docs = {d.path for d in manifest.documents if d.path}
    for name in sorted(skipped - set(all_folders)):
        errors.append(
            f"skip_skills names {name!r}, which is not a skill folder in {manifest.skills_dir}/"
        )

    # Completeness: every top-level entry is accounted for, or the run fails.
    for child in sorted(skills_root.iterdir()):
        if child.name in ignored or child.name in skipped:
            continue
        if child.is_dir() and (child / "SKILL.md").exists():
            continue
        if child.is_file() and child.name in declared_docs:
            continue
        errors.append(
            f"unaccounted entry {manifest.skills_dir}/{child.name}: not a skill folder, not a "
            "declared document, not ignored — declare it in the manifest"
        )
    for old in manifest.renames:
        if old not in folder_ids:
            errors.append(f"rename {old!r} names no skill folder in {manifest.skills_dir}/")
    for doc in manifest.documents:
        doc_file = (root / doc.repo_path) if doc.repo_path else (skills_root / doc.path)
        if not doc_file.is_file():
            errors.append(f"declared document {doc.key!r} is missing")
    # The same complete-or-loud rule in every declared document directory.
    for ddir in manifest.document_dirs:
        dir_path = root / ddir.dir
        if not dir_path.is_dir():
            errors.append(f"declared document_dir {ddir.dir!r} does not exist")
            continue
        declared_here = {
            d.repo_path.rsplit("/", 1)[-1]
            for d in manifest.documents
            if d.repo_path.startswith(ddir.dir + "/")
        }
        for name in sorted(set(ddir.skip) - {c.name for c in dir_path.iterdir()}):
            errors.append(f"document_dir {ddir.dir!r} skips {name!r}, which does not exist there")
        for name in sorted(set(ddir.skip) & declared_here):
            errors.append(f"{ddir.dir}/{name} is both declared and skipped")
        for child in sorted(dir_path.iterdir()):
            if child.name in ignored or child.name in ddir.skip or child.name in declared_here:
                continue
            errors.append(
                f"unaccounted entry {ddir.dir}/{child.name}: not a declared document, not skipped "
                "— declare it in the manifest"
            )

    id_map = _id_map(manifest, folder_ids)
    library_ids = list(id_map.values())
    if len(set(library_ids)) != len(library_ids):
        errors.append("two pack entries map to the same library skill id")

    skills: list[ParsedSkill] = []
    carried: list[str] = []
    category_slug = str(manifest.category["slug"])

    for folder_id in folder_ids:
        folder = skills_root / folder_id
        rel_path = f"{manifest.skills_dir}/{folder_id}/SKILL.md"
        content = (folder / "SKILL.md").read_text(encoding="utf-8")
        parsed = _parse_content(content, skill_id=folder_id, source_path=rel_path)
        if parsed is None:
            errors.append(f"{rel_path}: could not parse")
            continue
        fm, _ = _parse_frontmatter(content)
        library_id = id_map[folder_id]
        rename = manifest.renames.get(folder_id, {})

        body = rewrite_references(parsed.body, manifest, id_map)
        label = rename.get("label") or parsed.label
        if rename.get("label"):
            body = _rewrite_h1(body, label)

        # Support files beside SKILL.md — carried verbatim, fenced, in path order.
        support = sorted(
            p
            for p in folder.rglob("*")
            if p.is_file() and p.name != "SKILL.md" and p.name not in ignored
        )
        if support:
            parts = [
                "---",
                "",
                "## Imported supporting files",
                "",
                "These files sat beside this skill in its source folder. They are carried here "
                "verbatim so nothing from the original is lost.",
            ]
            for f in support:
                rel = f.relative_to(folder).as_posix()
                carried.append(f"{library_id}: {rel}")
                try:
                    text = f.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    errors.append(f"{folder_id}/{rel}: binary file cannot be carried as text")
                    continue
                if f.suffix.lower() == ".md":
                    # Prose references to sibling skills resolve like the body's;
                    # code and data files stay byte-for-byte.
                    text = rewrite_references(text, manifest, id_map)
                parts += [
                    "",
                    f"### `{rel}`",
                    "",
                    _fence(text, _FENCE_LANG.get(f.suffix.lower(), "text")),
                ]
            body = body.rstrip() + "\n\n" + "\n".join(parts)

        hits = tooling_hits(body, manifest)
        tools = tool_mentions(body, manifest)
        banner = build_banner(
            manifest,
            source_rel_path=rel_path,
            original_id=folder_id,
            library_id=library_id,
            hits=hits,
            tools=tools,
        )
        final_body = f"{banner}\n\n{body.strip()}\n"
        description = rewrite_references(parsed.description, manifest, id_map)
        when = fm.get("when_to_use")
        triggers = [rewrite_references(str(when).strip(), manifest, id_map)] if when else []

        skills.append(
            ParsedSkill(
                skill_id=library_id,
                label=label[:300],
                description=description[:2000],
                skill_type=manifest.skill_type,
                declared_skill_type=True,
                body=final_body,
                category=category_slug,
                allowed_tools=[],
                trigger_patterns=triggers,
                disable_auto_invocation=False,
                version=None,
                source_hash=_hash(final_body),
                source_path=rel_path,
                visibility=manifest.visibility,
                ingested_from=OUTSIDE_PACK_SOURCE,
                extra_config={
                    **_provenance(manifest, rel_path, folder_id, head),
                    "tooling_not_runnable": [label for label, _ in hits],
                    **_tool_config(tools),
                    "support_files": [f.relative_to(folder).as_posix() for f in support],
                },
            )
        )

    for doc in manifest.documents:
        path = (root / doc.repo_path) if doc.repo_path else (skills_root / doc.path)
        if not path.is_file():
            continue
        rel_path = doc.repo_path or f"{manifest.skills_dir}/{doc.path}"
        fm, raw_body = _split_doc_frontmatter(path.read_text(encoding="utf-8"))
        lifted = bool(fm.get("title") or fm.get("description"))
        if lifted:
            # Lift the file's own title/summary into the body so nothing is lost.
            head_lines = [f"# {fm['title']}"] if fm.get("title") else []
            if fm.get("description"):
                head_lines += ["", f"*{str(fm['description']).strip()}*"]
            raw_body = "\n".join(head_lines) + "\n\n" + raw_body.lstrip()
        body = rewrite_references(raw_body, manifest, id_map)
        description = doc.description or str(fm.get("description") or "").strip()
        if not description:
            errors.append(
                f"document {doc.key!r} has no description (none in the manifest or its frontmatter)"
            )
        hits = tooling_hits(instruction_text(body, manifest), manifest)
        tools = tool_mentions(body, manifest)
        banner = build_banner(
            manifest,
            source_rel_path=rel_path,
            original_id=doc.key,
            library_id=doc.skill_id,
            hits=hits,
            is_document=True,
            tools=tools,
            frontmatter_lifted=lifted,
            note=doc.note,
        )
        final_body = f"{banner}\n\n{body.strip()}\n"
        skills.append(
            ParsedSkill(
                skill_id=doc.skill_id,
                label=doc.label,
                description=description[:2000],
                skill_type=manifest.skill_type,
                declared_skill_type=True,
                body=final_body,
                category=category_slug,
                allowed_tools=[],
                trigger_patterns=[],
                disable_auto_invocation=False,
                version=None,
                source_hash=_hash(final_body),
                source_path=rel_path,
                visibility=manifest.visibility,
                ingested_from=OUTSIDE_PACK_SOURCE,
                extra_config={
                    **_provenance(manifest, rel_path, doc.key, head),
                    "tooling_not_runnable": [label for label, _ in hits],
                    **_tool_config(tools),
                    "support_files": [],
                },
            )
        )

    try:
        _check_product_name(manifest, [(s.skill_id, s.label) for s in skills])
    except PackError as exc:
        errors.append(str(exc))
    return PackWalk(skills=skills, carried_support_files=carried, errors=errors, head=head)


def _tool_config(tools: tuple[list[ToolEquivalent], list[ToolEquivalent]]) -> dict[str, Any]:
    with_equiv, without = tools
    if not (with_equiv or without):
        return {}
    return {
        "source_tools_with_equivalent": {t.name: t.ours for t in with_equiv},
        "source_tools_without_equivalent": [t.name for t in without],
    }


# ---------------------------------------------------------------------------
# Ingest
# ---------------------------------------------------------------------------


def pack_owns(pack_id: str):
    """Ownership predicate: a row belongs to THIS pack and nothing else."""

    def _owns(row: Any) -> bool:
        cfg = _row_config(row)
        return cfg.get("ingested_from") == OUTSIDE_PACK_SOURCE and cfg.get("pack_id") == pack_id

    return _owns


async def _ensure_category(
    manifest: PackManifest, *, admin_user_id: str, dry_run: bool
) -> dict[str, Any]:
    """Make sure the pack's skill category exists (see :func:`ensure_skill_category`)."""
    return await ensure_skill_category(
        manifest.category,
        visibility=manifest.visibility,
        extra_metadata={"pack_id": manifest.pack_id, "source_repo": manifest.repo_url},
        admin_user_id=admin_user_id,
        dry_run=dry_run,
    )


async def ingest_outside_pack(
    manifest_path: Path | str,
    source_root: Path | str,
    *,
    admin_user_id: UUID | str,
    dry_run: bool = False,
    prune: bool = False,
) -> dict[str, Any]:
    """Import (or re-sync) one outside pack. Idempotent; writes only its own rows.

    Refuses to write anything when the walk found an error (unaccounted file,
    wrong commit, missing document) — a partial import would be a silent drop.
    ``prune`` deactivates (never deletes) this pack's rows whose skill left
    the pack.
    """

    def _read() -> tuple[PackManifest, PackWalk, str]:
        m = load_manifest(Path(manifest_path).expanduser().resolve())
        root = Path(source_root).expanduser().resolve()
        return m, walk_pack(m, root), str(root / m.skills_dir)

    # Manifest + tree read, git HEAD check and hashing are sync disk work —
    # never on the event loop (same rule as ingest_filesystem's walk).
    manifest, walk, skills_root = await asyncio.to_thread(_read)
    if walk.errors:
        return {
            "pack_id": manifest.pack_id,
            "parsed": len(walk.skills),
            "created": 0,
            "updated": 0,
            "unchanged": 0,
            "skipped_foreign": 0,
            "deactivated": 0,
            "errors": walk.errors,
            "skills": [],
            "roots": [str(source_root)],
            "collisions": [],
            "prune_plan": [],
            "category": None,
            "carried_support_files": walk.carried_support_files,
        }
    category = await _ensure_category(manifest, admin_user_id=str(admin_user_id), dry_run=dry_run)
    owns = pack_owns(manifest.pack_id)
    report = await upsert_parsed_skills(
        walk.skills,
        admin_user_id=admin_user_id,
        dry_run=dry_run,
        is_system=True,
        adopt=False,
        owns=owns,
        prune_candidate=(lambda _row: True) if prune else None,
        roots=[skills_root],
    )
    report["pack_id"] = manifest.pack_id
    report["category"] = category
    report["carried_support_files"] = walk.carried_support_files
    report["source_head"] = walk.head
    return report
