"""The skills the CLI's wheel ships (`share/probe-research/skills`, pyproject's shared-data): where they are,
and each install profile's list (`profiles.json`). Stdlib only."""

from __future__ import annotations

import json
import site
import sys
import sysconfig
from pathlib import Path

#: The one list of which skills each profile has (`agent/skills/profiles.json`).
PROFILES_FILE = "profiles.json"
#: A skill every shipped folder holds: how a candidate folder is told from an empty one.
PROBE_SKILL = "track-work"


def find_shipped_skills() -> Path | None:
    """The installed skills (the wheel's shared data: under the environment's prefix, or the user base for
    `pip install --user`), else the repo's (a source checkout)."""
    data = [sys.prefix, sysconfig.get_path("data"), site.getuserbase()]
    candidates = [Path(d) / "share" / "probe-research" / "skills" for d in dict.fromkeys(data) if d]
    candidates.append(Path(__file__).resolve().parents[4] / "skills")
    return next((c for c in candidates if (c / PROBE_SKILL / "SKILL.md").is_file()), None)


def load_profile_skills(name: str, root: Path | None = None) -> tuple[str, ...]:
    """`profiles.json`'s list for `name` (`runs`, `full`, `daemon`); () when it names none or is unreadable."""
    folder = root if root is not None else find_shipped_skills()
    if folder is None:
        return ()
    try:
        listed = json.loads((folder / PROFILES_FILE).read_text(encoding="utf-8")).get(name)
    except (OSError, ValueError, AttributeError):
        return ()
    return tuple(slug for slug in listed if isinstance(slug, str)) if isinstance(listed, list) else ()
