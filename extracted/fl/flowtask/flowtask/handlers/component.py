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

    def _filter_components(
        self,
        components: dict,
        category: Optional[str] = None,
        tag: Optional[str] = None
    ) -> list[str]:
        """Filter components by category or tag.

        Args:
            components: Dictionary of component info from the index
            category: Optional category to filter by
            tag: Optional tag to filter by

        Returns:
            List of component names matching the filters
        """
        result = []
        for name, info in components.items():
            # If no filters, include all
            if category is None and tag is None:
                result.append(name)
                continue

            # Check category filter
            if category is not None:
                component_category = info.get("category", "")
                if component_category.lower() != category.lower():
                    continue

            # Check tag filter
            if tag is not None:
                component_tags = info.get("tags", [])
                if tag.lower() not in [t.lower() for t in component_tags]:
                    continue

            result.append(name)

        return sorted(result)

    async def get(self) -> web.Response:
        """Handle GET requests for component documentation.

        Routes:
            GET /api/v1/flowtask/components
                Returns a list of all documented component names.
                Supports optional query parameters:
                - category: Filter by component category
                - tag: Filter by component tag

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
        else:
            # List all components with optional filtering
            index = self._load_index()
            components = index.get("components", {})

            # Get optional filter parameters from query string
            query = self.request.query
            category = query.get("category")
            tag = query.get("tag")

            filtered_components = self._filter_components(
                components,
                category=category,
                tag=tag
            )

            return self.json_response({
                "components": filtered_components,
                "count": len(filtered_components)
            })
