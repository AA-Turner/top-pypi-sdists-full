"""
Functions to help with state arguments via pre contracts
"""
from typing import Any
from typing import Dict


def sync_sls_name_and_tag(hub, ref: str, kwargs: Dict[str, Any]):
    """
    Modify the kwargs passed to a state to have the same value for "Name" tag and sls name
    """
    # If the given state doesn't have "tags" as a parameter then quit early
    try:
        if "tags" not in hub[ref].present.signature.parameters:
            return
    except KeyError:
        return

    try:
        sync_sls_name_and_tag = hub.OPT.idem.sync_sls_name_and_name_tag
    except KeyError:
        sync_sls_name_and_tag = False

    if not sync_sls_name_and_tag:
        return

    # Make the "name" attribute and the "Name" tag match each other

    name = kwargs["name"]

    # Transform tag_specification to tags
    hub.tool.aws.parameters.tag_specs_to_dict(kwargs)
    tags = kwargs["tags"]

    # Patch the "name" attribute to match the "Name" tag
    kwargs["name"] = tags.get("Name", name)

    # Patch the "Name" tag to match the "name" attribute
    if "Name" not in tags:
        tags["Name"] = name

    kwargs["tags"] = tags


def tag_specs_to_dict(hub, kwargs: Dict[str, Any]):
    """
    Turn tag specificiations to a dict
    """
    tags = kwargs.get("tags") or {}

    # Transform tag_specification to tags
    if isinstance(tags, list):
        tags = {t["Key"]: t["Value"] for t in tags}

    # Override the "tags" in kwargs with the new value
    kwargs["tags"] = tags
