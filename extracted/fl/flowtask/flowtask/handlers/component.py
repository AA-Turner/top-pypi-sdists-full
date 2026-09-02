"""HTTP handlers for the Flowtask component documentation API.

Two surfaces are exposed:

1. :class:`FlowtaskComponentHandler` — the existing Navigator-style
   ``BaseView`` subclass kept for backward compatibility. Now reads from
   the package-shipped ``flowtask/documentation/generated/`` corpus via
   :mod:`importlib.resources` instead of the legacy ``BASE_DIR/docs``
   tree, so the documentation always matches the installed wheel.

2. :func:`attach_routes` — a small helper for plain aiohttp apps that
   wires the full read-only documentation API:

   .. code-block:: text

       GET  /api/v1/flowtask/components                 # full list / filter
       GET  /api/v1/flowtask/components/{name}          # doc + schema + example
       GET  /api/v1/flowtask/components/{name}/schema   # schema only
       GET  /api/v1/flowtask/categories                 # categories with counts
       GET  /api/v1/flowtask/search?q=...&category=...  # BM25 search

   The search endpoint is backed by the same
   :class:`~flowtask.documentation.toolkit.ComponentDocsToolkit` the
   factory agent uses, so behaviour stays consistent between humans
   browsing the UI and LLMs invoking tools.
"""
from __future__ import annotations

import logging
from importlib import resources
from typing import Any, Optional

import orjson
from aiohttp import web

try:
    from navigator.views import BaseView
except ImportError:  # pragma: no cover — Navigator is optional at runtime
    BaseView = object  # type: ignore[assignment,misc]


DEFAULT_CATEGORY = "Other"
DOCS_PACKAGE = "flowtask.documentation.generated"


# ---------------------------------------------------------------------------
# Package-resource helpers
# ---------------------------------------------------------------------------


def _read_package_bytes(*parts: str) -> Optional[bytes]:
    """Read a file from the docs package, chunked joinpath for MultiplexedPath."""
    try:
        node = resources.files(DOCS_PACKAGE)
    except (ModuleNotFoundError, AttributeError):
        return None
    for part in parts:
        node = node.joinpath(part)
    if not node.is_file():
        return None
    return node.read_bytes()


def _load_index() -> dict:
    """Return the parsed ``index.json`` or an empty structure."""
    raw = _read_package_bytes("index.json")
    if raw is None:
        return {"components": {}}
    try:
        return orjson.loads(raw)
    except orjson.JSONDecodeError:
        return {"components": {}}


def _load_component_doc(rel_file: str) -> Optional[dict]:
    """Load the merged ``<Name>.doc.json`` for a single component.

    The JSON Schema is embedded under the ``schema`` key.
    """
    if not rel_file:
        return None
    raw = _read_package_bytes(*rel_file.split("/"))
    if raw is None:
        return None
    try:
        return orjson.loads(raw)
    except orjson.JSONDecodeError:
        return None


# ---------------------------------------------------------------------------
# Legacy Navigator-style handler
# ---------------------------------------------------------------------------


