import inspect

from bir_mcp.grafana.resources import get_flux_instruction, get_mcp_resource_uri_functions


def get_prompts() -> list[callable]:
    prompts = [
        get_lowest_network_usage_virtual_machines_prompt,
    ]
    return prompts


def get_lowest_network_usage_virtual_machines_prompt() -> str:
    """The prompt for finding virtual machines with the lowest network usage."""
    uri_functions = get_mcp_resource_uri_functions()
    flux_instruction_uri = uri_functions.inverse[get_flux_instruction]
    prompt = inspect.cleandoc(f"""
        Which virtual machines had the lowest network usage over the last week in the bank, 
        based on Vsphere logs in InfluxDB? To answer this question, follow these steps:
        - Refer to Flux language instructions in the MCP resources {flux_instruction_uri}.
        - Find InfluxDB datasource in the Grafana instance.
        - Find the InfluxDB datasource, bucket and measurement name that relates to Vsphere virtual machines usage in the bank.
        - Find the tag that identifies virtual machines.
        - Construct a query for finding the virtual machines with the lowest network usage using the lowestAverage() Flux function.
        - Present the results.
    """)
    return prompt
