"""Registry API for community component browser.

Provides endpoints to:
- Browse the community registry from GitHub
- List installed components
- Install/uninstall components
"""

import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/registry", tags=["registry"])

# GitHub raw URL base for the registry
GITHUB_REPO = "mendyEdri/emdash-registry"
GITHUB_BRANCH = "main"
REGISTRY_BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}"

ComponentType = Literal["skill", "rule", "agent", "verifier", "plugin"]


# ─────────────────────────────────────────────────────────────────────────────
# Request/Response Models
# ─────────────────────────────────────────────────────────────────────────────

class InstallRequest(BaseModel):
    component_type: ComponentType
    name: str


class UninstallRequest(BaseModel):
    plugin_name: str


class InstalledPlugin(BaseModel):
    name: str
    version: str
    description: str
    installed_at: str
    components: dict[str, list[str]]
    hook_ids: list[str]


# ─────────────────────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────────────────────

def _get_emdash_dir() -> Path:
    """Get the .emdash directory."""
    return Path.cwd() / ".emdash"


def _fetch_registry() -> dict | None:
    """Fetch the registry.json from GitHub."""
    url = f"{REGISTRY_BASE_URL}/registry.json"
    try:
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def _fetch_component(path: str) -> str | None:
    """Fetch a component file from GitHub."""
    url = f"{REGISTRY_BASE_URL}/{path}"
    try:
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception:
        return None


def _get_plugins_file_path() -> Path:
    """Get the path to the plugins.json file."""
    return _get_emdash_dir() / "plugins.json"


def _load_plugins_file() -> dict:
    """Load the plugins.json file."""
    plugins_file = _get_plugins_file_path()
    if not plugins_file.exists():
        return {"plugins": {}}
    try:
        return json.loads(plugins_file.read_text())
    except Exception:
        return {"plugins": {}}


def _save_plugins_file(data: dict) -> None:
    """Save the plugins.json file."""
    file_path = _get_plugins_file_path()
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(data, indent=2) + "\n")


def _install_skill(name: str, content: str) -> bool:
    """Install a skill to .emdash/skills/."""
    skill_dir = _get_emdash_dir() / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(content)
    return True


def _install_rule(name: str, content: str) -> bool:
    """Install a rule to .emdash/rules/."""
    rules_dir = _get_emdash_dir() / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    rule_file = rules_dir / f"{name}.md"
    rule_file.write_text(content)
    return True


def _install_agent(name: str, content: str) -> bool:
    """Install an agent to .emdash/agents/."""
    agents_dir = _get_emdash_dir() / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    agent_file = agents_dir / f"{name}.md"
    agent_file.write_text(content)
    return True


def _install_verifier(name: str, content: str) -> bool:
    """Install a verifier to .emdash/verifiers.json."""
    verifiers_file = _get_emdash_dir() / "verifiers.json"

    if verifiers_file.exists():
        existing = json.loads(verifiers_file.read_text())
    else:
        _get_emdash_dir().mkdir(parents=True, exist_ok=True)
        existing = {"verifiers": [], "max_attempts": 3}

    new_verifier = json.loads(content)
    existing_names = [v.get("name") for v in existing.get("verifiers", [])]

    if name in existing_names:
        existing["verifiers"] = [
            new_verifier if v.get("name") == name else v
            for v in existing["verifiers"]
        ]
    else:
        existing["verifiers"].append(new_verifier)

    verifiers_file.write_text(json.dumps(existing, indent=2))
    return True


def _remove_skill(name: str) -> bool:
    """Remove a skill from .emdash/skills/."""
    skill_dir = _get_emdash_dir() / "skills" / name
    if skill_dir.exists():
        shutil.rmtree(skill_dir)
        return True
    return False


def _remove_rule(name: str) -> bool:
    """Remove a rule from .emdash/rules/."""
    rule_file = _get_emdash_dir() / "rules" / f"{name}.md"
    if rule_file.exists():
        rule_file.unlink()
        return True
    return False


