"""Language Server Protocol integration for codrninja."""

from __future__ import annotations

import json
import os
import queue
import shutil
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import unquote, urlparse


DEFAULT_REQUEST_TIMEOUT = 10.0
DEFAULT_RESTART_BACKOFF = 2.0
MAX_RESTART_BACKOFF = 30.0

SYMBOL_KIND_NAMES = {
    1: "File",
    2: "Module",
    3: "Namespace",
    4: "Package",
    5: "Class",
    6: "Method",
    7: "Property",
    8: "Field",
    9: "Constructor",
    10: "Enum",
    11: "Interface",
    12: "Function",
    13: "Variable",
    14: "Constant",
    15: "String",
    16: "Number",
    17: "Boolean",
    18: "Array",
    19: "Object",
    20: "Key",
    21: "Null",
    22: "EnumMember",
    23: "Struct",
    24: "Event",
    25: "Operator",
    26: "TypeParameter",
}

SEVERITY_NAMES = {
    1: "Error",
    2: "Warning",
    3: "Information",
    4: "Hint",
}


@dataclass
class ServerConfig:
    language_id: str
    command: List[str]
    extensions: List[str] = field(default_factory=list)
    initialization_options: Dict[str, Any] = field(default_factory=dict)
    root_uri: Optional[str] = None
    env: Dict[str, str] = field(default_factory=dict)


class LSPError(RuntimeError):
    """Raised for LSP transport or protocol failures."""


