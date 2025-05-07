"""Setup MongoDB repro environment."""

import json
import os
import pathlib
import re
from typing import List, NamedTuple, Optional, Set

import inject
import structlog

from db_contrib_tool.clients.download_client import DownloadError
from db_contrib_tool.clients.file_service import FileService
from db_contrib_tool.clients.resmoke_proxy import ResmokeProxy
from db_contrib_tool.config import (
    CONTINUOUS_RELEASE_ALIAS,
    LTS_RELEASE_ALIAS,
    WINDOWS_BIN_PATHS_FILE,
    DownloadTarget,
)
from db_contrib_tool.services.evergreen_service import EvergreenService
from db_contrib_tool.setup_repro_env.artifact_discovery_service import (
    ArtifactDiscoveryService,
    EvergreenVersionIsTooOld,
    MissingBuildVariantError,
)
from db_contrib_tool.setup_repro_env.download_service import (
    ArtifactDownloadService,
    DownloadOptions,
)
from db_contrib_tool.setup_repro_env.release_discovery_service import ReleaseDiscoveryService
from db_contrib_tool.setup_repro_env.request_models import (
    DownloadRequest,
    RequestTarget,
    RequestType,
    EvgUrlsInfo,
)
from db_contrib_tool.utils import is_windows

BINARY_ARTIFACT_NAME = "Binaries"
KNOWN_BRANCHES = {"master"}
RELEASE_VERSION_RE = re.compile(r"^\d+\.\d+$")
PATCH_VERSION_RE = re.compile(r"^\d+\.\d+\.\d+")
BRANCH_RE = re.compile(r"^v\d+\.\d+")
EXTERNAL_LOGGERS = [
    "evergreen",
    "github",
    "inject",
    "urllib3",
]

LOGGER = structlog.getLogger(__name__)


class SetupReproParameters(NamedTuple):
    """
    Parameters describing how a repro environment should be setup.

    * edition: MongoDB edition to download.
    * platform: Target platform to download.
    * architecture: Target architecture to download.
    * variant: Build Variant to download from.

    * versions: List of items to download.
    * ignore_failed_push: Download version even if the push task failed.
    * fallback_to_master: Should the latest master be downloaded if the version doesn't exist.

    * evg_versions_file: Write which evergreen versions were downloaded from to this file.

    * download_options: Options specifying how downloads should occur.
    """

    edition: str
    platform: Optional[str]
    architecture: str
    variant: Optional[str]

    versions: List[str]
    ignore_failed_push: bool
    fallback_to_master: bool

    evg_versions_file: Optional[str]

    download_options: DownloadOptions

    def get_download_target(self, platform: Optional[str] = None) -> DownloadTarget:
        """
        Get the download target to use based on these parameters.

        :param platform: Override the platform with this platform.
        :return: Download target specified by this options.
        """
        platform = platform if platform is not None else self.platform
        return DownloadTarget(
            edition=self.edition, platform=platform, architecture=self.architecture
        )


