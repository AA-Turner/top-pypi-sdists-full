from typing import List

from cuga.backend.tools_env.registry.utils.types import AppDefinition


def assign_applications(tools) -> List[AppDefinition]:
    """
    Detects application prefixes and assigns server_name to tool metadata.
    Returns list of AppDefinition objects for all detected applications.
    - For tools with metadata=None OR server_name=None: assigns detected app name or 'default'
    - For tools with existing server_name: leaves unchanged

    Args:
        tools (list): List of tool objects with .name and .metadata attributes

    Returns:
        List[AppDefinition]: List of app definitions with tools description
    """

    # Common prefixes to exclude (HTTP methods, etc.)
    excluded_prefixes = {'get', 'post', 'put', 'delete', 'patch', 'head', 'options', 'trace'}

    # Step 1: Extract tool names for analysis (only for tools that need server_name assignment)
    tools_to_process = [
        tool for tool in tools if tool.metadata is None or tool.metadata.get("server_name", None) is None
    ]
    tool_names = [tool.name for tool in tools_to_process]

    # Step 2: Find potential prefixes and count occurrences
    prefix_candidates = {}

    for tool_name in tool_names:
        # Split by underscore and take the first part as potential prefix
        if '_' in tool_name:
            potential_prefix = tool_name.split('_')[0].lower()

            # Skip if it's an excluded prefix
            if potential_prefix not in excluded_prefixes:
                if potential_prefix not in prefix_candidates:
                    prefix_candidates[potential_prefix] = []
                prefix_candidates[potential_prefix].append(tool_name)

    # Step 3: Filter prefixes that appear in multiple tools (consistency check)
    detected_applications = {}
    for prefix, tool_list in prefix_candidates.items():
        if len(tool_list) > 1:  # Prefix appears in multiple tools - consistent!
            detected_applications[prefix.upper()] = tool_list

    # Step 4: Assign server_name to metadata for tools that need it
    for tool in tools:
        # Only process tools with metadata=None OR server_name=None
        if tool.metadata is None or tool.metadata.get("server_name", None) is None:
            tool_name = tool.name
            server_name = 'default'  # Default assignment

            # Check if this tool belongs to any detected application
            for app_name, app_tools in detected_applications.items():
                if tool_name in app_tools:
                    server_name = app_name
                    break

            # Initialize metadata if it's None, otherwise just update server_name
            if tool.metadata is None:
                tool.metadata = {"server_name": server_name}
            else:
                tool.metadata["server_name"] = server_name

    # Step 5: Collect all unique server_names and their associated tools
    app_tools_map = {}
    for tool in tools:
        if tool.metadata is not None:
            server_name = tool.metadata.get("server_name")
            if server_name:
                if server_name not in app_tools_map:
                    app_tools_map[server_name] = []
                app_tools_map[server_name].append(tool.name)

    # Step 6: Create AppDefinition objects
    app_definitions = []
    for app_name, tool_list in app_tools_map.items():
        tools_description = "Available tools: " + ", ".join(sorted(tool_list))

        app_def = AppDefinition(name=app_name, description=tools_description, url=None)
        app_definitions.append(app_def)

    return app_definitions
