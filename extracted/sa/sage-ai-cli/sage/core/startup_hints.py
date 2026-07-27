"""Lightweight git / CI context shown when starting the interactive agent (`sage run`)."""

from __future__ import annotations

import os
from pathlib import Path

__all__ = ["run_startup_devops_hints"]


def run_startup_devops_hints(cwd: Path) -> list[str]:
    """One-line git summary; optional latest CI status if ``SAGE_SHOW_CI_ON_START=1``.

    Avoids network/API calls by default so startup stays fast.
    """
    lines: list[str] = []
    cwd = cwd.resolve()

    try:
        from sage.devops.git import GitOps

        git = GitOps(cwd)
        if git.is_repo:
            st = git.status()
            n_changed = len(st.staged) + len(st.modified) + len(st.untracked)
            tip = f"Git: {st.branch}"
            tip += " (clean)" if st.is_clean else f" ({n_changed} path(s) changed)"
            lines.append(tip)
    except Exception:
        pass

    if os.environ.get("SAGE_SHOW_CI_ON_START") == "1":
        try:
            from sage.devops.ci_cd import CICDMonitor

            monitor = CICDMonitor()
            run = monitor.get_latest_run()
            if run:
                c = run.conclusion or run.status or "?"
                lines.append(f"Latest CI: {run.workflow_name} → {c}")
        except Exception:
            pass

    return lines
