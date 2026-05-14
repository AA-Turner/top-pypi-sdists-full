from __future__ import annotations

from contextvars import ContextVar
from pathlib import Path
from typing import Sequence

from chalk_rs import AstProjectIndex

CURRENT_PROJECT_AST_CONTEXT: ContextVar[AstProjectIndex | None] = ContextVar(
    "CURRENT_PROJECT_AST_CONTEXT",
    default=None,
)


def get_project_ast_context(project_root: Path | None = None) -> AstProjectIndex:
    index = CURRENT_PROJECT_AST_CONTEXT.get()
    if index is not None:
        return index

    resolved_root = (project_root or Path.cwd()).resolve()
    index = AstProjectIndex([], str(resolved_root))
    CURRENT_PROJECT_AST_CONTEXT.set(index)
    return index


def set_project_ast_context(
    project_root: Path,
    repo_files: Sequence[Path],
) -> AstProjectIndex:
    project_root = project_root.resolve()
    resolved_repo_files = [str(path.resolve()) for path in repo_files]
    index = AstProjectIndex(resolved_repo_files, str(project_root))
    index.nonblocking_start_index()
    CURRENT_PROJECT_AST_CONTEXT.set(index)
    return index
