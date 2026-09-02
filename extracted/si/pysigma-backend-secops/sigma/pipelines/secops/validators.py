def is_valid_udm_field(field_path: str, udm_schema: dict) -> bool:
    """
    Check if a field path is valid according to the UDM schema.

    Args:
        field_path (str): The field path to validate.
        udm_schema (dict): The UDM schema to validate against.

    Returns:
        bool: True if the field path is valid, False otherwise.
    """

    parts = field_path.split(".")
    if not parts:
        return False

    # Start traversal
    current_level = None

    # Check if part[0] in GroupedFields
    if len(parts) == 1 and parts[0] in udm_schema["GroupedFields"]:
        return True
    # Check if the first part is a noun
    if parts[0] in udm_schema["Nouns"]:
        current_level = udm_schema["TopLevelFields"]["noun"]
        parts = parts[1:]
    elif parts[0] in udm_schema["TopLevelFields"]:
        current_level = udm_schema["TopLevelFields"][parts[0]]
        parts = parts[1:]
    else:
        return False

    for part in parts:
        if isinstance(current_level, dict) and part in current_level:
            field_type = current_level[part]
            if isinstance(field_type, str):
                if field_type.startswith("@enum:"):
                    return True
                elif field_type.startswith("@"):
                    subtype_name = field_type[1:]
                    current_level = udm_schema["Subtypes"].get(subtype_name, {})
                else:
                    # Standard data type or subtype
                    if field_type in ["string", "integer", "boolean", "list"]:
                        return True
                    else:
                        current_level = udm_schema["Subtypes"].get(field_type, {})
            elif isinstance(field_type, dict):
                current_level = field_type
            else:
                return False
        else:
            return False
    return True


def is_valid_udm_field_value(field_path: str, value, udm_schema) -> bool:
    parts = field_path.split(".")
    if not parts:
        return False

    # Start traversal
    current_level = None

    if parts[0] in udm_schema["Nouns"]:
        current_level = udm_schema["TopLevelFields"]["noun"]
        parts = parts[1:]
    elif parts[0] in udm_schema["TopLevelFields"]:
        current_level = udm_schema["TopLevelFields"][parts[0]]
        parts = parts[1:]
    else:
        return False

    for part in parts[:-1]:  # Traverse until the second-to-last part
        if isinstance(current_level, dict) and part in current_level:
            field_type = current_level[part]
            if isinstance(field_type, str):
                if field_type.startswith("@"):
                    subtype_name = field_type[1:]
                    current_level = udm_schema["Subtypes"].get(subtype_name, {})
                else:
                    current_level = udm_schema["Subtypes"].get(field_type, {})
            elif isinstance(field_type, dict):
                current_level = field_type
            else:
                return False
        else:
            return False

    # Check the last part
    last_part = parts[-1]
    if isinstance(current_level, dict) and last_part in current_level:
        field_type = current_level[last_part]
        if isinstance(field_type, str):
            if field_type.startswith("@enum:"):
                enum_name = field_type[len("@enum:") :]
                enum_values = udm_schema["Enums"].get(enum_name, [])
                return value in enum_values
            elif field_type in udm_schema["Enums"]:
                enum_values = udm_schema["Enums"][field_type]
                return value in enum_values
            else:
                return check_value_type(value, field_type)
        elif isinstance(field_type, dict):
            return isinstance(value, str)  # For complex types, just check if it's a string

    return False


def check_value_type(value, expected_type):
    if expected_type == "string":
        return isinstance(value, str)
    elif expected_type in ["integer", "int64"]:
        if isinstance(value, int):
            return True
        elif isinstance(value, str):
            try:
                int(value)
                return True
            except ValueError:
                return False
        else:
            return False
    elif expected_type == "boolean":
        if isinstance(value, bool):
            return True
        elif isinstance(value, str):
            return value.lower() in ["true", "false"]
        else:
            return False
    elif expected_type == "list":
        return isinstance(value, list)
    else:
        return True  # For unknown types, assume it's valid
