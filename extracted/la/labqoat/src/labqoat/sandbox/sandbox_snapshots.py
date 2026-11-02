"""Snapshots of one sandbox's filesystem or of one of its directories."""

from typing import ClassVar

from labqoat.json_document import JsonDocument
from labqoat.sandbox.sandbox_files import SandboxFiles
from labqoat.sandbox.sandbox_request import SandboxRequest
from labqoat.sandbox.sandbox_response import SandboxResponse


class SandboxSnapshots(SandboxFiles):
    """Snapshot what a sandbox holds as an image, as Modal does, and put directory snapshots into sandboxes.

    ``snapshot_filesystem`` captures the whole filesystem: pass the image it returns as ``image=`` to start new
    sandboxes from it, with the original image's environment and working directory. ``snapshot_directory``
    captures one directory, which ``mount_image`` puts into any running sandbox, replacing what that directory
    held. Mounted volumes and system directories are never captured. Snapshots are kept for 30 days.
    """

    SNAPSHOT_SECONDS: ClassVar[float] = 1800.0

    def snapshot_filesystem(self) -> str:
        """Capture the sandbox's whole filesystem and return the image reference new sandboxes start from."""
        return self._image(self.transport.send(self._snapshot_request("/")))

    async def snapshot_filesystem_async(self) -> str:
        """Capture the filesystem without blocking the event loop; see ``snapshot_filesystem``."""
        return self._image(await self.transport.send_async(self._snapshot_request("/")))

    def snapshot_directory(self, path: str) -> str:
        """Capture the directory at ``path`` and return the image reference ``mount_image`` takes."""
        return self._image(self.transport.send(self._snapshot_request(path)))

    async def snapshot_directory_async(self, path: str) -> str:
        """Capture a directory without blocking the event loop; see ``snapshot_directory``."""
        return self._image(await self.transport.send_async(self._snapshot_request(path)))

    def mount_image(self, path: str, image: str) -> None:
        """Replace what the directory at ``path`` holds with a directory snapshot, creating it if absent."""
        self.transport.send(self._mount_request(path, image))

    async def mount_image_async(self, path: str, image: str) -> None:
        """Put a directory snapshot into the sandbox without blocking the event loop; see ``mount_image``."""
        await self.transport.send_async(self._mount_request(path, image))

    def _snapshot_request(self, path: str) -> SandboxRequest:
        """Ask the host to capture ``path``, which may take as long as the sandbox's files take to pack."""
        document = {"path": self._absolute(path)}
        return SandboxRequest("POST", f"{self._path}/snapshot", document=document, timeout=self.SNAPSHOT_SECONDS)

    def _mount_request(self, path: str, image: str) -> SandboxRequest:
        """Ask the host to put ``image`` at ``path``."""
        document = {"path": self._absolute(path), "image": image}
        return SandboxRequest("POST", f"{self._path}/mount", document=document, timeout=self.SNAPSHOT_SECONDS)

    @staticmethod
    def _absolute(path: str) -> str:
        """Refuse a relative path before anything is sent."""
        if not path.startswith("/"):
            raise ValueError(f"Snapshot paths are absolute, not {path!r}")
        return path

    @staticmethod
    def _image(content: bytes) -> str:
        """The image reference the host answered with."""
        return SandboxResponse.decoded(content, SandboxSnapshots._reference)

    @staticmethod
    def _reference(document: JsonDocument) -> str:
        """Read the image reference out of the host's answer."""
        return JsonDocument.expect_scalar(document["image"], str)
