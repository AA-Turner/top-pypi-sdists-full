import asyncio
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from core.indexer import CodeIndex
from core.logger import get_logger
from core.state_manager import load_state
from handlers.tool_handlers import handle_call_tool, get_tool_definitions
from handlers.prompt_handlers import handle_get_prompt, get_prompt_definitions

logger = get_logger("server")

state = load_state(
    env_root=os.environ.get("SPRING_PROJECT_ROOT", ""),
    env_url=os.environ.get("SPRING_BOOT_URL", ""),
)

index = CodeIndex()
app = Server("springboot-api-intel")

_read_stream = None
_write_stream = None


@app.list_tools()
async def _list_tools() -> list[types.Tool]:
    return get_tool_definitions()


@app.list_prompts()
async def _list_prompts() -> list[types.Prompt]:
    return get_prompt_definitions()


@app.get_prompt()
async def _get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    return handle_get_prompt(name, arguments)


@app.call_tool()
async def _call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    return await handle_call_tool(
        name, arguments, index, state, _read_stream, _write_stream
    )


async def main():
    global _read_stream, _write_stream
    if state["project_root"]:
        index.build(state["project_root"])
        logger.info(
            f"Started — indexed {len(index.classes)} classes, "
            f"{len(index.endpoints)} endpoints from {state['project_root']}"
        )
    else:
        logger.info("Started — no project set. Use set_project to point at a codebase.")

    async with stdio_server() as (read_stream, write_stream):
        _read_stream = read_stream
        _write_stream = write_stream
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main_sync():
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())