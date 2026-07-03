import ast as _ast_mod
import atexit
import builtins as _builtins_mod
import io as _io_mod
import itertools
import json
import keyword as _keyword_mod
import os
import subprocess
import sys
import threading
import tokenize as _tokenize_mod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel

from abstra_internals.settings import Settings


def _path_to_uri(path) -> str:
    return Path(path).as_uri()


def _uri_to_path(uri: str) -> str:
    """Filesystem path from a ``file://`` URI, cross-platform.

    Stripping the ``file://`` prefix is WRONG on Windows: ``file:///C:/x`` would
    become ``/C:/x``. url2pathname maps it back to ``C:\\x`` (and to ``/x`` on
    POSIX)."""
    from urllib.parse import unquote, urlparse
    from urllib.request import url2pathname

    return url2pathname(unquote(urlparse(uri).path))


class Position(BaseModel):
    line: int = 0
    character: int = 0


class TextDocumentContext(BaseModel):
    code: str
    position: Position = Position()


# Pyrefly's semantic token legend (must match server's encoding order)
SEMANTIC_TOKEN_TYPES = [
    "namespace",
    "type",
    "class",
    "enum",
    "interface",
    "struct",
    "typeParameter",
    "parameter",
    "variable",
    "property",
    "enumMember",
    "event",
    "function",
    "method",
    "macro",
    "keyword",
    "modifier",
    "comment",
    "string",
    "number",
    "regexp",
    "operator",
    "decorator",
]

SEMANTIC_TOKEN_MODIFIERS = [
    "declaration",
    "definition",
    "readonly",
    "static",
    "deprecated",
    "abstract",
    "async",
    "modification",
    "documentation",
    "defaultLibrary",
]


# Map token type names to indices
_TT = {t: i for i, t in enumerate(SEMANTIC_TOKEN_TYPES)}
_TM = {m: (1 << i) for i, m in enumerate(SEMANTIC_TOKEN_MODIFIERS)}

_PYTHON_KEYWORDS = set(_keyword_mod.kwlist) | {"True", "False", "None"}
_BUILTIN_FUNCS = {
    n for n in dir(_builtins_mod) if callable(getattr(_builtins_mod, n, None))
}
_BUILTIN_TYPES = {
    "int",
    "float",
    "str",
    "bool",
    "bytes",
    "list",
    "dict",
    "set",
    "tuple",
    "frozenset",
    "complex",
    "range",
    "type",
    "object",
    "bytearray",
    "memoryview",
    "slice",
    "super",
    "property",
    "classmethod",
    "staticmethod",
}


