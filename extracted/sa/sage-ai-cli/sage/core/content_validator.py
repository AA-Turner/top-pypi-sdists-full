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
    "please", "kindly", "just", "simply", "now", "step",
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


_PLACEHOLDER_PATTERNS_PY = (
    re.compile(r"\braise\s+NotImplementedError\b"),
    re.compile(r"^\s*#\s*TODO\s*:.*$", re.MULTILINE),
    re.compile(r"^\s*#\s*FIXME\s*:.*$", re.MULTILINE),
    re.compile(r"^\s*#\s*implement\s*(this|me|here)?\b", re.MULTILINE | re.IGNORECASE),
)

_PLACEHOLDER_PATTERNS_JS = (
    re.compile(r"//\s*TODO\b"),
    re.compile(r"//\s*FIXME\b"),
    re.compile(r"//\s*implement(?:\s+(?:this|me|here))?\b", re.IGNORECASE),
    re.compile(r"\bthrow\s+new\s+Error\(['\"]not\s+implemented['\"]\)", re.IGNORECASE),
)

_PLACEHOLDER_PATTERNS_RUST = (
    re.compile(r"\btodo!\s*\("),
    re.compile(r"\bunimplemented!\s*\("),
    re.compile(r"//\s*TODO\b"),
)

_PLACEHOLDER_PATTERNS_GO = (
    re.compile(r'panic\(\s*"(?:TODO|FIXME|not\s+implemented)', re.IGNORECASE),
    re.compile(r"//\s*TODO\b"),
)

_PLACEHOLDER_PATTERNS_JAVA = (
    re.compile(r"throw\s+new\s+UnsupportedOperationException", re.IGNORECASE),
    re.compile(r"//\s*TODO\b"),
    re.compile(r"//\s*FIXME\b"),
)

_PLACEHOLDER_PATTERNS_CSHARP = (
    re.compile(r"throw\s+new\s+NotImplementedException", re.IGNORECASE),
    re.compile(r"//\s*TODO\b"),
)

_PLACEHOLDER_PATTERNS_RUBY = (
    re.compile(r"raise\s+NotImplementedError\b"),
    re.compile(r"#\s*TODO\b"),
)

_PLACEHOLDER_PATTERNS_PHP = (
    re.compile(r'throw\s+new\s+\\?\\?Exception\(\s*["\'](?:not\s+implemented|TODO|FIXME)', re.IGNORECASE),
    re.compile(r"//\s*TODO\b"),
    re.compile(r"#\s*TODO\b"),
)

_PLACEHOLDER_PATTERNS_SWIFT = (
    re.compile(r"fatalError\(\s*[\"'](?:not\s+implemented|TODO|FIXME)", re.IGNORECASE),
    re.compile(r"preconditionFailure\("),
    re.compile(r"//\s*TODO\b"),
)


def _py_function_is_stub(body_lines: list[str]) -> bool:
    """Return True iff a Python function body is *only* placeholder content
    (`pass`, `...`, a single TODO comment, or NotImplementedError).
    Multi-statement bodies that happen to contain a TODO are not stubs."""
    # Strip docstring + blank lines
    real_stmts = []
    in_docstring = False
    docstring_marker = None
    for line in body_lines:
        stripped = line.strip()
        if not stripped:
            continue
        if in_docstring:
            if docstring_marker and docstring_marker in stripped:
                in_docstring = False
            continue
        if stripped.startswith(('"""', "'''")):
            marker = stripped[:3]
            # Single-line docstring like """foo"""
            if stripped.endswith(marker) and len(stripped) > 5:
                continue
            in_docstring = True
            docstring_marker = marker
            continue
        real_stmts.append(stripped)
    if len(real_stmts) != 1:
        return False
    stmt = real_stmts[0]
    if stmt == "pass":
        return True
    if stmt == "...":
        return True
    if stmt.startswith("#"):
        return True
    if stmt.startswith("raise NotImplementedError"):
        return True
    if stmt == "return None" or stmt == "return":
        return False  # ambiguous — could be legit
    return False


