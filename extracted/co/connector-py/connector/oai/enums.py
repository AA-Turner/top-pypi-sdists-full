"""Common enums for connector implementations.

This module provides standardized enums for common patterns in connectors,
particularly for relationship labels in access graphs.

Usage Example:
    from connector.oai.enums import ResourceRelationshipLabel
    from connector_sdk_types.generated import AccessGraphResourceRelationship

    # Use enum for standardized relationship labels
    relationship = AccessGraphResourceRelationship(
        from_id="org-1",
        to_ids=["team-1", "team-2"],
        label=ResourceRelationshipLabel.CONTAINS,  # Serializes to "contains"
    )

    # Or use custom labels when needed
    custom_relationship = AccessGraphResourceRelationship(
        from_id="project-1",
        to_ids=["milestone-1"],
        label="tracks",  # Custom label
    )
"""

from connector_sdk_types import BaseEnum


class ResourceRelationshipLabel(str, BaseEnum):
    """Common labels for resource relationships in the access graph.

    These labels describe the nature of parent-child relationships between resources.
    Use these standardized labels when appropriate, or define custom labels when needed.
    """

    # Hierarchical containment
    CONTAINS = "contains"
    """Parent resource contains child resources (e.g., Organization contains Teams)"""

    PARENT_OF = "parent_of"
    """Parent-child relationship (e.g., Directory is parent of Subdirectory)"""

    CHILD_OF = "child_of"
    """Child-parent relationship (inverse of parent_of)"""

    # Membership
    MEMBER_OF = "member_of"
    """Resource is a member of another resource (e.g., User is member of Group)"""

    HAS_MEMBER = "has_member"
    """Resource has members (inverse of member_of)"""

    # Ownership
    OWNS = "owns"
    """Resource owns another resource (e.g., User owns Repository)"""

    OWNED_BY = "owned_by"
    """Resource is owned by another resource (inverse of owns)"""

    # Access relationships
    HAS_ACCESS_TO = "has_access_to"
    """Resource has access to another resource"""

    GRANTS_ACCESS_TO = "grants_access_to"
    """Resource grants access to another resource"""

    # Grouping
    BELONGS_TO = "belongs_to"
    """Resource belongs to a group or organization"""

    INCLUDES = "includes"
    """Resource includes other resources"""

    UNKNOWN = "unknown"  # Required to be defined when using BaseEnum