def _remove_agent(name: str) -> bool:
    """Remove an agent from .emdash/agents/."""
    agent_file = _get_emdash_dir() / "agents" / f"{name}.md"
    if agent_file.exists():
        agent_file.unlink()
        return True
    return False


def _remove_verifier(name: str) -> bool:
    """Remove a verifier from .emdash/verifiers.json."""
    verifiers_file = _get_emdash_dir() / "verifiers.json"
    if not verifiers_file.exists():
        return False

    try:
        existing = json.loads(verifiers_file.read_text())
        original_count = len(existing.get("verifiers", []))
        existing["verifiers"] = [
            v for v in existing.get("verifiers", [])
            if v.get("name") != name
        ]
        if len(existing["verifiers"]) < original_count:
            verifiers_file.write_text(json.dumps(existing, indent=2))
            return True
    except Exception:
        pass
    return False


def _add_plugin_hook(hook: dict, plugin_name: str) -> str | None:
    """Add a hook from a plugin. Returns the hook ID or None on failure."""
    hooks_file = _get_emdash_dir() / "hooks.json"

    if hooks_file.exists():
        try:
            hooks_data = json.loads(hooks_file.read_text())
        except json.JSONDecodeError:
            hooks_data = {"hooks": []}
    else:
        _get_emdash_dir().mkdir(parents=True, exist_ok=True)
        hooks_data = {"hooks": []}

    hook_id = f"{plugin_name}-{hook.get('event', '')}-{len(hooks_data['hooks'])}"
    existing_ids = [h.get("id") for h in hooks_data.get("hooks", [])]
    while hook_id in existing_ids:
        hook_id = f"{plugin_name}-{hook.get('event', '')}-{len(hooks_data['hooks']) + 1}"

    hook_entry = {
        "id": hook_id,
        "event": hook.get("event", ""),
        "command": hook.get("command", ""),
        "enabled": True,
        "plugin": plugin_name,
    }
    if hook.get("timeout"):
        hook_entry["timeout"] = hook["timeout"]
    if hook.get("working_dir"):
        hook_entry["working_dir"] = hook["working_dir"]

    hooks_data["hooks"].append(hook_entry)
    hooks_file.write_text(json.dumps(hooks_data, indent=2) + "\n")

    return hook_id


def _remove_plugin_hooks(hook_ids: list[str]) -> None:
    """Remove hooks by their IDs."""
    hooks_file = _get_emdash_dir() / "hooks.json"
    if not hooks_file.exists():
        return

    try:
        hooks_data = json.loads(hooks_file.read_text())
        hooks_data["hooks"] = [
            h for h in hooks_data.get("hooks", [])
            if h.get("id") not in hook_ids
        ]
        hooks_file.write_text(json.dumps(hooks_data, indent=2) + "\n")
    except Exception:
        pass


def _parse_plugin_manifest(content: str) -> dict | None:
    """Parse a PLUGIN.md file and extract the manifest from frontmatter."""
    import yaml

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None

    try:
        frontmatter = yaml.safe_load(match.group(1))
        if not frontmatter:
            return None
        return frontmatter
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# API Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@router.get("")
async def get_registry():
    """Fetch the community registry from GitHub."""
    registry = _fetch_registry()
    if not registry:
        raise HTTPException(status_code=503, detail="Failed to fetch registry")
    return registry


@router.get("/installed")
async def get_installed():
    """Get list of installed plugins and components."""
    plugins_data = _load_plugins_file()

    # Also scan for individually installed components
    emdash_dir = _get_emdash_dir()
    installed = {
        "plugins": plugins_data.get("plugins", {}),
        "skills": [],
        "rules": [],
        "agents": [],
        "verifiers": [],
    }

    # Scan skills directory
    skills_dir = emdash_dir / "skills"
    if skills_dir.exists():
        installed["skills"] = [d.name for d in skills_dir.iterdir() if d.is_dir()]

    # Scan rules directory
    rules_dir = emdash_dir / "rules"
    if rules_dir.exists():
        installed["rules"] = [f.stem for f in rules_dir.glob("*.md")]

    # Scan agents directory
    agents_dir = emdash_dir / "agents"
    if agents_dir.exists():
        installed["agents"] = [f.stem for f in agents_dir.glob("*.md")]

    # Scan verifiers
    verifiers_file = emdash_dir / "verifiers.json"
    if verifiers_file.exists():
        try:
            verifiers_data = json.loads(verifiers_file.read_text())
            installed["verifiers"] = [
                v.get("name") for v in verifiers_data.get("verifiers", [])
                if v.get("name")
            ]
        except Exception:
            pass

    return installed


