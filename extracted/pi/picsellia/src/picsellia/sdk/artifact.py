import logging

import orjson
from beartype import beartype

from picsellia.colors import Colors
from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.sdk.downloadable import Downloadable
from picsellia.types.schemas import ArtifactSchema
from picsellia.utils import filter_payload

logger = logging.getLogger("picsellia")


class Artifact(Dao, Downloadable):
    def __init__(self, connexion: Connection, data: dict):
        Dao.__init__(self, connexion, data)
        Downloadable.__init__(self)

    def __str__(self):
        return f"{Colors.GREEN}Artifact {self.name}{Colors.ENDC} (id: {self.id})"

    @property
    def filename(self) -> str:
        """Filename of this (Artifact)"""
        return self._filename

    @property
    def large(self) -> bool:
        """If true, this (Artifact) has a large size"""
        return self._large

    @property
    def name(self) -> str:
        """(Artifact) name"""
        return self._name

    @property
    def object_name(self) -> str:
        """(Artifact) object name stored in storage"""
        return self._object_name

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> ArtifactSchema:
        schema = ArtifactSchema(**data)
        self._name = schema.name
        self._object_name = schema.object_name
        self._large = schema.large
        self._filename = schema.filename
        self._url = schema.url
        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"/api/artifact/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def reset_url(self) -> str:
        """Reset url property of this Artifact by calling platform.

        Returns:
            A url as str of this Artifact.
        """
        self._url = self.connection.init_download(self.object_name)
        return self._url

    @exception_handler
    @beartype
    def update(
        self,
        name: str | None = None,
        filename: str | None = None,
        object_name: str | None = None,
        large: bool | None = None,
    ) -> None:
        """Update this artifact with a new name, filename, object_name or large

        Examples:
            ```python
            this_artifact.update(object_name="another-path-to-artifact")
            ```

        Arguments:
            name (str, optional): New name of the artifact. Defaults to None.
            filename (str, optional): New filename of the artifact. Defaults to None.
            object_name (str, optional): New object_name of the artifact. Defaults to None.
            large (bool, optional): New large of the artifact. Defaults to None.
        """
        payload = {
            "name": name,
            "filename": filename,
            "object_name": object_name,
            "large": large,
        }
        filtered_payload = filter_payload(payload)
        r = self.connection.patch(
            f"/api/artifact/{self.id}", data=orjson.dumps(filtered_payload)
        ).json()
        self.refresh(r)

    @exception_handler
    @beartype
    def delete(self) -> None:
        """Delete this artifact

        Examples:
            ```python
            this_artifact.delete()
            ```
        """
        self.connection.delete(f"/api/artifact/{self.id}")
