"""Pose the credential for the Node ecosystem — npm, pnpm, Yarn and bun.

Configuration goes into the **user's** home, never the project: a repo that
declares no registry must still install private packages, so no environment
variable and no project file are involved.

Two files are needed because the ecosystem is split:

- ``~/.npmrc`` — read by npm, pnpm, Yarn 1 and bun: the scope mapping
  (``@<owner>:registry=``) plus the token attached to the host
  (``//<host>/api/v4/packages/npm/:_authToken=``).
- ``~/.yarnrc.yml`` — **Yarn 2+ ignores .npmrc** and reads its own home config:
  ``npmScopes.<owner>.npmRegistryServer`` for the mapping and ``npmRegistries``
  for that registry's token.

The token is always attached to the GitLab host and never posed as a global
setting, so no request to a public registry can carry it. Writes are surgical:
only the GitLab-registry keys are created or updated, and the rest of each file
— which may hold other registries — is left as it was.
"""

from pathlib import Path
from typing import Any

import yaml

from ..fs import atomic_write_private_text
from .consumer import ApplyResult, ConsumerState, RegistryConsumer
from .targets import RegistryTargets

_AUTH_SUFFIX = ":_authToken"


def npmrc_path() -> Path:
    return Path.home() / ".npmrc"


def yarnrc_path() -> Path:
    return Path.home() / ".yarnrc.yml"


def _scope_key(owner: str) -> str:
    return f"@{owner}:registry"


def _auth_key(targets: RegistryTargets) -> str:
    return f"{targets.npm_auth_key}{_AUTH_SUFFIX}"


def _npmrc_entries(token: str, targets: RegistryTargets) -> dict[str, str]:
    return {
        _scope_key(targets.owner): targets.npm_registry,
        _auth_key(targets): token,
    }


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (FileNotFoundError, OSError):
        return ""


def _line_key(line: str) -> str:
    return line.split("=", 1)[0].strip() if "=" in line else ""


def _upsert_ini(existing: str, entries: dict[str, str]) -> str:
    """Set each ``entries`` key in an ``.npmrc``, leaving every other line intact.

    An existing key is updated in place (so its position is preserved), any
    later duplicate of a managed key is dropped, and missing keys are appended.
    """
    written: set[str] = set()
    out: list[str] = []
    for line in existing.splitlines():
        key = _line_key(line)
        if key in entries:
            if key in written:
                continue
            written.add(key)
            out.append(f"{key}={entries[key]}")
        else:
            out.append(line)
    out.extend(f"{key}={value}" for key, value in entries.items() if key not in written)
    return "\n".join(out).strip("\n") + "\n"


