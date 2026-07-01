import contextlib
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from io import BytesIO
import json
import os
import shutil
import tarfile
import tempfile
from typing import Callable, Dict, List, Optional, Tuple

import requests

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.skills.errors import (
    AlreadyInstalledError,
    PlatformVersionMismatchError,
    SKILLS_TERMS_DOC_URL,
    TermsNotAcceptedError,
)
from anyscale.skills.models import (
    CatalogEntry,
    InstalledMetadata,
    Platform,
    PlatformInstallInfo,
    PlatformMetadata,
    PLATFORMS,
    SkillsListResult,
    SkillsManifest,
    TermsStatus,
)


METADATA_DIR = os.path.join("~", ".anyscale", "skills")
INSTALLED_METADATA_FILE = "installed.json"

_MANAGED_BY_TAG = "anyscale-skills"

_SKILLS_PREFIX = "skills" + os.sep


def _normalize_version(version: Optional[str]) -> Optional[str]:
    """Strip a single leading 'v' so '0.0.1' and 'v0.0.1' are equivalent."""
    if version is None:
        return None
    stripped = version.strip()
    if stripped[:1] in ("v", "V"):
        stripped = stripped[1:]
    return stripped


def _catalog_entry_key(entry: CatalogEntry) -> tuple:
    """Stable composite key for a catalog entry."""
    platforms = tuple(sorted(entry.platforms)) if entry.platforms else ()
    return (entry.type, entry.name, platforms)


def _catalog_diff(old: List[CatalogEntry], new: List[CatalogEntry]) -> tuple:
    """Return (added, removed) catalog entries between two versions."""
    old_map = {_catalog_entry_key(entry): entry for entry in old}
    new_map = {_catalog_entry_key(entry): entry for entry in new}
    added = [new_map[key] for key in new_map if key not in old_map]
    removed = [old_map[key] for key in old_map if key not in new_map]
    return added, removed


def _load_json(path: str, *, strict: bool = False) -> dict:
    """Load a JSON file. Returns {} if missing or (when not strict) on parse error.

    Use strict=True for bundle files where a malformed JSON should fail fast.
    """
    if not os.path.exists(path):
        return {}
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        if strict:
            raise
        return {}


