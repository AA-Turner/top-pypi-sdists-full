"""Read an OmegaConf config without resolving what could reveal a secret (#2009).

Resolving ``${wandb.api_key}`` or ``${oc.env:KEY}`` would send the secret under a
name no rule redacts. An interpolation stays as its unresolved text when it

* reads the environment (``oc.env`` / ``env``),
* names anything credential-shaped (``${wandb.api_key}``, ``Bearer ${auth_token}``), or
* resolves to a value equal to, or containing, a secret of the config (a value
  under a credential-shaped key, or an interpolation above). That catches chains
  (``a: ${b}``, ``b: ${wandb.api_key}``) and aliases to a whole node (checked
  leaf by leaf; an unresolvable node keeps its text). A number is also checked
  written out (``password: "839201"``). A secret of ``_MIN_CONTAINED_SECRET``
  chars or more is also searched INSIDE strings (``pw=${alias}``); a shorter one
  only as the whole value, so ``lr=0.1`` stays a number.

Everything else resolves as OmegaConf would; an unresolvable value (``???``, a
broken reference) keeps its text instead of raising.

Not covered: a custom resolver that fetches a secret under a harmless name
(``${vault:db/pass}``).

Stdlib-only; omegaconf is imported only for values that already are its objects.
"""

from __future__ import annotations

import re
from typing import Any

# scanning disabled: from .redaction import is_sensitive_key

_ENV_RESOLVER = re.compile(r"\$\{\s*(?:oc\.env|env)\s*:")
_NAME = re.compile(r"[A-Za-z0-9_\-]+")
#: Shorter secrets are only matched as a whole value: an ``${oc.env:...}`` that
#: read ``0`` or ``8`` would otherwise turn every ``lr=0.1`` into text.
_MIN_CONTAINED_SECRET = 4


def is_omegaconf(value: Any) -> bool:
    module = getattr(type(value), "__module__", "") or ""
    return module == "omegaconf" or module.startswith("omegaconf.")


def reveals_secret(text: str) -> bool:
    """Whether resolving this text would read the environment or a credential-shaped name."""
    if "${" not in text:
        return False
    if _ENV_RESOLVER.search(text):
        return True
    # scanning disabled: return any(is_sensitive_key(name) for name in _NAME.findall(text))
    return False


def _keys(cfg: Any) -> list:
    return list(cfg.keys()) if hasattr(cfg, "keys") else list(range(len(cfg)))


def _raw(cfg: Any) -> Any:
    from omegaconf import OmegaConf  # noqa: PLC0415 -- the caller already imported it

    try:
        return OmegaConf.to_container(cfg, resolve=False)
    except Exception:  # noqa: BLE001
        return {} if hasattr(cfg, "keys") else []


def _is_interpolation(cfg: Any, key: Any) -> bool:
    from omegaconf import OmegaConf  # noqa: PLC0415

    try:
        return bool(OmegaConf.is_interpolation(cfg, key))
    except Exception:  # noqa: BLE001
        return False


def _root(cfg: Any) -> Any:
    try:
        return cfg._get_root()  # stable across omegaconf 2.x; no public accessor
    except Exception:  # noqa: BLE001
        return cfg


