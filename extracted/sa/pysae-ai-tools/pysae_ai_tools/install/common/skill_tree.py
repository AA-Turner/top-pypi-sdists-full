"""Shared per-skill materialization for the per-assistant deployments.

Both the Claude plugin deployment and the Codex deployment take the bundled skills under
``pysae_ai_tools/claude_plugin/skills`` and materialize each skill that targets their
assistant into that assistant's own location — always a copy with a per-assistant transform
of ``SKILL.md`` (never a symlink), so the deployed artefact is identical in dev, CI and prod.

This module holds what they share: the skill selection (``assistants:`` frontmatter filter),
the per-assistant materializer (transformed ``SKILL.md``, per-assistant reference/companion
``.md`` files, verbatim non-Markdown companions, merged ``_<assistant>/`` sub-directory), the
shared companion trees deployed alongside the skills (e.g. ``references/``, linked via
``../references/…``), and a content fingerprint of the materialized set so a deploy re-runs
exactly when the source that reaches an assistant changed.
"""

import hashlib
import shutil
from collections.abc import Iterator
from pathlib import Path

from ...common.skills import read_assistants
from .skill_convert import converting_assistants, get_skill_converter

_SKILL_MD = "SKILL.md"


def clear_path(dst: Path) -> None:
    """Remove ``dst`` whether it is a file, directory, or symlink."""
    if dst.is_symlink() or dst.is_file():
        try:
            dst.unlink()
        except OSError:
            pass
    elif dst.is_dir():
        shutil.rmtree(dst, ignore_errors=True)


def skill_targets(skill_dir: Path, assistant: str) -> bool:
    """True when the skill at ``skill_dir`` should deploy to ``assistant``: its
    ``assistants:`` list includes it, or the field is absent (unrestricted)."""
    skill_md = skill_dir / _SKILL_MD
    if not skill_md.is_file():
        return False
    assistants = read_assistants(skill_md.read_text(encoding="utf-8", errors="replace"))
    return assistants is None or assistant in assistants


def iter_skill_dirs(skills_root: Path) -> list[Path]:
    """Every immediate sub-directory of ``skills_root`` that holds a ``SKILL.md``."""
    if not skills_root.is_dir():
        return []
    return sorted(p for p in skills_root.iterdir() if p.is_dir() and (p / _SKILL_MD).is_file())


def selected_skills(skills_root: Path, assistant: str) -> list[Path]:
    """The skill directories under ``skills_root`` that target ``assistant``."""
    return [d for d in iter_skill_dirs(skills_root) if skill_targets(d, assistant)]


def iter_shared_dirs(skills_root: Path) -> list[Path]:
    """Every immediate sub-directory of ``skills_root`` that is *not* a skill (no ``SKILL.md``):
    the shared companion trees — e.g. ``references/`` — that skills link to via ``../references/…``.
    Not gated by ``assistants:`` (they carry no frontmatter), so they deploy for every assistant,
    materialized alongside the skills."""
    if not skills_root.is_dir():
        return []
    return sorted(p for p in skills_root.iterdir() if p.is_dir() and not (p / _SKILL_MD).is_file())


def _assistant_subdirs() -> set[str]:
    """The reserved per-assistant sub-directory names (``_claude``, ``_codex``, …)."""
    return {f"_{name}" for name in converting_assistants()}


def _materialized_sources(skill_dir: Path, assistant: str) -> Iterator[tuple[Path, Path]]:
    """Yield ``(rel_dest, src_file)`` for every source file of ``skill_dir`` that deploys to
    ``assistant``: the ``SKILL.md``, the verbatim companions/subtrees, and the contents of the
    skill's own ``_<assistant>/`` (merged into the deployed root, its prefix dropped). Files
    under another assistant's ``_<other>/`` are skipped.
    """
    reserved = _assistant_subdirs()
    own = f"_{assistant}"
    for src in sorted(p for p in skill_dir.rglob("*") if p.is_file()):
        rel = src.relative_to(skill_dir)
        top = rel.parts[0]
        if top in reserved:
            if top != own:
                continue
            rel = Path(*rel.parts[1:])  # merge _<assistant>/x → x
        yield rel, src


def _materialize_tree(src_dir: Path, dst: Path, assistant: str, skill_names: frozenset[str]) -> None:
    """Copy ``src_dir`` → ``dst`` for ``assistant``: ``SKILL.md`` runs through the assistant's
    full converter (frontmatter + body), every other ``.md`` (reference/companion) through its
    frontmatter-free reference converter so inline ``<!-- assistant:… -->`` blocks resolve there
    too, and any non-Markdown file is copied verbatim. ``skill_names`` is the full deployed set,
    used to rewrite cross-skill references to the assistant's invocation syntax."""
    converter = get_skill_converter(assistant)
    clear_path(dst)
    dst.mkdir(parents=True, exist_ok=True)
    for rel, src in _materialized_sources(src_dir, assistant):
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if rel == Path(_SKILL_MD):
            target.write_text(converter.convert(src.read_text(encoding="utf-8"), skill_names), encoding="utf-8")
        elif src.suffix == ".md":
            target.write_text(
                converter.convert_reference(src.read_text(encoding="utf-8"), skill_names), encoding="utf-8"
            )
        else:
            shutil.copy2(src, target)


def materialize_skills(skills_root: Path, dest_root: Path, *, assistant: str) -> int:
    """Materialize into ``dest_root`` every skill under ``skills_root`` that targets
    ``assistant`` (``dest_root/<skill>/``) plus the shared companion trees (``dest_root/<name>/``,
    e.g. ``references/``) that skills link to. Returns the number of *skills* materialized.

    Only the managed trees are (re)written — ``dest_root`` itself is never wiped, so a shared
    location such as Codex's ``~/.agents/skills`` keeps the user's own skills. Each managed
    tree is cleared before it is re-materialized (idempotent).
    """
    dest_root.mkdir(parents=True, exist_ok=True)
    skills = selected_skills(skills_root, assistant)
    skill_names = frozenset(skill_dir.name for skill_dir in skills)
    count = 0
    for skill_dir in skills:
        _materialize_tree(skill_dir, dest_root / skill_dir.name, assistant, skill_names)
        count += 1
    for shared_dir in iter_shared_dirs(skills_root):
        _materialize_tree(shared_dir, dest_root / shared_dir.name, assistant, skill_names)
    return count


def skills_fingerprint(skills_root: Path, assistant: str) -> str:
    """A SHA-256 digest of everything that materializes for ``assistant``: the relative
    destination path and raw bytes of each source file, over every selected skill and shared
    companion tree.

    A deploy stores this and re-runs when it changes — which happens on any add, removal or
    rename of a skill or shared file, and on any edit to a file that reaches ``assistant`` (the ``SKILL.md``
    is hashed as source, so an edit inside another assistant's inline block conservatively
    still triggers a redeploy; that is harmless — materialization is idempotent).
    """
    digest = hashlib.sha256()
    for tree in (*selected_skills(skills_root, assistant), *iter_shared_dirs(skills_root)):
        for rel, src in _materialized_sources(tree, assistant):
            digest.update(f"{tree.name}/{rel.as_posix()}\0".encode())
            digest.update(src.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()
