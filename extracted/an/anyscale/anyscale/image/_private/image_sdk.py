import os
from typing import cast, List, Optional

from anyscale._private.anyscale_client.common import AnyscaleClientInterface
from anyscale._private.models.image_uri import ImageURI
from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.cli_logger import BlockLogger
from anyscale.image.models import ImageBuild, ImageBuildStatus
from anyscale.sdk.anyscale_client import (
    ClusterEnvironmentBuild,
    ClusterEnvironmentBuildStatus,
)


ENABLE_IMAGE_BUILD_FOR_TRACKED_REQUIREMENTS = (
    os.environ.get("ANYSCALE_ENABLE_IMAGE_BUILD_FOR_TRACKED_REQUIREMENTS", "0") == "1"
)


class PrivateImageSDK(BaseSDK):
    def __init__(
        self,
        *,
        logger: Optional[BlockLogger] = None,
        client: Optional[AnyscaleClientInterface] = None,
    ):
        super().__init__(logger=logger, client=client)
        self._enable_image_build_for_tracked_requirements = (
            ENABLE_IMAGE_BUILD_FOR_TRACKED_REQUIREMENTS
        )

    @property
    def enable_image_build_for_tracked_requirements(self) -> bool:
        return self._enable_image_build_for_tracked_requirements

    def get_default_image(self) -> str:
        return self.client.get_default_build_id()

    def get_image_build(self, build_id: str) -> Optional[ClusterEnvironmentBuild]:
        return self.client.get_cluster_env_build(build_id)

    _BACKEND_IMAGE_STATUS_TO_IMAGE_BUILD_STATUS = {
        ClusterEnvironmentBuildStatus.PENDING: ImageBuildStatus.IN_PROGRESS,
        ClusterEnvironmentBuildStatus.IN_PROGRESS: ImageBuildStatus.IN_PROGRESS,
        ClusterEnvironmentBuildStatus.SUCCEEDED: ImageBuildStatus.SUCCEEDED,
        ClusterEnvironmentBuildStatus.FAILED: ImageBuildStatus.FAILED,
        ClusterEnvironmentBuildStatus.PENDING_CANCELLATION: ImageBuildStatus.FAILED,
        ClusterEnvironmentBuildStatus.CANCELED: ImageBuildStatus.FAILED,
    }

    def _get_image_build_status(
        self, build: ClusterEnvironmentBuild
    ) -> ImageBuildStatus:
        return cast(
            ImageBuildStatus,
            self._BACKEND_IMAGE_STATUS_TO_IMAGE_BUILD_STATUS.get(
                build.status, ImageBuildStatus.UNKNOWN
            ),
        )

    def get(self, name: str) -> ImageBuild:
        if ":" in name:
            name, version = name.split(":", 2)
        else:
            version = None
        cluster_env = self.client.get_cluster_env_by_name(name=name)
        if cluster_env:
            build = None
            for b in self.client.list_cluster_env_builds(cluster_env.id):
                if version is None:
                    # use the latest
                    build = b
                    break
                if b.revision == int(version):
                    build = b
                    break

            if not build:
                raise RuntimeError(f"Version {version} not found for image {name}.")

            image_uri = ImageURI.from_cluster_env_build(
                cluster_env=cluster_env, build=build
            )
            return ImageBuild(
                status=self._get_image_build_status(build),
                uri=str(image_uri),
                ray_version=build.ray_version,
            )
        else:
            raise RuntimeError(f"Image {name} not found.")

    def build_image_from_containerfile(
        self,
        name: str,
        containerfile: str,
        ray_version: Optional[str] = None,
        anonymous: bool = False,
    ) -> str:
        return self.client.get_cluster_env_build_id_from_containerfile(
            cluster_env_name=name,
            containerfile=containerfile,
            anonymous=anonymous,
            ray_version=ray_version,
        )

    def build_image_from_containerfile_with_image_uri(
        self,
        name: str,
        containerfile: str,
        ray_version: Optional[str] = None,
        anonymous: bool = False,
    ) -> str:
        build_id = self.build_image_from_containerfile(
            name=name,
            containerfile=containerfile,
            ray_version=ray_version,
            anonymous=anonymous,
        )
        image_uri = self.get_image_uri_from_build_id(build_id)
        if image_uri:
            return image_uri.image_uri
        raise RuntimeError(
            f"This is a bug! Failed to get image uri for build {build_id} that just created."
        )

    def build_image_from_requirements(
        self, name: str, base_build_id: str, requirements: List[str]
    ):
        if requirements:
            base_build = self.client.get_cluster_env_build(base_build_id)
            if (
                base_build
                and base_build.status == ClusterEnvironmentBuildStatus.SUCCEEDED
                and base_build.docker_image_name
            ):
                self.logger.info(f"Using tracked python packages: {requirements}")
                lines = [
                    "# syntax=docker/dockerfile:1",
                    f"FROM {base_build.docker_image_name}",
                ]
                for requirement in requirements:
                    lines.append(f'RUN pip install "{requirement}"')
                return self.build_image_from_containerfile(
                    name, "\n".join(lines), ray_version=base_build.ray_version
                )
            else:
                raise RuntimeError(
                    f"Base build {base_build_id} is not a successful build."
                )
        else:
            return base_build_id

    def registery_image(
        self,
        image_uri: str,
        registry_login_secret: Optional[str] = None,
        ray_version: Optional[str] = None,
    ) -> str:
        image_uri_checked = ImageURI.from_str(image_uri_str=image_uri)
        return self.client.get_cluster_env_build_id_from_image_uri(
            image_uri=image_uri_checked,
            registry_login_secret=registry_login_secret,
            ray_version=ray_version,
        )

    def register_byod_image_with_name(
        self,
        image_uri_str: str,
        name: str,
        ray_version: Optional[str] = None,
        registry_login_secret: Optional[str] = None,
    ) -> str:
        # Validate the image URI is a BYOD image
        image_uri_checked = ImageURI.from_str(image_uri_str=image_uri_str)
        if image_uri_checked.is_cluster_env_image():
            raise RuntimeError(
                f"Image URI {image_uri_str} is not a BYOD image. "
                "The 'register' command only works with BYOD images."
            )

        build_id = self.client.get_cluster_env_build_id_from_image_uri(
            image_uri=image_uri_checked,
            registry_login_secret=registry_login_secret,
            ray_version=ray_version,
            name=name,
        )

        fetched_image_uri = self.get_image_uri_from_build_id(
            build_id, use_image_alias=True
        )
        if fetched_image_uri:
            return fetched_image_uri.image_uri
        raise RuntimeError(
            f"This is a bug! Failed to get image uri for build {build_id} that just created."
        )

    def get_image_uri_from_build_id(
        self, build_id: str, use_image_alias: bool = False
    ) -> Optional[ImageURI]:
        return self.client.get_cluster_env_build_image_uri(
            cluster_env_build_id=build_id, use_image_alias=use_image_alias,
        )