@router.post("/install")
async def install_component(request: InstallRequest):
    """Install a component from the registry."""
    registry = _fetch_registry()
    if not registry:
        raise HTTPException(status_code=503, detail="Failed to fetch registry")

    ctype = request.component_type
    name = request.name

    # Handle plugin installation
    if ctype == "plugin":
        return await _install_plugin_api(name, registry)

    # Get component info
    type_plural = ctype + "s" if not ctype.endswith("s") else ctype
    components = registry.get(type_plural, {})

    if name not in components:
        raise HTTPException(status_code=404, detail=f"{ctype} '{name}' not found")

    info = components[name]
    content = _fetch_component(info["path"])

    if not content:
        raise HTTPException(status_code=503, detail="Failed to fetch component content")

    installers = {
        "skill": _install_skill,
        "rule": _install_rule,
        "agent": _install_agent,
        "verifier": _install_verifier,
    }

    installer = installers.get(ctype)
    if not installer:
        raise HTTPException(status_code=400, detail=f"Unknown component type: {ctype}")

    try:
        installer(name, content)
        return {"success": True, "message": f"Installed {ctype}:{name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _install_plugin_api(name: str, registry: dict) -> dict:
    """Install a plugin and all its components."""
    plugins = registry.get("plugins", {})
    if name not in plugins:
        raise HTTPException(status_code=404, detail=f"Plugin '{name}' not found")

    plugin_info = plugins[name]
    plugin_path = plugin_info.get("path", f"plugins/{name}/PLUGIN.md")

    # Check if already installed
    plugins_file_data = _load_plugins_file()
    if name in plugins_file_data.get("plugins", {}):
        raise HTTPException(status_code=400, detail=f"Plugin '{name}' is already installed")

    # Fetch PLUGIN.md
    content = _fetch_component(plugin_path)
    if not content:
        raise HTTPException(status_code=503, detail="Failed to fetch plugin manifest")

    # Parse manifest
    manifest = _parse_plugin_manifest(content)
    if not manifest:
        raise HTTPException(status_code=400, detail="Invalid plugin manifest")

    # Save PLUGIN.md
    plugin_dir = _get_emdash_dir() / "plugins" / name
    plugin_dir.mkdir(parents=True, exist_ok=True)
    (plugin_dir / "PLUGIN.md").write_text(content)

    # Track installed components
    installed_components: dict[str, list[str]] = {
        "skills": [],
        "rules": [],
        "agents": [],
        "verifiers": [],
    }
    installed_hook_ids: list[str] = []
    plugin_base_path = f"plugins/{name}"

    components_data = manifest.get("components", {})

    # Install skills
    for skill_name in components_data.get("skills", []):
        embedded_path = f"{plugin_base_path}/skills/{skill_name}/SKILL.md"
        skill_content = _fetch_component(embedded_path)

        if not skill_content:
            skill_info = registry.get("skills", {}).get(skill_name)
            if skill_info:
                skill_content = _fetch_component(skill_info["path"])

        if skill_content:
            _install_skill(skill_name, skill_content)
            installed_components["skills"].append(skill_name)

    # Install rules
    for rule_name in components_data.get("rules", []):
        embedded_path = f"{plugin_base_path}/rules/{rule_name}.md"
        rule_content = _fetch_component(embedded_path)

        if not rule_content:
            rule_info = registry.get("rules", {}).get(rule_name)
            if rule_info:
                rule_content = _fetch_component(rule_info["path"])

        if rule_content:
            _install_rule(rule_name, rule_content)
            installed_components["rules"].append(rule_name)

    # Install agents
    for agent_name in components_data.get("agents", []):
        embedded_path = f"{plugin_base_path}/agents/{agent_name}.md"
        agent_content = _fetch_component(embedded_path)

        if not agent_content:
            agent_info = registry.get("agents", {}).get(agent_name)
            if agent_info:
                agent_content = _fetch_component(agent_info["path"])

        if agent_content:
            _install_agent(agent_name, agent_content)
            installed_components["agents"].append(agent_name)

    # Install verifiers
    for verifier_name in components_data.get("verifiers", []):
        embedded_path = f"{plugin_base_path}/verifiers/{verifier_name}.json"
        verifier_content = _fetch_component(embedded_path)

        if not verifier_content:
            verifier_info = registry.get("verifiers", {}).get(verifier_name)
            if verifier_info:
                verifier_content = _fetch_component(verifier_info["path"])

        if verifier_content:
            _install_verifier(verifier_name, verifier_content)
            installed_components["verifiers"].append(verifier_name)

    # Install hooks
    for hook in components_data.get("hooks", []):
        if isinstance(hook, dict):
            hook_id = _add_plugin_hook(hook, name)
            if hook_id:
                installed_hook_ids.append(hook_id)

    # Save plugin record
    plugins_file_data["plugins"][name] = {
        "name": name,
        "version": manifest.get("version", "1.0.0"),
        "description": manifest.get("description", ""),
        "installed_at": datetime.now().isoformat(),
        "components": installed_components,
        "hook_ids": installed_hook_ids,
    }
    _save_plugins_file(plugins_file_data)

    total = sum(len(v) for v in installed_components.values()) + len(installed_hook_ids)
    return {
        "success": True,
        "message": f"Plugin '{name}' installed ({total} components)",
        "components": installed_components,
    }


@router.delete("/uninstall/{plugin_name}")
async def uninstall_plugin(plugin_name: str):
    """Uninstall a plugin and all its components."""
    plugins_file_data = _load_plugins_file()

    if plugin_name not in plugins_file_data.get("plugins", {}):
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_name}' is not installed")

    plugin = plugins_file_data["plugins"][plugin_name]
    removed_count = 0

    # Remove skills
    for skill_name in plugin.get("components", {}).get("skills", []):
        if _remove_skill(skill_name):
            removed_count += 1

    # Remove rules
    for rule_name in plugin.get("components", {}).get("rules", []):
        if _remove_rule(rule_name):
            removed_count += 1

    # Remove agents
    for agent_name in plugin.get("components", {}).get("agents", []):
        if _remove_agent(agent_name):
            removed_count += 1

    # Remove verifiers
    for verifier_name in plugin.get("components", {}).get("verifiers", []):
        if _remove_verifier(verifier_name):
            removed_count += 1

    # Remove hooks
    hook_ids = plugin.get("hook_ids", [])
    if hook_ids:
        _remove_plugin_hooks(hook_ids)
        removed_count += len(hook_ids)

    # Remove plugin directory
    plugin_dir = _get_emdash_dir() / "plugins" / plugin_name
    if plugin_dir.exists():
        shutil.rmtree(plugin_dir)

    # Remove from plugins.json
    del plugins_file_data["plugins"][plugin_name]
    _save_plugins_file(plugins_file_data)

    return {
        "success": True,
        "message": f"Plugin '{plugin_name}' uninstalled ({removed_count} components removed)",
    }


@router.get("/component/{component_type}/{name}")
async def get_component(component_type: ComponentType, name: str):
    """Get details of a specific component."""
    registry = _fetch_registry()
    if not registry:
        raise HTTPException(status_code=503, detail="Failed to fetch registry")

    type_plural = component_type + "s" if not component_type.endswith("s") else component_type
    components = registry.get(type_plural, {})

    if name not in components:
        raise HTTPException(status_code=404, detail=f"{component_type} '{name}' not found")

    info = components[name]
    content = _fetch_component(info["path"])

    result = {
        "name": name,
        "type": component_type,
        **info,
        "content": content,
    }

    # For plugins, parse and include manifest details
    if component_type == "plugin" and content:
        manifest = _parse_plugin_manifest(content)
        if manifest:
            result["manifest"] = manifest

    return result
