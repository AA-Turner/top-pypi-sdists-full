"""Directory trees moved through one uncompressed tar archive per transfer."""

import io
import tarfile
import uuid
from pathlib import Path


class DirectoryArchive:
    """Pack and unpack directory contents on both sides of the sandbox boundary.

    The sandbox protocol transfers single files, so a directory travels as one archive that ``tar`` reads or
    writes inside the sandbox. Archives stay uncompressed: they cross a local socket, and a task image need
    not ship a compressor.
    """

    @staticmethod
    def pack(source: Path) -> bytes:
        """Archive a local directory's contents, keeping modes and links and assigning every entry to root."""
        if not source.is_dir():
            raise NotADirectoryError(f"{source} is not a directory")
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w") as archive:
            archive.add(source, arcname=".", filter=DirectoryArchive._owned_by_root)
        return buffer.getvalue()

    @staticmethod
    def extract(content: bytes, destination: Path) -> None:
        """Unpack an archive a sandbox produced, skipping entries that would leave the destination.

        The archive is untrusted. Absolute paths, parent traversal, escaping links and device nodes are
        refused one entry at a time, so a stray pipe or link does not cost the rest of the directory.
        """
        destination.mkdir(parents=True, exist_ok=True)
        with tarfile.open(fileobj=io.BytesIO(content), mode="r:") as archive:
            for member in archive:
                try:
                    archive.extract(member, destination, filter="data")
                except tarfile.FilterError:
                    continue

    @staticmethod
    def remote_path() -> str:
        """Name a fresh archive inside a sandbox, outside any transferred directory."""
        return f"/tmp/.labqoat-transfer-{uuid.uuid4().hex}.tar"

    @staticmethod
    def pack_command(directory: str, archive: str) -> list[str]:
        """Archive a sandbox directory's contents into a sandbox file."""
        return ["tar", "-cf", archive, "-C", directory, "."]

    @staticmethod
    def unpack_command(archive: str, directory: str) -> list[str]:
        """Create a sandbox directory, unpack an uploaded archive into it, and remove the archive either way."""
        script = 'mkdir -p "$1" && tar -xf "$2" -C "$1"; status=$?; rm -f "$2"; exit "$status"'
        return ["sh", "-c", script, "sh", directory, archive]

    @staticmethod
    def _owned_by_root(member: tarfile.TarInfo) -> tarfile.TarInfo:
        """Drop the local owner: sandboxes run as root and know nothing of the caller's accounts."""
        member.uid = member.gid = 0
        member.uname = member.gname = "root"
        return member
