"""Extract code references from plan Markdown text (FR-001, FR-004)."""

from __future__ import annotations

import re

from .models import Reference, ReferenceKind

# Patterns for extracting references from plan text
_BACKTICK_RE = re.compile(r"`([^`\n]+)`")
_CODE_FENCE_RE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
_FILE_EXTENSIONS = (
    "py",
    "toml",
    "yml",
    "yaml",
    "json",
    "md",
    "txt",
    "cfg",
    "ini",
    "sh",
    "ts",
    "js",
    "rs",
    "go",
    "proto",
    "ipynb",
    "j2",
    "lock",
    # Passthrough extensions accepted by verify_artifacts._PASSTHROUGH_EXT_RE
    "sql",
    "css",
    "html",
    "xml",
    "tf",
    "env",
    "conf",
    "csv",
    "in",
)
_FILE_EXT_PATTERN = "|".join(_FILE_EXTENSIONS)
_FILE_EXT_RE = re.compile(rf"\.(?:{_FILE_EXT_PATTERN})$", re.IGNORECASE)
_CONVENTIONAL_EXTENSIONLESS_FILENAMES = (
    "Dockerfile",
    "Makefile",
    "Vagrantfile",
    "Procfile",
    "Jenkinsfile",
    "Brewfile",
    "Gemfile",
    "Pipfile",
    "Rakefile",
    "CMakeLists",
)
_CONVENTIONAL_EXTENSIONLESS_ALT = "|".join(
    re.escape(filename) for filename in sorted(_CONVENTIONAL_EXTENSIONLESS_FILENAMES)
)
_FENCE_FILE_PATH_RE = re.compile(
    rf"(?<![\w`])((?:"
    rf"(?i:[a-zA-Z_][\w/.-]*\.(?:{_FILE_EXT_PATTERN}))"
    rf"|(?i:\.(?:{_FILE_EXT_PATTERN}))"
    rf"|(?:[\w.-]+/)+(?:{_CONVENTIONAL_EXTENSIONLESS_ALT})"
    rf"|(?:{_CONVENTIONAL_EXTENSIONLESS_ALT})"
    rf"))(?![\w./-])"
)


def extract_references(plan_text: str, *, dedup: bool = True) -> list[Reference]:
    """Extract code references from *plan_text* (FR-001, FR-004, FR-015).

    Extracts backtick-quoted identifiers and code fence contents.
    When *dedup* is ``True`` (the default) deduplicates by reference text,
    preserving first occurrence line number.  Pass ``dedup=False`` to retain
    every occurrence so callers can aggregate across occurrences (e.g. suppress
    only when *all* occurrences are conditional).
    """
    if not plan_text.strip():
        return []

    references: list[Reference] = []
    seen: set[str] = set()

    lines = plan_text.splitlines()

    # Extract backtick-quoted identifiers
    for line_num, line in enumerate(lines, start=1):
        for match in _BACKTICK_RE.finditer(line):
            text = match.group(1).strip()
            if text and (not dedup or text not in seen):
                if dedup:
                    seen.add(text)
                kind = classify_reference_kind(text)
                references.append(
                    Reference(
                        text=text,
                        kind=kind,
                        plan_location=f"L{line_num}",
                        context_sentence=line.strip(),
                    )
                )

    # Extract identifiers from code fences
    for match in _CODE_FENCE_RE.finditer(plan_text):
        fence_content = match.group(1)
        # Find line number of the fence start
        fence_start = plan_text[: match.start()].count("\n") + 1
        for rel_line, fence_line in enumerate(fence_content.splitlines()):
            # Extract bare identifiers that look like file paths.
            # Exclude backtick-prefixed tokens — the global backtick pass above
            # already captures those, so including them here would double-count
            # every backtick-quoted reference inside code fences.
            for bare_match in _FENCE_FILE_PATH_RE.finditer(fence_line):
                text = bare_match.group(1).strip()
                if text and (not dedup or text not in seen):
                    if dedup:
                        seen.add(text)
                    kind = classify_reference_kind(text)
                    references.append(
                        Reference(
                            text=text,
                            kind=kind,
                            plan_location=f"L{fence_start + rel_line + 1}",
                            context_sentence=fence_line.strip(),
                        )
                    )

    return references


def classify_reference_kind(text: str) -> ReferenceKind:
    """Classify a reference text into a ReferenceKind (FR-001, FR-007)."""
    # File path: contains / or ends with known extension
    if "/" in text or _FILE_EXT_RE.search(text):
        return ReferenceKind.FILE_PATH

    # CLI command: starts with agdt- or contains dashes typical of CLI
    if text.startswith("agdt-") or text.startswith("agdt_"):
        return ReferenceKind.CLI_COMMAND

    # Module path: dotted notation without uppercase start
    if "." in text and not text[0].isupper():
        return ReferenceKind.MODULE_PATH

    # Class name: starts with uppercase, CamelCase
    if text[0].isupper() and re.match(r"^[A-Z][a-zA-Z0-9]*$", text):
        return ReferenceKind.CLASS_NAME

    # Method name: contains a dot with lowercase after
    if "." in text and text.split(".")[-1][0:1].islower():
        return ReferenceKind.METHOD_NAME

    # Function name: snake_case starting lowercase
    if re.match(r"^[a-z_][a-z0-9_]*$", text) and len(text) > 2:
        return ReferenceKind.FUNCTION_NAME

    return ReferenceKind.UNCLASSIFIED