def _save_json(path: str, data: dict) -> None:
    """Atomically write JSON to path via a sibling tempfile + os.replace.

    A crash or disk-full mid-write can't leave the target truncated: either
    the old file is still intact, or the new file is fully written and
    renamed into place.
    """
    parent = os.path.dirname(os.path.abspath(path))
    os.makedirs(parent, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=parent, prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        os.replace(tmp_path, path)
    except Exception:
        with contextlib.suppress(OSError):
            os.remove(tmp_path)
        raise


def _skills_filter(member: tarfile.TarInfo, dest_path: str) -> tarfile.TarInfo:
    """Reject unsafe tar members; delegate the rest to tarfile.data_filter.

    Strictly refuses symlinks, hardlinks, device files, and FIFOs. When
    tarfile.data_filter is available (Python 3.9.17+/3.10.12+/3.11.4+/3.12+
    via PEP 706 backport) we delegate path-traversal and mode-bit sanitization
    to the stdlib; otherwise we fall back to a manual realpath containment
    check. Raises ValueError on any unsafe member.
    """
    if member.issym() or member.islnk():
        raise ValueError(f"Skills bundle contains link: {member.name}")
    if not (member.isfile() or member.isdir()):
        raise ValueError(
            f"Skills bundle contains unsupported entry type: {member.name}"
        )
    data_filter = getattr(tarfile, "data_filter", None)
    if data_filter is not None:
        try:
            return data_filter(member, dest_path)
        except tarfile.FilterError as e:  # type: ignore[attr-defined]
            # FilterError ships alongside data_filter in the same PEP 706 backport.
            raise ValueError(f"Skills bundle contains unsafe entry: {e}") from e
    real_dest = os.path.realpath(dest_path)
    resolved = os.path.realpath(os.path.join(dest_path, member.name))
    if resolved != real_dest and not resolved.startswith(real_dest + os.sep):
        raise ValueError(f"Skills bundle contains unsafe path: {member.name}")
    return member


def _strip_managed_hooks(hooks: dict) -> dict:
    """Remove all hook groups tagged with _managed_by from a hooks dict."""
    return {
        event: [
            group for group in groups if group.get("_managed_by") != _MANAGED_BY_TAG
        ]
        for event, groups in hooks.items()
    }


def _merge_hooks_config(existing_path: str, bundle_path: str) -> None:
    """Merge hooks from the bundle config into an existing config file."""
    existing = _load_json(existing_path)
    bundle = _load_json(bundle_path, strict=True)

    merged_hooks = _strip_managed_hooks(existing.get("hooks", {}))
    for event, groups in bundle.get("hooks", {}).items():
        merged_hooks.setdefault(event, []).extend(groups)

    existing["hooks"] = merged_hooks
    _save_json(existing_path, existing)


def _migrate_v1_to_v2(data: dict) -> dict:
    """Split v1 per-platform {target_dir, installed_files} into v2 fields."""
    new_platforms = {}
    for platform_key, info in data.get("platforms", {}).items():
        target_dir = info.get("target_dir", "")
        installed_files = info.get("installed_files", []) or []
        skills_files: List[str] = []
        hooks_files: List[str] = []
        for rel_path in installed_files:
            if rel_path.startswith(_SKILLS_PREFIX):
                skills_files.append(rel_path[len(_SKILLS_PREFIX) :])
            else:
                hooks_files.append(rel_path)
        new_platforms[platform_key] = {
            "skills_dir": (os.path.join(target_dir, "skills") if target_dir else ""),
            "hooks_dir": target_dir,
            "skills_files": skills_files,
            "hooks_files": hooks_files,
        }
    return {**data, "schema_version": 2, "platforms": new_platforms}


_MIGRATIONS: List[Tuple[int, int, Callable[[dict], dict]]] = [
    (1, 2, _migrate_v1_to_v2),
]


def _migrate_to_current(data: dict) -> dict:
    """Walk _MIGRATIONS until data is at InstalledMetadata.CURRENT_SCHEMA_VERSION."""
    current = data.get("schema_version", 1)
    for src, dst, fn in _MIGRATIONS:
        if current == src:
            data = fn(data)
            current = dst
    if current != InstalledMetadata.CURRENT_SCHEMA_VERSION:
        raise ValueError(
            f"No migration path from schema_version {current} to "
            f"{InstalledMetadata.CURRENT_SCHEMA_VERSION}."
        )
    return data


@dataclass(frozen=True)
class _InstallPlan:
    """Resolved install inputs. Bundle is either pre-loaded bytes or a URL.

    `bundle_checksum` is the server-supplied SHA-256 of the tarball and is
    only present on the API path, where we verify what we downloaded matches
    what the manifest response declared. For `--from-file` the bytes are
    already on disk and there's no out-of-band hash to verify against.
    """

    version: str
    license_hash: str
    catalog: List[CatalogEntry]
    bundle_checksum: Optional[str] = None
    bundle: Optional[bytes] = None
    bundle_url: Optional[str] = None

    def __post_init__(self):
        if (self.bundle is None) == (self.bundle_url is None):
            raise ValueError(
                "_InstallPlan requires exactly one of bundle or bundle_url."
            )
        if self.bundle_url is not None and self.bundle_checksum is None:
            raise ValueError("_InstallPlan with bundle_url requires bundle_checksum.")


class PrivateSkillsSDK(BaseSDK):
    """Private SDK for skills install/update operations."""

    def __init__(
        self,
        *,
        platform_configs: Optional[Dict[Platform, PlatformMetadata]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.metadata_dir = os.path.expanduser(METADATA_DIR)
        self.metadata_path = os.path.join(self.metadata_dir, INSTALLED_METADATA_FILE)
        self._platform_configs: Dict[Platform, PlatformMetadata] = (
            platform_configs if platform_configs is not None else PLATFORMS
        )

    def list(self, version: Optional[str] = None) -> SkillsListResult:
        """List installed skills and available updates.

        Fetches the manifest catalog-only (no presigned bundle URL) so the
        call succeeds before the user has accepted the license terms.
        """
        version = _normalize_version(version)
        if version is not None:
            manifest = self._fetch_manifest(version, include_bundle_url=False)
            return SkillsListResult(
                installed=None,
                available_version=manifest.version,
                available_catalog=manifest.catalog,
                up_to_date=False,
            )

        metadata = self._load_metadata()
        manifest = self._fetch_manifest(include_bundle_url=False)

        installed_catalog = metadata.catalog if metadata else []

        up_to_date = metadata is not None and metadata.version == manifest.version
        added: List[CatalogEntry] = []
        removed: List[CatalogEntry] = []
        if metadata and not up_to_date:
            added, removed = _catalog_diff(installed_catalog, manifest.catalog)

        return SkillsListResult(
            installed=metadata,
            available_version=manifest.version,
            available_catalog=manifest.catalog,
            up_to_date=up_to_date,
            added=added,
            removed=removed,
        )

    def install(
        self,
        platforms: List[Platform],
        version: Optional[str] = None,
        accept_terms: bool = False,
        force: bool = False,
        from_file: Optional[str] = None,
    ) -> str:
        """Install skills for the specified platform(s).

        Returns the installed version string.
        """
        version = _normalize_version(version)
        plan = self._resolve_install_source(
            version=version, accept_terms=accept_terms, from_file=from_file,
        )
        existing_metadata = self._load_metadata()
        target_platforms = self._resolve_target_platforms(
            requested=list(platforms),
            plan=plan,
            existing_metadata=existing_metadata,
            force=force,
        )
        if target_platforms is None:
            return plan.version

        self._install_from_plan(
            plan, target_platforms, existing_metadata=existing_metadata,
        )
        return plan.version

    def update(self, force: bool = False, accept_terms: bool = False) -> str:
        """Update skills to the latest version.

        Returns the updated version string.
        """
        metadata = self._load_metadata()
        if metadata is None:
            raise ValueError(
                "No skills installed. Run 'anyscale skills install' first."
            )

        terms = self._fetch_terms()
        if terms.version == metadata.version and not force:
            return metadata.version

        self._handle_terms_acceptance(terms, accept_terms=accept_terms)
        manifest = self._fetch_manifest(terms.version)
        plan = _InstallPlan(
            version=terms.version,
            license_hash=terms.license_hash,
            bundle_checksum=manifest.bundle_checksum,
            catalog=manifest.catalog,
            bundle_url=manifest.bundle_url,
        )

        self._install_from_plan(
            plan, list(metadata.platforms), existing_metadata=metadata,
        )

        if metadata.license_hash != plan.license_hash:
            self._logger.info(
                f"License terms have been updated: {SKILLS_TERMS_DOC_URL}"
            )
        return plan.version

    def _fetch_manifest(
        self, version: Optional[str] = None, *, include_bundle_url: bool = True,
    ) -> SkillsManifest:
        """Fetch the skills manifest from the API.

        When include_bundle_url is False, the returned manifest has
        bundle_url and bundle_checksum set to None and the backend does
        not require terms acceptance.
        """
        response = self.client.get_skills_manifest(
            version=version, include_bundle_url=include_bundle_url,
        )
        return SkillsManifest(
            version=response.version,
            catalog=[
                CatalogEntry(
                    name=entry.name,
                    type=entry.type,
                    description=entry.description,
                    platforms=entry.platforms or [],
                )
                for entry in response.catalog
            ],
            bundle_url=response.bundle_url,
            bundle_checksum=response.bundle_checksum,
        )

    def _fetch_terms(self, version: Optional[str] = None) -> TermsStatus:
        """Fetch the current user's terms acceptance status."""
        response = self.client.get_skills_terms(version=version)
        return TermsStatus(
            version=response.version,
            license_hash=response.license_hash,
            accepted=response.accepted,
            accepted_at=str(response.accepted_at) if response.accepted_at else None,
            license_text=response.license_text,
        )

    def accept_terms(self, terms: TermsStatus) -> None:
        """Record acceptance of the given terms version.

        No-op if the user has already accepted this version's license.
        """
        if terms.accepted:
            return
        self.client.accept_skills_terms(license_hash=terms.license_hash)

    def _handle_terms_acceptance(self, terms: TermsStatus, accept_terms: bool) -> None:
        """Raise if terms are unaccepted and the caller didn't opt in; else record."""
        if terms.accepted:
            return
        if not accept_terms:
            raise TermsNotAcceptedError(terms)
        self.accept_terms(terms)

    def get_terms(self, version: Optional[str] = None) -> TermsStatus:
        """Fetch current terms status for a version (defaults to latest)."""
        return self._fetch_terms(version=_normalize_version(version))

    def _verify_checksum(self, data: bytes, expected: str) -> None:
        """Verify the downloaded bundle matches the manifest's SHA256."""
        expected_hex = (
            expected[len("sha256:") :] if expected.startswith("sha256:") else expected
        )
        actual_hex = hashlib.sha256(data).hexdigest()
        if actual_hex.lower() != expected_hex.lower():
            raise ValueError(
                f"Bundle checksum mismatch: expected {expected_hex}, got {actual_hex}.\n"
                "  The download may be corrupted; please retry."
            )

    def _resolve_install_source(
        self, *, version: Optional[str], accept_terms: bool, from_file: Optional[str],
    ) -> _InstallPlan:
        """Pick the install source (local file or API) and return a plan."""
        if from_file is not None:
            if not accept_terms:
                raise ValueError(
                    "--from-file requires --accept-terms since the terms API "
                    "is not called in offline mode."
                )
            return self._load_plan_from_file(from_file)
        return self._load_plan_from_api(version=version, accept_terms=accept_terms)

    def _load_plan_from_api(
        self, *, version: Optional[str], accept_terms: bool,
    ) -> _InstallPlan:
        """Fetch terms + manifest from the API; license acceptance happens here."""
        terms = self._fetch_terms(version)
        self._handle_terms_acceptance(terms, accept_terms)
        manifest = self._fetch_manifest(terms.version)
        return _InstallPlan(
            version=terms.version,
            license_hash=terms.license_hash,
            bundle_checksum=manifest.bundle_checksum,
            catalog=manifest.catalog,
            bundle_url=manifest.bundle_url,
        )

    def _load_plan_from_file(self, path: str) -> _InstallPlan:
        """Read a local bundle tarball and parse its embedded manifest.json."""
        try:
            with open(path, "rb") as f:
                bundle_bytes = f.read()
        except OSError as e:
            raise ValueError(f"Failed to read bundle file '{path}': {e}") from e

        try:
            with tarfile.open(fileobj=BytesIO(bundle_bytes), mode="r:gz") as tar:
                manifest_member = tar.getmember("manifest.json")
                extracted = tar.extractfile(manifest_member)
                if extracted is None:
                    raise ValueError(f"Cannot read manifest.json from '{path}'.")
                manifest = json.loads(extracted.read().decode("utf-8"))
        except KeyError:
            raise ValueError(
                f"Bundle '{path}' does not contain manifest.json at the root."
            ) from None
        except (tarfile.ReadError, tarfile.CompressionError) as e:
            raise ValueError(f"Bundle '{path}' is not a valid tar.gz: {e}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Bundle manifest.json is not valid JSON: {e}") from e

        try:
            return _InstallPlan(
                version=manifest["version"],
                license_hash=manifest["license_hash"],
                catalog=[
                    CatalogEntry.from_dict(catalog_dict)
                    for catalog_dict in manifest.get("catalog", [])
                ],
                bundle=bundle_bytes,
            )
        except (KeyError, TypeError) as e:
            raise ValueError(
                f"Bundle manifest.json is missing required field {e}."
            ) from e

    def _resolve_target_platforms(
        self,
        *,
        requested: List[Platform],
        plan: _InstallPlan,
        existing_metadata: Optional[InstalledMetadata],
        force: bool,
    ) -> Optional[List[Platform]]:
        """Return the final platform list, or None if nothing to install.

        Raises `PlatformVersionMismatchError` or `AlreadyInstalledError` when
        the user's request can't be satisfied without a force/explicit choice.
        """
        if existing_metadata is None:
            return requested
        if force:
            if existing_metadata.version == plan.version:
                return requested
            # Cross-version force: bring existing platforms along too.
            return list(dict.fromkeys([*requested, *existing_metadata.platforms]))
        return self._check_existing_install(requested, plan.version, existing_metadata)

    def _fetch_bundle(self, plan: _InstallPlan) -> bytes:
        """Return bundle bytes from the plan, downloading if URL-based.

        A presigned bundle URL carries its own signature; no CLI auth
        headers are attached to the request.
        """
        if plan.bundle is not None:
            return plan.bundle
        assert plan.bundle_url is not None  # enforced by _InstallPlan invariant
        try:
            response = requests.get(plan.bundle_url, timeout=60)
            response.raise_for_status()
            return response.content
        except Exception as e:
            raise ValueError(
                f"Failed to download skills bundle: {e}\n"
                "  Please try again. If the problem persists, contact support@anyscale.com."
            ) from e

    def _install_from_plan(
        self,
        plan: _InstallPlan,
        target_platforms: List[Platform],
        existing_metadata: Optional[InstalledMetadata],
    ) -> None:
        """Download (if needed), verify, and install the plan's bundle for targets."""
        self._logger.info(f"Installing Anyscale skills v{plan.version}...")
        bundle = self._fetch_bundle(plan)
        if plan.bundle_checksum is not None:
            self._verify_checksum(bundle, plan.bundle_checksum)
        self._install_platforms(
            bundle, plan, target_platforms, existing_metadata=existing_metadata,
        )
        self._warn_about_unsupported_skills(plan.catalog)

    def _warn_about_unsupported_skills(self, catalog: List[CatalogEntry]) -> None:
        """Log a warning for catalog entries whose platforms the CLI doesn't know."""
        known_platforms = set(self._platform_configs)
        skipped = [
            entry
            for entry in catalog
            if entry.platforms and not set(entry.platforms) & known_platforms
        ]
        if not skipped:
            return
        self._logger.info("")
        self._logger.info(
            f"  {len(skipped)} skill(s) require a newer anyscale CLI; "
            "upgrade to enable:"
        )
        for entry in skipped:
            self._logger.info(
                f"    /{entry.name} (requires: {', '.join(entry.platforms)})"
            )

    def _check_existing_install(
        self,
        requested: List[Platform],
        resolved_version: str,
        existing_metadata: InstalledMetadata,
    ) -> Optional[List[Platform]]:
        """Check for version conflicts with an existing install.

        Returns the (possibly updated) platforms list to proceed with,
        or None if the install should be aborted. Raises
        `AlreadyInstalledError` or `PlatformVersionMismatchError` when a
        conflict requires user guidance.
        """
        existing_version = existing_metadata.version
        already_installed = set(existing_metadata.platforms)
        requested_set = set(requested)

        if resolved_version != existing_version:
            new_platforms = requested_set - already_installed

            if new_platforms:
                raise PlatformVersionMismatchError(
                    existing_version=existing_version,
                    resolved_version=resolved_version,
                    already_installed=sorted(already_installed),
                    new_platforms=sorted(new_platforms),
                    all_platforms=sorted(already_installed | requested_set),
                )

            raise AlreadyInstalledError(
                existing_version=existing_version,
                resolved_version=resolved_version,
                already_installed=sorted(already_installed),
            )

        if requested_set.issubset(already_installed):
            return None

        return requested

    def _install_platforms(
        self,
        bundle: bytes,
        plan: _InstallPlan,
        platforms: List[Platform],
        existing_metadata: Optional[InstalledMetadata] = None,
    ) -> None:
        """Install bundle for each platform, saving metadata after each for crash safety."""
        if existing_metadata is not None:
            platforms_info: Dict[Platform, PlatformInstallInfo] = dict(
                existing_metadata.platforms
            )
        else:
            platforms_info = {}

        for platform in platforms:
            platform_config = self._platform_configs[platform]
            previous = platforms_info.get(platform)
            skills_files, hooks_files = self._install_for_platform(
                bundle, platform, previous,
            )
            platforms_info[platform] = PlatformInstallInfo(
                skills_dir=platform_config.skills_dir,
                hooks_dir=platform_config.hooks_dir,
                skills_files=skills_files,
                hooks_files=hooks_files,
            )
            self._save_metadata(
                InstalledMetadata(
                    version=plan.version,
                    license_hash=plan.license_hash,
                    platforms=platforms_info,
                    checksum=plan.bundle_checksum or "",
                    catalog=plan.catalog,
                    schema_version=InstalledMetadata.CURRENT_SCHEMA_VERSION,
                    installed_at=datetime.now(timezone.utc).isoformat(),
                )
            )
            total = len(skills_files) + len(hooks_files)
            self._logger.info(f"  [{platform}] {total} file(s) installed")

    def _install_for_platform(
        self,
        bundle: bytes,
        platform: Platform,
        previous: Optional[PlatformInstallInfo] = None,
    ) -> Tuple[List[str], List[str]]:
        """Extract and install skill + hooks files for a given platform."""
        if platform not in self._platform_configs:
            raise ValueError(
                f"Unsupported platform: {platform}. "
                f"Supported: {', '.join(self._platform_configs.keys())}"
            )

        platform_config = self._platform_configs[platform]
        skills_dir = os.path.expanduser(platform_config.skills_dir)
        hooks_dir = os.path.expanduser(platform_config.hooks_dir)
        hooks_config_name = platform_config.hooks_config
        hooks_config_path = os.path.join(hooks_dir, hooks_config_name)

        skills_files: List[str] = []
        hooks_files: List[str] = []
        written_files: List[str] = []
        hooks_backup: Optional[bytes] = None
        hooks_existed_before = False

        with tempfile.TemporaryDirectory() as tmpdir:
            self._extract_bundle(bundle, tmpdir)

            platform_source_dir = os.path.join(tmpdir, platform)
            if not os.path.isdir(platform_source_dir):
                raise ValueError(
                    f"Skills bundle does not contain files for platform '{platform}'."
                )

            self._pre_write_validate(skills_dir, hooks_dir, hooks_config_path)

            if os.path.exists(hooks_config_path):
                hooks_existed_before = True
                with open(hooks_config_path, "rb") as f:
                    hooks_backup = f.read()

            try:
                for root, _dirs, files in os.walk(platform_source_dir):
                    for filename in files:
                        source_path = os.path.join(root, filename)
                        rel_path = os.path.relpath(source_path, platform_source_dir)

                        if rel_path == hooks_config_name:
                            _merge_hooks_config(hooks_config_path, source_path)
                            hooks_files.append(rel_path)
                        elif rel_path.startswith(_SKILLS_PREFIX):
                            skills_rel = rel_path[len(_SKILLS_PREFIX) :]
                            dest_path = os.path.join(skills_dir, skills_rel)
                            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                            shutil.copy2(source_path, dest_path)
                            written_files.append(dest_path)
                            skills_files.append(skills_rel)
                        else:
                            dest_path = os.path.join(hooks_dir, rel_path)
                            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                            shutil.copy2(source_path, dest_path)
                            written_files.append(dest_path)
                            hooks_files.append(rel_path)
            except Exception as e:
                self._rollback_platform_install(
                    written_files,
                    hooks_config_path,
                    hooks_backup,
                    hooks_existed_before,
                )
                if isinstance(e, PermissionError):
                    raise ValueError(
                        f"Permission denied while installing skills for '{platform}': {e}.\n"
                        "  No changes were applied. Check write access to "
                        f"'{skills_dir}' and '{hooks_dir}' and retry."
                    ) from e
                raise

        if previous is not None:
            self._cleanup_orphaned_files(
                platform, previous, skills_files, hooks_files,
            )

        return skills_files, hooks_files

    def _pre_write_validate(
        self, skills_dir: str, hooks_dir: str, hooks_config_path: str,
    ) -> None:
        """Check both target dirs are writable and any existing hooks config is valid JSON."""
        for target_dir in (skills_dir, hooks_dir):
            if os.path.exists(target_dir):
                if not os.access(target_dir, os.W_OK):
                    raise ValueError(
                        f"Target directory '{target_dir}' is not writable.\n"
                        "  Check permissions and retry."
                    )
            else:
                try:
                    os.makedirs(target_dir, exist_ok=True)
                except OSError as e:
                    raise ValueError(
                        f"Cannot create target directory '{target_dir}': {e}"
                    ) from e

        if os.path.exists(hooks_config_path):
            try:
                with open(hooks_config_path) as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Existing hooks config '{hooks_config_path}' is not valid JSON: {e}.\n"
                    "  Fix or delete the file before retrying."
                ) from e
            except OSError as e:
                raise ValueError(
                    f"Cannot read hooks config '{hooks_config_path}': {e}"
                ) from e

    def _rollback_platform_install(
        self,
        written_files: List[str],
        hooks_config_path: str,
        hooks_backup: Optional[bytes],
        hooks_existed_before: bool,
    ) -> None:
        """Undo files written during a failed per-platform install."""
        for path in written_files:
            with contextlib.suppress(OSError):
                os.remove(path)

        if hooks_existed_before and hooks_backup is not None:
            with contextlib.suppress(OSError), open(hooks_config_path, "wb") as f:
                f.write(hooks_backup)
        elif not hooks_existed_before and os.path.exists(hooks_config_path):
            with contextlib.suppress(OSError):
                os.remove(hooks_config_path)

    def _extract_bundle(self, bundle: bytes, dest_dir: str) -> None:
        """Extract a tar.gz bundle to dest_dir, applying `_skills_filter` per member."""
        try:
            with tarfile.open(fileobj=BytesIO(bundle), mode="r:gz") as tar:
                for member in tar.getmembers():
                    tar.extract(_skills_filter(member, dest_dir), dest_dir)
        except (tarfile.ReadError, tarfile.CompressionError) as e:
            raise ValueError(
                f"Failed to extract skills bundle: {e}\n"
                "  The download may be corrupted. Please try again."
            ) from e

    def _cleanup_orphaned_files(
        self,
        platform: Platform,
        previous: PlatformInstallInfo,
        skills_files: List[str],
        hooks_files: List[str],
    ) -> None:
        """Remove files from the previous version that are no longer in the bundle."""
        platform_config = self._platform_configs[platform]
        skills_dir = os.path.expanduser(platform_config.skills_dir)
        hooks_dir = os.path.expanduser(platform_config.hooks_dir)
        hooks_config_name = platform_config.hooks_config

        skills_orphans = set(previous.skills_files) - set(skills_files)
        hooks_orphans = (
            set(previous.hooks_files) - set(hooks_files) - {hooks_config_name}
        )

        cleaned_any_skills = self._remove_orphans(platform, skills_dir, skills_orphans,)
        cleaned_any_hooks = self._remove_orphans(platform, hooks_dir, hooks_orphans,)

        if cleaned_any_skills:
            self._cleanup_empty_dirs(skills_dir)
        if cleaned_any_hooks:
            self._cleanup_empty_dirs(hooks_dir)

    def _remove_orphans(self, platform: Platform, base_dir: str, orphans: set,) -> bool:
        """Remove orphan files under base_dir. Returns True if any were removed."""
        removed_any = False
        for rel_path in orphans:
            abs_path = os.path.join(base_dir, rel_path)
            if os.path.exists(abs_path):
                try:
                    os.remove(abs_path)
                except PermissionError:
                    self._logger.info(
                        f"  [{platform}] warning: permission denied removing {rel_path}"
                    )
                    continue
                self._logger.info(f"  [{platform}] removed: {rel_path}")
                removed_any = True
        return removed_any

    def _load_metadata(self) -> Optional[InstalledMetadata]:
        """Load installation metadata, or None if not installed."""
        if not os.path.exists(self.metadata_path):
            return None

        def corrupted(reason: str) -> ValueError:
            return ValueError(
                f"Skills metadata is corrupted ({self.metadata_path}): {reason}\n"
                "  Delete the file manually and reinstall."
            )

        try:
            with open(self.metadata_path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise corrupted(str(e)) from e

        for key in ("version", "platforms"):
            if key not in data:
                raise corrupted(f"missing '{key}'")
        if not isinstance(data["platforms"], dict):
            raise corrupted("'platforms' must be a dict")

        try:
            data = _migrate_to_current(data)
            return InstalledMetadata.from_dict(
                {
                    **data,
                    "platforms": {
                        Platform(platform_key): PlatformInstallInfo.from_dict(
                            platform_info_dict
                        )
                        for platform_key, platform_info_dict in data[
                            "platforms"
                        ].items()
                    },
                    "catalog": [
                        CatalogEntry.from_dict(catalog_dict)
                        for catalog_dict in data.get("catalog", [])
                    ],
                }
            )
        except (ValueError, TypeError) as e:
            raise corrupted(str(e)) from e

    def _save_metadata(self, metadata: InstalledMetadata) -> None:
        """Save installation metadata."""
        _save_json(self.metadata_path, metadata.to_dict())

    def _cleanup_empty_dirs(self, base_dir: str) -> None:
        """Remove empty directories under base_dir, bottom-up."""
        for root, _dirs, _files in os.walk(base_dir, topdown=False):
            if root == base_dir:
                break
            if not os.listdir(root):
                with contextlib.suppress(OSError):
                    os.rmdir(root)
