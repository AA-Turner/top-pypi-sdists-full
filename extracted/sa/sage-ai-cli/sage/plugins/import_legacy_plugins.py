"""Import legacy Claude/Codex plugin metadata into SAGE snapshot format.

This script is optional maintenance tooling. Runtime does not depend on it.

Usage:
  python -m sage.plugins.import_legacy_plugins \
    --source ~/.claude/plugins/cache/claude-plugins-official \
    --source ~/.claude/plugins/marketplaces/claude-plugins-official/plugins \
    --source ~/.claude/plugins/marketplaces/claude-plugins-official/external_plugins \
    --output ai-platform/sage/plugins/claude_plugins_snapshot.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def _sanitize_name(text: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9._-]+", "-", text.strip().lower())
    return normalized.strip("-")


def _strip_markdown_frontmatter(markdown: str) -> str:
    """Strip YAML-style markdown frontmatter block when present."""
    if not markdown.startswith("---\n"):
        return markdown
    end_index = markdown.find("\n---\n", 4)
    if end_index < 0:
        return markdown
    return markdown[end_index + len("\n---\n") :]


def _clean_step_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"^\*+|\*+$", "", text)
    return text.strip()


def _extract_list_steps(block_text: str) -> list[str]:
    """Extract ordered and bullet list items from markdown block text."""
    steps: list[str] = []
    for line in block_text.splitlines():
        text = line.strip()
        if not text:
            continue
        if re.match(r"^\d+[.)]\s+", text):
            normalized = re.sub(r"^\d+[.)]\s*", "", text)
            cleaned = _clean_step_text(normalized)
            if cleaned:
                steps.append(cleaned)
            continue
        if re.match(r"^[-*]\s+", text):
            normalized = re.sub(r"^[-*]\s*", "", text)
            cleaned = _clean_step_text(normalized)
            if cleaned:
                steps.append(cleaned)
            continue
    return steps


def _extract_workflow_steps(markdown: str) -> list[str]:
    """Extract structured workflow steps from markdown text.

    Many Claude plugins use section labels like "Actions", "Core Process",
    "Phase X", or "Workflow". We search those first, then gracefully fall back
    to any ordered list items in the document.
    """
    markdown = _strip_markdown_frontmatter(markdown)
    section_titles = (
        "Workflow",
        "Default Workflow",
        "Core Workflow",
        "Process",
        "Core Process",
        "Steps",
        "Actions",
        "Execution",
        "Implementation",
        "Quick start",
        "Routing Rules",
        "Guardrails",
    )
    phase_regex = r"^##\s+Phase\s+\d+[:\s-].*$"

    collected: list[str] = []
    for title in section_titles:
        pattern = rf"^##\s+{re.escape(title)}\s*$([\s\S]*?)(?=^##\s+|\Z)"
        match = re.search(pattern, markdown, flags=re.M)
        if not match:
            continue
        steps = _extract_list_steps(match.group(1))
        if steps:
            collected.extend(steps)

    # Handle docs that use explicit "Phase X" sections.
    for match in re.finditer(phase_regex + r"([\s\S]*?)(?=^##\s+|\Z)", markdown, flags=re.M):
        phase_steps = _extract_list_steps(match.group(1))
        if phase_steps:
            collected.extend(phase_steps)

    if collected:
        deduped: list[str] = []
        seen: set[str] = set()
        for step in collected:
            if step in seen:
                continue
            seen.add(step)
            deduped.append(step)
        return deduped[:40]

    # Fallback: grab any ordered list line in the entire document.
    global_steps = _extract_list_steps(markdown)
    deduped_global: list[str] = []
    seen_global: set[str] = set()
    for step in global_steps:
        if step in seen_global:
            continue
        seen_global.add(step)
        deduped_global.append(step)
    if deduped_global:
        return deduped_global[:40]

    # Last-resort fallback: derive steps from imperative instruction lines.
    inferred: list[str] = []
    in_code_block = False
    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if line.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block or not line:
            continue
        if line.startswith("#") or line.startswith(">"):
            continue
        if line.lower().startswith(("note:", "example:", "output:", "inputs:")):
            continue
        if len(line) < 24:
            continue
        if line.endswith(":"):
            continue
        inferred.append(_clean_step_text(line))
        if len(inferred) >= 12:
            break
    return inferred


def _extract_default_prompt(agent_yaml_path: Path) -> str:
    """Extract `default_prompt` from agent metadata YAML text."""
    if not agent_yaml_path.exists():
        return ""
    text = agent_yaml_path.read_text(encoding="utf-8")
    # Quoted single-line value
    quoted = re.search(
        r"""^default_prompt:\s*["'](?P<value>[\s\S]*?)["']\s*$""",
        text,
        flags=re.M,
    )
    if quoted:
        return quoted.group("value").strip()

    # YAML block literal/folded style
    block = re.search(
        r"^default_prompt:\s*[>|]\s*$([\s\S]*?)(?=^[A-Za-z0-9_-]+:\s|\Z)",
        text,
        flags=re.M,
    )
    if block:
        lines = []
        for raw_line in block.group(1).splitlines():
            if raw_line.startswith("  "):
                lines.append(raw_line[2:])
            elif raw_line.startswith("\t"):
                lines.append(raw_line.lstrip("\t"))
            elif not raw_line.strip():
                lines.append("")
            else:
                break
        return "\n".join(lines).strip()

    # Unquoted single-line fallback
    plain = re.search(r"^default_prompt:\s*(.+)$", text, flags=re.M)
    if plain:
        return plain.group(1).strip().strip('"').strip("'")
    return ""


