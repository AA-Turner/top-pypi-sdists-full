"""Skills — Claude-Code-style markdown skill loader for pw-agent.

A skill is a directory under ~/.pw-agent/skills/<name>/ containing a
SKILL.md file with YAML frontmatter:

    ---
    name: my-skill
    description: When to use this skill (one-line trigger)
    ---

    # Skill content
    ...

On startup, pw-agent scans the skills directory and injects a list of
available skills (just their names + descriptions) into the system prompt.
When the user query semantically matches a skill, the FULL SKILL.md
content is loaded into the next message as additional context.

Skills can also live in a project at ./.pw-agent/skills/ — these
override or extend global skills for the current project.
"""

import os
import re
import hashlib
from typing import Optional

DEFAULT_SKILLS_DIR = os.path.expanduser("~/.pw-agent/skills")
PROJECT_SKILLS_DIR = ".pw-agent/skills"

# Trigger threshold — how many keyword overlaps to auto-load a skill
MIN_TRIGGER_OVERLAP = 2


class Skill:
    """A single loaded skill."""

    def __init__(self, name: str, description: str, body: str, path: str):
        self.name = name
        self.description = description
        self.body = body
        self.path = path
        self.id = hashlib.md5(path.encode()).hexdigest()[:8]

    @property
    def keywords(self) -> set[str]:
        """Lowercased keywords from name + description for trigger matching."""
        text = f"{self.name} {self.description}".lower()
        # Strip punctuation, split on whitespace
        words = re.findall(r"[a-z0-9_-]{3,}", text)
        # Filter common stopwords
        stopwords = {
            "the", "and", "for", "use", "with", "this", "that", "your",
            "when", "from", "into", "skill", "uses", "also", "user", "wants",
            "create", "creates", "creating", "make", "makes", "making",
            "use", "using", "used",
        }
        return {w for w in words if w not in stopwords}

    def __repr__(self):
        return f"<Skill {self.name}: {self.description[:40]}>"


def parse_skill_file(path: str) -> Optional[Skill]:
    """Parse a SKILL.md file and return a Skill object, or None on error."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return None

    # Parse YAML frontmatter (simple regex — no PyYAML dep)
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        # No frontmatter — use the parent directory name as the skill name
        # and the first non-empty line as description
        name = os.path.basename(os.path.dirname(path))
        lines = [l.strip() for l in content.split("\n") if l.strip()]
        description = lines[0] if lines else f"Skill: {name}"
        return Skill(name=name, description=description, body=content, path=path)

    frontmatter, body = match.group(1), match.group(2)

    # Parse simple key: value lines from frontmatter
    fm = {}
    for line in frontmatter.split("\n"):
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        fm[key.strip().lower()] = val.strip().strip('"').strip("'")

    name = fm.get("name") or os.path.basename(os.path.dirname(path))
    description = fm.get("description") or "(no description)"

    return Skill(name=name, description=description, body=body, path=path)


def load_skills(project_dir: str = "") -> list[Skill]:
    """Load all skills from the global and project skill directories.

    Returns: list of Skill objects, project skills first (higher priority).
    """
    skills = []
    seen_names = set()

    # Project-level skills first (highest priority)
    if project_dir:
        proj_path = os.path.join(project_dir, PROJECT_SKILLS_DIR)
        if os.path.isdir(proj_path):
            for skill in _scan_dir(proj_path):
                if skill.name not in seen_names:
                    skills.append(skill)
                    seen_names.add(skill.name)

    # Global user skills
    if os.path.isdir(DEFAULT_SKILLS_DIR):
        for skill in _scan_dir(DEFAULT_SKILLS_DIR):
            if skill.name not in seen_names:
                skills.append(skill)
                seen_names.add(skill.name)

    return skills


def _scan_dir(skills_dir: str) -> list[Skill]:
    """Scan a directory for SKILL.md files (one level deep)."""
    skills = []
    try:
        entries = sorted(os.listdir(skills_dir))
    except OSError:
        return skills

    for entry in entries:
        skill_dir = os.path.join(skills_dir, entry)
        if not os.path.isdir(skill_dir):
            continue
        # Look for SKILL.md or skill.md
        for filename in ("SKILL.md", "skill.md"):
            skill_file = os.path.join(skill_dir, filename)
            if os.path.exists(skill_file):
                skill = parse_skill_file(skill_file)
                if skill:
                    skills.append(skill)
                break
    return skills


def format_skills_for_prompt(skills: list[Skill]) -> str:
    """Format the skill list as a section for the system prompt."""
    if not skills:
        return ""
    lines = ["## Available Skills (use when relevant — call /skill <name> to read the full guide):"]
    for s in skills:
        # Trim long descriptions
        desc = s.description if len(s.description) <= 120 else s.description[:117] + "..."
        lines.append(f"- {s.name}: {desc}")
    return "\n".join(lines)


def find_relevant_skills(query: str, skills: list[Skill], top_k: int = 3) -> list[Skill]:
    """Naive keyword-overlap matcher. Returns skills whose keywords overlap
    the query the most. Falls back to substring match on name/description.
    """
    if not skills or not query:
        return []

    query_lower = query.lower()
    # Tokenize query
    query_words = set(re.findall(r"[a-z0-9_-]{3,}", query_lower))

    scored = []
    for skill in skills:
        # Score 1: keyword overlap
        overlap = len(skill.keywords & query_words)
        # Score 2: substring match on skill name (heavy weight)
        name_match = 5 if skill.name.lower() in query_lower else 0
        # Score 3: substring match on description
        desc_words_in_query = sum(
            1 for w in skill.description.lower().split()
            if len(w) >= 4 and w in query_lower
        )

        score = overlap + name_match + desc_words_in_query
        if score >= MIN_TRIGGER_OVERLAP or name_match:
            scored.append((skill, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [s for s, _ in scored[:top_k]]


def get_skill_by_name(name: str, skills: list[Skill]) -> Optional[Skill]:
    """Look up a skill by exact name match (case-insensitive)."""
    name_lower = name.lower().strip()
    for skill in skills:
        if skill.name.lower() == name_lower:
            return skill
    # Fallback: prefix match
    for skill in skills:
        if skill.name.lower().startswith(name_lower):
            return skill
    return None
