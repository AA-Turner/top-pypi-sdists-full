"""HTTP handler for Flowtask component documentation API."""
import logging
from pathlib import Path
from typing import Any, Optional

import orjson
from aiohttp import web
from navigator.views import BaseView
from navconfig import BASE_DIR


class FlowtaskComponentHandler(BaseView):
    """Handler for component documentation API.

    Provides REST API access to pre-generated component documentation.
    Documentation files are read from the BASE_DIR/documentation directory.

    Endpoints:
        GET /api/v1/flowtask/components - List all documented components
        GET /api/v1/flowtask/components/{component_name} - Get component documentation

    Attributes:
        docs_dir: Path to the documentation directory
        logger: Logger instance for this handler
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the handler.

        Args:
            *args: Positional arguments passed to BaseView
            **kwargs: Keyword arguments passed to BaseView
        """
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.docs_dir: Path = BASE_DIR / "docs"

    def _load_index(self) -> dict:
        """Load the component documentation index.

        Returns:
            Dictionary containing the documentation index.
            Returns empty structure if index file doesn't exist.
        """
        index_path = self.docs_dir / "index.json"
        if not index_path.exists():
            self.logger.error(
                f"Documentation index not found: {index_path}"
            )
            return {"components": {}}
        try:
            return orjson.loads(index_path.read_bytes())
        except (orjson.JSONDecodeError, OSError) as e:
            self.logger.error(
                f"Failed to load documentation index: {index_path}: {e}"
            )
            return {"components": {}}

    def _load_component_doc(self, name: str) -> Optional[dict]:
        """Load documentation for a specific component.

        Args:
            name: The component name to load documentation for

        Returns:
            Dictionary with schema, doc, and example keys, or None if not found
        """
        index = self._load_index()
        components = index.get("components", {})

        if name not in components:
            return None

        component_info = components[name]
        schema_path = self.docs_dir / component_info.get("schema", "")
        doc_path = self.docs_dir / component_info.get("doc", "")

        # Verify both files exist
        if not schema_path.exists() or not doc_path.exists():
            self.logger.warning(
                f"Documentation files missing for component {name}: schema={schema_path.exists()}, doc={doc_path.exists()}"
            )
            return None

        try:
            schema_data = orjson.loads(schema_path.read_bytes())
            doc_data = orjson.loads(doc_path.read_bytes())
        except (orjson.JSONDecodeError, OSError) as e:
            self.logger.error(
                f"Failed to load documentation for {name}: {e}"
            )
            return None

        # Format response as specified in the spec
        return {
            "schema": orjson.dumps(schema_data).decode("utf-8"),
            "doc": doc_data.get("description", ""),
            "example": "\n".join(doc_data.get("examples", []))
        }

    DEFAULT_CATEGORY = "Other"

    def _read_description(self, doc_rel_path: str) -> str:
        """Read the description field from a component doc file.

        Used as a fallback when the index entry doesn't carry a description
        (older indexes generated before the field was inlined).

        Args:
            doc_rel_path: Path to the doc JSON file, relative to docs_dir

        Returns:
            The component description, or an empty string if unavailable.
        """
        if not doc_rel_path:
            return ""
        doc_path = self.docs_dir / doc_rel_path
        if not doc_path.exists():
            return ""
        try:
            return orjson.loads(doc_path.read_bytes()).get("description", "") or ""
        except (orjson.JSONDecodeError, OSError) as e:
            self.logger.warning(
                f"Failed to read description from {doc_path}: {e}"
            )
            return ""

    def _component_entry(self, name: str, info: dict) -> dict:
        """Build the public list-entry payload for one component.

        Args:
            name: Component class name.
            info: The matching value from ``index.json``'s components map.

        Returns:
            Dict with ``name``, ``description``, and ``category``.
        """
        description = info.get("description")
        if description is None:
            description = self._read_description(info.get("doc", ""))
        return {
            "name": name,
            "description": description or "",
            "category": info.get("category") or self.DEFAULT_CATEGORY,
        }

    def _filter_components(
        self,
        components: dict,
        category: Optional[str] = None,
        tag: Optional[str] = None
    ) -> list[dict]:
        """Filter components by category or tag.

        Args:
            components: Dictionary of component info from the index
            category: Optional category to filter by
            tag: Optional tag to filter by

        Returns:
            List of dicts with `name`, `description`, and `category`,
            sorted by name.
        """
        matched: list[tuple[str, dict]] = []
        for name, info in components.items():
            if category is not None:
                if info.get("category", "").lower() != category.lower():
                    continue
            if tag is not None:
                component_tags = info.get("tags", [])
                if tag.lower() not in [t.lower() for t in component_tags]:
                    continue
            matched.append((name, info))

        matched.sort(key=lambda item: item[0])
        return [self._component_entry(name, info) for name, info in matched]

    def _group_by_category(self, entries: list[dict]) -> list[dict]:
        """Group a flat list of component entries by category.

        Args:
            entries: List of dicts produced by ``_component_entry``.

        Returns:
            List of ``{"category": str, "components": [...]}`` dicts, sorted by
            category name.
        """
        grouped: dict[str, list[dict]] = {}
        for entry in entries:
            grouped.setdefault(entry["category"], []).append(entry)
        return [
            {"category": cat, "components": grouped[cat]}
            for cat in sorted(grouped)
        ]

    async def get(self) -> web.Response:
        """Handle GET requests for component documentation.

        Routes:
            GET /api/v1/flowtask/components
                Returns a list of all documented components, each as a dict
                with ``name``, ``description``, and ``category``.
                Optional query parameters:
                - category: Filter by component category
                - tag: Filter by component tag
                - group_by=category: Return components grouped by category

            GET /api/v1/flowtask/components/{component_name}
                Returns documentation for a specific component.

        Returns:
            JSON response with component list or documentation,
            or 404 error if component not found.
        """
        params = self.match_parameters()
        component_name = params.get("component_name")

        if component_name:
            # Get specific component documentation
            doc = self._load_component_doc(component_name)
            if doc is None:
                return self.error(
                    response={"error": f"Component '{component_name}' not found"},
                    status=404
                )
            return self.json_response(doc)

        # List all components with optional filtering
        index = self._load_index()
        components = index.get("components", {})

        query = self.request.query
        category = query.get("category")
        tag = query.get("tag")
        group_by = (query.get("group_by") or "").lower()

        filtered_components = self._filter_components(
            components,
            category=category,
            tag=tag
        )

        if group_by == "category":
            return self.json_response({
                "categories": self._group_by_category(filtered_components),
                "count": len(filtered_components),
            })

        return self.json_response({
            "components": filtered_components,
            "count": len(filtered_components),
        })
