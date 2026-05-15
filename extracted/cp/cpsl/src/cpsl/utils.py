"""Shared utilities for CLI commands (deploy, serve)."""

import importlib
import json
import os
import sys
import tempfile
import zipfile
from importlib import metadata
from pathlib import Path
from typing import Any

from . import terminal

IGNORE_PATTERNS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    ".DS_Store",
    ".idea",
    ".vscode",
    ".env.local",
    ".envrc",
    ".next",
    ".capsuleignore",
    ".capsule",
}

IGNORE_EXTENSIONS = {".pyc"}
PAGE_BUNDLE_CACHE_DIR = Path(".capsule") / "cache" / "page-bundles"


def resolve_entry_point(entry_point: str) -> dict:
    """Import the entry point module, resolve the target, and return
    its ``_cpsl_config`` dict.

    The target can be a class decorated with ``@app.cls`` or a functional
    ``App`` instance.  Accepts formats like ``app.py:MyAgent``,
    ``app.py:app``, or ``examples/echo/app.py:app``.
    """
    from .app import App

    if ":" not in entry_point:
        terminal.error("Invalid entry point. Expected format: capsule <command> <file.py>:<name>")

    module_path, target_name = entry_point.rsplit(":", 1)
    if not target_name:
        terminal.error("Invalid entry point. Expected format: capsule <command> <file.py>:<name>")

    file_path = Path(module_path)
    if file_path.parent != Path("."):
        os.chdir(file_path.parent)
        module_name = file_path.stem
    else:
        module_name = module_path.replace(".py", "")

    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

    try:
        mod = importlib.import_module(module_name)
    except ImportError as e:
        terminal.error(f"Cannot import '{module_path}': {e}")

    obj = getattr(mod, target_name, None)
    if obj is None:
        terminal.error(f"'{target_name}' not found in module '{module_path}'")

    if isinstance(obj, App):
        obj._finalize_config()
        cfg = obj._cpsl_config
        if cfg.get("module") is None:
            cfg["module"] = module_name
        return cfg

    config = getattr(obj, "_cpsl_config", None)
    if config is None:
        terminal.error(
            f"'{target_name}' is not a functional App or a class decorated with @app.cls"
        )

    return config


def should_ignore(name: str) -> bool:
    """Return True if *name* matches an ignore pattern or extension."""
    if name in IGNORE_PATTERNS:
        return True
    return any(name.endswith(ext) for ext in IGNORE_EXTENSIONS)


def collect_source_archive(extra_files: list[Path] | None = None) -> bytes:
    """ZIP the current working directory, respecting ignore patterns."""
    root = Path.cwd()
    root_resolved = root.resolve()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    tmp.close()
    file_count = 0
    archived: set[str] = set()

    try:
        with zipfile.ZipFile(tmp.name, "w", zipfile.ZIP_DEFLATED) as zf:
            for dirpath, dirnames, filenames in os.walk(root):
                dirnames[:] = [d for d in dirnames if not should_ignore(d)]
                for fname in filenames:
                    if should_ignore(fname):
                        continue
                    full = os.path.join(dirpath, fname)
                    rel = os.path.relpath(full, root)
                    zf.write(full, rel)
                    archived.add(rel)
                    terminal.detail(f"  + {rel}")
                    file_count += 1

            for path in extra_files or []:
                full_path = (root / path).resolve() if not path.is_absolute() else path.resolve()
                try:
                    rel = full_path.relative_to(root_resolved).as_posix()
                except ValueError:
                    continue
                if rel in archived or not full_path.is_file():
                    continue
                zf.write(full_path, rel)
                archived.add(rel)
                terminal.detail(f"  + {rel}")
                file_count += 1

        data = Path(tmp.name).read_bytes()
        terminal.detail(
            f"  {file_count} file{'' if file_count == 1 else 's'}, "
            f"{terminal.humanize_memory(len(data), base=10)}"
        )
        return data
    finally:
        os.unlink(tmp.name)


def react_page_bundle_specs(config: dict[str, Any]) -> list[tuple[str, str, list[str]]]:
    specs: list[tuple[str, str, list[str]]] = []
    for page in config.get("pages", []):
        if page.get("type") == "react" and page.get("component"):
            specs.append((page["name"], page["component"], list(page.get("packages") or [])))

    onboarding = config.get("onboarding")
    if onboarding and onboarding.get("type") == "react" and onboarding.get("component"):
        specs.append((
            "__onboarding__",
            onboarding["component"],
            list(onboarding.get("packages") or []),
        ))

    return specs


