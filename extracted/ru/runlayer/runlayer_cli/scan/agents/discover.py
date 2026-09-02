"""Filesystem agent discovery.

Walks one or more directory trees and groups files into :class:`AgentUnit`s. An
agent unit is a candidate agent project: either a directory that holds a
recognized dependency manifest (the common case) or a directory of orphan source
files with no manifest ancestor. Source files attach to the nearest enclosing
manifest directory so nested layouts (e.g. ``project/src/agent.ts``) collapse
into a single unit.

Standard-library only (``os``, ``pathlib``); safe for the frozen ``aiwatch``
bundle.
"""

from __future__ import annotations

import os
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path

from runlayer_cli.scan.agents.languages import EXT_LANGUAGE
from runlayer_cli.scan.agents.manifests import (
    ManifestInfo,
    manifest_kind,
    parse_manifest,
)
from runlayer_cli.scan.skip_dirs import SKIP_DIR_NAMES, SKIP_DIR_PATH_SUFFIXES

# Directories that never contain first-party agent source worth scanning.
# Sourced from the canonical scan skip set so the agent walk and the project
# crawl stay in lockstep (see runlayer_cli.scan.skip_dirs).
IGNORED_DIRS: frozenset[str] = SKIP_DIR_NAMES

# Bound per-file reads so a single huge file cannot blow up memory on a scan.
MAX_FILE_BYTES = 512 * 1024

# How often (in files) the walk re-checks its deadline. os.walk yields per
# directory, so a per-directory check alone lets one huge directory's reads run
# well past the budget; re-check inside the file loop to keep the overrun small.
_DEADLINE_CHECK_EVERY = 128

# Cap source files attached per unit. Framework detection leans on the manifest
# (declared deps are the strongest signal) with source imports/symbols as a
# secondary confirmation, so a handful of source files is plenty -- but a giant
# monorepo package can hold thousands. Reading and regex-scoring every one is
# the dominant cost of the walk (and a single unbounded ``detect`` can blow the
# time budget), so cap it: the first N files are representative for detection.
MAX_SOURCES_PER_UNIT = 400

# Global cap on source text held in memory per ``discover`` call. A tree full
# of large units (400 files x 512 KB each) can otherwise retain gigabytes of
# text at once; past the budget, files keep their paths (language signal for
# unit shape) but skip the content read.
# Retained size uses ``len(str)`` as a cheap code-point approximation.
MAX_TOTAL_SOURCE_BYTES = 128 * 1024 * 1024


@dataclass
class SourceFile:
    """A single source file with its (bounded) text content."""

    path: Path
    text: str

    @property
    def ext(self) -> str:
        return self.path.suffix.lower()

    @property
    def language(self) -> str | None:
        return EXT_LANGUAGE.get(self.ext)


@dataclass
class AgentUnit:
    """A discovered agent project: a root directory plus its manifests/sources."""

    root: Path
    manifests: list[ManifestInfo] = field(default_factory=list)
    sources: list[SourceFile] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.root.name

    @property
    def deps(self) -> set[str]:
        out: set[str] = set()
        for m in self.manifests:
            out.update(m.deps)
        return out

    @property
    def ecosystems(self) -> set[str]:
        return {m.ecosystem for m in self.manifests}

    @property
    def languages(self) -> set[str]:
        """Languages implied by manifests and by source-file extensions."""
        langs = {m.language for m in self.manifests}
        langs.update(sf.language for sf in self.sources if sf.language)
        return {lang for lang in langs if lang and lang != "Unknown"}


def _should_skip_dir(name: str) -> bool:
    return name in IGNORED_DIRS or name.endswith(".egg-info")


def _has_skip_path_suffix(path: Path) -> bool:
    parts = path.parts
    return any(
        len(parts) >= len(suffix) and parts[-len(suffix) :] == suffix
        for suffix in SKIP_DIR_PATH_SUFFIXES
    )


def _read_text(path: Path) -> str:
    try:
        with path.open("rb") as f:
            data = f.read(MAX_FILE_BYTES)
    except OSError:
        return ""
    return data.decode("utf-8", errors="replace")


def _nearest_manifest_dir(directory: Path, manifest_dirs: list[Path]) -> Path | None:
    """Return the deepest manifest dir that is ``directory`` or an ancestor of it.

    ``manifest_dirs`` must be sorted by descending depth so the first match is
    the nearest enclosing project root.
    """
    parents = set(directory.parents)
    for md in manifest_dirs:
        if md == directory or md in parents:
            return md
    return None


