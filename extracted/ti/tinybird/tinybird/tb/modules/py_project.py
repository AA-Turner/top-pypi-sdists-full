import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project

PY_CONFIG_FILES = (
    "tinybird.config.py",
    "tinybird_config.py",
    "tinybird.config.json",
    "tinybird.json",
)


@dataclass
class PythonVirtualProject:
    project: Project
    temp_dir: tempfile.TemporaryDirectory[str]
    config_path: Path


def find_python_config_file(start_dir: Path) -> Optional[Path]:
    current = start_dir.resolve()
    while True:
        for filename in PY_CONFIG_FILES:
            candidate = current / filename
            if candidate.exists():
                return candidate
        if current.parent == current:
            return None
        current = current.parent


def _sdk_generator_python_script() -> str:
    return """
import dataclasses
import importlib
import json
import os
import sys
from pathlib import Path

cwd = sys.argv[1]
sdk_path = os.environ.get("TB_PYTHON_SDK_PATH")

if sdk_path:
    normalized_sdk_path = sdk_path[:-1] if sdk_path.endswith("/") else sdk_path
    candidates = [Path(normalized_sdk_path), Path(normalized_sdk_path) / "src"]
    for candidate in candidates:
        if candidate.exists():
            sys.path.insert(0, str(candidate))


def load_generator_bridge():
    candidates = [
        ("generate", "tinybird_sdk.cli.commands.generate", "run_generate"),
        ("generate", "tinybird_sdk.cli.commands.generate", "runGenerate"),
        ("build", "tinybird_sdk.cli.commands.build", "run_build"),
        ("build", "tinybird_sdk.cli.commands.build", "runBuild"),
    ]

    errors = []
    for mode, module_name, fn_name in candidates:
        try:
            module = importlib.import_module(module_name)
            fn = getattr(module, fn_name, None)
            if callable(fn):
                return mode, fn
            errors.append(f"{module_name}.{fn_name}: missing callable")
        except Exception as error:
            errors.append(f"{module_name}.{fn_name}: {error}")

    raise RuntimeError(
        "Unable to load Tinybird Python SDK generator bridge. Tried: " + " | ".join(errors)
    )


def normalize_object(value):
    if dataclasses.is_dataclass(value):
        return normalize_object(dataclasses.asdict(value))
    if isinstance(value, dict):
        return {key: normalize_object(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize_object(item) for item in value]
    if hasattr(value, "__dict__"):
        return normalize_object(vars(value))
    return value


def to_legacy_resource_shape_from_artifacts(artifacts):
    grouped = {"datasources": [], "pipes": [], "connections": []}
    for artifact in artifacts or []:
        if not artifact or not isinstance(artifact, dict):
            continue
        name = artifact.get("name") if isinstance(artifact.get("name"), str) else ""
        content = artifact.get("content") if isinstance(artifact.get("content"), str) else ""
        if not name:
            continue

        artifact_type = artifact.get("type")
        if artifact_type == "datasource":
            grouped["datasources"].append({"name": name, "content": content})
        elif artifact_type == "pipe":
            grouped["pipes"].append({"name": name, "content": content})
        elif artifact_type == "connection":
            grouped["connections"].append({"name": name, "content": content})
    return grouped


def to_legacy_resource_shape_from_build(payload):
    if not isinstance(payload, dict) or not payload.get("success"):
        error_message = payload.get("error") if isinstance(payload, dict) else None
        raise RuntimeError(error_message or "Tinybird Python SDK returned an invalid build response")

    build = payload.get("build")
    resources = build.get("resources") if isinstance(build, dict) else None
    if not isinstance(resources, dict):
        raise RuntimeError("Tinybird Python SDK build response did not include resources")

    return {
        "datasources": resources.get("datasources") or [],
        "pipes": resources.get("pipes") or [],
        "connections": resources.get("connections") or [],
    }


def main():
    mode, bridge_fn = load_generator_bridge()

    if mode == "generate":
        payload = normalize_object(bridge_fn({"cwd": cwd}))
        if not isinstance(payload, dict) or not payload.get("success") or not isinstance(payload.get("artifacts"), list):
            error_message = payload.get("error") if isinstance(payload, dict) else None
            raise RuntimeError(error_message or "Tinybird Python SDK returned an invalid generate response")
        print(json.dumps(to_legacy_resource_shape_from_artifacts(payload.get("artifacts"))))
        return

    payload = normalize_object(bridge_fn({"cwd": cwd, "dry_run": True}))
    print(json.dumps(to_legacy_resource_shape_from_build(payload)))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
"""


def generate_python_resources(project_root: Path) -> Dict[str, Any]:
    process = subprocess.run(
        [sys.executable, "-c", _sdk_generator_python_script(), str(project_root)],
        capture_output=True,
        text=True,
        check=False,
    )
    if process.returncode != 0:
        stderr = (process.stderr or "").strip()
        stdout = (process.stdout or "").strip()
        details = stderr or stdout or "Unknown error"
        raise RuntimeError(
            FeedbackManager.error(
                message=(f"Failed to generate Tinybird resources from Python SDK definitions. {details}")
            )
        )

    output = (process.stdout or "").strip()
    if not output:
        raise RuntimeError(
            FeedbackManager.error(
                message="Tinybird Python SDK generator returned no output while processing definitions."
            )
        )

    try:
        data = json.loads(output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            FeedbackManager.error(message=f"Tinybird Python SDK generator returned invalid JSON output: {exc}")
        ) from exc

    return data


def _write_virtual_resources(temp_project_dir: Path, resources: Dict[str, Any]) -> None:
    layouts: Tuple[Tuple[str, str, str], ...] = (
        ("datasources", "datasources", ".datasource"),
        ("pipes", "pipes", ".pipe"),
        ("connections", "connections", ".connection"),
    )

    for resource_key, folder_name, suffix in layouts:
        target_dir = temp_project_dir / folder_name
        target_dir.mkdir(parents=True, exist_ok=True)
        for entry in resources.get(resource_key, []) or []:
            name = str(entry.get("name", "")).strip()
            content = str(entry.get("content", ""))
            if not name:
                continue
            file_path = target_dir / f"{name}{suffix}"
            file_path.write_text(content)


def get_python_virtual_project(
    project_folder: str,
    workspace_name: str,
    max_depth: int,
) -> Optional[PythonVirtualProject]:
    config_path = find_python_config_file(Path(project_folder))
    if not config_path:
        return None

    resources = generate_python_resources(config_path.parent)

    temp_dir = tempfile.TemporaryDirectory(prefix="tb-py-project-")
    temp_project_dir = Path(temp_dir.name)
    _write_virtual_resources(temp_project_dir, resources)

    project = Project(folder=str(temp_project_dir), workspace_name=workspace_name, max_depth=max_depth)
    return PythonVirtualProject(project=project, temp_dir=temp_dir, config_path=config_path)
