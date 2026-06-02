"""A service for finding MongoDB releases."""

import http
import json
from abc import ABC, abstractmethod
from enum import Enum
from functools import cmp_to_key
from typing import Any, Dict, List, Optional

import boto3
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
ATLAS_FEED_BUCKET = "origin-mongodb-server-atlas"
ATLAS_FEED_KEY = "server/feeds/all.json"


class ReleaseSource(str, Enum):
    """Source of MongoDB release metadata."""

    PUBLIC_FEED = "public"  # https://downloads.mongodb.org/cloud.json
    ATLAS_FEED = "atlas"  # s3://origin-mongodb-server-atlas/server/feeds/all.json


class ReleaseFeedProvider(ABC):
    """A provider of MongoDB release metadata."""

    def __init__(self) -> None:
        """Initialize."""
        self._cached_releases: Optional[Releases] = None

    def get_releases(self) -> Releases:
        """Get the list of MongoDB releases, caching the result."""
        if self._cached_releases is None:
            self._cached_releases = Releases.from_json(self._fetch())
        return self._cached_releases

    @abstractmethod
    def _fetch(self) -> Dict[str, Any]:
        """Fetch the raw release metadata json from the feed."""
        raise NotImplementedError


class PublicReleaseFeedProvider(ReleaseFeedProvider):
    """Fetch release metadata from the public downloads feed over HTTP."""

    @retry(tries=3, delay=3)
    def _fetch(self) -> Dict[str, Any]:
        """Fetch release metadata from the public downloads feed over HTTP."""
        LOGGER.info("Fetching public release feed json file", url=DOWNLOADS_JSON_URL)
        response = requests.get(DOWNLOADS_JSON_URL)
        if response.status_code != http.HTTPStatus.OK:
            raise RuntimeError("Http response for release json file was not 200")
        return response.json()


class AtlasReleaseFeedProvider(ReleaseFeedProvider):
    """Fetch release metadata from the Atlas S3 feed.

    Uses the default boto3 credential chain (env vars, ~/.aws, profiles,
    instance role).
    """

    def _fetch(self) -> Dict[str, Any]:
        """Fetch release metadata from the Atlas S3 feed."""
        LOGGER.info(
            "Fetching Atlas release feed json file",
            s3_bucket=ATLAS_FEED_BUCKET,
            object=ATLAS_FEED_KEY,
        )
        try:
            s3 = boto3.client("s3")
            obj = s3.get_object(Bucket=ATLAS_FEED_BUCKET, Key=ATLAS_FEED_KEY)
        except Exception as e:
            raise RuntimeError("Failed to download Atlas release feed json file") from e
        return json.loads(obj["Body"].read())


def release_feed_provider_for(source: ReleaseSource) -> ReleaseFeedProvider:
    """Build the release feed provider matching the given source."""
    if source is ReleaseSource.ATLAS_FEED:
        return AtlasReleaseFeedProvider()
    return PublicReleaseFeedProvider()


class ReleaseDiscoveryService:
    """A service for finding releases."""

    @inject.autoparams()
    def __init__(
        self,
        release_feed_provider: ReleaseFeedProvider,
        platform_service: PlatformService,
    ) -> None:
        """Initialize."""
        self.release_feed_provider = release_feed_provider
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
        releases = self.release_feed_provider.get_releases()

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
