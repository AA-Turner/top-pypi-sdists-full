"""Models for downloads json."""

from __future__ import annotations

from typing import Any, Dict, NamedTuple, Optional

from db_contrib_tool.config import DownloadTarget


class Releases(NamedTuple):
    """
    Representation of downloads json.

    * versions: From version number to release metadata dict.
    * git_hashes: From git hash to release metadata dict.
    """

    versions: Dict[str, Release]
    git_hashes: Dict[str, Release]

    @classmethod
    def from_json(cls, full_json: Dict[str, Any]) -> Releases:
        """
        Make list of releases from the given json.

        :param full_json: Downloads json as dict.
        :return: Releases.
        """
        versions = [
            Release.from_json(version_json)
            for version_json in full_json.get("versions", [])
            if Release.is_parsable(version_json)
        ]
        return cls(
            versions={version.version: version for version in versions},
            git_hashes={version.git_hash: version for version in versions},
        )


class Release(NamedTuple):
    """
    MongoDB release metadata.

    * version: MongoDB released version number.
    * git_hash: Git hash of the release version.
    * builds: List of builds.
    """

    version: str
    git_hash: str
    builds: Dict[BuildMetadataKey, DownloadMetadata]

    @classmethod
    def is_parsable(cls, version_json: Dict[str, Any]) -> bool:
        """
        Check if version json can be parsed.

        :param version_json: Version json as dict.
        :return: True if parsable.
        """
        return all(key in version_json for key in ["version", "githash", "downloads"])

    @classmethod
    def from_json(cls, version_json: Dict[str, Any]) -> Release:
        """
        Make release instance from the given json.

        :param version_json: Version json as dict.
        :return: Release.
        """
        downloads = [
            DownloadMetadata.from_json(download_json)
            for download_json in version_json["downloads"]
            if DownloadMetadata.is_parsable(download_json)
        ]
        return cls(
            version=version_json["version"],
            git_hash=version_json["githash"],
            builds={
                BuildMetadataKey.from_download_metadata(download): download
                for download in downloads
            },
        )


class BuildMetadataKey(NamedTuple):
    """Representation of build metadata key."""

    arch: str
    edition: str
    target: str

    def __hash__(self) -> int:
        """Return object hash value."""
        return hash((self.arch, self.edition, self.target))

    def __eq__(self, other: object) -> bool:
        """Keys are identical if all their attributes are identical."""
        if isinstance(other, self.__class__):
            return (
                other.arch == self.arch
                and other.edition == self.edition
                and other.target == self.target
            )
        return False

    @classmethod
    def from_download_metadata(cls, download_metadata: DownloadMetadata) -> BuildMetadataKey:
        """
        Make build metadata key instance from the given download metadata.

        :param download_metadata: Download metadata.
        :return: Build metadata key.
        """
        return cls(
            arch=download_metadata.arch,
            edition=download_metadata.edition,
            target=download_metadata.target,
        )

    @classmethod
    def from_download_target(cls, target: DownloadTarget) -> BuildMetadataKey:
        """
        Make build metadata key instance from the given download target.

        :param target: Attributes of the build to download.
        :return: Build metadata key.
        """
        return cls(
            arch=target.architecture,
            edition=target.edition,
            target=target.platform or "",
        )


class DownloadMetadata(NamedTuple):
    """
    Download metadata for the build.

    * arch: Build architecture, e.g. `x86_64`.
    * edition: Build edition, e.g. `enterprise`.
    * target: Build target platform, e.g. `ubuntu2204`.
    * urls: List of URLs to download build from.
    """

    arch: str
    edition: str
    target: str
    urls: ReleaseUrls

    @classmethod
    def is_parsable(cls, download_metadata_json: Dict[str, Any]) -> bool:
        """
        Check if download metadata json can be parsed.

        :param download_metadata_json: Download metadata json as dict.
        :return: True if parsable.
        """
        return all(
            key in download_metadata_json for key in ["arch", "edition", "target", "archive"]
        )

    @classmethod
    def from_json(cls, download_metadata_json: Dict[str, Any]) -> DownloadMetadata:
        """
        Parse download metadata instance from json.

        :param download_metadata_json: Download metadata json as dict.
        :return: Download metadata.
        """
        return cls(
            arch=download_metadata_json["arch"],
            edition=download_metadata_json["edition"],
            target=download_metadata_json["target"],
            urls=ReleaseUrls(
                binary=download_metadata_json["archive"].get("url"),
                debug_symbols=download_metadata_json["archive"].get("debug_symbols"),
            ),
        )


class ReleaseUrls(NamedTuple):
    """
    URLs to download build from.

    * binary: URL to binary archive.
    * debug_symbols: URL to debug symbols archive.
    """

    binary: Optional[str] = None
    debug_symbols: Optional[str] = None
