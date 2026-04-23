"""Local artifact discovery and loading from filesystem directories.

Local artifacts live in ``~/.anteroom/local/`` (global) and
``.anteroom/local/`` (project). They are loaded at ``local`` precedence
(highest — override everything including packs).

Directory structure::

    local/
        skills/
            my-skill/
                SKILL.md
        rules/
            my-rule.md
        instructions/
            my-instruction.md
        context/
            my-context.md
        memories/
            my-memory.md
        mcp_servers/
            my-server.yaml
        config_overlays/
            my-overlay.yaml
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection

from .artifact_storage import upsert_artifact
from .artifacts import ArtifactSource, ArtifactType, build_fqn
from .skill_bundles import (
    _extract_yaml_frontmatter,
    _inline_resources,
    _parse_resource_list_from_frontmatter,
    _resolve_bundle_resources,
)

logger = logging.getLogger(__name__)

_LOCAL_DIR = "local"
_ANTEROOM_DIR = ".anteroom"
_LOCAL_NAMESPACE = "local"

# Default memory metadata for filesystem-discovered memories.
_DEFAULT_MEMORY_METADATA: dict[str, Any] = {
    "memory_scope": "local",
    "memory_category": "project_fact",
    "memory_status": "active",
    "provenance": {},
    "created_by": "user",
    "promoted_by": None,
    "last_recalled_at": None,
    "recall_count": 0,
}


def _apply_memory_scope(art: dict[str, Any], scope: str, namespace: str) -> dict[str, Any]:
    """Rewrite a discovered memory artifact's identity and metadata for *scope*.

    ``discover_local_artifacts()`` returns all artifacts under ``@local/...``.
    For memory-type artifacts the FQN, namespace, and metadata must reflect the
    discovery root (global → ``user``, project → ``project``, space → ``local``).
    Non-memory artifacts are returned unchanged.
    """
    if art.get("type") != ArtifactType.MEMORY.value:
        return art
    art = dict(art)  # shallow copy to avoid mutating the original
    art["namespace"] = namespace
    try:
        art["fqn"] = build_fqn(namespace, ArtifactType.MEMORY.value, art["name"])
    except ValueError:
        logger.warning("Cannot build memory FQN for name=%s namespace=%s, keeping original", art["name"], namespace)
        return art
    art["metadata"] = {**_DEFAULT_MEMORY_METADATA, "memory_scope": scope}
    return art


# Map artifact type to subdirectory name
_TYPE_DIRS: dict[str, str] = {
    ArtifactType.SKILL: "skills",
    ArtifactType.RULE: "rules",
    ArtifactType.INSTRUCTION: "instructions",
    ArtifactType.CONTEXT: "context",
    ArtifactType.MEMORY: "memories",
    ArtifactType.MCP_SERVER: "mcp_servers",
    ArtifactType.CONFIG_OVERLAY: "config_overlays",
}

_EXT_MAP: dict[str, tuple[str, ...]] = {
    ArtifactType.SKILL: (".md",),
    ArtifactType.RULE: (".md", ".txt"),
    ArtifactType.INSTRUCTION: (".md", ".txt"),
    ArtifactType.CONTEXT: (".md", ".txt", ".json"),
    ArtifactType.MEMORY: (".md", ".txt"),
    ArtifactType.MCP_SERVER: (".yaml", ".yml", ".json"),
    ArtifactType.CONFIG_OVERLAY: (".yaml", ".yml"),
}


def discover_local_artifacts(
    local_dir: Path,
) -> list[dict[str, Any]]:
    """Scan a ``local/`` directory and return artifact dicts ready for DB upsert.

    Does NOT write to DB — returns the discovered artifact metadata.
    """
    if not local_dir.is_dir():
        return []

    artifacts: list[dict[str, Any]] = []
    # Spec artifacts are DB-native only — never discovered from filesystem.
    # See #996: prevents restart-clobber of approval state.
    skip_discovery = frozenset({ArtifactType.SPEC})
    for art_type in ArtifactType:
        if art_type in skip_discovery:
            continue
        subdir_name = _TYPE_DIRS.get(art_type, art_type.value)
        subdir = local_dir / subdir_name
        if not subdir.is_dir():
            continue

        # Skills use directory-based layout: skills/<name>/SKILL.md
        if art_type == ArtifactType.SKILL:
            for path in sorted(subdir.glob("*/SKILL.md")):
                name = path.parent.name.lower()
                content = _read_content(path, art_type)
                if content is None:
                    continue

                # Bundle resources declared in frontmatter
                metadata: dict[str, Any] = {}
                resource_list = _parse_resource_list_from_frontmatter(content, path)
                if resource_list:
                    try:
                        resources = _resolve_bundle_resources(path.parent, resource_list, local_dir)
                        content = _inline_resources(content, resources)
                        metadata = {
                            "bundle": True,
                            "resource_count": len(resources),
                            "resource_names": [r[0] for r in resources],
                        }
                    except ValueError as e:
                        logger.warning("Skipping resources for %s: %s", name, e)
                    from ..cli.skills import MAX_PROMPT_SIZE

                    if len(content) > MAX_PROMPT_SIZE:
                        logger.warning("Skipping %s: bundled content exceeds %dKB limit", name, MAX_PROMPT_SIZE // 1000)
                        continue

                # Extract non-core frontmatter into metadata (#1395)
                _raw = _read_content(path, art_type) or ""
                if _raw.startswith("---\n") or _raw.startswith("---\r\n"):
                    try:
                        _body, _fm = _extract_yaml_frontmatter(_raw, path)
                        _core_keys = {
                            "name",
                            "description",
                            "prompt",
                            "allowed-tools",
                            "allowed_tools",
                            "denied-tools",
                            "denied_tools",
                            "resources",
                        }
                        for k, v in _fm.items():
                            if k not in _core_keys and k not in metadata:
                                metadata[k] = v
                    except Exception:
                        pass

                # Resource-directory detection (recognized, not loaded)
                for rdir in ("scripts", "references", "assets"):
                    if (path.parent / rdir).is_dir():
                        logger.debug(
                            "Skill '%s' has %s/ directory (recognized, not loaded)",
                            name,
                            rdir,
                        )

                try:
                    fqn = build_fqn(_LOCAL_NAMESPACE, art_type.value, name)
                except ValueError:
                    logger.warning("Invalid artifact name %s in %s, skipping", name, subdir)
                    continue

                artifacts.append(
                    {
                        "fqn": fqn,
                        "type": art_type.value,
                        "namespace": _LOCAL_NAMESPACE,
                        "name": name,
                        "content": content,
                        "source": ArtifactSource.LOCAL,
                        "path": str(path),
                        "metadata": metadata,
                    }
                )
            continue

        # All other types use flat-file layout
        valid_exts = _EXT_MAP.get(art_type, (".yaml", ".yml", ".md", ".txt"))
        for path in sorted(subdir.iterdir()):
            if not path.is_file():
                continue
            if path.suffix.lower() not in valid_exts:
                continue

            name = path.stem
            content = _read_content(path, art_type)
            if content is None:
                continue

            try:
                fqn = build_fqn(_LOCAL_NAMESPACE, art_type.value, name)
            except ValueError:
                logger.warning("Invalid artifact name %s in %s, skipping", name, subdir)
                continue

            artifacts.append(
                {
                    "fqn": fqn,
                    "type": art_type.value,
                    "namespace": _LOCAL_NAMESPACE,
                    "name": name,
                    "content": content,
                    "source": ArtifactSource.LOCAL,
                    "path": str(path),
                }
            )

    return artifacts


def load_local_artifacts(
    db: ThreadSafeConnection,
    data_dir: Path,
    *,
    project_dir: Path | None = None,
    space_dirs: list[Path] | None = None,
) -> int:
    """Discover and upsert local artifacts from global, project, and space directories.

    Returns the number of artifacts loaded.
    """
    count = 0

    # Global local artifacts: ~/.anteroom/local/
    global_local = data_dir / _LOCAL_DIR
    for art in discover_local_artifacts(global_local):
        art = _apply_memory_scope(art, scope="user", namespace="user")
        upsert_artifact(
            db,
            fqn=art["fqn"],
            artifact_type=art["type"],
            namespace=art["namespace"],
            name=art["name"],
            content=art["content"],
            source=ArtifactSource.LOCAL,
            metadata=art.get("metadata", {}),
        )
        count += 1

    # Project local artifacts: .anteroom/local/
    if project_dir is not None:
        project_local = project_dir / _ANTEROOM_DIR / _LOCAL_DIR
        for art in discover_local_artifacts(project_local):
            art = _apply_memory_scope(art, scope="project", namespace="project")
            upsert_artifact(
                db,
                fqn=art["fqn"],
                artifact_type=art["type"],
                namespace=art["namespace"],
                name=art["name"],
                content=art["content"],
                source=ArtifactSource.LOCAL,
                metadata=art.get("metadata", {}),
            )
            count += 1

    # Space local artifacts: <repo_path>/.anteroom/local/
    if space_dirs:
        for space_dir in space_dirs:
            if not space_dir.is_dir():
                continue
            space_local = space_dir / _ANTEROOM_DIR / _LOCAL_DIR
            for art in discover_local_artifacts(space_local):
                art = _apply_memory_scope(art, scope="local", namespace="local")
                upsert_artifact(
                    db,
                    fqn=art["fqn"],
                    artifact_type=art["type"],
                    namespace=art["namespace"],
                    name=art["name"],
                    content=art["content"],
                    source=ArtifactSource.LOCAL,
                    metadata=art.get("metadata", {}),
                )
                count += 1

    if count:
        logger.info("Loaded %d local artifact(s)", count)
    return count


_SAFE_NAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,62}$")


def scaffold_local_artifact(
    artifact_type: str,
    name: str,
    data_dir: Path,
    *,
    project: bool = False,
    project_dir: Path | None = None,
) -> Path:
    """Create a template local artifact file.

    Returns the path to the created file.
    Raises ``ValueError`` if the type is invalid or the file already exists.
    """
    if not _SAFE_NAME_RE.match(name) or ".." in name:
        msg = f"Invalid artifact name: {name!r}. Use alphanumeric, hyphens, underscores, dots only."
        raise ValueError(msg)

    try:
        art_type = ArtifactType(artifact_type)
    except ValueError:
        valid = ", ".join(t.value for t in ArtifactType)
        msg = f"Invalid artifact type: {artifact_type!r}. Must be one of: {valid}"
        raise ValueError(msg)

    subdir_name = _TYPE_DIRS[art_type]

    if project:
        if project_dir is None:
            msg = "project_dir required when project=True"
            raise ValueError(msg)
        base = project_dir / _ANTEROOM_DIR / _LOCAL_DIR / subdir_name
    else:
        base = data_dir / _LOCAL_DIR / subdir_name

    # Skills use directory-based layout: skills/<name>/SKILL.md
    if art_type == ArtifactType.SKILL:
        skill_dir = base / name
        path = skill_dir / "SKILL.md"

        if path.exists():
            msg = f"Artifact already exists: {path}"
            raise ValueError(msg)

        skill_dir.mkdir(parents=True, exist_ok=True)
        template = _get_template(art_type, name)
        path.write_text(template, encoding="utf-8")
        return path

    ext = ".yaml" if art_type in (ArtifactType.MCP_SERVER, ArtifactType.CONFIG_OVERLAY) else ".md"
    path = base / f"{name}{ext}"

    if path.exists():
        msg = f"Artifact already exists: {path}"
        raise ValueError(msg)

    base.mkdir(parents=True, exist_ok=True)
    template = _get_template(art_type, name)
    path.write_text(template, encoding="utf-8")
    return path


def _read_content(path: Path, art_type: ArtifactType) -> str | None:
    """Read artifact content from a file."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as e:
        logger.warning("Cannot read %s: %s", path, e)
        return None

    if path.suffix in (".yaml", ".yml"):
        import yaml

        data = yaml.safe_load(raw)
        if isinstance(data, dict) and "content" in data:
            return str(data["content"])

    return raw


def _get_template(art_type: ArtifactType, name: str) -> str:
    """Return a template for a new local artifact."""
    if art_type == ArtifactType.SKILL:
        return f"---\nname: {name}\ndescription: TODO\n---\n\nTODO: skill prompt here\n"
    if art_type in (ArtifactType.MCP_SERVER, ArtifactType.CONFIG_OVERLAY):
        return f"# {name}\n# TODO: add configuration\n"
    return f"# {name}\n\nTODO: add content here\n"
