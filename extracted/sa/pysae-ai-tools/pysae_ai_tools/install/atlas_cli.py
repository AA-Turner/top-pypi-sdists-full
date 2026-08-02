"""Install or update the MongoDB Atlas CLI.

The Atlas CLI is published by MongoDB as a single ``atlas`` binary. Releases
live on GitHub at ``mongodb/mongodb-atlas-cli`` under tags shaped like
``atlascli/v1.54.0`` (the repo also ships a sibling ``mongocli`` binary that
has its own tag stream). We pull the matching tar/zip from the release page
and drop ``atlas`` (or ``atlas.exe``) on the user's PATH.

Native package managers are skipped on purpose:

- The brew formula lives in the third-party ``mongodb/brew`` tap, which would
  force every macOS user to add the tap before install.
- Past experience with ``MongoDB.*`` winget packages (see ``mongo_tools.py``)
  shows silent no-op installs. The archive route gives predictable behaviour
  on every OS.

After the binary install succeeds, the ``dev`` and ``prod`` profiles are
written to ``atlas``'s config file via ``atlas config set`` using API keys
resolved through :mod:`pysae_ai_tools.env.resolve` (env → AWS Secrets
Manager via ``iam/<username>/<env>/atlas`` → MCP config). Other profiles in the
config are preserved — only ``pysae-dev`` and ``pysae-prod`` are upserted.
Missing keys are reported but never fail the install. Users select a context
at runtime with ``atlas --profile pysae-dev …`` (or ``atlas -P pysae-prod …``).
"""

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
import tomlkit
import typer

from .common import binary, github, platform
from .common.base import ArchiveBinaryTool, InstallReport, ToolState

# GitHub uses a per-product tag stream ``atlascli/v<version>`` to share the
# repo with ``mongocli``. ``releases/latest`` returns whichever stream was
# tagged last — so we instead list ``releases`` and pick the newest tag
# matching the ``atlascli/`` prefix.
RELEASES_API = "https://api.github.com/repos/mongodb/mongodb-atlas-cli/releases"
TAG_PREFIX = "atlascli/v"


# Pysae Atlas access materialised as Atlas CLI profiles. ``pysae-dev`` /
# ``pysae-prod`` are project-scoped (one Atlas project each); ``pysae-org``
# is organisation-scoped (one key across every project). Selection is by
# profile at runtime (``atlas -P pysae-dev`` / ``-P pysae-org`` …).
#
# The ``pysae-`` prefix avoids a regression in atlascli v1.54.0 where
# a profile literally named ``dev`` (case-insensitive) silently routes
# auth to a different — internal — MongoDB endpoint and returns 401 on
# every real API call, even though the keys are perfectly valid. Any
# other profile name with the same keys works. We picked the
# unambiguous ``pysae-<scope>`` form so the bug stays buried regardless
# of how atlas chooses to interpret short names in future versions.
@dataclass(frozen=True)
class AtlasProfile:
    name: str  # profile name written to atlascli/config.toml
    pub_var: str  # resolver var for the public API key
    priv_var: str  # resolver var for the private API key
    id_prop: str  # atlas config property: "project_id" or "org_id"
    id_var: str  # resolver var feeding ``id_prop``
    optional: bool = False  # additive profile — absent (no key) is not an error


PROFILES: tuple[AtlasProfile, ...] = (
    AtlasProfile(
        "pysae-dev",
        "MONGODB_ATLAS_PUBLIC_API_KEY_DEV",
        "MONGODB_ATLAS_PRIVATE_API_KEY_DEV",
        "project_id",
        "MONGODB_ATLAS_PROJECT_ID_DEV",
    ),
    AtlasProfile(
        "pysae-prod",
        "MONGODB_ATLAS_PUBLIC_API_KEY_PROD",
        "MONGODB_ATLAS_PRIVATE_API_KEY_PROD",
        "project_id",
        "MONGODB_ATLAS_PROJECT_ID_PROD",
    ),
    AtlasProfile(
        "pysae-org",
        "MONGODB_ATLAS_ORG_PUBLIC_API_KEY",
        "MONGODB_ATLAS_ORG_PRIVATE_API_KEY",
        "org_id",
        "MONGODB_ATLAS_ORG_ID",
        optional=True,
    ),
)


