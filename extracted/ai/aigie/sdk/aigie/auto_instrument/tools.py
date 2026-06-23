"""
Tool call auto-instrumentation.

Automatically detects and traces tool/function calls in workflows.
"""

import functools
import logging

logger = logging.getLogger(__name__)

_patched_functions = set()


def patch_tools() -> None:
    """Patch tool-related functions for auto-instrumentation."""
    _patch_langchain_tools()
    _patch_function_calls()


def _patch_langchain_tools() -> None:
    """Patch LangChain Tool class."""
    try:
        from langchain_core.tools import Tool

        if Tool in _patched_functions:
            return

        original_run = Tool.run
        original_arun = Tool.arun

        @functools.wraps(original_run)
        def traced_run(self, tool_input: str, **kwargs) -> str:
            """Traced version of Tool.run."""
            from aigie.auto_instrument.trace import get_or_create_trace_sync
            from aigie.client import get_aigie

            aigie = get_aigie()
            if aigie and aigie._initialized:
                trace = get_or_create_trace_sync(
                    name="Tool Execution", metadata={"type": "tool", "tool_name": self.name}
                )

                if trace:
                    # Create span synchronously (for sync run)
                    span_ctx = trace.span(f"Tool: {self.name}", type="tool")
                    span_ctx.set_input({"input": tool_input, "tool": self.name})

                    try:
                        result = original_run(self, tool_input, **kwargs)
                        span_ctx.set_output({"output": result, "status": "success"})
                        return result
                    except Exception as e:
                        span_ctx.set_output(
                            {"error": str(e), "error_type": type(e).__name__, "status": "error"}
                        )
                        raise

            return original_run(self, tool_input, **kwargs)

        @functools.wraps(original_arun)
        async def traced_arun(self, tool_input: str, **kwargs) -> str:
            """Traced version of Tool.arun."""
            from aigie.auto_instrument.trace import get_or_create_trace
            from aigie.client import get_aigie

            aigie = get_aigie()
            if aigie and aigie._initialized:
                trace = await get_or_create_trace(
                    name="Tool Execution", metadata={"type": "tool", "tool_name": self.name}
                )

                if trace:
                    async with trace.span(f"Tool: {self.name}", type="tool") as span:
                        span.set_input({"input": tool_input, "tool": self.name})

                        try:
                            result = await original_arun(self, tool_input, **kwargs)
                            span.set_output({"output": result, "status": "success"})
                            return result
                        except Exception as e:
                            span.set_output(
                                {"error": str(e), "error_type": type(e).__name__, "status": "error"}
                            )
                            raise

            return await original_arun(self, tool_input, **kwargs)

        Tool.run = traced_run
        Tool.arun = traced_arun
        _patched_functions.add(Tool)

        logger.debug("Patched LangChain Tool for auto-instrumentation")

    except ImportError:
        pass  # LangChain not installed
    except Exception as e:
        logger.warning(f"Failed to patch LangChain Tool: {e}")


def _patch_function_calls() -> None:
    """Patch generic function calls (for custom tools)."""
    # This is a placeholder for future enhancement
    # Could use decorators or AST manipulation to trace arbitrary function calls
    pass
