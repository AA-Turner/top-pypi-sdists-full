from __future__ import annotations

from collections.abc import Mapping
import os
from pathlib import Path
from urllib.parse import quote


EnvMapping = Mapping[str, str]
_DEFAULT_AEGIS_HOME = Path.home() / ".aegis"


def _environ(environ: EnvMapping | None = None) -> EnvMapping:
    return environ if environ is not None else os.environ


def default_install_root(*, environ: EnvMapping | None = None) -> Path:
    env = _environ(environ)
    override = env.get("AEGIS_HOME")
    if override:
        return Path(override).expanduser()
    return _DEFAULT_AEGIS_HOME


def default_cli_state_dir(*, environ: EnvMapping | None = None) -> Path:
    env = _environ(environ)
    override = env.get("AEGIS_STATE_DIR")
    if override:
        return Path(override).expanduser()
    return default_install_root(environ=env) / "state"


def default_profile_dir(*, environ: EnvMapping | None = None) -> Path:
    env = _environ(environ)
    override = env.get("AEGIS_PROFILE_DIR")
    if override:
        return Path(override).expanduser()
    return default_install_root(environ=env) / "profile"


def default_gateway_state_dir(*, environ: EnvMapping | None = None) -> Path:
    env = _environ(environ)
    override = env.get("AEGIS_GATEWAY_STATE_DIR")
    if override:
        return Path(override).expanduser()
    return default_install_root(environ=env) / "state" / "gateway"


def default_skills_dir(*, environ: EnvMapping | None = None, install_root: Path | None = None) -> Path:
    env = _environ(environ)
    override = env.get("AEGIS_SKILLS_DIR")
    if override:
        return Path(override).expanduser()
    root = install_root.expanduser() if install_root is not None else default_install_root(environ=env)
    return root / "skills"


def default_builtin_skills_dir(
    *,
    environ: EnvMapping | None = None,
    install_root: Path | None = None,
) -> Path:
    env = _environ(environ)
    override = env.get("AEGIS_BUILTIN_SKILLS_DIR")
    if override:
        return Path(override).expanduser()
    return default_skills_dir(environ=env, install_root=install_root) / "builtin"


def default_installed_skills_dir(
    *,
    environ: EnvMapping | None = None,
    install_root: Path | None = None,
) -> Path:
    env = _environ(environ)
    override = env.get("AEGIS_INSTALLED_SKILLS_DIR") or env.get("AEGIS_SHARED_SKILLS_DIR")
    if override:
        return Path(override).expanduser()
    return default_skills_dir(environ=env, install_root=install_root) / "installed"


def default_authored_skills_dir(
    *,
    environ: EnvMapping | None = None,
    install_root: Path | None = None,
) -> Path:
    env = _environ(environ)
    override = env.get("AEGIS_AUTHORED_SKILLS_DIR")
    if override:
        return Path(override).expanduser()
    return default_skills_dir(environ=env, install_root=install_root) / "authored"


def default_skill_search_cache_dir(
    *,
    environ: EnvMapping | None = None,
    install_root: Path | None = None,
) -> Path:
    env = _environ(environ)
    override = env.get("AEGIS_SKILL_SEARCH_CACHE_DIR")
    if override:
        return Path(override).expanduser()
    return default_skills_dir(environ=env, install_root=install_root) / ".cache" / "search"


def default_cron_dir(*, environ: EnvMapping | None = None, install_root: Path | None = None) -> Path:
    env = _environ(environ)
    override = env.get("AEGIS_CRON_DIR")
    if override:
        return Path(override).expanduser()
    root = install_root.expanduser() if install_root is not None else default_install_root(environ=env)
    return root / "cron"


def default_workspace_dir(*, environ: EnvMapping | None = None, install_root: Path | None = None) -> Path:
    env = _environ(environ)
    override = env.get("AEGIS_WORKSPACE_DIR")
    if override:
        return Path(override).expanduser()
    root = install_root.expanduser() if install_root is not None else default_install_root(environ=env)
    return root / "workspaces"


def default_pairing_dir(*, environ: EnvMapping | None = None, install_root: Path | None = None) -> Path:
    env = _environ(environ)
    override = env.get("AEGIS_PAIRING_DIR")
    if override:
        return Path(override).expanduser()
    root = install_root.expanduser() if install_root is not None else default_install_root(environ=env)
    return root / "pairing"


def workspace_path_for_clone(
    clone_id: str,
    *,
    environ: EnvMapping | None = None,
    install_root: Path | None = None,
) -> Path:
    key = quote(clone_id.strip(), safe="")
    if not key:
        raise ValueError("clone id is required")
    return default_workspace_dir(environ=environ, install_root=install_root) / key


def infer_install_root_from_runtime_paths(
    *,
    state_dir: Path,
    profile_dir: Path,
    environ: EnvMapping | None = None,
) -> Path:
    env = _environ(environ)
    override = env.get("AEGIS_HOME")
    if override:
        return Path(override).expanduser()
    resolved_state = state_dir.expanduser().resolve()
    resolved_profile = profile_dir.expanduser().resolve()
    state_parent = resolved_state.parent
    profile_parent = resolved_profile.parent
    if state_parent == profile_parent:
        return state_parent
    if resolved_state.name == "gateway" and state_parent.parent == profile_parent:
        return profile_parent
    return default_install_root(environ=env)


__all__ = [
    "default_authored_skills_dir",
    "default_builtin_skills_dir",
    "default_cli_state_dir",
    "default_cron_dir",
    "default_gateway_state_dir",
    "default_install_root",
    "default_installed_skills_dir",
    "default_pairing_dir",
    "default_profile_dir",
    "default_skill_search_cache_dir",
    "default_skills_dir",
    "default_workspace_dir",
    "infer_install_root_from_runtime_paths",
    "workspace_path_for_clone",
]