def _tokenize_syntax_tokens(code: str) -> List[tuple]:
    """Generate semantic tokens using Python's tokenize + ast modules.

    Combines tokenize (strings, numbers, comments, keywords, operators)
    with ast (functions, methods, classes, parameters, decorators,
    type hints, builtins, constants).

    Returns list of (line, col, length, type_index, modifiers) tuples (0-based).
    """
    tokens: List[tuple] = []
    code_lines = code.split("\n")

    # ── Phase 1: tokenize (lexical tokens) ────────────────────────

    string_types = {_tokenize_mod.STRING}
    for attr in ("FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END"):
        val = getattr(_tokenize_mod, attr, None)
        if val is not None:
            string_types.add(val)

    try:
        raw_tokens = list(
            _tokenize_mod.generate_tokens(_io_mod.StringIO(code).readline)
        )
    except _tokenize_mod.TokenError:
        raw_tokens = []

    for tok in raw_tokens:
        tok_type = tok.type
        start_line, start_col = tok.start
        end_line, end_col = tok.end

        if tok_type in string_types:
            type_idx = _TT["string"]
        elif tok_type == _tokenize_mod.NUMBER:
            type_idx = _TT["number"]
        elif tok_type == _tokenize_mod.COMMENT:
            type_idx = _TT["comment"]
        elif tok_type == _tokenize_mod.NAME and tok.string in _PYTHON_KEYWORDS:
            type_idx = _TT["keyword"]
        elif tok_type == _tokenize_mod.OP:
            type_idx = _TT["operator"]
        else:
            continue

        line0 = start_line - 1

        if start_line == end_line:
            length = end_col - start_col
            if length > 0:
                tokens.append((line0, start_col, length, type_idx, 0))
        else:
            for ln in range(start_line - 1, end_line):
                if ln == start_line - 1:
                    col = start_col
                    line_len = (
                        len(code_lines[ln]) - start_col if ln < len(code_lines) else 0
                    )
                elif ln == end_line - 1:
                    col = 0
                    line_len = end_col
                else:
                    col = 0
                    line_len = len(code_lines[ln]) if ln < len(code_lines) else 0
                if line_len > 0:
                    tokens.append((ln, col, line_len, type_idx, 0))

    # ── Phase 2: ast (semantic classifications) ───────────────────

    try:
        tree = _ast_mod.parse(code)
    except SyntaxError:
        return tokens

    class _Classifier(_ast_mod.NodeVisitor):
        def __init__(self):
            self.items: List[tuple] = []
            self._in_class = False

        def _add(self, node, name: str, tt: int, tm: int = 0):
            self.items.append((node.lineno - 1, node.col_offset, len(name), tt, tm))

        def visit_ClassDef(self, node):
            # 'class MyClass' — classify the name after 'class '
            self.items.append(
                (
                    node.lineno - 1,
                    node.col_offset + 6,
                    len(node.name),
                    _TT["class"],
                    _TM["definition"],
                )
            )
            for dec in node.decorator_list:
                if isinstance(dec, _ast_mod.Name):
                    self.items.append(
                        (
                            dec.lineno - 1,
                            dec.col_offset,
                            len(dec.id),
                            _TT["decorator"],
                            0,
                        )
                    )
            old = self._in_class
            self._in_class = True
            self.generic_visit(node)
            self._in_class = old

        def visit_FunctionDef(self, node):
            self._visit_func(node, is_async=False)

        def visit_AsyncFunctionDef(self, node):
            self._visit_func(node, is_async=True)

        def _visit_func(self, node, is_async: bool):
            tt = _TT["method"] if self._in_class else _TT["function"]
            kw_len = 10 if is_async else 4  # 'async def ' or 'def '
            self.items.append(
                (
                    node.lineno - 1,
                    node.col_offset + kw_len,
                    len(node.name),
                    tt,
                    _TM["definition"],
                )
            )

            for dec in node.decorator_list:
                if isinstance(dec, _ast_mod.Name):
                    self.items.append(
                        (
                            dec.lineno - 1,
                            dec.col_offset,
                            len(dec.id),
                            _TT["decorator"],
                            0,
                        )
                    )

            all_args = node.args.args + node.args.posonlyargs + node.args.kwonlyargs
            for arg in all_args:
                self.items.append(
                    (
                        arg.lineno - 1,
                        arg.col_offset,
                        len(arg.arg),
                        _TT["parameter"],
                        0,
                    )
                )
                if arg.annotation and isinstance(arg.annotation, _ast_mod.Name):
                    self.items.append(
                        (
                            arg.annotation.lineno - 1,
                            arg.annotation.col_offset,
                            len(arg.annotation.id),
                            _TT["type"],
                            0,
                        )
                    )
            for extra in (node.args.vararg, node.args.kwarg):
                if extra:
                    self.items.append(
                        (
                            extra.lineno - 1,
                            extra.col_offset,
                            len(extra.arg),
                            _TT["parameter"],
                            0,
                        )
                    )

            if node.returns and isinstance(node.returns, _ast_mod.Name):
                self.items.append(
                    (
                        node.returns.lineno - 1,
                        node.returns.col_offset,
                        len(node.returns.id),
                        _TT["type"],
                        0,
                    )
                )

            self.generic_visit(node)

        def visit_Name(self, node):
            name = node.id
            if name in _PYTHON_KEYWORDS:
                pass  # handled by tokenize
            elif name in _BUILTIN_TYPES:
                self.items.append(
                    (
                        node.lineno - 1,
                        node.col_offset,
                        len(name),
                        _TT["type"],
                        _TM["defaultLibrary"],
                    )
                )
            elif name in _BUILTIN_FUNCS:
                self.items.append(
                    (
                        node.lineno - 1,
                        node.col_offset,
                        len(name),
                        _TT["function"],
                        _TM["defaultLibrary"],
                    )
                )
            elif name.isupper() and len(name) > 1:
                self.items.append(
                    (
                        node.lineno - 1,
                        node.col_offset,
                        len(name),
                        _TT["variable"],
                        _TM["readonly"],
                    )
                )
            self.generic_visit(node)

        def visit_Attribute(self, node):
            if (
                isinstance(node.value, _ast_mod.Name)
                and node.value.id == "self"
                and node.end_lineno is not None
                and node.end_col_offset is not None
            ):
                self.items.append(
                    (
                        node.end_lineno - 1,
                        node.end_col_offset - len(node.attr),
                        len(node.attr),
                        _TT["property"],
                        0,
                    )
                )
            self.generic_visit(node)

    classifier = _Classifier()
    classifier.visit(tree)
    tokens.extend(classifier.items)

    return tokens


