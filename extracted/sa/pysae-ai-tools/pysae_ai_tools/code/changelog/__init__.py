"""Changelog entry generation, validation and CHANGELOG.md merge.

The pure logic (entry generation, validation, markdown merge) lives in
:mod:`.core`; the Typer command layer and file-I/O orchestration in :mod:`.cli`;
version-tag semantics in :mod:`..versioning`. This package re-exports the stable
public surface so callers keep importing from ``pysae_ai_tools.code.changelog``.
"""

from ..versioning import is_hotfix_tag as is_hotfix_tag
from ..versioning import is_store_skipping_prerelease as is_store_skipping_prerelease
from .cli import _validate_files as _validate_files
from .cli import app as app
from .cli import release as release
from .cli import resolve_project_url as resolve_project_url
from .core import MAX_ENTRY_LENGTH as MAX_ENTRY_LENGTH
from .core import ChangelogEntry as ChangelogEntry
from .core import ChangelogTooLongError as ChangelogTooLongError
from .core import _delink_issue_refs as _delink_issue_refs
from .core import _description_from_branch as _description_from_branch
from .core import _detect_type_from_branch as _detect_type_from_branch
from .core import _detect_type_from_labels as _detect_type_from_labels
from .core import _extract_issue_iid as _extract_issue_iid
from .core import _length_failure_reason as _length_failure_reason
from .core import _linkify_issue_refs as _linkify_issue_refs
from .core import find_existing_section as find_existing_section
from .core import generate_entry as generate_entry
from .core import merge_changelog as merge_changelog
