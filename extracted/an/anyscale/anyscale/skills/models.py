from dataclasses import dataclass, field
from enum import Enum
import os
from typing import Any, ClassVar, Dict, List, Optional

from anyscale._private.models import ModelBase


class Platform(str, Enum):
    """Supported installation platforms for skills."""

    CLAUDE_CODE = "claude-code"
    CURSOR = "cursor"
    CODEX = "codex"
    COPILOT = "copilot"


@dataclass(frozen=True)
class ConfigDir:
    """A config directory root that an env var may relocate."""

    default: str
    """Directory used when the env var is unset; a leading `~` is expanded."""

    env_var: Optional[str] = None
    """Env var that overrides `default` when set and non-empty; None means fixed."""

    env_subpath: str = ""
    """Subpath appended only under an override (`default` already includes it)."""

    def resolve(self) -> str:
        """Absolute dir, honoring env_var when set and non-empty."""
        # Env values should be absolute: ~ is expanded here (CLI-side) but NOT by the shipped
        # shell hook (${VAR:-$HOME/...}), so absolute values keep them in sync. A relative
        # override is still normalized to absolute so metadata/cleanup don't depend on cwd.
        override = os.environ.get(self.env_var) if self.env_var else None
        if override:
            base = os.path.expanduser(override)
            resolved = (
                os.path.join(base, self.env_subpath) if self.env_subpath else base
            )
        else:
            resolved = os.path.expanduser(self.default)
        return os.path.abspath(resolved)


@dataclass(frozen=True)
class PlatformMetadata:
    """Static install layout for a supported skills CLI target."""

    display: str
    skills_dir: ConfigDir
    hooks_dir: ConfigDir
    hooks_config: str


@dataclass(frozen=True)
class CatalogEntry(ModelBase):
    """A skill or hook entry in the skills catalog."""

    name: str = field(metadata={"docstring": "Unique identifier (e.g. 'deploy')."})
    type: str = field(  # noqa: A003
        metadata={"docstring": "Entry type (e.g. 'skill', 'hook')."}
    )
    description: str = field(metadata={"docstring": "Human-readable description."})
    # Intentionally List[str], not List[Platform]: this field is backend-owned
    # and may include platform values the installed CLI doesn't yet know about
    # (forward-compat). Converting to Platform at the boundary would crash on
    # unknown values; keeping it as str lets older CLIs pass-through cleanly.
    platforms: List[str] = field(
        default_factory=list,
        metadata={
            "docstring": "Target platforms (e.g. ['claude-code', 'cursor', 'codex'])."
        },
    )

    def _validate_name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("name must be a string.")

    def _validate_type(self, type: str):  # noqa: A002
        if not isinstance(type, str):
            raise TypeError("type must be a string.")

    def _validate_description(self, description: str):
        if not isinstance(description, str):
            raise TypeError("description must be a string.")

    def _validate_platforms(self, platforms: List[str]):
        if not isinstance(platforms, list):
            raise TypeError("platforms must be a list.")


@dataclass(frozen=True)
class SkillsManifest(ModelBase):
    """Manifest describing a skills version's catalog and (optionally) its bundle.

    `bundle_url` / `bundle_checksum` are None when the manifest was fetched
    without requesting the bundle URL (e.g. by `list`, which only needs the
    catalog and must work before the user has accepted the license).
    """

    version: str = field(metadata={"docstring": "Semantic version string."})
    catalog: List[CatalogEntry] = field(
        metadata={"docstring": "List of skills/hooks in this version."}
    )
    bundle_url: Optional[str] = field(
        default=None,
        metadata={
            "docstring": (
                "Presigned S3 GET URL for the bundle tarball. "
                "None when the manifest was fetched without the bundle URL."
            )
        },
    )
    bundle_checksum: Optional[str] = field(
        default=None,
        metadata={
            "docstring": (
                "SHA-256 hex digest of the bundle tarball. "
                "None when the manifest was fetched without the bundle URL."
            )
        },
    )

    def _validate_version(self, version: str):
        if not isinstance(version, str):
            raise TypeError("version must be a string.")

    def _validate_catalog(self, catalog: List[CatalogEntry]):
        if not isinstance(catalog, list):
            raise TypeError("catalog must be a list.")

    def _validate_bundle_url(self, bundle_url: Optional[str]):
        if bundle_url is not None and not isinstance(bundle_url, str):
            raise TypeError("bundle_url must be a string or None.")

    def _validate_bundle_checksum(self, bundle_checksum: Optional[str]):
        if bundle_checksum is not None and not isinstance(bundle_checksum, str):
            raise TypeError("bundle_checksum must be a string or None.")


