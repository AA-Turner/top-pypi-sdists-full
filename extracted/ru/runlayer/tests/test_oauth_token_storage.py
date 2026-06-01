"""Tests for OAuth token storage and refresh functionality."""

import json
import tempfile
import time
from pathlib import Path

import pytest
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken

from runlayer_cli.oauth import FileTokenStorage


@pytest.fixture
def temp_cache_dir():
    """Create a temporary directory for token storage tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def storage(temp_cache_dir: Path):
    """Create a FileTokenStorage instance with temporary directory."""
    return FileTokenStorage(
        server_url="https://test-server.example.com",
        cache_dir=temp_cache_dir,
    )


class TestFileTokenStorageBasics:
    """Test basic FileTokenStorage operations."""

    def test_get_base_url(self, storage: FileTokenStorage):
        """Test URL base extraction preserves path for RFC 8707 resource matching."""
        assert storage.get_base_url("https://example.com/path/to/resource") == "https://example.com/path/to/resource"
        assert storage.get_base_url("http://localhost:8080/api") == "http://localhost:8080/api"
        assert storage.get_base_url("https://example.com") == "https://example.com"
        # Query string and fragment should be stripped
        assert storage.get_base_url("https://example.com/mcp?foo=bar#frag") == "https://example.com/mcp"

    def test_get_cache_key(self, storage: FileTokenStorage):
        """Test cache key generation."""
        key = storage.get_cache_key()
        assert "https" in key
        assert "test-server_example_com" in key
        # Should not contain problematic filesystem characters
        assert "/" not in key
        assert ":" not in key.replace("https_", "")

    def test_cache_dir_created(self, temp_cache_dir: Path):
        """Test that cache directory is created if it doesn't exist."""
        new_cache_dir = temp_cache_dir / "new_subdir"
        assert not new_cache_dir.exists()
        
        FileTokenStorage(
            server_url="https://example.com",
            cache_dir=new_cache_dir,
        )
        
        assert new_cache_dir.exists()


class TestTokenStorage:
    """Test token save/load operations."""

    @pytest.mark.asyncio
    async def test_set_and_get_tokens(self, storage: FileTokenStorage):
        """Test saving and loading tokens."""
        token = OAuthToken(
            access_token="test_access_token",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="test_refresh_token",
            scope="read write",
        )
        
        await storage.set_tokens(token)
        loaded_token = await storage.get_tokens()
        
        assert loaded_token is not None
        assert loaded_token.access_token == "test_access_token"
        assert loaded_token.token_type == "Bearer"
        assert loaded_token.refresh_token == "test_refresh_token"
        assert loaded_token.scope == "read write"

    @pytest.mark.asyncio
    async def test_get_tokens_not_found(self, storage: FileTokenStorage):
        """Test loading tokens when file doesn't exist."""
        token = await storage.get_tokens()
        assert token is None

    @pytest.mark.asyncio
    async def test_get_tokens_corrupted_file(self, storage: FileTokenStorage, temp_cache_dir: Path):
        """Test loading tokens from corrupted file."""
        # Write corrupted data
        path = storage._get_file_path("tokens")
        path.write_text("not valid json {{{")
        
        token = await storage.get_tokens()
        assert token is None

    @pytest.mark.asyncio
    async def test_tokens_backwards_compatible_old_format(self, storage: FileTokenStorage):
        """Test loading tokens from old format (direct token fields)."""
        # Write old format directly
        path = storage._get_file_path("tokens")
        old_format = {
            "access_token": "old_format_token",
            "token_type": "Bearer",
            "expires_in": 3600,
        }
        path.write_text(json.dumps(old_format))
        
        token = await storage.get_tokens()
        assert token is not None
        assert token.access_token == "old_format_token"

    @pytest.mark.asyncio
    async def test_tokens_new_format_with_expiry(self, storage: FileTokenStorage):
        """Test that new format includes expiry_time."""
        token = OAuthToken(
            access_token="test_token",
            token_type="Bearer",
            expires_in=3600,
        )
        
        before_save = time.time()
        await storage.set_tokens(token)
        after_save = time.time()
        
        # Read raw file to verify format
        path = storage._get_file_path("tokens")
        data = json.loads(path.read_text())
        
        assert "token" in data
        assert "expiry_time" in data
        assert data["expiry_time"] >= before_save + 3600
        assert data["expiry_time"] <= after_save + 3600


class TestTokenExpiryTime:
    """Test token expiry time storage and retrieval."""

    @pytest.mark.asyncio
    async def test_get_token_expiry_time(self, storage: FileTokenStorage):
        """Test retrieving token expiry time."""
        token = OAuthToken(
            access_token="test_token",
            token_type="Bearer",
            expires_in=3600,
        )
        
        await storage.set_tokens(token)
        expiry_time = storage.get_token_expiry_time()
        
        assert expiry_time is not None
        # Should be approximately now + 3600 seconds
        assert expiry_time > time.time() + 3500
        assert expiry_time < time.time() + 3700

    def test_get_token_expiry_time_not_found(self, storage: FileTokenStorage):
        """Test expiry time when file doesn't exist."""
        expiry_time = storage.get_token_expiry_time()
        assert expiry_time is None

    def test_get_token_expiry_time_invalid_value(self, storage: FileTokenStorage):
        """Test expiry time with invalid (non-numeric) value."""
        path = storage._get_file_path("tokens")
        data = {
            "token": {"access_token": "test", "token_type": "Bearer"},
            "expiry_time": "not-a-number",
        }
        path.write_text(json.dumps(data))
        
        expiry_time = storage.get_token_expiry_time()
        assert expiry_time is None

    @pytest.mark.asyncio
    async def test_token_without_expires_in(self, storage: FileTokenStorage):
        """Test token without expires_in field."""
        token = OAuthToken(
            access_token="test_token",
            token_type="Bearer",
            expires_in=None,
        )
        
        await storage.set_tokens(token)
        expiry_time = storage.get_token_expiry_time()
        
        assert expiry_time is None