def _merge_and_encode_tokens(
    syntax_tokens: List[tuple], lsp_tokens: Optional[dict]
) -> List[int]:
    """Merge tokenize-based syntax tokens with pyrefly's semantic tokens.

    Pyrefly tokens take priority (they have richer semantic info).
    Returns the flat LSP-encoded array.
    """
    # Decode pyrefly tokens into (line, col, length, type, mods) tuples
    pyrefly_tokens = []
    if lsp_tokens and "data" in lsp_tokens:
        data = lsp_tokens["data"]
        line = 0
        col = 0
        for i in range(0, len(data), 5):
            dl, dc, length, tt, tm = data[i : i + 5]
            line += dl
            col = col + dc if dl == 0 else dc
            pyrefly_tokens.append((line, col, length, tt, tm))

    # Build a set of (line, col) positions covered by pyrefly
    pyrefly_positions = set()
    for line, col, length, _, _ in pyrefly_tokens:
        for c in range(col, col + length):
            pyrefly_positions.add((line, c))

    # Filter syntax tokens: skip positions already covered by pyrefly
    filtered_syntax = []
    for line, col, length, tt, tm in syntax_tokens:
        if (line, col) not in pyrefly_positions:
            filtered_syntax.append((line, col, length, tt, tm))

    # Merge and sort by position
    all_tokens = sorted(filtered_syntax + pyrefly_tokens, key=lambda t: (t[0], t[1]))

    # Encode as LSP relative format
    encoded = []
    prev_line = 0
    prev_col = 0
    for line, col, length, tt, tm in all_tokens:
        dl = line - prev_line
        dc = col - prev_col if dl == 0 else col
        encoded.extend([dl, dc, length, tt, tm])
        prev_line = line
        prev_col = col

    return encoded


