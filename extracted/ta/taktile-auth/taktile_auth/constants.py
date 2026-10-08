NULL_RESOURCE_ARG = "null"
"""Value a grant uses for a nullable arg when there is no id to name."""

INTERNAL_FLOW_PREFIX = "tktl_"
"""Slug prefix Taktile reserves for its own hidden flows, e.g. the `tktl_webhooks` flow."""

INTERNAL_FLOW_FOLDER_ID = "14ad6914-5a3b-48d3-8fab-fd92f570345e"
"""Folder every internal flow counts as being in for permission checks. It has no folder row:
services put this id in the folder argument for an internal flow, so the role YAML can grant it
statically. It is a UUID4 because services parse folder grants as UUID4 and drop anything else."""


def is_internal_flow(flow_slug: str) -> bool:
    return flow_slug.startswith(INTERNAL_FLOW_PREFIX)


def normalize_resource_arg(value: str) -> str:
    """Queried args come from f-strings, so a `None` id arrives as Python's `str(None)`.
    It means the same "no id to name" that NULL_RESOURCE_ARG does. Grants are unaffected —
    they never pass through here, so `null` stays their only spelling."""
    return NULL_RESOURCE_ARG if value == "None" else value
