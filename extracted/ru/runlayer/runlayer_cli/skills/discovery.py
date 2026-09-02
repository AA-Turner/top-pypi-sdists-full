import os
from pathlib import Path, PurePosixPath

import structlog
import yaml

from runlayer_cli.skills.models import DiscoveredSkill, SkillFile

logger = structlog.get_logger(__name__)

SKILL_MARKER = "SKILL.md"
SKIP_DIRS = {
    ".agents",
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".tox",
    "dist",
    "build",
}
SUPPORTED_EXTENSIONS = {
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".md",
    ".markdown",
    ".py",
    ".sh",
    ".svg",
    ".ts",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}


def parse_frontmatter(content: str) -> dict:
    if not content.startswith("---"):
        return {}
    close = content.find("\n---", 3)
    if close == -1:
        return {}
    try:
        data = yaml.safe_load(content[3:close])
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError:
        return {}


def _collect_files(skill_dir: Path) -> list[SkillFile]:
    files = []
    for dirpath, _, filenames in os.walk(skill_dir):
        dp = Path(dirpath)
        for fname in sorted(filenames):
            fpath = dp / fname
            if fpath.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            try:
                content = fpath.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                logger.warning("skipping_non_utf8_file", path=str(fpath))
                continue
            rel = fpath.relative_to(skill_dir)
            title = PurePosixPath(rel).as_posix()
            files.append(SkillFile(title=title, path=fpath, content=content))
    return files


def discover_skills(root: Path) -> list[DiscoveredSkill]:
    root = root.resolve()
    skills = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        # Case-insensitive marker match, preferring the exact canonical name.
        if SKILL_MARKER in filenames:
            marker_name = SKILL_MARKER
        else:
            marker_name = next(
                (
                    name
                    for name in sorted(filenames)
                    if name.lower() == SKILL_MARKER.lower()
                ),
                None,
            )
        if marker_name is None:
            continue

        skill_dir = Path(dirpath)

        if skill_dir == root:
            rel_path = root.name
        else:
            rel_path = PurePosixPath(skill_dir.relative_to(root)).as_posix()

        dirnames.clear()

        marker_path = skill_dir / marker_name
        try:
            marker_content = marker_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            logger.warning("skipping_unreadable_skill", path=str(marker_path))
            continue

        fm = parse_frontmatter(marker_content)
        name = fm.get("name")
        if not name:
            name = skill_dir.name
        name = str(name)
        if len(name) > 100:
            name = name[:100]
        description = fm.get("description")
        if description is not None:
            description = str(description)
            if len(description) > 1024:
                description = description[:1024]

        files = _collect_files(skill_dir)

        skills.append(
            DiscoveredSkill(
                path=rel_path,
                name=name,
                description=description,
                files=files,
            )
        )

    return sorted(skills, key=lambda s: s.path)
