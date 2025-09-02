from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List

"""
Util functions to convert raw resource state from AWS ECR to present input format.
"""


def convert_raw_repository_to_present(
    hub, raw_resource: Dict[str, Any], tags: List = None, idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_id = raw_resource.get("repositoryName")
    resource_parameters = OrderedDict(
        {
            "repositoryArn": "repository_arn",
            "registryId": "registry_id",
            "repositoryName": "repository_name",
            "repositoryUri": "repository_uri",
            "imageTagMutability": "image_tag_mutability",
            "imageScanningConfiguration": "image_scanning_configuration",
            "encryptionConfiguration": "encryption_configuration",
        }
    )

    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if tags:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            tags
        )

    return resource_translated


def convert_raw_repository_policy_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    """
    Convert AWS ECR Repository Policy response to a common idem present state

    Args:
        hub: required for functions in hub
        raw_resource(Dict[str, Any]): The AWS response to convert.
        idem_resource_name(str, Optional): An Idem name of the resource.

    Returns:
        Dict[str, Any]: Common idem present state
    """

    resource_id = (
        f"{raw_resource.get('registryId')}-{raw_resource.get('repositoryName')}"
    )
    resource_parameters = OrderedDict(
        {
            "registryId": "registry_id",
            "repositoryName": "repository_name",
        }
    )
    resource_translated = {
        "name": idem_resource_name if idem_resource_name else resource_id,
        "resource_id": resource_id,
    }

    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if raw_resource.get("policyText"):
        resource_translated[
            "policy_text"
        ] = hub.tool.aws.state_comparison_utils.standardise_json(
            raw_resource.get("policyText")
        )

    return resource_translated


def convert_raw_image_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_parameters = OrderedDict(
        {
            "registryId": "registry_id",
            "repositoryName": "repository_name",
            "imageDigest": "image_digest",
            "imageTags": "image_tags",
            "imageSizeInBytes": "image_size_in_bytes",
            "imageScanStatus": "image_scan_status",
            "imageScanFindingsSummary": "image_scan_findings_summary",
            "imageManifestMediaType": "image_manifest_media_type",
            "artifactMediaType": "artifact_media_type",
        }
    )

    resource_translated = {}
    if idem_resource_name:
        resource_translated["name"] = idem_resource_name
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


def convert_raw_lifecycle_policy_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    """
    Convert AWS ECR Lifecycle Policy response to a common idem present state

    Args:
        raw_resource(Dict[str, Any]): The AWS response to convert.
        idem_resource_name(str, Optional): An Idem name of the resource.

    Returns:
        Dict[str, Any]: Common idem present state
    """

    resource_id = (
        f"{raw_resource.get('registryId')}-{raw_resource.get('repositoryName')}"
    )
    resource_id = raw_resource.get("repositoryName")
    resource_parameters = OrderedDict(
        {
            "registryId": "registry_id",
            "repositoryName": "repository_name",
            "lifecyclePolicyText": "lifecycle_policy_text",
        }
    )
    resource_translated = {
        "name": idem_resource_name if idem_resource_name else resource_id,
        "resource_id": resource_id,
    }
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated
