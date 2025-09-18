from __future__ import annotations

import os
from fnmatch import fnmatch
from pathlib import Path
from typing import TYPE_CHECKING

from .defaults import (
    CONFIG_MARKERS,
    EXCLUDE_DIRS,
    SKIP_DIRS,
    TEST_FILES,
    Language,
)

if TYPE_CHECKING:
    from collections.abc import Iterable


def _detect_languages_in_dir(files: Iterable[str]) -> list[Language]:
    """Return programming languages detected in a directory via exact filenames or glob patterns.

    Handles conflicts between similar languages by using a priority system and confidence scoring.
    """
    names = {f.casefold() for f in files}
    hits: list[Language] = []

    # Language priority mapping (higher number = higher priority)
    # This helps resolve conflicts between similar languages
    language_priorities = {
        Language.TypeScript: 10,  # TypeScript has priority over JavaScript
        Language.JavaScript: 5,
        Language.Kotlin: 8,  # Kotlin has priority over Java
        Language.Java: 6,
        Language.Rust: 9,  # Rust has priority over C
        Language.C: 4,
        Language.Scala: 7,  # Scala has priority over Java
        Language.Dart: 8,  # Dart has priority over JavaScript
        Language.Python: 7,
        Language.Go: 8,
        Language.PHP: 6,
        Language.Ruby: 6,
        Language.CSharp: 7,
        Language.Swift: 8,
    }

    # Track confidence scores for each language
    language_scores: dict[Language, int] = {}

    for lang, markers in CONFIG_MARKERS.items():
        exacts: set[str] = {n.casefold() for n in markers["names"]}
        patterns: list[str] = list(markers["globs"])

        score = 0

        # Check exact name matches (higher confidence)
        exact_matches = [n for n in exacts if n in names]
        if exact_matches:
            score += len(exact_matches) * 10  # Each exact match adds 10 points

        # Check glob pattern matches (lower confidence)
        glob_matches = 0
        for f in names:
            if any(fnmatch(f, pat) for pat in patterns):
                glob_matches += 1
        if glob_matches:
            score += glob_matches * 5  # Each glob match adds 5 points

        if score > 0:
            language_scores[lang] = score
            hits.append(lang)

    # Resolve conflicts using priority system
    if len(hits) > 1:
        # Sort by priority (descending) and then by confidence score (descending)
        hits.sort(
            key=lambda lang: (
                language_priorities.get(lang, 0),
                language_scores.get(lang, 0),
            ),
            reverse=True,
        )

        # Remove lower priority languages that conflict with higher priority ones
        resolved_hits = []
        for lang in hits:
            # Check if this language conflicts with any already resolved language
            conflicts = _get_language_conflicts(lang)
            if not any(conflict in resolved_hits for conflict in conflicts):
                resolved_hits.append(lang)

        hits = resolved_hits

    return hits


def _get_language_conflicts(lang: Language) -> set[Language]:
    """Return languages that conflict with the given language."""
    conflicts = {
        Language.TypeScript: {Language.JavaScript},
        Language.JavaScript: {Language.TypeScript, Language.Dart},
        Language.Kotlin: {Language.Java, Language.Scala},
        Language.Java: {Language.Kotlin, Language.Scala},
        Language.Scala: {Language.Java, Language.Kotlin},
        Language.Rust: {Language.C},
        Language.C: {Language.Rust},
        Language.Dart: {Language.JavaScript},
    }
    return conflicts.get(lang, set())


def _optimize_exclusions(exclusions: list[str]) -> list[str]:
    """Optimize a list of exclusion paths.

    If a directory is present in the list, its subdirectories are removed to avoid redundancy.
    For example:
        ['a', 'a/b', 'c'] -> ['a', 'c']
    """
    if not exclusions:
        return []

    # sorting ensures that parent directories are processed before children
    paths = sorted([Path(p) for p in set(exclusions)])

    optimized: list[Path] = []
    for p in paths:
        # if 'p' is a subpath of something already optimized, it is ignored
        if not any(p.is_relative_to(opt_p) for opt_p in optimized):
            optimized.append(p)

    return sorted([p.as_posix() for p in optimized])


