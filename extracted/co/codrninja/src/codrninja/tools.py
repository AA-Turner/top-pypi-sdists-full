"""Tool system for codrninja — allows the AI to read/write/execute."""

import json
import os
import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from .lsp import LSPManager
from .mcp import MCPManager
from .memory import remember as _mem_remember, recall as _mem_recall, forget as _mem_forget
from .permissions import PermissionManager
from .todo import TodoManager, format_todo_item
from .web_tools import WebToolError, fetch_web_text, search_web


@dataclass
class ToolResult:
    """Result from a tool execution."""
    success: bool
    output: str
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ToolRegistry:
    """Registry of available tools."""

    def __init__(self):
        self.mcp = MCPManager()
        self.todo_manager = TodoManager()
        self.current_session_id: Optional[str] = None
        self.workspace_root = os.getcwd()
        self.lsp = LSPManager(self.workspace_root)
        self.permissions: Optional[PermissionManager] = None
        self.agent_type: str = "build"
        self.tools = {
            "read_file": self.read_file,
            "write_file": self.write_file,
            "edit_file": self.edit_file,
            "execute_command": self.execute_command,
            "list_files": self.list_files,
            "search_files": self.search_files,
            "web_fetch": self.web_fetch,
            "web_search": self.web_search,
            "todo_add": self.todo_add,
            "todo_list": self.todo_list,
            "todo_complete": self.todo_complete,
            "todo_remove": self.todo_remove,
            "lsp_definition": self.lsp_definition,
            "lsp_hover": self.lsp_hover,
            "lsp_references": self.lsp_references,
            "lsp_diagnostics": self.lsp_diagnostics,
            "lsp_symbols": self.lsp_symbols,
            "lsp_rename": self.lsp_rename,
            "remember": self.remember,
            "recall": self.recall,
            "forget": self.forget,
        }
        self.refresh_mcp_tools()

    def set_session(self, session_id: Optional[str]):
        """Set the active session for session-scoped tools."""
        self.current_session_id = session_id

    def set_permissions(self, permissions: PermissionManager, agent_type: str = "build"):
        self.permissions = permissions
        self.agent_type = agent_type

    def refresh_mcp_tools(self, force: bool = False):
        """Discover MCP tools and register them into the registry."""
        discovered = self.mcp.discover_tools(force=force)

        self.tools = {name: tool for name, tool in self.tools.items() if not getattr(tool, "_is_mcp_tool", False)}

        for server_name, tools in discovered.items():
            for tool in tools:
                tool_name = tool.get("name") or tool.get("id")
                if not tool_name:
                    continue
                qualified_name = f"mcp_{server_name}_{tool_name}".replace("-", "_")
                wrapper = self._make_mcp_tool(server_name, tool_name)
                wrapper._is_mcp_tool = True
                self.tools[qualified_name] = wrapper

    def _make_mcp_tool(self, server_name: str, tool_name: str):
        def _tool(**kwargs):
            try:
                result = self.mcp.call_tool(server_name, tool_name, kwargs)
                if isinstance(result, (dict, list)):
                    output = json.dumps(result, indent=2)
                else:
                    output = str(result)
                return ToolResult(True, output)
            except Exception as e:
                return ToolResult(False, "", str(e))

        _tool.__name__ = f"mcp_{server_name}_{tool_name}"
        _tool.__doc__ = f"MCP tool '{tool_name}' from server '{server_name}'"
        return _tool

    def call(self, name: str, **kwargs) -> ToolResult:
        """Call a tool by name."""
        if name not in self.tools:
            return ToolResult(False, "", f"Unknown tool: {name}")

        try:
            return self.tools[name](**kwargs)
        except Exception as e:
            return ToolResult(False, "", str(e))

    def _permission_error(self, scope: str, target: str) -> Optional[ToolResult]:
        if not self.permissions:
            return None
        decision = self.permissions.check(scope, target, self.agent_type)
        if decision == "allow":
            return None
        explanation = self.permissions.explain(scope, target, self.agent_type)
        if decision == "ask":
            return ToolResult(False, "", f"Permission requires confirmation: {explanation}")
        return ToolResult(False, "", f"Permission denied: {explanation}")

    def read_file(self, path: str, offset: int = 0, limit: int = 500) -> ToolResult:
        """Read a file from disk."""
        permission_error = self._permission_error("read", path)
        if permission_error:
            return permission_error
        try:
            with open(path, 'r') as f:
                lines = f.readlines()

            start = offset
            end = min(offset + limit, len(lines))
            content = ''.join(lines[start:end])

            if len(lines) > end:
                content += f"\n[File truncated: showing lines {start + 1}–{end} of {len(lines)}. Call read_file with offset={end} to read more.]"

            return ToolResult(True, content)
        except Exception as e:
            return ToolResult(False, "", str(e))

    def write_file(self, path: str, content: str) -> ToolResult:
        """Write content to a file."""
        permission_error = self._permission_error("write", path)
        if permission_error:
            return permission_error
        try:
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            return ToolResult(True, f"File written: {path}")
        except Exception as e:
            return ToolResult(False, "", str(e))

    def edit_file(self, path: str, old_text: str, new_text: str) -> ToolResult:
        """Edit a file by replacing text."""
        permission_error = self._permission_error("write", path)
        if permission_error:
            return permission_error
        try:
            with open(path, 'r') as f:
                content = f.read()

            if old_text not in content:
                return ToolResult(False, "", f"Text not found in {path}")

            # Compute line offset and context before writing
            prefix = content[:content.index(old_text)]
            line_start = prefix.count('\n')  # 0-indexed
            all_lines = content.split('\n')
            old_lines = old_text.split('\n')
            if old_lines and old_lines[-1] == '':
                old_lines = old_lines[:-1]
            ctx_before = all_lines[max(0, line_start - 3):line_start]
            ctx_after_start = line_start + len(old_lines)
            ctx_after = all_lines[ctx_after_start:ctx_after_start + 3]

            content = content.replace(old_text, new_text, 1)

            with open(path, 'w') as f:
                f.write(content)

            return ToolResult(True, f"File edited: {path}", metadata={
                'line_start': line_start + 1,  # 1-indexed for display
                'context_before': ctx_before,
                'context_after': ctx_after,
            })
        except Exception as e:
            return ToolResult(False, "", str(e))

    def execute_command(self, command: str, cwd: Optional[str] = None) -> ToolResult:
        """Execute a shell command."""
        permission_error = self._permission_error("execute", command)
        if permission_error:
            return permission_error
        if self.permissions and self.permissions.check_dangerous(command):
            explanation = self.permissions.explain("execute", command, self.agent_type)
            if self.permissions.check("execute", command, self.agent_type) != "allow":
                return ToolResult(False, "", f"Dangerous command blocked: {explanation}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=300
            )

            output = result.stdout
            if result.stderr:
                output += f"\n[stderr]\n{result.stderr}"

            return ToolResult(
                result.returncode == 0,
                output,
                f"Exit code: {result.returncode}" if result.returncode != 0 else None
            )
        except subprocess.TimeoutExpired:
            return ToolResult(False, "", "Command timed out")
        except Exception as e:
            return ToolResult(False, "", str(e))

    def list_files(self, path: str = ".", depth: int = 1) -> ToolResult:
        """List files in a directory with a hard cap to avoid hanging on large trees."""
        try:
            max_items = 200
            files = []
            items = 0
            for root, dirs, filenames in os.walk(path):
                level = root.replace(path, '').count(os.sep)
                if level > depth:
                    dirs[:] = []
                    continue
                indent = ' ' * 2 * level
                files.append(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for f in filenames:
                    if items >= max_items:
                        files.append(f"{subindent}... ({items}+ items, truncated)")
                        return ToolResult(True, '\n'.join(files))
                    files.append(f"{subindent}{f}")
                    items += 1
            return ToolResult(True, '\n'.join(files))
        except Exception as e:
            return ToolResult(False, "", str(e))

    def search_files(self, pattern: str, path: str = ".") -> ToolResult:
        """Search for files matching a pattern."""
        try:
            import fnmatch
            matches = []
            for root, dirs, filenames in os.walk(path):
                for filename in fnmatch.filter(filenames, pattern):
                    matches.append(os.path.join(root, filename))
            return ToolResult(True, '\n'.join(matches) if matches else "No matches found")
        except Exception as e:
            return ToolResult(False, "", str(e))

    def web_fetch(self, url: str, max_length: int = 10000, timeout: int = 10) -> ToolResult:
        """Fetch a web page and return cleaned text."""
        try:
            content = fetch_web_text(url, timeout=timeout, max_length=max_length)
            return ToolResult(True, content)
        except WebToolError as e:
            return ToolResult(False, "", str(e))
        except Exception as e:
            return ToolResult(False, "", str(e))

    def web_search(self, query: str, num_results: int = 5) -> ToolResult:
        """Search the web and return structured results as JSON."""
        try:
            results = search_web(query, num_results=num_results)
            return ToolResult(True, json.dumps(results, indent=2))
        except WebToolError as e:
            return ToolResult(False, "", str(e))
        except Exception as e:
            return ToolResult(False, "", str(e))

    def _require_session(self, session_id: Optional[str] = None) -> str:
        active_session = session_id or self.current_session_id
        if not active_session:
            raise ValueError("No active session for todo tool")
        return active_session

    def todo_add(self, task: str, session_id: Optional[str] = None) -> ToolResult:
        """Create a todo item for the current session."""
        try:
            active_session = self._require_session(session_id)
            todo_id = self.todo_manager.add(task, active_session)
            item = self.todo_manager.get(todo_id)
            return ToolResult(True, format_todo_item(item) if item else todo_id)
        except Exception as e:
            return ToolResult(False, "", str(e))

    def todo_list(self, session_id: Optional[str] = None) -> ToolResult:
        """List todo items for the current session."""
        try:
            active_session = self._require_session(session_id)
            items = self.todo_manager.list(active_session)
            if not items:
                return ToolResult(True, "No todos for this session")
            return ToolResult(True, "\n".join(format_todo_item(item) for item in items))
        except Exception as e:
            return ToolResult(False, "", str(e))

    def todo_complete(self, todo_id: str) -> ToolResult:
        """Mark a todo item as done."""
        try:
            if not self.todo_manager.complete(todo_id):
                return ToolResult(False, "", f"Todo not found: {todo_id}")
            item = self.todo_manager.get(todo_id)
            return ToolResult(True, format_todo_item(item) if item else todo_id)
        except Exception as e:
            return ToolResult(False, "", str(e))

    def todo_remove(self, todo_id: str) -> ToolResult:
        """Remove a todo item."""
        try:
            if not self.todo_manager.remove(todo_id):
                return ToolResult(False, "", f"Todo not found: {todo_id}")
            return ToolResult(True, f"Removed todo {todo_id}")
        except Exception as e:
            return ToolResult(False, "", str(e))

    def _lsp_hint(self, file_path: str) -> str:
        language = self.lsp.detect_language(file_path)
        if not language:
            return "No language server available"
        return f"No language server available. {self.lsp.install_hint(language)}"

    def _open_lsp_document(self, file_path: str):
        try:
            client, uri, language = self.lsp.ensure_document_open(file_path)
        except UnicodeDecodeError:
            return None, None, None, "Cannot read file as UTF-8 for LSP"
        except FileNotFoundError:
            return None, None, None, f"File not found: {file_path}"
        except Exception as e:
            return None, None, None, str(e)
        if not client or not uri:
            return None, None, language, self._lsp_hint(file_path)
        return client, uri, language, None

    def lsp_definition(self, file_path: str, line: int, column: int) -> ToolResult:
        try:
            client, uri, _language, error = self._open_lsp_document(file_path)
            if error:
                return ToolResult(False, "", error)
            return ToolResult(True, client.definition(uri, line, column))
        except Exception as e:
            return ToolResult(False, "", str(e))

    def lsp_hover(self, file_path: str, line: int, column: int) -> ToolResult:
        try:
            client, uri, _language, error = self._open_lsp_document(file_path)
            if error:
                return ToolResult(False, "", error)
            return ToolResult(True, client.hover(uri, line, column))
        except Exception as e:
            return ToolResult(False, "", str(e))

    def lsp_references(self, file_path: str, line: int, column: int) -> ToolResult:
        try:
            client, uri, _language, error = self._open_lsp_document(file_path)
            if error:
                return ToolResult(False, "", error)
            return ToolResult(True, client.references(uri, line, column))
        except Exception as e:
            return ToolResult(False, "", str(e))

    def lsp_diagnostics(self, file_path: str) -> ToolResult:
        try:
            client, uri, _language, error = self._open_lsp_document(file_path)
            if error:
                return ToolResult(False, "", error)
            return ToolResult(True, client.diagnostics_text(uri))
        except Exception as e:
            return ToolResult(False, "", str(e))

    def lsp_symbols(self, file_path: str) -> ToolResult:
        try:
            client, uri, _language, error = self._open_lsp_document(file_path)
            if error:
                return ToolResult(False, "", error)
            return ToolResult(True, client.document_symbol(uri))
        except Exception as e:
            return ToolResult(False, "", str(e))

    def lsp_rename(self, file_path: str, line: int, column: int, new_name: str) -> ToolResult:
        try:
            client, uri, _language, error = self._open_lsp_document(file_path)
            if error:
                return ToolResult(False, "", error)
            return ToolResult(True, client.rename(uri, line, column, new_name))
        except Exception as e:
            return ToolResult(False, "", str(e))

    # ── Memory tools ──────────────────────────────────────────────────────────

    def remember(self, fact: str, scope: str = 'project') -> ToolResult:
        try:
            return ToolResult(True, _mem_remember(fact, scope))
        except Exception as e:
            return ToolResult(False, "", str(e))

    def recall(self, scope: str = 'all') -> ToolResult:
        try:
            return ToolResult(True, _mem_recall(scope))
        except Exception as e:
            return ToolResult(False, "", str(e))

    def forget(self, fact_key_or_text: str, scope: str = 'project') -> ToolResult:
        try:
            return ToolResult(True, _mem_forget(fact_key_or_text, scope))
        except Exception as e:
            return ToolResult(False, "", str(e))

    def get_schema(self) -> str:
        """Get JSON schema of all tools for the AI."""
        schema = {
            "read_file": {
                "description": "Read a file from disk",
                "parameters": {
                    "path": {"type": "string", "required": True},
                    "offset": {"type": "integer", "default": 0},
                    "limit": {"type": "integer", "default": 100}
                }
            },
            "write_file": {
                "description": "Write content to a file",
                "parameters": {
                    "path": {"type": "string", "required": True},
                    "content": {"type": "string", "required": True}
                }
            },
            "edit_file": {
                "description": "Edit a file by replacing text",
                "parameters": {
                    "path": {"type": "string", "required": True},
                    "old_text": {"type": "string", "required": True},
                    "new_text": {"type": "string", "required": True}
                }
            },
            "execute_command": {
                "description": "Execute a shell command",
                "parameters": {
                    "command": {"type": "string", "required": True},
                    "cwd": {"type": "string", "required": False}
                }
            },
            "list_files": {
                "description": "List files in a directory",
                "parameters": {
                    "path": {"type": "string", "default": "."},
                    "depth": {"type": "integer", "default": 1}
                }
            },
            "search_files": {
                "description": "Search for files matching a pattern",
                "parameters": {
                    "pattern": {"type": "string", "required": True},
                    "path": {"type": "string", "default": "."}
                }
            },
            "web_fetch": {
                "description": "Fetch a web page and return cleaned text content",
                "parameters": {
                    "url": {"type": "string", "required": True},
                    "max_length": {"type": "integer", "default": 10000},
                    "timeout": {"type": "integer", "default": 10}
                }
            },
            "web_search": {
                "description": "Search the web for up-to-date information",
                "parameters": {
                    "query": {"type": "string", "required": True},
                    "num_results": {"type": "integer", "default": 5}
                }
            },
            "todo_add": {
                "description": "Create a session todo item for multi-step work",
                "parameters": {
                    "task": {"type": "string", "required": True},
                    "session_id": {"type": "string", "required": False}
                }
            },
            "todo_list": {
                "description": "List session todo items",
                "parameters": {
                    "session_id": {"type": "string", "required": False}
                }
            },
            "todo_complete": {
                "description": "Mark a todo item as done",
                "parameters": {
                    "todo_id": {"type": "string", "required": True}
                }
            },
            "todo_remove": {
                "description": "Delete a todo item",
                "parameters": {
                    "todo_id": {"type": "string", "required": True}
                }
            },
            "lsp_definition": {
                "description": "Go to definition for a symbol using LSP",
                "parameters": {
                    "file_path": {"type": "string", "required": True},
                    "line": {"type": "integer", "required": True},
                    "column": {"type": "integer", "required": True}
                }
            },
            "lsp_hover": {
                "description": "Get hover/type info for a symbol using LSP",
                "parameters": {
                    "file_path": {"type": "string", "required": True},
                    "line": {"type": "integer", "required": True},
                    "column": {"type": "integer", "required": True}
                }
            },
            "lsp_references": {
                "description": "Find references for a symbol using LSP",
                "parameters": {
                    "file_path": {"type": "string", "required": True},
                    "line": {"type": "integer", "required": True},
                    "column": {"type": "integer", "required": True}
                }
            },
            "lsp_diagnostics": {
                "description": "Get LSP diagnostics for a file",
                "parameters": {
                    "file_path": {"type": "string", "required": True}
                }
            },
            "lsp_symbols": {
                "description": "Get document symbols for a file using LSP",
                "parameters": {
                    "file_path": {"type": "string", "required": True}
                }
            },
            "lsp_rename": {
                "description": "Preview rename edits for a symbol using LSP",
                "parameters": {
                    "file_path": {"type": "string", "required": True},
                    "line": {"type": "integer", "required": True},
                    "column": {"type": "integer", "required": True},
                    "new_name": {"type": "string", "required": True}
                }
            }
        }

        for server in self.mcp.list_servers():
            for tool in server.tools:
                tool_name = tool.get("name") or tool.get("id")
                if not tool_name:
                    continue
                qualified_name = f"mcp_{server.name}_{tool_name}".replace("-", "_")
                schema[qualified_name] = {
                    "description": tool.get("description", f"MCP tool '{tool_name}' from server '{server.name}'"),
                    "parameters": tool.get("inputSchema", {"type": "object"}),
                }

        return json.dumps(schema, indent=2)