@dataclass(frozen=True)
class TermsStatus(ModelBase):
    """Current user's terms acceptance status for a skills version."""

    version: str = field(metadata={"docstring": "Version the terms apply to."})
    license_hash: str = field(metadata={"docstring": "SHA-256 of the license text."})
    accepted: bool = field(
        metadata={"docstring": "Whether the user has accepted terms for this version."}
    )
    accepted_at: Optional[str] = field(
        default=None,
        metadata={"docstring": "ISO-8601 timestamp of acceptance, if accepted."},
    )
    license_text: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "Full license text. Only populated when accepted is false."
        },
    )

    def _validate_version(self, version: str):
        if not isinstance(version, str):
            raise TypeError("version must be a string.")

    def _validate_license_hash(self, license_hash: str):
        if not isinstance(license_hash, str):
            raise TypeError("license_hash must be a string.")

    def _validate_accepted(self, accepted: bool):
        if not isinstance(accepted, bool):
            raise TypeError("accepted must be a bool.")

    def _validate_accepted_at(self, accepted_at: Optional[str]):
        pass

    def _validate_license_text(self, license_text: Optional[str]):
        pass


@dataclass(frozen=True)
class PlatformInstallInfo(ModelBase):
    """Per-platform installation state stored in metadata."""

    skills_dir: str = field(
        metadata={"docstring": "Absolute root where skill folders were written."}
    )
    hooks_dir: str = field(
        metadata={
            "docstring": "Absolute root where hooks config + scripts were written."
        }
    )
    skills_files: List[str] = field(
        default_factory=list,
        metadata={"docstring": "Paths of skill files, relative to skills_dir."},
    )
    hooks_files: List[str] = field(
        default_factory=list,
        metadata={"docstring": "Paths of hooks files, relative to hooks_dir."},
    )

    def _validate_skills_dir(self, skills_dir: str):
        if not isinstance(skills_dir, str):
            raise TypeError("skills_dir must be a string.")

    def _validate_hooks_dir(self, hooks_dir: str):
        if not isinstance(hooks_dir, str):
            raise TypeError("hooks_dir must be a string.")

    def _validate_skills_files(self, skills_files: List[str]):
        if not isinstance(skills_files, list):
            raise TypeError("skills_files must be a list.")

    def _validate_hooks_files(self, hooks_files: List[str]):
        if not isinstance(hooks_files, list):
            raise TypeError("hooks_files must be a list.")