def _drop_ini_keys(existing: str, keys: set[str]) -> str:
    kept = [line for line in existing.splitlines() if _line_key(line) not in keys]
    body = "\n".join(kept).strip("\n")
    return f"{body}\n" if body else ""


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    raw = _read_text(path)
    if not raw.strip():
        return {}
    try:
        loaded = yaml.safe_load(raw)
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _nested_mapping(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    return dict(value) if isinstance(value, dict) else {}


class NpmConsumer(RegistryConsumer):
    name = "node"

    def state(self, targets: RegistryTargets) -> ConsumerState:
        if not targets.owner:
            return ConsumerState(name=self.name, detail="no GitLab owner resolved — scope mapping unavailable")

        npmrc = _read_text(npmrc_path())
        npmrc_keys = {_line_key(line) for line in npmrc.splitlines()}
        npmrc_ok = _auth_key(targets) in npmrc_keys and _scope_key(targets.owner) in npmrc_keys

        yarnrc = _load_yaml_mapping(yarnrc_path())
        registries = _nested_mapping(yarnrc, "npmRegistries")
        scopes = _nested_mapping(yarnrc, "npmScopes")
        registry_entry = registries.get(targets.npm_auth_key)
        scope_entry = scopes.get(targets.owner)
        yarn_ok = (
            isinstance(registry_entry, dict)
            and bool(registry_entry.get("npmAuthToken"))
            and isinstance(scope_entry, dict)
            and bool(scope_entry.get("npmRegistryServer"))
        )

        locations = tuple(str(path) for path, ok in ((npmrc_path(), npmrc_ok), (yarnrc_path(), yarn_ok)) if ok)
        detail = "" if (npmrc_ok and yarn_ok) else "npm and Yarn 2+ each need their own file"
        return ConsumerState(
            name=self.name,
            configured=npmrc_ok and yarn_ok,
            locations=locations,
            detail=detail,
        )

    def apply(self, token: str, targets: RegistryTargets) -> ApplyResult:
        if not targets.owner:
            return ApplyResult(error="no GitLab owner resolved — cannot map the private npm scope")

        try:
            npm_changed = self._apply_npmrc(token, targets)
            yarn_changed = self._apply_yarnrc(token, targets)
        except OSError as exc:
            return ApplyResult(error=f"could not write the Node configuration: {exc}")

        return ApplyResult(
            changed=npm_changed or yarn_changed,
            locations=(str(npmrc_path()), str(yarnrc_path())),
        )

    def _apply_npmrc(self, token: str, targets: RegistryTargets) -> bool:
        path = npmrc_path()
        existing = _read_text(path)
        updated = _upsert_ini(existing, _npmrc_entries(token, targets))
        if updated == existing:
            return False
        atomic_write_private_text(path, updated)
        return True

    def _apply_yarnrc(self, token: str, targets: RegistryTargets) -> bool:
        path = yarnrc_path()
        existing = _read_text(path)
        data = _load_yaml_mapping(path)

        scopes = _nested_mapping(data, "npmScopes")
        scope_entry = dict(scopes.get(targets.owner) or {}) if isinstance(scopes.get(targets.owner), dict) else {}
        scope_entry["npmRegistryServer"] = targets.npm_registry
        scopes[targets.owner] = scope_entry
        data["npmScopes"] = scopes

        registries = _nested_mapping(data, "npmRegistries")
        registry_key = targets.npm_auth_key
        registry_entry = (
            dict(registries.get(registry_key) or {}) if isinstance(registries.get(registry_key), dict) else {}
        )
        registry_entry["npmAuthToken"] = token
        registries[registry_key] = registry_entry
        data["npmRegistries"] = registries

        updated = yaml.safe_dump(data, sort_keys=False, default_flow_style=False, allow_unicode=True)
        if updated == existing:
            return False
        atomic_write_private_text(path, updated)
        return True

    def remove(self, targets: RegistryTargets) -> tuple[str, ...]:
        cleaned: list[str] = []

        npm_path = npmrc_path()
        existing = _read_text(npm_path)
        managed = {_auth_key(targets)} | ({_scope_key(targets.owner)} if targets.owner else set())
        stripped = _drop_ini_keys(existing, managed)
        if stripped != existing:
            try:
                if stripped:
                    atomic_write_private_text(npm_path, stripped)
                else:
                    npm_path.unlink(missing_ok=True)
                cleaned.append(str(npm_path))
            except OSError:
                pass

        yarn_path = yarnrc_path()
        yarn_existing = _read_text(yarn_path)
        data = _load_yaml_mapping(yarn_path)
        touched = False

        registries = _nested_mapping(data, "npmRegistries")
        if registries.pop(targets.npm_auth_key, None) is not None:
            touched = True
            if registries:
                data["npmRegistries"] = registries
            else:
                data.pop("npmRegistries", None)

        scopes = _nested_mapping(data, "npmScopes")
        if targets.owner and scopes.pop(targets.owner, None) is not None:
            touched = True
            if scopes:
                data["npmScopes"] = scopes
            else:
                data.pop("npmScopes", None)

        if touched:
            try:
                if data:
                    atomic_write_private_text(
                        yarn_path,
                        yaml.safe_dump(data, sort_keys=False, default_flow_style=False, allow_unicode=True),
                    )
                elif yarn_existing:
                    yarn_path.unlink(missing_ok=True)
                cleaned.append(str(yarn_path))
            except OSError:
                pass

        return tuple(cleaned)


consumer = NpmConsumer()
