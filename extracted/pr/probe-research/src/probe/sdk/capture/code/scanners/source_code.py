"""The credential rules a captured file is judged by: the shared rules read through SecretScanner, then code context --
placeholders, code-shaped values, UTF-16 views, notebook cells."""

from __future__ import annotations
import json
import re
import time
from collections import Counter
from typing import Any

from ..scanner import ScanDepth, get_scanner

#: Source files, where `name = <expression>` is ordinary code. The scanner's
#: key-name tier (``anchored-secret``) exists for transcripts, where a false
#: positive costs a mangled string; here it costs the whole file. So in these
#: files that ONE rule's hit is dropped when its value is unquoted AND its first
#: word is code (see ``_code_shaped``) -- `token = tokens[0]`, `getpass.getpass()`,
#: `contextvars.Token` -- while `# api_key: a8f5...` in a comment still counts.
#: Notebooks are NOT here: `%env KEY=...` lines and printed outputs are data.
_SOURCE_SUFFIXES = (
    ".py", ".pyi", ".pyx", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx",
    ".go", ".rs", ".java", ".kt", ".scala", ".c", ".h", ".cc", ".cpp", ".cxx", ".hpp",
    ".cu", ".cuh", ".swift", ".rb", ".php", ".lua", ".jl", ".r", ".cs",
)
#: The shared rules, picked once: every rule with decoding, or the quick check past FULL_SCAN_MAX_BYTES.
_FULL_SCANNER = get_scanner(ScanDepth.FULL)
_QUICK_SCANNER = get_scanner(ScanDepth.QUICK)
_KEY_NAME_RULE = "anchored-secret"
#: A field name that marks its value as a credential, matched anywhere in the
#: KEY of a `key = value` / `key: value` pair (camelCase included). The scanner
#: finds the hit; this decides whether the separator in front of it really
#: belongs to such a key, or to another one on the same line (`help=`, `noqa:`).
_ANCHOR_WORD = re.compile(
    r"(?i)secret|passw(?:or)?d|pwd|api[_ \-]?key|access[_ \-]?key|private[_ \-]?key"
    r"|token|credential|bearer|encryption[_ \-]?key|signing[_ \-]?key|(?-i:[A-Z0-9]_KEY)(?![A-Za-z0-9])"
    # The scanner's vendor-owned key names (`azure_openai_key`, `openaiKey`); it
    # has already checked that the name says who issued the key.
    r"|(?-i:[a-z0-9]_key|[A-Za-z0-9]Key)(?![A-Za-z0-9])"
)
#: `key` then `:`/`=` (and an opening quote) at the end of the text before a
#: value. A `<`, `>`, `!` or `=` in front of the `=` makes it a comparison.
_SEPARATOR_TAIL = re.compile(r"(?P<op>[<>!=]?)(?P<sep>[:=])\s*[\"']?\s*$")
_KEY_SPLIT = re.compile(r"[,;(){}\[\]\"'`#?&<>|]")
#: A value that is a template slot, not a value: `{user}` (f-string, JSX),
#: `${VAR}`, `$2::uuid` (SQL bind), `$db_password` (a lower-case variable, in
#: letters and `_` only, like the scanner's `_SLOT`), `%s`, `%(name)s`,
#: `<TOKEN>`, `***`, `...`.
_PLACEHOLDER = re.compile(
    r"\{[^{}]*\}|\$\{[^{}]*\}|\$\d+(?:::\w+)?|\$[A-Z_][A-Z0-9_]*|\$[a-z_][A-Za-z_]*|%s|%\(\w+\)s"
    r"|<[^<>]*>|\*{3,}|\.{3}|:[A-Za-z_]\w*"
)
#: The password part of `scheme://user:PASSWORD@` when it is a slot or a word
#: that names what goes there (`https://user:password@host` in a docstring).
_USERINFO_PLACEHOLDER = re.compile(
    r"(?i)" + _PLACEHOLDER.pattern + r"|pass(?:word)?|passwd|pwd|secret|token|changeme|example|x{3,}"
)
_CREDENTIAL_URI_PASSWORD = re.compile(r"://[^/@\s:]*:(?P<pw>[^/@\s]+)@")
_TYPE_NAMES = frozenset({
    "str", "int", "float", "bool", "bytes", "None", "Any", "Optional", "Union", "Final",
    "ClassVar", "SecretStr", "SecretBytes", "dict", "list", "tuple", "set", "Dict", "List",
    "Tuple", "Set", "Sequence", "Mapping", "object", "type", "Literal",
})
_NAME_ATTR = re.compile(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+(?:\(.*)?")
_CALL_OR_INDEX = re.compile(r"[A-Za-z_][\w.]*[(\[]")
_IDENTIFIER = re.compile(r"[A-Za-z_]\w*")
_HEXISH = re.compile(r"[0-9a-fA-F]{16,}")
#: ` = "literal"` (an assignment, spaced) or `default="literal"` on the rest of
#: a line -- not `==`, and not another keyword argument (`description="..."`).
_DEFAULT_LITERAL = re.compile(r"(?:(?<=\s)=(?!=)|\bdefault\s*=)\s*[rbuRBU]?([\"'])(?P<lit>[^\"'\n]+)\1")
_UTF16_BOMS = (b"\xff\xfe", b"\xfe\xff")
#: Punctuation that ends a value without being part of it (a closing quote or
#: bracket, a sentence's period). Not `=`: that is base64 padding.
_TRAILING = ".,;:)]}\"'`"
#: How far past (``_VERDICT_REACH``) and before (``_VERDICT_LOOKBACK``) one
#: key-name hit `_anchored_verdict` and the re-reads in `_counted_rules` look.
#: The scanner puts a key within 24 characters of its separator and a typed
#: field's literal within ~40 more, so these hold all a verdict reads. Reading
#: the whole line made a one-line file quadratic: a 150 KB minified JSON of
#: `"password": ...` rows took 17 s, a 1 MB line of `azure_openai_key=...`
#: 550 s. A line cut at the reach reads as going on; a key cut at the lookback
#: still ends in its anchor word.
_VERDICT_REACH = 1024
_VERDICT_LOOKBACK = 256
_FIRST_WORD = re.compile(r"\s*(\S*)")
_WORD_RUN = re.compile(r"\w+")


class _ScanOutOfTime(Exception):
    """A file's content scan ran past its time budget (see FILE_SCAN_BUDGET_SEC)."""


def _check_deadline(deadline: float | None) -> None:
    if deadline is not None and time.monotonic() > deadline:
        raise _ScanOutOfTime


def _is_placeholder(first: str) -> bool:
    """A template slot, with or without the punctuation that closes it
    (`{counter}`, `{counter}}`, `$2::uuid"`)."""
    for candidate in (first, first.rstrip(_TRAILING), first.rstrip(_TRAILING) + "}"):
        if _PLACEHOLDER.fullmatch(candidate.strip("\"'`")):
            return True
    return False


def _code_shaped(first: str, text: str, uses: Any = None) -> bool:
    """Whether the first word of an unquoted value is code, not a literal:
    `name.attr`, `name(`, `name[`, a type name, a lone `#` (a comment follows),
    or a plain identifier that is used elsewhere in the same file. Only the
    FIRST word counts -- the rest of the line (`(rotate monthly)`, `. Ask ops`)
    says nothing about the value -- and a trailing `=` is base64 padding.
    ``uses(word)`` counts a word's whole-word uses in ``text`` (`_counted_rules`
    counts every word once instead of searching the file once per hit)."""
    if first == "#":
        return True
    word = first.rstrip(_TRAILING)
    if not word:
        return True
    if word in _TYPE_NAMES or _NAME_ATTR.fullmatch(word) or _CALL_OR_INDEX.match(word):
        return True
    if _IDENTIFIER.fullmatch(word) and not _HEXISH.fullmatch(word):
        if uses is not None:
            return uses(word) >= 2
        return len(re.findall(r"(?<!\w)" + re.escape(word) + r"(?!\w)", text)) >= 2
    return False


def _line_end(text: str, at: int) -> int:
    """The end of ``at``'s line, or ``at + _VERDICT_REACH`` if that comes first."""
    reach = min(len(text), at + _VERDICT_REACH)
    newline = text.find("\n", at, reach)
    return reach if newline < 0 else newline


def _anchored_verdict(text: str, f: Any, source: bool, uses: Any = None) -> tuple[bool, str | None]:
    """``(counts, key)`` for one key-name hit. ``key`` is set when the hit is
    dropped as CODE under a credential key, so the caller can look further along
    the line (a typed field: `password: str = "..."`). Reads `_VERDICT_LOOKBACK`
    before the hit and `_VERDICT_REACH` after it, never the whole line."""
    floor = max(0, f.start - _VERDICT_LOOKBACK)
    newline = text.rfind("\n", floor, f.start)
    line_start = floor if newline < 0 else newline + 1
    line_end = _line_end(text, f.start)
    before = text[line_start:f.start]
    if not before.strip() and (newline >= 0 or floor == 0):
        return False, None  # the value is on the NEXT line (YAML `token:` then a block)
    # The separator and what follows it end `before`: 64 characters hold them
    # (more whitespace than that and the hit counts, below).
    tail = _SEPARATOR_TAIL.search(before, max(0, len(before) - 64))
    if tail is None:
        return True, None  # cannot tell what it belongs to: count it
    if tail.group("op"):
        return False, None  # `<=`, `>=`, `!=`, `==`: a comparison
    key = _KEY_SPLIT.split(before[: tail.start()].rstrip(" \t\"'`]"))[-1].strip()
    if not _ANCHOR_WORD.search(key):
        # A `default=` belongs to whatever the line declares: an option
        # (`add_argument("--api-key", default=...)`), a lookup
        # (`os.getenv("WANDB_API_KEY", default=...)`) or a typed field
        # (`api_key: str = Field(default=...)`).
        if key.lower() != "default" or not _ANCHOR_WORD.search(before[: tail.start()]):
            return False, None  # the separator belongs to another key (`help=`, `noqa:`)
    first = _FIRST_WORD.match(text, f.start, line_end).group(1)
    if _is_placeholder(first):
        return False, None
    if f.start > 0 and text[f.start - 1] in "\"'":
        return True, None  # a quoted literal is never code
    if source and _code_shaped(first, text, uses):
        return False, key
    return True, None


def _vendor_rules(text: str) -> set[str]:
    """Every rule but the key-name one, over ``text`` with the decoding layer."""
    return {
        g.rule for g in _FULL_SCANNER.scan(text)
        if g.rule != _KEY_NAME_RULE and not _placeholder_uri(text, g)
    }


def _placeholder_uri(text: str, f: Any) -> bool:
    if f.rule != "credential-uri":
        return False
    m = _CREDENTIAL_URI_PASSWORD.search(text[f.start:f.end])
    return bool(m and _USERINFO_PLACEHOLDER.fullmatch(m.group("pw")))


def _counted_rules(text: str, findings: list, source: bool, deadline: float | None = None) -> set[str]:
    """The rules that keep a file out, after the false-positive rules below.

    - A `scheme://user:PASSWORD@` whose password is a slot (`{password}`,
      `<TOKEN>`, `$PW`) or a placeholder word is a template, not a credential.
    - A key-name hit counts unless: its value starts on the next line; its
      separator is a comparison or belongs to a non-credential key on the same
      line (`add_argument("--token", help=...)`, `# noqa:`); its value is a slot
      (`{counter}`, `$2::uuid`); or, in source files, the value's FIRST word is
      code (see ``_code_shaped``). A quoted literal always counts.
    - A dropped span is scanned again with the full rules and decoding, so a
      vendor token the scanner merged into it (it keeps one name for
      overlapping hits) still counts; and a dropped typed field
      (`password: str = "..."`, `password: str = field(default="...")`) is
      re-read as `key = "<the literal later on the line>"`.

    Each hit's work is bounded (`_VERDICT_REACH`), and past ``deadline`` (a
    `time.monotonic()` value) it raises `_ScanOutOfTime`.
    """
    rules: set[str] = set()
    counted: Counter[str] | None = None
    rescanned: dict[str, set[str]] = {}

    def uses(word: str) -> int:
        nonlocal counted
        if counted is None:
            # `(?<!\w)word(?!\w)` for an identifier `word` is exactly a whole
            # `\w+` run equal to it, so one count serves every hit.
            counted = Counter(_WORD_RUN.findall(text))
        return counted[word]

    for f in findings:
        _check_deadline(deadline)
        if _placeholder_uri(text, f):
            continue
        if f.rule != _KEY_NAME_RULE:
            rules.add(f.rule)
            continue
        counts, key = _anchored_verdict(text, f, source, uses)
        if counts:
            rules.add(f.rule)
            continue
        # The scanner's findings do not overlap, so a vendor token merged into
        # this one lies INSIDE its span: the span is what is read again, once
        # per distinct span (a generated file repeats `token = tokens[0]`).
        span = text[f.start:f.end]
        if span not in rescanned:
            rescanned[span] = _vendor_rules(span)
        rules |= rescanned[span]
        if key:
            # From the VALUE's start: the password rule's span can swallow the
            # `=` (`password: str = "..."` -> `str =`).
            line_end = _line_end(text, f.start)
            quoted = text.find('"', f.start, line_end) >= 0 or text.find("'", f.start, line_end) >= 0
            default = _DEFAULT_LITERAL.search(text, f.start, line_end) if quoted else None
            if default:
                synthetic = f'{key} = "{default.group("lit")}"'
                rules |= {g.rule for g in _FULL_SCANNER.scan(synthetic) if not _placeholder_uri(synthetic, g)}
    return rules


def _utf16_codec(raw: bytes | bytearray) -> str | None:
    """``utf-16-le``/``utf-16-be`` when the bytes read as UTF-16 -- a byte-order
    mark, or (no mark, Windows tools often omit it) NUL in most odd or even
    positions of the first 4 KB -- else None."""
    if raw[:2] == b"\xff\xfe":
        return "utf-16-le"
    if raw[:2] == b"\xfe\xff":
        return "utf-16-be"
    head = bytes(raw[:4096])
    if len(head) < 8:
        return None
    even, odd = head[0::2], head[1::2]
    if odd.count(0) >= 0.7 * len(odd) and even.count(0) <= 0.1 * len(even):
        return "utf-16-le"
    if even.count(0) >= 0.7 * len(even) and odd.count(0) <= 0.1 * len(odd):
        return "utf-16-be"
    return None


def _text_views(raw: bytes | bytearray, codec: str | None = None) -> list[tuple[str, bool]]:
    """``[(text, is_text), ...]`` to scan. UTF-8 is read as UTF-8. UTF-16 (a
    byte-order mark, or NUL-interleaved without one) is read as UTF-16, beside
    a latin-1 view in case a binary file only looked like it. Anything else goes
    through the latin-1 view -- one character per byte -- so a plainly written
    token inside a pickle or a stored zip member is still seen."""
    codec = codec or _utf16_codec(raw)
    if codec:
        body = raw[2:] if raw[:2] in _UTF16_BOMS else raw
        return [(bytes(body).decode(codec, "replace"), True), (raw.decode("latin-1"), False)]
    try:
        return [(raw.decode("utf-8"), True)]
    except UnicodeDecodeError:
        return [(raw.decode("latin-1"), False)]


def _notebook_code(raw: bytes | bytearray) -> str | None:
    """The source of a notebook's code cells, JSON-decoded, one cell after
    another; None when ``raw`` is not a notebook with code in it. nbformat 4
    (`cells`, `source`) and 3 (`worksheets`, `input`)."""
    try:
        notebook = json.loads(bytes(raw))
    except (ValueError, RecursionError):  # not JSON (UnicodeDecodeError is a ValueError)
        return None
    if not isinstance(notebook, dict):
        return None
    cells = notebook.get("cells")
    if not isinstance(cells, list):
        sheets = notebook.get("worksheets")
        cells = [
            cell for sheet in sheets if isinstance(sheet, dict) and isinstance(sheet.get("cells"), list)
            for cell in sheet["cells"]
        ] if isinstance(sheets, list) else []
    parts: list[str] = []
    for cell in cells:
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue
        source = cell.get("source", cell.get("input"))
        if isinstance(source, list):
            source = "".join(line for line in source if isinstance(line, str))
        if isinstance(source, str) and source.strip():
            parts.append(source)
    return "\n\n".join(parts) or None


def _notebook_rules(raw: bytes | bytearray, deadline: float | None = None) -> set[str]:
    """Rules found in a notebook's code cells, read as Python source (the
    verdict the same code gets in a `.py` file). The raw JSON is scanned as
    well, by the caller: outputs and `%env` lines are read there."""
    code = _notebook_code(raw)
    if code is None:
        return set()
    findings = _FULL_SCANNER.scan(code)
    _check_deadline(deadline)
    return _counted_rules(code, findings, True, deadline)


def credential_rules(
    raw: bytes | bytearray, name: str, *, deadline: float | None = None
) -> tuple[str, ...]:
    """Rule names (never a matched value) of the credentials in ``raw``; empty
    when it looks clean. ``name`` is the file's basename. Past ``deadline`` (a
    `time.monotonic()` value, checked between hits) it raises
    `_ScanOutOfTime`, and the caller withholds the file.

    The scanner is the shared one (``tap_core.secrets``, through SecretScanner): its full rule set with
    the decoding layer up to FULL_SCAN_MAX_BYTES, the quick check above that,
    then the false-positive rules in ``_counted_rules``. NOT a backstop: the
    server's upload relay inspects every object it stores and records what it
    finds (``artifacts.credential_findings``), but it stores the bytes
    regardless -- so what this check misses IS stored. Known misses: a token
    split across strings or lines; a bare credential with no recognizable shape
    or key name; decoding (base64, escapes) above FULL_SCAN_MAX_BYTES; and the
    scanner residuals listed in agent/TODOS.md (all-letter values under camelCase
    keys, owner-less `*_key` names, URL passwords with `/`). Compressed archives
    are opened separately (``_archive_rules``); a notebook's code cells are read
    again, JSON-decoded, as Python source (``_notebook_rules``).

    A scanner failure is a finding: a file that could not be checked does not
    ship.
    """
    lowered = name.lower()
    code = lowered.endswith(_SOURCE_SUFFIXES)
    rules: set[str] = set()
    try:
        for text, is_text in _text_views(raw):
            if len(raw) <= FULL_SCAN_MAX_BYTES:
                findings = _FULL_SCANNER.scan(text)
            else:
                findings = _QUICK_SCANNER.scan(text)
            _check_deadline(deadline)
            rules |= _counted_rules(text, findings, is_text and code, deadline)
        if lowered.endswith(".ipynb") and len(raw) <= NOTEBOOK_DECODE_MAX_BYTES:
            rules |= _notebook_rules(raw, deadline)
    except _ScanOutOfTime:
        raise
    except Exception:  # noqa: BLE001 -- fail closed: unscanned bytes stay home
        return ("inspection-failed",)
    return tuple(sorted(rules))


def _chunk_rules(chunk: bytes | bytearray, name: str, codec: str | None = None) -> set[str]:
    """One window of a big file: the quick check over a latin-1 view (length-
    preserving, so lowering it is cheap; every rule's shape is ASCII), plus a
    UTF-16 view when the file is UTF-16 (windows stay on even byte offsets)."""
    code = name.lower().endswith(_SOURCE_SUFFIXES)
    views = [(chunk.decode("latin-1"), code)]
    if codec:
        views.insert(0, (bytes(chunk).decode(codec, "replace"), code))
    rules: set[str] = set()
    try:
        for text, source in views:
            rules |= _counted_rules(text, _QUICK_SCANNER.scan(text), source)
    except Exception:  # noqa: BLE001 -- fail closed
        return {"inspection-failed"}
    return rules
from probe.sdk.capture.code.content_gate import FULL_SCAN_MAX_BYTES, NOTEBOOK_DECODE_MAX_BYTES  # noqa: E402 -- pieces need each other; the front door loads this one first