class Reader:
    """Reads a config's children safely. Build one per call.

    Collects the root's secrets once (in memory only) to check other values against."""

    def __init__(self) -> None:
        self._secrets_by_root: dict[int, tuple[set, list[str]]] = {}

    def items(self, cfg: Any) -> list[tuple[Any, Any]]:
        """``(key, value)`` per child (``(index, value)`` for a ListConfig), resolved
        except as the module docstring says. Raises only if the node cannot be listed."""
        keys = _keys(cfg)
        scalars, strings = self._secrets(cfg)
        raw: Any = None
        out: list[tuple[Any, Any]] = []
        for key in keys:
            if _is_interpolation(cfg, key):
                raw = _raw(cfg) if raw is None else raw
                text = _pick(raw, key)
                if not isinstance(text, str) or reveals_secret(text):
                    out.append((key, text))
                    continue
                try:
                    value = cfg[key]
                except Exception:  # noqa: BLE001
                    out.append((key, text))
                    continue
                out.append((key, text if _holds_secret(value, scalars, strings) else value))
                continue
            try:
                out.append((key, cfg[key]))
            except Exception:  # noqa: BLE001 -- `???`: keep the text
                raw = _raw(cfg) if raw is None else raw
                out.append((key, _pick(raw, key)))
        return out

    def _secrets(self, cfg: Any) -> tuple[set, list[str]]:
        root = _root(cfg)
        cached = self._secrets_by_root.get(id(root))
        if cached is None:
            scalars: set = set()
            strings: list[str] = []
            _collect(root, scalars, strings, depth=0)
            cached = (scalars, strings)
            self._secrets_by_root[id(root)] = cached
        return cached


def _pick(raw: Any, key: Any) -> Any:
    try:
        return raw[key]
    except Exception:  # noqa: BLE001
        return "???"


def _collect(cfg: Any, scalars: set, strings: list[str], *, depth: int) -> None:
    """Gather values under credential-shaped keys and revealing interpolations."""
    if depth > 32:
        return
    try:
        keys = _keys(cfg)
    except Exception:  # noqa: BLE001
        return
    raw: Any = None
    for key in keys:
        # scanning disabled: sensitive = isinstance(key, str) and is_sensitive_key(key)
        sensitive = False
        revealing = False
        if _is_interpolation(cfg, key):
            raw = _raw(cfg) if raw is None else raw
            text = _pick(raw, key)
            revealing = isinstance(text, str) and reveals_secret(text)
        try:
            value = cfg[key]
        except Exception:  # noqa: BLE001
            continue
        if is_omegaconf(value) and hasattr(value, "__len__") and not isinstance(value, str):
            if not sensitive:
                _collect(value, scalars, strings, depth=depth + 1)
                continue
        if sensitive or revealing:
            _remember(value, scalars, strings)


def _remember(value: Any, scalars: set, strings: list[str]) -> None:
    if isinstance(value, str):
        if value:
            strings.append(value)
        return
    if isinstance(value, bool):
        # A switch, not a secret; and True == 1 would keep every `${...}` = 1 as text.
        return
    if isinstance(value, (int, float)):
        scalars.add(value)
        strings.append(str(value))  # `pw=${alias}` with `password: 839201`
        return
    # A whole node under a secret name: remember what is inside it.
    try:
        from omegaconf import OmegaConf  # noqa: PLC0415

        inner = OmegaConf.to_container(value, resolve=True)
    except Exception:  # noqa: BLE001
        return
    for leaf in _leaves(inner):
        _remember(leaf, scalars, strings)


def _leaves(value: Any):
    if isinstance(value, dict):
        for child in value.values():
            yield from _leaves(child)
    elif isinstance(value, list):
        for child in value:
            yield from _leaves(child)
    else:
        yield value


def _holds_secret(value: Any, scalars: set, strings: list[str]) -> bool:
    """Whether a resolved value equals or contains a secret."""
    if is_omegaconf(value):
        # `auth: ${alias}` can resolve to a whole node, later sent leaf by leaf.
        try:
            from omegaconf import OmegaConf  # noqa: PLC0415

            inner = OmegaConf.to_container(value, resolve=True)
        except Exception:  # noqa: BLE001 -- cannot tell what is inside: keep the text
            return True
        return any(_holds_secret(leaf, scalars, strings) for leaf in _leaves(inner))
    if isinstance(value, str):
        return any(
            secret == value or (len(secret) >= _MIN_CONTAINED_SECRET and secret in value)
            for secret in strings
        )
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    if value in scalars:
        return True
    written = {str(value)}
    if isinstance(value, float) and value.is_integer():
        written.add(str(int(value)))
    return any(len(secret) >= _MIN_CONTAINED_SECRET and secret in written for secret in strings)
