from __future__ import annotations

import os
import re
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path

import click

from .. import terminal

DEFAULT_TEMPLATE = "default"
EXAMPLES_ARCHIVE_URL = "https://github.com/beam-cloud/capsule-examples/archive/refs/heads/main.zip"
TEXT_EXTENSIONS = {".baml", ".gitignore", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"}


def _project_slug(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")
    return slug or "capsule-app"


def _package_name(slug: str) -> str:
    pkg = slug.replace("-", "_")
    if pkg[0].isdigit():
        pkg = "app_" + pkg
    return pkg


def _repo_root() -> Path:
    # sdk/src/cpsl/cli/create.py -> capsule/
    return Path(__file__).resolve().parents[4]


def _local_examples_dir() -> Path | None:
    root = _repo_root()
    candidates = [
        Path(os.environ["CAPSULE_EXAMPLES_DIR"]).expanduser()
        if os.environ.get("CAPSULE_EXAMPLES_DIR")
        else None,
        Path.cwd() / "capsule-examples",
        Path.cwd().parent / "capsule-examples",
        Path.home() / "beam" / "capsule-examples",
        root.parent / "capsule-examples",
        root / "capsule-examples",
    ]
    for candidate in candidates:
        if candidate is None:
            continue
        if _is_examples_dir(candidate):
            return candidate
        legacy = candidate / "templates"
        if _is_examples_dir(legacy):
            return legacy
    return None


def _is_examples_dir(path: Path) -> bool:
    return (path / DEFAULT_TEMPLATE / "template.yaml").exists() and bool(_template_names(path))


def _template_names(path: Path) -> list[str]:
    if not path.exists():
        return []
    return sorted(
        child.name
        for child in path.iterdir()
        if child.is_dir() and (child / "template.yaml").exists()
    )


def _download_examples_dir(tmp: Path) -> Path:
    archive = tmp / "capsule-examples.zip"
    urllib.request.urlretrieve(EXAMPLES_ARCHIVE_URL, archive)
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(tmp)
    for root in tmp.glob("capsule-examples-*"):
        if _is_examples_dir(root):
            return root
        legacy = root / "templates"
        if _is_examples_dir(legacy):
            return legacy
    raise click.ClickException("Downloaded capsule-examples archive did not contain examples.")


def _examples_dir(tmp: Path) -> Path:
    return _local_examples_dir() or _download_examples_dir(tmp)


def _read_manifest(template_dir: Path) -> dict[str, object]:
    manifest = template_dir / "template.yaml"
    data: dict[str, object] = {"required_secrets": [], "optional_secrets": []}
    if not manifest.exists():
        return data

    current_list: str | None = None
    for raw in manifest.read_text().splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if current_list and stripped.startswith("-"):
            data.setdefault(current_list, [])
            data[current_list].append(stripped[1:].strip().strip('"'))  # type: ignore[index]
            continue
        current_list = None
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            current_list = key
            data[key] = []
        else:
            data[key] = value.strip('"')
    return data


def _copy_template(src: Path, dst: Path, *, force: bool) -> None:
    if dst.exists() and any(dst.iterdir()) and not force:
        raise click.ClickException(f"{dst} already exists and is not empty. Use --force to overwrite.")
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))


def _copy_shared_files(examples_dir: Path, dst: Path) -> None:
    for name in ("SKILL.md",):
        source = examples_dir / name
        if source.exists():
            shutil.copy2(source, dst / name)


def _render_files(root: Path, replacements: dict[str, str]) -> None:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in TEXT_EXTENSIONS and path.name not in TEXT_EXTENSIONS:
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        for key, value in replacements.items():
            text = text.replace("{{ " + key + " }}", value).replace("{{" + key + "}}", value)
        path.write_text(text)


def _has_uv() -> bool:
    return shutil.which("uv") is not None


def _secret_lines(secrets: list[str]) -> list[str]:
    return [f"capsule secret create {name}=..." for name in secrets]


@click.command("create")
@click.argument("name")
@click.option("--template", "template_name", default=DEFAULT_TEMPLATE, show_default=True, help="Template to use.")
@click.option("--force", is_flag=True, help="Overwrite an existing non-empty project directory.")
def create(name: str, template_name: str, force: bool) -> None:
    """Create a production-shaped Capsule project from a template."""
    requested = Path(name).expanduser()
    target = requested if requested.is_absolute() or requested.parent != Path(".") else Path.cwd() / requested
    slug = _project_slug(target.name)
    package = _package_name(slug)

    with tempfile.TemporaryDirectory() as td:
        examples = _examples_dir(Path(td))
        available = _template_names(examples)
        if template_name not in available:
            valid = ", ".join(available) if available else "none found"
            raise click.ClickException(f"Unknown template {template_name!r}. Choose one of: {valid}.")
        source = examples / template_name
        manifest = _read_manifest(source)
        _copy_template(source, target, force=force)
        _copy_shared_files(examples, target)

    replacements = {
        "project_name": name,
        "project_slug": slug,
        "package_name": package,
        "template_name": template_name,
    }
    _render_files(target, replacements)

    entrypoint = str(manifest.get("entrypoint") or "app.py:app")
    required = list(manifest.get("required_secrets") or [])
    channels = list(manifest.get("required_channels") or [])

    terminal.header("Created Capsule app", f"[bold]{slug}[/bold]")
    terminal.detail(f"  template: {template_name}")
    terminal.detail(f"  entry:    {entrypoint}")
    terminal.info("")
    terminal.info("Next steps:")
    terminal.info(f"  cd {target}")
    terminal.info("  uv sync" if _has_uv() else "  pip install -e .")
    if required:
        terminal.info("")
        terminal.info("Add secrets before using the app:")
        for line in _secret_lines(required):
            terminal.info(f"  {line}")
    else:
        terminal.info("")
        terminal.info("No secrets required for this template.")
    if channels:
        terminal.info("")
        terminal.info("Add channels before using external chat:")
        for line in channels:
            terminal.info(f"  {line}")
    terminal.info("")
    terminal.info("Run locally:")
    terminal.info(f"  capsule serve {entrypoint}")
    terminal.info("")
    terminal.info("Deploy when ready:")
    terminal.info(f"  capsule deploy {entrypoint}")
    terminal.info("")
    terminal.url("https://docs.capsule.new")