def _extract_markdown_frontmatter(path: Path) -> dict[str, str]:
    """Extract simple frontmatter keys from markdown files."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    if not text.startswith("---\n"):
        return {}
    end_index = text.find("\n---\n", 4)
    if end_index < 0:
        return {}
    block = text[4:end_index]
    data: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def _extract_markdown_title(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return ""
    match = re.search(r"^#\s+(.+)$", text, flags=re.M)
    return match.group(1).strip() if match else ""


def _extract_instruction_markdown(path: Path) -> str:
    """Read markdown content and strip frontmatter for instruction payloads."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return ""
    return _strip_markdown_frontmatter(text).strip()


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def _plugin_meta_path(plugin_root: Path) -> Path | None:
    """Return plugin metadata path for Claude/Codex plugin formats."""
    candidates = (
        plugin_root / ".claude-plugin" / "plugin.json",
        plugin_root / ".codex-plugin" / "plugin.json",
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _sanitize_capability_name(path: Path) -> str:
    """Build a stable capability name from relative markdown/yaml path."""
    parts = [segment for segment in path.with_suffix("").parts if segment]
    return _sanitize_name(".".join(parts))


def _parse_mcp_servers(
    payload: dict[str, Any],
    *,
    allow_flat_map: bool,
) -> dict[str, dict[str, Any]]:
    """Parse .mcp.json or plugin.json-style MCP server maps."""
    if not payload:
        return {}
    servers = payload.get("mcpServers")
    if isinstance(servers, dict):
        return {str(name): cfg for name, cfg in servers.items() if isinstance(cfg, dict)}
    if not allow_flat_map:
        return {}
    # Some .mcp.json files store the map at top-level.
    return {str(name): cfg for name, cfg in payload.items() if isinstance(cfg, dict)}


def _extract_mcp_entries(plugin_root: Path, plugin_meta: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract normalized MCP server entries from plugin metadata files."""
    servers: dict[str, dict[str, Any]] = {}

    for source in (
        _parse_mcp_servers(plugin_meta, allow_flat_map=False),
        _parse_mcp_servers(_load_json(plugin_root / ".mcp.json"), allow_flat_map=True),
    ):
        servers.update(source)

    entries: list[dict[str, Any]] = []
    for server_name, config in sorted(servers.items()):
        url = str(config.get("url", "")).strip()
        command = str(config.get("command", "")).strip()
        args = config.get("args", [])
        transport = str(config.get("type", "")).strip()
        if not transport:
            transport = "http" if url else "command" if command else "unknown"
        if url:
            description = f"MCP server `{server_name}` over {transport}: {url}"
        elif command:
            description = f"MCP server `{server_name}` command: {command}"
        else:
            description = f"MCP server `{server_name}` integration"
        entries.append(
            {
                "server": server_name,
                "description": description,
                "transport": transport,
                "url": url,
                "command": command,
                "args": args if isinstance(args, list) else [],
            }
        )
    return entries


def _collect_skill_markdown_paths(plugin_root: Path, plugin_meta: dict[str, Any]) -> list[Path]:
    """Collect skill markdown files from convention paths and metadata references."""
    discovered: set[Path] = set(plugin_root.rglob("skills/*/SKILL.md"))

    declared_skills = plugin_meta.get("skills", [])
    if isinstance(declared_skills, list):
        for raw in declared_skills:
            path_text = str(raw).strip()
            if not path_text:
                continue
            candidate = (plugin_root / path_text).resolve()
            if candidate.is_dir():
                candidate = candidate / "SKILL.md"
            if candidate.is_file():
                discovered.add(candidate)

    return sorted(discovered)


def _iter_plugin_roots(source_root: Path) -> list[Path]:
    """Find plugin roots that contain Claude/Codex plugin metadata."""
    roots: list[Path] = []
    if not source_root.exists():
        return roots

    if _plugin_meta_path(source_root):
        return [source_root]

    for marker in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
        for meta in source_root.rglob(marker):
            roots.append(meta.parent.parent)
    return sorted(set(roots))


def _list_recent_revision_dirs(source_root: Path) -> list[Path]:
    """Handle roots like `.../cache/vendor/plugin/<rev>` by picking latest revision."""
    if not source_root.exists() or not source_root.is_dir():
        return []

    roots: list[Path] = []
    for child in sorted(source_root.iterdir()):
        if not child.is_dir():
            continue
        revisions = [path for path in child.iterdir() if path.is_dir()]
        if not revisions:
            continue
        latest = sorted(revisions)[-1]
        if _plugin_meta_path(latest):
            roots.append(latest)
    return roots


def _merge_unique(items: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    seen: set[str] = set()
    merged: list[dict[str, Any]] = []
    for item in items:
        value = str(item.get(key, "")).strip()
        if not value or value in seen:
            continue
        seen.add(value)
        merged.append(item)
    return merged


def _extract_plugin_entry(plugin_root: Path) -> dict[str, Any] | None:
    plugin_meta_path = _plugin_meta_path(plugin_root)
    plugin_meta = _load_json(plugin_meta_path) if plugin_meta_path else {}
    if not plugin_meta:
        return None

    name = str(plugin_meta.get("name", plugin_root.name)).strip()
    if not name:
        return None

    entry: dict[str, Any] = {
        "name": name,
        "description": str(plugin_meta.get("description", "")).strip(),
        "display_name": str(plugin_meta.get("interface", {}).get("displayName", "")).strip(),
        "skills": [],
        "commands": [],
        "agents": [],
        "mcp_servers": [],
    }

    for skill_markdown in _collect_skill_markdown_paths(plugin_root, plugin_meta):
        if not skill_markdown.exists():
            continue
        try:
            markdown = skill_markdown.read_text(encoding="utf-8")
        except Exception:
            continue
        frontmatter = _extract_markdown_frontmatter(skill_markdown)
        skill_name = frontmatter.get("name", "").strip() or skill_markdown.parent.name
        skill_description = frontmatter.get("description", "").strip()
        entry["skills"].append(
            {
                "skill": skill_name,
                "description": skill_description,
                "default_prompt": "",
                "workflow_steps": _extract_workflow_steps(markdown),
                "instruction_markdown": _extract_instruction_markdown(skill_markdown),
                "source_file": str(skill_markdown.relative_to(plugin_root)),
            }
        )
        if not entry["skills"][-1]["default_prompt"]:
            default_prompt = _extract_default_prompt(
                skill_markdown.parent / "agents" / "openai.yaml"
            )
            if not default_prompt:
                default_prompt = entry["skills"][-1]["instruction_markdown"][:2000]
            entry["skills"][-1]["default_prompt"] = default_prompt

    commands_root = plugin_root / "commands"
    if commands_root.exists():
        for command_markdown in sorted(commands_root.rglob("*.md")):
            if command_markdown.name.endswith(".md.tmpl"):
                continue
            relative = command_markdown.relative_to(commands_root)
            title = _extract_markdown_title(command_markdown)
            frontmatter = _extract_markdown_frontmatter(command_markdown)
            command_name = _sanitize_capability_name(relative) or command_markdown.stem
            command_text = command_markdown.read_text(encoding="utf-8")
            entry["commands"].append(
                {
                    "command": command_name,
                    "description": frontmatter.get("description", "").strip() or title,
                    "workflow_steps": _extract_workflow_steps(command_text),
                    "instruction_markdown": _extract_instruction_markdown(command_markdown),
                    "source_file": str(command_markdown.relative_to(plugin_root)),
                }
            )

    agents_root = plugin_root / "agents"
    if agents_root.exists():
        for agent_file in sorted(agents_root.rglob("*")):
            if not agent_file.is_file() or agent_file.suffix not in {".md", ".yaml", ".yml"}:
                continue
            relative = agent_file.relative_to(agents_root)
            agent_name = _sanitize_capability_name(relative) or agent_file.stem
            default_prompt = ""
            if agent_file.suffix in {".yaml", ".yml"}:
                default_prompt = _extract_default_prompt(agent_file)
            instruction_markdown = ""
            if agent_file.suffix == ".md":
                instruction_markdown = _extract_instruction_markdown(agent_file)
                if not default_prompt:
                    default_prompt = instruction_markdown[:3000]
            title = _extract_markdown_title(agent_file) if agent_file.suffix == ".md" else ""
            description = title or default_prompt
            entry["agents"].append(
                {
                    "agent": agent_name,
                    "description": description.strip(),
                    "default_prompt": default_prompt,
                    "instruction_markdown": instruction_markdown,
                    "source_file": str(agent_file.relative_to(plugin_root)),
                }
            )

    entry["mcp_servers"] = _extract_mcp_entries(plugin_root, plugin_meta)
    entry["skills"] = _merge_unique(entry["skills"], "skill")
    entry["commands"] = _merge_unique(entry["commands"], "command")
    entry["agents"] = _merge_unique(entry["agents"], "agent")
    entry["mcp_servers"] = _merge_unique(entry["mcp_servers"], "server")
    return entry


def build_snapshot(source_roots: list[Path]) -> dict[str, Any]:
    """Build SAGE snapshot shape from one or more legacy plugin roots."""
    merged_by_name: dict[str, dict[str, Any]] = {}

    for source_root in source_roots:
        candidate_roots = _iter_plugin_roots(source_root)
        if not candidate_roots:
            candidate_roots = _list_recent_revision_dirs(source_root)
        for plugin_root in candidate_roots:
            entry = _extract_plugin_entry(plugin_root)
            if entry is None:
                continue
            name = str(entry["name"])
            existing = merged_by_name.get(name)
            if existing is None:
                merged_by_name[name] = entry
                continue
            if not existing.get("description") and entry.get("description"):
                existing["description"] = entry["description"]
            if not existing.get("display_name") and entry.get("display_name"):
                existing["display_name"] = entry["display_name"]
            existing["skills"] = _merge_unique(
                list(existing.get("skills", [])) + list(entry.get("skills", [])),
                "skill",
            )
            existing["commands"] = _merge_unique(
                list(existing.get("commands", [])) + list(entry.get("commands", [])),
                "command",
            )
            existing["agents"] = _merge_unique(
                list(existing.get("agents", [])) + list(entry.get("agents", [])),
                "agent",
            )
            existing["mcp_servers"] = _merge_unique(
                list(existing.get("mcp_servers", [])) + list(entry.get("mcp_servers", [])),
                "server",
            )

    plugins = sorted(merged_by_name.values(), key=lambda item: str(item.get("name", "")))
    # Helpful snapshot-level metadata
    for plugin in plugins:
        skill_count = len(plugin.get("skills", []))
        command_count = len(plugin.get("commands", []))
        agent_count = len(plugin.get("agents", []))
        mcp_count = len(plugin.get("mcp_servers", []))
        plugin["capability_count"] = skill_count + command_count + agent_count + mcp_count

    return {"plugins": plugins}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        action="append",
        required=True,
        help="Legacy plugin root (repeat for multiple roots)",
    )
    parser.add_argument("--output", required=True, help="Snapshot output JSON path")
    args = parser.parse_args()

    source_roots = [Path(item).expanduser() for item in args.source]
    output_path = Path(args.output).expanduser()

    missing = [path for path in source_roots if not path.exists()]
    if missing:
        missing_text = ", ".join(str(path) for path in missing)
        raise SystemExit(f"Source path(s) do not exist: {missing_text}")

    snapshot = build_snapshot(source_roots)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    plugins = len(snapshot.get("plugins", []))
    skills = sum(len(plugin.get("skills", [])) for plugin in snapshot.get("plugins", []))
    commands = sum(len(plugin.get("commands", [])) for plugin in snapshot.get("plugins", []))
    agents = sum(len(plugin.get("agents", [])) for plugin in snapshot.get("plugins", []))
    mcp_servers = sum(len(plugin.get("mcp_servers", [])) for plugin in snapshot.get("plugins", []))
    print(
        "Imported "
        f"{plugins} plugins / {skills} skills / {commands} commands / "
        f"{agents} agents / {mcp_servers} mcp servers -> {output_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
