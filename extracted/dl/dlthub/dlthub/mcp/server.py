from typing import Optional

from dlt._workspace.mcp import DltMCP

from dlthub.project.project_context import ProjectRunContext
from dlthub.mcp import tools
from dlthub.mcp import prompts
from dlthub.mcp import resources


class ProjectMCP(DltMCP):
    # TODO: allow to  configure in a standard way
    # @with_config(ProjectMCPConfiguration)
    def __init__(
        self, project_context: Optional[ProjectRunContext], port: int = 8000, path: str = "/"
    ) -> None:
        self._project_context = project_context
        super().__init__(name="", port=port, path=path)

    def _register_features(self) -> None:
        # NOTE: at this moment there's no way to launch this server without valid project context
        if self.project_context is None:
            self.add_tool(tools.project.select_project)

        for tool in tools.project.__tools__:
            self.logger.debug(f"add tool: {tool}")
            self.add_tool(tool)
        self.logger.debug("project tools registered.")

        for resource_fn in resources.docs.__resources__:
            self.add_resource(resource_fn())
        self.logger.debug("project resources registered.")

        from mcp.server.fastmcp.prompts.base import Prompt

        for prompt_fn in prompts.project.__prompts__:
            self.add_prompt(Prompt.from_function(prompt_fn))
        self.logger.debug("project prompts registered.")

    @property
    def project_context(self) -> Optional[ProjectRunContext]:
        """Reference to the dlthub project.

        This value is set on the `FastMCP` server instance is available to tools
        via the special `ctx: Context` kwarg. This allows to define stateless tool
        functions while avoiding to specify the project directory for each tool call.
        """
        return self._project_context

    @project_context.setter
    def project_context(self, new_project_context: ProjectRunContext) -> None:
        self._project_context = new_project_context
