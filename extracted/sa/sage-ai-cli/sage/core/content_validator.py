"""FILE: block content validator — reject prose-as-code writes."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "ContentValidationResult",
    "validate_content",
    "validate_file_content",
]


@dataclass
class ContentValidationResult:
    ok: bool
    reason: str = ""
    signal: str = ""

    def __bool__(self) -> bool:
        return self.ok


_PROTOCOL_MARKERS = (
    re.compile(r"^\s*## (STEP|TASK|NEXT STEPS|CURRENT PLAN|LOGIC REQUIRED|EDGE CASES|NEXT ACTION|SESSION CONTEXT)\b", re.MULTILINE),
    re.compile(r"^---\s*END OF PREVIOUS FINDINGS\s*---", re.MULTILINE),
    re.compile(r"^Plan ID:\s*plan_\d{8}_\d{6}", re.MULTILINE),
    re.compile(r"^\s*FILE:\s+\S+\.[a-zA-Z]+\s*$", re.MULTILINE),
    re.compile(r"^\s*READ:\s+", re.MULTILINE),
    re.compile(r"^\s*SEARCH:\s+", re.MULTILINE),
    re.compile(r"^\s*RUN:\s+npm install", re.MULTILINE),
    re.compile(r"^\s*WEB_FETCH:\s+", re.MULTILINE),
    re.compile(r"^\s*SEARCH_WEB:\s+", re.MULTILINE),
)

_BAD_PACKAGE_NAMES = frozenset({
    "are", "is", "be", "been", "being", "am",
    "and", "or", "but", "the", "a", "an",
    "you", "we", "they", "it", "this", "that", "your", "my", "our",
    "to", "from", "with", "for", "of", "at", "in", "on", "by",
    "ensure", "ensured", "met", "make", "sure", "use", "using", "needed",
    "install", "installed", "must", "should", "should've", "would",
    "dependencies", "package", "packages", "modules", "all",
    "please", "kindly", "just", "simply", "now", "next", "step",
})

_VALID_VERSION_RE = re.compile(
    r"^\s*(?:\^|~|>=|<=|>|<|=)?\s*"
    r"(?:\d+\.\d+\.\d+(?:-[\w.]+)?(?:\+[\w.]+)?"
    r"|latest|\*|\d+\.x|\d+\.\d+\.x"
    r"|(?:git\+)?https?://\S+"
    r"|(?:file|workspace|npm|github):\S+"
    r")\s*$"
)


def _detect_protocol_leak(content: str) -> ContentValidationResult:
    hits: list[str] = []
    for pattern in _PROTOCOL_MARKERS:
        m = pattern.search(content)
        if m:
            hits.append(m.group(0).strip()[:80])
            if len(hits) >= 2:
                break
    if hits:
        return ContentValidationResult(
            ok=False, signal="protocol_leak",
            reason=f"content contains SAGE protocol markers (e.g. {hits[0]!r})",
        )
    return ContentValidationResult(ok=True)


def _detect_json_poison(filepath: str, content: str) -> ContentValidationResult:
    name = Path(filepath).name.lower()
    if not (name.endswith(".json") or name in {"package.json", "tsconfig.json", "composer.json"}):
        return ContentValidationResult(ok=True)
    if not content.strip():
        return ContentValidationResult(ok=True)
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        return ContentValidationResult(
            ok=False, signal="json_invalid",
            reason=f"{name} is not valid JSON: {exc.msg} at line {exc.lineno}",
        )
    if not isinstance(data, dict):
        return ContentValidationResult(ok=True)

    suspicious: list[str] = []
    for dep_key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        deps = data.get(dep_key)
        if not isinstance(deps, dict):
            continue
        for pkg_name, version in deps.items():
            pkg_lower = (pkg_name or "").lower().strip()
            if pkg_lower in _BAD_PACKAGE_NAMES:
                suspicious.append(f"{pkg_name!r}={version!r} (English-word name)")
            elif isinstance(version, str) and not _VALID_VERSION_RE.match(version):
                suspicious.append(f"{pkg_name!r}={version!r} (bad version)")
            if len(suspicious) >= 3:
                break
        if len(suspicious) >= 3:
            break

    if suspicious:
        return ContentValidationResult(
            ok=False, signal="json_poison",
            reason=f"{name} has suspicious deps: {'; '.join(suspicious[:3])}",
        )
    return ContentValidationResult(ok=True)


def _detect_prose_mass(filepath: str, content: str) -> ContentValidationResult:
    suffix = Path(filepath).suffix.lower()
    code_suffixes = {".py", ".js", ".jsx", ".ts", ".tsx", ".rs", ".go",
                     ".java", ".rb", ".php", ".c", ".cpp", ".cs", ".swift"}
    if suffix not in code_suffixes:
        return ContentValidationResult(ok=True)

    lines = [l for l in content.split("\n") if l.strip()]
    if len(lines) < 4:
        return ContentValidationResult(ok=True)
    prose_lines = sum(1 for l in lines
                      if l.lstrip().startswith(("# ", "## ", "### ", "- ", "* ", "1.", "2.", "3.")))
    if prose_lines / len(lines) > 0.5:
        return ContentValidationResult(
            ok=False, signal="prose_mass",
            reason=f"{filepath}: {prose_lines}/{len(lines)} lines are markdown prose, not code",
        )
    return ContentValidationResult(ok=True)


def _detect_prompt_echo(content: str) -> ContentValidationResult:
    has_task = bool(re.search(r"^\s*## TASK:", content, re.MULTILINE))
    has_plan = bool(re.search(r"^\s*Plan ID:\s*plan_", content, re.MULTILINE))
    has_steps = bool(re.search(r"^\s*## NEXT STEPS", content, re.MULTILINE))
    if (has_task + has_plan + has_steps) >= 2:
        return ContentValidationResult(
            ok=False, signal="prompt_echo",
            reason="content is the planning prompt echoed back, not code",
        )
    return ContentValidationResult(ok=True)


_DETECTORS = (
    ("protocol_leak", lambda fp, c: _detect_protocol_leak(c)),
    ("prompt_echo",   lambda fp, c: _detect_prompt_echo(c)),
    ("json_poison",   _detect_json_poison),
    ("prose_mass",    _detect_prose_mass),
)


def validate_content(filepath: str, content: str) -> ContentValidationResult:
    if not content or not content.strip():
        return ContentValidationResult(ok=True)
    for _name, detector in _DETECTORS:
        result = detector(filepath, content)
        if not result.ok:
            return result
    return ContentValidationResult(ok=True)


def validate_file_content(filepath: str, content: str) -> ContentValidationResult:
    return validate_content(filepath, content)
