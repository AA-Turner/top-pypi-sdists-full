"""User-facing release notes: validation, generation and per-language merge.

The pure logic (validation, section building, markdown/txt merge, config) lives
in :mod:`.core`; git data collection in :mod:`.gather`; the Typer command layer
in :mod:`.cli`; version-tag semantics in :mod:`..versioning`. This package
re-exports the stable public surface so callers keep importing from
``pysae_ai_tools.code.release_notes``.
"""

from .cli import app as app
from .core import APPLE_STORE_SUFFIX as APPLE_STORE_SUFFIX
from .core import CANONICAL_SECTIONS as CANONICAL_SECTIONS
from .core import CANONICAL_TXT_SECTIONS as CANONICAL_TXT_SECTIONS
from .core import GOOGLE_PLAY_SUFFIX as GOOGLE_PLAY_SUFFIX
from .core import LANGUAGE_HEADERS as LANGUAGE_HEADERS
from .core import MAINTENANCE_NOTE as MAINTENANCE_NOTE
from .core import MAX_LINE_LENGTH as MAX_LINE_LENGTH
from .core import MAX_TXT_500_LENGTH as MAX_TXT_500_LENGTH
from .core import MAX_TXT_4000_LENGTH as MAX_TXT_4000_LENGTH
from .core import SUPPORTED_LANGUAGES as SUPPORTED_LANGUAGES
from .core import SUPPORTED_VARIANTS as SUPPORTED_VARIANTS
from .core import BodyViolation as BodyViolation
from .core import ChangelogPendingEntry as ChangelogPendingEntry
from .core import CommitInfo as CommitInfo
from .core import ReleaseNotesConfig as ReleaseNotesConfig
from .core import _merge_variant_content as _merge_variant_content
from .core import build_section as build_section
from .core import build_txt_section as build_txt_section
from .core import merge_release_notes as merge_release_notes
from .core import merge_txt_release_notes as merge_txt_release_notes
from .core import release_config as release_config
from .core import release_notes_apple_app_store_file as release_notes_apple_app_store_file
from .core import release_notes_file as release_notes_file
from .core import release_notes_google_play_file as release_notes_google_play_file
from .core import validate_body as validate_body
from .core import validate_txt_body as validate_txt_body
from .gather import list_commits_since_tag as list_commits_since_tag
from .gather import list_pending_changelog_entries as list_pending_changelog_entries
from .gather import resolve_latest_tag as resolve_latest_tag
