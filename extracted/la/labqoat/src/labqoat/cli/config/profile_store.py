"""Loading and saving non-secret CLI profiles."""

from __future__ import annotations

import os
import re
from pathlib import Path

from labqoat.cli.config.profile import Profile


class ProfileStore:
    """TOML-free profile storage using explicit line files."""

    _PROFILE_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z")

    def __init__(self, config_dir: Path | None = None) -> None:
        """Select the configuration directory."""
        if config_dir is None:
            config_dir = Path(os.environ.get("LABQOAT_CONFIG_DIR", str(Path.home() / ".config" / "labqoat")))
        self._config_dir = config_dir

    def profile_path(self, name: str) -> Path:
        """Return the file holding one profile."""
        if not self._PROFILE_NAME.fullmatch(name):
            msg = "profile name must contain 1-64 letters, digits, underscores, or hyphens"
            raise ValueError(msg)
        return self._config_dir / f"{name}.profile"

    def load(self, name: str) -> Profile:
        """Load a profile, falling back to the production endpoint."""
        path = self.profile_path(name)
        if not path.exists():
            return Profile(name=name, base_url=Profile.default_base_url(), username="")
        values = ProfileStore.read_values(path)
        return Profile(
            name=name,
            base_url=values.get("base_url", Profile.default_base_url()),
            username=values.get("username", ""),
            timeout_seconds=float(values.get("timeout_seconds", "30.0")),
            environment=values.get("environment", "default"),
        )

    def save(self, profile: Profile) -> None:
        """Persist non-secret profile settings."""
        path = self.profile_path(profile.name)
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            f"base_url={profile.base_url}",
            f"username={profile.username}",
            f"timeout_seconds={profile.timeout_seconds}",
            f"environment={profile.environment}",
        ]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    @staticmethod
    def read_values(path: Path) -> dict[str, str]:
        """Read key=value lines without executing them."""
        values: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            key, separator, value = line.partition("=")
            if separator and key.strip() and "\n" not in value:
                values[key.strip()] = value.strip()
        return values
