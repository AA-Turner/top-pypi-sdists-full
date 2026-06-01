"""
Semantic Kernel auto-instrumentation.

Automatically patches Semantic Kernel classes to create traces.
"""

import functools
import logging
from typing import Any

logger = logging.getLogger(__name__)

_patched_classes: set[str] = set()
_original_methods: dict[str, Any] = {}


def patch_semantic_kernel() -> bool:
    """
    Patch Semantic Kernel classes for auto-instrumentation.

    This patches:
    - Kernel.invoke() - Function invocation
    - Kernel.invoke_stream() - Streaming function invocation
    - Planner classes - Plan generation

    Returns:
        True if patching was successful (or already patched)
    """
    success = True
    success = _patch_kernel_invoke() and success
    return _patch_planners() and success


def unpatch_semantic_kernel() -> None:
    """Remove Semantic Kernel patches (for testing)."""
    global _patched_classes, _original_methods

    try:
        from semantic_kernel import Kernel

        if "Kernel.invoke" in _original_methods:
            Kernel.invoke = _original_methods["Kernel.invoke"]

        if "Kernel.invoke_stream" in _original_methods:
            Kernel.invoke_stream = _original_methods["Kernel.invoke_stream"]

    except ImportError:
        pass

    _patched_classes.clear()
    _original_methods.clear()


def is_semantic_kernel_patched() -> bool:
    """Check if Semantic Kernel has been patched."""
    return len(_patched_classes) > 0


