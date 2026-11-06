from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx2

DEFAULT_BASE_URL = "https://api.trajectory.ai"


class AuthError(Exception):
  def __init__(self, code: str, message: str) -> None:
    super().__init__(message)
    self.code = code


@dataclass(frozen=True)
class Credential:
  base_url: str
  source: str
  api_key: str | None = field(default=None, repr=False)
  profile: str | None = None
  organization: dict[str, str] | None = None


class CredentialStore:
  def __init__(self, directory: Path | None = None) -> None:
    config_home = os.environ.get("TRAJECTORY_CONFIG_HOME")
    self.directory = directory or (
      Path(config_home)
      if config_home
      else Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))) / "trajectory"
    )

  @staticmethod
  def origin(base_url: str | httpx2.URL) -> str:
    url = httpx2.URL(base_url)
    if url.scheme not in {"https", "http"} or not url.host:
      raise AuthError("invalid_origin", "The API URL must be an HTTP(S) URL.")
    port = url.port or (443 if url.scheme == "https" else 80)
    host = f"[{url.host}]" if ":" in url.host else url.host
    return f"{url.scheme}://{host}:{port}"

  @staticmethod
  def validate_login_url(base_url: str) -> str:
    CredentialStore.origin(base_url)
    url = httpx2.URL(base_url)
    if url.username or url.password:
      raise AuthError("invalid_origin", "Login requires an API origin without credentials.")
    if url.query or url.fragment or url.path not in {"", "/"}:
      raise AuthError("invalid_origin", "Login requires an API origin without a path or query.")
    if url.scheme != "https" and url.host not in {"localhost", "127.0.0.1", "::1"}:
      raise AuthError("invalid_origin", "Login requires HTTPS, except for a local development API.")
    return str(url).rstrip("/")

  def metadata(self) -> dict[str, Any]:
    path = self.directory / "profiles.json"
    if not path.exists():
      return {"version": 1, "active": None, "profiles": {}}
    data = self._read_json(path)
    if data.get("version") != 1 or not isinstance(data.get("profiles"), dict):
      raise AuthError(
        "invalid_credentials", "Unsupported login profile file; restore a valid copy."
      )
    return data

  def get(self, name: str, base_url: str | None = None) -> Credential:
    metadata = self.metadata()
    profile = metadata["profiles"].get(name)
    if profile is None:
      raise AuthError("profile_not_found", f"No login profile named {name!r}; run tj login.")
    destination = base_url or profile["base_url"]
    if self.origin(destination) != self.origin(profile["base_url"]):
      raise AuthError(
        "profile_origin_mismatch", "The selected profile belongs to a different API origin."
      )
    secret = self._read_json(self._secret_path(name))
    if (
      secret.get("origin") != self.origin(destination)
      or secret.get("organization") != profile["organization"]
    ):
      raise AuthError(
        "invalid_credentials", "Profile and credential do not match; restore a valid copy."
      )
    key = secret.get("api_key")
    if not isinstance(key, str) or not key:
      raise AuthError("invalid_credentials", "The saved credential is empty; run tj login.")
    return Credential(destination, "profile", key, name, profile["organization"])

  def save(
    self, name: str, base_url: str, api_key: str, organization: dict[str, str], user_email: str
  ) -> None:
    if not name.strip() or len(name) > 128:
      raise AuthError("invalid_profile", "Profile names must contain 1–128 characters.")
    with self._lock():
      data = self.metadata()
      if name in data["profiles"]:
        raise AuthError(
          "profile_exists", "That profile already exists; log out or choose a new profile name."
        )
      self._write_json(
        self._secret_path(name),
        {"origin": self.origin(base_url), "organization": organization, "api_key": api_key},
      )
      data["profiles"][name] = {
        "base_url": base_url,
        "organization": organization,
        "user_email": user_email,
      }
      data["active"] = name
      self._write_json(self.directory / "profiles.json", data)

  def use(self, name: str) -> dict[str, Any]:
    with self._lock():
      data = self.metadata()
      if name not in data["profiles"]:
        raise AuthError("profile_not_found", f"No login profile named {name!r}.")
      data["active"] = name
      self._write_json(self.directory / "profiles.json", data)
      return {"profile": name, **data["profiles"][name]}

  def remove(self, name: str, expected_api_key: str | None = None) -> None:
    with self._lock():
      data = self.metadata()
      if name in data["profiles"] and expected_api_key is not None:
        if self.get(name).api_key != expected_api_key:
          raise AuthError(
            "profile_changed",
            "This profile changed during logout; its newer credential was retained.",
          )
      data["profiles"].pop(name, None)
      if data["active"] == name:
        data["active"] = None
      self._write_json(self.directory / "profiles.json", data)
      self._secret_path(name).unlink(missing_ok=True)

  @classmethod
  def resolve(
    cls,
    api_key: str | None = None,
    base_url: str | httpx2.URL | None = None,
    profile: str | None = None,
  ) -> Credential:
    destination = str(base_url or os.environ.get("TRAJECTORY_BASE_URL") or DEFAULT_BASE_URL)
    cls.origin(destination)
    if api_key is not None:
      return Credential(destination, "argument", api_key)
    if "TRAJECTORY_API_KEY" in os.environ:
      return Credential(destination, "environment", os.environ["TRAJECTORY_API_KEY"])
    store = cls()
    metadata = store.metadata()
    selected = profile or os.environ.get("TRAJECTORY_PROFILE") or metadata["active"]
    if not selected:
      return Credential(destination, "none")
    explicit_selection = profile is not None or bool(os.environ.get("TRAJECTORY_PROFILE"))
    selected_metadata = metadata["profiles"].get(selected)
    if selected_metadata is None:
      raise AuthError("profile_not_found", f"No login profile named {selected!r}.")
    if base_url is None and not os.environ.get("TRAJECTORY_BASE_URL"):
      destination = selected_metadata["base_url"]
    if (
      cls.origin(destination) != cls.origin(selected_metadata["base_url"])
      and not explicit_selection
    ):
      return Credential(destination, "none")
    return store.get(selected, destination)

  def _secret_path(self, name: str) -> Path:
    digest = hashlib.sha256(name.encode()).hexdigest()
    return self.directory / f"credential-{digest}.json"

  @staticmethod
  def _read_json(path: Path) -> dict[str, Any]:
    try:
      flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
      descriptor = os.open(path, flags)
      with os.fdopen(descriptor, "r", encoding="utf-8") as stream:
        mode = os.fstat(stream.fileno())
        if os.name == "posix" and (
          mode.st_uid != os.getuid() or stat.S_IMODE(mode.st_mode) & 0o077
        ):
          raise AuthError(
            "insecure_credentials",
            "Login files must be owned by you and readable only by you (chmod 600).",
          )
        data = json.load(stream)
    except (OSError, ValueError) as error:
      raise AuthError(
        "invalid_credentials",
        "Unable to read saved login; check the profile files and permissions.",
      ) from error
    if not isinstance(data, dict):
      raise AuthError("invalid_credentials", "Invalid login profile file.")
    return data

  def _write_json(self, path: Path, data: dict[str, Any]) -> None:
    descriptor, temporary = tempfile.mkstemp(dir=self.directory, prefix=".login-")
    try:
      with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        json.dump(data, stream)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
      os.replace(temporary, path)
    finally:
      Path(temporary).unlink(missing_ok=True)

  @contextmanager
  def _lock(self) -> Iterator[None]:
    self.directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    if self.directory.is_symlink():
      raise AuthError("insecure_credentials", "The login directory must not be a symbolic link.")
    if os.name == "posix":
      directory_stat = self.directory.stat()
      if directory_stat.st_uid != os.getuid() or stat.S_IMODE(directory_stat.st_mode) & 0o077:
        raise AuthError(
          "insecure_credentials", "The login directory must be owned by you with mode 700."
        )
    lock_path = self.directory / ".lock"
    deadline = time.monotonic() + 5
    while True:
      try:
        descriptor = os.open(lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        break
      except FileExistsError:
        if time.monotonic() >= deadline:
          raise AuthError(
            "credentials_busy",
            "Another login is updating profiles. If it stopped unexpectedly, remove the .lock file.",
          ) from None
        time.sleep(0.05)
    try:
      yield
    finally:
      os.close(descriptor)
      lock_path.unlink()
