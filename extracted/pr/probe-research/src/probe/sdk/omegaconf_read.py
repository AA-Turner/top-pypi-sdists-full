"""Read an OmegaConf config without resolving what could reveal a secret.

Reading a ``DictConfig`` resolves its ``${...}`` interpolations. Before plan (d)
a DictConfig given to ``Run.log`` was sent as its ``repr()``, which shows the
unresolved text. Flattening READS it, so ``{"client": {"auth":
"${wandb.api_key}"}}`` sent the resolved API key under a name no rule redacts,
and ``${oc.env:SERVICE_KEY}`` sent the environment's value (#2009 review).

So an interpolation is kept as its unresolved text when it

* reads the environment (``oc.env`` / ``env``),
* names anything credential-shaped (``${wandb.api_key}``,
  ``${oc.select:db.password}``, ``Bearer ${auth_token}``), or
* resolves to a value that equals, or contains, one of the config's secrets:
  a value under a credential-shaped key, or one of the interpolations above.
  That catches a chain (``a: ${b}``, ``b: ${wandb.api_key}``) through a name
  that looks harmless, and an alias to a whole node (``alias:
  ${credentials}``, ``auth: ${alias}``): a node is checked leaf by leaf,
  resolved, and one that cannot be resolved keeps its text. A number is also
  checked written out (``password: "839201"`` read back by
  ``${oc.decode:...}``). A secret of ``_MIN_CONTAINED_SECRET`` characters or
  more is also looked for INSIDE a string (``pw=${alias}``); a shorter one
  only when it is the whole value, as ``lr=0.1`` must not turn to text because
  an ``${oc.env:LOCAL_RANK}`` somewhere read ``0``.

Everything else resolves as OmegaConf would. A value that cannot be resolved
(``???``, a broken reference) is kept as its text instead of raising. The
unresolved text is what was sent before, and the scrubber treats it as a
reference rather than a value.

Not covered: a custom resolver that fetches a secret under a harmless-looking
name (``${vault:db/pass}``) resolves like any other interpolation.

Stdlib-only. omegaconf is imported only for a value that is already one of its
objects, so ``import probe`` never loads it.
"""

from __future__ import annotations

import re
from typing import Any

from .redaction import is_sensitive_key

_ENV_RESOLVER = re.compile(r"\$\{\s*(?:oc\.env|env)\s*:")
_NAME = re.compile(r"[A-Za-z0-9_\-]+")
#: A secret shorter than this is not searched for inside other values, and a
#: number is not compared with it: an ``${oc.env:...}`` that read ``0`` or ``8``
#: would otherwise turn every ``lr=0.1`` and every ``${trainer.devices}`` into
#: text. Such a value still counts when it IS the whole value.
_MIN_CONTAINED_SECRET = 4


def is_omegaconf(value: Any) -> bool:
    module = getattr(type(value), "__module__", "") or ""
    return module == "omegaconf" or module.startswith("omegaconf.")


def reveals_secret(text: str) -> bool:
    """Whether resolving this interpolation text would read the environment
    or a credential-shaped name."""
    if "${" not in text:
        return False
    if _ENV_RESOLVER.search(text):
        return True
    return any(is_sensitive_key(name) for name in _NAME.findall(text))


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
    """Children of one config's nodes, read safely. Build one per call.

    The first read of a node collects its root config's secrets once:
    the values under credential-shaped keys and those of revealing
    interpolations. They stay in memory only, to check other values against."""

    def __init__(self) -> None:
        self._secrets_by_root: dict[int, tuple[set, list[str]]] = {}

    def items(self, cfg: Any) -> list[tuple[Any, Any]]:
        """``(key, value)`` for each child of a DictConfig (``(index, value)``
        for a ListConfig), resolved except as the module docstring says.
        Never raises for an unresolvable value; raises only when the node
        itself cannot be listed."""
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
    """Every value under a credential-shaped key, and every revealing
    interpolation's resolved value, anywhere under ``cfg``."""
    if depth > 32:
        return
    try:
        keys = _keys(cfg)
    except Exception:  # noqa: BLE001
        return
    raw: Any = None
    for key in keys:
        sensitive = isinstance(key, str) and is_sensitive_key(key)
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
        # `use_auth_token: true` is a switch, not a secret; and True == 1, so
        # remembering it would keep every `${...}` that resolves to 1 as text.
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
    """Whether a resolved value equals or contains a secret; see the module
    docstring."""
    if is_omegaconf(value):
        # `auth: ${alias}` with `alias: ${credentials}` resolves to the whole
        # credentials node, which flattening would then send leaf by leaf.
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