def _scan_dir(
    dir_path: Path,
    root_dir: Path,
    excluded_by_skip: set[str],
) -> list[tuple[Path, Language, list[str]]]:
    """Recursively scan *dir_path* to detect projects.

    This helper contains the heavy-lifting previously embedded in
    ``find_projects``. Extracting it keeps ``find_projects`` concise and
    under the configured complexity threshold.
    """
    try:
        entries = list(os.scandir(dir_path))
    except PermissionError:
        # avoid problems with protected paths (e.g., /proc in Linux)
        return []

    files: list[str] = []
    for e in entries:
        if not e.is_file():
            continue
        name = e.name
        if any(fnmatch(name, pat) for pat in TEST_FILES) or any(
            fnmatch(name, pat) for pat in EXCLUDE_DIRS
        ):
            # register for global exclusion (relative to the root)
            excluded_by_skip.add(Path(e.path).relative_to(root_dir).as_posix())
            continue
        files.append(name)

    subdirs_entries = [e for e in entries if e.is_dir()]
    langs = _detect_languages_in_dir(files)
    subprojects: list[tuple[Path, Language, list[str]]] = []

    for sd in subdirs_entries:
        name = sd.name
        rel_sd = Path(sd.path).relative_to(root_dir).as_posix()
        # should we skip this directory?
        skip_dir = (
            name.startswith(".tox")
            or any(fnmatch(name, pat) for pat in SKIP_DIRS)
            or any(fnmatch(rel_sd, pat) for pat in EXCLUDE_DIRS)
        )
        if skip_dir:
            excluded_by_skip.add(rel_sd)
            continue
        subprojects.extend(_scan_dir(Path(sd.path), root_dir, excluded_by_skip))

    if langs:
        language = langs[0] if len(langs) == 1 else Language.Unknown
        exclusions = [sp[0].relative_to(dir_path).as_posix() for sp in subprojects]
        exclusions = _optimize_exclusions(exclusions)
        return [(dir_path, language, exclusions), *subprojects]

    # if there is no project here, simply propagate the subprojects
    return subprojects


def find_projects(root_dir: str | Path) -> list[tuple[Path, str, list[str]]]:
    """Recursively detect projects and sub-projects grouped by language.

    Returns a tuple (project_path, language_str, exclusions) where 'exclusions' are POSIX paths
    relative to 'project_path' only. The root directory is always included with the language
    set to "root".
    """
    root_dir = Path(root_dir).resolve()

    excluded_by_skip: set[str] = set()

    # recursive scan
    projects = _scan_dir(root_dir, root_dir, excluded_by_skip)

    # add specific excluded files/dirs to each project
    enriched_projects: list[tuple[Path, str, list[str]]] = []
    for p_path, p_lang, p_excls in projects:
        extra: list[str] = []
        for rel in excluded_by_skip:
            abs_rel = root_dir / rel
            if abs_rel.is_relative_to(p_path):
                extra.append(abs_rel.relative_to(p_path).as_posix())
        final_excls = _optimize_exclusions([*p_excls, *extra]) if extra else p_excls

        # Ensure absolute path and string language code
        lang_str = p_lang.value if isinstance(p_lang, Language) else str(p_lang)
        enriched_projects.append((p_path, lang_str, final_excls))

    # Exclusions for the root = all detected projects + skipped dirs
    # 'p[0]' is already relative to 'root_dir' thanks to the transformation above,
    # so calling '.relative_to(root_dir)' again would raise a ValueError. We can
    # use it directly.
    # Compute root exclusions as POSIX paths relative to the root directory
    root_exclusions = [p[0].relative_to(root_dir).as_posix() for p in enriched_projects]
    root_exclusions.extend(excluded_by_skip)
    root_exclusions = _optimize_exclusions(root_exclusions)

    return [
        (
            root_dir,
            "root",
            root_exclusions,
        ),
        *enriched_projects,
    ]


__all__ = ["Language", "find_projects"]
