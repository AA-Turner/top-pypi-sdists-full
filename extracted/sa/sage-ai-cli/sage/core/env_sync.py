"""Ensure `.gitignore` covers `.env` files and optionally push keys to GitHub Actions secrets.

Used from ``sage run`` startup (`run_startup_env_maintenance`). Vite ``VITE_*`` vars must be
present at **docker build** time; runtime-only vars use Cloud Run ``--set-env-vars``.
This module never prints secret values."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

from sage.core.credentials import parse_env_file

__all__ = [
    "discover_github_secret_names_from_workflows",
    "ensure_gitignore_for_monorepo",
    "merge_env_file",
    "run_startup_env_maintenance",
    "sync_keys_to_github_secrets",
]

_GITIGNORE_LINES = (
    ".env",
    ".env.local",
    "!.env.example",
)


def _git_root(start: Path) -> Path | None:
    cur = start.resolve()
    for p in [cur, *cur.parents]:
        if (p / ".git").exists():
            return p
    return None


def ensure_gitignore_for_monorepo(project_root: Path) -> list[str]:
    """Ensure `.gitignore` at repo root and under `ai-platform/frontend/` protect `.env` files.

    Returns human-readable paths that were created or updated.
    """
    project_root = project_root.resolve()
    notes: list[str] = []
    roots: list[Path] = []

    gr = _git_root(project_root)
    if gr:
        roots.append(gr)

    # Typical clone layout: repo/ai-platform/frontend/.env
    for candidate in (
        project_root / "ai-platform" / "frontend",
        project_root / "frontend",
    ):
        if candidate.is_dir() and _git_root(candidate):
            roots.append(candidate)

    dedup: list[Path] = []
    seen: set[str] = set()
    for r in roots:
        key = str(r.resolve())
        if key not in seen:
            seen.add(key)
            dedup.append(r.resolve())

    for root in dedup:
        gi = root / ".gitignore"
        lines: list[str] = []
        if gi.exists():
            lines = gi.read_text("utf-8").splitlines()
        changed = False
        for entry in _GITIGNORE_LINES:
            if entry not in lines:
                if lines and not lines[-1].strip():
                    pass
                lines.append(entry)
                changed = True
        if changed:
            gi.write_text("\n".join(lines).rstrip() + "\n", "utf-8")
            notes.append(str(gi))
    return notes


def discover_github_secret_names_from_workflows(project_root: Path) -> frozenset[str]:
    """Parse `.github/workflows/*.yml` for `${{ secrets.NAME }}` references."""
    names: set[str] = set()
    pr = project_root.resolve()
    roots: list[Path] = []
    gr = _git_root(pr)
    if gr:
        roots.append(gr)
    roots.append(pr)
    if (pr / "ai-platform").is_dir():
        roots.append(pr / "ai-platform")

    seen_dirs: set[Path] = set()
    for base in roots:
        wf_root = base / ".github" / "workflows"
        if not wf_root.is_dir() or wf_root in seen_dirs:
            continue
        seen_dirs.add(wf_root)
        for wf in sorted(wf_root.glob("*.yml")) + sorted(wf_root.glob("*.yaml")):
            try:
                text = wf.read_text("utf-8", errors="ignore")
            except OSError:
                continue
            for m in re.finditer(
                r"secrets\.([A-Z][A-Z0-9_]+)",
                text,
            ):
                names.add(m.group(1))
    return frozenset(names)


def merge_env_file(target: Path, updates: dict[str, str], *, header: str = "# Local secrets (not committed)") -> None:
    """Merge key/value pairs into a `.env` file using existing parse/write rules."""
    from sage.core.credentials import _format_env_value

    target.parent.mkdir(parents=True, exist_ok=True)
    existing = parse_env_file(target) if target.exists() else {}
    existing.update(updates)
    lines = [
        header,
        "# Do not commit — auto gitignore on `sage run`",
        "",
    ]
    for key in sorted(existing):
        lines.append(f"{key}={_format_env_value(existing[key])}")
    target.write_text("\n".join(lines).rstrip() + "\n", "utf-8")
    try:
        target.chmod(0o600)
    except OSError:
        pass


def _gh_available() -> bool:
    try:
        r = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        return r.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def sync_keys_to_github_secrets(
    keys_values: dict[str, str],
    *,
    dry_run: bool,
) -> tuple[list[str], list[str]]:
    """Upload each key to `gh secret set` (stdin body). Returns (ok, errors)."""
    ok: list[str] = []
    errors: list[str] = []
    if not keys_values:
        return ok, errors
    if not dry_run and not _gh_available():
        return [], ["GitHub CLI not authenticated. Run: gh auth login"]

    for name, value in sorted(keys_values.items()):
        if dry_run:
            ok.append(f"gh secret set {name}  # ({len(value)} chars)")
            continue
        try:
            proc = subprocess.run(
                ["gh", "secret", "set", name],
                input=(value or "").encode("utf-8"),
                capture_output=True,
                timeout=120,
            )
            if proc.returncode == 0:
                ok.append(name)
            else:
                err = (proc.stderr or proc.stdout or b"").decode("utf-8", errors="replace").strip()
                errors.append(f"{name}: {err or proc.returncode}")
        except (OSError, subprocess.TimeoutExpired) as exc:
            errors.append(f"{name}: {exc}")

    return ok, errors


def select_keys_for_github_sync(
    env_values: dict[str, str],
    workflow_secrets: frozenset[str],
    *,
    only_prefix: str | None,
    extra_keys: frozenset[str] | None,
) -> dict[str, str]:
    """Prefer keys referenced by workflows; always include VITE_* for frontend builds."""
    if only_prefix:
        return {k: v for k, v in env_values.items() if k.startswith(only_prefix)}

    out: dict[str, str] = {}
    # Workflow-declared names that exist in .env
    for k in workflow_secrets:
        if k in env_values and env_values[k] != "":
            out[k] = env_values[k]
    # Vite build secrets (often required even if workflow regex missed a fork)
    for k, v in env_values.items():
        if k.startswith("VITE_") and v != "":
            out[k] = v
    if extra_keys:
        for k in extra_keys:
            if k in env_values and env_values[k] != "":
                out[k] = env_values[k]
    return out


def _discover_env_file_candidates(cwd: Path) -> list[Path]:
    """Prefer frontend `.env`, then package `.env`, walking up for `ai-platform/` layouts."""
    from sage.core.credentials import find_project_root

    root = find_project_root(cwd)
    candidates: list[Path] = []
    for rel in ("frontend/.env", ".env"):
        p = (root / rel).resolve()
        if p.exists():
            candidates.append(p)
    repo = root
    while repo.parent != repo:
        for rel in ("ai-platform/frontend/.env", "ai-platform/.env"):
            p = (repo / rel).resolve()
            if p.exists() and p not in candidates:
                candidates.append(p)
        repo = repo.parent
    return candidates


def run_startup_env_maintenance(cwd: Path) -> list[str]:
    """Run at interactive agent startup: update `.gitignore` for `.env`; optionally sync to GitHub.

    Set environment variable ``SAGE_SYNC_SECRETS_TO_GITHUB=1`` to upload keys from the first
    discovered `.env` (workflow references + ``VITE_*``). Requires ``gh auth login``.
    """
    lines: list[str] = []
    cwd = cwd.resolve()
    updated = ensure_gitignore_for_monorepo(cwd)
    for p in updated:
        lines.append(f"Updated .gitignore for local secrets: {p}")

    if os.environ.get("SAGE_SYNC_SECRETS_TO_GITHUB") != "1":
        return lines

    from sage.core.credentials import find_project_root

    root = find_project_root(cwd)
    candidates = _discover_env_file_candidates(cwd)
    if not candidates:
        lines.append(
            "SAGE_SYNC_SECRETS_TO_GITHUB=1 is set but no .env file found — skipped GitHub secret sync."
        )
        return lines

    chosen = candidates[0]
    values = parse_env_file(chosen)
    if not values:
        lines.append(f"SAGE_SYNC_SECRETS_TO_GITHUB=1 but {chosen} has no entries — skipped sync.")
        return lines

    wf_keys = discover_github_secret_names_from_workflows(root)
    selected = select_keys_for_github_sync(values, wf_keys, only_prefix=None, extra_keys=None)
    if not selected:
        lines.append("GitHub secret sync: no workflow-matching or VITE_* keys in .env — skipped.")
        return lines

    ok, errs = sync_keys_to_github_secrets(selected, dry_run=False)
    if ok:
        lines.append(
            "Pushed to GitHub Actions secrets: "
            + ", ".join(ok)
            + " (re-run deploy CI so Docker build picks them up)."
        )
    for e in errs:
        lines.append(f"GitHub secret sync error: {e}")
    return lines
