"""Tool module for managing Amazon S3 bucket versioning."""
from typing import Any
from typing import Dict


def convert_raw_bucket_versioning_to_present(
    hub, bucket: str, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    """Convert an AWS S3 bucket versioning resource to a common idem present state.

    Args:
        bucket(str):
            The S3 bucket name in Amazon Web Services.

        raw_resource(Dict[str, Any]):
            The AWS response to convert.

        idem_resource_name(str, Optional):
            An Idem name of the resource.

    Returns:
        Dict[str, Any]: Common idem present state.
    """
    raw_resource.pop("ResponseMetadata", None)

    resource_translated = {
        "name": idem_resource_name if idem_resource_name else f"{bucket}-versioning",
        "resource_id": bucket,
        "bucket": bucket,
        "mfa_delete": raw_resource.get("MFADelete", "Disabled"),
        "status": raw_resource.get("Status", "Suspended"),
    }

    return resource_translated
