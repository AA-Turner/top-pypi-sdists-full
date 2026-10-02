import abc
import logging
import os
import json
import uuid
from functools import cached_property
from typing import TypeAlias, Union, Optional, TYPE_CHECKING
from pathlib import Path
import hashlib
import tempfile
from threading import Lock

from istari_digital_client.legacy.log_utils import log_method

if TYPE_CHECKING:
    from istari_digital_client.legacy.v2.models.properties import Properties
    from istari_digital_client.legacy.configuration import Configuration
    from istari_digital_client.legacy.v2.models.token import Token
    from istari_digital_client.legacy.v2.api.v2_api import V2Api

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
PathLike = Union[str, os.PathLike, Path]

logger = logging.getLogger("istari-digital-client.readable")


class ReadError(IOError):
    pass


class CacheError(Exception):
    pass


class InvalidChecksumError(ValueError):
    pass


class Readable(abc.ABC):
    """
    Abstract base class for objects that expose readable file-like content.

    This interface provides convenient methods for accessing raw bytes, text content,
    JSON data, and for copying contents to a local path with optional filesystem caching.
    """

    _filesystem_cache_hits: int = 0
    _filesystem_cache_misses: int = 0
    _filesystem_cache_puts: int = 0

    @abc.abstractmethod
    def read_bytes(self) -> bytes:
        """
        Read the contents as raw bytes.
        """
        ...

    def _require_client(self) -> "V2Api":
        client = getattr(self, "_client", None)
        if client is None:
            raise ValueError(
                f"`client` is not set for instance of {self.__class__.__name__}"
            )
        return client

    @property
    def _client_config(self) -> "Configuration":
        return self._require_client().config

    def _content_token(self) -> "Token":
        """
        Ensure that a content token is available on this instance.

        :raises ValueError: If the ``content_token`` attribute is not set.
        """
        content_token = getattr(self, "content_token", None)
        if content_token is None:
            raise ValueError(
                f"`content_token` is not set for instance of {self.__class__.__name__}"
            )
        return content_token

    def _properties_token(self) -> "Token":
        """
        Ensure that a properties token is available on this instance.

        :raises ValueError: If the ``properties_token`` attribute is not set.
        """
        properties_token = getattr(self, "properties_token", None)
        if properties_token is None:
            raise ValueError(
                f"`properties_token` is not set for instance of {self.__class__.__name__}"
            )
        return properties_token

    def _should_use_cache(self) -> bool:
        """
        Determine if filesystem caching should be used.

        :returns: True if caching is enabled and requirements are met
        """
        try:
            return bool(self._client_config.filesystem_cache_enabled)
        except (ValueError, AttributeError):
            return False

    def read_contents(self) -> bytes:
        return self._require_client().read_contents(token=self._content_token())

    def read_properties(self) -> "Properties":
        return self._require_client().read_properties(
            token=self._properties_token()
        )

    @log_method
    def read_text(self, encoding: str = "utf-8") -> str:
        """
        Read the contents as decoded text.

        :param encoding: Text encoding to use. Defaults to "utf-8".
        :raises UnicodeDecodeError: If the byte content cannot be decoded.
        """
        return self.read_bytes().decode(encoding)

    @log_method
    def copy_to(self, dest: PathLike) -> Path:
        """
        Copy the contents to a local file.

        :param dest: Path to write the file to. This can be a string, Path, or os.PathLike.
        :raises OSError: If the file cannot be written.
        """
        dest_path = Path(str(dest))
        dest_path.write_bytes(self.read_bytes())
        return dest_path

    @log_method
    def read_json(self, encoding: str = "utf-8") -> JSON:
        """
        Parse the contents as JSON.

        :param encoding: Text encoding to use when decoding the content. Defaults to "utf-8".
        :raises UnicodeDecodeError: If the byte content cannot be decoded.
        :raises json.JSONDecodeError: If the decoded content is not valid JSON.
        """
        return json.loads(self.read_text(encoding=encoding))

    def cleanup_cache(self) -> None:
        """
        Clean up cached files if they exist.
        """
        try:
            cache_path = self._cache_path
            if cache_path is not None and cache_path.exists():
                cache_path.unlink(missing_ok=True)
                logger.debug("Cleaned up cache file: %s", cache_path)
        except Exception as e:
            logger.debug("Failed to cleanup cache: %s", e)

    @log_method
    def __del__(self):
        """
        Delete the cached file content if it exists.
        """
        self.cleanup_cache()

    @cached_property
    def _cache_path_lock(self) -> Lock:
        return Lock()

    @cached_property
    def _log_msg_pfx(self) -> str:
        try:
            content_token = self._content_token()
            return f"token {content_token.id} -"
        except ValueError:
            return f"readable {id(self)} -"

    def _cache_identifier(self, size: int = 16) -> str:
        content_token = self._content_token()
        # This names a cache file; it is not a security operation, so it is
        # hashed with usedforsecurity=False. Besides being the correct semantic,
        # this is required under FIPS, where the default (security) digest path
        # may be unavailable.
        _hash = hashlib.sha384(usedforsecurity=False)
        _hash.update(content_token.sha.encode("utf-8"))
        _hash.update(content_token.salt.encode("utf-8"))
        return _hash.hexdigest()[: size * 2]  # size bytes -> size*2 hex chars

    @cached_property
    def _cache_dir(self) -> Path:
        subdir = self._cache_identifier(size=2)
        _dir = self._client_config.filesystem_cache_root / subdir
        _dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        return _dir

    @cached_property
    def _cache_name(self) -> str:
        return self._cache_identifier(size=32)

    @cached_property
    def _cache_path(self) -> Optional[Path]:
        try:
            return self._cache_dir / self._cache_name
        except (ValueError, CacheError) as e:
            # Log the cause; a bare None here otherwise surfaces only as the
            # opaque "Cache path is not available".
            logger.debug("%s cache path unavailable: %r", self._log_msg_pfx, e)
            return None

    def _cache_dir_mktemp(self) -> Path:
        fd, path = tempfile.mkstemp(
            suffix=str(uuid.uuid4()) + ".tmp",
            prefix=self._cache_name,
            dir=self._cache_dir,
        )
        os.close(fd)
        return Path(path)

    def _verify_checksum(self, data: bytes) -> bytes:
        """
        Verify the checksum of data against the content token.

        :param data: The data to verify
        :returns: The data if checksum is valid
        :raises InvalidChecksumError: If checksum verification fails
        """
        content_token = self._content_token()
        # Content-integrity check, not a security operation — usedforsecurity=False
        # (see `_cache_identifier`).
        hasher = hashlib.sha384(usedforsecurity=False)
        hasher.update(data)
        hasher.update(content_token.salt.encode("utf-8"))
        actual = hasher.hexdigest()
        expected = content_token.sha

        if actual != expected:
            msg = f"Token data content checksum is invalid ({actual} != {expected})"
            raise InvalidChecksumError(msg)
        return data

    def _read_from_cache(self) -> bytes:
        """
        Read and verify data from cache.

        :returns: Verified cached data
        :raises FileNotFoundError: If cache file doesn't exist
        :raises InvalidChecksumError: If checksum verification fails
        """
        cache_path = self._cache_path
        if cache_path is None:
            raise CacheError("Cache path is not available")
        if not cache_path.exists():
            raise FileNotFoundError(f"Cache file not found: {cache_path}")

        data = cache_path.read_bytes()
        return self._verify_checksum(data)

    def _write_to_cache(self, data: bytes) -> None:
        """
        Write data to cache atomically.

        :param data: Data to cache
        """
        cache_path = self._cache_path
        if cache_path is None:
            raise CacheError("Cache path is not available")

        # Ensure cache directory exists
        cache_dir = self._cache_dir
        if not cache_dir.exists():
            cache_dir.mkdir(mode=0o700, parents=True, exist_ok=True)

        # Write to temporary file first for atomic operation
        temp_path = self._cache_dir_mktemp()
        try:
            temp_path.write_bytes(data)
            size = temp_path.stat().st_size
            temp_path.replace(cache_path)

            logger.debug(
                "%s cached contents (size: %d): %s",
                self._log_msg_pfx,
                size,
                cache_path,
            )
            self._filesystem_cache_puts += 1
        except Exception:
            # Clean up temp file if something goes wrong
            temp_path.unlink(missing_ok=True)
            raise

    def _filesystem_caching_read_bytes(self) -> bytes:
        """
        Read bytes using filesystem caching with proper error handling.

        :returns: File content as bytes
        """
        cache_path = self._cache_path
        if cache_path is None:
            raise CacheError("Cache path is not available")

        with self._cache_path_lock:
            try:
                # Try to read from cache first
                data = self._read_from_cache()
                self._filesystem_cache_hits += 1
                logger.debug("%s cache hit: %s", self._log_msg_pfx, cache_path)
                return data

            except (FileNotFoundError, InvalidChecksumError) as e:
                # Cache miss or corruption - need to fetch fresh data
                self._filesystem_cache_misses += 1
                logger.debug(
                    "%s cache miss (%s): %s", self._log_msg_pfx, type(e).__name__, e
                )

                # Remove corrupted cache file if it exists
                if cache_path.exists():
                    cache_path.unlink(missing_ok=True)

                # Fetch fresh data
                logger.debug("%s fetching fresh content", self._log_msg_pfx)

                data = self.read_contents()

                # Verify the fresh data before caching
                verified_data = self._verify_checksum(data)

                # Cache the verified data
                self._write_to_cache(verified_data)

                return verified_data

    def get_cache_stats(self) -> dict[str, int]:
        """
        Get filesystem cache statistics.

        :returns: Dictionary with cache hit/miss/put counts
        """
        return {
            "hits": self._filesystem_cache_hits,
            "misses": self._filesystem_cache_misses,
            "puts": self._filesystem_cache_puts,
        }
