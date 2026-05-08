"""Integration tests for Component Documentation API.

These tests verify that the routes are properly registered and the handler
returns correct responses.
"""
import pytest
from unittest.mock import patch
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer
import orjson


@pytest.fixture
def mock_docs_dir(tmp_path):
    """Create mock documentation directory with test data."""
    docs = tmp_path / "documentation"
    docs.mkdir()
    components = docs / "components"
    components.mkdir()

    # Create index
    index = {
        "updated_at": "2026-03-03T12:00:00",
        "components": {
            "AddDataset": {
                "schema": "components/AddDataset.schema.json",
                "doc": "components/AddDataset.doc.json",
                "category": "data",
                "tags": ["join", "pandas"]
            },
            "FileList": {
                "schema": "components/FileList.schema.json",
                "doc": "components/FileList.doc.json",
                "category": "io",
                "tags": ["file", "list"]
            }
        }
    }
    (docs / "index.json").write_bytes(orjson.dumps(index))

    # Create AddDataset files
    schema = {
        "title": "AddDataset",
        "type": "object",
        "properties": {"dataset": {"type": "string", "description": "Dataset name"}},
        "required": ["dataset"]
    }
    doc = {
        "description": "Joins two pandas DataFrames.",
        "examples": ["AddDataset:\n  dataset: my_data"]
    }
    (components / "AddDataset.schema.json").write_bytes(orjson.dumps(schema))
    (components / "AddDataset.doc.json").write_bytes(orjson.dumps(doc))

    # Create FileList files
    schema2 = {
        "title": "FileList",
        "type": "object",
        "properties": {"pattern": {"type": "string"}},
        "required": ["pattern"]
    }
    doc2 = {
        "description": "Lists files matching a pattern.",
        "examples": ["FileList:\n  pattern: '*.csv'"]
    }
    (components / "FileList.schema.json").write_bytes(orjson.dumps(schema2))
    (components / "FileList.doc.json").write_bytes(orjson.dumps(doc2))

    return docs


def create_test_app():
    """Create a test aiohttp application with routes registered."""
    from flowtask.handlers.component import FlowtaskComponentHandler

    app = web.Application()
    app.router.add_view("/api/v1/flowtask/components", FlowtaskComponentHandler)
    app.router.add_view(
        "/api/v1/flowtask/components/{component_name}",
        FlowtaskComponentHandler
    )
    return app


class TestComponentAPIRoutes:
    """Test that component API routes are properly registered."""

    @pytest.mark.asyncio
    async def test_list_components_route_exists(self, mock_docs_dir):
        """Test GET /api/v1/flowtask/components route is accessible."""
        app = create_test_app()

        with patch("flowtask.handlers.component.BASE_DIR", mock_docs_dir.parent):
            async with TestClient(TestServer(app)) as client:
                resp = await client.get("/api/v1/flowtask/components")

                assert resp.status == 200
                data = await resp.json()
                assert "components" in data
                assert "count" in data

    @pytest.mark.asyncio
    async def test_list_components_returns_all(self, mock_docs_dir):
        """Test GET /api/v1/flowtask/components returns all components."""
        app = create_test_app()

        with patch("flowtask.handlers.component.BASE_DIR", mock_docs_dir.parent):
            async with TestClient(TestServer(app)) as client:
                resp = await client.get("/api/v1/flowtask/components")

                assert resp.status == 200
                data = await resp.json()
                assert data["count"] == 2
                names = [c["name"] for c in data["components"]]
                assert "AddDataset" in names
                assert "FileList" in names
                for entry in data["components"]:
                    assert set(entry.keys()) == {"name", "description"}

    @pytest.mark.asyncio
    async def test_get_component_returns_doc(self, mock_docs_dir):
        """Test GET /api/v1/flowtask/components/{name} returns documentation."""
        app = create_test_app()

        with patch("flowtask.handlers.component.BASE_DIR", mock_docs_dir.parent):
            async with TestClient(TestServer(app)) as client:
                resp = await client.get("/api/v1/flowtask/components/AddDataset")

                assert resp.status == 200
                data = await resp.json()
                assert "schema" in data
                assert "doc" in data
                assert "example" in data
                assert data["doc"] == "Joins two pandas DataFrames."

    @pytest.mark.asyncio
    async def test_get_unknown_component_404(self, mock_docs_dir):
        """Test GET /api/v1/flowtask/components/{unknown} returns 404."""
        app = create_test_app()

        with patch("flowtask.handlers.component.BASE_DIR", mock_docs_dir.parent):
            async with TestClient(TestServer(app)) as client:
                resp = await client.get("/api/v1/flowtask/components/NonExistent")

                assert resp.status == 404
                data = await resp.json()
                assert "error" in data

    @pytest.mark.asyncio
    async def test_filter_by_category(self, mock_docs_dir):
        """Test GET /api/v1/flowtask/components?category=data filters results."""
        app = create_test_app()

        with patch("flowtask.handlers.component.BASE_DIR", mock_docs_dir.parent):
            async with TestClient(TestServer(app)) as client:
                resp = await client.get("/api/v1/flowtask/components?category=data")

                assert resp.status == 200
                data = await resp.json()
                assert data["count"] == 1
                assert data["components"][0]["name"] == "AddDataset"

    @pytest.mark.asyncio
    async def test_filter_by_tag(self, mock_docs_dir):
        """Test GET /api/v1/flowtask/components?tag=file filters results."""
        app = create_test_app()

        with patch("flowtask.handlers.component.BASE_DIR", mock_docs_dir.parent):
            async with TestClient(TestServer(app)) as client:
                resp = await client.get("/api/v1/flowtask/components?tag=file")

                assert resp.status == 200
                data = await resp.json()
                assert data["count"] == 1
                assert data["components"][0]["name"] == "FileList"


class TestComponentDocumentationExtension:
    """Test the ComponentDocumentation extension."""

    def test_extension_registers_routes(self, mock_docs_dir):
        """Test that the extension registers the expected routes."""
        from flowtask.extensions.component_docs import ComponentDocumentation

        app = web.Application()
        extension = ComponentDocumentation()

        with patch("flowtask.handlers.component.BASE_DIR", mock_docs_dir.parent):
            extension.setup(app)

        # Check routes are registered
        routes = [route.resource.canonical for route in app.router.routes()]
        assert "/api/v1/flowtask/components" in routes
        assert "/api/v1/flowtask/components/{component_name}" in routes

    def test_extension_inherits_base_extension(self):
        """Test that ComponentDocumentation inherits from BaseExtension."""
        from flowtask.extensions.component_docs import ComponentDocumentation
        from flowtask.extensions import BaseExtension

        assert issubclass(ComponentDocumentation, BaseExtension)

    @pytest.mark.asyncio
    async def test_extension_with_test_client(self, mock_docs_dir):
        """Test the extension works with aiohttp test client."""
        from flowtask.extensions.component_docs import ComponentDocumentation

        app = web.Application()
        extension = ComponentDocumentation()

        with patch("flowtask.handlers.component.BASE_DIR", mock_docs_dir.parent):
            extension.setup(app)

            async with TestClient(TestServer(app)) as client:
                # Test list endpoint
                resp = await client.get("/api/v1/flowtask/components")
                assert resp.status == 200

                # Test detail endpoint
                resp = await client.get("/api/v1/flowtask/components/AddDataset")
                assert resp.status == 200
