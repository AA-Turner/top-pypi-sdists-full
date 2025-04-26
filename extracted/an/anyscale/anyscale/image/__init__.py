from typing import Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale.cli_logger import BlockLogger
from anyscale.image._private.image_sdk import PrivateImageSDK
from anyscale.image.commands import (
    _BUILD_ARG_DOCSTRINGS,
    _BUILD_EXAMPLE,
    _GET_ARG_DOCSTRINGS,
    _GET_EXAMPLE,
    _REGISTER_ARG_DOCSTRINGS,
    _REGISTER_EXAMPLE,
    build,
    get,
    register,
)
from anyscale.image.models import ImageBuild


class ImageSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
    ):
        self._private_sdk = PrivateImageSDK(client=client, logger=logger,)

    @sdk_docs(
        doc_py_example=_BUILD_EXAMPLE, arg_docstrings=_BUILD_ARG_DOCSTRINGS,
    )
    def build(  # noqa: F811
        self, containerfile: str, *, name: str, ray_version: Optional[str] = None
    ) -> str:  # noqa: F811
        """Build an image from a Containerfile.

        Returns the URI of the image.
        """
        return self._private_sdk.build_image_from_containerfile_with_image_uri(
            name, containerfile, ray_version=ray_version
        )

    @sdk_docs(
        doc_py_example=_GET_EXAMPLE, arg_docstrings=_GET_ARG_DOCSTRINGS,
    )
    def get(self, *, name: str) -> ImageBuild:  # noqa: F811
        """The name can contain an optional version tag, i.e., 'name:version'.

        If no version is provided, the latest one will be returned.
        """
        return self._private_sdk.get(name)

    @sdk_docs(
        doc_py_example=_REGISTER_EXAMPLE, arg_docstrings=_REGISTER_ARG_DOCSTRINGS,
    )
    def register(  # noqa: F811
        self,
        image_uri: str,
        *,
        name: str,
        ray_version: Optional[str] = None,
        registry_login_secret: Optional[str] = None,
    ) -> str:
        """
        Register a BYOD image with a container image name.
        """
        return self._private_sdk.register_byod_image_with_name(
            image_uri,
            registry_login_secret=registry_login_secret,
            ray_version=ray_version,
            name=name,
        )