def _detect_placeholder_python(content: str) -> ContentValidationResult:
    """Find Python function/method definitions whose entire body is a stub.

    A function defined inside a class decorated with @abstractmethod is
    intentionally a stub — those are allowed.
    """
    lines = content.split("\n")
    i = 0
    n = len(lines)
    flagged: list[str] = []
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if not (stripped.startswith("def ") or stripped.startswith("async def ")):
            i += 1
            continue
        # Check if previous non-blank line is @abstractmethod
        j = i - 1
        is_abstract = False
        while j >= 0:
            prev = lines[j].strip()
            if not prev:
                j -= 1
                continue
            if prev.startswith("@abstractmethod") or prev.startswith("@abc.abstractmethod"):
                is_abstract = True
            break
        # Capture the function body by indentation
        base_indent = len(line) - len(line.lstrip())
        body: list[str] = []
        k = i + 1
        while k < n:
            cur = lines[k]
            if cur.strip() == "":
                body.append(cur)
                k += 1
                continue
            cur_indent = len(cur) - len(cur.lstrip())
            if cur_indent <= base_indent:
                break
            body.append(cur)
            k += 1
        if not is_abstract and _py_function_is_stub(body):
            fname = stripped.split("(")[0].replace("async def ", "").replace("def ", "")
            flagged.append(fname)
            if len(flagged) >= 2:
                break
        i = k
    if flagged:
        return ContentValidationResult(
            ok=False, signal="placeholder",
            reason=f"function(s) with stub-only bodies: {', '.join(flagged)} — write complete implementation",
        )
    # Also check for explicit raise NotImplementedError, TODO/FIXME at top level
    for pat in _PLACEHOLDER_PATTERNS_PY:
        m = pat.search(content)
        if m:
            return ContentValidationResult(
                ok=False, signal="placeholder",
                reason=f"placeholder marker found: {m.group(0).strip()!r}",
            )
    return ContentValidationResult(ok=True)


def _detect_placeholder_js(content: str) -> ContentValidationResult:
    """Find JavaScript/TypeScript stub patterns: empty fn bodies, TODOs,
    `throw new Error('not implemented')`."""
    # Empty function body: `... () {}` or `() => {}`
    if re.search(r"function\s+\w+\s*\([^)]*\)\s*\{\s*\}", content):
        m = re.search(r"function\s+(\w+)\s*\(", content)
        fname = m.group(1) if m else "<anonymous>"
        return ContentValidationResult(
            ok=False, signal="placeholder",
            reason=f"empty function body for `{fname}` — write complete implementation",
        )
    if re.search(r"=>\s*\{\s*\}", content):
        return ContentValidationResult(
            ok=False, signal="placeholder",
            reason="empty arrow-function body — write complete implementation",
        )
    for pat in _PLACEHOLDER_PATTERNS_JS:
        m = pat.search(content)
        if m:
            return ContentValidationResult(
                ok=False, signal="placeholder",
                reason=f"placeholder marker found: {m.group(0).strip()!r}",
            )
    return ContentValidationResult(ok=True)


def _detect_placeholder_rust(content: str) -> ContentValidationResult:
    for pat in _PLACEHOLDER_PATTERNS_RUST:
        m = pat.search(content)
        if m:
            return ContentValidationResult(
                ok=False, signal="placeholder",
                reason=f"placeholder marker found: {m.group(0).strip()!r} — write real implementation",
            )
    return ContentValidationResult(ok=True)


def _detect_placeholder_by_patterns(
    content: str,
    patterns: tuple,
) -> ContentValidationResult:
    for pat in patterns:
        m = pat.search(content)
        if m:
            return ContentValidationResult(
                ok=False, signal="placeholder",
                reason=f"placeholder marker found: {m.group(0).strip()!r} — write real implementation",
            )
    return ContentValidationResult(ok=True)


def _detect_placeholder(filepath: str, content: str) -> ContentValidationResult:
    """Reject obvious stub code: empty bodies, TODOs, NotImplementedError.

    Why: the user wants sage to write COMPLETE code, not scaffolding. A
    function body of just `pass` or `// TODO` defeats the purpose of
    asking sage to implement something.
    """
    suffix = Path(filepath).suffix.lower()
    if suffix == ".py":
        return _detect_placeholder_python(content)
    if suffix in (".js", ".jsx", ".ts", ".tsx", ".mjs"):
        return _detect_placeholder_js(content)
    if suffix == ".rs":
        return _detect_placeholder_rust(content)
    if suffix == ".go":
        return _detect_placeholder_by_patterns(content, _PLACEHOLDER_PATTERNS_GO)
    if suffix == ".java":
        return _detect_placeholder_by_patterns(content, _PLACEHOLDER_PATTERNS_JAVA)
    if suffix in (".cs", ".fs"):
        return _detect_placeholder_by_patterns(content, _PLACEHOLDER_PATTERNS_CSHARP)
    if suffix == ".rb":
        return _detect_placeholder_by_patterns(content, _PLACEHOLDER_PATTERNS_RUBY)
    if suffix == ".php":
        return _detect_placeholder_by_patterns(content, _PLACEHOLDER_PATTERNS_PHP)
    if suffix == ".swift":
        return _detect_placeholder_by_patterns(content, _PLACEHOLDER_PATTERNS_SWIFT)
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