def discover(
    root: str | os.PathLike[str],
    *,
    seed_manifests: Mapping[Path, ManifestInfo] | None = None,
    deadline: float | None = None,
    checkpoint: Callable[[], None] | None = None,
    max_total_source_bytes: int | None = MAX_TOTAL_SOURCE_BYTES,
) -> list[AgentUnit]:
    """Discover candidate agent units under ``root``.

    Returns units sorted by path for stable output. Directories with a manifest
    become units directly; orphan source directories (no manifest ancestor) are
    emitted as manifest-less units so the detector can still classify them.

    ``seed_manifests`` maps a *resolved* manifest path to its already-parsed
    :class:`ManifestInfo`. The unified project crawl already located and parsed
    these (see :func:`runlayer_cli.scan.agent_scan.parse_crawl_manifests`), so
    reusing them here means a manifest is parsed once instead of re-parsed by
    this walk -- the crawl owns manifest parsing, the walk only collects nearby
    sources. Manifests absent from the seed (e.g. nested deeper than the crawl
    reached) are parsed here as before, so seeding never drops coverage.

    ``deadline`` is an optional :func:`time.monotonic` cutoff. The walk reads
    every first-party source file (up to :data:`MAX_FILE_BYTES` each), so a
    shallow root over a big multi-repo tree (e.g. ``~/src``) is unbounded I/O.
    When set, the walk stops descending once the cutoff passes and returns the
    units gathered so far -- best-effort by design, so the scan stays within its
    ``--project-timeout`` budget instead of hanging.

    ``checkpoint`` is the resource governor's cooperative throttle/abort hook,
    invoked at the same cadence as the deadline checks.
    ``max_total_source_bytes`` bounds the source text retained by this call;
    past it, files are enumerated without reading their content.
    """
    root = Path(root)
    seeds = seed_manifests or {}

    manifests_by_dir: dict[Path, list[ManifestInfo]] = {}
    source_paths: list[Path] = []

    hit_deadline = False
    for dirpath, dirnames, filenames in os.walk(root):
        if deadline is not None and time.monotonic() >= deadline:
            hit_deadline = True
        if not hit_deadline:
            here = Path(dirpath)
            dirnames[:] = [
                dirname
                for dirname in dirnames
                if not _should_skip_dir(dirname)
                and not _has_skip_path_suffix(here / dirname)
            ]
            for idx, filename in enumerate(filenames):
                if idx % _DEADLINE_CHECK_EVERY == 0:
                    if checkpoint is not None:
                        checkpoint()
                    if deadline is not None and time.monotonic() >= deadline:
                        hit_deadline = True
                        break
                file_path = here / filename
                if manifest_kind(filename) is not None:
                    info = seeds.get(file_path.resolve()) if seeds else None
                    if info is None:
                        info = parse_manifest(file_path)
                    if info is not None:
                        manifests_by_dir.setdefault(here, []).append(info)
                elif file_path.suffix.lower() in EXT_LANGUAGE:
                    source_paths.append(file_path)
        if hit_deadline:
            # Prune the rest of the walk (mutate dirnames in place) and stop;
            # partial units are still valid detections for what we did reach.
            dirnames[:] = []
            break

    manifest_dirs = sorted(manifests_by_dir, key=lambda p: len(p.parts), reverse=True)

    units: dict[Path, AgentUnit] = {
        d: AgentUnit(root=d, manifests=infos) for d, infos in manifests_by_dir.items()
    }
    orphan_units: dict[Path, AgentUnit] = {}

    # Reading source text is the walk's dominant cost, so honor the deadline here
    # too (the enumeration above only listed paths) and cap files per unit. The
    # deadline cadence keys off the loop index, not the read count, so capped
    # units (which skip the read) can't stall the periodic check.
    total_source_bytes = 0
    for idx, source_path in enumerate(source_paths):
        if idx % _DEADLINE_CHECK_EVERY == 0:
            if checkpoint is not None:
                checkpoint()
            if deadline is not None and time.monotonic() >= deadline:
                break
        owner = _nearest_manifest_dir(source_path.parent, manifest_dirs)
        if owner is not None:
            unit = units[owner]
        else:
            unit = orphan_units.get(source_path.parent)
            if unit is None:
                unit = AgentUnit(root=source_path.parent)
                orphan_units[source_path.parent] = unit
        if len(unit.sources) >= MAX_SOURCES_PER_UNIT:
            continue
        if (
            max_total_source_bytes is not None
            and total_source_bytes >= max_total_source_bytes
        ):
            text = ""
        else:
            text = _read_text(source_path)
            total_source_bytes += len(text)
        unit.sources.append(SourceFile(path=source_path, text=text))

    all_units = list(units.values()) + list(orphan_units.values())
    for unit in all_units:
        unit.sources.sort(key=lambda sf: str(sf.path))
    all_units.sort(key=lambda u: str(u.root))
    return all_units
