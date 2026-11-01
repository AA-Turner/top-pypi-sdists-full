"""pi's settings.json files: where they are, read and written atomically under the D3 contract."""

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from pathlib import Path

# Stdlib-only as well (its only import is `probe._shared.oscompat`, also
# stdlib-only), and it imports nothing from probe.cli back.
from probe.foundation.durable.durable import through_symlink, write_text_atomic


class _SettingsRefusal(Exception):
    """Internal only. `install_package_entry`/`remove_package_entry` catch this
    and turn it into a `claude_cli.Result(ok=False, ...)` -- callers of THIS
    module never see it, because the whole point of the settings-edit contract
    (plan D3) is "return a refusal", never "raise into the wizard".
    """


def pi_agent_dir(env: Mapping[str, str] | None = None) -> Path:
    """pi's own global agent directory: `PI_CODING_AGENT_DIR`, else `~/.pi/agent`.

    Moved here from `agent_rules.memory_path`'s pi branch (this logic must not
    exist in a third place -- `agent/plugins/probe-research-pi/src/core/paths.ts`'s
    `piAgentDir` is the second). `PI_CODING_AGENT_DIR` is not a guess: pi
    0.86.0's own `dist/config.js` (as 0.84.3's) derives it as
    `${APP_NAME.toUpperCase()}_CODING_AGENT_DIR` and `getAgentDir()` -- read by
    every pi entry point -- returns it verbatim when set. Unlike Codex's
    `CODEX_HOME` (a parent directory Codex appends `AGENTS.md` onto), this
    names the agent directory itself, so nothing is appended before it here
    either.
    """
    active = env if env is not None else os.environ
    configured = active.get("PI_CODING_AGENT_DIR")
    return Path(configured).expanduser() if configured else Path.home() / ".pi" / "agent"


def settings_path(env: Mapping[str, str] | None = None) -> Path:
    """`<agent-dir>/settings.json` -- the file pi and pi-mcp-adapter both read."""
    return pi_agent_dir(env) / "settings.json"


def project_settings_path(cwd: Path | str) -> Path:
    """`<cwd>/.pi/settings.json` -- pi's project-scope settings.

    Not an ancestor walk: pi reads the project file at the directory it was
    started in, and inventing a walk here would claim an install pi itself
    would not load.
    """
    return Path(cwd) / ".pi" / "settings.json"


def _load_settings(path: Path) -> dict:
    """Read `settings.json` under the D3 contract, or raise `_SettingsRefusal`.

    Missing file is NOT a refusal -- it is the documented "treat as {}" case,
    because a fresh pi install (fact 8: this machine's real settings.json has
    no `packages` key at all yet) is the common case, not an error.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError as exc:
        raise _SettingsRefusal(f"could not read {path}: {exc}") from exc

    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        raise _SettingsRefusal(f"{path} is not valid JSON, refusing to edit it ({exc})") from exc
    if not isinstance(data, dict):
        raise _SettingsRefusal(
            f"{path}'s root is a {type(data).__name__}, not a JSON object -- refusing to edit it"
        )
    packages = data.get("packages")
    if packages is not None and not isinstance(packages, list):
        raise _SettingsRefusal(f'{path}\'s "packages" key is not a list -- refusing to edit it')
    return data


def _write_settings(path: Path, data: dict) -> None:
    """Atomic write: a uniquely named temp file in the SAME directory, then a
    replace (`write_text_atomic`).

    Same-directory is load-bearing, not decoration -- a replace is only atomic
    within one filesystem, and a tmp file in `/tmp` replacing a target under
    `~/.pi` can cross a mount boundary silently on some setups. The temp name
    is unique and created exclusively: with a symlinked settings.json it lands
    in the user's dotfiles folder, where a fixed name could already be taken
    (or be a link). The file keeps its mode.
    2-space indent + trailing newline matches how pi itself writes this file,
    so a subsequent pi-side write does not show a whole-file diff.
    A settings.json symlinked into a dotfiles repo is written through, so the
    link survives.
    """
    path = through_symlink(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        write_text_atomic(path, json.dumps(data, indent=2) + "\n", keep_mode=True)
    except OSError as exc:
        raise _SettingsRefusal(f"could not write {path}: {exc}") from exc
