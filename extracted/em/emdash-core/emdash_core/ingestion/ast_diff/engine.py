"""AST Diff Engine: orchestrates git diff -> parse -> symbol diff."""

import tempfile
from pathlib import Path
from typing import Optional

import git

from ...core.models import FileEntities
from ..parsers.registry import ParserRegistry
from ..parsers import PythonParser, TypeScriptParser  # noqa: F401 — trigger registration
from .git_content import get_file_at_ref, get_changed_file_paths
from .models import SymbolDiff, SymbolChange, ChangeKind
from .symbol_differ import diff_file_entities, detect_cross_file_moves


class ASTDiffEngine:
    """Produce a symbol-level diff between two git refs.

    Uses the existing parser infrastructure to parse both versions
    of each changed file, then compares extracted entities.
    """

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path).resolve()
        self.repo = git.Repo(str(self.repo_path))

    def diff(
        self,
        base_ref: str = "HEAD~1",
        head_ref: str = "HEAD",
    ) -> SymbolDiff:
        """Compute symbol-level diff between two refs.

        Args:
            base_ref: Base git ref (older).
            head_ref: Head git ref (newer).

        Returns:
            SymbolDiff with classified changes.
        """
        result = SymbolDiff(base_ref=base_ref, head_ref=head_ref)

        changed_paths = get_changed_file_paths(self.repo, base_ref, head_ref)
        if not changed_paths:
            return result

        all_changes: list[SymbolChange] = []

        for file_path, change_type in changed_paths.items():
            if not ParserRegistry.is_supported(Path(file_path)):
                continue

            result.files_analyzed += 1

            old_entities = self._parse_at_ref(file_path, base_ref) if change_type != "A" else _empty_entities()
            new_entities = self._parse_at_ref(file_path, head_ref) if change_type != "D" else _empty_entities()

            if old_entities is None:
                result.parse_errors.append(f"Failed to parse old version of {file_path}")
                old_entities = _empty_entities()
            if new_entities is None:
                result.parse_errors.append(f"Failed to parse new version of {file_path}")
                new_entities = _empty_entities()

            file_changes = diff_file_entities(old_entities, new_entities, file_path)
            all_changes.extend(file_changes)

        # Cross-file move detection
        all_removed = [c for c in all_changes if c.change_kind == ChangeKind.REMOVED]
        all_added = [c for c in all_changes if c.change_kind == ChangeKind.ADDED]
        moves = detect_cross_file_moves(all_removed, all_added)

        if moves:
            moved_old_qns = {m.old_qualified_name for m in moves}
            moved_new_qns = {m.qualified_name for m in moves}
            all_changes = [
                c for c in all_changes
                if not (c.change_kind == ChangeKind.REMOVED and c.qualified_name in moved_old_qns)
                and not (c.change_kind == ChangeKind.ADDED and c.qualified_name in moved_new_qns)
            ]
            all_changes.extend(moves)

        result.changes = all_changes
        return result

    def _parse_at_ref(self, file_path: str, ref: str) -> Optional[FileEntities]:
        """Parse a file at a specific git ref.

        Writes the blob content to a temp file so the existing
        parsers (which read from the filesystem) can process it.
        """
        content = get_file_at_ref(self.repo, file_path, ref)
        if content is None:
            return None

        parser_cls = ParserRegistry.get_parser(Path(file_path))
        if parser_cls is None:
            return None

        suffix = Path(file_path).suffix
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=suffix,
                dir=str(self.repo_path),
                delete=True,
                encoding="utf-8",
            ) as tmp:
                tmp.write(content)
                tmp.flush()

                parser = parser_cls(
                    file_path=Path(tmp.name),
                    repo_root=self.repo_path,
                )
                return parser.parse()
        except Exception:
            return None


def _empty_entities() -> FileEntities:
    """Return an empty FileEntities instance."""
    return FileEntities()
