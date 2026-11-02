# ruff: noqa: ARG001, RUF029
import json
import tempfile
import zipfile
from io import BytesIO
from pathlib import Path
from unittest.mock import ANY, AsyncMock, Mock, patch
from uuid import uuid4

import httpx
import pytest
import requests as requests_lib
from httpx import HTTPStatusError, codes

from edison_client.clients.data_storage_methods import (
    DataStorageCreationError,
    DataStorageError,
    DataStorageMethods,
    DataStorageRetrievalError,
    RestClientError,
)
from edison_client.clients.multipart_upload import (
    _aupload_file_multipart,
    _aupload_one_part,
    _b64_md5,
    _calculate_multipart_ranges,
    _upload_file_multipart,
)
from edison_client.models.data_storage_methods import (
    DataStorageEntryStatus,
    DataStorageLocationPayload,
    DataStorageRequestPayload,
    DataStorageResponse,
    DirectoryManifest,
    ManifestEntry,
    RawFetchResponse,
)


class MockDataStorageMethods(DataStorageMethods):
    """Mock implementation of DataStorageMethods for testing."""

    def __init__(self):
        self._client = Mock()
        self._async_client = AsyncMock()

    @property
    def client(self):
        return self._client

    @property
    def async_client(self):
        return self._async_client


