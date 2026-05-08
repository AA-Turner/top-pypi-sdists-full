"""Lazy reader for the per-component JSON Schemas under ``docs/components/``.

The HTTP handler at ``flowtask.handlers.component.FlowtaskComponentHandler``
reads the same files; this class is the CLI-side counterpart for the
``--syntax`` checker.
"""
import logging
from pathlib import Path
from typing import Optional

import orjson
from navconfig import BASE_DIR


class ComponentSchemaRegistry:
    """Cached, lazy-loaded view over ``<docs_dir>/components/*.schema.json``.

    Reads the same per-component schema files as the HTTP documentation
    handler, but is designed for safe CLI-side use (no running server required).

    Usage::

        reg = ComponentSchemaRegistry()
        if reg.has("AddDataset"):
            schema = reg.get("AddDataset")

    Args:
        docs_dir: Path to the ``docs/`` directory.  When ``None``, defaults
            to ``BASE_DIR / "docs"``.
    """

    INDEX_FILENAME = "index.json"
    COMPONENTS_DIRNAME = "components"

    def __init__(self, docs_dir: Optional[Path] = None) -> None:
        self.docs_dir: Path = Path(docs_dir) if docs_dir else (BASE_DIR / "docs")
        self.logger = logging.getLogger("FlowTask.Syntax.Registry")
        self._index: Optional[dict] = None
        self._schema_cache: dict[str, dict] = {}

    # --- public API --------------------------------------------------------

    def known(self) -> set[str]:
        """Return the set of component names listed in ``index.json``.

        Returns:
            Set of component name strings; empty if the index is missing.
        """
        index = self._load_index()
        return set(index.get(self.COMPONENTS_DIRNAME, {}).keys())

    def has(self, component: str) -> bool:
        """Return whether ``component`` is documented in the index.

        Args:
            component: Component class name to look up.

        Returns:
            ``True`` if the component is in the index; ``False`` otherwise.
        """
        return component in self._load_index().get(self.COMPONENTS_DIRNAME, {})

    def get(self, component: str) -> Optional[dict]:
        """Load and return the JSON Schema dict for ``component``.

        Results are cached per-component on first read.

        Args:
            component: Component class name to look up.

        Returns:
            Parsed JSON Schema ``dict``, or ``None`` if the component is
            unknown or its schema file is missing or unreadable.
        """
        if component in self._schema_cache:
            return self._schema_cache[component]

        index = self._load_index()
        info = index.get(self.COMPONENTS_DIRNAME, {}).get(component)
        if not info:
            return None
        rel = info.get("schema")
        if not rel:
            return None

        schema_path = self.docs_dir / rel
        if not schema_path.exists():
            self.logger.warning(
                "Component schema missing on disk: %s", schema_path
            )
            return None
        try:
            data = orjson.loads(schema_path.read_bytes())
        except (orjson.JSONDecodeError, OSError) as e:
            self.logger.warning("Failed to read %s: %s", schema_path, e)
            return None
        self._schema_cache[component] = data
        return data

    # --- internals ---------------------------------------------------------

    def _load_index(self) -> dict:
        """Load and cache ``index.json``, returning an empty dict on failure.

        Returns:
            Parsed index dict (always has at least ``{"components": {}}``).
        """
        if self._index is not None:
            return self._index
        index_path = self.docs_dir / self.INDEX_FILENAME
        if not index_path.exists():
            self.logger.warning(
                "Documentation index not found: %s", index_path
            )
            self._index = {self.COMPONENTS_DIRNAME: {}}
            return self._index
        try:
            self._index = orjson.loads(index_path.read_bytes())
        except (orjson.JSONDecodeError, OSError) as e:
            self.logger.warning("Failed to load %s: %s", index_path, e)
            self._index = {self.COMPONENTS_DIRNAME: {}}
        return self._index
