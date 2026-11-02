"""Stage caller files through the SDK's root Session file manager."""

from collections.abc import AsyncIterator, Callable
from pathlib import Path

from mistralai.vibe.harness.app_server.session import ResourceLinkContentBlock
from mistralai.vibe.harness.app_server.session.file_upload import FileUploader

from .session_file_manager import LocalSessionFileManager


class SessionFileStager(FileUploader):
    """Validate a Session and delegate uploads to its root-owned file manager.

    The manager snapshots bytes in the host file store, registers catalog metadata,
    and returns a link. The sandbox copy is created later when a message references
    that link; staging alone does not submit a message or write into the sandbox.
    """

    def __init__(self, files: LocalSessionFileManager, validate_session: Callable[[str], None]) -> None:
        self._files = files
        self._validate_session = validate_session

    async def __call__(
        self,
        session_id: str,
        source: str | Path | bytes | AsyncIterator[bytes],
        *,
        name: str | None,
        media_type: str | None,
    ) -> ResourceLinkContentBlock:
        self._validate_session(session_id)

        def validate_session() -> None:
            self._validate_session(session_id)

        return await self._files.upload(source, name=name, media_type=media_type, validate_session=validate_session)


__all__ = ["SessionFileStager"]
