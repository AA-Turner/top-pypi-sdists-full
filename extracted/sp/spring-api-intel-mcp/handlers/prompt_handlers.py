from mcp import types
from core.logger import get_logger

logger = get_logger("prompt_handlers")


def get_prompt_definitions() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="summarize-class",
            description="Get an AI summary of a Java class in your Spring Boot project",
            arguments=[
                types.PromptArgument(
                    name="class_name",
                    description="The Java class name e.g. CustomerService",
                    required=True,
                )
            ],
        ),
        types.Prompt(
            name="generate-dashboard",
            description="Generate a visual HTML architecture dashboard for the current project",
            arguments=[],
        ),
        types.Prompt(
            name="trace-endpoint",
            description="Trace an endpoint through controller → service → repository",
            arguments=[
                types.PromptArgument(
                    name="path",
                    description="The endpoint path e.g. /api/v1/customer/get",
                    required=True,
                )
            ],
        ),
        types.Prompt(
            name="onboarding-overview",
            description="Full codebase overview for a new developer joining the project",
            arguments=[],
        ),
        types.Prompt(
            name="find-usages",
            description="Find all classes that reference a given class",
            arguments=[
                types.PromptArgument(
                    name="class_name",
                    description="The class name to search for e.g. CustomerRepository",
                    required=True,
                )
            ],
        ),
        types.Prompt(
            name="architecture-review",
            description="Full architecture review — endpoints, dependencies, design observations",
            arguments=[],
        ),
        types.Prompt(
            name="analyse-github-repo",
            description="Clone and analyse any public Spring Boot GitHub repository",
            arguments=[
                types.PromptArgument(
                    name="github_url",
                    description="GitHub URL or owner/repo shorthand",
                    required=True,
                )
            ],
        ),
    ]


def handle_get_prompt(
    name: str,
    arguments: dict[str, str] | None
) -> types.GetPromptResult:
    args = arguments or {}

    if name == "summarize-class":
        class_name = args.get("class_name", "")
        return types.GetPromptResult(
            description=f"Summarize {class_name}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Use the summarize_class tool to summarize the {class_name} class. "
                             f"Explain what it does, its dependencies, key methods, and any design observations."
                    )
                )
            ]
        )

    elif name == "trace-endpoint":
        path = args.get("path", "")
        return types.GetPromptResult(
            description=f"Trace {path}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Use the trace_endpoint tool to trace {path}. "
                             f"Walk me through the full call chain from the HTTP request "
                             f"down to the repository layer, and explain what each layer does."
                    )
                )
            ]
        )

    elif name == "onboarding-overview":
        return types.GetPromptResult(
            description="Codebase onboarding overview",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text="I'm a new developer joining this project. "
                             "Use list_endpoints, get_project_info, and summarize_class "
                             "to give me a complete onboarding overview: what the project does, "
                             "the tech stack, all endpoints, key services and what they depend on."
                    )
                )
            ]
        )

    elif name == "find-usages":
        class_name = args.get("class_name", "")
        return types.GetPromptResult(
            description=f"Find usages of {class_name}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Use the find_usages tool to find all classes that reference {class_name}. "
                             f"Then explain the relationship between those classes and why they depend on it."
                    )
                )
            ]
        )

    elif name == "architecture-review":
        return types.GetPromptResult(
            description="Full architecture review",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text="Use list_endpoints, get_project_info, and summarize_class on the key service classes "
                             "to give me a full architecture review. Cover: tech stack, endpoint structure, "
                             "service dependencies, separation of concerns, and any design observations or concerns."
                    )
                )
            ]
        )

    elif name == "analyse-github-repo":
        url = args.get("github_url", "")
        return types.GetPromptResult(
            description=f"Analyse {url}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Use clone_and_set_project to clone {url}. "
                             f"Once indexed, give me a full onboarding overview — "
                             f"tech stack, all endpoints, key service dependencies, "
                             f"and any architectural observations."
                    )
                )
            ]
        )

    elif name == "generate-dashboard":
        return types.GetPromptResult(
            description="Generate architecture dashboard",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text="Use the generate_dashboard tool to create a visual architecture "
                             "dashboard for this project. Then tell me the file path so I can open it."
                    )
                )
            ]
        )

    raise ValueError(f"Unknown prompt: {name}")