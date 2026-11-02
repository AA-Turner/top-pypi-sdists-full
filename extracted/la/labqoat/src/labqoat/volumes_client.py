"""A project's volumes: create, list and remove them, and copy files in and out."""

from __future__ import annotations

import builtins
from pathlib import Path

from labqoat._generated.volume import Volume
from labqoat._generated.volume_list import VolumeList
from labqoat.base_client import BaseClient
from labqoat.errors.api_error import ApiError
from labqoat.volumes.client_volume_api import ClientVolumeApi
from labqoat.volumes.volume_entry import VolumeEntry
from labqoat.volumes.volume_files import VolumeFiles


class VolumesClient(BaseClient):
    """Volumes of the client's selected project; file content moves straight to and from platform storage."""

    def list(self) -> VolumeList:
        """List the project's volumes with their versions, file counts and sizes."""
        path = "/api/v1/volumes"
        return self.decode(self.send("GET", path), path, VolumeList.from_dict)

    def create(self, name: str) -> Volume:
        """Create an empty volume; a function mounting a missing volume creates it too."""
        path = "/api/v1/volumes"
        return self.decode(self.send_json("POST", path, {"name": name}), path, Volume.from_dict)

    def get(self, name: str) -> Volume:
        """Read one volume's version, file count and size."""
        path = f"/api/v1/volumes/{self.encode_ref(name)}"
        return self.decode(self.send("GET", path), path, Volume.from_dict)

    def delete(self, name: str) -> None:
        """Remove a volume and everything in it; its name is free again at once."""
        path = f"/api/v1/volumes/{self.encode_ref(name)}"
        response = self.send("DELETE", path)
        if response.status_code != 204:
            raise ApiError("Expected an empty deletion response.", status=response.status_code)

    def entries(self, name: str, path: str = "", *, recursive: bool = False) -> tuple[int, builtins.list[VolumeEntry]]:
        """The volume's version and what it holds at ``path``: a directory's children, or all below it."""
        return ClientVolumeApi(self, name).entries(VolumeFiles.remote(path), recursive)

    def put(self, name: str, local: str | Path, remote: str = "") -> int:
        """Copy a local file or directory's contents into the volume at ``remote`` and return the new version.

        A file goes to ``remote`` itself, or into it when ``remote`` is empty or ends with ``/``. Only blocks
        storage does not hold yet are sent, so repeating an interrupted put resumes it.
        """
        return VolumeFiles(ClientVolumeApi(self, name)).put(Path(local), remote)

    def download(self, name: str, remote: str, local: str | Path) -> int:
        """Copy what the volume holds at ``remote`` to ``local`` and return how many files were written.

        Files already present with the same content are skipped, and a partly downloaded file resumes.
        """
        return VolumeFiles(ClientVolumeApi(self, name)).get(VolumeFiles.remote(remote), Path(local))

    def remove(self, name: str, path: str, *, recursive: bool = False) -> int:
        """Remove ``path`` from the volume, a non-empty directory only when ``recursive``; return the version."""
        return VolumeFiles(ClientVolumeApi(self, name)).remove(VolumeFiles.remote(path), recursive=recursive)
