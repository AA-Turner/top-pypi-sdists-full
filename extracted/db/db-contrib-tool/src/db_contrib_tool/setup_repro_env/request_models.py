"""Setup request models."""

from __future__ import annotations

from enum import Enum
from typing import Dict, NamedTuple, Optional

from db_contrib_tool.setup_repro_env.release_models import ReleaseUrls

BRANCH_FALLBACK = "master"


class EvgUrlsInfo(NamedTuple):
    """Wrapper around Evergreen URLs with metadata."""

    urls: Dict[str, str]
    evg_version_id: str
    project_identifier: str
    evg_build_variant: str
    evg_revision: str
    is_patch: bool

    def get_unique_identifier(self) -> str:
        """
        Get unique identifier.

        Return evergreen revision, which is a git hash,
        and for patches append evergreen version id.
        """
        if self.is_patch:
            return f"{self.evg_revision}_{self.evg_version_id}"
        return self.evg_revision


class ReleaseUrlsInfo(NamedTuple):
    """Wrapper around Release URLs with metadata."""

    urls: ReleaseUrls
    git_hash: str


class RequestType(Enum):
    """
    How the mongo binaries are being requested.

    * git_commit: Get binaries from a specific commit.
    * git_branch: Get binaries from a specific git branch.
    * evg_version: Get binaries from a specific evergreen version.
    * evg_task: Get binaries from a specific evergreen task.
    * mongo_release_version: Get binaries for a release version of mongo (e.g. 4.4, 5.0, etc).
    * mongo_patch_version: Get binaries for a patch version of mongo (e.g. 4.2.18, 6.0.0-rc4, 6.1.0-alpha, etc).
    """

    GIT_COMMIT = "git_commit"
    GIT_BRANCH = "git_branch"
    EVG_VERSION = "evg_version"
    EVG_TASK = "evg_task"
    MONGO_RELEASE_VERSION = "mongo_release_version"
    MONGO_PATCH_VERSION = "mongo_patch_version"
    VERSIONS_FILE = "versions_file"

    def __str__(self) -> str:
        """Display item as a string."""
        return self.value


class RequestTarget(NamedTuple):
    """
    Version of mongo binaries that was requested.

    * request_type: Type of the identifier.
    * identifier: Identifier used to find request.
    * bin_suffix: Multiversion bin suffix.
    """

    request_type: RequestType
    identifier: str
    bin_suffix: Optional[str] = None

    def branch_fallback(self) -> RequestTarget:
        """
        Make a target from the current target for the default fallback branch.

        :return: Request target to download given release.
        """
        return RequestTarget(
            request_type=RequestType.GIT_BRANCH,
            identifier=BRANCH_FALLBACK,
            bin_suffix=self.bin_suffix,
        )

    def __str__(self) -> str:
        """Display item as a string."""
        return f"{self.request_type}({self.identifier})"


class DownloadRequest(NamedTuple):
    """Class representing the request to download a repro environment."""

    bin_suffix: str
    discovery_request: RequestTarget
    evg_urls_info: Optional[EvgUrlsInfo]
    release_urls_info: Optional[ReleaseUrlsInfo]

    def __hash__(self) -> int:
        """Return object hash value."""
        return hash((self.get_unique_identifier(), self.bin_suffix))

    def __eq__(self, other: object) -> bool:
        """Download objects are identical if evg version id, project id and name suffix are identical."""
        if isinstance(other, self.__class__):
            return (
                other.get_unique_identifier() == self.get_unique_identifier()
                and other.bin_suffix == self.bin_suffix
            )
        return False

    def get_unique_identifier(self) -> Optional[str]:
        """Get unique identifier from URLs metadata."""
        if self.evg_urls_info:
            return self.evg_urls_info.get_unique_identifier()
        if self.release_urls_info:
            return self.release_urls_info.git_hash
        return None

    def get_evergreen_urls(self) -> Dict[str, str]:
        """Get evergreen URLs."""
        if self.evg_urls_info is None:
            return {}
        return self.evg_urls_info.urls

    def get_release_urls(self) -> Optional[ReleaseUrls]:
        """Get release URLs."""
        if self.release_urls_info is None:
            return None
        return self.release_urls_info.urls
