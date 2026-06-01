"""Preflight checks for services targeted by csrd-utils feature augmentation."""

from dataclasses import dataclass, field
from pathlib import Path

from .compose.loader import load_spec


@dataclass
class DoctorReport:
    """Structured doctor output."""

    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def run_doctor(service_root: Path) -> DoctorReport:
    """Validate that a service is compatible with feature augmentation."""
    root = service_root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    required_files = ["requirements.txt", "pyproject.toml"]

    compose_candidates = [root / "docker-compose.yml"]
    parent_is_workspace = root.parent.name == "src" and (
        (root.parent.parent / ".csrd-workspace").is_file()
        or (root.parent.parent / "csrd-compose.yaml").is_file()
    )
    if parent_is_workspace:
        compose_candidates.append(root.parent.parent / "docker-compose.yml")

    for rel in required_files:
        if not (root / rel).is_file():
            errors.append(f"Missing required file: {rel}")

    if not any(path.is_file() for path in compose_candidates):
        errors.append("Missing required file: docker-compose.yml")

    # Find the service package dir — check src/ layout first, then flat layout
    src_dir = root / "src"
    pkg_dir = root if (root / "__init__.py").is_file() else None
    if src_dir.is_dir():
        pkg_dir = next(
            (
                p
                for p in src_dir.iterdir()
                if p.is_dir() and not p.name.startswith(".") and (p / "__init__.py").is_file()
            ),
            None,
        )
    if pkg_dir is None:
        pkg_dir = next(
            (
                p
                for p in root.iterdir()
                if p.is_dir()
                and not p.name.startswith(".")
                and p.name not in {"tests", "src"}
                and (p / "__init__.py").is_file()
            ),
            None,
        )

    marker_files: dict[str, str] = {}
    if pkg_dir is not None:
        marker_files[f"{pkg_dir.name}/settings.py"] = "# [INSERT: fields]"
    workspace_root = root.parent.parent if parent_is_workspace else None

    if workspace_root is not None and pkg_dir is not None:
        marker_files[f"tests/acceptance/{pkg_dir.name}/conftest.py"] = "# [INSERT: fixtures]"
    else:
        marker_files["tests/conftest.py"] = "# [INSERT: fixtures]"

    for rel, marker in marker_files.items():
        path = (
            (workspace_root / rel)
            if workspace_root is not None and rel.startswith("tests/")
            else (root / rel)
        )
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if marker not in text:
                warnings.append(f"Optional insertion marker missing in {rel}: {marker}")

    # Workspace-aware realtime integration warning (v1 direct-connect mode).
    if workspace_root is not None and pkg_dir is not None:
        spec_path = workspace_root / "csrd-compose.yaml"
        if spec_path.is_file():
            try:
                spec = load_spec(spec_path)
            except Exception:
                spec = None

            if spec is not None:
                service_match = next(
                    (svc for svc in spec.services if svc.name.replace("-", "_") == pkg_dir.name),
                    None,
                )
                has_gateway = any(svc.role == "gateway" for svc in spec.services)
                if service_match is not None:
                    has_realtime = any(
                        aug.name == "realtime-websocket" for aug in service_match.augments
                    )
                    if has_realtime and has_gateway:
                        warnings.append(
                            "Workspace includes a gateway and this service enables "
                            "'realtime-websocket'. In v1, websocket traffic is "
                            "direct-to-service (gateway WS proxy is not supported yet)."
                        )

    return DoctorReport(ok=not errors, errors=errors, warnings=warnings)
