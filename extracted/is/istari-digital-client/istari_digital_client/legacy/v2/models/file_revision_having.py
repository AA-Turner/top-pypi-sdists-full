import abc
from pydantic import BaseModel

from istari_digital_client.legacy.v2.models.file_revision import FileRevision
from istari_digital_client.legacy.v2.models.readable import Readable
from istari_digital_client.legacy.v2.models.properties import Properties
from istari_digital_client.legacy.log_utils import log_method


class FileRevisionHaving(BaseModel, Readable, abc.ABC):
    """
    Mixin for objects that expose a ``FileRevision`` and delegate common behaviors to it.

    Provides convenience access to revision properties, metadata, and content.
    Subclasses must implement the ``revision`` property.
    """

    @property
    @abc.abstractmethod
    def revision(self) -> FileRevision:
        """
        Abstract property that must return the associated ``FileRevision`` instance.
        """
        ...

    def read_bytes(self) -> bytes:
        """
        Read and return the raw byte contents of the associated file revision.
        """

        return self.revision.read_bytes()

    @property
    @log_method
    def properties(self) -> Properties:
        """
        Return the file metadata properties from the associated revision.
        """

        return self.revision.read_properties()

    @property
    @log_method
    def extension(self) -> str | None:
        """
        Return the file extension (lowercased, without dot) from the associated revision.
        """

        return self.revision.extension

    @property
    @log_method
    def name(self) -> str | None:
        """
        Return the full file name with extension.

        If ``revision.name`` already ends with the extension (case-insensitive), it is returned as-is.
        Otherwise, the extension is appended.
        """

        if self.revision.name is None or self.extension is None:
            return None

        file_name = self.revision.name
        if file_name.lower().endswith(f".{self.extension}"):
            return file_name
        return ".".join([file_name, self.extension])

    @property
    @log_method
    def stem(self) -> str | None:
        """
        Return the file name without its suffix from the associated revision.
        """

        return self.revision.stem

    @property
    @log_method
    def suffix(self) -> str | None:
        """
        Return the file suffix (with dot and original casing) from the associated revision.
        """

        return self.revision.suffix

    @property
    @log_method
    def description(self) -> str | None:
        """
        Return the description set on the file revision, if any.
        """

        return self.revision.description

    @property
    @log_method
    def size(self) -> int | None:
        """
        Return the file size in bytes from the associated revision.
        """

        return self.revision.size

    @property
    @log_method
    def mime(self) -> str | None:
        """
        Return the MIME type of the file from the associated revision.
        """

        return self.revision.mime

    @property
    @log_method
    def version_name(self) -> str | None:
        """
        Return the version label assigned to the file revision.
        """

        return self.revision.version_name

    @property
    @log_method
    def external_identifier(self) -> str | None:
        """
        Return the external system identifier assigned to the file revision, if any.
        """

        return self.revision.external_identifier

    @property
    @log_method
    def display_name(self) -> str | None:
        """
        Return the human-readable display name of the file revision, if set.
        """

        return self.revision.display_name