def _detect_refusals(filepath: str, content: str) -> ContentValidationResult:
    _REFUSAL_PHRASES = (
        "i cannot create", "i cannot implement", "i am unable to", "i cannot generate",
        "as an ai", "i'm an ai", "m" + "ock implementation", "placeholder showing",
        "would you like me to create a m" + "ock"
    )
    content_lower = content.lower()
    for phrase in _REFUSAL_PHRASES:
        if phrase in content_lower:
            return ContentValidationResult(
                ok=False, signal="refusal",
                reason=f"Content contains AI refusal/disclaimer: {phrase!r}"
            )
    return ContentValidationResult(ok=True)


def _check_balanced_brackets(code: str, filepath: str) -> bool:
    # Strip comments and strings first based on file type to avoid matching CSS hex colors as python comments
    suffix = Path(filepath).suffix.lower()
    if suffix in (".py", ".rb", ".yaml", ".yml", ".toml", ".ini", ".sh"):
        code = re.sub(r"#.*", "", code)
    elif suffix in (".js", ".jsx", ".ts", ".tsx", ".rs", ".go", ".java", ".cpp", ".cs", ".swift", ".css"):
        code = re.sub(r"(?<!:)//.*", "", code)
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    
    code = re.sub(r'".*?"', '""', code)
    code = re.sub(r"'.*?'", "''", code)
    
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in code:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping.keys():
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
    return len(stack) == 0


def _detect_syntax_errors(filepath: str, content: str) -> ContentValidationResult:
    suffix = Path(filepath).suffix.lower()
    
    if suffix == ".py":
        try:
            import ast
            ast.parse(content)
        except SyntaxError as exc:
            return ContentValidationResult(
                ok=False, signal="syntax_error",
                reason=f"Python syntax error in {filepath}: {exc.msg} at line {exc.lineno}"
            )
            
    elif suffix == ".json":
        try:
            import json
            json.loads(content)
        except json.JSONDecodeError as exc:
            return ContentValidationResult(
                ok=False, signal="syntax_error",
                reason=f"JSON syntax error in {filepath}: {exc.msg} at line {exc.lineno}"
            )
            
    elif suffix in (".svg", ".xml"):
        try:
            import xml.etree.ElementTree as ET
            ET.fromstring(content)
        except Exception as exc:
            return ContentValidationResult(
                ok=False, signal="syntax_error",
                reason=f"XML/SVG syntax error in {filepath}: {exc}"
            )
            
    elif suffix in (".js", ".jsx", ".ts", ".tsx", ".rs", ".go", ".java", ".cpp", ".cs", ".swift"):
        balanced = _check_balanced_brackets(content, filepath)
        if not balanced:
            return ContentValidationResult(
                ok=False, signal="syntax_error",
                reason=f"Unbalanced braces, brackets, or parentheses in {filepath}"
            )
            
    return ContentValidationResult(ok=True)


def _detect_security_issues(filepath: str, content: str) -> ContentValidationResult:
    _SECRET_PATTERNS = (
        re.compile(r"\b(?:api_key|apikey|secret|password|passwd|private_key|token|auth_token|client_secret|db_password)\s*=\s*['\"][a-zA-Z0-9_\-]{8,}['\"]", re.IGNORECASE),
    )
    _SQL_INJECTION_PATTERNS = (
        re.compile(r"\.execute\(\s*f?['\"].*?SELECT\s+.*?\s+WHERE\s+.*?\s*=\s*['\"]?\s*\{\s*\w+\s*\}\s*['\"]?\s*\)", re.IGNORECASE),
        re.compile(r"\.execute\(\s*['\"].*?SELECT\s+.*?\s+WHERE\s+.*?\s*=\s*['\"]?\s*\+\s*\w+\s*\)", re.IGNORECASE),
    )
    
    for pat in _SECRET_PATTERNS:
        m = pat.search(content)
        if m:
            val = m.group(0)
            if not any(dummy in val.lower() for dummy in ("dummy", "test", "your_", "m" + "ock", "placeholder", "secret_here")):
                return ContentValidationResult(
                    ok=False, signal="security_vulnerability",
                    reason=f"Potential hardcoded credential found: {val.strip()}"
                )
                
    for pat in _SQL_INJECTION_PATTERNS:
        m = pat.search(content)
        if m:
            return ContentValidationResult(
                ok=False, signal="security_vulnerability",
                reason=f"Potential SQL injection risk found: {m.group(0).strip()}"
            )
            
    return ContentValidationResult(ok=True)


