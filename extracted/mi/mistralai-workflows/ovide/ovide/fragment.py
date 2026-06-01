from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

from ovide.config import CHANGELOG_DIR, VALID_BUMPS, VALID_KINDS


@dataclass
class Fragment:
    bump: str
    kind: str
    body: str
    path: Path

    @staticmethod
    def parse(path: Path) -> Fragment:
        content = path.read_text()
        if not content.startswith("---"):
            raise FragmentError(path, "Missing frontmatter (must start with ---)")

        parts = content.split("---", 2)
        if len(parts) < 3:
            raise FragmentError(path, "Invalid frontmatter (missing closing ---)")

        try:
            meta = yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            raise FragmentError(path, f"Invalid YAML in frontmatter: {e}")

        if not isinstance(meta, dict):
            raise FragmentError(path, "Frontmatter must be a YAML mapping")

        bump = meta.get("bump")
        kind = meta.get("kind")
        errors: list[str] = []

        if not bump:
            errors.append("Missing 'bump' field")
        elif bump not in VALID_BUMPS:
            errors.append(f"Invalid bump '{bump}', must be one of: {', '.join(VALID_BUMPS)}")

        if not kind:
            errors.append("Missing 'kind' field")
        elif kind not in VALID_KINDS:
            errors.append(f"Invalid kind '{kind}', must be one of: {', '.join(VALID_KINDS)}")

        body = parts[2].strip()
        if not body:
            errors.append("Empty body (describe the change after the frontmatter)")

        if errors:
            raise FragmentError(path, "; ".join(errors))

        return Fragment(bump=bump, kind=kind, body=body, path=path)


class FragmentError(Exception):
    def __init__(self, path: Path, message: str):
        self.path = path
        self.message = message
        super().__init__(f"{path}: {message}")


def list_fragments() -> list[Path]:
    if not CHANGELOG_DIR.exists():
        return []
    return sorted(p for p in CHANGELOG_DIR.glob("*.md"))


def generate_filename(slug: str | None = None) -> str:
    today = date.today().strftime("%Y%m%d")
    short_id = uuid.uuid4().hex[:6]
    parts = [today, short_id]
    if slug:
        parts.append(slug)
    return "-".join(parts) + ".md"


def create_fragment(bump: str, kind: str, message: str, slug: str | None = None) -> Path:
    CHANGELOG_DIR.mkdir(exist_ok=True)
    filename = generate_filename(slug)
    path = CHANGELOG_DIR / filename
    content = f"---\nbump: {bump}\nkind: {kind}\n---\n\n{message}\n"
    path.write_text(content)
    return path
