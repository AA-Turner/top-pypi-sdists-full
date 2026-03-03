from __future__ import annotations

from typing import Any

from abstra_internals.settings import Settings

from .base_migration import Migration


def _group_permissions(permissions: list[dict[str, Any]]) -> list[str]:
    """Group agent permissions into tool constructor calls matching real tool classes."""
    tables: dict[str, list[str]] = {}
    files_actions: list[str] = []
    connections_actions: list[str] = []
    has_browser = False
    browser_urls: list[str] | None = None

    for perm in permissions:
        perm_type = perm.get("type")
        action = perm.get("action", "")

        if perm_type == "tables":
            table_name = perm.get("tableName", "")
            tables.setdefault(table_name, []).append(action)
        elif perm_type == "files":
            files_actions.append(action)
        elif perm_type == "connections":
            connections_actions.append(action)
        elif perm_type == "browser":
            has_browser = True
            allowed = perm.get("allowedUrls")
            if allowed is not None:
                if browser_urls is None:
                    browser_urls = []
                browser_urls.extend(allowed)
        # source_code permissions are intentionally skipped

    tool_lines = []

    for table_name, actions in sorted(tables.items()):
        method_str = ", ".join(f'"{a}"' for a in actions)
        if table_name:
            tool_lines.append(
                f'TablesTools(method=[{method_str}], table="{table_name}")'
            )
        else:
            tool_lines.append(f"TablesTools(method=[{method_str}])")

    if files_actions:
        actions_str = ", ".join(f'"{a}"' for a in files_actions)
        tool_lines.append(f"FilesTools(actions=[{actions_str}])")

    if connections_actions:
        actions_str = ", ".join(f'"{a}"' for a in connections_actions)
        tool_lines.append(f"ConnectorsTools(action=[{actions_str}])")

    if has_browser:
        if browser_urls:
            urls_str = ", ".join(f'"{u}"' for u in browser_urls)
            tool_lines.append(f"BrowserTools(url=[{urls_str}])")
        else:
            tool_lines.append("BrowserTools()")

    return tool_lines


def _get_tool_imports(permissions: list[dict[str, Any]]) -> list[str]:
    """Determine which tool import lines are needed."""
    types = {p.get("type") for p in permissions}
    imports = []
    if "tables" in types:
        imports.append("from abstra_internals.agents.tools.tables import TablesTools")
    if "files" in types:
        imports.append("from abstra_internals.agents.tools.files import FilesTools")
    if "connections" in types:
        imports.append(
            "from abstra_internals.agents.tools.connectors import ConnectorsTools"
        )
    if "browser" in types:
        imports.append("from abstra_internals.agents.tools.browser import BrowserTools")
    return imports


def _generate_py_content(
    prompt_content: str,
    permissions: list[dict[str, Any]],
    max_steps: int,
) -> str:
    """Generate the Python file content for a converted agent."""
    tool_imports = _get_tool_imports(permissions)
    tool_lines = _group_permissions(permissions)

    lines = ["from abstra.ai import run_agent"]
    for imp in tool_imports:
        lines.append(imp)

    lines.append("")

    kwargs = []
    prompt_repr = repr(prompt_content)
    kwargs.append(f"    prompt={prompt_repr}")

    if tool_lines:
        tools_formatted = ",\n        ".join(tool_lines)
        kwargs.append(f"    tools=[\n        {tools_formatted},\n    ]")

    if max_steps != 30:
        kwargs.append(f"    max_steps={max_steps}")

    kwargs_str = ",\n".join(kwargs)
    lines.append(f"run_agent(\n{kwargs_str},\n)")
    lines.append("")

    return "\n".join(lines)


class Migration018(Migration):
    def set_as_test(self):
        self.test_mode = True

    @staticmethod
    def target_version() -> str:
        return "18.0"

    @staticmethod
    def source_version() -> str:
        return "17.0"

    def _read_prompt_file(self, file_path: str) -> str:
        if self.test_mode:
            return self._test_prompts.get(file_path, "")
        try:
            full_path = Settings.root_path / file_path
            return full_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return ""

    def _write_py_file(self, file_path: str, content: str) -> None:
        if self.test_mode:
            self._test_written_files[file_path] = content
            return
        full_path = Settings.root_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")

    def _delete_md_file(self, file_path: str) -> None:
        if self.test_mode:
            self._test_deleted_files.add(file_path)
            return
        full_path = Settings.root_path / file_path
        if full_path.exists():
            full_path.unlink()

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.test_mode: bool = False
        self._test_prompts: dict[str, str] = {}
        self._test_written_files: dict[str, str] = {}
        self._test_deleted_files: set[str] = set()

    def _convert_agent_to_script(self, agent: dict[str, Any]) -> dict[str, Any]:
        md_file = agent.get("file", "")
        prompt_content = self._read_prompt_file(md_file)
        permissions = agent.get("permissions", [])

        source_code_perms = [p for p in permissions if p.get("type") == "source_code"]
        if source_code_perms:
            agent_title = agent.get("title", agent.get("id", "unknown"))
            self.warnings.append(
                f"Agent '{agent_title}': source_code permissions were skipped "
                f"during migration (not supported in the new model)."
            )
        max_steps = agent.get("max_steps", 30)

        py_content = _generate_py_content(prompt_content, permissions, max_steps)

        # Change .md extension to .py
        if md_file.endswith(".md"):
            py_file = md_file[:-3] + ".py"
        else:
            py_file = md_file + ".py"

        self._write_py_file(py_file, py_content)
        self._delete_md_file(md_file)

        return {
            "id": agent["id"],
            "file": py_file,
            "title": agent.get("title", ""),
            "is_initial": agent.get("is_initial", True),
            "workflow_position": agent.get("workflow_position", [0, 0]),
            "transitions": agent.get("transitions", []),
            "input": agent.get("input", False),
            "output": agent.get("output", False),
            "task_schema": agent.get("task_schema"),
        }

    def _rewrite_transitions(self) -> None:
        """Change target_type from 'agents' to 'scripts' across all stages."""
        stage_keys = ["forms", "hooks", "scripts", "jobs", "components"]
        for key in stage_keys:
            for stage in self.data.get(key, []):
                for transition in stage.get("transitions", []):
                    if transition.get("target_type") == "agents":
                        transition["target_type"] = "scripts"

    def _migrate(self) -> None:
        agents = self.data.get("agents", [])
        scripts = self.data.get("scripts", [])

        for agent in agents:
            script = self._convert_agent_to_script(agent)
            scripts.append(script)

        self.data["scripts"] = scripts

        self._rewrite_transitions()

        self.data.pop("agents", None)