class PyreflyLSP:
    """Manages a pyrefly Language Server Protocol subprocess."""

    def __init__(self):
        self._process: Optional[subprocess.Popen] = None
        self._lock = threading.Lock()
        self._write_lock = threading.Lock()
        self._op_lock = threading.Lock()
        self._initialized = threading.Event()
        self._request_id = itertools.count(1)
        self._pending: Dict[int, threading.Event] = {}
        self._results: Dict[int, Any] = {}
        self._diagnostics: Dict[str, list] = {}
        self._diagnostics_events: Dict[str, threading.Event] = {}
        self._doc_version = 0
        self._doc_open = False
        self._last_code: Optional[str] = None
        self._root_path: Optional[str] = None
        self._temp_path: Optional[str] = None
        self._config_path: Optional[str] = None
        self._uri: Optional[str] = None
        self._root_uri: Optional[str] = None
        atexit.register(self._cleanup)

    def _cleanup(self):
        self.shutdown()
        # Clean up buffer file from project root (config stays in .abstra/)
        if self._temp_path:
            try:
                os.unlink(self._temp_path)
            except OSError:
                pass

    # Pyrefly strict config — must be in project root for LSP to find it.
    # project_includes ensures the buffer file is part of the project.
    _PYREFLY_CONFIG = """\
# Managed by Abstra — do not edit
project_includes = [".pyrefly_buffer.py", "**/*.py"]

# All rules promoted to error — maximum strictness
[errors]
bad-argument-type = "error"
bad-assignment = "error"
bad-function-definition = "error"
bad-index = "error"
bad-override = "error"
bad-return = "error"
bad-typed-dict-key = "error"
missing-argument = "error"
missing-attribute = "error"
missing-module-attribute = "error"
no-matching-overload = "error"
not-a-type = "error"
not-callable = "error"
not-iterable = "error"
unbound-name = "error"
unexpected-keyword = "error"
unknown-name = "error"
unsupported-operation = "error"
"""

    def _resolve_paths(self):
        if self._root_path is None:
            self._root_path = os.getcwd()
            self._temp_path = os.path.join(self._root_path, ".pyrefly_buffer.py")
            self._config_path = os.path.join(self._root_path, "pyrefly.toml")
            # Create empty buffer file so pyrefly can find it
            try:
                open(self._temp_path, "w", encoding="utf-8").close()
            except OSError:
                pass
            # Write strict config (always overwrite — managed by Abstra)
            try:
                with open(self._config_path, "w", encoding="utf-8") as f:
                    f.write(self._PYREFLY_CONFIG)
            except OSError:
                pass
            self._uri = _path_to_uri(self._temp_path)
            self._root_uri = _path_to_uri(self._root_path)

    def _ensure_running(self):
        self._resolve_paths()
        if self._process is None or self._process.poll() is not None:
            with self._lock:
                if self._process is None or self._process.poll() is not None:
                    self._start()
        if not self._initialized.wait(timeout=10.0):
            return

    def _start(self):
        self._initialized.clear()
        self._process = subprocess.Popen(
            [sys.executable, "-m", "pyrefly", "lsp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        self._doc_open = False
        self._doc_version = 0
        reader = threading.Thread(target=self._read_loop, daemon=True)
        reader.start()
        self._do_initialize()

    def _read_loop(self):
        assert self._process is not None
        stdout = self._process.stdout
        assert stdout is not None
        while True:
            try:
                header = b""
                while b"\r\n\r\n" not in header:
                    byte = stdout.read(1)
                    if not byte:
                        return
                    header += byte

                content_length = int(
                    header.decode().split("Content-Length: ")[1].split("\r\n")[0]
                )
                body = stdout.read(content_length)
                msg = json.loads(body)

                if "id" in msg and "method" not in msg:
                    rid = msg["id"]
                    if rid in self._pending:
                        self._results[rid] = msg
                        self._pending[rid].set()
                    else:
                        # Late response after timeout — discard to prevent leak
                        pass
                elif "id" in msg and "method" in msg:
                    # Server-initiated request (e.g. client/registerCapability).
                    # Ack with null so pyrefly doesn't block waiting on us.
                    try:
                        self._send({"jsonrpc": "2.0", "id": msg["id"], "result": None})
                    except Exception:
                        pass
                elif msg.get("method") == "textDocument/publishDiagnostics":
                    params = msg.get("params", {})
                    uri = params.get("uri", "")
                    self._diagnostics[uri] = params.get("diagnostics", [])
                    event = self._diagnostics_events.get(uri)
                    if event:
                        event.set()
            except Exception:
                if self._process and self._process.poll() is not None:
                    return

    def _send(self, msg: dict):
        assert self._process is not None and self._process.stdin is not None
        data = json.dumps(msg).encode()
        header = f"Content-Length: {len(data)}\r\n\r\n".encode()
        with self._write_lock:
            self._process.stdin.write(header + data)
            self._process.stdin.flush()

    def _request(self, method: str, params: dict, timeout: float = 5.0) -> Any:
        rid = next(self._request_id)

        event = threading.Event()
        self._pending[rid] = event

        self._send({"jsonrpc": "2.0", "id": rid, "method": method, "params": params})

        if not event.wait(timeout):
            self._pending.pop(rid, None)
            return None

        self._pending.pop(rid, None)
        result = self._results.pop(rid, None)
        if result and "result" in result:
            return result["result"]
        return None

    def _notify(self, method: str, params: dict):
        self._send({"jsonrpc": "2.0", "method": method, "params": params})

    def _do_initialize(self):
        self._request(
            "initialize",
            {
                "processId": os.getpid(),
                "capabilities": {
                    "textDocument": {
                        "completion": {"completionItem": {"snippetSupport": False}},
                        "hover": {},
                        "publishDiagnostics": {},
                        "semanticTokens": {
                            "requests": {"full": True},
                            "tokenTypes": SEMANTIC_TOKEN_TYPES,
                            "tokenModifiers": SEMANTIC_TOKEN_MODIFIERS,
                            "formats": ["relative"],
                            "augmentsSyntaxTokens": True,
                        },
                    }
                },
                "rootUri": self._root_uri,
            },
        )
        self._notify("initialized", {})
        self._initialized.set()

    def _assert_paths(self) -> tuple:
        """Assert that paths have been resolved. Returns (uri, temp_path, root_path)."""
        assert self._uri is not None, "_resolve_paths not called"
        assert self._temp_path is not None
        assert self._root_path is not None
        return self._uri, self._temp_path, self._root_path

    def _sync_document(self, code: str):
        uri, temp_path, _ = self._assert_paths()
        if not self._doc_open:
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(code)
            self._doc_version += 1
            self._diagnostics_events[uri] = threading.Event()
            self._notify(
                "textDocument/didOpen",
                {
                    "textDocument": {
                        "uri": uri,
                        "languageId": "python",
                        "version": self._doc_version,
                        "text": code,
                    }
                },
            )
            self._doc_open = True
            self._last_code = code
        elif code != self._last_code:
            self._doc_version += 1
            self._diagnostics_events[uri] = threading.Event()
            self._notify(
                "textDocument/didChange",
                {
                    "textDocument": {
                        "uri": uri,
                        "version": self._doc_version,
                    },
                    "contentChanges": [{"text": code}],
                },
            )
            self._last_code = code

    def _resolve_uri(self, uri: str) -> str:
        self._assert_paths()
        if uri == self._uri:
            return "self"
        prefix = (self._root_uri or "") + "/"
        if uri.startswith(prefix):
            relative = uri[len(prefix) :]
            # Pyrefly extracts bundled typeshed in CWD — treat as external
            if "pyrefly_bundled_typeshed" in relative:
                return uri
            return "project:" + relative
        return uri

    # ── Public LSP methods ────────────────────────────────────────

    def get_completions(self, code: str, line: int, character: int) -> list:
        self._ensure_running()
        with self._op_lock:
            self._sync_document(code)
            result = self._request(
                "textDocument/completion",
                {
                    "textDocument": {"uri": self._uri},
                    "position": {"line": line, "character": character},
                },
            )
        if result is None:
            return []
        if isinstance(result, list):
            return result
        return result.get("items", [])

    def get_hover(self, code: str, line: int, character: int) -> Optional[dict]:
        self._ensure_running()
        with self._op_lock:
            self._sync_document(code)
            return self._request(
                "textDocument/hover",
                {
                    "textDocument": {"uri": self._uri},
                    "position": {"line": line, "character": character},
                },
            )

    def get_diagnostics(self, code: str, timeout: float = 5.0) -> list:
        """Sync document and wait for fresh diagnostics from Pyrefly."""
        diagnostics, _ = self.get_diagnostics_checked(code, timeout)
        return diagnostics

    def get_diagnostics_checked(
        self, code: str, timeout: float = 5.0
    ) -> Tuple[list, bool]:
        """Like get_diagnostics, but also reports whether Pyrefly answered.

        ``responded`` is False when the publishDiagnostics notification never
        arrived within ``timeout`` (server dead, unreachable or mute) — so a
        caller looping over many files can stop hammering a server that will
        only ever cost a full timeout per file."""
        self._ensure_running()
        uri = self._assert_paths()[0]
        with self._op_lock:
            self._sync_document(code)
            event = self._diagnostics_events.get(uri)
        responded = True
        if event:
            responded = event.wait(timeout)
        return self._diagnostics.get(uri, []), responded

    def get_cached_diagnostics(self) -> list:
        """Return last-known diagnostics without syncing or waiting.

        Use this when diagnostics are a side-effect of another operation
        (completion, hover, etc.) that already synced the document.
        """
        if self._uri is None:
            return []
        return self._diagnostics.get(self._uri, [])

    def get_definition(self, code: str, line: int, character: int) -> Optional[dict]:
        self._ensure_running()
        with self._op_lock:
            self._sync_document(code)
            result = self._request(
                "textDocument/definition",
                {
                    "textDocument": {"uri": self._uri},
                    "position": {"line": line, "character": character},
                },
            )
        if result is None:
            return None
        if isinstance(result, list):
            if not result:
                return None
            location = result[0]
        else:
            location = result
        location["uri"] = self._resolve_uri(location.get("uri", ""))
        return location

    def get_references(self, code: str, line: int, character: int) -> list:
        self._ensure_running()
        with self._op_lock:
            self._sync_document(code)
            result = self._request(
                "textDocument/references",
                {
                    "textDocument": {"uri": self._uri},
                    "position": {"line": line, "character": character},
                    "context": {"includeDeclaration": True},
                },
            )
        if not result:
            return []
        for loc in result:
            loc["uri"] = self._resolve_uri(loc.get("uri", ""))
        return result

    def get_document_highlights(self, code: str, line: int, character: int) -> list:
        self._ensure_running()
        with self._op_lock:
            self._sync_document(code)
            result = self._request(
                "textDocument/documentHighlight",
                {
                    "textDocument": {"uri": self._uri},
                    "position": {"line": line, "character": character},
                },
            )
        return result or []

    def get_signature_help(
        self, code: str, line: int, character: int
    ) -> Optional[dict]:
        self._ensure_running()
        with self._op_lock:
            self._sync_document(code)
            return self._request(
                "textDocument/signatureHelp",
                {
                    "textDocument": {"uri": self._uri},
                    "position": {"line": line, "character": character},
                },
            )

    def get_rename_edits(
        self, code: str, line: int, character: int, new_name: str
    ) -> Optional[dict]:
        self._ensure_running()
        with self._op_lock:
            self._sync_document(code)
            return self._request(
                "textDocument/rename",
                {
                    "textDocument": {"uri": self._uri},
                    "position": {"line": line, "character": character},
                    "newName": new_name,
                },
            )

    def get_semantic_tokens(self, code: str) -> Optional[dict]:
        self._ensure_running()
        with self._op_lock:
            self._sync_document(code)
            return self._request(
                "textDocument/semanticTokens/full",
                {"textDocument": {"uri": self._assert_paths()[0]}},
            )

    def notify_file_changed(self, abs_path: str, change_type: int = 2) -> None:
        # LSP FileChangeType: 1=Created, 2=Changed, 3=Deleted.
        # Skip if the daemon isn't up yet — it'll read fresh state on next start.
        if self._process is None or self._process.poll() is not None:
            return
        if not self._initialized.is_set():
            return
        if abs_path == self._temp_path or abs_path == self._config_path:
            return
        try:
            self._notify(
                "workspace/didChangeWatchedFiles",
                {"changes": [{"uri": _path_to_uri(abs_path), "type": change_type}]},
            )
        except Exception:
            pass

    def read_external_file(self, file_uri: str) -> Optional[str]:
        """Read file content from a file:// URI (for viewing external definitions).

        Only allows reading .py/.pyi files to prevent arbitrary file access.
        """
        if not file_uri.startswith("file://"):
            return None
        file_path = os.path.realpath(_uri_to_path(file_uri))
        if not file_path.endswith((".py", ".pyi")):
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except (OSError, UnicodeDecodeError):
            return None

    def shutdown(self):
        if self._process and self._process.poll() is None:
            try:
                self._request("shutdown", {}, timeout=5.0)
                self._notify("exit", {})
                self._process.wait(timeout=5.0)
            except Exception:
                self._process.kill()


_lsp = PyreflyLSP()


# ── Public API ────────────────────────────────────────────────────


def get_status() -> dict:
    proc = _lsp._process
    alive = proc is not None and proc.poll() is None
    return {
        "alive": alive,
        "poll": proc.poll() if proc else "no_process",
        "initialized": _lsp._initialized.is_set(),
        "temp_path": _lsp._temp_path,
        "root_uri": _lsp._root_uri,
        "doc_version": _lsp._doc_version,
        "doc_open": _lsp._doc_open,
    }


def get_completions(code: str, line: int, character: int) -> list:
    try:
        return _lsp.get_completions(code, line, character)
    except Exception:
        return []


def get_hover(code: str, line: int, character: int) -> Optional[dict]:
    try:
        return _lsp.get_hover(code, line, character)
    except Exception:
        return None


def get_diagnostics(code: str) -> list:
    try:
        return _lsp.get_diagnostics(code)
    except Exception:
        return []


def get_diagnostics_checked(code: str) -> Tuple[List[dict], bool]:
    """Module wrapper: returns (diagnostics, responded). ``responded`` is False
    when Pyrefly did not answer within the timeout (dead/unreachable/mute)."""
    try:
        return _lsp.get_diagnostics_checked(code)
    except Exception:
        return [], False


def get_cached_diagnostics() -> list:
    try:
        return _lsp.get_cached_diagnostics()
    except Exception:
        return []


def get_definition(code: str, line: int, character: int) -> Optional[dict]:
    try:
        return _lsp.get_definition(code, line, character)
    except Exception:
        return None


def get_references(code: str, line: int, character: int) -> list:
    try:
        return _lsp.get_references(code, line, character)
    except Exception:
        return []


def get_document_highlights(code: str, line: int, character: int) -> list:
    try:
        return _lsp.get_document_highlights(code, line, character)
    except Exception:
        return []


def get_signature_help(code: str, line: int, character: int) -> Optional[dict]:
    try:
        return _lsp.get_signature_help(code, line, character)
    except Exception:
        return None


def get_rename_edits(
    code: str, line: int, character: int, new_name: str
) -> Optional[dict]:
    try:
        return _lsp.get_rename_edits(code, line, character, new_name)
    except Exception:
        return None


def get_semantic_tokens(code: str) -> Optional[dict]:
    try:
        syntax_tokens = _tokenize_syntax_tokens(code)
        lsp_tokens = _lsp.get_semantic_tokens(code)
        merged = _merge_and_encode_tokens(syntax_tokens, lsp_tokens)
        return {"data": merged}
    except Exception:
        # Fallback to syntax-only tokens if LSP fails
        try:
            syntax_tokens = _tokenize_syntax_tokens(code)
            encoded = _merge_and_encode_tokens(syntax_tokens, None)
            return {"data": encoded}
        except Exception:
            return None


def read_external_file(file_uri: str) -> Optional[str]:
    try:
        return _lsp.read_external_file(file_uri)
    except Exception:
        return None


def notify_file_changed(path, change_type: int = 2) -> None:
    # change_type follows LSP FileChangeType: 1=Created, 2=Changed, 3=Deleted.
    try:
        abs_path = os.path.abspath(os.fspath(path))
        _lsp.notify_file_changed(abs_path, change_type)
    except Exception:
        pass


_TYPE_DISCIPLINE_HINT = (
    "Do not silence these errors with `Any`, `cast(Any, ...)`, untyped "
    "`list`/`dict`, or `# type: ignore`. Import the correct type from "
    "`abstra.types` (or the specific submodule like `abstra.forms`, "
    "`abstra.tables`, `abstra.tasks`, `abstra.hooks`, `abstra.connectors`, "
    "`abstra.ai`, `abstra.pages`) and fix the root cause."
)


def analyze_python_syntax(code: str) -> dict:
    """
    Analyze Python code for syntax and type errors using Pyrefly.

    Args:
        code (str): Python source code to analyze.

    Returns:
        dict with keys:
            - diagnostics (List[dict]): LSP Diagnostic objects with
                range/severity/message/source. Severities: 1=Error, 2=Warning,
                3=Information, 4=Hint.
            - error_count (int): Number of severity=1 diagnostics.
            - warning_count (int): Number of severity=2 diagnostics.
            - type_discipline_hint (str | None): Short reminder pointing at the
                Abstra SDK types. Set whenever there is at least one error.

    Copywritings:
        Analyze Python code for syntax and type errors
        Analyzing Python code for errors...
    """
    diagnostics = get_diagnostics(code)
    error_count = sum(1 for d in diagnostics if d.get("severity") == 1)
    warning_count = sum(1 for d in diagnostics if d.get("severity") == 2)
    return {
        "diagnostics": diagnostics,
        "error_count": error_count,
        "warning_count": warning_count,
        "type_discipline_hint": _TYPE_DISCIPLINE_HINT if error_count > 0 else None,
    }


def analyze_python_syntax_file(file: str) -> Optional[dict]:
    """
    Analyze a Python file for syntax and type errors using Pyrefly.

    Args:
        file (str): Relative path to the Python file from the project root
            directory. Should include the `.py` extension.

    Copywritings:
        Analyze a Python file for syntax and type errors
        Analyzing Python file for errors...
    """
    file_path = Settings.root_path.joinpath(file)
    if not file_path.is_file():
        return None
    code = file_path.read_text(encoding="utf-8")
    return analyze_python_syntax(code)
