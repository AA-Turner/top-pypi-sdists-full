"""Compare two versions of parsed file entities to produce symbol-level changes."""

from ...core.models import FileEntities, FunctionEntity, ClassEntity
from .models import SymbolChange, ChangeKind, SymbolKind, SEVERITY_MAP


def diff_file_entities(
    old: FileEntities,
    new: FileEntities,
    file_path: str,
) -> list[SymbolChange]:
    """Compare old and new FileEntities for a single file.

    Args:
        old: Entities parsed from the old version (may have empty lists).
        new: Entities parsed from the new version (may have empty lists).
        file_path: Relative path of the file.

    Returns:
        List of SymbolChange records for this file.
    """
    changes: list[SymbolChange] = []
    changes.extend(_diff_functions(old.functions, new.functions, file_path))
    changes.extend(_diff_classes(old.classes, new.classes, file_path))
    return changes


def _diff_functions(
    old_funcs: list[FunctionEntity],
    new_funcs: list[FunctionEntity],
    file_path: str,
) -> list[SymbolChange]:
    """Diff function entities between old and new versions."""
    old_map = {f.qualified_name: f for f in old_funcs}
    new_map = {f.qualified_name: f for f in new_funcs}

    old_names = set(old_map.keys())
    new_names = set(new_map.keys())

    added_names = new_names - old_names
    removed_names = old_names - new_names
    common_names = old_names & new_names

    changes: list[SymbolChange] = []

    # Check for renames: match REMOVED with ADDED by same parameters + similar short name
    matched_renames: set[tuple[str, str]] = set()  # (old_qn, new_qn)
    for removed_qn in list(removed_names):
        old_fn = old_map[removed_qn]
        for added_qn in list(added_names):
            new_fn = new_map[added_qn]
            if _is_likely_rename(old_fn, new_fn):
                matched_renames.add((removed_qn, added_qn))
                changes.append(SymbolChange(
                    symbol_kind=SymbolKind.FUNCTION,
                    change_kind=ChangeKind.RENAMED,
                    qualified_name=new_fn.qualified_name,
                    file_path=file_path,
                    old_qualified_name=old_fn.qualified_name,
                    line_start=new_fn.line_start,
                    line_end=new_fn.line_end,
                    severity=SEVERITY_MAP[ChangeKind.RENAMED],
                    details={
                        "old_name": old_fn.name,
                        "new_name": new_fn.name,
                    },
                ))
                break

    renamed_old = {r[0] for r in matched_renames}
    renamed_new = {r[1] for r in matched_renames}

    # Pure additions
    for qn in added_names - renamed_new:
        fn = new_map[qn]
        changes.append(SymbolChange(
            symbol_kind=SymbolKind.FUNCTION,
            change_kind=ChangeKind.ADDED,
            qualified_name=fn.qualified_name,
            file_path=file_path,
            line_start=fn.line_start,
            line_end=fn.line_end,
            severity=SEVERITY_MAP[ChangeKind.ADDED],
        ))

    # Pure removals
    for qn in removed_names - renamed_old:
        fn = old_map[qn]
        changes.append(SymbolChange(
            symbol_kind=SymbolKind.FUNCTION,
            change_kind=ChangeKind.REMOVED,
            qualified_name=fn.qualified_name,
            file_path=file_path,
            line_start=fn.line_start,
            line_end=fn.line_end,
            severity=SEVERITY_MAP[ChangeKind.REMOVED],
        ))

    # Compare common functions for signature vs body changes
    for qn in common_names:
        old_fn = old_map[qn]
        new_fn = new_map[qn]

        sig_changed = (
            old_fn.parameters != new_fn.parameters
            or old_fn.return_annotation != new_fn.return_annotation
        )

        if sig_changed:
            changes.append(SymbolChange(
                symbol_kind=SymbolKind.FUNCTION,
                change_kind=ChangeKind.SIGNATURE_CHANGED,
                qualified_name=qn,
                file_path=file_path,
                line_start=new_fn.line_start,
                line_end=new_fn.line_end,
                severity=SEVERITY_MAP[ChangeKind.SIGNATURE_CHANGED],
                details={
                    "old_params": old_fn.parameters,
                    "new_params": new_fn.parameters,
                    "old_return": old_fn.return_annotation,
                    "new_return": new_fn.return_annotation,
                },
            ))
        else:
            # Check for body changes via call list diff or line count change
            body_changed = (
                old_fn.calls != new_fn.calls
                or (old_fn.line_end - old_fn.line_start) != (new_fn.line_end - new_fn.line_start)
                or old_fn.cyclomatic_complexity != new_fn.cyclomatic_complexity
            )
            if body_changed:
                changes.append(SymbolChange(
                    symbol_kind=SymbolKind.FUNCTION,
                    change_kind=ChangeKind.BODY_CHANGED,
                    qualified_name=qn,
                    file_path=file_path,
                    line_start=new_fn.line_start,
                    line_end=new_fn.line_end,
                    severity=SEVERITY_MAP[ChangeKind.BODY_CHANGED],
                ))

    return changes