def build_react_page_bundle_cache(config: dict[str, Any]) -> list[Path]:
    specs = react_page_bundle_specs(config)
    if not specs:
        return []

    from .page_bundle import build_page_bundle

    paths: list[Path] = []
    terminal.header("Building page bundles")
    for name, component, packages in specs:
        try:
            result = build_page_bundle(component, packages)
        except Exception as exc:
            terminal.detail(f"  ! {name}: {exc}")
            continue
        state = "cached" if result.cached else "built"
        terminal.detail(f"  + {name} ({state})")
        paths.append(result.path)
    return paths


def _pip_package_name(spec: str) -> str:
    for i, c in enumerate(spec.strip()):
        if c in "=<>!~[ ":
            return spec[:i].strip().lower()
    return spec.strip().lower()


def _local_sdk_version() -> str | None:
    pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
    try:
        for line in pyproject.read_text().splitlines():
            line = line.strip()
            if line.startswith("version = "):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass

    try:
        return metadata.version("cpsl")
    except metadata.PackageNotFoundError:
        return None

    return None


def normalize_image(image: dict) -> dict:
    normalized = {
        "python_packages": list(image.get("python_packages", [])),
        "apt_packages": list(image.get("apt_packages", [])),
        "commands": list(image.get("commands", [])),
    }

    if not any(_pip_package_name(pkg) == "cpsl" for pkg in normalized["python_packages"]):
        version = _local_sdk_version()
        if version:
            normalized["python_packages"].insert(0, f"cpsl=={version}")

    return normalized


def build_image_spec(image: dict, *, cpu: float = 0.25, memory: int = 512, gpu: str | None = None):
    """Build a gRPC ``ImageSpec`` from the config dict."""
    from .clients.capsule import ImageSpec

    image = normalize_image(image)
    return ImageSpec(
        python_packages=image.get("python_packages", []),
        apt_packages=image.get("apt_packages", []),
        commands=image.get("commands", []),
        cpu=cpu,
        memory_mib=memory,
        gpu=gpu or "",
    )


def build_channel_specs(channels: list[dict]):
    """Build a list of gRPC ``ChannelSpec`` from channel config dicts.

    Handles both built-in types (chat, api) and named resource references
    (type="_resource", name="my-channel").
    """
    from .clients.capsule import ChannelSpec

    return [
        ChannelSpec(
            type=ch["type"],
            config={
                k: (json.dumps(v) if isinstance(v, dict) else str(v))
                for k, v in ch.items()
                if k != "type"
            },
        )
        for ch in channels
    ]


def build_integration_specs(integrations: list[dict]):
    """Build a list of gRPC ``IntegrationSpec`` from integration config dicts."""
    from .clients.capsule import IntegrationSpec

    return [
        IntegrationSpec(
            type=ig["type"],
            scopes=ig.get("scopes", []),
            client_id_secret=ig.get("client_id_secret", ""),
            client_secret_secret=ig.get("client_secret_secret", ""),
            mode=ig.get("mode", "oauth"),
            fields=ig.get("fields", []),
        )
        for ig in integrations
    ]


def build_schedule_specs(schedules: list[dict]):
    """Build a list of gRPC ``ScheduleSpec`` from schedule config dicts."""
    from .clients.capsule import ScheduleSpec

    return [ScheduleSpec(name=s["name"], cron=s["cron"]) for s in schedules]


def build_filesystem_mount_specs(filesystems: dict[str, dict]):
    """Build gRPC filesystem mount specs from App config."""
    from .clients.capsule import (
        FilesystemMountSpec,
        FilesystemSourceSpec,
        FilesystemToolSpec,
    )

    specs = []
    for mount_path, fs in filesystems.items():
        sources = []
        for source in fs.get("sources", []):
            filter_value = source.get("filter", "")
            if isinstance(filter_value, dict):
                filter_value = json.dumps(filter_value)
            sources.append(
                FilesystemSourceSpec(
                    mode=source.get("mode", "smart"),
                    integration=source.get("integration", ""),
                    name=source.get("name", ""),
                    guidance=source.get("guidance", ""),
                    filter=str(filter_value) if filter_value else "",
                    output_format=source.get("output_format", "folder"),
                    file_ext=source.get("file_ext", ""),
                    filename_format=source.get("filename_format", ""),
                    cache_ttl=int(source.get("cache_ttl", 0)),
                )
            )

        tools = []
        for tool in fs.get("tools", []):
            config = {k: v for k, v in tool.items() if k not in {"kind", "name"}}
            tools.append(
                FilesystemToolSpec(
                    kind=tool.get("kind", "tool"),
                    name=tool.get("name", ""),
                    config_json=json.dumps(config).encode(),
                )
            )

        specs.append(
            FilesystemMountSpec(
                mount_path=mount_path,
                name=fs.get("name", ""),
                sources=sources,
                tools=tools,
            )
        )
    return specs
