"""Pre-write validation gate for LLM-generated files.

The principle: NEVER write a syntactically-broken or import-broken file
to disk. Instead, validate the LLM output, and on failure, regenerate
with the SPECIFIC error fed back into the next prompt.

This is the behaviour a careful engineer follows: if your code doesn't
parse, you fix it before saving. Sage was previously writing broken
files and hoping a later "doctor" pass would patch them. That's
backwards — bad code shouldn't be persisted in the first place.

Checks per language:

  Python (.py):
    1. `ast.parse` must succeed (catches syntax errors + truncation)
    2. Every name used at module scope must be bound somewhere
       (catches `from app.X import Y` references to non-existent Y,
       or `bcrypt.hash(...)` without importing bcrypt)
    3. File is not "obviously truncated" (heuristics: ends mid-function,
       trailing colon without body, unclosed paren)

  TypeScript / TSX (.ts, .tsx, .jsx):
    1. Balanced braces, parens, brackets
    2. Final character is sane (closing brace, semicolon, newline —
       not mid-token like `<Text` or `const x = `)
    3. (For TSX) no `react-router-dom` or `<div>` if file is under
       `frontend/app/` or `frontend/src/`

If validation fails, returns a `ValidationResult` with the specific
errors. The caller builds a retry prompt that says "your previous
attempt had THESE specific defects — regenerate fixing them."
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Literal


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str] = field(default_factory=list)

    def to_retry_prompt_section(self) -> str:
        """Convert to a prompt section listing the specific defects."""
        if self.ok:
            return ""
        bullets = "\n".join(f"  - {e}" for e in self.errors)
        return (
            "\n\n## Your previous attempt had these specific defects "
            "(regenerate fixing ALL of them):\n"
            f"{bullets}\n\n"
            "Output the COMPLETE corrected file. Do not omit anything. "
            "Do not say 'truncated' or 'continued from previous'. "
            "Output ONLY the full file contents."
        )


# ─────────────────────────── Python validation ──────────────────────────


_PY_BUILTINS = set(dir(__builtins__) if isinstance(__builtins__, type) else __builtins__) | {
    "True", "False", "None", "self", "cls", "__name__", "__file__", "__doc__",
    "__init__", "__main__", "annotations",
}


def _python_bound_names(tree: ast.AST) -> set[str]:
    """Names that are bound (defined / imported / assigned) anywhere in the file."""
    bound: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            bound.add(node.name)
            for arg in (node.args.args + node.args.kwonlyargs + node.args.posonlyargs):
                bound.add(arg.arg)
            if node.args.vararg:
                bound.add(node.args.vararg.arg)
            if node.args.kwarg:
                bound.add(node.args.kwarg.arg)
        elif isinstance(node, ast.ClassDef):
            bound.add(node.name)
        elif isinstance(node, ast.Lambda):
            for arg in (node.args.args + node.args.kwonlyargs + node.args.posonlyargs):
                bound.add(arg.arg)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                _bind_target(t, bound)
        elif isinstance(node, ast.AugAssign):
            _bind_target(node.target, bound)
        elif isinstance(node, ast.AnnAssign):
            _bind_target(node.target, bound)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                bound.add(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                bound.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.For):
            _bind_target(node.target, bound)
        elif isinstance(node, ast.AsyncFor):
            _bind_target(node.target, bound)
        elif isinstance(node, ast.With) or isinstance(node, ast.AsyncWith):
            for item in node.items:
                if item.optional_vars:
                    _bind_target(item.optional_vars, bound)
        elif isinstance(node, ast.comprehension):
            _bind_target(node.target, bound)
        elif isinstance(node, ast.ExceptHandler):
            if node.name:
                bound.add(node.name)
        elif isinstance(node, ast.Global) or isinstance(node, ast.Nonlocal):
            for n in node.names:
                bound.add(n)
    return bound


def _bind_target(target: ast.AST, bound: set[str]) -> None:
    if isinstance(target, ast.Name):
        bound.add(target.id)
    elif isinstance(target, (ast.Tuple, ast.List)):
        for elt in target.elts:
            _bind_target(elt, bound)
    elif isinstance(target, ast.Starred):
        _bind_target(target.value, bound)


def _python_used_names(tree: ast.AST) -> set[str]:
    """Names referenced as `Load` somewhere in the tree."""
    used: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used.add(node.id)
    return used


# Truncation patterns that look at the LAST non-blank line.
# We DON'T try to detect unclosed strings here — `ast.parse` already
# catches those reliably and false-positives kill us (e.g. a line
# ending with a closed string like `return "ok"`).
_PY_TRUNCATION_PATTERNS = (
    # Lone block-header keyword with no body (e.g. `if foo` with nothing after)
    re.compile(r"^\s*(if|elif|else|while|for|try|except|finally|with|async\s+(?:def|with|for))\b[^:]*$"),
    # Bare opening brace/paren as last token
    re.compile(r"[\(\[\{]\s*$"),
    # Trailing comma at module scope (multi-line list/dict still open)
    re.compile(r",\s*$"),
)


def _python_looks_truncated(source: str) -> bool:
    """Heuristic: does the file end in a way that suggests the LLM ran out?

    Tightened to avoid false positives on normal code. Pure syntax-level
    truncation is already caught by `ast.parse`; this catches the
    "valid syntax but obviously cut off" cases.
    """
    if not source.strip():
        return True
    lines = [ln for ln in source.splitlines() if ln.strip()]
    if not lines:
        return True
    last = lines[-1]
    return any(pat.search(last) for pat in _PY_TRUNCATION_PATTERNS)


def _python_indent_check(source: str) -> str | None:
    """Return error message if file has indentation problems, else None.

    `ast.parse` catches MOST indent errors, but mixed tabs/spaces sometimes
    parse and then fail at runtime. We use `tokenize` (what Python itself
    uses) which is stricter than ast.
    """
    import io
    import tokenize
    try:
        list(tokenize.generate_tokens(io.StringIO(source).readline))
    except (tokenize.TokenizeError, IndentationError) as exc:
        return f"IndentationError: {exc}"
    return None


def validate_python(source: str, *, path: Path | None = None) -> ValidationResult:
    """Full Python validation: syntax + undefined names + truncation heuristic + indent."""
    errors: list[str] = []

    if not source.strip():
        return ValidationResult(ok=False, errors=["file is empty"])

    # 1. Syntax parse
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        errors.append(
            f"SyntaxError at line {exc.lineno}: {exc.msg}. "
            "This usually means the file was truncated or malformed."
        )
        return ValidationResult(ok=False, errors=errors)

    # 1b. Stricter indent check via tokenize (catches mixed tabs/spaces
    # that ast.parse accepts but later runtime tools reject)
    indent_err = _python_indent_check(source)
    if indent_err:
        errors.append(indent_err)

    # 2. Truncation heuristic
    if _python_looks_truncated(source):
        errors.append(
            "File appears truncated — ends mid-statement (colon, unclosed string, "
            "or block header). You MUST output the COMPLETE file."
        )

    # 3. Undefined names — names used but not bound anywhere
    bound = _python_bound_names(tree) | _PY_BUILTINS
    used = _python_used_names(tree)
    undefined = sorted(n for n in (used - bound) if not n.startswith("_"))
    # Filter: ignore single-char loop vars (the AST already covers them; this
    # protects against false positives from comprehension scopes etc.)
    undefined = [n for n in undefined if len(n) > 1]

    if undefined:
        # Cap to 8 to keep the prompt concise
        head = undefined[:8]
        errors.append(
            "Used these names but never imported/defined them: "
            + ", ".join(f"`{n}`" for n in head)
            + (f" (+ {len(undefined) - 8} more)" if len(undefined) > 8 else "")
            + ". Add the correct `from X import Y` or `import X` for each."
        )

    return ValidationResult(ok=not errors, errors=errors)


# ───────────────────────── TypeScript / TSX validation ──────────────────


_TSX_FORBIDDEN_RN = (
    ("react-router-dom",
     "react-router-dom is NOT available in React Native / Expo. Use expo-router."),
    ("<div", "HTML <div> is invalid in React Native. Use <View> from react-native."),
    ("<input", "HTML <input> is invalid in RN. Use <TextInput> from react-native."),
    ("<button", "HTML <button> is invalid in RN. Use <Pressable> from react-native."),
    ("<form", "HTML <form> is invalid in RN. Use <View> from react-native."),
    ("<span", "HTML <span> is invalid in RN. Use <Text> from react-native."),
    ("<p>", "HTML <p> is invalid in RN. Use <Text> from react-native."),
    ("<h1", "HTML headings are invalid in RN. Use <Text> with style."),
    ("className=", "className is invalid in RN. Use style={...} with StyleSheet."),
)


def _strip_strings_comments_ts(source: str) -> str:
    """Remove TS strings + comments before counting braces (rough but useful)."""
    # Remove // line comments
    out = re.sub(r"//[^\n]*", "", source)
    # Remove /* block */ comments
    out = re.sub(r"/\*.*?\*/", "", out, flags=re.DOTALL)
    # Remove triple-quoted template strings (rare but possible)
    out = re.sub(r"`(?:\\.|[^`\\])*`", "``", out, flags=re.DOTALL)
    # Remove single-quoted strings
    out = re.sub(r"'(?:\\.|[^'\\])*'", "''", out)
    # Remove double-quoted strings
    out = re.sub(r"\"(?:\\.|[^\"\\])*\"", '""', out)
    return out


def _tsx_looks_truncated(source: str) -> bool:
    """End-of-file heuristic for TS/TSX truncation."""
    if not source.strip():
        return True
    lines = [ln for ln in source.splitlines() if ln.strip()]
    if not lines:
        return True
    last = lines[-1].strip()
    # Trailing tokens that scream "cut off"
    bad_tails = ("<", "<Text", "<View", "<Press", "const ", "let ", "function ",
                 "return (", "=>", "{", "(", "[", ",", "&&", "||")
    if any(last.endswith(t) for t in bad_tails):
        return True
    return False


def validate_typescript(
    source: str,
    *,
    path: Path | None = None,
    is_rn_frontend: bool = False,
) -> ValidationResult:
    """TS/TSX validation: balanced braces + no truncation + no RN forbidden patterns."""
    errors: list[str] = []

    if not source.strip():
        return ValidationResult(ok=False, errors=["file is empty"])

    cleaned = _strip_strings_comments_ts(source)
    opens = cleaned.count("{")
    closes = cleaned.count("}")
    parens_open = cleaned.count("(")
    parens_close = cleaned.count(")")
    bracks_open = cleaned.count("[")
    bracks_close = cleaned.count("]")

    if opens != closes:
        errors.append(
            f"Unbalanced braces: {opens} '{{' vs {closes} '}}' "
            f"(diff={opens - closes}). File is likely truncated mid-block."
        )
    if parens_open != parens_close:
        errors.append(
            f"Unbalanced parens: {parens_open} '(' vs {parens_close} ')'."
        )
    if bracks_open != bracks_close:
        errors.append(
            f"Unbalanced brackets: {bracks_open} '[' vs {bracks_close} ']'."
        )

    if _tsx_looks_truncated(source):
        errors.append(
            "File appears truncated — ends with an open token. "
            "Output the COMPLETE file."
        )

    if is_rn_frontend:
        for needle, msg in _TSX_FORBIDDEN_RN:
            if needle in source:
                errors.append(
                    f"Forbidden pattern `{needle}`: {msg}"
                )

    return ValidationResult(ok=not errors, errors=errors)


# ─────────────────────────── public entry ──────────────────────────────


def validate_generated_file(
    content: str,
    path: str,
    *,
    is_rn_frontend: bool = False,
) -> ValidationResult:
    """Dispatch validator based on file extension."""
    suffix = Path(path).suffix.lower()
    if suffix == ".py":
        return validate_python(content, path=Path(path))
    if suffix in {".ts", ".tsx", ".jsx", ".js", ".mjs"}:
        return validate_typescript(content, path=Path(path), is_rn_frontend=is_rn_frontend)
    # Other languages — pass through (caller may add their own checks)
    return ValidationResult(ok=True)


def validated_generate(
    *,
    initial_prompt: str,
    path: str,
    generate: Callable[[str], str],
    sanitize: Callable[[str], str],
    max_attempts: int = 3,
    is_rn_frontend: bool = False,
    log: Callable[[str], None] | None = None,
) -> tuple[str, ValidationResult]:
    """Generate a file content, validate, retry on failure with specific errors.

    Returns (final_content, final_validation_result). If all attempts fail,
    returns the last attempt's content + the validation result so the caller
    can decide whether to write it anyway or skip.
    """
    log_fn = log or (lambda _m: None)
    prompt = initial_prompt
    last_content = ""
    last_result = ValidationResult(ok=False, errors=["no attempts yet"])

    for attempt in range(1, max_attempts + 1):
        raw = generate(prompt)
        content = sanitize(raw)
        result = validate_generated_file(content, path, is_rn_frontend=is_rn_frontend)
        if result.ok:
            return content, result
        last_content = content
        last_result = result
        log_fn(
            f"  [validate] {path} attempt {attempt}/{max_attempts} failed: "
            f"{result.errors[0][:80]}"
        )
        # Build retry prompt — append specific defects from THIS attempt
        prompt = initial_prompt + result.to_retry_prompt_section()

    log_fn(
        f"  [validate] {path} exhausted {max_attempts} attempts; "
        f"writing best-effort content with {len(last_result.errors)} defects remaining"
    )
    return last_content, last_result


__all__ = [
    "ValidationResult",
    "validate_generated_file",
    "validate_python",
    "validate_typescript",
    "validated_generate",
]