def _diff_classes(
    old_classes: list[ClassEntity],
    new_classes: list[ClassEntity],
    file_path: str,
) -> list[SymbolChange]:
    """Diff class entities between old and new versions."""
    old_map = {c.qualified_name: c for c in old_classes}
    new_map = {c.qualified_name: c for c in new_classes}

    old_names = set(old_map.keys())
    new_names = set(new_map.keys())

    changes: list[SymbolChange] = []

    for qn in new_names - old_names:
        cls = new_map[qn]
        changes.append(SymbolChange(
            symbol_kind=SymbolKind.CLASS,
            change_kind=ChangeKind.ADDED,
            qualified_name=qn,
            file_path=file_path,
            line_start=cls.line_start,
            line_end=cls.line_end,
            severity=SEVERITY_MAP[ChangeKind.ADDED],
        ))

    for qn in old_names - new_names:
        cls = old_map[qn]
        changes.append(SymbolChange(
            symbol_kind=SymbolKind.CLASS,
            change_kind=ChangeKind.REMOVED,
            qualified_name=qn,
            file_path=file_path,
            line_start=cls.line_start,
            line_end=cls.line_end,
            severity=SEVERITY_MAP[ChangeKind.REMOVED],
        ))

    for qn in old_names & new_names:
        old_cls = old_map[qn]
        new_cls = new_map[qn]

        sig_changed = (
            old_cls.base_classes != new_cls.base_classes
            or old_cls.is_abstract != new_cls.is_abstract
        )

        if sig_changed:
            changes.append(SymbolChange(
                symbol_kind=SymbolKind.CLASS,
                change_kind=ChangeKind.SIGNATURE_CHANGED,
                qualified_name=qn,
                file_path=file_path,
                line_start=new_cls.line_start,
                line_end=new_cls.line_end,
                severity=SEVERITY_MAP[ChangeKind.SIGNATURE_CHANGED],
                details={
                    "old_bases": old_cls.base_classes,
                    "new_bases": new_cls.base_classes,
                },
            ))
        else:
            body_changed = (
                old_cls.methods != new_cls.methods
                or old_cls.attributes != new_cls.attributes
            )
            if body_changed:
                changes.append(SymbolChange(
                    symbol_kind=SymbolKind.CLASS,
                    change_kind=ChangeKind.BODY_CHANGED,
                    qualified_name=qn,
                    file_path=file_path,
                    line_start=new_cls.line_start,
                    line_end=new_cls.line_end,
                    severity=SEVERITY_MAP[ChangeKind.BODY_CHANGED],
                ))

    return changes


def detect_cross_file_moves(
    all_removed: list[SymbolChange],
    all_added: list[SymbolChange],
) -> list[SymbolChange]:
    """Detect symbols that moved from one file to another.

    Matches REMOVED in file A with ADDED in file B when they share
    the same short name and symbol kind.

    Args:
        all_removed: All REMOVED changes across files.
        all_added: All ADDED changes across files.

    Returns:
        List of MOVED changes (replaces the matched ADDED/REMOVED pairs).
    """
    moves: list[SymbolChange] = []
    matched_removed: set[str] = set()
    matched_added: set[str] = set()

    for removed in all_removed:
        removed_short = removed.qualified_name.rsplit(".", 1)[-1]
        for added in all_added:
            if added.file_path == removed.file_path:
                continue
            added_short = added.qualified_name.rsplit(".", 1)[-1]
            if (
                removed_short == added_short
                and removed.symbol_kind == added.symbol_kind
                and removed.qualified_name not in matched_removed
                and added.qualified_name not in matched_added
            ):
                moves.append(SymbolChange(
                    symbol_kind=added.symbol_kind,
                    change_kind=ChangeKind.MOVED,
                    qualified_name=added.qualified_name,
                    file_path=added.file_path,
                    old_qualified_name=removed.qualified_name,
                    old_file_path=removed.file_path,
                    line_start=added.line_start,
                    line_end=added.line_end,
                    severity=SEVERITY_MAP[ChangeKind.MOVED],
                ))
                matched_removed.add(removed.qualified_name)
                matched_added.add(added.qualified_name)
                break

    return moves


def _is_likely_rename(old: FunctionEntity, new: FunctionEntity) -> bool:
    """Heuristic: same parameters and similar body size suggests a rename."""
    if old.parameters != new.parameters:
        return False
    old_size = old.line_end - old.line_start
    new_size = new.line_end - new.line_start
    if old_size == 0:
        return new_size <= 2
    ratio = new_size / old_size
    return 0.5 <= ratio <= 2.0
