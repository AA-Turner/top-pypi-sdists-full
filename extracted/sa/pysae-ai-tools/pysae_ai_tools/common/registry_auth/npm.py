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
  for that registry's token. That scope entry also carries
  ``npmMinimalAgeGate: 0``: Yarn's cooldown refuses packages published less than
  N minutes ago, which is aimed at the public registry but would equally block a
  private package built minutes earlier by our own CI. The gate has to go
  **inside the scope entry**: a scope declared in ``npmScopes`` does not inherit
  the root value, it keeps a hardcoded 1440-minute default until set explicitly
  (yarnpkg/berry#7192), so a root ``npmMinimalAgeGate: 0`` leaves our packages
  quarantined. Written next to ``npmRegistryServer``, matching what the
  ``registry-auth.yml`` CI template already does.

The token is always attached to the GitLab host and never posed as a global
setting, so no request to a public registry can carry it.

Both files belong to the user, so writes are surgical: only our own keys are
created or updated and everything else is left as it was — the ``.npmrc`` is
edited line by line, and the ``.yarnrc.yml`` through a round-trip parser, so
comments, key order and quoting style all survive. A ``.yarnrc.yml`` we cannot
parse is never rewritten: the apply refuses (before touching the ``.npmrc``, so
nothing is left half-configured) and says so, rather than replacing a file whose
contents it doesn't understand.
"""

import io
from collections.abc import Mapping, MutableMapping
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML, YAMLError
from ruamel.yaml.comments import CommentedMap

from ..fs import atomic_write_private_text
from .consumer import ApplyResult, ConsumerState, RegistryConsumer
from .targets import RegistryTargets

_AUTH_SUFFIX = ":_authToken"

# Yarn's publish cooldown, in minutes, set inside the scope entry (a declared scope
# ignores the root value — see the module docstring). Zero disables it.
_MINIMAL_AGE_GATE_KEY = "npmMinimalAgeGate"
_MINIMAL_AGE_GATE = 0


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


def _round_trip() -> YAML:
    """A round-trip parser: what it loads and dumps back keeps its comments and layout."""
    parser = YAML()
    parser.preserve_quotes = True
    return parser


def _load_yarnrc(path: Path) -> CommentedMap | None:
    """Load ``~/.yarnrc.yml`` for editing, or ``None`` when it exists but can't be read.

    A missing or blank file is a fresh mapping. Anything we fail to parse — or that
    isn't a mapping at all — returns ``None`` so the caller refuses to write rather
    than replacing a file whose contents it doesn't understand.
    """
    raw = _read_text(path)
    if not raw.strip():
        return CommentedMap()
    try:
        loaded = _round_trip().load(raw)
    except YAMLError:
        return None
    if loaded is None:
        return CommentedMap()
    return loaded if isinstance(loaded, CommentedMap) else None


def _dump_yarnrc(data: CommentedMap) -> str:
    buffer = io.StringIO()
    _round_trip().dump(data, buffer)
    return buffer.getvalue()


def _nested_mapping(data: Mapping[str, Any], key: str) -> Any:
    """The mapping under ``key``, edited in place so its comments survive."""
    value = data.get(key)
    return value if isinstance(value, MutableMapping) else CommentedMap()


class NpmConsumer(RegistryConsumer):
    name = "node"

    def state(self, targets: RegistryTargets) -> ConsumerState:
        if not targets.owner:
            return ConsumerState(name=self.name, detail="no GitLab owner resolved — scope mapping unavailable")

        npmrc = _read_text(npmrc_path())
        npmrc_keys = {_line_key(line) for line in npmrc.splitlines()}
        npmrc_ok = _auth_key(targets) in npmrc_keys and _scope_key(targets.owner) in npmrc_keys

        yarnrc = _load_yarnrc(yarnrc_path()) or CommentedMap()
        registries = _nested_mapping(yarnrc, "npmRegistries")
        scopes = _nested_mapping(yarnrc, "npmScopes")
        registry_entry = registries.get(targets.npm_auth_key)
        scope_entry = scopes.get(targets.owner)
        yarn_ok = (
            isinstance(registry_entry, dict)
            and bool(registry_entry.get("npmAuthToken"))
            and isinstance(scope_entry, dict)
            and bool(scope_entry.get("npmRegistryServer"))
            and scope_entry.get(_MINIMAL_AGE_GATE_KEY) == _MINIMAL_AGE_GATE
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

        # Read before writing anything: a yarnrc we can't parse must stop the whole
        # apply, not leave the npmrc half-configured behind us.
        yarnrc = _load_yarnrc(yarnrc_path())
        if yarnrc is None:
            return ApplyResult(
                error=f"{yarnrc_path()} is not valid YAML — refusing to overwrite it; fix or move it, then retry"
            )

        try:
            npm_changed = self._apply_npmrc(token, targets)
            yarn_changed = self._apply_yarnrc(yarnrc, token, targets)
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

    def _apply_yarnrc(self, data: CommentedMap, token: str, targets: RegistryTargets) -> bool:
        path = yarnrc_path()
        existing = _read_text(path)

        scopes = _nested_mapping(data, "npmScopes")
        scope_entry = _nested_mapping(scopes, targets.owner)
        scope_entry["npmRegistryServer"] = targets.npm_registry
        scope_entry[_MINIMAL_AGE_GATE_KEY] = _MINIMAL_AGE_GATE
        scopes[targets.owner] = scope_entry
        data["npmScopes"] = scopes

        # Earlier versions wrote the gate at the root, which our scope never picks up.
        # Drop that key so the home ends up with one gate, in the only place that works
        # — but only when it holds the value we used to write, never a cooldown the
        # user chose for everything else.
        if data.get(_MINIMAL_AGE_GATE_KEY) == _MINIMAL_AGE_GATE:
            data.pop(_MINIMAL_AGE_GATE_KEY)

        registries = _nested_mapping(data, "npmRegistries")
        registry_entry = _nested_mapping(registries, targets.npm_auth_key)
        registry_entry["npmAuthToken"] = token
        registries[targets.npm_auth_key] = registry_entry
        data["npmRegistries"] = registries

        updated = _dump_yarnrc(data)
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
        data = _load_yarnrc(yarn_path)
        if data is None:
            # Same rule as apply(): a file we can't parse is left alone.
            return tuple(cleaned)
        touched = False

        registries = _nested_mapping(data, "npmRegistries")
        if registries.pop(targets.npm_auth_key, None) is not None:
            touched = True
            if registries:
                data["npmRegistries"] = registries
            else:
                data.pop("npmRegistries", None)

        scopes = _nested_mapping(data, "npmScopes")
        scope_entry = scopes.get(targets.owner) if targets.owner else None
        if isinstance(scope_entry, MutableMapping):
            # Key by key rather than dropping the whole scope entry: anything the user
            # added next to our two keys is theirs and stays.
            if scope_entry.pop("npmRegistryServer", None) is not None:
                touched = True
            # Only drop the gate when we are the ones who set it to zero — a user who
            # picked their own cooldown keeps it.
            if scope_entry.get(_MINIMAL_AGE_GATE_KEY) == _MINIMAL_AGE_GATE:
                scope_entry.pop(_MINIMAL_AGE_GATE_KEY)
                touched = True
            # `scopes` is the mapping from the file, edited in place — an emptied scope
            # entry leaves no trace behind, and neither does an emptied `npmScopes`.
            if not scope_entry:
                scopes.pop(targets.owner)
            if not scopes:
                data.pop("npmScopes", None)

        # A root gate left by a version that wrote it there — same guard, same reason.
        if data.get(_MINIMAL_AGE_GATE_KEY) == _MINIMAL_AGE_GATE:
            data.pop(_MINIMAL_AGE_GATE_KEY)
            touched = True

        if touched:
            try:
                if data:
                    atomic_write_private_text(yarn_path, _dump_yarnrc(data))
                elif yarn_existing:
                    yarn_path.unlink(missing_ok=True)
                cleaned.append(str(yarn_path))
            except OSError:
                pass

        return tuple(cleaned)


consumer = NpmConsumer()