class LSPClient:
    """Minimal JSON-RPC LSP client over stdio."""

    def __init__(
        self,
        command: List[str],
        language_id: str,
        root_uri: Optional[str] = None,
        initialization_options: Optional[Dict[str, Any]] = None,
        env: Optional[Dict[str, str]] = None,
        request_timeout: float = DEFAULT_REQUEST_TIMEOUT,
    ):
        self.command = command
        self.language_id = language_id
        self.root_uri = root_uri
        self.initialization_options = initialization_options or {}
        self.env = env or {}
        self.request_timeout = request_timeout

        self.process: Optional[subprocess.Popen] = None
        self.reader_thread: Optional[threading.Thread] = None
        self.stderr_thread: Optional[threading.Thread] = None
        self.pending: Dict[int, queue.Queue] = {}
        self.next_id = 1
        self.write_lock = threading.Lock()
        self.pending_lock = threading.Lock()
        self.running = False
        self.initialized = False
        self.shutdown_requested = False
        self.server_capabilities: Dict[str, Any] = {}
        self.workspace_root: Optional[str] = None
        self.open_documents: Dict[str, Dict[str, Any]] = {}
        self.diagnostics: Dict[str, List[Dict[str, Any]]] = {}
        self.last_error: Optional[str] = None
        self.stderr_output: List[str] = []
        self.restart_count = 0
        self.last_start_time = 0.0

    def start(self) -> None:
        if self.running and self.process and self.process.poll() is None:
            return

        self.shutdown_requested = False
        self.last_error = None

        try:
            self.process = subprocess.Popen(
                self.command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False,
                bufsize=0,
                env={**os.environ, **self.env},
            )
        except FileNotFoundError as exc:
            raise LSPError(f"Language server not found: {self.command[0]}") from exc
        except Exception as exc:
            raise LSPError(f"Failed to start language server: {exc}") from exc

        self.running = True
        self.initialized = False
        self.last_start_time = time.time()

        self.reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
        self.reader_thread.start()

        self.stderr_thread = threading.Thread(target=self._stderr_loop, daemon=True)
        self.stderr_thread.start()

    def initialize(self, workspace_root: str) -> Dict[str, Any]:
        self.workspace_root = workspace_root
        if not self.root_uri:
            self.root_uri = self.path_to_uri(workspace_root)

        self.start()

        params = {
            "processId": os.getpid(),
            "clientInfo": {"name": "codrninja", "version": "0.6.0-dev5"},
            "rootUri": self.root_uri,
            "workspaceFolders": [
                {"uri": self.root_uri, "name": os.path.basename(workspace_root) or workspace_root}
            ],
            "capabilities": {
                "workspace": {
                    "workspaceFolders": True,
                    "symbol": {"dynamicRegistration": False},
                    "didChangeWatchedFiles": {"dynamicRegistration": True},
                },
                "textDocument": {
                    "definition": {"dynamicRegistration": False},
                    "hover": {"dynamicRegistration": False, "contentFormat": ["markdown", "plaintext"]},
                    "references": {"dynamicRegistration": False},
                    "documentSymbol": {"hierarchicalDocumentSymbolSupport": True},
                    "documentHighlight": {"dynamicRegistration": False},
                    "codeAction": {"dynamicRegistration": False},
                    "rename": {"dynamicRegistration": False, "prepareSupport": True},
                    "formatting": {"dynamicRegistration": False},
                    "publishDiagnostics": {"relatedInformation": True},
                    "synchronization": {
                        "dynamicRegistration": False,
                        "willSave": False,
                        "didSave": True,
                        "willSaveWaitUntil": False,
                    },
                },
            },
            "initializationOptions": self.initialization_options,
        }

        result = self.request("initialize", params)
        self.server_capabilities = result.get("capabilities", {}) if isinstance(result, dict) else {}
        self.notify("initialized", {})
        self.initialized = True
        return self.server_capabilities

    def shutdown(self) -> None:
        self.shutdown_requested = True
        if not self.process:
            return

        try:
            if self.running and self.process.poll() is None and self.initialized:
                try:
                    self.request("shutdown", timeout=3.0)
                except Exception:
                    pass
                try:
                    self.notify("exit", {})
                except Exception:
                    pass
        finally:
            self.running = False
            try:
                if self.process.stdin:
                    self.process.stdin.close()
            except Exception:
                pass
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass
            self.process = None
            self.initialized = False

    def ensure_running(self, workspace_root: str) -> None:
        if self.process is None or self.process.poll() is not None or not self.initialized:
            self.initialize(workspace_root)
            for uri, doc in list(self.open_documents.items()):
                self.did_open(uri, doc.get("text", ""), doc.get("language_id", self.language_id))

    def did_open(self, uri: str, text: str, language_id: str) -> None:
        version = self.open_documents.get(uri, {}).get("version", 0) + 1
        self.open_documents[uri] = {"text": text, "language_id": language_id, "version": version}
        self.notify(
            "textDocument/didOpen",
            {
                "textDocument": {
                    "uri": uri,
                    "languageId": language_id,
                    "version": version,
                    "text": text,
                }
            },
        )

    def did_change(self, uri: str, text: str) -> None:
        doc = self.open_documents.setdefault(uri, {"text": "", "language_id": self.language_id, "version": 0})
        doc["version"] = doc.get("version", 0) + 1
        doc["text"] = text
        self.notify(
            "textDocument/didChange",
            {
                "textDocument": {"uri": uri, "version": doc["version"]},
                "contentChanges": [{"text": text}],
            },
        )

    def did_close(self, uri: str) -> None:
        self.open_documents.pop(uri, None)
        self.notify("textDocument/didClose", {"textDocument": {"uri": uri}})

    def did_save(self, uri: str) -> None:
        self.notify("textDocument/didSave", {"textDocument": {"uri": uri}})

    def definition(self, uri: str, line: int, char: int) -> str:
        result = self.request("textDocument/definition", self._text_document_position_params(uri, line, char))
        return self._format_locations(result, default_message="No definition found")

    def hover(self, uri: str, line: int, char: int) -> str:
        result = self.request("textDocument/hover", self._text_document_position_params(uri, line, char))
        if not result:
            return "No hover information available"
        contents = result.get("contents") if isinstance(result, dict) else result
        return self._format_hover_contents(contents)

    def references(self, uri: str, line: int, char: int) -> str:
        params = self._text_document_position_params(uri, line, char)
        params["context"] = {"includeDeclaration": True}
        result = self.request("textDocument/references", params)
        return self._format_locations(result, default_message="No references found")

    def document_symbol(self, uri: str) -> str:
        result = self.request("textDocument/documentSymbol", {"textDocument": {"uri": uri}})
        if not result:
            return "No document symbols found"
        lines = self._format_symbols(result)
        return "\n".join(lines) if lines else "No document symbols found"

    def document_highlight(self, uri: str, line: int, char: int) -> str:
        result = self.request("textDocument/documentHighlight", self._text_document_position_params(uri, line, char))
        if not result:
            return "No document highlights found"
        lines = []
        for item in result:
            start = item.get("range", {}).get("start", {})
            end = item.get("range", {}).get("end", {})
            kind = item.get("kind", 1)
            lines.append(
                f"Highlight(kind={kind}) at {start.get('line', 0)+1}:{start.get('character', 0)+1}-"
                f"{end.get('line', 0)+1}:{end.get('character', 0)+1}"
            )
        return "\n".join(lines)

    def code_action(self, uri: str, line: int, char: int, diagnostics: Optional[List[Dict[str, Any]]] = None) -> str:
        diag_payload = diagnostics if diagnostics is not None else self.get_diagnostics(uri)
        params = {
            **self._text_document_position_params(uri, line, char),
            "range": {
                "start": {"line": line, "character": char},
                "end": {"line": line, "character": char},
            },
            "context": {"diagnostics": diag_payload},
        }
        result = self.request("textDocument/codeAction", params)
        if not result:
            return "No code actions available"
        lines = []
        for action in result:
            if isinstance(action, dict):
                title = action.get("title", "Untitled action")
                kind = action.get("kind")
                lines.append(f"- {title}" + (f" [{kind}]" if kind else ""))
        return "\n".join(lines) if lines else "No code actions available"

    def formatting(self, uri: str) -> str:
        result = self.request(
            "textDocument/formatting",
            {
                "textDocument": {"uri": uri},
                "options": {
                    "tabSize": 4,
                    "insertSpaces": True,
                    "trimTrailingWhitespace": True,
                    "insertFinalNewline": True,
                    "trimFinalNewlines": True,
                },
            },
        )
        if not result:
            return "No formatting changes suggested"
        lines = []
        for edit in result:
            rng = edit.get("range", {})
            start = rng.get("start", {})
            lines.append(
                f"Edit at {start.get('line', 0)+1}:{start.get('character', 0)+1}\n{edit.get('newText', '')}"
            )
        return "\n\n".join(lines)

    def rename(self, uri: str, line: int, char: int, new_name: str) -> str:
        result = self.request(
            "textDocument/rename",
            {
                **self._text_document_position_params(uri, line, char),
                "newName": new_name,
            },
        )
        return self._format_workspace_edit(result)

    def workspace_symbol(self, query: str) -> str:
        result = self.request("workspace/symbol", {"query": query})
        if not result:
            return "No workspace symbols found"
        lines = []
        for item in result:
            name = item.get("name", "<unknown>")
            kind = SYMBOL_KIND_NAMES.get(item.get("kind"), str(item.get("kind")))
            location = item.get("location", {})
            lines.append(f"{name} ({kind}) — {self._format_location(location)}")
        return "\n".join(lines)

    def workspace_folders(self) -> str:
        result = self.request("workspace/workspaceFolders", {})
        if not result:
            return "No workspace folders reported"
        return "\n".join(f"- {item.get('name', item.get('uri', ''))}: {item.get('uri', '')}" for item in result)

    def get_diagnostics(self, uri: str) -> List[Dict[str, Any]]:
        return self.diagnostics.get(uri, [])

    def diagnostics_text(self, uri: str) -> str:
        diagnostics = self.get_diagnostics(uri)
        if not diagnostics:
            return "No diagnostics"
        lines = []
        for diag in diagnostics:
            start = diag.get("range", {}).get("start", {})
            severity = SEVERITY_NAMES.get(diag.get("severity"), "Info")
            source = diag.get("source") or self.language_id
            message = diag.get("message", "")
            code = diag.get("code")
            code_text = f" [{code}]" if code else ""
            lines.append(
                f"{severity} at {start.get('line', 0)+1}:{start.get('character', 0)+1}{code_text} ({source}) — {message}"
            )
        return "\n".join(lines)

    def notify_watched_files(self, changes: List[Dict[str, Any]]) -> None:
        self.notify("workspace/didChangeWatchedFiles", {"changes": changes})

    def request(self, method: str, params: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None) -> Any:
        self._ensure_process_alive()
        request_id = self.next_id
        self.next_id += 1

        response_queue: queue.Queue = queue.Queue(maxsize=1)
        with self.pending_lock:
            self.pending[request_id] = response_queue

        self._send_message({"jsonrpc": "2.0", "id": request_id, "method": method, "params": params or {}})

        try:
            response = response_queue.get(timeout=timeout or self.request_timeout)
        except queue.Empty as exc:
            with self.pending_lock:
                self.pending.pop(request_id, None)
            raise LSPError(f"LSP request timed out: {method}") from exc

        if "error" in response:
            error = response["error"]
            raise LSPError(f"LSP error for {method}: {error}")
        return response.get("result")

    def notify(self, method: str, params: Optional[Dict[str, Any]] = None) -> None:
        self._ensure_process_alive()
        self._send_message({"jsonrpc": "2.0", "method": method, "params": params or {}})

    def _send_message(self, payload: Dict[str, Any]) -> None:
        if not self.process or not self.process.stdin:
            raise LSPError("Language server is not running")

        body = json.dumps(payload).encode("utf-8")
        header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")

        with self.write_lock:
            try:
                self.process.stdin.write(header)
                self.process.stdin.write(body)
                self.process.stdin.flush()
            except Exception as exc:
                self.running = False
                raise LSPError(f"Failed to write to language server: {exc}") from exc

    def _reader_loop(self) -> None:
        try:
            assert self.process and self.process.stdout
            stdout = self.process.stdout
            while True:
                headers = self._read_headers(stdout)
                if headers is None:
                    break
                content_length = int(headers.get("content-length", "0"))
                if content_length <= 0:
                    continue
                body = stdout.read(content_length)
                if not body:
                    break
                message = json.loads(body.decode("utf-8"))
                self._handle_message(message)
        except Exception as exc:
            self.last_error = f"Reader loop failed: {exc}"
        finally:
            self.running = False
            self._fail_pending(self.last_error or "Language server exited")

    def _stderr_loop(self) -> None:
        if not self.process or not self.process.stderr:
            return
        try:
            while True:
                line = self.process.stderr.readline()
                if not line:
                    break
                text = line.decode("utf-8", errors="replace").rstrip()
                if text:
                    self.stderr_output.append(text)
                    self.stderr_output = self.stderr_output[-50:]
        except Exception as exc:
            self.last_error = f"stderr read failed: {exc}"

    def _read_headers(self, stream) -> Optional[Dict[str, str]]:
        headers: Dict[str, str] = {}
        while True:
            line = stream.readline()
            if not line:
                return None
            if line in (b"\r\n", b"\n"):
                return headers
            decoded = line.decode("ascii", errors="ignore").strip()
            if ":" in decoded:
                key, value = decoded.split(":", 1)
                headers[key.lower()] = value.strip()

    def _handle_message(self, message: Dict[str, Any]) -> None:
        if "id" in message:
            with self.pending_lock:
                waiter = self.pending.pop(message["id"], None)
            if waiter:
                waiter.put(message)
            return

        method = message.get("method")
        params = message.get("params", {})
        if method == "textDocument/publishDiagnostics":
            uri = params.get("uri")
            diagnostics = params.get("diagnostics", [])
            if uri:
                self.diagnostics[uri] = diagnostics
        elif method == "window/logMessage":
            msg = params.get("message")
            if msg:
                self.stderr_output.append(msg)
                self.stderr_output = self.stderr_output[-50:]

    def _fail_pending(self, error_message: str) -> None:
        with self.pending_lock:
            pending = list(self.pending.items())
            self.pending.clear()
        for _, waiter in pending:
            waiter.put({"error": error_message})

    def _ensure_process_alive(self) -> None:
        if not self.process:
            raise LSPError("Language server is not running")
        poll = self.process.poll()
        if poll is not None:
            self.running = False
            raise LSPError(self.last_error or f"Language server exited with code {poll}")

    def _text_document_position_params(self, uri: str, line: int, char: int) -> Dict[str, Any]:
        return {
            "textDocument": {"uri": uri},
            "position": {"line": line, "character": char},
        }

    def _format_locations(self, result: Any, default_message: str = "No locations found") -> str:
        if not result:
            return default_message
        if isinstance(result, dict):
            result = [result]
        lines = []
        for item in result:
            if "targetUri" in item:
                location = {
                    "uri": item.get("targetUri"),
                    "range": item.get("targetSelectionRange") or item.get("targetRange"),
                }
            else:
                location = item
            lines.append(self._format_location(location))
        return "\n".join(lines) if lines else default_message

    def _format_location(self, location: Dict[str, Any]) -> str:
        uri = location.get("uri", "")
        rng = location.get("range", {})
        start = rng.get("start", {})
        line = start.get("line", 0) + 1
        character = start.get("character", 0) + 1
        return f"{self.uri_to_path(uri)}:{line}:{character}"

    def _format_hover_contents(self, contents: Any) -> str:
        if contents is None:
            return "No hover information available"
        if isinstance(contents, str):
            return contents.strip() or "No hover information available"
        if isinstance(contents, list):
            parts = [self._format_hover_contents(item) for item in contents]
            return "\n\n".join(part for part in parts if part).strip() or "No hover information available"
        if isinstance(contents, dict):
            if "value" in contents:
                language = contents.get("language")
                value = contents.get("value", "")
                return f"```{language or ''}\n{value}\n```".strip()
            return self._format_hover_contents(contents.get("contents"))
        return str(contents)

    def _format_symbols(self, symbols: List[Dict[str, Any]], indent: int = 0) -> List[str]:
        lines: List[str] = []
        for symbol in symbols:
            kind = SYMBOL_KIND_NAMES.get(symbol.get("kind"), str(symbol.get("kind")))
            name = symbol.get("name", "<unnamed>")
            detail = symbol.get("detail")
            prefix = "  " * indent
            line = f"{prefix}- {name} ({kind})"
            if detail:
                line += f": {detail}"
            location = symbol.get("location")
            selection_range = symbol.get("selectionRange")
            if location:
                line += f" — {self._format_location(location)}"
            elif selection_range:
                start = selection_range.get("start", {})
                line += f" — line {start.get('line', 0)+1}"
            lines.append(line)
            children = symbol.get("children") or []
            lines.extend(self._format_symbols(children, indent + 1))
        return lines

    def _format_workspace_edit(self, result: Any) -> str:
        if not result:
            return "Rename produced no changes"
        changes = result.get("changes") or {}
        document_changes = result.get("documentChanges") or []
        lines = []
        for uri, edits in changes.items():
            lines.append(f"{self.uri_to_path(uri)}: {len(edits)} edit(s)")
        for change in document_changes:
            text_document = change.get("textDocument", {})
            uri = text_document.get("uri")
            edits = change.get("edits") or []
            if uri:
                lines.append(f"{self.uri_to_path(uri)}: {len(edits)} edit(s)")
        return "\n".join(lines) if lines else "Rename applied"

    @staticmethod
    def path_to_uri(path: str) -> str:
        return Path(path).resolve().as_uri()

    @staticmethod
    def uri_to_path(uri: str) -> str:
        if uri.startswith("file://"):
            parsed = urlparse(uri)
            return unquote(parsed.path)
        return uri


