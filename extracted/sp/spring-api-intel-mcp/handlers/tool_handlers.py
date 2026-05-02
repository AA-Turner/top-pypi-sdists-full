import os
from mcp import types
from core.indexer import CodeIndex
from core.logger import get_logger
from core.state_manager import save_state, clear_state
from tools.list_endpoints import list_endpoints
from tools.trace_endpoints import trace_endpoint
from tools.find_usages import find_usages
from tools.summarize_class import summarize_class

logger = get_logger("tool_handlers")


async def handle_call_tool(
    name: str,
    arguments: dict,
    index: CodeIndex,
    state: dict,
    read_stream,
    write_stream,
) -> list[types.TextContent]:
    logger.debug(f"Tool called: {name}  args: {arguments}")
    try:
        if name == "list_endpoints":
            result = await list_endpoints(index, state["spring_boot_url"])

        elif name == "trace_endpoint":
            result = trace_endpoint(index, arguments["path"])

        elif name == "find_usages":
            result = find_usages(index, arguments["class_name"])

        elif name == "summarize_class":
            result = await summarize_class(
                index,
                arguments["class_name"],
                use_sampling=True,
                streams=(read_stream, write_stream)
            )

        elif name == "list_cloned_repos":
            from tools.git_clone import list_cloned_repos
            result = list_cloned_repos()

        elif name == "delete_cloned_repo":
            from tools.git_clone import delete_cloned_repo
            result = delete_cloned_repo(arguments["repo_name"])

        elif name == "delete_all_cloned_repos":
            from tools.git_clone import delete_all_cloned_repos
            result = delete_all_cloned_repos()

        elif name == "reindex":
            index.build(state["project_root"])
            result = (
                f"Re-indexed {len(index.classes)} classes and "
                f"{len(index.endpoints)} endpoints from {state['project_root']}"
            )

        elif name == "get_project_info":
            from tools.project_info import get_project_info
            result = get_project_info(state["project_root"])

        elif name == "set_project":
            new_path = arguments["path"]
            if not os.path.isdir(new_path):
                result = f"Path does not exist or is not a directory: {new_path}"
            else:
                state["project_root"] = new_path
                index.build(new_path)
                save_state(state)
                result = (
                    f"Switched to project: {new_path}\n"
                    f"Indexed {len(index.classes)} classes and {len(index.endpoints)} endpoints"
                )

        elif name == "generate_dashboard":
            from tools.dashboard import generate_dashboard
            result = await generate_dashboard(
                index,
                state["project_root"],
                state["spring_boot_url"],
                (read_stream, write_stream)
            )

        elif name == "clear_saved_state":
            clear_state()
            state["project_root"] = ""
            state["spring_boot_url"] = ""
            result = "Saved state cleared. Use set_project to point at a codebase."

        elif name == "clone_and_set_project":
            from tools.git_clone import clone_and_index
            result = clone_and_index(index, arguments["github_url"], state)
            save_state(state)

        else:
            logger.error(f"Unknown tool called: {name}")
            result = f"Unknown tool: {name}"
            return [types.TextContent(type="text", text=result)]

        logger.debug(f"Tool {name} completed successfully")

    except Exception as e:
        logger.error(f"Tool {name} failed: {str(e)}", exc_info=True)
        result = f"Error running {name}: {str(e)}"

    return [types.TextContent(type="text", text=result)]


def get_tool_definitions() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_endpoints",
            description="List all REST endpoints in the Spring Boot project. Enriches with live Swagger/Actuator data if the app is running.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="trace_endpoint",
            description="Trace the full call chain for an endpoint path. Shows controller → service → repository.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The endpoint path to trace, e.g. /api/orders"}
                },
                "required": ["path"],
            },
        ),
        types.Tool(
            name="clone_and_set_project",
            description=(
                "Clone a public GitHub repository and index it as the active project. "
                "Accepts a full URL (https://github.com/owner/repo) or shorthand (owner/repo). "
                "Uses --depth=1 for speed. Re-uses existing clones automatically."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "github_url": {
                        "type": "string",
                        "description": "GitHub repo URL or owner/repo e.g. gothinkster/spring-boot-realworld-example-app"
                    }
                },
                "required": ["github_url"],
            },
        ),
        types.Tool(
            name="list_cloned_repos",
            description="List all GitHub repos currently cached in the temp folder with their disk usage.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="delete_cloned_repo",
            description="Delete a specific cloned repo from the temp folder to free up disk space.",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_name": {
                        "type": "string",
                        "description": "The repo folder name to delete e.g. spring-boot-realworld-example-app"
                    }
                },
                "required": ["repo_name"],
            },
        ),
        types.Tool(
            name="delete_all_cloned_repos",
            description="Delete all cloned repos from the temp folder to free up disk space.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="generate_dashboard",
            description="Generate a visual HTML architecture dashboard — layers, dependency graph, tech stack, and class overview. Opens in any browser.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="find_usages",
            description="Find all classes in the codebase that reference a given class name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "class_name": {"type": "string", "description": "The class name to search for, e.g. UserService"}
                },
                "required": ["class_name"],
            },
        ),
        types.Tool(
            name="summarize_class",
            description="Get a structured summary of a Java class including its annotations, dependencies, and methods.",
            inputSchema={
                "type": "object",
                "properties": {
                    "class_name": {"type": "string", "description": "The Java class name, e.g. OrderService"}
                },
                "required": ["class_name"],
            },
        ),
        types.Tool(
            name="reindex",
            description="Re-scan the project directory to pick up new or changed files.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="get_project_info",
            description="Extract project metadata from pom.xml or build.gradle — Java version, Spring Boot version, build tool, and all dependencies.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        types.Tool(
            name="set_project",
            description="Switch the active Spring Boot project by providing a directory path. Use this to point the server at a different codebase.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Absolute path to the Spring Boot project root"
                    }
                },
                "required": ["path"],
            },
        ),
        types.Tool(
            name="clear_saved_state",
            description="Clear the saved project state so the server starts fresh next session.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
    ]