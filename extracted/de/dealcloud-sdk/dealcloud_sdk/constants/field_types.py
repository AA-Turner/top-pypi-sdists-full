"""Field type constants and utilities (matching real SDK)."""

# Field type integer constants
TEXT = 1
CHOICE = 2
NUMBER = 3
DATE = 4
REFERENCE = 5
BOOLEAN = 6
USER = 7
BINARY = 13
ENTRY_LIST_ID = 14
COUNTER = 15
IMAGE = 16
DATA_SOURCE = 17
CURRENCY = 18

# Field type ID to name mapping
FIELD_TYPE_NAMES = {
    TEXT: "Text",
    CHOICE: "Choice",
    NUMBER: "Number",
    DATE: "Date",
    REFERENCE: "Reference",
    BOOLEAN: "Boolean",
    USER: "User",
    BINARY: "Binary",
    ENTRY_LIST_ID: "EntryListId",
    COUNTER: "Counter",
    IMAGE: "Image",
    DATA_SOURCE: "DataSource",
    CURRENCY: "Currency",
}

# Reverse mapping: name to ID
FIELD_TYPE_IDS = {v: k for k, v in FIELD_TYPE_NAMES.items()}


def get_field_type_name(field_type_id: int) -> str:
    """
    Get the display name for a field type ID.
    
    Args:
        field_type_id: The integer field type ID
    
    Returns:
        Human-readable field type name (e.g., "Text", "Choice", "Reference")
    
    Example:
        >>> get_field_type_name(1)
        'Text'
        >>> get_field_type_name(5)
        'Reference'
    """
    return FIELD_TYPE_NAMES.get(field_type_id, f"Unknown({field_type_id})")


def get_field_type_id(field_type_name: str) -> int:
    """
    Get the field type ID for a display name.
    
    Args:
        field_type_name: The field type name (e.g., "Text", "Choice")
    
    Returns:
        Integer field type ID, or -1 if not found
    
    Example:
        >>> get_field_type_id("Text")
        1
        >>> get_field_type_id("Reference")
        5
    """
    return FIELD_TYPE_IDS.get(field_type_name, -1)