class FlowtaskComponentHandler(BaseView):
    """Backward-compatible Navigator handler for component documentation.

    Endpoints (registered by the Navigator app):
        ``GET /api/v1/flowtask/components``
            List components. Optional ``category=`` and ``tag=`` filters;
            ``group_by=category`` to nest the result.
        ``GET /api/v1/flowtask/components/{component_name}``
            Return ``{"schema": str, "doc": str, "example": str}`` for one
            component (schema and example are pre-stringified to keep the
            response shape compatible with older clients).
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)

    def _component_doc(self, name: str) -> Optional[dict]:
        """Return the legacy ``{schema, doc, example}`` payload for a component."""
        index = _load_index()
        components = index.get("components", {})
        if name not in components:
            return None

        info = components[name]
        doc_data = _load_component_doc(info.get("file", ""))
        if doc_data is None:
            self.logger.warning(
                "Documentation file missing for component %s", name
            )
            return None
        schema_data = doc_data.get("schema") or {}
        return {
            "schema": orjson.dumps(schema_data).decode("utf-8"),
            "doc": doc_data.get("description", ""),
            "example": "\n".join(doc_data.get("examples", [])),
        }

    def _read_description(self, doc_rel_path: str) -> str:
        """Fallback when an older index doesn't inline ``description``."""
        if not doc_rel_path:
            return ""
        raw = _read_package_bytes(*doc_rel_path.split("/"))
        if raw is None:
            return ""
        try:
            return orjson.loads(raw).get("description", "") or ""
        except orjson.JSONDecodeError:
            return ""

    def _component_entry(self, name: str, info: dict) -> dict:
        description = info.get("description")
        if description is None:
            description = self._read_description(info.get("file", ""))
        return {
            "name": name,
            "description": description or "",
            "category": info.get("category") or DEFAULT_CATEGORY,
        }

    def _filter_components(
        self,
        components: dict,
        category: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> list[dict]:
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
        grouped: dict[str, list[dict]] = {}
        for entry in entries:
            grouped.setdefault(entry["category"], []).append(entry)
        return [
            {"category": cat, "components": grouped[cat]}
            for cat in sorted(grouped)
        ]

    async def get(self) -> web.Response:
        """Dispatch list vs. detail based on the path parameter."""
        params = self.match_parameters()
        component_name = params.get("component_name")

        if component_name:
            doc = self._component_doc(component_name)
            if doc is None:
                return self.error(
                    response={"error": f"Component '{component_name}' not found"},
                    status=404,
                )
            return self.json_response(doc)

        index = _load_index()
        components = index.get("components", {})
        query = self.request.query
        category = query.get("category")
        tag = query.get("tag")
        group_by = (query.get("group_by") or "").lower()

        filtered = self._filter_components(components, category=category, tag=tag)

        if group_by == "category":
            return self.json_response(
                {
                    "categories": self._group_by_category(filtered),
                    "count": len(filtered),
                }
            )

        return self.json_response({"components": filtered, "count": len(filtered)})


# ---------------------------------------------------------------------------
# Plain aiohttp API (no Navigator dependency)
# ---------------------------------------------------------------------------


_TOOLKIT_APP_KEY = "flowtask_docs_toolkit"


async def _get_or_create_toolkit(app: web.Application):
    """Lazily start a :class:`ComponentDocsToolkit` and cache it on the app."""
    # Lazy import keeps the handler module light when only the legacy
    # FlowtaskComponentHandler is needed.
    from flowtask.documentation.toolkit import ComponentDocsToolkit

    toolkit = app.get(_TOOLKIT_APP_KEY)
    if toolkit is None:
        toolkit = ComponentDocsToolkit()
        app[_TOOLKIT_APP_KEY] = toolkit
    await toolkit.start()
    return toolkit


def _json(data: Any, status: int = 200) -> web.Response:
    return web.Response(
        body=orjson.dumps(data),
        status=status,
        content_type="application/json",
    )


async def list_components(request: web.Request) -> web.Response:
    """``GET /components`` — full list with optional ``category=`` filter."""
    index = _load_index()
    components = index.get("components", {})
    category = request.query.get("category")
    entries = []
    for name, info in sorted(components.items()):
        if category is not None and info.get("category") != category:
            continue
        entries.append(
            {
                "name": name,
                "description": info.get("description", ""),
                "category": info.get("category") or DEFAULT_CATEGORY,
            }
        )
    return _json({"components": entries, "count": len(entries)})


async def get_component(request: web.Request) -> web.Response:
    """``GET /components/{name}`` — full doc + schema + examples."""
    name = request.match_info["name"]
    index = _load_index()
    info = index.get("components", {}).get(name)
    if info is None:
        return _json({"error": f"Component '{name}' not found"}, status=404)
    doc_data = _load_component_doc(info.get("file", ""))
    if doc_data is None:
        return _json({"error": f"Documentation file missing for '{name}'"}, status=500)
    schema_data = doc_data.get("schema") or {}
    return _json({"doc": doc_data, "schema": schema_data})


async def get_component_schema(request: web.Request) -> web.Response:
    """``GET /components/{name}/schema`` — JSON schema only."""
    name = request.match_info["name"]
    index = _load_index()
    info = index.get("components", {}).get(name)
    if info is None:
        return _json({"error": f"Component '{name}' not found"}, status=404)
    doc_data = _load_component_doc(info.get("file", ""))
    if doc_data is None:
        return _json({"error": f"Documentation file missing for '{name}'"}, status=500)
    schema_data = doc_data.get("schema")
    if not isinstance(schema_data, dict):
        return _json({"error": f"Schema missing for '{name}'"}, status=500)
    return web.Response(
        body=orjson.dumps(schema_data),
        content_type="application/json",
    )


async def list_categories(request: web.Request) -> web.Response:
    """``GET /categories`` — every category with member counts."""
    index = _load_index()
    buckets: dict[str, list[str]] = {}
    for name, info in index.get("components", {}).items():
        cat = info.get("category") or DEFAULT_CATEGORY
        buckets.setdefault(cat, []).append(name)
    payload = [
        {"name": cat, "count": len(names), "components": sorted(names)}
        for cat, names in sorted(buckets.items())
    ]
    return _json({"categories": payload})


async def search_components(request: web.Request) -> web.Response:
    """``GET /search?q=...&category=...&top_k=...`` — BM25-ranked match."""
    query = request.query.get("q", "")
    if not query.strip():
        return _json({"results": [], "count": 0})
    category = request.query.get("category") or None
    try:
        top_k = int(request.query.get("top_k", "8"))
    except ValueError:
        top_k = 8

    toolkit = await _get_or_create_toolkit(request.app)
    results = await toolkit.search_components(query, category=category, top_k=top_k)
    return _json(
        {
            "results": [r.model_dump() for r in results],
            "count": len(results),
        }
    )


def attach_routes(
    app: web.Application,
    *,
    prefix: str = "/api/v1/flowtask",
) -> None:
    """Register every read-only documentation route on an aiohttp app.

    Args:
        app: The aiohttp application.
        prefix: URL prefix; defaults to ``/api/v1/flowtask`` to match the
            existing Navigator handler.
    """
    app.router.add_get(f"{prefix}/components", list_components)
    app.router.add_get(f"{prefix}/components/{{name}}", get_component)
    app.router.add_get(f"{prefix}/components/{{name}}/schema", get_component_schema)
    app.router.add_get(f"{prefix}/categories", list_categories)
    app.router.add_get(f"{prefix}/search", search_components)
