from typing import Optional

from anyscale._private.sdk import sdk_command
from anyscale.image._private.image_sdk import PrivateImageSDK
from anyscale.image.models import ImageBuild


_IMAGE_SDK_SINGLETON_KEY = "image_sdk"

_BUILD_EXAMPLE = """
import anyscale

containerfile = '''
FROM anyscale/ray:2.21.0-py39
RUN pip install --no-cache-dir pandas
'''

image_uri: str = anyscale.image.build(containerfile, name="mycoolimage")
"""

_BUILD_ARG_DOCSTRINGS = {
    "name": "The name of the image.",
    "containerfile": "The content of the Containerfile.",
    "ray_version": "The version of Ray to use in the image",
}


@sdk_command(
    _IMAGE_SDK_SINGLETON_KEY,
    PrivateImageSDK,
    doc_py_example=_BUILD_EXAMPLE,
    arg_docstrings=_BUILD_ARG_DOCSTRINGS,
)
def build(
    containerfile: str,
    *,
    name: str,
    ray_version: Optional[str] = None,
    _private_sdk: Optional[PrivateImageSDK] = None,
) -> str:
    """Build an image from a Containerfile.

    Returns the URI of the image.
    """
    return _private_sdk.build_image_from_containerfile_with_image_uri(  # type: ignore
        name, containerfile, ray_version=ray_version
    )


_GET_EXAMPLE = """
import anyscale

image_status = anyscale.image.get(name="mycoolimage")
"""

_GET_ARG_DOCSTRINGS = {
    "name": (
        "Get the details of an image.\n\n"
        "The name can contain an optional version, e.g., 'name:version'. "
        "If no version is provided, the latest one will be used.\n\n"
    )
}


@sdk_command(
    _IMAGE_SDK_SINGLETON_KEY,
    PrivateImageSDK,
    doc_py_example=_GET_EXAMPLE,
    arg_docstrings=_GET_ARG_DOCSTRINGS,
)
def get(*, name: str, _private_sdk: Optional[PrivateImageSDK] = None) -> ImageBuild:
    """The name can contain an optional version tag, i.e., 'name:version'.

    If no version is provided, the latest one will be returned.
    """
    return _private_sdk.get(name)  # type: ignore


_REGISTER_EXAMPLE = """
import anyscale

image_uri: str = anyscale.image.register("docker.io/myuser/myimage:v2", name="mycoolimage")
"""

_REGISTER_ARG_DOCSTRINGS = {
    "image_uri": "The URI of the BYOD image to register.",
    "name": "Name for the container image. If the name already exists, a new version will be built. Otherwise, a new container image will be created.",
    "ray_version": "The Ray version (X.Y.Z) specified for this image specified by either an image URI or a containerfile. If not provided, the latest Ray version will be used.",
    "registry_login_secret": "Name or identifier of the secret containing credentials to authenticate to the docker registry hosting the image.",  # pragma: allowlist secret
}


@sdk_command(
    _IMAGE_SDK_SINGLETON_KEY,
    PrivateImageSDK,
    doc_py_example=_REGISTER_EXAMPLE,
    arg_docstrings=_REGISTER_ARG_DOCSTRINGS,
)
def register(
    image_uri: str,
    *,
    name: str,
    ray_version: Optional[str] = None,
    registry_login_secret: Optional[str] = None,
    _private_sdk: Optional[PrivateImageSDK] = None,
) -> str:
    """
    Registers a BYOD image with a container image name.

    Returns the URI of the image.
    """
    return _private_sdk.register_byod_image_with_name(  # type: ignore
        image_uri,
        registry_login_secret=registry_login_secret,
        ray_version=ray_version,
        name=name,
    )