@dataclass(frozen=True)
class InstalledMetadata(ModelBase):
    """On-disk installation metadata (installed.json)."""

    CURRENT_SCHEMA_VERSION: ClassVar[int] = 2

    version: str = field(metadata={"docstring": "Installed version string."})
    license_hash: str = field(metadata={"docstring": "SHA-256 of accepted license."})
    platforms: Dict[Platform, PlatformInstallInfo] = field(
        metadata={"docstring": "Per-platform install info keyed by platform value."},
    )
    checksum: str = field(
        default="",
        metadata={"docstring": "SHA-256 hex digest of the installed bundle."},
    )
    catalog: List[CatalogEntry] = field(
        default_factory=list,
        metadata={"docstring": "Catalog entries at the installed version."},
    )
    schema_version: int = field(
        default=CURRENT_SCHEMA_VERSION,
        metadata={"docstring": "Metadata schema version."},
    )
    installed_at: Optional[str] = field(
        default=None,
        metadata={"docstring": "ISO-8601 timestamp of last install/update."},
    )

    def _validate_version(self, version: str):
        if not isinstance(version, str):
            raise TypeError("version must be a string.")

    def _validate_license_hash(self, license_hash: str):
        if not isinstance(license_hash, str):
            raise TypeError("license_hash must be a string.")

    def _validate_platforms(self, platforms: Dict[Platform, PlatformInstallInfo]):
        if not isinstance(platforms, dict):
            raise TypeError("platforms must be a dict.")

    def _validate_checksum(self, checksum: str):
        if not isinstance(checksum, str):
            raise TypeError("checksum must be a string.")

    def _validate_catalog(self, catalog: List[CatalogEntry]):
        if not isinstance(catalog, list):
            raise TypeError("catalog must be a list.")

    def _validate_schema_version(self, schema_version: int):
        pass

    def _validate_installed_at(self, installed_at: Optional[str]):
        pass

    def to_dict(self, *, exclude_none: bool = True) -> Dict[str, Any]:
        # ModelBase.to_dict doesn't recurse into Dict[K, ModelBase] fields; do
        # the platforms conversion explicitly so on-disk shape stays flat.
        d = super().to_dict(exclude_none=exclude_none)
        d["platforms"] = {
            (k.value if isinstance(k, Platform) else k): v.to_dict(
                exclude_none=exclude_none
            )
            for k, v in self.platforms.items()
        }
        return d


@dataclass(frozen=True)
class SkillsListResult(ModelBase):
    """Return type for the skills list operation."""

    installed: Optional[InstalledMetadata] = field(
        metadata={
            "docstring": "Current installation metadata, or None if not installed."
        },
    )
    available_version: str = field(
        metadata={"docstring": "Latest (or requested) available version."},
    )
    available_catalog: List[CatalogEntry] = field(
        metadata={"docstring": "Catalog entries for the available version."},
    )
    up_to_date: bool = field(
        metadata={"docstring": "Whether the installed version matches available."},
    )
    added: List[CatalogEntry] = field(
        default_factory=list,
        metadata={"docstring": "Catalog entries added since the installed version."},
    )
    removed: List[CatalogEntry] = field(
        default_factory=list,
        metadata={"docstring": "Catalog entries removed since the installed version."},
    )
    updated: List[CatalogEntry] = field(
        default_factory=list,
        metadata={
            "docstring": (
                "Catalog entries whose description changed since the installed "
                "version. Platform-list-only changes are not counted here; see "
                "added_platforms / removed_platforms."
            )
        },
    )
    added_platforms: List[str] = field(
        default_factory=list,
        metadata={
            "docstring": (
                "Platforms newly supported by the available catalog (union "
                "across all entries) since the installed version."
            )
        },
    )
    removed_platforms: List[str] = field(
        default_factory=list,
        metadata={
            "docstring": (
                "Platforms no longer supported by the available catalog since "
                "the installed version."
            )
        },
    )

    def _validate_installed(self, installed: Optional[InstalledMetadata]):
        pass

    def _validate_available_version(self, available_version: str):
        if not isinstance(available_version, str):
            raise TypeError("available_version must be a string.")

    def _validate_available_catalog(self, available_catalog: List[CatalogEntry]):
        if not isinstance(available_catalog, list):
            raise TypeError("available_catalog must be a list.")

    def _validate_up_to_date(self, up_to_date: bool):
        if not isinstance(up_to_date, bool):
            raise TypeError("up_to_date must be a bool.")

    def _validate_added(self, added: List[CatalogEntry]):
        if not isinstance(added, list):
            raise TypeError("added must be a list.")

    def _validate_removed(self, removed: List[CatalogEntry]):
        if not isinstance(removed, list):
            raise TypeError("removed must be a list.")

    def _validate_updated(self, updated: List[CatalogEntry]):
        if not isinstance(updated, list):
            raise TypeError("updated must be a list.")

    def _validate_added_platforms(self, added_platforms: List[str]):
        if not isinstance(added_platforms, list):
            raise TypeError("added_platforms must be a list.")

    def _validate_removed_platforms(self, removed_platforms: List[str]):
        if not isinstance(removed_platforms, list):
            raise TypeError("removed_platforms must be a list.")