class AtlasCliTool(ArchiveBinaryTool):
    name = "atlas"
    binary_name = "atlas"
    cli_help = "Install/update the MongoDB Atlas CLI and authenticate dev/prod profiles"
    env_pre_configure = (
        "MONGODB_ATLAS_PUBLIC_API_KEY_DEV",
        "MONGODB_ATLAS_PRIVATE_API_KEY_DEV",
        "MONGODB_ATLAS_PUBLIC_API_KEY_PROD",
        "MONGODB_ATLAS_PRIVATE_API_KEY_PROD",
    )
    # Project ids are optional — written to the profile when resolved (lets
    # `atlas clusters list -P pysae-dev` work without --projectId) but their
    # absence never blocks the install, unlike the keys above. Org key + ids are
    # optional too — the org profile (pysae-org) is additive and skipped cleanly
    # when its key is absent.
    env_optional = (
        "MONGODB_ATLAS_PROJECT_ID_DEV",
        "MONGODB_ATLAS_PROJECT_ID_PROD",
        "MONGODB_ATLAS_ORG_PUBLIC_API_KEY",
        "MONGODB_ATLAS_ORG_PRIVATE_API_KEY",
        "MONGODB_ATLAS_ORG_ID",
    )
    env_help = {
        "MONGODB_ATLAS_PUBLIC_API_KEY_DEV": "AWS Secrets Manager (iam/<user>/dev/atlas mongodb-atlas-public-key)",
        "MONGODB_ATLAS_PRIVATE_API_KEY_DEV": "AWS Secrets Manager (iam/<user>/dev/atlas mongodb-atlas-private-key)",
        "MONGODB_ATLAS_PUBLIC_API_KEY_PROD": "AWS Secrets Manager (iam/<user>/prod/atlas mongodb-atlas-public-key)",
        "MONGODB_ATLAS_PRIVATE_API_KEY_PROD": "AWS Secrets Manager (iam/<user>/prod/atlas mongodb-atlas-private-key)",
        "MONGODB_ATLAS_PROJECT_ID_DEV": "AWS Secrets Manager (iam/<user>/dev/atlas mongodb-atlas-pysae-project-id)",
        "MONGODB_ATLAS_PROJECT_ID_PROD": "AWS Secrets Manager (iam/<user>/prod/atlas mongodb-atlas-pysae-project-id)",
        "MONGODB_ATLAS_ORG_PUBLIC_API_KEY": "AWS Secrets Manager (iam/<user>/atlas mongodb-atlas-org-public-key)",
        "MONGODB_ATLAS_ORG_PRIVATE_API_KEY": "AWS Secrets Manager (iam/<user>/atlas mongodb-atlas-org-private-key)",
        "MONGODB_ATLAS_ORG_ID": "AWS Secrets Manager (iam/<user>/atlas mongodb-atlas-org-id)",
    }

    def fetch_latest_version(self) -> str:
        r = httpx.get(
            RELEASES_API, timeout=10.0, follow_redirects=True, params={"per_page": 30}, headers=github.github_headers()
        )
        r.raise_for_status()
        data = r.json()
        if not isinstance(data, list):
            return ""
        for release in data:
            tag = release.get("tag_name", "") if isinstance(release, dict) else ""
            if isinstance(tag, str) and tag.startswith(TAG_PREFIX) and not release.get("prerelease"):
                return tag[len(TAG_PREFIX) :]
        return ""

    def archive_info(self, version: str, plat: platform.Platform) -> tuple[str, str | None]:
        ver = version.lstrip("v")
        arch = "arm64" if plat.arch.value == "arm64" else "x86_64"
        # Tag in URL must keep its ``/`` percent-encoded.
        tag = f"atlascli%2Fv{ver}"

        if plat.is_linux:
            asset = f"mongodb-atlas-cli_{ver}_linux_{arch}.tar.gz"
            member = "bin/atlas"
        elif plat.is_macos:
            asset = f"mongodb-atlas-cli_{ver}_macos_{arch}.zip"
            member = "bin/atlas"
        elif plat.is_windows:
            # MongoDB ships an .msi too, but the .zip drops the binary
            # straight into ~/.local/bin via the shared archive path —
            # no admin prompt, no PATH surgery.
            asset = f"mongodb-atlas-cli_{ver}_windows_{arch}.zip"
            member = "bin/atlas.exe"
        else:
            raise ValueError(f"unsupported OS: {plat.os}")

        url = f"https://github.com/mongodb/mongodb-atlas-cli/releases/download/{tag}/{asset}"
        return url, member

    # ------------------------------------------------------------------
    # Profile authentication (post-install)
    # ------------------------------------------------------------------

    @staticmethod
    def _config_path() -> Path:
        """Return the Atlas CLI's TOML config path for the current OS.

        Mirrors Go's ``os.UserConfigDir()`` semantics, which is what the
        atlas binary uses internally:

        - Linux: ``$XDG_CONFIG_HOME/atlascli/config.toml`` (default
          ``~/.config``)
        - macOS: ``~/Library/Application Support/atlascli/config.toml``
        - Windows: ``%AppData%\\atlascli\\config.toml``
        """
        if sys.platform == "darwin":
            base = Path.home() / "Library" / "Application Support"
        elif sys.platform == "win32":
            appdata = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
            base = Path(appdata)
        else:
            xdg = os.environ.get("XDG_CONFIG_HOME")
            base = Path(xdg) if xdg else Path.home() / ".config"
        return base / "atlascli" / "config.toml"

    def _upsert_profiles(self, profile_data: dict[str, dict[str, str]]) -> None:
        """Upsert ``profile_data`` (``{name: {prop: value}}``) into config.toml.

        Each inner dict carries whatever properties resolved this round —
        typically ``public_api_key`` / ``private_api_key`` (always) and
        ``project_id`` (when AWS Secrets Manager has it). Properties not
        present in the dict are left untouched, so partial rotations of a
        single property don't wipe the rest of the profile.

        Other profiles and the top-level ``version`` marker are preserved.
        Writes with restricted permissions — the file holds secrets.

        Why we write the TOML ourselves rather than calling ``atlas config
        set``: the binary's ``config set`` command reports "Updated
        property '<key>'" but does not persist anything to disk in
        ``atlascli v1.54.0`` (likely a regression — read it back and the
        keys are gone). Writing the TOML directly is what we know works:
        ``atlas auth whoami -P <profile>`` succeeds against a profile we
        seeded by hand.
        """
        path = self._config_path()
        path.parent.mkdir(parents=True, exist_ok=True)

        doc: tomlkit.TOMLDocument
        if path.exists():
            try:
                doc = tomlkit.parse(path.read_text(encoding="utf-8"))
            except tomlkit.exceptions.TOMLKitError:
                doc = tomlkit.document()
        else:
            doc = tomlkit.document()
        if "version" not in doc:
            doc["version"] = 2

        for profile, props in profile_data.items():
            section = doc.get(profile)
            if not isinstance(section, dict):
                section = tomlkit.table()
                doc[profile] = section
            for key, value in props.items():
                section[key] = value

        # 0600 — keys are secrets; mirror the argocd config approach.
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(tomlkit.dumps(doc))

    def _authenticate_profiles(self) -> dict[str, str]:
        """Upsert each Atlas profile with keys + scope id resolved from env / AWS Secrets.

        Keys are required (missing → profile skipped). The scope id
        (``project_id`` for dev/prod, ``org_id`` for the org profile) is
        a "nice to have": when resolved, it's written so that scoped
        commands (``atlas clusters list``, ``atlas projects list``, …)
        work without ``--projectId`` / ``--orgId``; when unavailable the
        profile is still written with just the keys.
        """
        from ..env.resolve import try_auto_resolve

        results: dict[str, str] = {}
        to_write: dict[str, dict[str, str]] = {}

        for profile in PROFILES:
            pub = os.environ.get(profile.pub_var) or try_auto_resolve(profile.pub_var) or ""
            priv = os.environ.get(profile.priv_var) or try_auto_resolve(profile.priv_var) or ""
            scope_id = os.environ.get(profile.id_var) or try_auto_resolve(profile.id_var) or ""
            if not pub or not priv:
                missing = [v for v, val in [(profile.pub_var, pub), (profile.priv_var, priv)] if not val]
                results[profile.name] = f"skipped — {', '.join(missing)} unavailable"
                continue
            props: dict[str, str] = {"public_api_key": pub, "private_api_key": priv}
            if scope_id:
                props[profile.id_prop] = scope_id
            to_write[profile.name] = props

        if to_write:
            try:
                self._upsert_profiles(to_write)
            except OSError as exc:
                for profile_name in to_write:
                    results[profile_name] = f"failed — {exc}"
                return results
            for profile_name in to_write:
                ok, err = self._profile_status(profile_name)
                results[profile_name] = "ok" if ok else f"failed — {err}"
        return results

    def _profile_status(self, profile: str) -> tuple[bool, str]:
        """Return ``(authenticated, error)`` for ``atlas --profile <name>``."""
        if not binary.which(self.binary_name):
            return False, "binary not installed"
        try:
            r = subprocess.run(
                [self.binary_name, "auth", "whoami", "--profile", profile],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return False, f"atlas auth whoami failed: {exc}"
        if r.returncode != 0:
            stderr = (r.stderr or r.stdout or "").strip().splitlines()
            return False, stderr[-1] if stderr else f"exit code {r.returncode}"
        return True, (r.stdout + r.stderr).strip()

    def do_install(self) -> InstallReport:
        # When the only reason we're being re-run is unauthenticated profiles
        # (``needs_reconfigure_profiles`` flag), skip the binary download —
        # re-pulling the tarball adds latency without changing anything.
        binary_current = False
        installed_version = ""
        if binary.which(self.binary_name):
            installed_version = binary.get_version(self.binary_name, version_arg=self.version_arg) or ""
            try:
                latest = self.fetch_latest_version().lstrip("v")
            except Exception:  # noqa: BLE001
                latest = ""
            if installed_version and (not latest or not binary.needs_update(installed_version, latest)):
                binary_current = True

        if binary_current:
            report = InstallReport(version=installed_version, method="already up-to-date")
        else:
            report = super().do_install()
            if report.error:
                return report

        auth = self._authenticate_profiles()
        if auth:
            report.extra["auth"] = auth
        return report

    # ------------------------------------------------------------------
    # State / display
    # ------------------------------------------------------------------

    def _profile_props(self, profile: str) -> dict[str, str]:
        """Return the property keys present in ``config.toml`` for ``profile``."""
        path = self._config_path()
        if not path.exists():
            return {}
        try:
            doc = tomlkit.parse(path.read_text(encoding="utf-8"))
        except tomlkit.exceptions.TOMLKitError:
            return {}
        section = doc.get(profile)
        if not isinstance(section, dict):
            return {}
        return {k: str(v) for k, v in section.items() if isinstance(v, str)}

    def get_state(self) -> ToolState:
        state = super().get_state()
        profiles: dict[str, dict[str, Any]] = {}
        any_unauthenticated = False
        any_incomplete = False
        for profile in PROFILES:
            if state.needs_install:
                profiles[profile.name] = {"ok": False, "error": "binary not installed", "message": ""}
                continue
            # An optional profile (org) never written to config.toml is
            # simply absent — surface it as informational, without flagging
            # auth failure or forcing a reconfigure.
            if profile.optional and not self._profile_props(profile.name):
                profiles[profile.name] = {
                    "ok": False,
                    "optional_absent": True,
                    "error": "",
                    "message": "not configured (optional)",
                }
                continue
            ok, msg = self._profile_status(profile.name)
            entry: dict[str, Any] = {"ok": ok, "error": "" if ok else msg, "message": msg if ok else ""}
            if ok and profile.id_prop not in self._profile_props(profile.name):
                # Auth works but the profile would force users to type
                # ``--projectId`` / ``--orgId`` for every scoped command —
                # flag so ``tools install`` re-runs and writes the id if
                # AWS Secrets Manager has it.
                entry["missing_id"] = True
                any_incomplete = True
            profiles[profile.name] = entry
            if not ok:
                any_unauthenticated = True
        state.extra["profiles"] = profiles
        if not state.needs_install:
            # ``auth_ok`` drives the ⚠ icon in ``tools status``;
            # ``needs_reconfigure`` makes ``tools install`` re-run the auth step.
            state.extra["auth_ok"] = not any_unauthenticated
            if any_unauthenticated:
                state.extra["auth_message"] = "one or more Atlas profiles need authentication"
                state.extra["needs_reconfigure_profiles"] = True
                state.needs_reconfigure = True
            elif any_incomplete:
                state.extra["needs_reconfigure_profiles"] = True
                state.needs_reconfigure = True
        return state

    def extract_identity(self, state: dict[str, Any]) -> list[tuple[str, str | None]]:
        lines: list[tuple[str, str | None]] = []
        profiles = state.get("profiles", {})
        for name, data in profiles.items():
            if not isinstance(data, dict):
                continue
            if data.get("optional_absent"):
                lines.append((f"– {name} — {data.get('message', 'not configured')}", typer.colors.YELLOW))
                continue
            ok = bool(data.get("ok"))
            icon = "✓" if ok else "✗"
            if ok:
                msg = str(data.get("message", ""))
                email = re.search(r"logged in as ([^\s.]+)", msg, re.IGNORECASE)
                api = re.search(r"API Key:\s*(\S+)", msg)
                identity = email.group(1) if email else (f"API key {api.group(1)}" if api else "")
                suffix = f" — {identity}" if identity else ""
            else:
                err = str(data.get("error", "")).strip()
                suffix = f" — {err}" if err else ""
            lines.append((f"{icon} {name}{suffix}", typer.colors.GREEN if ok else typer.colors.RED))
        return lines


tool = AtlasCliTool()
