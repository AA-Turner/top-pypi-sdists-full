import json
import urllib.request
from sys import version
from typing import List

from openapi_client.models import OrmKernelImage, ResponseKernelImage
from vessl import vessl_api
from vessl.organization import _get_organization_name


def read_kernel_image(image_id: int) -> ResponseKernelImage:
    """Read the kernel image.

    Args:
        image_id(int): Image ID.

    Example:
        ```python
        vessl.read_kernel_image(
            image_id=1,
        )
        ```
    """
    return vessl_api.kernel_image_read_api(image_id=image_id)


def list_kernel_images(**kwargs) -> List[OrmKernelImage]:
    """List kernel images in the default organization. If you
    want to override the default organization, then pass `organization_name` as
    `**kwargs`.

    Example:
        ```python
        vessl.list_kernel_images()
        ```
    """
    return vessl_api.kernel_image_list_api(
        organization_name=_get_organization_name(**kwargs),
    ).results

def list_vessl_managed_images(repository: str, only_latest_revisions: bool = True):
    try:
        response = urllib.request.urlopen(f"https://quay.io/api/v1/repository/vessl-ai/{repository}?includeTags=true").read().decode()
        if response:
            body = json.loads(response)
            tags_raw = body.get("tags", [])
            tags = [tag for tag in tags_raw]
            if only_latest_revisions:
                tags = filter(lambda tag: "-r" not in tag, tags) # Only latest tags by skipping -rN revision tags
            return tags
        return []
    except Exception as e:
        print(f"Error while fetching vessl managed images for {repository}: {e}")
        return []

def get_recent_framework_and_matchin_cuda_versions(framework: str):
    if framework != "torch" and framework != "tensorflow":
        raise ValueError("Only torch and tensorflow are supported")
    all_tags = list_vessl_managed_images(framework)
    
    framework_cuda_version_map = {}
    for tag in all_tags:
        framework_version = tag.split("-")[0]
        if "cuda" in tag:
            cuda_version = tag.split("cuda")[1]
            if framework_version not in framework_cuda_version_map:
                framework_cuda_version_map[framework_version] = []
            framework_cuda_version_map[framework_version].append(cuda_version)
    return framework_cuda_version_map

def list_framework_supported_cuda_version_for_vessl_managed(framework: str, version: str):
    if framework != "torch" and framework != "tensorflow":
        raise ValueError("Only torch and tensorflow are supported")
    all_tags = list_vessl_managed_images(framework)
    target_versions = []
    for tag in all_tags:
        if version in tag:
            target_versions.append(tag)

    cuda_versions = []
    for tag in target_versions:
        if "cuda" in tag:
            cuda_versions.append(tag.split("cuda")[1])

    return cuda_versions