@dataclass(frozen=True)
class InstalledSkillsOutput(ModelBase):
    """Installed-state summary in `anyscale skills list` structured output."""

    version: str = field(metadata={"docstring": "Installed version string."})
    platforms: List[str] = field(
        default_factory=list,
        metadata={"docstring": "Platform names the skills are installed for."},
    )
    installed_at: Optional[str] = field(
        default=None,
        metadata={"docstring": "ISO-8601 install timestamp, if recorded."},
    )

    def _validate_version(self, version: str):
        if not isinstance(version, str):
            raise TypeError("version must be a string.")

    def _validate_platforms(self, platforms: List[str]):
        if not isinstance(platforms, list):
            raise TypeError("platforms must be a list.")

    def _validate_installed_at(self, installed_at: Optional[str]):
        if installed_at is not None and not isinstance(installed_at, str):
            raise TypeError("installed_at must be a string.")


@dataclass(frozen=True)
class SkillsListOutput(ModelBase):
    """Structured output of `anyscale skills list`.

    A curated view of SkillsListResult: what is installed, whether it is up to
    date, and the available catalog.
    """

    available_version: str = field(
        metadata={"docstring": "Latest (or requested) available version."},
    )
    up_to_date: bool = field(
        metadata={"docstring": "Whether the installed version matches available."},
    )
    installed: Optional[InstalledSkillsOutput] = field(
        default=None,
        metadata={
            "docstring": "Current installation summary, or None if not installed."
        },
    )
    available_catalog: List[CatalogEntry] = field(
        default_factory=list,
        metadata={"docstring": "Catalog entries for the available version."},
    )

    def _validate_available_version(self, available_version: str):
        if not isinstance(available_version, str):
            raise TypeError("available_version must be a string.")

    def _validate_up_to_date(self, up_to_date: bool):
        if not isinstance(up_to_date, bool):
            raise TypeError("up_to_date must be a bool.")

    def _validate_installed(self, installed: Optional[InstalledSkillsOutput]):
        pass

    def _validate_available_catalog(self, available_catalog: List[CatalogEntry]):
        if not isinstance(available_catalog, list):
            raise TypeError("available_catalog must be a list.")


PLATFORMS: Dict[Platform, PlatformMetadata] = {
    Platform.CLAUDE_CODE: PlatformMetadata(
        display="Claude Code",
        skills_dir=ConfigDir("~/.claude/skills", "CLAUDE_CONFIG_DIR", "skills"),
        hooks_dir=ConfigDir("~/.claude", "CLAUDE_CONFIG_DIR"),
        hooks_config="settings.json",
    ),
    Platform.CURSOR: PlatformMetadata(
        display="Cursor",
        skills_dir=ConfigDir("~/.cursor/skills", "CURSOR_CONFIG_DIR", "skills"),
        hooks_dir=ConfigDir("~/.cursor", "CURSOR_CONFIG_DIR"),
        hooks_config="hooks.json",
    ),
    Platform.CODEX: PlatformMetadata(
        display="Codex",
        skills_dir=ConfigDir("~/.agents/skills"),
        hooks_dir=ConfigDir("~/.codex", "CODEX_HOME"),
        hooks_config="hooks.json",
    ),
    Platform.COPILOT: PlatformMetadata(
        display="GitHub Copilot",
        # ~/.agents/skills is shared with Codex; COPILOT_HOME relocates only hooks.
        skills_dir=ConfigDir("~/.agents/skills"),
        hooks_dir=ConfigDir("~/.copilot", "COPILOT_HOME"),
        hooks_config="settings.json",
    ),
}
