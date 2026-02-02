from tooluniverse.base_tool import BaseTool
from tooluniverse.tool_registry import register_tool


@register_tool(
    "GhostTool",
    config={
        "name": "ghost_tool",
        "type": "GhostTool",
        "description": "A ghost tool that exists in code but not in JSON configs.",
        "parameter": {"type": "object", "properties": {"msg": {"type": "string"}}},
    },
)
class GhostTool(BaseTool):
    def run(self, arguments):
        return {"response": f"Boo! {arguments.get('msg', '')}"}