def _patch_kernel_invoke() -> bool:
    """Patch Kernel.invoke() and invoke_stream() methods."""
    try:
        from semantic_kernel import Kernel

        if "Kernel" in _patched_classes:
            return True

        # Patch invoke
        if hasattr(Kernel, "invoke"):
            original_invoke = Kernel.invoke
            _original_methods["Kernel.invoke"] = original_invoke

            @functools.wraps(original_invoke)
            async def traced_invoke(self, *args, **kwargs):
                """Traced version of Kernel.invoke()."""
                from ...client import get_aigie
                from .config import SemanticKernelConfig
                from .handler import SemanticKernelHandler

                aigie = get_aigie()
                config = SemanticKernelConfig.from_env()

                if aigie and aigie._initialized and config.enabled:
                    handler = SemanticKernelHandler(
                        capture_function_results=config.capture_function_results,
                        capture_plan_details=config.capture_plan_details,
                    )
                    handler._aigie = aigie

                    # Extract function info from args
                    function_name = "unknown"
                    plugin_name = None
                    arguments = {}

                    if args:
                        # First arg is usually the function or plugin/function
                        first_arg = args[0]
                        if hasattr(first_arg, "name"):
                            function_name = first_arg.name
                        elif isinstance(first_arg, str):
                            function_name = first_arg

                    # Get plugin name if available
                    if len(args) > 1:
                        second_arg = args[1]
                        if isinstance(second_arg, str):
                            plugin_name = function_name
                            function_name = second_arg

                    # Get arguments from kwargs
                    arguments = kwargs.get("arguments", kwargs.get("input", {}))

                    await handler.handle_invoke_start(
                        function_name=function_name,
                        plugin_name=plugin_name,
                        arguments=arguments,
                    )

                    try:
                        result = await original_invoke(self, *args, **kwargs)

                        # Extract usage from result metadata if available
                        usage = None
                        if hasattr(result, "metadata") and result.metadata:
                            meta = result.metadata
                            if "usage" in meta:
                                usage = meta["usage"]

                        await handler.handle_invoke_end(result, usage)
                        return result

                    except Exception as e:
                        await handler.handle_invoke_end(None, error=str(e))
                        raise
                else:
                    return await original_invoke(self, *args, **kwargs)

            Kernel.invoke = traced_invoke

        # Patch invoke_stream
        if hasattr(Kernel, "invoke_stream"):
            original_invoke_stream = Kernel.invoke_stream
            _original_methods["Kernel.invoke_stream"] = original_invoke_stream

            @functools.wraps(original_invoke_stream)
            async def traced_invoke_stream(self, *args, **kwargs):
                """Traced version of Kernel.invoke_stream()."""
                from ...client import get_aigie
                from .config import SemanticKernelConfig
                from .handler import SemanticKernelHandler

                aigie = get_aigie()
                config = SemanticKernelConfig.from_env()

                if aigie and aigie._initialized and config.enabled:
                    handler = SemanticKernelHandler(
                        capture_function_results=config.capture_function_results,
                        capture_plan_details=config.capture_plan_details,
                    )
                    handler._aigie = aigie

                    function_name = "unknown"
                    plugin_name = None
                    arguments = {}

                    if args:
                        first_arg = args[0]
                        if hasattr(first_arg, "name"):
                            function_name = first_arg.name
                        elif isinstance(first_arg, str):
                            function_name = first_arg

                    if len(args) > 1:
                        second_arg = args[1]
                        if isinstance(second_arg, str):
                            plugin_name = function_name
                            function_name = second_arg

                    arguments = kwargs.get("arguments", kwargs.get("input", {}))

                    await handler.handle_invoke_start(
                        function_name=function_name,
                        plugin_name=plugin_name,
                        arguments=arguments,
                    )

                    chunks = []
                    error_msg = None

                    try:
                        async for chunk in original_invoke_stream(self, *args, **kwargs):
                            chunks.append(chunk)
                            yield chunk

                    except Exception as e:
                        error_msg = str(e)
                        raise
                    finally:
                        # Combine chunks for result
                        result = "".join(str(c) for c in chunks) if chunks else None
                        await handler.handle_invoke_end(result, error=error_msg)
                else:
                    async for chunk in original_invoke_stream(self, *args, **kwargs):
                        yield chunk

            Kernel.invoke_stream = traced_invoke_stream

        _patched_classes.add("Kernel")
        logger.debug("Patched Kernel for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("semantic_kernel not installed, skipping Kernel patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch Kernel: {e}")
        return False


def _patch_planners() -> bool:
    """Patch Semantic Kernel planner classes."""
    try:
        # Try to patch various planners
        planners_patched = []

        # Sequential Planner
        try:
            from semantic_kernel.planners import SequentialPlanner

            if hasattr(SequentialPlanner, "create_plan"):
                original_create_plan = SequentialPlanner.create_plan
                _original_methods["SequentialPlanner.create_plan"] = original_create_plan

                @functools.wraps(original_create_plan)
                async def traced_create_plan(self, goal: str, *args, **kwargs):
                    from ...client import get_aigie
                    from .config import SemanticKernelConfig
                    from .handler import SemanticKernelHandler

                    aigie = get_aigie()
                    config = SemanticKernelConfig.from_env()

                    if aigie and aigie._initialized and config.enabled:
                        handler = SemanticKernelHandler(
                            capture_plan_details=config.capture_plan_details,
                        )
                        handler._aigie = aigie

                        # Get available functions
                        available_functions = []
                        if hasattr(self, "_kernel") and hasattr(self._kernel, "plugins"):
                            for plugin in self._kernel.plugins.values():
                                for func in plugin.functions.values():
                                    available_functions.append(f"{plugin.name}.{func.name}")

                        await handler.handle_plan_start(
                            planner_type="SequentialPlanner",
                            goal=goal,
                            available_functions=available_functions,
                        )

                        try:
                            plan = await original_create_plan(self, goal, *args, **kwargs)
                            await handler.handle_plan_end(plan)
                            return plan
                        except Exception as e:
                            await handler.handle_plan_end(None, error=str(e))
                            raise
                    else:
                        return await original_create_plan(self, goal, *args, **kwargs)

                SequentialPlanner.create_plan = traced_create_plan
                planners_patched.append("SequentialPlanner")

        except ImportError:
            pass

        # Action Planner
        try:
            from semantic_kernel.planners import ActionPlanner

            if hasattr(ActionPlanner, "create_plan"):
                original_create_plan = ActionPlanner.create_plan
                _original_methods["ActionPlanner.create_plan"] = original_create_plan

                @functools.wraps(original_create_plan)
                async def traced_action_plan(self, goal: str, *args, **kwargs):
                    from ...client import get_aigie
                    from .config import SemanticKernelConfig
                    from .handler import SemanticKernelHandler

                    aigie = get_aigie()
                    config = SemanticKernelConfig.from_env()

                    if aigie and aigie._initialized and config.enabled:
                        handler = SemanticKernelHandler(
                            capture_plan_details=config.capture_plan_details,
                        )
                        handler._aigie = aigie

                        await handler.handle_plan_start(
                            planner_type="ActionPlanner",
                            goal=goal,
                        )

                        try:
                            plan = await original_create_plan(self, goal, *args, **kwargs)
                            await handler.handle_plan_end(plan)
                            return plan
                        except Exception as e:
                            await handler.handle_plan_end(None, error=str(e))
                            raise
                    else:
                        return await original_create_plan(self, goal, *args, **kwargs)

                ActionPlanner.create_plan = traced_action_plan
                planners_patched.append("ActionPlanner")

        except ImportError:
            pass

        if planners_patched:
            _patched_classes.update(planners_patched)
            logger.debug(f"Patched planners: {planners_patched}")

        return True

    except ImportError:
        logger.debug("semantic_kernel planners not available, skipping")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch planners: {e}")
        return False
