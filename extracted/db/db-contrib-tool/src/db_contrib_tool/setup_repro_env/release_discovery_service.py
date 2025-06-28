"""A service for finding MongoDB releases."""

import http
from functools import cmp_to_key, lru_cache
from typing import List, Optional

import inject
import requests
import structlog
from packaging.version import parse
from retry import retry

from db_contrib_tool.config import DownloadTarget
from db_contrib_tool.services.platform_service import PlatformService
from db_contrib_tool.setup_repro_env.release_models import BuildMetadataKey, Release, Releases
from db_contrib_tool.setup_repro_env.request_models import (
    ReleaseUrlsInfo,
    RequestTarget,
    RequestType,
)

LOGGER = structlog.get_logger(__name__)
DOWNLOADS_JSON_URL = "https://downloads.mongodb.org/cloud.json"


class DownloadsJsonClient:
    """A client to fetch metadata about MongoDB releases."""

    @staticmethod
    @lru_cache()
    @retry(tries=3, delay=3)
    def get_releases() -> Releases:
        """Get the list of MongoDB releases."""
        response = requests.get(DOWNLOADS_JSON_URL)
        if response.status_code != http.HTTPStatus.OK:
            raise RuntimeError("Http response for release json file was not 200")
        downloads_json = response.json()
        return Releases.from_json(downloads_json)


class ReleaseDiscoveryService:
    """A service for finding releases."""

    @inject.autoparams()
    def __init__(
        self, downloads_json_client: DownloadsJsonClient, platform_service: PlatformService
    ) -> None:
        """Initialize."""
        self.downloads_json_client = downloads_json_client
        self.platform_service = platform_service

    def find_release_urls(
        self, request: RequestTarget, target: DownloadTarget
    ) -> Optional[ReleaseUrlsInfo]:
        """
        Find release URLs for the given request.

        :param request: Request of mongo instance to find.
        :param target: Attributes of the build to download.
        :return: Links to found releases.
        """
        if not target.is_complete():
            target_platform = self.platform_service.infer_platform()
            target = DownloadTarget(
                architecture=target.architecture, edition=target.edition, platform=target_platform
            )

        release = self.find_release(request)
        if release is None:
            LOGGER.info("Release not found", request=request)
            return None

        LOGGER.info("Release found", request=request)
        build_metadata_key = BuildMetadataKey.from_download_target(target)
        build = release.builds.get(build_metadata_key)
        if build is None:
            LOGGER.info("Build not found", build_metadata=build_metadata_key)
            return None

        LOGGER.info("Build found", build_metadata=build_metadata_key)
        return ReleaseUrlsInfo(urls=build.urls, git_hash=release.git_hash)

    def find_release(self, request: RequestTarget) -> Optional[Release]:
        """
        Find release given the request target.

        :param request: Request of mongo instance to find.
        :return: Release metadata.
        """
        releases = self.downloads_json_client.get_releases()

        if request.request_type == RequestType.MONGO_RELEASE_VERSION:
            version = self.get_latest_version(
                [
                    version
                    for version in releases.versions.keys()
                    if version.startswith(request.identifier)
                ]
            )
            if version is not None:
                LOGGER.info("Found the latest version", version=version)
                return releases.versions.get(version)

        elif request.request_type == RequestType.MONGO_PATCH_VERSION:
            return releases.versions.get(request.identifier)

        elif request.request_type == RequestType.GIT_COMMIT:
            return releases.git_hashes.get(request.identifier)

        return None

    def get_latest_version(self, versions: List[str]) -> Optional[str]:
        """
        Calculate the latest version number.

        :param versions: List of version numbers.
        :return: The latest version number.
        """
        if len(versions) == 0:
            return None
        versions.sort(key=cmp_to_key(self.compare_versions))
        return versions[-1]

    @staticmethod
    def compare_versions(version_1: str, version_2: str) -> int:
        """
        Compare version strings.

        :param version_1: 1st version string.
        :param version_2: 2nd version string.
        :return: `1` if 1st version is bigger, if 2nd - `-1`, if equals - `0`.
        """
        parsed_version_1 = parse(version_1)
        parsed_version_2 = parse(version_2)
        if parsed_version_1 > parsed_version_2:
            return 1
        if parsed_version_1 < parsed_version_2:
            return -1
        return 0
