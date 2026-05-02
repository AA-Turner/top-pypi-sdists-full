"""Searchable skill-package discovery and canonical catalog projections."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
import os
from pathlib import Path
import re
from typing import Any

from packages.runtime_layout import (
    default_authored_skills_dir,
    default_builtin_skills_dir,
    default_installed_skills_dir,
)

from .runtime import SkillDefinition, SkillDependency, SkillScope, load_skill_package_definition


@dataclass(frozen=True, slots=True)
class SkillCatalogVisibility:
    include_in_hub: bool = True
    include_in_prompt_index: bool = True
    include_in_site: bool = True
    include_in_overlay: bool = False


@dataclass(frozen=True, slots=True)
class SkillHubEntry:
    skill_id: str
    display_name: str
    summary: str
    source_id: str
    source_label: str
    skill_path: str
    entry_path: str
    provenance: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def reference(self) -> str:
        return f"{self.source_id}:{self.skill_id}"


@dataclass(frozen=True, slots=True)
class SkillHubSource:
    source_id: str
    label: str
    root: Path


@dataclass(frozen=True, slots=True)
class SkillCatalogEntry:
    skill_id: str
    display_name: str
    summary: str
    version: str
    source_id: str
    source_label: str
    source_kind: str
    storage_tier: str
    default_enabled: bool
    skill_path: str
    entry_path: str
    provenance: str
    instruction_text: str = ""
    scope: SkillScope = field(default_factory=SkillScope)
    dependencies: tuple[SkillDependency, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
    visibility: SkillCatalogVisibility = field(default_factory=SkillCatalogVisibility)

    @property
    def reference(self) -> str:
        return f"{self.source_id}:{self.skill_id}"

    def to_skill_definition(self, *, enabled_override: bool | None = None) -> SkillDefinition:
        enabled = self.default_enabled if enabled_override is None else bool(enabled_override)
        metadata = dict(self.metadata)
        metadata.setdefault("source_kind", self.source_kind)
        metadata.setdefault("source_id", self.source_id)
        metadata.setdefault("source_label", self.source_label)
        metadata.setdefault("hub_reference", self.reference)
        metadata.setdefault("storage_tier", self.storage_tier)
        metadata.setdefault("default_enabled", self.default_enabled)
        metadata.setdefault("include_in_hub", self.visibility.include_in_hub)
        metadata.setdefault("include_in_prompt_index", self.visibility.include_in_prompt_index)
        metadata.setdefault("include_in_site", self.visibility.include_in_site)
        metadata.setdefault("include_in_overlay", self.visibility.include_in_overlay)
        return SkillDefinition(
            skill_id=self.skill_id,
            display_name=self.display_name,
            version=self.version,
            summary=self.summary,
            scope=self.scope,
            dependencies=self.dependencies,
            provenance=self.provenance,
            enabled=enabled,
            instruction_text=self.instruction_text,
            entry_path=self.entry_path,
            metadata=metadata,
        )

    def to_hub_entry(self) -> SkillHubEntry:
        metadata = dict(self.metadata)
        metadata.setdefault("source_kind", self.source_kind)
        metadata.setdefault("storage_tier", self.storage_tier)
        metadata.setdefault("default_enabled", self.default_enabled)
        metadata.setdefault("include_in_hub", self.visibility.include_in_hub)
        metadata.setdefault("include_in_prompt_index", self.visibility.include_in_prompt_index)
        metadata.setdefault("include_in_site", self.visibility.include_in_site)
        metadata.setdefault("include_in_overlay", self.visibility.include_in_overlay)
        return SkillHubEntry(
            skill_id=self.skill_id,
            display_name=self.display_name,
            summary=self.summary,
            source_id=self.source_id,
            source_label=self.source_label,
            skill_path=self.skill_path,
            entry_path=self.entry_path,
            provenance=self.provenance,
            metadata=metadata,
        )


class SkillHub:
    """Search local skill shelves and resolve installable skill packages."""

    def __init__(self, sources: tuple[SkillHubSource, ...] | None = None) -> None:
        self._sources = sources or default_skill_hub_sources()

    @property
    def sources(self) -> tuple[SkillHubSource, ...]:
        return self._sources

    def list(self, enabled_overrides: Mapping[str, bool] | None = None) -> tuple[SkillHubEntry, ...]:
        entries: list[SkillHubEntry] = []
        overrides = dict(enabled_overrides or {})
        for source in self._sources:
            if not source.root.exists():
                continue
            if source.source_id == "builtin":
                from .builtins import builtin_skill_hub_entries

                entries.extend(builtin_skill_hub_entries(overrides, root=source.root))
                continue
            for skill_md in source.root.rglob("SKILL.md"):
                if ".git" in skill_md.parts:
                    continue
                if "__pycache__" in skill_md.parts:
                    continue
                try:
                    catalog_entry = load_skill_catalog_entry(skill_md, source=source)
                except Exception:
                    continue
                if catalog_entry.skill_id in overrides:
                    catalog_entry = _replace_default_enabled(catalog_entry, overrides[catalog_entry.skill_id])
                if not catalog_entry.visibility.include_in_hub or not catalog_entry.default_enabled:
                    continue
                entries.append(catalog_entry.to_hub_entry())
        entries.sort(key=lambda item: _hub_sort_key(item))
        return tuple(entries)

    def search(
        self,
        query: str,
        *,
        limit: int = 12,
        enabled_overrides: Mapping[str, bool] | None = None,
    ) -> tuple[SkillHubEntry, ...]:
        tokens = tuple(token for token in _normalize_query(query).split() if token)
        if not tokens:
            return self.list(enabled_overrides)[:limit]
        scored: list[tuple[int, str, SkillHubEntry]] = []
        for entry in self.list(enabled_overrides):
            metadata_terms = " ".join(_metadata_search_terms(entry.metadata))
            haystack = " ".join(
                (
                    entry.skill_id,
                    entry.reference,
                    entry.display_name,
                    entry.summary,
                    metadata_terms,
                )
            ).lower()
            if not all(token in haystack for token in tokens):
                continue
            score = 0
            normalized_tokens = " ".join(tokens)
            if _normalize_query(entry.skill_id) == normalized_tokens:
                score += 6
            if _normalize_query(entry.display_name) == normalized_tokens:
                score += 5
            if all(token in _normalize_query(entry.display_name) for token in tokens):
                score += 3
            if all(token in _normalize_query(entry.summary) for token in tokens):
                score += 1
            if all(token in _normalize_query(metadata_terms) for token in tokens):
                score += 1
            scored.append((score, entry.reference, entry))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return tuple(item[2] for item in scored[:limit])

    def resolve(self, reference: str) -> SkillHubEntry | None:
        candidate = reference.strip()
        if not candidate:
            return None
        path_candidate = Path(candidate).expanduser()
        if path_candidate.exists():
            catalog_entry = load_skill_catalog_entry(
                path_candidate,
                source=SkillHubSource(
                    source_id="path",
                    label="Path",
                    root=path_candidate.resolve().parent if path_candidate.is_file() else path_candidate.resolve(),
                ),
            )
            return catalog_entry.to_hub_entry()
        lowered = candidate.lower()
        for entry in self.list():
            if lowered in {
                entry.reference.lower(),
                entry.skill_id.lower(),
                entry.display_name.lower(),
            }:
                return entry
        return None


def default_skill_hub_sources() -> tuple[SkillHubSource, ...]:
    configured = os.environ.get("AEGIS_SKILL_PATHS", "").strip()
    if configured:
        sources: list[SkillHubSource] = []
        for index, raw_path in enumerate(configured.split(os.pathsep)):
            path = Path(raw_path).expanduser()
            if not raw_path.strip():
                continue
            sources.append(
                SkillHubSource(
                    source_id=f"custom-{index + 1}",
                    label=path.name or f"custom-{index + 1}",
                    root=path,
                )
            )
        return _prepend_builtin_source(_append_aegis_skill_sources(tuple(sources)))

    home = Path.home()
    candidates = (
        SkillHubSource("builtin", "Built In", builtin_aegis_skill_source_root()),
        SkillHubSource("aegis-installed", "Aegis Installed", default_aegis_skill_source_root()),
        SkillHubSource("aegis-authored", "Aegis Authored", default_authored_aegis_skill_source_root()),
        SkillHubSource("codex", "Codex", home / ".codex" / "skills"),
        SkillHubSource("agents", "Agents", home / ".agents" / "skills"),
        SkillHubSource("orchestra", "Orchestra", home / ".orchestra" / "skills"),
        SkillHubSource("skills", "Skills", home / "skills"),
        SkillHubSource("local-workbench", "Local Workbench", home / "local-workbench" / "skills"),
    )
    return tuple(source for source in candidates if source.root.exists())


def aegis_operator_skill_sources(*, install_root: Path | None = None) -> tuple[SkillHubSource, ...]:
    sources = [
        SkillHubSource("builtin", "Built In", builtin_aegis_skill_source_root()),
        SkillHubSource("aegis-installed", "Aegis Installed", default_installed_aegis_skill_source_root() if install_root is None else default_installed_skills_dir(install_root=install_root)),
        SkillHubSource("aegis-authored", "Aegis Authored", default_authored_aegis_skill_source_root() if install_root is None else default_authored_skills_dir(install_root=install_root)),
    ]
    return tuple(source for source in sources if source.root.exists())


def operator_skill_catalog_entries(
    *,
    install_root: Path | None = None,
) -> tuple[SkillCatalogEntry, ...]:
    entries: list[SkillCatalogEntry] = []
    for source in aegis_operator_skill_sources(install_root=install_root):
        if source.source_id == "builtin":
            entries.extend(builtin_skill_catalog_entries(root=source.root))
            continue
        for skill_md in source.root.rglob("SKILL.md"):
            if ".git" in skill_md.parts or "__pycache__" in skill_md.parts:
                continue
            entries.append(load_skill_catalog_entry(skill_md, source=source))
    entries.sort(key=_catalog_sort_key)
    return tuple(entries)


def default_aegis_skill_source_root() -> Path:
    return default_installed_aegis_skill_source_root()


def default_installed_aegis_skill_source_root() -> Path:
    return default_installed_skills_dir()


def default_authored_aegis_skill_source_root() -> Path:
    return default_authored_skills_dir()


def builtin_aegis_skill_source_root() -> Path:
    materialized = default_builtin_skills_dir()
    if materialized.exists():
        return materialized
    return repo_builtin_aegis_skill_source_root()


def repo_builtin_aegis_skill_source_root() -> Path:
    return Path(__file__).resolve().parent / "builtin_packages"


def builtin_skill_catalog_entries(
    enabled_overrides: Mapping[str, bool] | None = None,
    *,
    root: Path | None = None,
) -> tuple[SkillCatalogEntry, ...]:
    source_root = (root or builtin_aegis_skill_source_root()).expanduser().resolve()
    if not source_root.exists():
        return ()
    source = SkillHubSource("builtin", "Built In", source_root)
    entries: list[SkillCatalogEntry] = []
    overrides = dict(enabled_overrides or {})
    for skill_md in source_root.rglob("SKILL.md"):
        if ".git" in skill_md.parts or "__pycache__" in skill_md.parts:
            continue
        catalog_entry = load_skill_catalog_entry(skill_md, source=source)
        if catalog_entry.skill_id in overrides:
            catalog_entry = _replace_default_enabled(catalog_entry, overrides[catalog_entry.skill_id])
        entries.append(catalog_entry)
    entries.sort(key=_catalog_sort_key)
    return tuple(entries)


def load_skill_catalog_entry(path: Path, *, source: SkillHubSource) -> SkillCatalogEntry:
    definition = load_skill_package_definition(path)
    return catalog_entry_from_definition(definition, source=source)


def source_for_skill_path(path: Path) -> SkillHubSource:
    resolved = path.expanduser().resolve()
    package_root = resolved.parent if resolved.is_file() else resolved
    builtin_root = builtin_aegis_skill_source_root().expanduser().resolve()
    installed_root = default_installed_aegis_skill_source_root().expanduser().resolve()
    authored_root = default_authored_aegis_skill_source_root().expanduser().resolve()
    for source in (
        SkillHubSource("builtin", "Built In", builtin_root),
        SkillHubSource("aegis-installed", "Aegis Installed", installed_root),
        SkillHubSource("aegis-authored", "Aegis Authored", authored_root),
    ):
        try:
            package_root.relative_to(source.root)
        except ValueError:
            continue
        return source
    return SkillHubSource(
        "path",
        "Path",
        package_root if package_root.is_dir() else package_root.parent,
    )


def catalog_entry_from_definition(definition: SkillDefinition, *, source: SkillHubSource) -> SkillCatalogEntry:
    entry_path = Path(definition.entry_path or definition.provenance or "").expanduser().resolve()
    skill_path = entry_path.parent if entry_path.name == "SKILL.md" else entry_path
    metadata = dict(definition.metadata)
    source_kind = str(metadata.get("source_kind") or "skill-package").strip() or "skill-package"
    metadata.setdefault("source_kind", source_kind)
    try:
        relative_parts = skill_path.relative_to(source.root.expanduser().resolve()).parts
    except ValueError:
        relative_parts = ()
    category = "/".join(relative_parts[:-1]).strip("/") if len(relative_parts) > 1 else ""
    if category:
        metadata.setdefault("category", category)
    metadata.setdefault("slash_command", _skill_command_slug(definition.skill_id or definition.display_name))
    storage_tier = _storage_tier_for_source(source.source_id)
    metadata.setdefault("storage_tier", storage_tier)
    is_builtin = source.source_id == "builtin" or source_kind == "aegis-builtin"
    default_enabled = _metadata_bool(
        metadata.get("default_enabled"),
        default=True if is_builtin else definition.enabled,
    )
    metadata.setdefault("default_enabled", default_enabled)
    visibility = SkillCatalogVisibility(
        include_in_hub=_metadata_bool(metadata.get("include_in_hub"), default=True),
        include_in_prompt_index=_metadata_bool(metadata.get("include_in_prompt_index"), default=is_builtin),
        include_in_site=_metadata_bool(metadata.get("include_in_site"), default=is_builtin),
        include_in_overlay=_metadata_bool(metadata.get("include_in_overlay"), default=not is_builtin),
    )
    return SkillCatalogEntry(
        skill_id=definition.skill_id,
        display_name=definition.display_name,
        summary=definition.summary,
        version=definition.version,
        source_id=source.source_id,
        source_label=source.label,
        source_kind=source_kind,
        storage_tier=storage_tier,
        default_enabled=default_enabled,
        skill_path=str(skill_path),
        entry_path=str(entry_path),
        provenance=definition.provenance,
        instruction_text=definition.instruction_text,
        scope=definition.scope,
        dependencies=definition.dependencies,
        metadata=metadata,
        visibility=visibility,
    )


def _append_aegis_skill_sources(sources: tuple[SkillHubSource, ...]) -> tuple[SkillHubSource, ...]:
    resolved = list(sources)
    existing_roots = {source.root.expanduser().resolve() for source in sources}
    aegis_sources = (
        SkillHubSource("aegis-installed", "Aegis Installed", default_installed_aegis_skill_source_root()),
        SkillHubSource("aegis-authored", "Aegis Authored", default_authored_aegis_skill_source_root()),
    )
    for source in aegis_sources:
        root = source.root.expanduser().resolve()
        if root in existing_roots:
            continue
        resolved.append(source)
        existing_roots.add(root)
    return tuple(source for source in resolved if source.root.exists())


def _prepend_builtin_source(sources: tuple[SkillHubSource, ...]) -> tuple[SkillHubSource, ...]:
    builtin_root = builtin_aegis_skill_source_root()
    resolved = [source for source in sources if source.root.exists()]
    if not builtin_root.exists():
        return tuple(resolved)
    builtin_resolved = builtin_root.expanduser().resolve()
    existing_roots = {source.root.expanduser().resolve() for source in resolved}
    if builtin_resolved not in existing_roots:
        resolved.insert(0, SkillHubSource("builtin", "Built In", builtin_root))
    return tuple(resolved)


def _catalog_sort_key(entry: SkillCatalogEntry) -> tuple[int, int, str, str]:
    default_rank = 0 if entry.default_enabled else 1
    return (
        _hub_source_rank(entry.source_id),
        default_rank,
        entry.display_name.lower(),
        entry.skill_id,
    )


def _hub_sort_key(entry: SkillHubEntry) -> tuple[int, int, str, str]:
    default_enabled = bool(entry.metadata.get("default_enabled"))
    return (
        _hub_source_rank(entry.source_id),
        0 if default_enabled else 1,
        entry.display_name.lower(),
        entry.skill_id,
    )


def _replace_default_enabled(entry: SkillCatalogEntry, enabled: bool) -> SkillCatalogEntry:
    return SkillCatalogEntry(
        skill_id=entry.skill_id,
        display_name=entry.display_name,
        summary=entry.summary,
        version=entry.version,
        source_id=entry.source_id,
        source_label=entry.source_label,
        source_kind=entry.source_kind,
        storage_tier=entry.storage_tier,
        default_enabled=bool(enabled),
        skill_path=entry.skill_path,
        entry_path=entry.entry_path,
        provenance=entry.provenance,
        instruction_text=entry.instruction_text,
        scope=entry.scope,
        dependencies=entry.dependencies,
        metadata=entry.metadata,
        visibility=entry.visibility,
    )


def _metadata_search_terms(metadata: Mapping[str, Any]) -> tuple[str, ...]:
    terms: list[str] = []
    for key in ("category", "source_kind", "storage_tier"):
        value = str(metadata.get(key) or "").strip()
        if value:
            terms.append(value)
    for key in ("aliases", "trigger_phrases", "keywords", "platforms"):
        raw = metadata.get(key)
        if isinstance(raw, (tuple, list, set)):
            terms.extend(str(item).strip() for item in raw if str(item).strip())
    return tuple(terms)


def _normalize_query(value: str) -> str:
    return " ".join(value.lower().replace("-", " ").replace("_", " ").split())


def _skill_command_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9-]+", "-", value.lower().replace("_", "-").replace(" ", "-"))
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug


def _storage_tier_for_source(source_id: str) -> str:
    if source_id == "builtin":
        return "builtin"
    if source_id == "aegis-installed":
        return "installed"
    if source_id == "aegis-authored":
        return "authored"
    return "external"


def _hub_source_rank(source_id: str) -> int:
    order = {
        "builtin": 0,
        "aegis-installed": 1,
        "aegis-authored": 2,
        "path": 3,
    }
    return order.get(source_id, 8)


def _metadata_bool(value: Any, *, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    text = str(value).strip().lower()
    if text in {"true", "yes", "1", "on"}:
        return True
    if text in {"false", "no", "0", "off"}:
        return False
    return default
