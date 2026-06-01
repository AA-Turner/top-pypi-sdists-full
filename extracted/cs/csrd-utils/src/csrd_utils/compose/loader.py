"""Load/save helpers for `csrd-compose.yaml`."""

from pathlib import Path

from ..models import ComposeSpec, WorkspaceConfig
from .yaml_editor import dumps_yaml, load_yaml

SPEC_FILENAME = "csrd-compose.yaml"


def spec_file_path(output_dir: Path) -> Path:
    """Return the canonical spec path for a workspace directory."""

    return output_dir / SPEC_FILENAME


def default_spec(workspace_dir: Path) -> ComposeSpec:
    """Build a default baseline spec for an empty workspace."""

    return ComposeSpec(workspace=WorkspaceConfig(name=workspace_dir.name or "workspace"))


def load_spec(spec_path: Path) -> ComposeSpec:
    """Load and validate a compose spec from disk."""

    if not spec_path.is_file():
        raise FileNotFoundError(f"Compose spec file not found: {spec_path}")

    raw = load_yaml(spec_path)
    return ComposeSpec.model_validate(raw)


def save_spec(spec: ComposeSpec, spec_path: Path) -> None:
    """Persist a compose spec to disk with stable key ordering."""

    spec_path.parent.mkdir(parents=True, exist_ok=True)
    payload = spec.model_dump(mode="python")
    spec_path.write_text(dumps_yaml(payload), encoding="utf-8")
