"""
DSPy auto-instrumentation.

Automatically patches DSPy classes to trace module executions,
predictions, and optimizations with Aigie.
"""

import functools
import logging
import uuid
from typing import Any

logger = logging.getLogger(__name__)

_patched_classes: set[Any] = set()


def patch_dspy() -> bool:
    """Patch DSPy classes for auto-instrumentation.

    Returns:
        True if patching was successful (or already patched)
    """
    success = True
    success = _patch_module() and success
    success = _patch_predict() and success
    success = _patch_chain_of_thought() and success
    success = _patch_react() and success
    return _patch_retrieve() and success


def unpatch_dspy() -> None:
    """Remove DSPy patches (for testing)."""
    global _patched_classes
    _patched_classes.clear()


def is_dspy_patched() -> bool:
    """Check if DSPy has been patched."""
    return len(_patched_classes) > 0


def _patch_module() -> bool:
    """Patch dspy.Module to trace forward calls.

    Returns:
        True if successful
    """
    try:
        import dspy

        if dspy.Module in _patched_classes:
            return True

        original_call = dspy.Module.__call__

        @functools.wraps(original_call)
        def traced_call(self, *args, **kwargs):
            """Traced version of Module.__call__()."""
            import asyncio

            from ...client import get_aigie
            from .handler import DSPyHandler

            aigie = get_aigie()
            if aigie and aigie._initialized:
                handler = DSPyHandler(
                    trace_name=f"DSPy: {self.__class__.__name__}",
                    metadata={"module_class": type(self).__name__},
                )
                handler._aigie = aigie

                # Determine module type
                module_type = _get_module_type(self)
                signature = _get_signature(self)

                module_id = str(uuid.uuid4())

                # Run async handler in sync context
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        import concurrent.futures

                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(
                                asyncio.run,
                                handler.handle_module_start(
                                    module_name=self.__class__.__name__,
                                    module_type=module_type,
                                    signature=signature,
                                    inputs=_serialize_inputs(args, kwargs),
                                ),
                            )
                            module_id = future.result(timeout=5)
                    else:
                        module_id = loop.run_until_complete(
                            handler.handle_module_start(
                                module_name=self.__class__.__name__,
                                module_type=module_type,
                                signature=signature,
                                inputs=_serialize_inputs(args, kwargs),
                            )
                        )
                except Exception as e:
                    logger.debug(f"Error starting module trace: {e}")

                self._aigie_handler = handler

                try:
                    result = original_call(self, *args, **kwargs)

                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            import concurrent.futures

                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                future = executor.submit(
                                    asyncio.run,
                                    handler.handle_module_end(
                                        module_id=module_id,
                                        output=result,
                                    ),
                                )
                                future.result(timeout=5)
                        else:
                            loop.run_until_complete(
                                handler.handle_module_end(
                                    module_id=module_id,
                                    output=result,
                                )
                            )
                    except Exception as e:
                        logger.debug(f"Error ending module trace: {e}")

                    return result

                except Exception as e:
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            import concurrent.futures

                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                future = executor.submit(
                                    asyncio.run, handler.handle_module_end(module_id, error=str(e))
                                )
                                future.result(timeout=5)
                        else:
                            loop.run_until_complete(
                                handler.handle_module_end(module_id, error=str(e))
                            )
                    except Exception:
                        pass
                    raise

            return original_call(self, *args, **kwargs)

        dspy.Module.__call__ = traced_call
        _patched_classes.add(dspy.Module)

        logger.debug("Patched dspy.Module for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("DSPy not installed, skipping Module patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch dspy.Module: {e}")
        return False


def _patch_predict() -> bool:
    """Patch dspy.Predict to trace predictions.

    Returns:
        True if successful
    """
    try:
        import dspy

        if not hasattr(dspy, "Predict"):
            return True

        if dspy.Predict in _patched_classes:
            return True

        # Predict inherits from Module, base patching covers it
        # Add to patched classes to track
        _patched_classes.add(dspy.Predict)
        logger.debug("Patched dspy.Predict for auto-instrumentation")
        return True

    except ImportError:
        return True
    except Exception as e:
        logger.warning(f"Failed to patch dspy.Predict: {e}")
        return False


def _patch_chain_of_thought() -> bool:
    """Patch dspy.ChainOfThought to trace CoT reasoning.

    Returns:
        True if successful
    """
    try:
        import dspy

        if not hasattr(dspy, "ChainOfThought"):
            return True

        if dspy.ChainOfThought in _patched_classes:
            return True

        # ChainOfThought inherits from Module
        _patched_classes.add(dspy.ChainOfThought)
        logger.debug("Patched dspy.ChainOfThought for auto-instrumentation")
        return True

    except ImportError:
        return True
    except Exception as e:
        logger.warning(f"Failed to patch dspy.ChainOfThought: {e}")
        return False


def _patch_react() -> bool:
    """Patch dspy.ReAct to trace ReAct agent loops.

    Returns:
        True if successful
    """
    try:
        import dspy

        if not hasattr(dspy, "ReAct"):
            return True

        if dspy.ReAct in _patched_classes:
            return True

        # ReAct inherits from Module
        _patched_classes.add(dspy.ReAct)
        logger.debug("Patched dspy.ReAct for auto-instrumentation")
        return True

    except ImportError:
        return True
    except Exception as e:
        logger.warning(f"Failed to patch dspy.ReAct: {e}")
        return False


def _patch_retrieve() -> bool:
    """Patch dspy.Retrieve to trace retrieval operations.

    Returns:
        True if successful
    """
    try:
        import dspy

        if not hasattr(dspy, "Retrieve"):
            return True

        if dspy.Retrieve in _patched_classes:
            return True

        original_forward = getattr(dspy.Retrieve, "forward", None)
        if not original_forward:
            return True

        @functools.wraps(original_forward)
        def traced_forward(self, query_or_queries, k=None, **kwargs):
            """Traced version of Retrieve.forward()."""
            import asyncio

            from ...client import get_aigie

            aigie = get_aigie()
            handler = getattr(self, "_aigie_handler", None)

            if not handler:
                # Try to get handler from parent module
                parent = getattr(self, "_parent_module", None)
                if parent:
                    handler = getattr(parent, "_aigie_handler", None)

            if aigie and aigie._initialized and handler:
                retrieval_id = str(uuid.uuid4())
                k_value = k or getattr(self, "k", 5)

                query_str = str(query_or_queries)[:500] if query_or_queries else None

                try:
                    loop = asyncio.get_event_loop()
                    if not loop.is_running():
                        loop.run_until_complete(
                            handler.handle_retrieval_start(
                                retriever_name=self.__class__.__name__,
                                query=query_str,
                                k=k_value,
                            )
                        )
                except Exception as e:
                    logger.debug(f"Error starting retrieval trace: {e}")

            result = original_forward(self, query_or_queries, k=k, **kwargs)

            if aigie and aigie._initialized and handler:
                passages = []
                scores = []

                # Extract passages from result
                if hasattr(result, "passages"):
                    passages = result.passages or []
                elif isinstance(result, (list, tuple)):
                    passages = list(result)

                try:
                    loop = asyncio.get_event_loop()
                    if not loop.is_running():
                        loop.run_until_complete(
                            handler.handle_retrieval_end(
                                retrieval_id=retrieval_id,
                                passages=passages,
                                scores=scores,
                            )
                        )
                except Exception as e:
                    logger.debug(f"Error ending retrieval trace: {e}")

            return result

        dspy.Retrieve.forward = traced_forward
        _patched_classes.add(dspy.Retrieve)

        logger.debug("Patched dspy.Retrieve for auto-instrumentation")
        return True

    except ImportError:
        return True
    except Exception as e:
        logger.warning(f"Failed to patch dspy.Retrieve: {e}")
        return False


def _get_module_type(module: Any) -> str:
    """Determine the type of a DSPy module.

    Args:
        module: The module instance

    Returns:
        Module type string
    """
    class_name = module.__class__.__name__

    if "ChainOfThought" in class_name:
        return "cot"
    if "ReAct" in class_name:
        return "react"
    if "Retrieve" in class_name:
        return "retriever"
    if "Predict" in class_name or hasattr(module, "signature"):
        return "predict"
    return "module"


def _get_signature(module: Any) -> str:
    """Extract signature from a DSPy module.

    Args:
        module: The module instance

    Returns:
        Signature string or None
    """
    if hasattr(module, "signature"):
        sig = module.signature
        if hasattr(sig, "__name__"):
            return sig.__name__
        if hasattr(sig, "signature"):
            return str(sig.signature)
        return str(sig)
    return None


def _serialize_inputs(args: tuple, kwargs: dict) -> dict:
    """Serialize DSPy inputs for tracing.

    Args:
        args: Positional arguments
        kwargs: Keyword arguments

    Returns:
        Serialized inputs dictionary
    """
    inputs = {}

    # Handle positional args
    for i, arg in enumerate(args):
        inputs[f"arg_{i}"] = _safe_serialize(arg)

    # Handle keyword args
    for key, value in kwargs.items():
        inputs[key] = _safe_serialize(value)

    return inputs


def _safe_serialize(value: Any) -> Any:
    """Safely serialize a value for JSON.

    Args:
        value: Value to serialize

    Returns:
        Serialized value
    """
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple)):
        return [_safe_serialize(v) for v in value[:100]]
    if isinstance(value, dict):
        return {k: _safe_serialize(v) for k, v in list(value.items())[:50]}
    try:
        return str(value)[:1000]
    except Exception:
        return f"<{type(value).__name__}>"