class TestOAuthMetadata:
    """Test OAuth metadata storage."""

    def test_get_oauth_metadata_not_found(self, storage: FileTokenStorage):
        """Test getting metadata when file doesn't exist."""
        metadata = storage.get_oauth_metadata()
        assert metadata is None

    def test_set_and_get_oauth_metadata(self, storage: FileTokenStorage):
        """Test saving and loading OAuth metadata."""
        metadata = {
            "issuer": "https://auth.example.com",
            "token_endpoint": "https://auth.example.com/token",
            "authorization_endpoint": "https://auth.example.com/authorize",
        }
        
        storage.set_oauth_metadata(metadata)
        loaded = storage.get_oauth_metadata()
        
        assert loaded == metadata

    def test_oauth_metadata_preserved_with_client_info(self, storage: FileTokenStorage):
        """Test that OAuth metadata is preserved when client info is updated."""
        # First, set OAuth metadata
        metadata = {"token_endpoint": "https://example.com/token"}
        storage.set_oauth_metadata(metadata)
        
        # Then, write client info (simulating what set_client_info does)
        path = storage._get_file_path("client_info")
        existing = json.loads(path.read_text())
        
        # Verify metadata is there
        assert existing.get("oauth_metadata") == metadata

    @pytest.mark.asyncio
    async def test_set_client_info_preserves_metadata(self, storage: FileTokenStorage):
        """Test that set_client_info preserves existing oauth_metadata."""
        # First set metadata
        metadata = {"token_endpoint": "https://example.com/token"}
        storage.set_oauth_metadata(metadata)
        
        # Then set client info
        client_info = OAuthClientInformationFull(
            client_id="test_client_id",
            client_secret="test_secret",
            redirect_uris=["http://localhost:8080/callback"],
        )
        await storage.set_client_info(client_info)
        
        # Verify metadata is still there
        loaded_metadata = storage.get_oauth_metadata()
        assert loaded_metadata == metadata


class TestClientInfoStorage:
    """Test client info save/load operations."""

    @pytest.mark.asyncio
    async def test_set_and_get_client_info(self, storage: FileTokenStorage):
        """Test saving and loading client info."""
        client_info = OAuthClientInformationFull(
            client_id="test_client_id",
            client_secret="test_secret",
            redirect_uris=["http://localhost:8080/callback"],
        )
        
        await storage.set_client_info(client_info)
        loaded = await storage.get_client_info()
        
        assert loaded is not None
        assert loaded.client_id == "test_client_id"
        assert loaded.client_secret == "test_secret"

    @pytest.mark.asyncio
    async def test_get_client_info_not_found(self, storage: FileTokenStorage):
        """Test loading client info when file doesn't exist."""
        client_info = await storage.get_client_info()
        assert client_info is None

    @pytest.mark.asyncio
    async def test_get_client_info_invalid_format(self, storage: FileTokenStorage):
        """Test loading client info with missing client_id."""
        path = storage._get_file_path("client_info")
        # Write data without client_id
        path.write_text(json.dumps({"some_field": "value"}))
        
        client_info = await storage.get_client_info()
        assert client_info is None
        # File should be cleared
        assert not path.exists()


class TestClear:
    """Test cache clearing operations."""

    @pytest.mark.asyncio
    async def test_clear(self, storage: FileTokenStorage):
        """Test clearing cache for a server."""
        # Set up some data
        token = OAuthToken(access_token="test", token_type="Bearer")
        client_info = OAuthClientInformationFull(
            client_id="test_id",
            redirect_uris=["http://localhost/callback"],
        )
        
        await storage.set_tokens(token)
        await storage.set_client_info(client_info)
        
        # Verify files exist
        assert storage._get_file_path("tokens").exists()
        assert storage._get_file_path("client_info").exists()
        
        # Clear
        storage.clear()
        
        # Verify files are gone
        assert not storage._get_file_path("tokens").exists()
        assert not storage._get_file_path("client_info").exists()

    @pytest.mark.asyncio
    async def test_clear_all(self, temp_cache_dir: Path):
        """Test clearing all cached data."""
        # Create multiple storages
        storage1 = FileTokenStorage("https://server1.com", temp_cache_dir)
        storage2 = FileTokenStorage("https://server2.com", temp_cache_dir)
        
        # Set up data for both
        token = OAuthToken(access_token="test", token_type="Bearer")
        await storage1.set_tokens(token)
        await storage2.set_tokens(token)
        
        # Verify files exist
        assert len(list(temp_cache_dir.glob("*_tokens.json"))) == 2
        
        # Clear all
        FileTokenStorage.clear_all(temp_cache_dir)
        
        # Verify all files are gone
        assert len(list(temp_cache_dir.glob("*_tokens.json"))) == 0
        assert len(list(temp_cache_dir.glob("*_client_info.json"))) == 0

