"""Sub-agent helper for CodeWords sandboxes.

Wraps the OpenAI Agents SDK + MCP transport into a simple interface
so users can launch tool-connected agents in ~3 lines:

    from codewords_client.agent import SubAgent
    agent = SubAgent(task="Research LLM templates", model="gpt-4.1-mini")
    result = await agent.run()

Requires the ``agent`` extra::

    pip install 'codewords-client[agent]'
"""

import os
from typing import Optional


class SubAgent:
    """Launches an MCP-connected agent inside a CodeWords sandbox.

    Parameters
    ----------
    task:
        The natural-language instruction the agent should carry out.
    system_prompt:
        Custom system prompt. A sensible default is provided.
    model:
        Model identifier. Plain names (e.g. ``"gpt-4.1-mini"``) are sent
        to the OpenAI Agents SDK directly. Names containing a ``/``
        (e.g. ``"anthropic/claude-sonnet-4-20250514"``) are routed through
        LiteLLM automatically.
    tools_filter:
        If set, only MCP tools whose names appear in this list will be
        exposed to the agent.  Pass ``None`` (default) to expose all tools.
    max_turns:
        Maximum agentic loop iterations before the run is stopped.
    mcp_url:
        Override the MCP endpoint URL.  Defaults to the DevX MCP server
        derived from ``CODEWORDS_RUNTIME_URI``.
    api_key:
        Override the bearer token sent to the MCP server.  Defaults to
        ``CODEWORDS_API_KEY``.
    """

    def __init__(
        self,
        task: str,
        system_prompt: str = "",
        model: str = "gpt-4.1-mini",
        tools_filter: Optional[list[str]] = None,
        max_turns: int = 15,
        mcp_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        self.task = task
        self.system_prompt = (
            system_prompt
            or "You are a helpful CodeWords agent. Use the available tools to complete your task efficiently."
        )
        self.model = model
        self.tools_filter = tools_filter
        self.max_turns = max_turns
        self.mcp_url = mcp_url or f"{os.environ['CODEWORDS_RUNTIME_URI']}/run/devx_mcp/mcp/"
        self.api_key = api_key or os.environ.get("CODEWORDS_API_KEY", "")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def run(self) -> dict:
        """Run the sub-agent and return its output.

        Returns a dict with ``status`` (``"completed"`` or ``"error"``),
        ``output`` on success, or ``error`` / ``error_type`` on failure.
        """
        Agent, Runner, RunConfig = self._import_agents_sdk()
        model = self._resolve_model()

        server = self._build_mcp_server()

        try:
            await server.connect()

            if self.tools_filter is not None:
                self._apply_tools_filter(server)

            agent = Agent(
                name="Sub-Agent",
                instructions=self.system_prompt,
                mcp_servers=[server],
                model=model,
            )

            result = await Runner.run(
                starting_agent=agent,
                input=self.task,
                max_turns=self.max_turns,
                run_config=RunConfig(tracing_disabled=True),
            )

            return {
                "status": "completed",
                "output": str(result.final_output),
            }
        except Exception as exc:
            return {
                "status": "error",
                "error": str(exc),
                "error_type": type(exc).__name__,
            }
        finally:
            try:
                await server.cleanup()
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _import_agents_sdk():
        """Lazy-import the OpenAI Agents SDK (fails fast with a helpful message)."""
        try:
            from agents import Agent, Runner, RunConfig  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "openai-agents is required for SubAgent. "
                "Install with: pip install 'codewords-client[agent]'"
            ) from None
        return Agent, Runner, RunConfig

    def _resolve_model(self):
        """Return the model object — LiteLLM wrapper when a ``/`` is present."""
        if "/" not in self.model:
            return self.model

        try:
            from agents.extensions.models.litellm_model import LitellmModel  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                f"litellm is required for model '{self.model}'. "
                "Install with: pip install 'codewords-client[agent]'"
            ) from None
        return LitellmModel(model=self.model)

    def _build_mcp_server(self):
        """Construct the ``MCPServerStreamableHttp`` transport."""
        try:
            from agents.mcp import MCPServerStreamableHttp  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "openai-agents is required for SubAgent. "
                "Install with: pip install 'codewords-client[agent]'"
            ) from None

        return MCPServerStreamableHttp(
            params={
                "url": self.mcp_url,
                "headers": {"Authorization": f"Bearer {self.api_key}"},
                "timeout": 30,
                "sse_read_timeout": 300,
            },
            name="devx-mcp",
            cache_tools_list=True,
        )

    def _apply_tools_filter(self, server) -> None:
        """Monkey-patch *server.list_tools* to return only allowed tools."""
        allowed = set(self.tools_filter)  # type: ignore[arg-type]
        original_list_tools = server.list_tools

        async def _filtered_list_tools():
            tools = await original_list_tools()
            return [t for t in tools if t.name in allowed]

        server.list_tools = _filtered_list_tools