class SetupReproOrchestrator:
    """Orchestrator for setting up repro environments."""

    @inject.autoparams()
    def __init__(
        self,
        evg_service: EvergreenService,
        resmoke_proxy: ResmokeProxy,
        artifact_download_service: ArtifactDownloadService,
        artifact_discovery_service: ArtifactDiscoveryService,
        release_discovery_service: ReleaseDiscoveryService,
        file_service: FileService,
    ) -> None:
        """
        Initialize the orchestrator.

        :param evg_service: Service for working with evergreen.
        :param resmoke_proxy: Proxy for working with resmoke.
        :param artifact_download_service: Service to download artifacts.
        :param artifact_discovery_service: Service to find artifacts.
        :param release_discovery_service: Service to find releases.
        :param file_service: Service to work with the filesystem.
        """
        self.evg_service = evg_service
        self.resmoke_proxy = resmoke_proxy
        self.artifact_download_service = artifact_download_service
        self.artifact_discovery_service = artifact_discovery_service
        self.release_discovery_service = release_discovery_service
        self.file_service = file_service

    def interpret_discovery_request(self, request: str) -> RequestTarget:
        """
        Translate the request from the user into an item we can understand.

        :param request: Request from user.
        :return: Targeted request to download.
        """
        if "=" in request:
            version, bin_suffix = request.split("=", 1)
        else:
            version, bin_suffix = request, None

        request_type = RequestType.GIT_COMMIT
        identifier = version

        if version.endswith(".json") and pathlib.Path(version).is_file():
            request_type = RequestType.VERSIONS_FILE
            identifier = version
            if bin_suffix is not None:
                LOGGER.warning(
                    "Binary suffix is ignored when using an existing versions file.",
                    bin_suffix=bin_suffix,
                )
        elif version in [LTS_RELEASE_ALIAS, CONTINUOUS_RELEASE_ALIAS]:
            request_type = RequestType.MONGO_RELEASE_VERSION
            identifier = self._get_release_version(version)
        elif version in KNOWN_BRANCHES or BRANCH_RE.match(version):
            request_type = RequestType.GIT_BRANCH
        elif RELEASE_VERSION_RE.match(version):
            request_type = RequestType.MONGO_RELEASE_VERSION
        elif PATCH_VERSION_RE.match(version):
            request_type = RequestType.MONGO_PATCH_VERSION
        elif self.evg_service.query_task_existence(version):
            request_type = RequestType.EVG_TASK
        elif self.evg_service.query_version_existence(version):
            request_type = RequestType.EVG_VERSION

        if bin_suffix in [LTS_RELEASE_ALIAS, CONTINUOUS_RELEASE_ALIAS]:
            bin_suffix = self._get_release_version(bin_suffix)

        request_target = RequestTarget(
            request_type=request_type,
            identifier=identifier,
            bin_suffix=bin_suffix,
        )

        LOGGER.debug("Interpreted setup request", original=request, interpreted=request_target)

        return request_target

    def interpret_discovery_requests(self, request_list: List[str]) -> List[RequestTarget]:
        """
        Translate all the requests from the user into a request for discovering the download information.

        :param request_list: Requests from user.
        :return: List of targeted request to download.
        """
        requests = [self.interpret_discovery_request(request) for request in request_list]

        return requests

    def _get_release_version(self, version_alias: str) -> str:
        """
        Translate version alias to a release version.

        :param version_alias: Alias like `last-lts`, `last-continuous`.
        :return: Release version.
        """
        multiversionconstants = self.resmoke_proxy.get_multiversion_constants()

        releases = {
            LTS_RELEASE_ALIAS: multiversionconstants.last_lts_fcv,
            CONTINUOUS_RELEASE_ALIAS: multiversionconstants.last_continuous_fcv,
        }

        release_version = releases[version_alias]
        LOGGER.debug("Got release version from alias", alias=version_alias, release=release_version)

        return release_version

    @staticmethod
    def _get_bin_suffix(request: RequestTarget, evg_project_id: str) -> str:
        """
        Get the multiversion bin suffix from the evergreen project ID.

        :param request: Targeted request to download.
        :param evg_project_id: Evergreen project ID.
        :return: Bin suffix.
        """
        if request.bin_suffix is not None:
            return request.bin_suffix

        if re.match(r"(\d+\.\d+)", request.identifier):
            # If the cmdline version is already a semvar, just use that.
            return request.identifier

        project_version_search = re.search(r"(\d+\.\d+$)", evg_project_id)
        if project_version_search:
            # Extract version from the Evergreen project ID as fallback.
            return project_version_search.group(0)

        # If the version is not a semvar, we can't add a suffix.
        return ""

    def execute(self, setup_repro_params: SetupReproParameters) -> bool:
        """
        Execute setup repro env mongodb.

        :param setup_repro_params: Setup repro env parameters.
        :return: Whether succeeded or not.
        """
        discovery_request_list = self.interpret_discovery_requests(setup_repro_params.versions)

        downloaded_versions = {}
        failed_requests = []
        link_directories = []

        download_target = setup_repro_params.get_download_target()
        LOGGER.info("Search criteria", search_criteria=download_target)

        download_request_set: Set[DownloadRequest] = set()

        for discovery_request in discovery_request_list:
            LOGGER.info("Setting up request", request=discovery_request)

            if discovery_request.request_type == RequestType.VERSIONS_FILE:
                LOGGER.info("Using download URLs from provided versions file")
                with open(discovery_request.identifier, "r") as fh:
                    versions = json.load(fh)
                    for bin_suffix, info in versions.items():
                        evg_urls_info: Optional[EvgUrlsInfo] = EvgUrlsInfo(**info)
                        download_request = DownloadRequest(
                            bin_suffix, discovery_request, evg_urls_info, None
                        )
                        download_request_set.add(download_request)
                continue

            try:
                LOGGER.info("Fetching download URLs from Evergreen")
                evg_urls_info = self.artifact_discovery_service.find_artifacts(
                    discovery_request,
                    setup_repro_params.variant,
                    download_target,
                    setup_repro_params.ignore_failed_push,
                    setup_repro_params.fallback_to_master,
                )
            except (EvergreenVersionIsTooOld, MissingBuildVariantError, ValueError) as err:
                LOGGER.warning("Could not find URLs in Evergreen", error=err)
                evg_urls_info = None

            LOGGER.info("Fetching fallback download URLs from Downloads json")
            release_urls_info = self.release_discovery_service.find_release_urls(
                discovery_request, download_target
            )

            bin_suffix = self._get_bin_suffix(
                discovery_request,
                evg_urls_info.project_identifier if evg_urls_info else "",
            )
            download_request = DownloadRequest(
                bin_suffix, discovery_request, evg_urls_info, release_urls_info
            )
            download_request_set.add(download_request)

        for download_request in download_request_set:
            try:
                linked_dir = self.artifact_download_service.download_and_extract(
                    download_request,
                    setup_repro_params.download_options,
                )
                if linked_dir:
                    link_directories.append(linked_dir)
                downloaded_versions[download_request.bin_suffix] = (
                    download_request.evg_urls_info._asdict()
                    if download_request.evg_urls_info
                    else {}
                )
                LOGGER.info("Setup request completed", request=download_request.discovery_request)
            except DownloadError:
                failed_requests.append(download_request.discovery_request)
                LOGGER.error(
                    "Setup request failed",
                    request=download_request.discovery_request,
                    exc_info=True,
                )

        if is_windows():
            self.file_service.write_windows_install_paths(WINDOWS_BIN_PATHS_FILE, link_directories)

        if setup_repro_params.evg_versions_file is not None:
            self.file_service.append_dict_to_json_file(
                setup_repro_params.evg_versions_file, downloaded_versions
            )
            LOGGER.info(
                "Finished writing downloaded Evergreen versions",
                target_file=os.path.abspath(setup_repro_params.evg_versions_file),
            )

        if failed_requests:
            LOGGER.error("Some requests were not able to setup.", failed_requests=failed_requests)
            return False

        LOGGER.info("Downloaded versions", request_list=discovery_request_list)
        return True