class LSPManager:
    """Manage per-language LSP clients for a workspace."""

    DEFAULT_SERVERS: Dict[str, List[Dict[str, Any]]] = {
        "python": [
            {"command": ["python3", "-m", "pylsp"]},
            {"command": ["jedi-language-server"]},
        ],
        "javascript": [
            {"command": ["typescript-language-server", "--stdio"]},
        ],
        "typescript": [
            {"command": ["typescript-language-server", "--stdio"]},
        ],
        "rust": [
            {"command": ["rust-analyzer"]},
        ],
        "go": [
            {"command": ["gopls"]},
        ],
        "ruby": [
            {"command": ["solargraph", "stdio"]},
        ],
    }

    def __init__(self, workspace_root: str, config_path: Optional[str] = None):
        self.workspace_root = os.path.abspath(workspace_root)
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), "lsp_servers.json")
        self.server_configs: Dict[str, ServerConfig] = {}
        self.extension_map: Dict[str, str] = {}
        self.clients: Dict[str, LSPClient] = {}
        self.restart_backoff: Dict[str, float] = {}
        self._load_configs()

    def _load_configs(self) -> None:
        config_data: Dict[str, Any] = {}
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as handle:
                config_data = json.load(handle)

        languages = set(self.DEFAULT_SERVERS.keys()) | set(config_data.keys())
        for language_id in languages:
            entry = config_data.get(language_id, {})
            detected_command = self._detect_command(language_id, entry.get("command"))
            extensions = entry.get("extensions") or self._default_extensions(language_id)
            config = ServerConfig(
                language_id=language_id,
                command=detected_command or entry.get("command") or self._default_command(language_id),
                extensions=extensions,
                initialization_options=entry.get("initialization_options", {}),
                root_uri=entry.get("root_uri") or Path(self.workspace_root).as_uri(),
            )
            self.server_configs[language_id] = config
            for ext in extensions:
                self.extension_map[ext.lower()] = language_id

    def _detect_command(self, language_id: str, preferred: Optional[List[str]] = None) -> Optional[List[str]]:
        candidates: List[List[str]] = []
        if preferred:
            candidates.append(preferred)
        for item in self.DEFAULT_SERVERS.get(language_id, []):
            candidates.append(item["command"])
        for command in candidates:
            if self._command_exists(command):
                return command
        return None

    def _command_exists(self, command: List[str]) -> bool:
        executable = command[0]
        if executable == "python3" and len(command) >= 3 and command[1] == "-m":
            try:
                probe = subprocess.run(
                    command[:3] + ["--help"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=5,
                )
                return probe.returncode == 0
            except Exception:
                return False
        return shutil.which(executable) is not None

    def _default_command(self, language_id: str) -> List[str]:
        defaults = self.DEFAULT_SERVERS.get(language_id) or []
        if defaults:
            return defaults[0]["command"]
        return [language_id]

    def _default_extensions(self, language_id: str) -> List[str]:
        mapping = {
            "python": [".py"],
            "javascript": [".js", ".jsx"],
            "typescript": [".ts", ".tsx"],
            "rust": [".rs"],
            "go": [".go"],
            "ruby": [".rb"],
        }
        return mapping.get(language_id, [])

    def register_server(self, language_id: str, command: List[str], args: Optional[List[str]] = None, root_uri: Optional[str] = None) -> None:
        full_command = list(command) + (args or [])
        config = self.server_configs.get(language_id)
        extensions = config.extensions if config else self._default_extensions(language_id)
        init_options = config.initialization_options if config else {}
        self.server_configs[language_id] = ServerConfig(
            language_id=language_id,
            command=full_command,
            extensions=extensions,
            initialization_options=init_options,
            root_uri=root_uri or Path(self.workspace_root).as_uri(),
        )

    def detect_language(self, file_path: str) -> Optional[str]:
        ext = Path(file_path).suffix.lower()
        return self.extension_map.get(ext)

    def get_client(self, language_id: str) -> Optional[LSPClient]:
        config = self.server_configs.get(language_id)
        if not config:
            return None

        client = self.clients.get(language_id)
        if client:
            if client.process is not None and client.process.poll() is None and client.initialized:
                return client
            self._handle_crash(language_id)

        if not self._command_exists(config.command):
            return None

        client = LSPClient(
            command=config.command,
            language_id=language_id,
            root_uri=config.root_uri,
            initialization_options=config.initialization_options,
        )
        try:
            client.initialize(self.workspace_root)
        except Exception as exc:
            client.last_error = str(exc)
            self.clients[language_id] = client
            return None

        self.clients[language_id] = client
        self.restart_backoff[language_id] = DEFAULT_RESTART_BACKOFF
        return client

    def stop(self, language_id: str) -> bool:
        client = self.clients.pop(language_id, None)
        if not client:
            return False
        client.shutdown()
        return True

    def stop_all(self) -> None:
        for client in list(self.clients.values()):
            client.shutdown()
        self.clients.clear()

    def ensure_document_open(self, file_path: str, language_id: Optional[str] = None) -> Tuple[Optional[LSPClient], str, Optional[str]]:
        language = language_id or self.detect_language(file_path)
        if not language:
            return None, "No language server available", None
        client = self.get_client(language)
        if not client:
            return None, "No language server available", language
        abs_path = os.path.abspath(file_path)
        uri = LSPClient.path_to_uri(abs_path)
        text = Path(abs_path).read_text(encoding="utf-8")
        if uri not in client.open_documents:
            client.did_open(uri, text, language)
        else:
            client.did_change(uri, text)
        client.did_save(uri)
        return client, uri, language

    def status(self) -> List[Dict[str, Any]]:
        rows = []
        for language, config in self.server_configs.items():
            client = self.clients.get(language)
            running = bool(client and client.process and client.process.poll() is None and client.initialized)
            rows.append(
                {
                    "language": language,
                    "command": config.command,
                    "running": running,
                    "available": self._command_exists(config.command),
                    "last_error": getattr(client, "last_error", None),
                }
            )
        return rows

    def _handle_crash(self, language_id: str) -> None:
        client = self.clients.get(language_id)
        if not client:
            return
        client.shutdown()
        delay = self.restart_backoff.get(language_id, DEFAULT_RESTART_BACKOFF)
        time.sleep(delay)
        self.restart_backoff[language_id] = min(delay * 2, MAX_RESTART_BACKOFF)

    @staticmethod
    def install_hint(language_id: str) -> str:
        hints = {
            "python": "Install Python LSP with: pip3 install python-lsp-server",
            "javascript": "Install TypeScript LSP with: npm install -g typescript-language-server typescript",
            "typescript": "Install TypeScript LSP with: npm install -g typescript-language-server typescript",
            "rust": "Install rust-analyzer from your package manager or rustup component.",
            "go": "Install gopls with: go install golang.org/x/tools/gopls@latest",
            "ruby": "Install solargraph with: gem install solargraph",
        }
        return hints.get(language_id, "No installation hint available")
