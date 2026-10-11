"""
User Activity API translation tables: Activity Types, Source Types, Export Data Type.
See: https://api.docs.dealcloud.com/docs/management/user_activity
"""

from typing import Dict, List, Tuple

# -----------------------------------------------------------------------------
# Activity Types (for get_user_activity activity param)
# -----------------------------------------------------------------------------
ACTIVITY_TYPES: Dict[int, str] = {
    1: "Login Successful",
    2: "Login Failed",
    3: "Logout",
    4: "Session Expired",
    5: "Login Failed (Locked Out)",
    6: "Login Requires Verification",
    7: "Login Failed (Forbidden)",
    8: "Export Data",
    9: "User Proxy / Switch",
    10: "BackupAccess",
    11: "IP Restriction Applied",
}

# -----------------------------------------------------------------------------
# Source Types (for get_user_activity source param)
# -----------------------------------------------------------------------------
SOURCE_TYPES: Dict[int, str] = {
    1: "Web UI",
    2: "Mobile",
    3: "Outlook",
    4: "Excel",
    5: "Word",
    6: "Unknown",
    7: "Chrome Extension",
    8: "Web Add-In",
    9: "Mobile Next",
    10: "PowerPoint",
    11: "Teams",
}

# -----------------------------------------------------------------------------
# Export Data Types (for get_user_activity export_data_type when activity=8)
# -----------------------------------------------------------------------------
EXPORT_DATA_TYPES: Dict[int, str] = {
    0: "Export Data",
    1: "Export Formula",
    2: "Export Image",
    3: "Download Document",
    4: "Template Report",
}


def get_activity_types() -> Dict[int, str]:
    """
    Return the full Activity Types mapping (ID -> name).
    See: https://api.docs.dealcloud.com/docs/management/user_activity
    """
    return dict(ACTIVITY_TYPES)


def get_activity_type_name(activity_id: int) -> str:
    """Return the display name for an activity type ID, or str(id) if unknown."""
    return ACTIVITY_TYPES.get(activity_id, str(activity_id))


def get_activity_type_id(name: str) -> int:
    """Return the activity type ID for an exact name. Raises ValueError if name is not found."""
    for id_, n in ACTIVITY_TYPES.items():
        if n == name:
            return id_
    raise ValueError(f"Unknown activity type name: {name!r}. Valid names: {list(ACTIVITY_TYPES.values())}")


def get_activity_type_ids() -> List[Tuple[int, str]]:
    """Return list of (id, name) for all activity types (e.g. for dropdowns)."""
    return list(ACTIVITY_TYPES.items())


def get_source_types() -> Dict[int, str]:
    """
    Return the full Source Types mapping (ID -> name).
    See: https://api.docs.dealcloud.com/docs/management/user_activity
    """
    return dict(SOURCE_TYPES)


def get_source_type_name(source_id: int) -> str:
    """Return the display name for a source type ID, or str(id) if unknown."""
    return SOURCE_TYPES.get(source_id, str(source_id))


def get_source_type_id(name: str) -> int:
    """Return the source type ID for an exact name. Raises ValueError if name is not found."""
    for id_, n in SOURCE_TYPES.items():
        if n == name:
            return id_
    raise ValueError(f"Unknown source type name: {name!r}. Valid names: {list(SOURCE_TYPES.values())}")


def get_source_type_ids() -> List[Tuple[int, str]]:
    """Return list of (id, name) for all source types (e.g. for dropdowns)."""
    return list(SOURCE_TYPES.items())


def get_export_data_types() -> Dict[int, str]:
    """
    Return the full Export Data Type mapping (ID -> name).
    Used when activity=8 (Export Data). See: https://api.docs.dealcloud.com/docs/management/user_activity
    """
    return dict(EXPORT_DATA_TYPES)


def get_export_data_type_name(export_data_type_id: int) -> str:
    """Return the display name for an export data type ID, or str(id) if unknown."""
    return EXPORT_DATA_TYPES.get(export_data_type_id, str(export_data_type_id))


def get_export_data_type_id(name: str) -> int:
    """Return the export data type ID for an exact name. Raises ValueError if name is not found."""
    for id_, n in EXPORT_DATA_TYPES.items():
        if n == name:
            return id_
    raise ValueError(f"Unknown export data type name: {name!r}. Valid names: {list(EXPORT_DATA_TYPES.values())}")


def get_export_data_type_ids() -> List[Tuple[int, str]]:
    """Return list of (id, name) for all export data types (e.g. for dropdowns)."""
    return list(EXPORT_DATA_TYPES.items())


__all__ = [
    "ACTIVITY_TYPES",
    "SOURCE_TYPES",
    "EXPORT_DATA_TYPES",
    "get_activity_types",
    "get_activity_type_name",
    "get_activity_type_id",
    "get_activity_type_ids",
    "get_source_types",
    "get_source_type_name",
    "get_source_type_id",
    "get_source_type_ids",
    "get_export_data_types",
    "get_export_data_type_name",
    "get_export_data_type_id",
    "get_export_data_type_ids",
]
