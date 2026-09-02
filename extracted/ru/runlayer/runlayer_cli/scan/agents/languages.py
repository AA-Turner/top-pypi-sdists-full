"""Single source of truth for the language / ecosystem / family taxonomy.

Three parallel maps used to live in three modules -- source-file extensions in
``discover``, package ecosystems in ``manifests``, and coarse families in
``detect`` -- so adding a language (Kotlin, Swift, ...) meant three edits that
could drift. They live here now: one edit, consumed everywhere.

Standard-library only; safe for the frozen ``aiwatch`` bundle.
"""

from __future__ import annotations

# Source-file extension -> human-readable language label (consumed by discover).
EXT_LANGUAGE: dict[str, str] = {
    ".py": "Python",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".rs": "Rust",
    ".go": "Go",
    ".java": "Java",
    ".cs": "C#",
}

# Package ecosystem -> the (default) human-readable language label (manifests).
ECOSYSTEM_LANGUAGE: dict[str, str] = {
    "python": "Python",
    "npm": "JavaScript",
    "cargo": "Rust",
    "go": "Go",
    "maven": "Java",
    "nuget": "C#",
}

# Language label -> coarse family so JS/TS (and JVM langs) interoperate (detect).
LANGUAGE_FAMILY: dict[str, str] = {
    "Python": "python",
    "TypeScript": "js",
    "JavaScript": "js",
    "Rust": "rust",
    "Go": "go",
    "Java": "jvm",
    "Kotlin": "jvm",
    "C#": "dotnet",
}


def language_family(language: str | None) -> str | None:
    """Coarse family for a language label, or ``None`` if unknown / ``None``."""
    if language is None:
        return None
    return LANGUAGE_FAMILY.get(language)
