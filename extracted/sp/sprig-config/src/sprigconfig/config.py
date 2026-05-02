# sprigconfig/config.py
"""
The Config class wraps deeply nested dictionaries into an immutable-ish
mapping structure with:

- dict-like API (keys, items, iteration, __contains__)
- dotted-key access via ["a.b.c"] and get("a.b.c")
- automatic recursive wrapping of nested dicts as Config instances
- safe .to_dict() conversion (deep copy, LazySecret redacted)
- .dump() to write YAML safely
"""

from collections.abc import Mapping
from pathlib import Path
import yaml

from .lazy_secret import LazySecret
from .exceptions import ConfigLoadError


class Config(Mapping):
    """
    Mapping wrapper around a dict, providing:

    - attribute-style nested access through Config[...] returning Config
    - dotted-key access: cfg["a.b.c"] and cfg.get("a.b.c")
    - safe serialization (.to_dict())
    - secure YAML dump (.dump(path, safe=True/False))

    Immutable-ish:
        underlying dict is private and should not be mutated directly.
        Users may mutate Config only through explicit methods if we add
        them in future versions (not supported currently).
    """

    def __init__(self, data):
        if not isinstance(data, dict):
            raise TypeError("Config must wrap a dict")

        # Deep wrap the root dict
        self._data = self._wrap(data)

    # ------------------------------------------------------------------
    # INTERNAL WRAPPING
    # ------------------------------------------------------------------
    def _wrap(self, obj):
        """Recursively wrap dictionaries as Config."""
        if isinstance(obj, Config):
            return obj
        if isinstance(obj, dict):
            return {k: self._wrap(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._wrap(v) for v in obj]
        return obj

    # ------------------------------------------------------------------
    # MAPPING INTERFACE WITH DOTTED-KEY LOOKUP
    # ------------------------------------------------------------------
    def __getitem__(self, key):
        """
        Support:
            cfg["a.b.c"]
            cfg["a"]["b"]["c"]
        Strict: raises KeyError if any part is missing.
        """
        if isinstance(key, str) and "." in key:
            parts = key.split(".")
            node = self._data

            for part in parts:
                if not isinstance(node, dict) or part not in node:
                    raise KeyError(key)
                node = node[part]

            # Wrap nested dicts as Config
            if isinstance(node, dict):
                return Config(node)
            return node

        # Non-dotted access
        value = self._data[key]
        if isinstance(value, dict):
            return Config(value)
        return value

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        """
        Both literal keys and dotted keys return True if resolvable.
        """
        try:
            self[key]
            return True
        except KeyError:
            return False

    # ------------------------------------------------------------------
    # DOTTED-KEY ACCESS VIA get()
    # ------------------------------------------------------------------
    def get(self, key, default=None):
        """
        cfg.get("a.b.c") resolves nested keys and returns default if missing.
        """
        if "." not in key:
            return self._resolve_leaf(key, default)

        parts = key.split(".")
        node = self._data

        for part in parts:
            if isinstance(node, dict):
                if part not in node:
                    return default
                node = node[part]
            else:
                return default

        if isinstance(node, dict):
            return Config(node)
        return node

    def _resolve_leaf(self, key, default):
        if key not in self._data:
            return default
        value = self._data[key]
        if isinstance(value, dict):
            return Config(value)
        return value

    # ------------------------------------------------------------------
    # SAFE TO_DICT
    # ------------------------------------------------------------------
    def to_dict(self, *, reveal_secrets=False):
        """
        Convert to a deep plain dict.

        reveal_secrets=False:
            LazySecret → "<LazySecret>"

        reveal_secrets=True:
            LazySecret → actual decrypted value or raise ConfigLoadError
        """
        return self._to_plain(self._data, reveal_secrets=reveal_secrets)

    def _to_plain(self, obj, *, reveal_secrets=False):
        if isinstance(obj, LazySecret):
            if reveal_secrets:
                try:
                    return obj.get()
                except Exception as e:
                    raise ConfigLoadError(
                        f"Failed to decrypt LazySecret during to_dict(): {e}"
                    )
            return "<LazySecret>"

        if isinstance(obj, Config):
            return obj.to_dict(reveal_secrets=reveal_secrets)

        if isinstance(obj, dict):
            return {k: self._to_plain(v, reveal_secrets=reveal_secrets) for k, v in obj.items()}

        if isinstance(obj, list):
            return [self._to_plain(v, reveal_secrets=reveal_secrets) for v in obj]

        return obj

    # ------------------------------------------------------------------
    # DUMP TO YAML
    # ------------------------------------------------------------------
    def dump(
        self,
        path: Path | None = None,
        *,
        safe: bool = True,
        pretty: bool = True,
        sprigconfig_first: bool = False,
    ) -> str:
        """
        Dump config to YAML and optionally return it as a string.

        Args:
            path: Optional filesystem path. If provided, YAML is written there.
                  If None, the YAML string is returned instead.
            safe: If True, LazySecret values are redacted. If False, secrets
                  are decrypted (if decryptable) or raise ConfigLoadError.
            pretty: If True, output human-friendly block-style YAML.
            sprigconfig_first: If True, reorder 'sprigconfig:' to appear first
                               in the YAML output (does not modify the internal
                               config structure).

        Returns:
            The YAML string (always returned, even if written to a file).
        """
        data = self.to_dict(reveal_secrets=not safe)

        if sprigconfig_first and "sprigconfig" in data:
            reordered = {"sprigconfig": data["sprigconfig"]}
            for key, value in data.items():
                if key != "sprigconfig":
                    reordered[key] = value
            data = reordered

        yaml_dump = yaml.safe_dump(
            data,
            sort_keys=False,
            default_flow_style=not pretty,
            indent=2,
            allow_unicode=True,
        )

        if path is not None:
            try:
                with open(path, "w") as f:
                    f.write(yaml_dump)
            except Exception as e:
                raise ConfigLoadError(f"Failed to write YAML dump to {path}: {e}")

        return yaml_dump

    # ------------------------------------------------------------------
    # REPRESENTATION
    # ------------------------------------------------------------------
    def __repr__(self):
        return f"Config({self._data!r})"
