from typing import Optional

from frogml_storage.models.entity_manifest import Checksums


class DownloadContext(object):
    """
    A class to represent the arguments for a download operation.

    Attributes
    ----------
    repo_key : str
        The key of the repository where the artifact is located.
    source_url : str
        The source relative URL of the artifact, relative to artifactory url and the repo key.
    target_path : str
        The target path where the artifact will be downloaded to.
    exists_locally : bool
        A flag indicating whether the artifact already exists locally in the target path.
    artifact_checksum: Checksums
        The checksum of the artifact.
    """

    repo_key: str
    source_url: str
    target_path: str
    exists_locally: bool = False
    artifact_checksum: Optional[Checksums]

    def __init__(
        self,
        repo_key: str,
        source_url: str,
        target_path: str,
        exists_locally: bool = False,
        artifact_checksum: Optional[Checksums] = None,
    ):
        self.repo_key = repo_key
        self.source_url = source_url
        self.target_path = target_path
        self.exists_locally = exists_locally
        self.artifact_checksum = artifact_checksum

    def __eq__(self, other):
        if not isinstance(other, DownloadContext):
            return False

        return (
            self.repo_key == other.repo_key
            and self.source_url == other.source_url
            and self.target_path == other.target_path
            and self.exists_locally == other.exists_locally
            and self.artifact_checksum == other.artifact_checksum
        )
