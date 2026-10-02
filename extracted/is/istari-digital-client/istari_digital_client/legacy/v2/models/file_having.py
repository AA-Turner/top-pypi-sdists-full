import abc
from typing import List, Optional

from istari_digital_client.legacy.v2.models.file import File
from istari_digital_client.legacy.v2.models.file_revision import FileRevision
from istari_digital_client.legacy.v2.models.file_revision_having import FileRevisionHaving
from istari_digital_client.legacy.log_utils import log_method


class FileHaving(FileRevisionHaving, abc.ABC):
    """
    Mixin for objects that contain a ``file`` and expose file revision behavior.

    Provides access to the file’s revisions and metadata update methods by
    delegating to the underlying ``File`` instance.
    """

    @property
    def _file(self) -> File:
        """
        Internal accessor for the ``file`` attribute.

        :raises ValueError: If the ``file`` attribute is not set.
        """

        file = getattr(self, "file", None)

        if file is None:
            raise ValueError("file is not set")

        return file

    @property
    @log_method
    def revisions(self) -> List[FileRevision]:
        """
        Return the list of revisions from the underlying file.
        """

        return self._file.revisions

    @property
    @log_method
    def revision(self) -> FileRevision:
        """
        Return the most recent revision from the file's revision list.
        """

        return self.revisions[-1]

    @log_method
    def update_properties(
        self,
        description: Optional[str] = None,
        display_name: Optional[str] = None,
        external_identifier: Optional[str] = None,
        version_name: Optional[str] = None,
    ) -> File:
        """
        Update one or more metadata fields on the underlying file.

        Delegates to the file’s ``update_properties()`` method.

        :param description: Optional file description.
        :type description: str or None
        :param display_name: Optional human-readable name for the file.
        :type display_name: str or None
        :param external_identifier: Optional external identifier.
        :type external_identifier: str or None
        :param version_name: Optional version label.
        :type version_name: str or None
        """

        return self._file.update_properties(
            description, display_name, external_identifier, version_name
        )

    @log_method
    def update_description(self, description: str) -> File:
        """
        Update the file's description.

        :param description: New description text.
        :type description: str
        """

        return self._file.update_description(description)

    @log_method
    def update_display_name(self, display_name: str) -> File:
        """
        Update the file's display name.

        :param display_name: New display name.
        :type display_name: str
        """

        return self._file.update_display_name(display_name)

    @log_method
    def update_external_identifier(self, external_identifier: str) -> File:
        """
        Update the file's external identifier.

        :param external_identifier: New external ID value.
        :type external_identifier: str
        """

        return self._file.update_external_identifier(external_identifier)

    @log_method
    def update_version_name(self, version_name: str) -> File:
        """
        Update the file's version name.

        :param version_name: New version name.
        :type version_name: str
        """

        return self._file.update_version_name(version_name)