class TestDataStorageMethods:
    """Test cases for DataStorageMethods class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.methods = MockDataStorageMethods()  # pylint: disable=attribute-defined-outside-init
        self.test_uuid = uuid4()  # pylint: disable=attribute-defined-outside-init
        self.test_project_id = uuid4()  # pylint: disable=attribute-defined-outside-init

    def _create_mock_response(
        self,
        storage_type="gcs",
        signed_url="https://example.com/signed-url",
        content=None,
    ):
        """Create a complete mock response with all required fields."""
        from datetime import datetime  # noqa: PLC0415

        now = datetime.now().isoformat() + "Z"
        user_id = str(uuid4())
        storage_location_id = str(uuid4())

        return {
            "data_storage": {
                "id": str(self.test_uuid),
                "name": "test",
                "user_id": user_id,
                "created_at": now,
                "modified_at": now,
                "content": content,
                "status": "active",
                "share_status": "private",
            },
            "storage_locations": [
                {
                    "id": storage_location_id,
                    "data_storage_id": str(self.test_uuid),
                    "storage_config": {
                        "signed_url": signed_url,
                        "storage_type": storage_type,
                        "content_type": "application/octet-stream",
                    },
                    "created_at": now,
                }
            ],
        }

    def test_handle_http_errors_forbidden(self):
        """Test handling of 403 Forbidden errors."""
        mock_response = Mock()
        mock_response.status_code = codes.FORBIDDEN
        mock_response.text = "Access denied"

        error = HTTPStatusError("Forbidden", request=Mock(), response=mock_response)

        with pytest.raises(DataStorageError, match="not authorized"):
            self.methods._handle_http_errors(error, "creating")

    def test_handle_http_errors_unprocessable_entity(self):
        """Test handling of 422 Unprocessable Entity errors."""
        mock_response = Mock()
        mock_response.status_code = codes.UNPROCESSABLE_ENTITY
        mock_response.text = "Invalid payload"

        error = HTTPStatusError(
            "Unprocessable Entity", request=Mock(), response=mock_response
        )

        with pytest.raises(DataStorageError, match="Invalid request payload"):
            self.methods._handle_http_errors(error, "creating")

    def test_handle_http_errors_generic(self):
        """Test handling of generic HTTP errors."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal server error"

        error = HTTPStatusError(
            "Internal Server Error", request=Mock(), response=mock_response
        )

        with pytest.raises(DataStorageError, match="500 - Internal server error"):
            self.methods._handle_http_errors(error, "creating")

    def test_validate_file_path_exists(self):
        """Test file path validation with existing file."""
        with tempfile.NamedTemporaryFile() as temp_file:
            result = self.methods._validate_file_path(temp_file.name)
            assert isinstance(result, Path)
            assert result.exists()

    def test_validate_file_path_not_exists(self):
        """Test file path validation with non-existent file."""
        with pytest.raises(DataStorageError, match="not found"):
            self.methods._validate_file_path("/nonexistent/file.txt")

    def test_build_zip_path_with_path(self):
        """Test building zip path with existing path."""
        result = self.methods._build_zip_path("test", "/some/path")

        # Verify path construction with existing path
        assert isinstance(result, str)
        assert result == "/some/path/test.zip"
        assert result.endswith(".zip")
        assert result.startswith("/some/path/")
        assert "test.zip" in result

    def test_build_zip_path_without_path(self):
        """Test building zip path without existing path."""
        result = self.methods._build_zip_path("test", None)

        # Verify path construction without existing path
        assert isinstance(result, str)
        assert result == "test.zip"
        assert result.endswith(".zip")
        assert result.startswith("test")
        assert len(result) == 8  # "test.zip" is 8 characters

    def test_build_zip_path_already_zip(self):
        """Test building zip path when name already has .zip extension."""
        result = self.methods._build_zip_path("test.zip", "/some/path")

        # Verify path construction handles existing .zip extension
        assert isinstance(result, str)
        assert result == "/some/path/test.zip"
        assert result.endswith(".zip")
        assert result.startswith("/some/path/")
        assert "test.zip" in result
        assert result.count(".zip") == 1  # Should not duplicate .zip extension

    def test_is_zip_file_true(self):
        """Test zip file detection with actual zip file."""
        with tempfile.NamedTemporaryFile(suffix=".zip") as temp_file:
            with zipfile.ZipFile(temp_file.name, "w") as zipf:
                zipf.writestr("test.txt", "test content")

            # Verify zip file detection works correctly
            result = self.methods._is_zip_file(Path(temp_file.name))
            assert isinstance(result, bool)
            assert result is True
            assert temp_file.name.endswith(".zip")
            assert Path(temp_file.name).exists()

    def test_is_zip_file_false(self):
        """Test zip file detection with non-zip file."""
        with tempfile.NamedTemporaryFile(suffix=".txt") as temp_file:
            temp_file.write(b"not a zip file")
            temp_file.flush()

            # Verify non-zip file detection works correctly
            result = self.methods._is_zip_file(Path(temp_file.name))
            assert isinstance(result, bool)
            assert result is False
            assert temp_file.name.endswith(".txt")
            assert Path(temp_file.name).exists()

    def test_extract_zip_file(self):
        """Test zip file extraction."""
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / "test.zip"

            # Create a test zip file
            with zipfile.ZipFile(zip_path, "w") as zipf:
                zipf.writestr("test.txt", "test content")
                zipf.writestr("subdir/file.txt", "subdir content")

            extract_to = Path(temp_dir) / "extract"
            extract_to.mkdir(exist_ok=True)
            result = self.methods._extract_zip_file(zip_path, extract_to)

            # Verify zip extraction creates the expected directory structure
            assert isinstance(result, Path)
            assert result.exists()
            assert result.is_dir()
            # The result path may include an "extracted" subdirectory
            assert extract_to in result.parents or result == extract_to
            assert (result / "test.txt").exists()
            assert (result / "subdir" / "file.txt").exists()
            assert (result / "subdir").is_dir()
            # Count the actual items in the extracted directory
            actual_items = list(result.iterdir())
            assert (
                len(actual_items) >= 2
            )  # Should have at least 2 items: test.txt and subdir

    @patch("edison_client.clients.data_storage_methods.requests_lib.get")
    def test_download_from_gcs_success(self, mock_get):
        """Test successful GCS download."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"content-disposition": 'filename="test.txt"'}
        mock_response.iter_content.return_value = [b"test content"]
        mock_get.return_value.__enter__.return_value = mock_response

        result = self.methods._download_from_gcs("https://example.com/signed-url")

        # Verify GCS download creates the expected file
        assert isinstance(result, Path)
        assert result.exists()
        assert result.is_file()
        assert result.name == "test.txt"
        assert result.suffix == ".txt"
        assert result.stat().st_size > 0  # File should have content

    @patch("edison_client.clients.data_storage_methods.requests_lib.get")
    def test_download_from_gcs_zip_file(self, mock_get):
        """Test GCS download of zip file with automatic extraction."""
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / "test.zip"

            # Create a test zip file
            with zipfile.ZipFile(zip_path, "w") as zipf:
                zipf.writestr("test.txt", "test content")

            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.headers = {"content-disposition": 'filename="test.zip"'}
            mock_response.iter_content.return_value = [zip_path.read_bytes()]
            mock_get.return_value.__enter__.return_value = mock_response

            result = self.methods._download_from_gcs("https://example.com/signed-url")

            # Verify zip file download and extraction
            assert isinstance(result, Path)
            assert result.exists()
            # The result should be the extracted directory, not the zip file
            if result.is_dir():
                assert result.is_dir()
                assert (result / "test.txt").exists()
                assert (result / "test.txt").is_file()
                assert len(list(result.iterdir())) == 1  # Should have 1 file
            else:
                # If it's a single file, check the file itself
                assert result.is_file()
                assert result.name == "test.txt"
                assert result.suffix == ".txt"

    @pytest.mark.parametrize("filename", ["study.prism", "study.phxproj"])
    @patch("edison_client.clients.data_storage_methods.requests_lib.get")
    def test_download_from_gcs_keeps_scientific_packages_packed(
        self, mock_get, filename: str
    ):
        """Prism and Phoenix project files must stay packed after GCS download."""
        packed = BytesIO()
        with zipfile.ZipFile(packed, "w") as archive:
            archive.writestr("document.json", "{}")
            archive.writestr("misc/info.txt", "x")

        mock_response = Mock()
        mock_response.headers = {"content-disposition": f'filename="{filename}"'}
        mock_response.iter_content.return_value = [packed.getvalue()]
        mock_get.return_value.__enter__.return_value = mock_response

        result = self.methods._download_from_gcs("https://example.com/signed-url")

        assert result.name == filename
        with zipfile.ZipFile(result) as archive:
            assert archive.namelist() == ["document.json", "misc/info.txt"]
        assert not (result.parent / "document.json").exists()

    @patch("edison_client.clients.data_storage_methods.requests_lib.get")
    def test_download_from_gcs_resumes_after_connection_drop(self, mock_get):
        """Resume logic sends Range header and appends on retry."""
        content = b"hello world full content"
        drop_at = 10  # drop after 10 bytes on first attempt

        call_count = 0

        def side_effect(url, **kwargs):
            nonlocal call_count
            call_count += 1
            mock_response = Mock()
            mock_response.__enter__ = lambda s: s
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.headers = {}
            if call_count == 1:
                # First attempt: drop mid-stream
                mock_response.status_code = 200

                def first_iter(chunk_size=8192):
                    yield content[:drop_at]
                    raise requests_lib.exceptions.ChunkedEncodingError("dropped")

                mock_response.iter_content = first_iter
                mock_response.raise_for_status = Mock()
            else:
                # Second attempt: serve remaining bytes (simulating Range response)
                mock_response.status_code = 206
                mock_response.iter_content = Mock(return_value=[content[drop_at:]])
                mock_response.raise_for_status = Mock()
            return mock_response

        mock_get.side_effect = side_effect

        result = self.methods._download_from_gcs(
            "https://example.com/signed-url", file_name="data.bin", retry_wait_base=0
        )

        assert result.read_bytes() == content
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_adownload_from_gcs_resumes_after_connection_drop(self):
        """Async resume logic retries and appends remaining bytes after a drop."""
        content = b"async full content here"
        drop_at = 10

        call_count = 0

        def make_stream_ctx(status_code, headers, chunks, drop_after=None):
            class FakeResponse:
                def __init__(self):
                    self.status_code = status_code
                    self.headers = headers

                def raise_for_status(self):
                    pass

                async def aiter_bytes(self, chunk_size=8192):
                    sent = 0
                    for chunk in chunks:
                        if drop_after is not None and sent >= drop_after:
                            raise httpx.ReadError("mock drop")
                        yield chunk
                        sent += len(chunk)

            class AsyncCtx:
                async def __aenter__(self):
                    return FakeResponse()

                async def __aexit__(self, *args):
                    pass

            return AsyncCtx()

        def stream_side_effect(method, url, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return make_stream_ctx(
                    200, {}, [content[:drop_at], content[drop_at:]], drop_after=drop_at
                )
            return make_stream_ctx(206, {}, [content[drop_at:]])

        fake_client = AsyncMock()
        fake_client.__aenter__.return_value = fake_client
        fake_client.stream = stream_side_effect

        with patch(
            "edison_client.clients.data_storage_methods.AsyncClient",
            return_value=fake_client,
        ):
            result = await self.methods._adownload_from_gcs(
                "https://example.com/signed-url",
                file_name="data.bin",
                retry_wait_base=0,
            )

        assert result.read_bytes() == content
        assert call_count == 2

    def test_prepare_single_file_upload_small_text(self):
        """Test preparation of small text file for upload."""
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", suffix=".txt", mode="w"
        ) as temp_file:
            temp_file.write("small text content")
            temp_file.flush()

            file_size, payload = self.methods._prepare_single_file_upload(
                name="test.txt",
                file_path=Path(temp_file.name),
                description="Test description",
                file_path_override=None,
                dataset_id=None,
                project_id=None,
                metadata=None,
                tags=None,
                parent_id=None,
            )

            assert file_size > 0
            assert payload is not None
            assert payload.content == "small text content"
            assert payload.name == "test.txt"

    def test_prepare_single_file_upload_empty_text_file_inlines(self):
        """Zero-byte text files inline content='' (server assigns RAW_CONTENT)."""
        with tempfile.TemporaryDirectory() as tmp:
            empty_txt = Path(tmp) / "empty.txt"
            empty_txt.write_text("")

            file_size, payload = self.methods._prepare_single_file_upload(
                name=empty_txt.name,
                file_path=empty_txt,
                description="",
                file_path_override=None,
                dataset_id=None,
                project_id=None,
                metadata=None,
                tags=None,
                parent_id=None,
            )

            assert file_size == 0
            assert payload is not None
            assert payload.content == ""  # noqa: PLC1901

    def test_prepare_single_file_upload_large_file(self):
        """Test preparation of large file for upload."""
        with tempfile.NamedTemporaryFile(suffix=".bin") as temp_file:
            # Write enough data to exceed the small file threshold
            temp_file.write(b"0" * (11 * 1024 * 1024))  # 11MB
            temp_file.flush()

            file_size, payload = self.methods._prepare_single_file_upload(
                name="large.bin",
                file_path=Path(temp_file.name),
                description="Large file",
                file_path_override=None,
                dataset_id=None,
                project_id=None,
                metadata=None,
                tags=None,
                parent_id=None,
            )

            assert file_size > 0
            assert payload is None  # Should not be sent as text content

    def test_create_data_storage_entry_sync(self):
        """Test synchronous data storage entry creation."""
        mock_response = Mock()
        mock_response.json.return_value = self._create_mock_response()
        mock_response.raise_for_status.return_value = None

        self.methods.client.post.return_value = mock_response

        payload = DataStorageRequestPayload(
            name="test", description="Test description", content="test content"
        )

        result = self.methods._create_data_storage_entry(payload)

        assert result.data_storage.id == self.test_uuid
        assert (
            result.storage_locations[0].storage_config.signed_url
            == "https://example.com/signed-url"
        )

    @pytest.mark.asyncio
    async def test_acreate_data_storage_entry_async(self):
        """Test asynchronous data storage entry creation."""
        mock_response = Mock()
        mock_response.json.return_value = self._create_mock_response()
        mock_response.raise_for_status.return_value = None

        # Make the post method return the mock response asynchronously
        self.methods.async_client.post = AsyncMock(return_value=mock_response)

        payload = DataStorageRequestPayload(
            name="test", description="Test description", content="test content"
        )

        result = await self.methods._acreate_data_storage_entry(payload)

        assert result.data_storage.id == self.test_uuid
        assert (
            result.storage_locations[0].storage_config.signed_url
            == "https://example.com/signed-url"
        )

    def test_generate_folder_description_from_files(self):
        """Test folder description generation from files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test files
            (temp_path / "file1.txt").write_text("content1")
            (temp_path / "file2.txt").write_text("content2")

            manifest = DirectoryManifest()
            manifest.entries = {
                "file1.txt": ManifestEntry(description="First file"),
                "file2.txt": ManifestEntry(description="Second file"),
            }

            result = self.methods._generate_folder_description_from_files(
                temp_path, manifest
            )

            # Verify the generated description contains expected content
            assert isinstance(result, str)
            assert "file1.txt: First file" in result
            assert "file2.txt: Second file" in result
            assert result.startswith("Directory containing:")
            assert (
                len(result.split(", ")) == 2
            )  # Should have exactly 2 file descriptions

    def test_load_manifest_json(self):
        """Test loading JSON manifest file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            manifest_path = temp_path / "manifest.json"

            manifest_data = {
                "test_dir": {
                    "type": "directory",
                    "description": "Test directory",
                    "entries": {},
                }
            }

            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest_data, f)

            result = self.methods._load_manifest(temp_path, "manifest.json")

            # Verify the manifest structure and content
            assert isinstance(result, DirectoryManifest)
            test_dir_entry = result.entries["test_dir"]
            assert isinstance(test_dir_entry, ManifestEntry)
            assert test_dir_entry.description == "Test directory"
            assert len(result.entries) == 1  # Should have exactly one entry

    def test_load_manifest_yaml(self):
        """Test loading YAML manifest file."""
        try:
            import yaml  # noqa: PLC0415
        except ImportError:
            pytest.skip("PyYAML not available")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            manifest_path = temp_path / "manifest.yaml"

            manifest_data = {
                "test_dir": {
                    "type": "directory",
                    "description": "Test directory",
                    "entries": {},
                }
            }

            with open(manifest_path, "w", encoding="utf-8") as f:
                yaml.dump(manifest_data, f)

            result = self.methods._load_manifest(temp_path, "manifest.yaml")

            # Verify the manifest structure and content
            assert isinstance(result, DirectoryManifest)
            test_dir_entry = result.entries["test_dir"]
            assert isinstance(test_dir_entry, ManifestEntry)
            assert test_dir_entry.description == "Test directory"
            assert len(result.entries) == 1  # Should have exactly one entry

    def test_load_manifest_file_not_found(self):
        """Test loading manifest when file doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            with pytest.raises(DataStorageCreationError, match="not found"):
                self.methods._load_manifest(temp_path, "nonexistent.json")

    @patch("edison_client.clients.data_storage_methods._create_directory_zip")
    @patch("edison_client.clients.data_storage_methods._upload_file_multipart")
    def test_upload_data_directory(self, mock_upload, mock_create_zip):
        """Test directory upload as zip collection."""
        mock_create_zip.return_value = 1024  # 1KB zip size

        mock_response = Mock()
        mock_response.json.return_value = self._create_mock_response()
        mock_response.raise_for_status.return_value = None

        self.methods.client.post.return_value = mock_response

        status_response = Mock()
        status_response.json.return_value = self._create_mock_response()
        status_response.json.return_value["data_storage"]["status"] = "active"
        status_response.raise_for_status.return_value = None

        self.methods.client.patch.return_value = status_response

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "test.txt").write_text("test content")

            result = self.methods._upload_data_directory(
                "test_dir", temp_path, "Test directory", None
            )

            assert result.data_storage.id == self.test_uuid
            mock_create_zip.assert_called_once_with(
                temp_path,
                ANY,
                None,
                ".gitignore",
            )
            # Multipart helper takes kwargs: client, entry_id, file_path,
            # file_size, progress_bar.
            mock_upload.assert_called_once_with(
                client=self.methods.client,
                entry_id=self.test_uuid,
                file_path=ANY,
                file_size=ANY,
                progress_bar=ANY,
            )

            # Assert that the path endpoint is called
            self.methods.client.post.assert_called_once_with(
                "/v0.1/data-storage/data-entries",
                json={
                    "name": "test_dir",
                    "description": "Test directory",
                    "file_path": "test_dir.zip",  # The actual path includes .zip extension
                    "is_collection": True,
                    "metadata": {
                        "size": 1024,
                    },
                },
            )

    @patch("edison_client.clients.data_storage_methods._aupload_file_multipart")
    @pytest.mark.asyncio
    async def test_aupload_data_directory(self, mock_upload):
        """Test asynchronous directory upload as zip collection."""
        mock_response = Mock()
        mock_response.json.return_value = self._create_mock_response()
        mock_response.raise_for_status.return_value = None

        # Make the post method return the mock response asynchronously
        self.methods.async_client.post = AsyncMock(return_value=mock_response)

        status_response = Mock()
        status_response.json.return_value = self._create_mock_response()
        status_response.json.return_value["data_storage"]["status"] = "active"
        status_response.raise_for_status.return_value = None

        self.methods.async_client.patch.return_value = status_response

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "test.txt").write_text("test content")

            result = await self.methods._aupload_data_directory(
                "test_dir", temp_path, "Test directory", None
            )

            assert result.data_storage.id == self.test_uuid
            mock_upload.assert_called_once_with(
                client=self.methods.async_client,
                entry_id=self.test_uuid,
                file_path=ANY,
                file_size=ANY,
                progress_bar=ANY,
            )

            # Assert that the path endpoint is called
            self.methods.async_client.post.assert_called_once_with(
                "/v0.1/data-storage/data-entries",
                json={
                    "name": "test_dir",
                    "description": "Test directory",
                    "file_path": "test_dir.zip",  # The actual path includes .zip extension
                    "is_collection": True,
                    "metadata": {
                        "size": ANY,  # Zip file size may vary
                    },
                },
            )

    def test_store_text_content_success(self):
        """Test successful text content storage."""
        mock_response = Mock()
        mock_response.json.return_value = self._create_mock_response(
            storage_type="raw_content", signed_url=None
        )
        mock_response.raise_for_status.return_value = None

        self.methods.client.post.return_value = mock_response

        result = self.methods.store_text_content(
            "test", "test content", "Test description", project_id=self.test_project_id
        )

        assert result.data_storage.id == self.test_uuid
        # Verify the API call was made with the correct endpoint and data
        self.methods.client.post.assert_called_once()
        call_args = self.methods.client.post.call_args
        assert call_args[0][0] == "/v0.1/data-storage/data-entries"

        # Verify the JSON payload contains the expected fields
        json_data = call_args[1]["json"]
        assert json_data["name"] == "test"
        assert json_data["content"] == "test content"
        assert json_data["description"] == "Test description"
        assert json_data["is_collection"] is False
        assert json_data["project_id"] == str(self.test_project_id)

    def test_store_text_content_http_error(self):
        """Test text content storage with HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "Access denied"

        error = HTTPStatusError("Forbidden", request=Mock(), response=mock_response)
        self.methods.client.post.side_effect = error

        with pytest.raises(DataStorageError, match="not authorized"):
            self.methods.store_text_content("test", "test content")

    @pytest.mark.asyncio
    async def test_astore_text_content_success(self):
        """Test successful asynchronous text content storage."""
        mock_response = Mock()
        mock_response.json.return_value = self._create_mock_response(
            storage_type="raw_content", signed_url=None
        )
        mock_response.raise_for_status.return_value = None

        # Make the post method return the mock response asynchronously
        self.methods.async_client.post = AsyncMock(return_value=mock_response)

        result = await self.methods.astore_text_content(
            "test", "test content", "Test description", project_id=self.test_project_id
        )

        assert result.data_storage.id == self.test_uuid
        # Verify the API call was made with the correct endpoint and data
        self.methods.async_client.post.assert_called_once()
        call_args = self.methods.async_client.post.call_args
        assert call_args[0][0] == "/v0.1/data-storage/data-entries"

        # Verify the JSON payload contains the expected fields
        json_data = call_args[1]["json"]
        assert json_data["name"] == "test"
        assert json_data["content"] == "test content"
        assert json_data["description"] == "Test description"
        assert json_data["is_collection"] is False
        assert json_data["project_id"] == str(self.test_project_id)

    @patch("edison_client.clients.data_storage_methods._upload_file_multipart")
    def test_store_file_content_single_file(self, mock_upload):
        """Test single file content storage."""
        mock_response = Mock()
        mock_response.json.return_value = self._create_mock_response()
        mock_response.raise_for_status.return_value = None

        self.methods.client.post.return_value = mock_response

        status_response = Mock()
        status_response.json.return_value = self._create_mock_response()
        status_response.json.return_value["data_storage"]["status"] = "active"
        status_response.raise_for_status.return_value = None

        self.methods.client.patch.return_value = status_response

        with tempfile.NamedTemporaryFile(suffix=".bin") as temp_file:
            temp_file.write(b"test binary content")
            temp_file.flush()

            result = self.methods.store_file_content(
                "test.bin", temp_file.name, "Test file", project_id=self.test_project_id
            )

            assert result.data_storage.id == self.test_uuid
            mock_upload.assert_called_once_with(
                client=self.methods.client,
                entry_id=self.test_uuid,
                file_path=ANY,
                file_size=ANY,
                progress_bar=ANY,
            )

            # Assert that the POST endpoint is called with size metadata
            self.methods.client.post.assert_called_once_with(
                "/v0.1/data-storage/data-entries",
                json={
                    "name": "test.bin",
                    "description": "Test file",
                    "file_path": ANY,  # Temporary file path varies
                    "is_collection": False,
                    "metadata": {
                        "size": ANY,  # File size in bytes
                    },
                    "project_id": str(self.test_project_id),
                },
            )

    @patch("edison_client.clients.data_storage_methods._upload_file_multipart")
    def test_store_file_content_with_embedding(self, mock_upload):
        """Test file content storage with embedding vector."""
        mock_response = Mock()
        mock_response.json.return_value = self._create_mock_response()
        mock_response.raise_for_status.return_value = None

        self.methods.client.post.return_value = mock_response

        status_response = Mock()
        status_response.json.return_value = self._create_mock_response()
        status_response.json.return_value["data_storage"]["status"] = "active"
        status_response.raise_for_status.return_value = None

        self.methods.client.patch.return_value = status_response

        test_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]

        with tempfile.NamedTemporaryFile(suffix=".bin") as temp_file:
            temp_file.write(b"test binary content")
            temp_file.flush()

            result = self.methods.store_file_content(
                "test.bin",
                temp_file.name,
                "Test file",
                project_id=self.test_project_id,
                embedding=test_embedding,
            )

            assert result.data_storage.id == self.test_uuid

            # Assert that the POST endpoint is called with embedding
            call_args = self.methods.client.post.call_args
            assert call_args[1]["json"]["embedding"] == test_embedding

    @patch("edison_client.clients.data_storage_methods._upload_file_multipart")
    def test_store_file_content_directory_collection(self, mock_upload):
        """Test directory content storage as collection."""
        mock_response = Mock()
        mock_response.json.return_value = self._create_mock_response()
        mock_response.raise_for_status.return_value = None

        self.methods.client.post.return_value = mock_response

        status_response = Mock()
        status_response.json.return_value = self._create_mock_response()
        status_response.json.return_value["data_storage"]["status"] = "active"
        status_response.raise_for_status.return_value = None

        self.methods.client.patch.return_value = status_response

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "test.txt").write_text("test content")

            result = self.methods.store_file_content(
                "test_dir",
                temp_path,
                "Test directory",
                as_collection=True,
                project_id=self.test_project_id,
            )

            assert result.data_storage.id == self.test_uuid
            mock_upload.assert_called_once_with(
                client=self.methods.client,
                entry_id=self.test_uuid,
                file_path=ANY,
                file_size=ANY,
                progress_bar=ANY,
            )

            # Assert that the POST endpoint is called with size metadata
            self.methods.client.post.assert_called_once_with(
                "/v0.1/data-storage/data-entries",
                json={
                    "name": "test_dir",
                    "description": "Test directory",
                    "file_path": "test_dir.zip",
                    "is_collection": True,
                    "metadata": {
                        "size": ANY,  # Zip file size may vary
                    },
                    "project_id": str(self.test_project_id),
                },
            )

    def test_register_existing_data_source_success(self):
        """Test successful registration of existing data source."""
        mock_response = Mock()
        mock_response.json.return_value = self._create_mock_response(signed_url=None)
        mock_response.raise_for_status.return_value = None

        self.methods.client.post.return_value = mock_response

        existing_location = DataStorageLocationPayload(
            storage_type="bigquery", content_type="bq_table"
        )

        result = self.methods.register_existing_data_source(
            "test",
            existing_location,
            "Test description",
            project_id=self.test_project_id,
        )

        assert result.data_storage.id == self.test_uuid
        # Verify the API call was made with the correct endpoint and data
        self.methods.client.post.assert_called_once()
        call_args = self.methods.client.post.call_args
        assert call_args[0][0] == "/v0.1/data-storage/data-entries"

        # Verify the JSON payload contains the expected fields
        json_data = call_args[1]["json"]
        assert json_data["name"] == "test"
        assert json_data["description"] == "Test description"
        assert json_data["is_collection"] is False
        assert json_data["project_id"] == self.test_project_id
        assert "existing_location" in json_data
        assert json_data["existing_location"]["storage_type"] == "bigquery"
        assert json_data["existing_location"]["content_type"] == "bq_table"

    @pytest.mark.asyncio
    async def test_aregister_existing_data_source_success(self):
        """Test successful asynchronous registration of existing data source."""
        mock_response = Mock()
        mock_response.json.return_value = self._create_mock_response(signed_url=None)
        mock_response.raise_for_status.return_value = None

        # Make the post method return the mock response asynchronously
        self.methods.async_client.post = AsyncMock(return_value=mock_response)

        existing_location = DataStorageLocationPayload(
            storage_type="bigquery", content_type="bq_table"
        )

        result = await self.methods.aregister_existing_data_source(
            name="test",
            existing_location=existing_location,
            description="Test description",
            as_collection=False,
            project_id=self.test_project_id,
        )

        assert result.data_storage.id == self.test_uuid
        # Verify the API call was made with the correct endpoint and data
        self.methods.async_client.post.assert_called_once()
        call_args = self.methods.async_client.post.call_args
        assert call_args[0][0] == "/v0.1/data-storage/data-entries"

        # Verify the JSON payload contains the expected fields
        json_data = call_args[1]["json"]
        assert json_data["name"] == "test"
        assert json_data["description"] == "Test description"
        assert json_data["project_id"] == self.test_project_id
        assert "existing_location" in json_data
        assert json_data["existing_location"]["storage_type"] == "bigquery"
        assert json_data["existing_location"]["content_type"] == "bq_table"

    @patch("edison_client.clients.data_storage_methods.requests_lib.get")
    def test_fetch_data_from_storage_gcs(self, mock_get):
        """Test fetching data from GCS storage."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"content-disposition": 'filename="test.txt"'}
        mock_response.iter_content.return_value = [b"test content"]
        mock_get.return_value.__enter__.return_value = mock_response

        api_response = Mock()
        api_response.json.return_value = self._create_mock_response()
        api_response.raise_for_status.return_value = None

        self.methods.client.get.return_value = api_response

        result = self.methods.fetch_data_from_storage(self.test_uuid)

        # Verify GCS data fetching returns a valid file path
        assert result is not None
        assert isinstance(result, Path)
        assert result.name == "test.txt"
        assert result.suffix == ".txt"
        assert result.exists()  # File should exist after download

    def test_fetch_data_from_storage_raw_content(self):
        """Test fetching data from raw content storage."""
        api_response = Mock()
        api_response.json.return_value = self._create_mock_response(
            storage_type="raw_content", signed_url=None, content="test content"
        )
        api_response.raise_for_status.return_value = None

        self.methods.client.get.return_value = api_response

        result = self.methods.fetch_data_from_storage(self.test_uuid)

        # Verify raw content storage returns the content directly
        assert isinstance(result, RawFetchResponse)
        assert result.content == "test content"
        assert result.entry_id == self.test_uuid
        assert result.entry_name == "test"

    def test_fetch_data_from_storage_no_id(self):
        """Test fetching data without providing storage ID."""
        with pytest.raises(DataStorageRetrievalError, match="must be provided"):
            self.methods.fetch_data_from_storage(None)

    def test_fetch_data_from_storage_unsupported_type(self):
        """Test fetching data from unsupported storage type."""
        api_response = Mock()
        api_response.json.return_value = self._create_mock_response(
            storage_type="unsupported", signed_url=None
        )
        api_response.raise_for_status.return_value = None

        self.methods.client.get.return_value = api_response

        with pytest.raises(DataStorageRetrievalError, match="Unsupported storage type"):
            self.methods.fetch_data_from_storage(self.test_uuid)

    @pytest.mark.asyncio
    async def test_afetch_data_from_storage_gcs(self, monkeypatch):
        """Test asynchronous fetching data from GCS storage."""

        async def mock_download(*args, **kwargs):
            with tempfile.NamedTemporaryFile(suffix=".txt") as temp_file:
                temp_file.write(b"test content")
                temp_file.flush()
                return Path(temp_file.name)

        monkeypatch.setattr(self.methods, "_adownload_from_gcs", mock_download)

        api_response = Mock()
        api_response.json.return_value = self._create_mock_response()
        api_response.raise_for_status.return_value = None

        # Make the get method return the mock response asynchronously
        self.methods.async_client.get = AsyncMock(return_value=api_response)

        result = await self.methods.afetch_data_from_storage(self.test_uuid)

        # Verify async GCS data fetching returns a valid file path
        assert result is not None
        assert isinstance(result, Path)
        assert result.suffix == ".txt"
        assert result.name.endswith(".txt")  # Should have .txt extension
        # Note: File existence check removed as it's a temporary file that may be cleaned up

    @pytest.mark.asyncio
    async def test_aget_data_storage_status(self):
        """Test asynchronously checking the status of a data storage entry."""
        api_response = Mock()
        api_response.json.return_value = {
            "id": str(self.test_uuid),
            "status": "active",
        }
        api_response.raise_for_status.return_value = None
        self.methods.async_client.get = AsyncMock(return_value=api_response)

        result = await self.methods.aget_data_storage_status(self.test_uuid)

        assert result.id == self.test_uuid
        assert result.status == DataStorageEntryStatus.ACTIVE
        self.methods.async_client.get.assert_awaited_once_with(
            f"/v0.1/data-storage/data-entries/{self.test_uuid}/status"
        )

    @pytest.mark.asyncio
    async def test_aget_data_storage_status_http_error(self):
        """Test that HTTP errors surface as DataStorageError."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        error = HTTPStatusError("Not Found", request=Mock(), response=mock_response)

        api_response = Mock()
        api_response.raise_for_status.side_effect = error
        self.methods.async_client.get = AsyncMock(return_value=api_response)

        with pytest.raises(DataStorageError, match="checking status of"):
            await self.methods.aget_data_storage_status(self.test_uuid)

    def test_upload_directory_hierarchically(self):
        """Test hierarchical directory upload."""
        mock_response = Mock()
        mock_response.json.return_value = self._create_mock_response(signed_url=None)
        mock_response.json.return_value["data_storage"]["dataset_id"] = str(uuid4())
        mock_response.raise_for_status.return_value = None

        self.methods.client.post.return_value = mock_response

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "file1.txt").write_text("content1")
            (temp_path / "subdir").mkdir()
            (temp_path / "subdir" / "file2.txt").write_text("content2")

            result = self.methods._upload_directory_hierarchically(
                "test_dir",
                temp_path,
                "Test description",
                project_id=self.test_project_id,
            )

            # Verify the result structure and content
            assert isinstance(result, list)
            assert len(result) >= 2  # Should have at least 2 responses
            assert all(isinstance(r, DataStorageResponse) for r in result)

            # Verify the responses have the expected structure
            for response in result:
                assert hasattr(response, "data_storage")
                assert hasattr(response.data_storage, "name")
                assert hasattr(response.data_storage, "description")
                assert hasattr(response.data_storage, "id")

    @pytest.mark.asyncio
    async def test_aupload_directory_hierarchically(self):
        """Test asynchronous hierarchical directory upload."""
        mock_response = Mock()
        mock_response.json.return_value = self._create_mock_response(signed_url=None)
        mock_response.json.return_value["data_storage"]["dataset_id"] = str(uuid4())
        mock_response.raise_for_status.return_value = None

        # Make the post method return the mock response asynchronously
        self.methods.async_client.post = AsyncMock(return_value=mock_response)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            (temp_path / "file1.txt").write_text("content1")
            (temp_path / "subdir").mkdir()
            (temp_path / "subdir" / "file2.txt").write_text("content2")

            result = await self.methods._aupload_directory_hierarchically(
                "test_dir",
                temp_path,
                "Test description",
                project_id=self.test_project_id,
            )

            # Verify the result structure and content
            assert isinstance(result, list)
            assert len(result) >= 2  # Should have at least 2 responses
            assert all(isinstance(r, DataStorageResponse) for r in result)

            # Verify the responses have the expected structure
            for response in result:
                assert hasattr(response, "data_storage")
                assert hasattr(response.data_storage, "name")
                assert hasattr(response.data_storage, "description")
                assert hasattr(response.data_storage, "id")

    @pytest.mark.asyncio
    async def test_acreate_dataset_success(self):
        """Test successful asynchronous dataset creation."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": str(self.test_uuid),
            "name": "test_dataset",
            "description": "Test dataset description",
            "user_id": "test_user_123",
        }
        mock_response.raise_for_status.return_value = None

        # Make the post method return the mock response asynchronously
        self.methods.async_client.post = AsyncMock(return_value=mock_response)

        result = await self.methods.acreate_dataset(
            name="test_dataset",
            description="Test dataset description",
        )

        # Verify the result structure and content
        assert result is not None
        # Verify the API call was made with the correct endpoint and data
        self.methods.async_client.post.assert_called_once()
        call_args = self.methods.async_client.post.call_args
        assert call_args[0][0] == "/v0.1/data-storage/datasets"

        # Verify the JSON payload contains the expected fields
        json_data = call_args[1]["json"]
        assert json_data["name"] == "test_dataset"
        assert json_data["description"] == "Test dataset description"
        assert "id" not in json_data  # Should not be included when None

    @pytest.mark.asyncio
    async def test_acreate_dataset_with_id_success(self):
        """Test successful asynchronous dataset creation with custom ID."""
        custom_dataset_id = uuid4()
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": str(custom_dataset_id),
            "name": "test_dataset",
            "description": "Test dataset description",
            "user_id": "test_user_123",
        }
        mock_response.raise_for_status.return_value = None

        # Make the post method return the mock response asynchronously
        self.methods.async_client.post = AsyncMock(return_value=mock_response)

        result = await self.methods.acreate_dataset(
            name="test_dataset",
            description="Test dataset description",
            dataset_id=custom_dataset_id,
        )

        # Verify the result structure and content
        assert result is not None
        # Verify the API call was made with the correct endpoint and data
        self.methods.async_client.post.assert_called_once()
        call_args = self.methods.async_client.post.call_args
        assert call_args[0][0] == "/v0.1/data-storage/datasets"

        # Verify the JSON payload contains the expected fields including custom ID
        json_data = call_args[1]["json"]
        assert json_data["name"] == "test_dataset"
        assert json_data["description"] == "Test dataset description"
        assert json_data["id"] == custom_dataset_id

    @pytest.mark.asyncio
    async def test_acreate_dataset_http_error(self):
        """Test dataset creation with HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "Access denied"

        error = HTTPStatusError("Forbidden", request=Mock(), response=mock_response)
        self.methods.async_client.post = AsyncMock(side_effect=error)

        with pytest.raises(DataStorageError, match="not authorized"):
            await self.methods.acreate_dataset(
                name="test_dataset",
                description="Test dataset description",
            )

    @pytest.mark.asyncio
    async def test_acreate_dataset_unexpected_error(self):
        """Test dataset creation with unexpected error."""
        unexpected_error = ValueError("Unexpected error")
        self.methods.async_client.post = AsyncMock(side_effect=unexpected_error)

        with pytest.raises(
            DataStorageCreationError, match="An unexpected error occurred"
        ):
            await self.methods.acreate_dataset(
                name="test_dataset",
                description="Test description",
            )

    @pytest.mark.asyncio
    async def test_adelete_dataset_success(self):
        """Test successful asynchronous dataset deletion."""
        # Make the delete method return successfully
        self.methods.async_client.delete = AsyncMock()

        dataset_id = uuid4()
        await self.methods.adelete_dataset(dataset_id)

        # Verify the API call was made with the correct endpoint
        self.methods.async_client.delete.assert_called_once_with(
            f"/v0.1/data-storage/datasets/{dataset_id}"
        )

    @pytest.mark.asyncio
    async def test_adelete_dataset_http_error(self):
        """Test dataset deletion with HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Dataset not found"

        error = HTTPStatusError("Not Found", request=Mock(), response=mock_response)
        self.methods.async_client.delete = AsyncMock(side_effect=error)

        dataset_id = uuid4()
        with pytest.raises(DataStorageError, match="Dataset not found"):
            await self.methods.adelete_dataset(dataset_id)

    @pytest.mark.asyncio
    async def test_adelete_dataset_unexpected_error(self):
        """Test dataset deletion with unexpected error."""
        unexpected_error = ValueError("Unexpected error")
        self.methods.async_client.delete = AsyncMock(side_effect=unexpected_error)

        dataset_id = uuid4()
        with pytest.raises(DataStorageError, match="An unexpected error occurred"):
            await self.methods.adelete_dataset(dataset_id)

    @pytest.mark.asyncio
    async def test_aget_dataset_success(self):
        """Test successful asynchronous dataset retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "dataset": {
                "id": str(self.test_uuid),
                "name": "test_dataset",
                "description": "Test dataset description",
                "user_id": "test_user_123",
                "created_at": "2024-01-01T00:00:00Z",
                "modified_at": "2024-01-01T00:00:00Z",
            },
            "data_storage_entries": [
                {
                    "id": str(uuid4()),
                    "name": "test_entry",
                    "description": "Test entry description",
                    "content": "Test content",
                    "embedding": None,
                    "is_collection": False,
                    "status": "active",
                    "tags": None,
                    "parent_id": None,
                    "project_id": str(self.test_project_id),
                    "dataset_id": str(self.test_uuid),
                    "path": None,
                    "bigquery_schema": None,
                    "user_id": "test_user_123",
                    "created_at": "2024-01-01T00:00:00Z",
                    "modified_at": "2024-01-01T00:00:00Z",
                    "share_status": "private",
                }
            ],
        }
        mock_response.raise_for_status.return_value = None

        # Make the get method return the mock response asynchronously
        self.methods.async_client.get = AsyncMock(return_value=mock_response)

        dataset_id = uuid4()
        result = await self.methods.aget_dataset(dataset_id)

        # Verify the result structure and content
        assert result is not None
        assert result.dataset.id == self.test_uuid
        assert result.dataset.name == "test_dataset"
        assert result.dataset.description == "Test dataset description"
        assert result.dataset.user_id == "test_user_123"

        # Verify data storage entries
        assert len(result.data_storage_entries) == 1
        assert result.data_storage_entries[0].name == "test_entry"
        assert result.data_storage_entries[0].description == "Test entry description"
        assert result.data_storage_entries[0].content == "Test content"
        assert result.data_storage_entries[0].dataset_id == self.test_uuid

        # Verify the API call was made with the correct endpoint
        self.methods.async_client.get.assert_called_once_with(
            f"/v0.1/data-storage/datasets/{dataset_id}"
        )

    @pytest.mark.asyncio
    async def test_aget_dataset_http_error(self):
        """Test dataset retrieval with HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Dataset not found"

        error = HTTPStatusError("Not Found", request=Mock(), response=mock_response)
        self.methods.async_client.get = AsyncMock(side_effect=error)

        dataset_id = uuid4()
        with pytest.raises(DataStorageError, match="Dataset not found"):
            await self.methods.aget_dataset(dataset_id)

    @pytest.mark.asyncio
    async def test_aget_dataset_unexpected_error(self):
        """Test dataset retrieval with unexpected error."""
        unexpected_error = ValueError("Unexpected error")
        self.methods.async_client.get = AsyncMock(side_effect=unexpected_error)

        dataset_id = uuid4()
        with pytest.raises(DataStorageError, match="An unexpected error occurred"):
            await self.methods.aget_dataset(dataset_id)

    @pytest.mark.asyncio
    async def test_adelete_data_storage_entry_success(self):
        """Test successful asynchronous data storage entry deletion."""
        # Make the delete method return successfully
        self.methods.async_client.delete = AsyncMock()

        entry_id = uuid4()
        await self.methods.adelete_data_storage_entry(entry_id)

        # Verify the API call was made with the correct endpoint
        self.methods.async_client.delete.assert_called_once_with(
            f"/v0.1/data-storage/data-entries/{entry_id}"
        )

    @pytest.mark.asyncio
    async def test_adelete_data_storage_entry_http_error(self):
        """Test data storage entry deletion with HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "Access denied"

        error = HTTPStatusError("Forbidden", request=Mock(), response=mock_response)
        self.methods.async_client.delete = AsyncMock(side_effect=error)

        entry_id = uuid4()
        with pytest.raises(DataStorageError, match="not authorized"):
            await self.methods.adelete_data_storage_entry(entry_id)

    @pytest.mark.asyncio
    async def test_adelete_data_storage_entry_unexpected_error(self):
        """Test data storage entry deletion with unexpected error."""
        unexpected_error = ValueError("Unexpected error")
        self.methods.async_client.delete = AsyncMock(side_effect=unexpected_error)

        entry_id = uuid4()
        with pytest.raises(DataStorageError, match="An unexpected error occurred"):
            await self.methods.adelete_data_storage_entry(entry_id)

    @pytest.mark.asyncio
    async def test_acreate_dataset_minimal_payload(self):
        """Test dataset creation with minimal required fields."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": str(self.test_uuid),
            "name": "minimal_dataset",
            "user_id": "test_user_123",
        }
        mock_response.raise_for_status.return_value = None

        # Make the post method return the mock response asynchronously
        self.methods.async_client.post = AsyncMock(return_value=mock_response)

        result = await self.methods.acreate_dataset(name="minimal_dataset")

        # Verify the result structure and content
        assert result is not None
        # Verify the API call was made with the correct endpoint and data
        self.methods.async_client.post.assert_called_once()
        call_args = self.methods.async_client.post.call_args
        assert call_args[0][0] == "/v0.1/data-storage/datasets"

        # Verify the JSON payload contains only the required fields
        json_data = call_args[1]["json"]
        assert json_data["name"] == "minimal_dataset"
        assert "description" not in json_data
        assert "id" not in json_data

    @pytest.mark.asyncio
    async def test_acreate_dataset_validation_error(self):
        """Test dataset creation with validation error."""
        mock_response = Mock()
        mock_response.status_code = 422
        mock_response.text = "Validation failed"

        error = HTTPStatusError(
            "Unprocessable Entity", request=Mock(), response=mock_response
        )
        self.methods.async_client.post = AsyncMock(side_effect=error)

        with pytest.raises(DataStorageError, match="Invalid request payload"):
            await self.methods.acreate_dataset(
                name="",  # Invalid empty name
                description="Test description",
            )

    @pytest.mark.asyncio
    async def test_adelete_dataset_not_found(self):
        """Test dataset deletion when dataset doesn't exist."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Dataset not found"

        error = HTTPStatusError("Not Found", request=Mock(), response=mock_response)
        self.methods.async_client.delete = AsyncMock(side_effect=error)

        dataset_id = uuid4()
        with pytest.raises(DataStorageError, match="Dataset not found"):
            await self.methods.adelete_dataset(dataset_id)

    @pytest.mark.asyncio
    async def test_adelete_data_storage_entry_not_found(self):
        """Test data storage entry deletion when entry doesn't exist."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Data storage entry not found"

        error = HTTPStatusError("Not Found", request=Mock(), response=mock_response)
        self.methods.async_client.delete = AsyncMock(side_effect=error)

        entry_id = uuid4()
        with pytest.raises(DataStorageError, match="Data storage entry not found"):
            await self.methods.adelete_data_storage_entry(entry_id)

    def test_get_dataset_success(self):
        """Test successful synchronous dataset retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "dataset": {
                "id": str(self.test_uuid),
                "name": "test_dataset",
                "description": "Test dataset description",
                "user_id": "test_user_123",
                "created_at": "2024-01-01T00:00:00Z",
                "modified_at": "2024-01-01T00:00:00Z",
            },
            "data_storage_entries": [
                {
                    "id": str(uuid4()),
                    "name": "test_entry",
                    "description": "Test entry description",
                    "content": "Test content",
                    "embedding": None,
                    "is_collection": False,
                    "status": "active",
                    "tags": None,
                    "parent_id": None,
                    "project_id": str(self.test_project_id),
                    "dataset_id": str(self.test_uuid),
                    "path": None,
                    "bigquery_schema": None,
                    "user_id": "test_user_123",
                    "created_at": "2024-01-01T00:00:00Z",
                    "modified_at": "2024-01-01T00:00:00Z",
                    "share_status": "private",
                }
            ],
        }
        mock_response.raise_for_status.return_value = None

        # Make the get method return the mock response
        self.methods.client.get = Mock(return_value=mock_response)

        dataset_id = uuid4()
        result = self.methods.get_dataset(dataset_id)

        # Verify the result structure and content
        assert result is not None
        assert result.dataset.id == self.test_uuid
        assert result.dataset.name == "test_dataset"
        assert result.dataset.description == "Test dataset description"
        assert result.dataset.user_id == "test_user_123"

        # Verify data storage entries
        assert len(result.data_storage_entries) == 1
        assert result.data_storage_entries[0].name == "test_entry"
        assert result.data_storage_entries[0].description == "Test entry description"
        assert result.data_storage_entries[0].content == "Test content"
        assert result.data_storage_entries[0].dataset_id == self.test_uuid

        # Verify the API call was made with the correct endpoint
        self.methods.client.get.assert_called_once_with(
            f"/v0.1/data-storage/datasets/{dataset_id}"
        )

    def test_get_dataset_http_error(self):
        """Test synchronous dataset retrieval with HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Dataset not found"

        error = HTTPStatusError("Not Found", request=Mock(), response=mock_response)
        self.methods.client.get = Mock(side_effect=error)

        dataset_id = uuid4()
        with pytest.raises(DataStorageError, match="Dataset not found"):
            self.methods.get_dataset(dataset_id)

    def test_get_dataset_unexpected_error(self):
        """Test synchronous dataset retrieval with unexpected error."""
        unexpected_error = ValueError("Unexpected error")
        self.methods.client.get = Mock(side_effect=unexpected_error)

        dataset_id = uuid4()
        with pytest.raises(DataStorageError, match="An unexpected error occurred"):
            self.methods.get_dataset(dataset_id)

    def test_get_dataset_empty_response(self):
        """Test synchronous dataset retrieval with minimal response."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "dataset": {
                "id": str(uuid4()),
                "name": "",
                "user_id": "test_user_123",
                "created_at": "2024-01-01T00:00:00Z",
                "modified_at": "2024-01-01T00:00:00Z",
            },
            "data_storage_entries": [],
        }
        mock_response.raise_for_status.return_value = None

        # Make the get method return the mock response
        self.methods.client.get = Mock(return_value=mock_response)

        dataset_id = uuid4()
        result = self.methods.get_dataset(dataset_id)

        # Verify the result structure
        assert result is not None
        assert result.dataset.id is not None
        assert not result.dataset.name
        assert result.dataset.user_id == "test_user_123"
        assert result.data_storage_entries == []
        assert len(result.data_storage_entries) == 0

        # Verify the API call was made with the correct endpoint
        self.methods.client.get.assert_called_once_with(
            f"/v0.1/data-storage/datasets/{dataset_id}"
        )


class TestUtilityFunctions:
    """Test cases for utility functions."""

    def test_should_ignore_file_no_patterns(self):
        """Test file ignoring when no patterns are provided."""
        from edison_client.clients.data_storage_methods import (  # noqa: PLC0415
            _should_ignore_file,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            test_file = temp_path / "test.txt"
            test_file.write_text("test")

            result = _should_ignore_file(test_file, temp_path, None)
            assert result is False

    def test_should_ignore_file_with_patterns(self):
        """Test file ignoring with specific patterns."""
        from edison_client.clients.data_storage_methods import (  # noqa: PLC0415
            _should_ignore_file,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            test_file = temp_path / "test.txt"
            test_file.write_text("test")

            # Test ignoring by filename pattern
            result = _should_ignore_file(test_file, temp_path, ["*.txt"])
            assert result is True

            # Test ignoring by specific name
            result = _should_ignore_file(test_file, temp_path, ["test.txt"])
            assert result is True

    def test_read_ignore_file_exists(self):
        """Test reading ignore file when it exists."""
        from edison_client.clients.data_storage_methods import (  # noqa: PLC0415
            _read_ignore_file,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            ignore_file = temp_path / ".gitignore"
            ignore_file.write_text("*.log\n*.tmp\nnode_modules/")

            result = _read_ignore_file(temp_path)

            # Verify the ignore patterns are correctly read
            assert isinstance(result, list)
            assert len(result) == 3  # Should have exactly 3 patterns
            assert "*.log" in result
            assert "*.tmp" in result
            assert "node_modules/" in result
            # Verify no empty lines or comments are included
            assert all(pattern.strip() for pattern in result)
            assert not any(pattern.startswith("#") for pattern in result)

    def test_read_ignore_file_not_exists(self):
        """Test reading ignore file when it doesn't exist."""
        from edison_client.clients.data_storage_methods import (  # noqa: PLC0415
            _read_ignore_file,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            result = _read_ignore_file(temp_path)

            # Verify empty ignore file returns empty list
            assert isinstance(result, list)
            assert result == []
            assert len(result) == 0
            assert not result  # Should be falsy

    def test_collect_ignore_patterns(self):
        """Test collecting ignore patterns from multiple sources."""
        from edison_client.clients.data_storage_methods import (  # noqa: PLC0415
            _collect_ignore_patterns,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            ignore_file = temp_path / ".gitignore"
            ignore_file.write_text("*.log\n*.tmp")

            result = _collect_ignore_patterns(temp_path, ["custom_pattern"])

            # Verify all expected patterns are collected
            assert isinstance(result, list)
            assert len(result) >= 5  # At least 2 from file + 1 custom + 2 default
            assert "*.log" in result
            assert "*.tmp" in result
            assert "custom_pattern" in result
            assert ".git" in result  # Default ignore
            assert "__pycache__" in result  # Default ignore

            # Verify patterns are unique and properly formatted
            assert len(result) == len(set(result))  # No duplicates
            assert all(isinstance(pattern, str) for pattern in result)

    def test_should_send_as_text_content_small_file(self):
        """Test text content detection for small files."""
        from edison_client.clients.data_storage_methods import (  # noqa: PLC0415
            _should_send_as_text_content,
        )

        with tempfile.NamedTemporaryFile(suffix=".txt") as temp_file:
            temp_file.write(b"small content")
            temp_file.flush()

            file_path = Path(temp_file.name)
            file_size = file_path.stat().st_size

            result = _should_send_as_text_content(file_path, file_size)

            # Verify the file size threshold logic
            assert isinstance(result, bool)
            assert result is True
            assert file_size < 10 * 1024 * 1024  # Should be under 10MB threshold
            assert file_path.suffix.lower() in {
                ".txt",
                ".md",
                ".csv",
                ".json",
                ".yaml",
                ".yml",
            }

    def test_should_send_as_text_content_large_file(self):
        """Test text content detection for large files."""
        from edison_client.clients.data_storage_methods import (  # noqa: PLC0415
            _should_send_as_text_content,
        )

        with tempfile.NamedTemporaryFile(suffix=".txt") as temp_file:
            # Write enough data to exceed the threshold
            temp_file.write(b"0" * (11 * 1024 * 1024))  # 11MB
            temp_file.flush()

            file_path = Path(temp_file.name)
            file_size = file_path.stat().st_size

            result = _should_send_as_text_content(file_path, file_size)

            # Verify the file size threshold logic for large files
            assert isinstance(result, bool)
            assert result is False
            assert file_size > 10 * 1024 * 1024  # Should be over 10MB threshold
            assert file_size == 11 * 1024 * 1024  # Exactly 11MB as written

    def test_should_send_as_text_content_unsupported_extension(self):
        """Test text content detection for unsupported file types."""
        from edison_client.clients.data_storage_methods import (  # noqa: PLC0415
            _should_send_as_text_content,
        )

        with tempfile.NamedTemporaryFile(suffix=".bin") as temp_file:
            temp_file.write(b"binary content")
            temp_file.flush()

            file_path = Path(temp_file.name)
            file_size = file_path.stat().st_size

            result = _should_send_as_text_content(file_path, file_size)

            # Verify unsupported file types are rejected regardless of size
            assert isinstance(result, bool)
            assert result is False
            assert file_path.suffix.lower() not in {
                ".txt",
                ".md",
                ".csv",
                ".json",
                ".yaml",
                ".yml",
            }
            assert file_path.suffix.lower() == ".bin"

    def test_extract_text_from_file_success(self):
        """Test successful text extraction from file."""
        from edison_client.clients.data_storage_methods import (  # noqa: PLC0415
            _extract_text_from_file,
        )

        with tempfile.NamedTemporaryFile(
            encoding="utf-8", suffix=".txt", mode="w"
        ) as temp_file:
            temp_file.write("test content")
            temp_file.flush()

            file_path = Path(temp_file.name)
            result = _extract_text_from_file(file_path)

            # Verify text extraction works correctly
            assert isinstance(result, str)
            assert result == "test content"
            assert len(result) == 12  # "test content" is 12 characters
            assert result.strip() == result  # No leading/trailing whitespace

    def test_extract_text_from_file_unsupported_extension(self):
        """Test text extraction from unsupported file type."""
        from edison_client.clients.data_storage_methods import (  # noqa: PLC0415
            _extract_text_from_file,
        )

        with tempfile.NamedTemporaryFile(suffix=".bin") as temp_file:
            temp_file.write(b"binary content")
            temp_file.flush()

            file_path = Path(temp_file.name)
            result = _extract_text_from_file(file_path)

            # Verify unsupported file types return None
            assert result is None
            assert file_path.suffix.lower() not in {
                ".txt",
                ".md",
                ".csv",
                ".json",
                ".yaml",
                ".yml",
            }
            assert file_path.suffix.lower() == ".bin"

    def test_extract_text_from_file_read_error(self):
        """Test text extraction when file read fails."""
        from edison_client.clients.data_storage_methods import (  # noqa: PLC0415
            _extract_text_from_file,
        )

        # Create a file path that will cause a read error
        file_path = Path("/nonexistent/file.txt")

        result = _extract_text_from_file(file_path)

        # Verify file read errors return None
        assert result is None
        assert not file_path.exists()  # File should not exist
        assert str(file_path) == "/nonexistent/file.txt"  # Verify the path


class TestExceptions:
    """Test cases for custom exceptions."""

    def test_exception_inheritance(self):
        """Test exception class inheritance hierarchy."""
        # Verify the exception class hierarchy is correct
        assert issubclass(DataStorageError, RestClientError)
        assert issubclass(DataStorageCreationError, DataStorageError)
        assert issubclass(DataStorageRetrievalError, DataStorageError)
        assert issubclass(
            DataStorageError, Exception
        )  # Should inherit from base Exception
        assert DataStorageError != RestClientError  # Should be different classes

    def test_exception_creation(self):
        """Test exception creation and message."""
        error = DataStorageCreationError("Test error message")

        # Verify exception creation and string representation
        assert isinstance(error, DataStorageCreationError)
        assert isinstance(error, DataStorageError)
        assert isinstance(error, Exception)
        assert str(error) == "Test error message"
        assert len(str(error)) == 18  # "Test error message" is 18 characters
        assert "Test error message" in str(error)

    def test_exception_with_cause(self):
        """Test exception creation with cause."""
        original_error = ValueError("Original error")
        error = DataStorageCreationError("Test error")
        error.__cause__ = original_error

        # Verify exception cause is properly set
        assert error.__cause__ == original_error
        assert isinstance(error.__cause__, ValueError)
        assert str(error.__cause__) == "Original error"
        assert error.__cause__.__class__.__name__ == "ValueError"


class TestMultipartUpload:
    """Tests for the multipart upload helpers.

    Covers:
      - _calculate_multipart_ranges: the part-sizing algorithm.
      - _b64_md5: the base64 MD5 helper.
      - _aupload_file_multipart / _upload_file_multipart: end-to-end mocked
        flows (initiate -> parallel part PUTs -> complete).
      - Retry semantics: transport errors retry, 429 + 5xx retry,
        4xx (other than 429) propagates immediately, retries exhaust into
        DataStorageCreationError chained from the last error.
    """

    # ----- _calculate_multipart_ranges -----

    def test_calculate_multipart_ranges_zero_bytes(self):
        assert _calculate_multipart_ranges(0) == [(0, 0)]

    def test_calculate_multipart_ranges_small_file_one_part(self):
        """Files smaller than the preferred 10 MiB part fit in 1 part."""
        # 5 MiB -> 1 part (also covers the S3 minimum-part-size edge case for
        # single-part uploads where the only part is also the last part).
        ranges = _calculate_multipart_ranges(5 * 1024 * 1024)
        assert ranges == [(0, 5 * 1024 * 1024)]

    def test_calculate_multipart_ranges_12mib_two_parts(self):
        """12 MiB -> 2 parts of 6 MiB each (both above 5 MiB minimum)."""
        size = 12 * 1024 * 1024
        ranges = _calculate_multipart_ranges(size)
        assert len(ranges) == 2
        # Each part exactly 6 MiB
        assert ranges[0] == (0, 6 * 1024 * 1024)
        assert ranges[1] == (6 * 1024 * 1024, 12 * 1024 * 1024)

    def test_calculate_multipart_ranges_medium_tier_at_1gib(self):
        """At 1 GiB exactly, switches to medium tier (50 MiB preferred)."""
        size = 1024 * 1024 * 1024  # 1 GiB
        ranges = _calculate_multipart_ranges(size)
        # ceil(1024 / 50) = 21 parts
        assert len(ranges) == 21
        # All parts (except possibly last) are >= MIN_PART_SIZE_BYTES
        for s, e in ranges[:-1]:
            assert (e - s) >= 5 * 1024 * 1024

    def test_calculate_multipart_ranges_large_tier_at_10gib(self):
        """At 10 GiB, switches to large tier (100 MiB preferred)."""
        size = 10 * 1024 * 1024 * 1024  # 10 GiB
        ranges = _calculate_multipart_ranges(size)
        # ceil(10240 / 100) = 103 parts
        assert len(ranges) == 103

    def test_calculate_multipart_ranges_covers_full_file(self):
        """Concatenating all part ranges must equal the full file."""
        for size in [
            12 * 1024 * 1024,
            50 * 1024 * 1024,
            123_456_789,  # awkward remainder
            1024 * 1024 * 1024,
        ]:
            ranges = _calculate_multipart_ranges(size)
            # No gaps, no overlaps
            assert ranges[0][0] == 0
            assert ranges[-1][1] == size
            for i in range(len(ranges) - 1):
                assert ranges[i][1] == ranges[i + 1][0]

    # ----- _b64_md5 -----

    def test_b64_md5_empty(self):
        """MD5 of empty bytes is the well-known constant 1B2M2Y8AsgTpgAmY7PhCfg==."""
        assert _b64_md5(b"") == "1B2M2Y8AsgTpgAmY7PhCfg=="

    def test_b64_md5_known_value(self):
        """MD5("hello") in hex = 5d41402abc4b2a76b9719d911017c592."""
        # Verify it's exactly 24 chars (base64 of 16 raw bytes), not 44
        # (base64 of 32-char hex string).
        result = _b64_md5(b"hello")
        assert len(result) == 24
        assert result == "XUFAKrxLKna5cZ2REBfFkg=="

    # ----- _aupload_file_multipart happy path -----

    @pytest.mark.asyncio
    async def test_aupload_file_multipart_happy_path(self, tmp_path):
        """End-to-end async happy path: small binary file, 1 part."""
        # Write a small 1 MiB file (-> 1 part, no minimum check).
        file_path = tmp_path / "test.bin"
        file_path.write_bytes(b"x" * (1024 * 1024))
        file_size = 1024 * 1024
        entry_id = uuid4()

        # Mock authenticated client (initiate + complete).
        auth_client = AsyncMock()
        initiate_resp = Mock()
        initiate_resp.json.return_value = {
            "upload_id": "test-upload-id",
            "part_urls": ["https://storage.example.com/part-1"],
        }
        initiate_resp.raise_for_status.return_value = None
        complete_resp = Mock()
        complete_resp.raise_for_status.return_value = None
        auth_client.post.side_effect = [initiate_resp, complete_resp]

        # Mock bare AsyncClient for part PUTs.
        part_client = AsyncMock()
        put_resp = Mock()
        put_resp.raise_for_status.return_value = None
        put_resp.headers = {"etag": '"part-1-etag"'}
        part_client.put.return_value = put_resp

        async_client_cm = AsyncMock()
        async_client_cm.__aenter__.return_value = part_client
        async_client_cm.__aexit__.return_value = None

        progress_bar = Mock()
        progress_bar.set_description = Mock()
        progress_bar.refresh = Mock()
        progress_bar.update = Mock()

        with patch(
            "edison_client.clients.multipart_upload.AsyncClient",
            return_value=async_client_cm,
        ):
            await _aupload_file_multipart(
                client=auth_client,
                entry_id=entry_id,
                file_path=file_path,
                file_size=file_size,
                progress_bar=progress_bar,
            )

        # Assert initiate POST.
        initiate_call = auth_client.post.call_args_list[0]
        assert (
            initiate_call.args[0]
            == f"/v0.1/data-storage/data-entries/{entry_id}/multipart-upload/initiate"
        )
        # part_hashes must be a 1-element list containing the base64 MD5 of the file.
        expected_hash = _b64_md5(b"x" * (1024 * 1024))
        assert initiate_call.kwargs["json"] == {"part_hashes": [expected_hash]}

        # Assert part PUT.
        part_put_call = part_client.put.call_args
        assert part_put_call.args[0] == "https://storage.example.com/part-1"
        assert part_put_call.kwargs["headers"] == {"Content-MD5": expected_hash}
        assert part_put_call.kwargs["content"] == b"x" * (1024 * 1024)

        # Assert complete POST.
        complete_call = auth_client.post.call_args_list[1]
        assert (
            complete_call.args[0]
            == f"/v0.1/data-storage/data-entries/{entry_id}/multipart-upload/complete"
        )
        assert complete_call.kwargs["json"] == {
            "upload_id": "test-upload-id",
            "parts": [
                {
                    "part_number": 1,
                    "etag": '"part-1-etag"',
                    "checksum": expected_hash,
                }
            ],
        }

        # Assert progress reported.
        progress_bar.update.assert_called_once_with(1024 * 1024)

    @pytest.mark.asyncio
    async def test_aupload_file_multipart_multiple_parts(self, tmp_path):
        """12 MiB file -> 2 parts; verifies parts come back in order."""
        file_path = tmp_path / "test.bin"
        file_size = 12 * 1024 * 1024
        # Distinct content per half so MD5s differ.
        file_path.write_bytes(b"a" * (6 * 1024 * 1024) + b"b" * (6 * 1024 * 1024))
        entry_id = uuid4()

        auth_client = AsyncMock()
        initiate_resp = Mock()
        initiate_resp.json.return_value = {
            "upload_id": "uid",
            "part_urls": [
                "https://storage.example.com/p1",
                "https://storage.example.com/p2",
            ],
        }
        initiate_resp.raise_for_status.return_value = None
        complete_resp = Mock()
        complete_resp.raise_for_status.return_value = None
        auth_client.post.side_effect = [initiate_resp, complete_resp]

        part_client = AsyncMock()

        # Different ETags per part so we can verify they map correctly.
        def make_put_resp(etag: str):
            r = Mock()
            r.raise_for_status.return_value = None
            r.headers = {"etag": etag}
            return r

        async def fake_put(url, content, headers):
            if url.endswith("/p1"):
                return make_put_resp("etag-1")
            return make_put_resp("etag-2")

        part_client.put.side_effect = fake_put

        async_client_cm = AsyncMock()
        async_client_cm.__aenter__.return_value = part_client
        async_client_cm.__aexit__.return_value = None

        progress_bar = Mock()

        with patch(
            "edison_client.clients.multipart_upload.AsyncClient",
            return_value=async_client_cm,
        ):
            await _aupload_file_multipart(
                client=auth_client,
                entry_id=entry_id,
                file_path=file_path,
                file_size=file_size,
                progress_bar=progress_bar,
            )

        # Parts must arrive at complete in part_number order with correct etags.
        complete_call = auth_client.post.call_args_list[1]
        parts = complete_call.kwargs["json"]["parts"]
        assert [p["part_number"] for p in parts] == [1, 2]
        assert parts[0]["etag"] == "etag-1"
        assert parts[1]["etag"] == "etag-2"
        # checksums match per-part hashes.
        assert parts[0]["checksum"] == _b64_md5(b"a" * (6 * 1024 * 1024))
        assert parts[1]["checksum"] == _b64_md5(b"b" * (6 * 1024 * 1024))

    @pytest.mark.asyncio
    async def test_aupload_file_multipart_part_url_count_mismatch(self, tmp_path):
        """If server returns wrong number of part URLs, raise."""
        file_path = tmp_path / "test.bin"
        file_path.write_bytes(b"x" * 1024)
        entry_id = uuid4()

        auth_client = AsyncMock()
        initiate_resp = Mock()
        # Returned 2 URLs but file only fits in 1 part.
        initiate_resp.json.return_value = {
            "upload_id": "uid",
            "part_urls": ["https://x/1", "https://x/2"],
        }
        initiate_resp.raise_for_status.return_value = None
        auth_client.post.return_value = initiate_resp

        async_client_cm = AsyncMock()
        progress_bar = Mock()

        with (
            patch(
                "edison_client.clients.multipart_upload.AsyncClient",
                return_value=async_client_cm,
            ),
            pytest.raises(DataStorageCreationError, match="2 part URLs"),
        ):
            await _aupload_file_multipart(
                client=auth_client,
                entry_id=entry_id,
                file_path=file_path,
                file_size=1024,
                progress_bar=progress_bar,
            )

    # ----- Retry semantics -----

    @pytest.mark.asyncio
    async def test_aupload_one_part_retries_on_transport_error(self, monkeypatch):
        """Transport errors trigger retry; HTTP errors do not."""

        # Skip the backoff sleeps so the test runs fast.
        async def fake_sleep(_):
            return None

        monkeypatch.setattr(
            "edison_client.clients.multipart_upload.asyncio.sleep", fake_sleep
        )

        part_client = AsyncMock()
        success_resp = Mock()
        success_resp.raise_for_status.return_value = None
        success_resp.headers = {"etag": "ok"}

        # First attempt: transport error. Second attempt: success.
        part_client.put.side_effect = [
            httpx.ConnectError("boom"),
            success_resp,
        ]

        etag = await _aupload_one_part(
            part_client=part_client,
            part_url="https://x/1",
            chunk=b"data",
            content_md5="md5",
            part_number=1,
        )
        assert etag == "ok"
        assert part_client.put.call_count == 2

    @pytest.mark.asyncio
    async def test_aupload_one_part_does_not_retry_on_4xx(self):
        """4xx (other than 429) propagates immediately.

        Bad signature / expired URL / wrong MD5 won't be fixed by retrying.
        Mirrors urllib3's status_forcelist behavior.
        """
        part_client = AsyncMock()
        bad_resp = Mock()
        bad_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "403", request=Mock(), response=Mock(status_code=403)
        )
        part_client.put.return_value = bad_resp

        with pytest.raises(httpx.HTTPStatusError):
            await _aupload_one_part(
                part_client=part_client,
                part_url="https://x/1",
                chunk=b"data",
                content_md5="md5",
                part_number=1,
            )
        # Crucial: only one PUT attempt, no retry.
        assert part_client.put.call_count == 1

    @pytest.mark.asyncio
    async def test_aupload_one_part_retries_on_5xx(self, monkeypatch):
        """503 (and other 5xx) triggers retry."""

        async def fake_sleep(_):
            return None

        monkeypatch.setattr(
            "edison_client.clients.multipart_upload.asyncio.sleep", fake_sleep
        )

        part_client = AsyncMock()
        # First call: 503. Second call: success.
        bad_resp = Mock()
        bad_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "503", request=Mock(), response=Mock(status_code=503)
        )
        good_resp = Mock()
        good_resp.raise_for_status.return_value = None
        good_resp.headers = {"etag": "after-503"}
        part_client.put.side_effect = [bad_resp, good_resp]

        etag = await _aupload_one_part(
            part_client=part_client,
            part_url="https://x/1",
            chunk=b"data",
            content_md5="md5",
            part_number=1,
        )
        assert etag == "after-503"
        assert part_client.put.call_count == 2

    @pytest.mark.asyncio
    async def test_aupload_one_part_exhausts_retries(self, monkeypatch):
        """All transport-error retries fail -> DataStorageCreationError."""

        async def fake_sleep(_):
            return None

        monkeypatch.setattr(
            "edison_client.clients.multipart_upload.asyncio.sleep", fake_sleep
        )

        part_client = AsyncMock()
        part_client.put.side_effect = httpx.ConnectError("persistent")

        with pytest.raises(DataStorageCreationError, match="part 1"):
            await _aupload_one_part(
                part_client=part_client,
                part_url="https://x/1",
                chunk=b"data",
                content_md5="md5",
                part_number=1,
            )
        assert part_client.put.call_count == 3  # PART_UPLOAD_MAX_RETRIES

    @pytest.mark.asyncio
    async def test_aupload_one_part_exhausts_retries_on_5xx(self, monkeypatch):
        """Three consecutive 5xx -> DataStorageCreationError.

        Verifies the retry-on-5xx policy correctly exhausts and chains the
        last HTTPStatusError as the cause.
        """

        async def fake_sleep(_):
            return None

        monkeypatch.setattr(
            "edison_client.clients.multipart_upload.asyncio.sleep", fake_sleep
        )

        part_client = AsyncMock()
        bad_resp = Mock()
        last_status_error = httpx.HTTPStatusError(
            "503", request=Mock(), response=Mock(status_code=503)
        )
        bad_resp.raise_for_status.side_effect = last_status_error
        part_client.put.return_value = bad_resp

        with pytest.raises(DataStorageCreationError, match="part 1") as exc_info:
            await _aupload_one_part(
                part_client=part_client,
                part_url="https://x/1",
                chunk=b"data",
                content_md5="md5",
                part_number=1,
            )
        assert part_client.put.call_count == 3  # PART_UPLOAD_MAX_RETRIES
        # Cause chain points at the last HTTPStatusError (the most recent
        # transient failure).
        assert isinstance(exc_info.value.__cause__, httpx.HTTPStatusError)

    # ----- Sync variant ----- (small smoke; sync mirrors async)

    def test_upload_file_multipart_happy_path(self, tmp_path):
        """End-to-end sync happy path: small file, 1 part."""
        file_path = tmp_path / "test.bin"
        file_path.write_bytes(b"y" * 4096)
        entry_id = uuid4()

        auth_client = Mock()
        initiate_resp = Mock()
        initiate_resp.json.return_value = {
            "upload_id": "uid",
            "part_urls": ["https://storage.example.com/part-1"],
        }
        initiate_resp.raise_for_status.return_value = None
        complete_resp = Mock()
        complete_resp.raise_for_status.return_value = None
        auth_client.post.side_effect = [initiate_resp, complete_resp]

        part_client = Mock()
        put_resp = Mock()
        put_resp.raise_for_status.return_value = None
        put_resp.headers = {"etag": "sync-etag"}
        part_client.put.return_value = put_resp

        client_cm = Mock()
        client_cm.__enter__ = Mock(return_value=part_client)
        client_cm.__exit__ = Mock(return_value=None)

        progress_bar = Mock()

        with patch(
            "edison_client.clients.multipart_upload.Client", return_value=client_cm
        ):
            _upload_file_multipart(
                client=auth_client,
                entry_id=entry_id,
                file_path=file_path,
                file_size=4096,
                progress_bar=progress_bar,
            )

        complete_call = auth_client.post.call_args_list[1]
        parts = complete_call.kwargs["json"]["parts"]
        assert len(parts) == 1
        assert parts[0]["etag"] == "sync-etag"
        assert parts[0]["checksum"] == _b64_md5(b"y" * 4096)
