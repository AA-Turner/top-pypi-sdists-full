"""Repository-specific guards used by skill injection."""

from __future__ import annotations

import warnings
from pathlib import Path


def _is_self_repo(git_root: Path) -> bool:
    """Return ``True`` when *git_root* is the agentic-devtools repository itself.

    Injecting into this repository is destructive: ``.github/agents/`` and
    ``.github/prompts/`` are *tracked source* here (they are force-included
    into the wheel), so stale cleanup would delete every classification-filtered
    file and a wheel install would additionally overwrite the survivors with
    older released content.

    Two independent signals are used so both install shapes are covered:

    * Editable install — the running package's repo root is *git_root*.
    * Wheel install — *git_root* carries the agentic-devtools package source
      (``agentic_devtools/skill_injector.py``) and a ``pyproject.toml`` whose
      ``[project]`` table declares ``name = "agentic-devtools"``.
    """
    try:
        resolved_root = git_root.resolve()
        # Editable install: the installed package lives inside this checkout.
        if Path(__file__).resolve().parent.parent == resolved_root:
            return True
    except OSError:
        return False

    if not (resolved_root / "agentic_devtools" / "skill_injector.py").is_file():
        return False

    pyproject = resolved_root / "pyproject.toml"
    try:
        content = pyproject.read_bytes()
    except OSError:
        return False

    try:
        try:
            import tomllib  # stdlib on 3.11+
        except ImportError:  # pragma: no cover
            import tomli as tomllib  # type: ignore[no-redef]  # pragma: no cover

        data = tomllib.loads(content.decode("utf-8"))
        return data.get("project", {}).get("name") == "agentic-devtools"
    except Exception:
        return False


def _ensure_github_gitignore_unignores_agdt(git_root: Path) -> None:
    """Ensure `.github/.gitignore` does not ignore injected `.agdt` skills.

    Many repositories have a blanket `.agdt/` rule in their root `.gitignore`.
    That would also ignore `.github/agents/.agdt/` and `.github/prompts/.agdt/`,
    which prevents injected skills from being committed. To avoid mutating the
    root ignore file, we maintain a `.github/.gitignore` file with explicit
    un-ignore rules for these managed directories.

    .. note::

        This function is no longer called by :func:`inject_skills` after the
        migration from ``.agdt/`` subdirectories to a flat layout.  It is
        retained for backward compatibility in case external code references it.
    """

    github_dir = git_root / ".github"
    github_dir.mkdir(parents=True, exist_ok=True)
    github_gitignore = github_dir / ".gitignore"

    # Desired lines (order matters: comment followed by un-ignore rules).
    desired_lines = [
        "# Managed by agentic-devtools: ensure injected skills under .github are tracked.",
        "!agents/.agdt/",
        "!agents/.agdt/**",
        "!prompts/.agdt/",
        "!prompts/.agdt/**",
    ]

    existing_lines: list[str] = []
    if github_gitignore.exists():
        try:
            existing_lines = github_gitignore.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            warnings.warn(
                f"agentic-devtools: failed to read {github_gitignore!s}; "
                "injected skills under .github may remain ignored. "
                f"Underlying error: {exc}",
                RuntimeWarning,
            )
            # Injection should still proceed, even if skills remain ignored.
            return

    # Append any missing desired lines, preserving existing content.
    updated = False
    for line in desired_lines:
        if line not in existing_lines:
            existing_lines.append(line)
            updated = True

    if updated:
        try:
            github_gitignore.write_text(
                "\n".join(existing_lines) + "\n",
                encoding="utf-8",
            )
        except OSError as exc:
            warnings.warn(
                f"agentic-devtools: failed to write {github_gitignore!s}; "
                "injected skills under .github may remain ignored. "
                f"Underlying error: {exc}",
                RuntimeWarning,
            )
            # Callers treat injection I/O errors as a best-effort operation.
            return