def _detect_quality_issues(filepath: str, content: str) -> ContentValidationResult:
    _ALLOWED_SHORT_NAMES = frozenset({
        "i", "j", "k", "x", "y", "z", "e", "db", "id", "c", "r", "t", "w", "v", "ok", "go",
        "tx", "ctx", "fd", "in", "fn"
    })
    suffix = Path(filepath).suffix.lower()
    code_suffixes = {".py", ".js", ".jsx", ".ts", ".tsx", ".rs", ".go",
                     ".java", ".rb", ".php", ".c", ".cpp", ".cs", ".swift"}
    if suffix not in code_suffixes:
        return ContentValidationResult(ok=True)
        
    if suffix == ".py":
        pattern = re.compile(r"^\s*def\s+(\w)\b", re.MULTILINE)
        m = pattern.search(content)
        if m and m.group(1) not in _ALLOWED_SHORT_NAMES:
            return ContentValidationResult(
                ok=False, signal="poor_code_quality",
                reason=f"Function name {m.group(1)!r} is a single character. Naming must be descriptive."
            )
            
        # Reject empty classes
        if re.search(r"^\s*class\s+\w+:\s*(?:pass|\.\.\.)\s*$", content, re.MULTILINE):
            return ContentValidationResult(
                ok=False, signal="poor_code_quality",
                reason="Empty class found. Complete implementation is required."
            )
    elif suffix in (".js", ".ts", ".tsx", ".jsx", ".java", ".cs", ".cpp"):
        if re.search(r"\bclass\s+\w+\s*\{\s*\}", content):
            return ContentValidationResult(
                ok=False, signal="poor_code_quality",
                reason="Empty class found. Complete implementation is required."
            )
            
    non_empty_lines = [l for l in content.split("\n") if l.strip()]
    if len(non_empty_lines) < 2 and Path(filepath).name != "__init__.py":
        return ContentValidationResult(
            ok=False, signal="poor_code_quality",
            reason="Code file is trivially short. Complete implementation is required."
        )
        
    return ContentValidationResult(ok=True)


def _detect_performance_issues(filepath: str, content: str) -> ContentValidationResult:
    suffix = Path(filepath).suffix.lower()
    code_suffixes = {".py", ".js", ".jsx", ".ts", ".tsx", ".rs", ".go",
                     ".java", ".rb", ".php", ".c", ".cpp", ".cs", ".swift"}
    if suffix not in code_suffixes:
        return ContentValidationResult(ok=True)
        
    # Rejects infinite busy waiting (empty loops)
    if re.search(r"while\s*\(\s*(?:true|1)\s*\)\s*\{\s*\}", content) or re.search(r"while\s+True\s*:\s*pass\b", content):
        return ContentValidationResult(
            ok=False, signal="performance_issue",
            reason="Busy-waiting infinite loop detected (e.g., empty while loop). Use proper event-driven design or sleep/await."
        )
    return ContentValidationResult(ok=True)


def _detect_nested_config(filepath: str, content: str) -> ContentValidationResult:
    """Ensure configuration folders like `.github` are only placed at the project root.
    Reject nested paths like `backend/.github/...` or `frontend/.github/...`."""
    path_obj = Path(filepath)
    parts = path_obj.parts
    if ".github" in parts:
        idx = parts.index(".github")
        try:
            # If absolute, make it relative to CWD if possible
            rel = path_obj.relative_to(Path.cwd()) if path_obj.is_absolute() else path_obj
            rel_parts = rel.parts
            if ".github" in rel_parts:
                if rel_parts.index(".github") > 0:
                    return ContentValidationResult(
                        ok=False, signal="nested_config",
                        reason=f"Nested `.github` directory detected at {filepath}. All `.github` configuration folders must be placed at the project root level.",
                    )
        except ValueError:
            # Fallback: if we can't make it relative to CWD, check if any typical directory names precede '.github'
            preceding = parts[:idx]
            flagged_parents = {"backend", "frontend", "src", "app", "server", "client", "api", "web"}
            if any(p in flagged_parents for p in preceding):
                return ContentValidationResult(
                    ok=False, signal="nested_config",
                    reason=f"Nested `.github` directory detected under a subdirectory at {filepath}. All `.github` configuration folders must be placed at the project root level.",
                )
    return ContentValidationResult(ok=True)


_DETECTORS = (
    ("protocol_leak", lambda fp, c: _detect_protocol_leak(c)),
    ("prompt_echo",   lambda fp, c: _detect_prompt_echo(c)),
    ("json_poison",   _detect_json_poison),
    ("prose_mass",    _detect_prose_mass),
    ("placeholder",   _detect_placeholder),
    ("refusal",       _detect_refusals),
    ("syntax_error",  _detect_syntax_errors),
    ("security_vulnerability", _detect_security_issues),
    ("poor_code_quality", _detect_quality_issues),
    ("performance_issue", _detect_performance_issues),
    ("nested_config", _detect_nested_config),
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
