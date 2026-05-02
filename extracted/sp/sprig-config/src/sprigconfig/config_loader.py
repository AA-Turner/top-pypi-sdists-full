"""
ConfigLoader with full import-trace support.

Responsibilities:
- Load application.<ext> (format-driven, extension-resolved)
- Load application-<profile>.<ext> overlay
- Expand ${ENV} and ${ENV:default}
- Perform deep merges
- Process recursive literal imports
- Detect circular imports
- Wrap ENC(...) values as LazySecret
- Inject metadata:
      sprigconfig._meta.profile
      sprigconfig._meta.sources
      sprigconfig._meta.import_trace
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

from .config import Config
from .lazy_secret import LazySecret
from .exceptions import ConfigLoadError
from .deepmerge import deep_merge
from .parsers import YamlParser, JsonParser, TomlParser

# ======================================================================
# CONSTANTS
# ======================================================================

ENV_PATTERN = re.compile(r"\$\{([^}:]+)(?::([^}]*))?\}")

SUPPORTED_FORMATS = {"yaml", "json", "toml"}

FORMAT_ALIASES = {
    "yml": "yaml",
}

FORMAT_EXTENSIONS = {
    "yaml": ("yaml", "yml"),
    "json": ("json",),
    "toml": ("toml",),
}

PARSERS = {
    "yaml": YamlParser(),
    "json": JsonParser(),
    "toml": TomlParser(),
}

# ======================================================================
# CONFIG LOADER
# ======================================================================

class ConfigLoader:
    """
    Loads config files from a directory with support for:
      - application.<ext> (base)
      - application-<profile>.<ext> (overlay)
      - recursive literal imports (format inheritance)
      - circular detection
      - LazySecret wrapping
      - metadata injection (profile, sources, import_trace)
    """

    # ------------------------------------------------------------------
    # FORMAT NORMALIZATION
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_format(config_format: str) -> str:
        normalized = FORMAT_ALIASES.get(config_format.lower(), config_format.lower())
        if normalized not in SUPPORTED_FORMATS:
            raise ConfigLoadError(f"Unsupported config format: {config_format}")
        return normalized

    # ------------------------------------------------------------------
    # INIT
    # ------------------------------------------------------------------

    def __init__(
        self,
        config_dir: Path,
        profile: str,
        *,
        config_format: Optional[str] = None,
    ):
        if config_dir is None:
            env_dir = os.getenv("APP_CONFIG_DIR")
            if not env_dir:
                raise ConfigLoadError(
                    "No config_dir provided and APP_CONFIG_DIR not set"
                )
            config_dir = Path(env_dir)

        self.config_dir = Path(config_dir)
        self.profile = profile

        raw_format = (
            config_format
            or os.getenv("SPRIGCONFIG_FORMAT")
            or "yaml"
        ).lstrip(".")

        self.format = self._normalize_format(raw_format)
        self.parser = PARSERS[self.format]

        # Import + merge tracking
        self._merge_trace: List[str] = []
        self._import_trace: List[dict] = []
        self._seen_imports: set[str] = set()
        self._order = 0

    # ==================================================================
    # PUBLIC API
    # ==================================================================

    def load(self) -> Config:
        # --------------------------------------------------
        # 1. Load base config
        # --------------------------------------------------
        base_file = self._resolve_root_file("application")
        base_data = self._load_file(base_file)

        root_path = str(base_file.resolve())
        self._record_import(
            file=root_path,
            imported_by=None,
            import_key=None,
            depth=0,
        )

        suppress = base_data.get("suppress_config_merge_warnings", False)

        self._apply_imports_recursive(
            base_data,
            parent_file=root_path,
            depth=0,
            suppress=suppress,
        )

        # --------------------------------------------------
        # 2. Load profile overlay
        # --------------------------------------------------
        profile_data = {}
        profile_file = self._resolve_root_file(f"application-{self.profile}")

        if profile_file.exists():
            profile_data = self._load_file(profile_file)

            profile_path = str(profile_file.resolve())
            self._record_import(
                file=profile_path,
                imported_by=root_path,
                import_key=profile_file.name,
                depth=1,
            )

            suppress = suppress or profile_data.get(
                "suppress_config_merge_warnings", False
            )

            self._apply_imports_recursive(
                profile_data,
                parent_file=profile_path,
                depth=1,
                suppress=suppress,
            )

        # --------------------------------------------------
        # 3. Merge
        # --------------------------------------------------
        merged = deep_merge(base_data, profile_data, suppress=suppress)

        merged.setdefault("app", {})["profile"] = self.profile

        self._inject_metadata(merged)
        self._inject_secrets(merged)

        return Config(merged)

    # ==================================================================
    # FILE RESOLUTION
    # ==================================================================

    def _resolve_root_file(self, stem: str) -> Path:
        """
        Resolve root config files using format-specific extension aliases.
        """
        for ext in FORMAT_EXTENSIONS[self.format]:
            candidate = self.config_dir / f"{stem}.{ext}"
            if candidate.exists():
                return candidate

        # Default canonical path (for error reporting)
        return self.config_dir / f"{stem}.{self.format}"

    def _resolve_import(self, import_key: str) -> Path:
        """
        Resolve import paths.

        Imports inherit format and never specify extensions.
        If the canonical extension does not exist on disk,
        try format-specific alias extensions (e.g. .yml for yaml).
        """
        import_path = Path(import_key)

        candidates: list[Path] = []

        if "." in import_path.name:
            # Explicit extension provided (rare, but allow it)
            candidates.append(self.config_dir / import_key)
        else:
            # No extension: try canonical first, then aliases
            for ext in FORMAT_EXTENSIONS[self.format]:
                candidates.append(self.config_dir / f"{import_key}.{ext}")

        base = self.config_dir.resolve()

        for candidate in candidates:
            resolved = candidate.resolve()

            # Path traversal protection
            try:
                resolved.relative_to(base)
            except ValueError:
                raise ConfigLoadError(
                    f"Path traversal detected: import '{import_key}' escapes config directory"
                )

            if resolved.exists():
                return resolved

        # If we get here, nothing matched
        tried = ", ".join(str(p.name) for p in candidates)
        raise ConfigLoadError(
            f"Import '{import_key}' not found. Tried: {tried}"
        )


    # ==================================================================
    # FILE LOADING
    # ==================================================================

    def _load_file(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}

        resolved = str(path.resolve())
        self._merge_trace.append(resolved)

        try:
            text = path.read_text(encoding="utf-8-sig")
            expanded = self._expand_env(text)
            data = self.parser.parse(expanded)
            return data or {}
        except Exception as e:
            raise ConfigLoadError(f"Invalid {self.format.upper()} in {path}: {e}") from e

    def _expand_env(self, text: str) -> str:
        def replacer(match):
            var, default = match.groups()
            return os.getenv(var, default if default is not None else match.group(0))

        return ENV_PATTERN.sub(replacer, text)

    # ==================================================================
    # IMPORT PROCESSING
    # ==================================================================

    def _record_import(
        self,
        *,
        file: str,
        imported_by: Optional[str],
        import_key: Optional[str],
        depth: int,
    ):
        self._import_trace.append(
            {
                "file": file,
                "imported_by": imported_by,
                "import_key": import_key,
                "depth": depth,
                "order": self._order,
            }
        )
        self._order += 1

    def _apply_imports_recursive(
        self,
        node: Dict[str, Any],
        *,
        parent_file: str,
        depth: int,
        suppress: bool,
        import_chain: Optional[List[str]] = None,
    ):
        if not isinstance(node, dict):
            return

        # Initialize import chain if not provided
        if import_chain is None:
            import_chain = [parent_file]

        if "imports" in node:
            imports = node.get("imports", [])
            if not isinstance(imports, list):
                raise ConfigLoadError("imports must be a list")

            for import_key in imports:
                import_file = self._resolve_import(import_key)
                import_path = str(import_file)

                if import_path in self._seen_imports:
                    # Build the cycle path for a clear error message
                    cycle_start_idx = import_chain.index(import_path) if import_path in import_chain else -1
                    if cycle_start_idx >= 0:
                        cycle_path = import_chain[cycle_start_idx:] + [import_path]
                    else:
                        cycle_path = import_chain + [import_path]
                    cycle_display = " -> ".join(Path(p).name for p in cycle_path)
                    raise ConfigLoadError(
                        f"Circular import detected: {cycle_display}\n"
                        f"File '{Path(import_path).name}' was already imported earlier in the chain."
                    )
                self._seen_imports.add(import_path)

                self._record_import(
                    file=import_path,
                    imported_by=parent_file,
                    import_key=import_key,
                    depth=depth + 1,
                )

                imported_data = self._load_file(import_file)

                # Extend the import chain for the recursive call
                extended_chain = import_chain + [import_path]

                self._apply_imports_recursive(
                    imported_data,
                    parent_file=import_path,
                    depth=depth + 1,
                    suppress=suppress,
                    import_chain=extended_chain,
                )

                deep_merge(node, imported_data, suppress=suppress)

            del node["imports"]

        for value in node.values():
            if isinstance(value, dict):
                self._apply_imports_recursive(
                    value,
                    parent_file=parent_file,
                    depth=depth,
                    suppress=suppress,
                    import_chain=import_chain,
                )
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._apply_imports_recursive(
                            item,
                            parent_file=parent_file,
                            depth=depth,
                            suppress=suppress,
                            import_chain=import_chain,
                        )

    # ==================================================================
    # SECRETS
    # ==================================================================

    # NOTE:
    # APP_SECRET_KEY is intentionally read directly from os.getenv()
    # and never stored on ConfigLoader or Config objects.
    # This minimizes secret lifetime and prevents accidental leakage.
    def _inject_secrets(self, data: Dict[str, Any]):
        for key, value in list(data.items()):
            if isinstance(value, str) and value.startswith("ENC(") and value.endswith(")"):
                data[key] = LazySecret(value, key=os.getenv("APP_SECRET_KEY"))
            elif isinstance(value, dict):
                self._inject_secrets(value)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, str) and item.startswith("ENC(") and item.endswith(")"):
                        value[i] = LazySecret(item, key=os.getenv("APP_SECRET_KEY"))
                    elif isinstance(item, dict):
                        self._inject_secrets(item)

    # ==================================================================
    # METADATA
    # ==================================================================

    def _inject_metadata(self, merged: dict):
        node = merged.setdefault("sprigconfig", {})
        meta = node.setdefault("_meta", {})

        meta.setdefault("profile", self.profile or "default")
        meta.setdefault("sources", list(self._merge_trace))
        meta.setdefault("import_trace", list(self._import_trace))
