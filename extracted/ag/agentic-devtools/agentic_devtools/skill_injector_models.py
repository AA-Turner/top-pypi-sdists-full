"""Value objects describing a planned injection."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class InjectionPlan:
    """The manifest diff computed for one kind (``agents``/``prompts``/``skills``).

    Attributes:
        kind: ``"agents"``, ``"prompts"`` or ``"skills"``.
        added: Destination names present in the source set and absent from the
            target directory.  Writing them is harmless.  Flat kinds use the
            flattened filename; the ``skills`` kind uses the skill-relative
            POSIX path (e.g. ``my-skill/SKILL.md``).
        overwritten: Destination names present in both, with different bytes.
            Under a wheel install these silently replace target content with
            the installed wheel's content.
        deleted: Planned deletion entries in the target directory.  For the flat
            kinds this includes managed ``agdt.*`` filenames absent from the
            source set (including files the classification filter pruned), plus
            ``".agdt/"`` when the legacy migration would remove that
            subdirectory or symlink.  For the ``skills`` kind it lists the
            previously-injected skill files (as recorded in the managed
            manifest) that the current source set no longer carries; a skill
            directory left empty by those deletions is removed too.
        case_renames: Pairs of ``(old_name, new_name)`` where both names share
            the same casefold and resolved to the same inode on the target
            filesystem (case-insensitive rename detected during planning).
            Only populated for the ``skills`` kind.  The execution phase uses
            this to perform a two-step rename so the directory-entry casing is
            updated before the new content is written.
    """

    kind: str
    added: tuple[str, ...]
    overwritten: tuple[str, ...]
    deleted: tuple[str, ...]
    case_renames: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class InjectionSummary:
    """Counts describing the outcome of a skill-injection pass.

    Attributes:
        injected: Total number of units selected for injection across the three
            kinds — the managed ``agdt.*`` files for ``agents`` and ``prompts``
            (de-duplicated by flattened filename within each kind, excluding the
            generated ``agdt.README.md`` manifests) plus one unit per mirrored
            skill for ``skills`` (its bundled resources are not counted
            separately).  This is a best-effort count and can include files
            counted before a later write-time ``OSError``.
        pruned: Total number of source units removed by the classification
            filter across the three kinds.  Always ``0`` when neither platform
            axis is resolved (legacy inject-all), because filtering is skipped
            entirely in that case.
        plans: The per-kind manifest diff (adds / overwrites / deletes) computed
            by the planning phase.  Excluded from equality comparisons so that
            summaries continue to compare by their counts.
        deletions_blocked: ``True`` when the pass refused to run because it
            would have deleted planned entries and the caller did not pass
            ``assume_yes``.  Nothing was written, copied or unlinked.
    """

    injected: int
    pruned: int
    plans: tuple[InjectionPlan, ...] = field(default=(), compare=False)
    deletions_blocked: bool = field(default=False, compare=False)
