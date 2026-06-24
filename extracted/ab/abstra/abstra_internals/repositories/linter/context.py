"""Per-pass linter context: load the project once and materialize its file list
once, instead of every project-reading rule recomputing them.

Before this, ~13 rules each called ``LocalProjectRepository().load()`` at the top
of ``find_issues`` (re-parsing abstra.json under the class-level project lock),
and several re-iterated ``project.project_files`` — a generator that re-traverses
every entrypoint's AST on each iteration — just to do a membership check. A pass
collapses all of that to one load and one traversal.

Propagation is a hybrid: ``LocalLinterRepository`` builds one ``LintContext`` per
pass and the fan-out workers publish it into a ``ContextVar`` for the duration of
their rule call (threads do NOT inherit the parent's context vars, so the worker
sets it explicitly). Rules read it with ``current_lint_context()`` and fall back
to building their own when called standalone (e.g. unit tests), preserving the
previous behavior exactly. The context is never stored on a rule instance (rules
are shared singletons — that would be racy) nor on the repository (it would serve
stale results across passes).

The values are computed lazily and guarded by an ``RLock`` so the shared instance
is safe to read concurrently from the threaded (kill-switch) fan-out: the first
worker to touch a value computes it; the rest block briefly and read the result.
"""

import contextvars
import threading
from pathlib import Path
from typing import List, Optional, Set

from abstra_internals.repositories.linter.models import linter_path_key
from abstra_internals.repositories.project.project import (
    LocalProjectRepository,
    Project,
)


class LintContext:
    def __init__(self) -> None:
        # Reentrant: project_files reads project, project_file_keys reads
        # project_files, all under the same lock.
        self._lock = threading.RLock()
        self._project: Optional[Project] = None
        self._project_files: Optional[List[Path]] = None
        self._project_file_keys: Optional[Set[str]] = None

    @property
    def project(self) -> Project:
        with self._lock:
            if self._project is None:
                self._project = LocalProjectRepository().load()
            return self._project

    @property
    def project_files(self) -> List[Path]:
        with self._lock:
            if self._project_files is None:
                self._project_files = list(self.project.project_files)
            return self._project_files

    @property
    def project_file_keys(self) -> Set[str]:
        with self._lock:
            if self._project_file_keys is None:
                self._project_file_keys = {
                    linter_path_key(f) for f in self.project_files
                }
            return self._project_file_keys


_current_context: "contextvars.ContextVar[Optional[LintContext]]" = (
    contextvars.ContextVar("abstra_lint_context", default=None)
)


def current_lint_context() -> Optional[LintContext]:
    return _current_context.get()


def set_lint_context(ctx: Optional[LintContext]) -> "contextvars.Token":
    return _current_context.set(ctx)


def reset_lint_context(token: "contextvars.Token") -> None:
    _current_context.reset(token)
