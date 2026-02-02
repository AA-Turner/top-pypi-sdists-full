"""
Interactive help system for FortiOS API endpoints.

Provides context-aware help based on endpoint category (cmdb, monitor, log, service).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing import Protocol

    class EndpointProtocol(Protocol):
        """Protocol for endpoint objects that support help."""

        def schema(self) -> dict[str, Any]: ...
        def fields(self) -> list[str]: ...
        def required_fields(self) -> list[str]: ...
        def defaults(self) -> dict[str, Any]: ...


def help(endpoint: Any, show_fields: bool = False) -> None:
    """
    Display comprehensive help for any FortiOS API endpoint.

    Provides context-aware documentation based on endpoint category:
    - CMDB: Configuration database operations
    - Monitor: Runtime status and statistics
    - Log: Log queries and retrieval
    - Service: Service operations and actions

    Args:
        endpoint: The API endpoint object (e.g., fgt.api.cmdb.firewall.policy)
        show_fields: Whether to list all available fields (default: False)

    Examples:
        >>> from hfortix_fortios import FortiOS, help
        >>> fgt = FortiOS('192.168.1.1', token='xxx')
        >>>
        >>> # Get help for firewall policy endpoint
        >>> help(fgt.api.cmdb.firewall.policy)
        >>>
        >>> # Show help with field listing
        >>> help(fgt.api.cmdb.system.interface, show_fields=True)
    """
    print("\n" + "=" * 80)
    print("FORTIOS API ENDPOINT HELP")
    print("=" * 80)

    # Get the class to call classmethod schema()
    endpoint_class = (
        endpoint if isinstance(endpoint, type) else endpoint.__class__
    )

    # Get schema to determine endpoint type
    schema = endpoint_class.schema()
    category = schema.get("category", "unknown")
    endpoint_path = schema.get("endpoint", "unknown")
    help_text = schema.get("help", "No description available")
    mkey = schema.get("mkey")
    mkey_type = schema.get("mkey_type")

    # Basic info
    print(f"\n📍 ENDPOINT: {endpoint_path}")
    print(f"📂 CATEGORY: {category.upper()}")
    print(f"ℹ️  DESCRIPTION: {help_text}")
    if mkey:
        print(f"🔑 PRIMARY KEY: {mkey} ({mkey_type})")

    # Field summary
    total_fields = schema.get("total_fields", 0)
    required_count = schema.get("required_fields_count", 0)
    defaults_count = schema.get("fields_with_defaults_count", 0)

    if total_fields:
        print("\n📊 FIELDS:")
        print(f"   Total: {total_fields}")
        print(f"   Required: {required_count}")
        print(f"   With Defaults: {defaults_count}")

    # Get available methods dynamically
    import inspect

    methods = []
    for name in dir(endpoint):
        if name.startswith("_"):
            continue
        attr = getattr(endpoint, name, None)
        if callable(attr) or (
            inspect.ismethod(attr) if hasattr(inspect, "ismethod") else False
        ):
            methods.append(name)

    # Categorize methods
    capabilities = [m for m in methods if m.startswith("SUPPORTS_")]

    # Known operation methods
    known_operations = [
        "get",
        "post",
        "put",
        "delete",
        "patch",
        "clone",
        "move",
        "set",
        "create",
        "update",
    ]
    operations = [m for m in methods if m in known_operations]

    # Known info/metadata methods
    known_info = [
        "help",
        "schema",
        "get_schema",
        "fields",
        "field_info",
        "required_fields",
        "defaults",
        "exists",
        "validate_field",
    ]
    info_methods = [m for m in methods if m in known_info]

    # Show supported capabilities
    print("\n📋 CAPABILITIES:")
    supported = [cap for cap in capabilities if getattr(endpoint, cap, False)]
    cap_names = [cap.replace("SUPPORTS_", "").lower() for cap in supported]
    if cap_names:
        print(f"   {', '.join(cap_names)}")
    else:
        print("   None")

    # Category-specific operation descriptions
    op_descriptions = _get_operation_descriptions(category)

    print("\n⚙️  OPERATIONS:")
    if operations:
        for op in operations:
            desc = op_descriptions.get(op, "Perform operation")
            print(f"   • {op}() - {desc}")
    else:
        print("   None")

    # Show info methods
    info_desc = {
        "help": "Show this help information",
        "schema": "Get full schema with field definitions",
        "get_schema": "Alias for schema()",
        "fields": "List all available field names",
        "field_info": "Get details about specific field",
        "required_fields": "List required fields for creation",
        "defaults": "Get default values for fields",
        "exists": "Check if object exists by ID",
        "validate_field": "Validate field value before sending",
    }

    print("\n📖 INFO METHODS:")
    if info_methods:
        for info in info_methods:
            desc = info_desc.get(info, "Information method")
            print(f"   • {info}() - {desc}")
    else:
        print("   None")

    print("\n" + "=" * 80)


def _get_operation_descriptions(category: str) -> dict[str, str]:
    """
    Get category-specific operation descriptions.

    Args:
        category: Endpoint category (cmdb, monitor, log, service)

    Returns:
        Dictionary mapping operation names to descriptions
    """
    if category == "cmdb":
        return {
            "get": "Retrieve configuration objects",
            "post": "Create new configuration object",
            "create": "Create new configuration object",
            "put": "Update existing configuration object",
            "update": "Update existing configuration object",
            "patch": "Partial update of configuration object",
            "delete": "Delete configuration object",
            "set": "Create or update object (upsert)",
            "clone": "Duplicate existing object",
            "move": "Reorder object position",
        }
    elif category == "monitor":
        return {
            "get": "Retrieve status/statistics",
            "post": "Perform action or query",
            "put": "Update runtime settings",
            "patch": "Partial update of runtime settings",
            "delete": "Clear/reset data",
        }
    elif category == "log":
        return {
            "get": "Retrieve log entries",
            "post": "Query logs with filters",
        }
    elif category == "service":
        return {
            "get": "Query service data",
            "post": "Trigger service action or query with parameters",
            "put": "Execute service operation",
            "patch": "Partial service operation",
            "delete": "Remove service data",
        }
    else:
        return {
            "get": "Retrieve data",
            "post": "Create/update/perform action",
            "create": "Create new resource",
            "put": "Update data",
            "update": "Update existing resource",
            "patch": "Partial update",
            "delete": "Delete data",
            "clone": "Duplicate resource",
            "move": "Reorder or move resource",
        }
