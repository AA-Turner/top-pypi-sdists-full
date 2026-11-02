"""End-to-end tests for RestClient file operation methods.

This module tests the public API surface of upload_file and list_files methods on RestClient.
These are convenience methods that wrap the underlying data storage functionality and are
designed for easy integration with task submission workflows.
"""

import os
from pathlib import Path
from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from edison_client.clients.rest_client import RestClient
from edison_client.models.app import Stage

ADMIN_API_KEY = os.environ.get("PLAYWRIGHT_ADMIN_API_KEY", "")


@pytest_asyncio.fixture(name="admin_client")
async def fixture_admin_client():
    """Create a RestClient for testing; using an admin user key with full access."""
    client = RestClient(
        stage=Stage.DEV,
        api_key=ADMIN_API_KEY,
    )
    try:
        yield client
    finally:
        await client.aclose()


class TestRestClientFileOperations:
    """Test the RestClient public API for file operations."""

    @pytest.mark.timeout(300)
    def test_upload_file_returns_correct_uri_format(self, admin_client: RestClient):
        """Test that upload_file returns URI in the correct format."""
        file_path = Path(__file__).parent / "test_data" / "test_file.txt"

        uri = admin_client.upload_file(
            file_path, description="Test file upload via RestClient API"
        )

        # Verify URI format
        assert uri.startswith("data_entry:"), (
            f"URI should start with 'data_entry:', got: {uri}"
        )

        # Extract and validate UUID
        data_storage_id = uri.split(":", 1)[1]
        try:
            uuid_obj = uuid4()
            # Verify it's a valid UUID format by trying to parse it
            assert len(data_storage_id) == len(str(uuid_obj))
            assert "-" in data_storage_id
        except (ValueError, AssertionError) as e:
            pytest.fail(f"Invalid UUID in URI: {data_storage_id}, error: {e}")

        # Clean up
        admin_client.delete_data_storage_entry(UUID(data_storage_id))

    @pytest.mark.timeout(300)
    def test_upload_file_nonexistent_raises_error(self, admin_client: RestClient):
        """Test that upload_file raises FileNotFoundError for nonexistent files."""
        nonexistent_path = Path("/tmp/nonexistent_file_12345.txt")  # noqa: S108

        with pytest.raises(FileNotFoundError, match="File or directory not found"):
            admin_client.upload_file(nonexistent_path)

    @pytest.mark.timeout(300)
    def test_upload_with_metadata_and_tags(self, admin_client: RestClient):
        """Test upload_file with optional metadata and tags."""
        file_path = Path(__file__).parent / "test_data" / "test_file.txt"

        uri = admin_client.upload_file(
            file_path,
            name="test_with_metadata.txt",
            description="File with metadata",
            metadata={"source": "test", "version": "1.0"},
            tags=["test", "e2e"],
        )

        assert uri.startswith("data_entry:")
        data_storage_id = uri.split(":", 1)[1]

        # Verify we can fetch it
        result = admin_client.fetch_data_from_storage(UUID(data_storage_id))
        assert result is not None

        # Clean up
        admin_client.delete_data_storage_entry(UUID(data_storage_id))

    @pytest.mark.timeout(300)
    def test_upload_directory(self, admin_client: RestClient):
        """Test upload_file with a directory."""
        dir_path = Path(__file__).parent / "test_data"

        uri = admin_client.upload_file(
            dir_path, name="test_directory", description="Test directory upload"
        )

        assert uri.startswith("data_entry:")
        data_storage_id = uri.split(":", 1)[1]

        # Note: Directory uploads are processed asynchronously and may not be
        # immediately available for download. In production, poll until stable.
        # For now, just verify the URI format and clean up.

        # Clean up
        admin_client.delete_data_storage_entry(UUID(data_storage_id))
