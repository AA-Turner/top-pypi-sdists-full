"""
DSPy auto-instrumentation.

Automatically patches DSPy classes to trace module executions, predictions,
and optimizations with Aigie.
"""

import functools
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

_patched_classes = set()


def patch_dspy() -> None:
    """Patch DSPy classes for auto-instrumentation."""
    _patch_module()
    _patch_predict()
    _patch_chain_of_thought()
    _patch_react()


def _patch_module() -> None:
    """Patch dspy.Module to trace forward calls."""
    try:
        import dspy

        if dspy.Module in _patched_classes:
            return

        getattr(dspy.Module, "forward", None)
        original_call = dspy.Module.__call__

        @functools.wraps(original_call)
        def traced_call(self, *args, **kwargs):
            """Traced version of __call__."""
            from ..auto_instrument.trace import get_or_create_trace_sync
            from ..client import get_aigie

            aigie = get_aigie()
            if not aigie or not aigie._initialized:
                return original_call(self, *args, **kwargs)

            # Get module info
            module_name = self.__class__.__name__
            module_type = "dspy_module"

            # Determine if this is a specific module type
            if hasattr(self, "signature"):
                module_type = "dspy_predict"
            if "ChainOfThought" in module_name:
                module_type = "dspy_cot"
            elif "ReAct" in module_name:
                module_type = "dspy_react"
            elif "Retrieve" in module_name:
                module_type = "dspy_retriever"

            # Build metadata
            metadata = {
                "type": module_type,
                "module_class": f"{self.__class__.__module__}.{module_name}",
                "inputs": _serialize_inputs(args, kwargs),
            }

            # Add signature info if available
            if hasattr(self, "signature"):
                sig = self.signature
                if hasattr(sig, "__name__"):
                    metadata["signature"] = sig.__name__
                elif hasattr(sig, "signature"):
                    metadata["signature"] = str(sig.signature)

            # Create or get trace
            trace = get_or_create_trace_sync(name=f"DSPy: {module_name}", metadata=metadata)

            start_time = datetime.utcnow()

            try:
                result = original_call(self, *args, **kwargs)

                # Update trace with output
                end_time = datetime.utcnow()
                duration_ms = (end_time - start_time).total_seconds() * 1000

                if trace and hasattr(trace, "set_output"):
                    output_data = _serialize_output(result)
                    trace.set_output(output_data)

                if trace and hasattr(trace, "_metadata"):
                    trace._metadata["duration_ms"] = duration_ms
                    trace._metadata["status"] = "success"

                return result

            except Exception as e:
                if trace and hasattr(trace, "_metadata"):
                    trace._metadata["status"] = "error"
                    trace._metadata["error"] = {"type": type(e).__name__, "message": str(e)}
                raise

        dspy.Module.__call__ = traced_call
        _patched_classes.add(dspy.Module)
        logger.debug("Patched dspy.Module for auto-instrumentation")

    except ImportError:
        logger.debug("DSPy not installed, skipping Module patch")
    except Exception as e:
        logger.warning(f"Failed to patch dspy.Module: {e}")


def _patch_predict() -> None:
    """Patch dspy.Predict to trace predictions."""
    try:
        import dspy

        if hasattr(dspy, "Predict") and dspy.Predict not in _patched_classes:
            # Predict inherits from Module, so base patching should cover it
            # But we can add specific tracking for prediction metrics
            _patched_classes.add(dspy.Predict)
            logger.debug("Patched dspy.Predict for auto-instrumentation")

    except ImportError:
        pass
    except Exception as e:
        logger.warning(f"Failed to patch dspy.Predict: {e}")


def _patch_chain_of_thought() -> None:
    """Patch dspy.ChainOfThought to trace CoT reasoning."""
    try:
        import dspy

        if hasattr(dspy, "ChainOfThought") and dspy.ChainOfThought not in _patched_classes:
            _patched_classes.add(dspy.ChainOfThought)
            logger.debug("Patched dspy.ChainOfThought for auto-instrumentation")

    except ImportError:
        pass
    except Exception as e:
        logger.warning(f"Failed to patch dspy.ChainOfThought: {e}")


def _patch_react() -> None:
    """Patch dspy.ReAct to trace ReAct agent loops."""
    try:
        import dspy

        if hasattr(dspy, "ReAct") and dspy.ReAct not in _patched_classes:
            _patched_classes.add(dspy.ReAct)
            logger.debug("Patched dspy.ReAct for auto-instrumentation")

    except ImportError:
        pass
    except Exception as e:
        logger.warning(f"Failed to patch dspy.ReAct: {e}")


def _serialize_inputs(args: tuple, kwargs: dict) -> dict[str, Any]:
    """Serialize DSPy inputs for tracing."""
    inputs = {}

    # Handle positional args
    for i, arg in enumerate(args):
        inputs[f"arg_{i}"] = _safe_serialize(arg)

    # Handle keyword args
    for key, value in kwargs.items():
        inputs[key] = _safe_serialize(value)

    return inputs


def _serialize_output(result: Any) -> dict[str, Any]:
    """Serialize DSPy output for tracing."""
    if result is None:
        return {"output": None}

    # DSPy Prediction objects
    if hasattr(result, "__dict__"):
        output = {}
        for key, value in result.__dict__.items():
            if not key.startswith("_"):
                output[key] = _safe_serialize(value)
        return output

    return {"output": _safe_serialize(result)}


def _safe_serialize(value: Any) -> Any:
    """Safely serialize a value for JSON."""
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple)):
        return [_safe_serialize(v) for v in value[:100]]  # Limit list size
    if isinstance(value, dict):
        return {k: _safe_serialize(v) for k, v in list(value.items())[:50]}
    # For complex objects, use string representation
    try:
        return str(value)[:1000]
    except Exception:
        return f"<{type(value).__name__}>"
