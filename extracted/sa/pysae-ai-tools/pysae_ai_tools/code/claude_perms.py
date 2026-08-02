"""Helpers to add path-scoped Claude Code permissions for the clone directory.

When the user picks (or updates) the git clone directory, we offer to write
the matching ``permissions.allow`` entries into ``~/.claude/settings.json``
so Claude Code stops asking for confirmation every time a skill reads or
greps a file in that directory.

Tools covered: Read, Grep, Glob, Bash (with ``git -C <path>...``).

If the user's existing settings already grant unscoped wildcards (e.g.
``"Read"`` directly in the allow list), the path-scoped rules are redundant
and we skip the addition.
"""

import json
import sys
from pathlib import Path

CLAUDE_SETTINGS_PATH = Path.home() / ".claude" / "settings.json"

# Tools that need to be authorized on the clone directory.
_TOOLS_NEEDING_PATH_RULES = ("Read", "Grep", "Glob")


def required_rules(clone_dir: Path) -> list[str]:
    """Return the per-tool ``Tool(<path>)`` rules to allow for ``clone_dir``."""
    p = str(clone_dir)
    rules = [f"{tool}({p}/**)" for tool in _TOOLS_NEEDING_PATH_RULES]
    rules.append(f"Bash(git -C {p}/*:*)")
    return rules


def _has_wildcard_for_all(allow: list[str]) -> bool:
    """True if every covered tool already has an unscoped wildcard in the allow list."""
    return {"Read", "Grep", "Glob", "Bash"}.issubset(set(allow))


def _read_settings(path: Path) -> dict[str, object] | None:
    """Read JSON settings, returning the dict or None on error / missing file."""
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _write_settings(path: Path, data: dict[str, object]) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return True
    except OSError:
        return False


def add_rules(
    clone_dir: Path,
    settings_path: Path = CLAUDE_SETTINGS_PATH,
) -> tuple[str, list[str]]:
    """Add path-scoped allow rules for ``clone_dir`` to the Claude Code settings file.

    Returns ``(status, details)`` where ``status`` is one of:

    - ``"added"``       — rules were appended; ``details`` lists the added rules
    - ``"already-present"`` — every rule was already in the allow list
    - ``"redundant"``   — wildcard tools already cover everything (no rule needed)
    - ``"error"``       — couldn't parse or write the file; ``details`` has the reason
    """
    rules = required_rules(clone_dir)
    data = _read_settings(settings_path)

    if data is None:
        if settings_path.exists():
            return "error", [f"could not parse {settings_path}"]
        data = {}

    perms = data.setdefault("permissions", {})
    if not isinstance(perms, dict):
        return "error", ["permissions key is not an object"]
    allow_raw = perms.setdefault("allow", [])
    if not isinstance(allow_raw, list):
        return "error", ["permissions.allow is not a list"]
    allow: list[str] = [str(x) for x in allow_raw]

    if _has_wildcard_for_all(allow):
        return "redundant", []

    missing = [r for r in rules if r not in allow]
    if not missing:
        return "already-present", []

    allow.extend(missing)
    perms["allow"] = allow
    if not _write_settings(settings_path, data):
        return "error", [f"could not write {settings_path}"]
    return "added", missing


def interactive_offer(clone_dir: Path, settings_path: Path = CLAUDE_SETTINGS_PATH) -> None:
    """Ask the user (TTY) whether to add the path-scoped rules and apply on yes.

    Silent no-op when stdin is not a TTY. Skips the prompt and prints an info
    line when the existing settings already cover the path via wildcards.
    """
    if not sys.stdin.isatty():
        return

    data = _read_settings(settings_path) or {}
    perms_raw = data.get("permissions", {})
    if isinstance(perms_raw, dict):
        allow_raw = perms_raw.get("allow", [])
        if isinstance(allow_raw, list):
            allow = [str(x) for x in allow_raw]
            if _has_wildcard_for_all(allow):
                print(
                    f"ℹ️  Permissions Claude Code : {settings_path} accorde déjà des wildcards "
                    "Read/Grep/Glob/Bash — rien à ajouter.",
                    file=sys.stderr,
                )
                return

    rules = required_rules(clone_dir)
    print(file=sys.stderr)
    print(
        "📜 Pour que Claude lise/grep/glob automatiquement dans le dossier des clones,",
        file=sys.stderr,
    )
    print(f"   ces règles peuvent être ajoutées à {settings_path} :", file=sys.stderr)
    for r in rules:
        print(f"     {r}", file=sys.stderr)

    try:
        answer = input("   Ajouter automatiquement ? [Y/n] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        answer = "n"

    if answer not in {"", "y", "yes", "o", "oui"}:
        print(
            "⏭  Permissions Claude Code inchangées — copie-colle les règles ci-dessus si besoin.",
            file=sys.stderr,
        )
        return

    status, details = add_rules(clone_dir, settings_path)
    if status == "added":
        print(
            f"✅ {len(details)} règle(s) ajoutée(s) dans {settings_path}",
            file=sys.stderr,
        )
    elif status == "already-present":
        print("ℹ️  Toutes les règles étaient déjà présentes.", file=sys.stderr)
    elif status == "redundant":
        print("ℹ️  Wildcards déjà présents — rien à ajouter.", file=sys.stderr)
    else:
        reason = details[0] if details else "raison inconnue"
        print(f"⚠️  Erreur : {reason}", file=sys.stderr)
