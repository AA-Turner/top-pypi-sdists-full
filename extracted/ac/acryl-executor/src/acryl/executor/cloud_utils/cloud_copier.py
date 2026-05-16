from abc import abstractmethod


class CloudCopier:
    """Abstract base class for uploading files to cloud storage.

    Implementations must override ``upload()``, which either returns the
    canonical cloud URI of the uploaded object or raises an exception on
    failure.  There is no silent-failure path.
    """

    @abstractmethod
    def upload(self, source_local_file: str, target_file: str) -> str:
        """Upload a local file to cloud storage.

        Args:
            source_local_file: Absolute path of the local file to upload.
            target_file: Relative destination path within the cloud storage
                location configured on this copier (e.g. a key suffix for S3).

        Returns:
            The canonical URI of the uploaded object (e.g. ``s3://bucket/key``).

        Raises:
            Exception: If the upload fails for any reason.
        """
