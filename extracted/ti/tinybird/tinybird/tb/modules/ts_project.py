import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.project import Project

TS_CONFIG_FILES = (
    "tinybird.config.mjs",
    "tinybird.config.cjs",
    "tinybird.config.json",
    "tinybird.json",
)


@dataclass
class TypescriptVirtualProject:
    project: Project
    temp_dir: tempfile.TemporaryDirectory[str]
    config_path: Path


def find_typescript_config_file(start_dir: Path) -> Optional[Path]:
    current = start_dir.resolve()
    while True:
        for filename in TS_CONFIG_FILES:
            candidate = current / filename
            if candidate.exists():
                return candidate
        if current.parent == current:
            return None
        current = current.parent


def _sdk_generator_node_script() -> str:
    return """
const cwd = process.argv[1];
const sdkPath = process.env.TB_SDK_PATH;

function normalizeSdkPath(pathValue) {
  if (!pathValue) return null;
  return pathValue.endsWith("/") ? pathValue.slice(0, -1) : pathValue;
}

async function loadGenerateBridge() {
  const candidates = [];
  const normalizedSdkPath = normalizeSdkPath(sdkPath);
  if (normalizedSdkPath) {
    candidates.push({
      mode: "generate",
      path: `file://${normalizedSdkPath}/dist/cli/commands/generate.js`,
      exportName: "runGenerate",
    });
  }
  candidates.push({
    mode: "generate",
    path: "@tinybirdco/sdk/cli/commands/generate",
    exportName: "runGenerate",
  });
  candidates.push({
    mode: "generate",
    path: "@tinybirdco/sdk/dist/cli/commands/generate.js",
    exportName: "runGenerate",
  });
  candidates.push({
    mode: "build",
    path: "@tinybirdco/sdk/cli/commands/build",
    exportName: "runBuild",
  });
  candidates.push({
    mode: "build",
    path: "@tinybirdco/sdk/dist/cli/commands/build.js",
    exportName: "runBuild",
  });

  // Backward-compatible fallback for local SDK path without generate command.
  if (normalizedSdkPath) {
    candidates.push({
      mode: "build",
      path: `file://${normalizedSdkPath}/dist/cli/commands/build.js`,
      exportName: "runBuild",
    });
  }


  const errors = [];
  for (const candidate of candidates) {
    try {
      const module = await import(candidate.path);
      const fn = module ? module[candidate.exportName] : null;
      if (typeof fn === "function") {
        return { mode: candidate.mode, fn };
      }
      errors.push(`${candidate.path}: missing ${candidate.exportName} export`);
    } catch (error) {
      const message = error && error.message ? error.message : String(error);
      errors.push(`${candidate.path}: ${message}`);
    }
  }

  throw new Error(`Unable to load Tinybird SDK generator bridge. Tried: ${errors.join(" | ")}`);
}

function toLegacyResourceShapeFromArtifacts(artifacts) {
  const grouped = { datasources: [], pipes: [], connections: [] };
  for (const artifact of artifacts || []) {
    if (!artifact || typeof artifact !== "object") continue;
    const name = typeof artifact.name === "string" ? artifact.name : "";
    const content = typeof artifact.content === "string" ? artifact.content : "";
    if (!name) continue;

    if (artifact.type === "datasource") {
      grouped.datasources.push({ name, content });
    } else if (artifact.type === "pipe") {
      grouped.pipes.push({ name, content });
    } else if (artifact.type === "connection") {
      grouped.connections.push({ name, content });
    }
  }
  return grouped;
}

async function main() {
  const bridge = await loadGenerateBridge();

  if (bridge.mode === "generate") {
    const result = await bridge.fn({ cwd });
    if (!result || !result.success || !Array.isArray(result.artifacts)) {
      const errorMessage =
        (result && result.error) ||
        "Tinybird SDK generator returned an invalid generate response";
      throw new Error(errorMessage);
    }

    process.stdout.write(JSON.stringify(toLegacyResourceShapeFromArtifacts(result.artifacts)));
    return;
  }

  const result = await bridge.fn({ cwd, dryRun: true });
  if (!result || !result.success || !result.build || !result.build.resources) {
    const errorMessage =
      (result && result.error) ||
      "Tinybird SDK generator returned an invalid build response";
    throw new Error(errorMessage);
  }
  const resources = result.build.resources;
  process.stdout.write(JSON.stringify({
    datasources: resources.datasources || [],
    pipes: resources.pipes || [],
    connections: resources.connections || [],
  }));
}

main().catch((error) => {
  const message = error && error.message ? error.message : String(error);
  console.error(message);
  process.exit(1);
});
"""


def generate_typescript_resources(project_root: Path) -> Dict[str, Any]:
    process = subprocess.run(
        ["node", "--input-type=module", "-e", _sdk_generator_node_script(), "--", str(project_root)],
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
                message=(f"Failed to generate Tinybird resources from TypeScript definitions. {details}")
            )
        )

    output = (process.stdout or "").strip()
    if not output:
        raise RuntimeError(
            FeedbackManager.error(
                message="Tinybird SDK generator returned no output while processing TypeScript definitions."
            )
        )

    try:
        data = json.loads(output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            FeedbackManager.error(message=f"Tinybird SDK generator returned invalid JSON output: {exc}")
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


def get_typescript_virtual_project(
    project_folder: str,
    workspace_name: str,
    max_depth: int,
) -> Optional[TypescriptVirtualProject]:
    config_path = find_typescript_config_file(Path(project_folder))
    if not config_path:
        return None

    resources = generate_typescript_resources(config_path.parent)

    temp_dir = tempfile.TemporaryDirectory(prefix="tb-ts-project-")
    temp_project_dir = Path(temp_dir.name)
    _write_virtual_resources(temp_project_dir, resources)

    project = Project(folder=str(temp_project_dir), workspace_name=workspace_name, max_depth=max_depth)
    return TypescriptVirtualProject(project=project, temp_dir=temp_dir, config_path=config_path)
