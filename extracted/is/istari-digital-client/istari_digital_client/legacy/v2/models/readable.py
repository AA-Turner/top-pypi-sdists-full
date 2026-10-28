import abc
import io
import logging
import os
import json
import shutil
import threading
import uuid
from functools import cached_property
from typing import Callable, TypeAlias, Union, Optional, TYPE_CHECKING
from pathlib import Path
import hashlib
import tempfile
from threading import Lock

from istari_digital_client import native_crypto

from istari_digital_client._transfer.download import check_written, open_partial, partial_path
from istari_digital_client._transfer.errors import TransferCancelledError
from istari_digital_client._transfer.events import EventForwarder, EventKind, TransferEvent
from istari_digital_client._transfer.http import check_cancel
from istari_digital_client.legacy.log_utils import log_method

if TYPE_CHECKING:
    from istari_digital_client.legacy.v2.models.properties import Properties
    from istari_digital_client.legacy.configuration import Configuration
    from istari_digital_client.legacy.v2.models.token import Token
    from istari_digital_client.legacy.v2.api.v2_api import V2Api

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
PathLike = Union[str, os.PathLike, Path]
ProgressCallback = Callable[[TransferEvent], None]

_COPY_CHUNK = 8 * 1024 * 1024

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
    def copy_to(
        self,
        dest: PathLike,
        *,
        progress: ProgressCallback | None = None,
        cancel: threading.Event | None = None,
    ) -> Path:
        """
        Copy the contents to a local file (an alias of ``download_to``).

        :param dest: Path to write the file to. This can be a string, Path, or os.PathLike.
        :raises OSError: If the file cannot be written.
        """
        return self.download_to(dest, progress=progress, cancel=cancel)

    def download_to(
        self,
        dest: PathLike,
        *,
        progress: ProgressCallback | None = None,
        cancel: threading.Event | None = None,
    ) -> Path:
        """
        Download the contents to a local file, verified, and return the path.

        The bytes stream to a temp file beside ``dest`` and are renamed into place only
        after the salted digest verifies, so a corrupt download never lands at ``dest``.
        A filesystem-cache hit is streamed and verified the same way; on a miss the
        content is downloaded to ``dest`` and copied into the cache only when it is at
        most ``filesystem_cache_max_size`` bytes.

        :param dest: Path to write the file to. This can be a string, Path, or os.PathLike.
        :param progress: Optional callback receiving ``TransferEvent`` notifications.
        :param cancel: Optional ``threading.Event``; setting it aborts the transfer.
        :raises OSError: If the file cannot be written.
        """
        size = getattr(self, "size", None)
        progress = EventForwarder(progress, int(size) if size is not None else None)
        try:
            check_cancel(cancel)
            return self._download_to(dest, progress=progress, cancel=cancel)
        except (TransferCancelledError, KeyboardInterrupt, SystemExit):
            progress(TransferEvent(EventKind.CANCELLED, 0, None))
            raise

    def _download_to(
        self,
        dest: PathLike,
        *,
        progress: EventForwarder,
        cancel: threading.Event | None,
    ) -> Path:
        """Share event ownership across cache copy and remote fallback."""
        dest_path = Path(str(dest))
        client = self._require_client()
        token = self._content_token()
        if not self._should_use_cache():
            return client.download_to(token, dest_path, progress=progress, cancel=cancel)

        cache_path = self._cache_path
        if cache_path is None:
            return client.download_to(token, dest_path, progress=progress, cancel=cancel)

        with self._cache_path_lock:
            if cache_path.exists():
                try:
                    self._stream_verified_copy(
                        cache_path, dest_path, token, progress=progress, cancel=cancel
                    )
                    self._filesystem_cache_hits += 1
                    logger.debug("%s cache hit: %s", self._log_msg_pfx, cache_path)
                    return dest_path
                except (FileNotFoundError, InvalidChecksumError) as e:
                    # another Readable's cleanup can unlink the file under us; the lock is per instance
                    self._filesystem_cache_misses += 1
                    logger.debug("%s cache file unusable (%s); re-fetching", self._log_msg_pfx, e)
                    cache_path.unlink(missing_ok=True)
            else:
                self._filesystem_cache_misses += 1

            client.download_to(token, dest_path, progress=progress, cancel=cancel)
            self._cache_from_file(dest_path)
        return dest_path

    def _stream_verified_copy(
        self,
        source: Path,
        dest: Path,
        token: "Token",
        progress: ProgressCallback | None = None,
        cancel: threading.Event | None = None,
    ) -> None:
        """Copy ``source`` to ``dest`` through a temp file, verifying the digest before the rename.

        Emits ``part_done`` and a terminal ``complete`` event so a cache hit reports
        progress the same way a download does.
        """
        forward = progress if isinstance(progress, EventForwarder) else EventForwarder(progress)
        check_cancel(cancel)
        verifier = native_crypto.VerifyingHasher(token.sha, token.salt)
        total = source.stat().st_size
        expected = getattr(self, "size", None)
        if expected is not None and total != int(expected):
            raise InvalidChecksumError("cached file size differs from expected object size")
        done = 0
        tmp = partial_path(dest)  # named before it exists, so cleanup never waits on the open
        try:
            with open_partial(tmp) as raw, io.BufferedWriter(raw) as out, source.open("rb") as inp:
                while True:
                    check_cancel(cancel)
                    chunk = inp.read(_COPY_CHUNK)
                    if not chunk:
                        break
                    verifier.update(chunk)
                    out.write(chunk)
                    done += len(chunk)
                    forward(TransferEvent(EventKind.PART_DONE, done, total))
            try:
                verifier.finalize()
            except ValueError as e:
                raise InvalidChecksumError(
                    f"Token data content checksum is invalid for cached file {source}"
                ) from e
            if expected is not None and done != int(expected):
                raise InvalidChecksumError("cached file size differs from expected object size")
            check_written(tmp, done)
            check_cancel(cancel)
            os.replace(tmp, dest)
        except BaseException as exc:
            tmp.unlink(missing_ok=True)
            if isinstance(exc, (TransferCancelledError, KeyboardInterrupt, SystemExit)):
                forward(TransferEvent(EventKind.CANCELLED, done, total))
            raise
        forward(TransferEvent(EventKind.COMPLETE, done, done))

    def _cache_free_bytes(self, directory: Path) -> int:
        """Return free bytes on the filesystem holding the cache directory."""
        return shutil.disk_usage(directory).free

    def _cache_has_capacity(self, size: int) -> bool:
        """Check only the additional cache copy; the destination is already allocated."""
        max_size = getattr(self._client_config, "filesystem_cache_max_size", None)
        if max_size is not None and size > int(max_size):
            return False
        directory = self._cache_dir
        directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        return size <= self._cache_free_bytes(directory)

    def _cache_from_file(self, source: Path) -> None:
        """Best-effort atomic cache insertion of a freshly verified download."""
        temp_path = None
        try:
            cache_path = self._cache_path
            if cache_path is None or not self._cache_has_capacity(source.stat().st_size):
                return
            temp_path = self._cache_dir_mktemp()
            shutil.copyfile(source, temp_path)
            temp_path.replace(cache_path)
            self._filesystem_cache_puts += 1
            logger.debug("%s cached contents: %s", self._log_msg_pfx, cache_path)
        except OSError as e:
            logger.warning("%s could not cache %s: %s", self._log_msg_pfx, source, e)
        finally:
            if temp_path is not None:
                try:
                    temp_path.unlink(missing_ok=True)
                except OSError as e:
                    logger.debug("%s could not clean cache temporary file: %s", self._log_msg_pfx, e)

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
        verifier = native_crypto.VerifyingHasher(content_token.sha, content_token.salt)
        verifier.update(data)
        try:
            verifier.finalize()
        except ValueError as e:
            raise InvalidChecksumError(
                f"Token data content checksum is invalid (expected {content_token.sha})"
            ) from e
        return data

    def _verify_cache_file(self, cache_path: Path) -> None:
        """
        Stream-verify a cache file against the content token.

        :raises InvalidChecksumError: If checksum verification fails
        """
        content_token = self._content_token()
        verifier = native_crypto.VerifyingHasher(content_token.sha, content_token.salt)
        with cache_path.open("rb") as f:
            while True:
                chunk = f.read(_COPY_CHUNK)
                if not chunk:
                    break
                verifier.update(chunk)
        try:
            verifier.finalize()
        except ValueError as e:
            raise InvalidChecksumError(
                f"Token data content checksum is invalid for cached file {cache_path}"
            ) from e

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
        expected = getattr(self, "size", None)
        if expected is not None and len(data) != int(expected):
            raise InvalidChecksumError("cached file size differs from expected object size")
        return self._verify_checksum(data)

    def _write_to_cache(self, data: bytes) -> None:
        """
        Write data to cache atomically.

        :param data: Data to cache
        """
        temp_path = None
        try:
            cache_path = self._cache_path
            if cache_path is None or not self._cache_has_capacity(len(data)):
                return
            temp_path = self._cache_dir_mktemp()
            temp_path.write_bytes(data)
            temp_path.replace(cache_path)
            self._filesystem_cache_puts += 1
            logger.debug("%s cached contents (size: %d): %s", self._log_msg_pfx, len(data), cache_path)
        except OSError as e:
            logger.warning("%s could not cache contents: %s", self._log_msg_pfx, e)
        finally:
            if temp_path is not None:
                try:
                    temp_path.unlink(missing_ok=True)
                except OSError as e:
                    logger.debug("%s could not clean cache temporary file: %s", self._log_msg_pfx, e)

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

                # Fetch fresh data (read_contents verifies the digest inline)
                logger.debug("%s fetching fresh content", self._log_msg_pfx)

                data = self.read_contents()

                self._write_to_cache(data)

                return data

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
