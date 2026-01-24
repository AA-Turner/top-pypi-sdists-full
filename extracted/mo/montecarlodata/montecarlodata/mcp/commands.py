import click

from montecarlodata.keys.mcp import McpKeyService


@click.group(help="Manage MCP Server Keys for the current user")
def mcp():
    pass


@mcp.command(name="create-key", help="Create a new MCP Server Key")
@click.pass_obj
@click.option("--description", required=True, help="Description for the key")
def create_key(ctx, description: str):
    McpKeyService(
        config=ctx["config"],
        command_name="mcp create_key",
    ).create(description=description)


@mcp.command(name="list-keys", help="List MCP Server Keys")
@click.pass_obj
def list_keys(ctx):
    McpKeyService(
        config=ctx["config"],
        command_name="mcp list_keys",
    ).get_all()


@mcp.command(name="delete-key", help="Delete an MCP Server Key")
@click.pass_obj
@click.option("--key-id", required=True, help="Id of the key to delete")
def delete_key(ctx, key_id: str):
    McpKeyService(
        config=ctx["config"],
        command_name="mcp delete_key",
    ).delete(key_id=key_id)
