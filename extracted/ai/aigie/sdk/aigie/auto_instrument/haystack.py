"""
Haystack auto-instrumentation.

Automatically patches Haystack pipelines and components to trace
document retrieval, LLM generations, and pipeline executions with Aigie.
"""

import functools
import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

_patched_classes = set()


def patch_haystack() -> None:
    """Patch Haystack classes for auto-instrumentation."""
    _patch_pipeline()
    _patch_component()
    _patch_generator()
    _patch_retriever()
    _patch_embedder()


def _patch_pipeline() -> None:
    """Patch Haystack Pipeline to trace pipeline runs."""
    try:
        from haystack import Pipeline

        if Pipeline in _patched_classes:
            return

        original_run = Pipeline.run

        @functools.wraps(original_run)
        def traced_run(self, data: dict[str, Any], **kwargs):
            """Traced version of Pipeline.run."""
            from aigie.auto_instrument.trace import get_or_create_trace_sync
            from aigie.client import get_aigie

            aigie = get_aigie()
            if not aigie or not aigie._initialized:
                return original_run(self, data, **kwargs)

            # Get pipeline info
            pipeline_name = getattr(self, "name", None) or "Haystack Pipeline"

            # Build metadata
            metadata = {
                "type": "haystack_pipeline",
                "pipeline_name": pipeline_name,
                "component_count": len(self.graph.nodes) if hasattr(self, "graph") else 0,
                "inputs": _safe_serialize(data),
            }

            # Create or get trace
            trace = get_or_create_trace_sync(name=f"Haystack: {pipeline_name}", metadata=metadata)

            start_time = datetime.utcnow()

            try:
                result = original_run(self, data, **kwargs)

                # Update trace with output
                end_time = datetime.utcnow()
                duration_ms = (end_time - start_time).total_seconds() * 1000

                if trace and hasattr(trace, "set_output"):
                    output_data = _safe_serialize(result)
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

        Pipeline.run = traced_run
        _patched_classes.add(Pipeline)
        logger.debug("Patched haystack.Pipeline for auto-instrumentation")

    except ImportError:
        logger.debug("Haystack not installed, skipping Pipeline patch")
    except Exception as e:
        logger.warning(f"Failed to patch haystack.Pipeline: {e}")


def _patch_component() -> None:
    """Patch Haystack Component base class for generic component tracing."""
    try:
        from haystack.core.component import Component

        if Component in _patched_classes:
            return

        # Component uses __call__ or run method
        original_call = getattr(Component, "__call__", None)

        if original_call:

            @functools.wraps(original_call)
            def traced_call(self, *args, **kwargs):
                """Traced version of Component.__call__."""
                from aigie.client import get_aigie

                aigie = get_aigie()
                if not aigie or not aigie._initialized:
                    return original_call(self, *args, **kwargs)

                component_name = self.__class__.__name__
                component_type = _detect_component_type(component_name)

                start_time = datetime.utcnow()

                try:
                    result = original_call(self, *args, **kwargs)

                    end_time = datetime.utcnow()
                    duration_ms = (end_time - start_time).total_seconds() * 1000

                    # Log component execution (spans are created by specific component patches)
                    logger.debug(
                        f"Haystack component {component_name} ({component_type}) "
                        f"completed in {duration_ms:.2f}ms"
                    )

                    return result

                except Exception as e:
                    logger.debug(f"Haystack component {component_name} failed: {e}")
                    raise

            Component.__call__ = traced_call

        _patched_classes.add(Component)
        logger.debug("Patched haystack.Component for auto-instrumentation")

    except ImportError:
        logger.debug("Haystack core not installed, skipping Component patch")
    except Exception as e:
        logger.warning(f"Failed to patch haystack.Component: {e}")


def _patch_generator() -> None:
    """Patch Haystack generators (LLM components)."""
    try:
        # Try to patch common generator classes
        generator_classes = []

        try:
            from haystack.components.generators import OpenAIGenerator

            generator_classes.append(("OpenAIGenerator", OpenAIGenerator))
        except ImportError:
            pass

        try:
            from haystack.components.generators import AzureOpenAIGenerator

            generator_classes.append(("AzureOpenAIGenerator", AzureOpenAIGenerator))
        except ImportError:
            pass

        try:
            from haystack.components.generators import HuggingFaceLocalGenerator

            generator_classes.append(("HuggingFaceLocalGenerator", HuggingFaceLocalGenerator))
        except ImportError:
            pass

        try:
            from haystack.components.generators import AnthropicGenerator

            generator_classes.append(("AnthropicGenerator", AnthropicGenerator))
        except ImportError:
            pass

        for name, cls in generator_classes:
            if cls in _patched_classes:
                continue

            _patch_generator_class(name, cls)
            _patched_classes.add(cls)

        logger.debug(f"Patched {len(generator_classes)} Haystack generators")

    except ImportError:
        logger.debug("Haystack generators not installed")
    except Exception as e:
        logger.warning(f"Failed to patch Haystack generators: {e}")


def _patch_generator_class(name: str, cls: type) -> None:
    """Patch a specific generator class."""
    original_run = getattr(cls, "run", None)

    if not original_run:
        return

    @functools.wraps(original_run)
    def traced_run(self, *args, **kwargs):
        """Traced version of Generator.run."""
        from aigie.auto_instrument.trace import get_or_create_trace_sync
        from aigie.client import get_aigie

        aigie = get_aigie()
        if not aigie or not aigie._initialized:
            return original_run(self, *args, **kwargs)

        # Build metadata
        metadata = {
            "type": "haystack_generator",
            "generator_class": name,
            "inputs": _serialize_inputs(args, kwargs),
        }

        # Get model info if available
        if hasattr(self, "model"):
            metadata["model"] = self.model
        if hasattr(self, "model_name"):
            metadata["model"] = self.model_name

        # Create span
        trace = get_or_create_trace_sync(name=f"Haystack Generator: {name}", metadata=metadata)

        start_time = datetime.utcnow()

        try:
            result = original_run(self, *args, **kwargs)

            end_time = datetime.utcnow()
            duration_ms = (end_time - start_time).total_seconds() * 1000

            if trace and hasattr(trace, "_metadata"):
                trace._metadata["duration_ms"] = duration_ms
                trace._metadata["status"] = "success"

                # Extract token usage if available
                if isinstance(result, dict):
                    if "meta" in result and isinstance(result["meta"], list):
                        for meta in result["meta"]:
                            if isinstance(meta, dict) and "usage" in meta:
                                trace._metadata["token_usage"] = meta["usage"]
                                break

            if trace and hasattr(trace, "set_output"):
                trace.set_output(_safe_serialize(result))

            return result

        except Exception as e:
            if trace and hasattr(trace, "_metadata"):
                trace._metadata["status"] = "error"
                trace._metadata["error"] = {"type": type(e).__name__, "message": str(e)}
            raise

    cls.run = traced_run


def _patch_retriever() -> None:
    """Patch Haystack retrievers."""
    try:
        retriever_classes = []

        try:
            from haystack.components.retrievers import InMemoryBM25Retriever

            retriever_classes.append(("InMemoryBM25Retriever", InMemoryBM25Retriever))
        except ImportError:
            pass

        try:
            from haystack.components.retrievers import InMemoryEmbeddingRetriever

            retriever_classes.append(("InMemoryEmbeddingRetriever", InMemoryEmbeddingRetriever))
        except ImportError:
            pass

        for name, cls in retriever_classes:
            if cls in _patched_classes:
                continue

            _patch_retriever_class(name, cls)
            _patched_classes.add(cls)

        logger.debug(f"Patched {len(retriever_classes)} Haystack retrievers")

    except ImportError:
        logger.debug("Haystack retrievers not installed")
    except Exception as e:
        logger.warning(f"Failed to patch Haystack retrievers: {e}")


def _patch_retriever_class(name: str, cls: type) -> None:
    """Patch a specific retriever class."""
    original_run = getattr(cls, "run", None)

    if not original_run:
        return

    @functools.wraps(original_run)
    def traced_run(self, *args, **kwargs):
        """Traced version of Retriever.run."""
        from aigie.auto_instrument.trace import get_or_create_trace_sync
        from aigie.client import get_aigie

        aigie = get_aigie()
        if not aigie or not aigie._initialized:
            return original_run(self, *args, **kwargs)

        # Build metadata
        metadata = {
            "type": "haystack_retriever",
            "retriever_class": name,
            "inputs": _serialize_inputs(args, kwargs),
        }

        # Get top_k if available
        if hasattr(self, "top_k"):
            metadata["top_k"] = self.top_k

        # Create span
        trace = get_or_create_trace_sync(name=f"Haystack Retriever: {name}", metadata=metadata)

        start_time = datetime.utcnow()

        try:
            result = original_run(self, *args, **kwargs)

            end_time = datetime.utcnow()
            duration_ms = (end_time - start_time).total_seconds() * 1000

            if trace and hasattr(trace, "_metadata"):
                trace._metadata["duration_ms"] = duration_ms
                trace._metadata["status"] = "success"

                # Count documents retrieved
                if isinstance(result, dict) and "documents" in result:
                    trace._metadata["document_count"] = len(result["documents"])

            if trace and hasattr(trace, "set_output"):
                trace.set_output(_safe_serialize(result))

            return result

        except Exception as e:
            if trace and hasattr(trace, "_metadata"):
                trace._metadata["status"] = "error"
                trace._metadata["error"] = {"type": type(e).__name__, "message": str(e)}
            raise

    cls.run = traced_run


def _patch_embedder() -> None:
    """Patch Haystack embedders."""
    try:
        embedder_classes = []

        try:
            from haystack.components.embedders import OpenAITextEmbedder

            embedder_classes.append(("OpenAITextEmbedder", OpenAITextEmbedder))
        except ImportError:
            pass

        try:
            from haystack.components.embedders import OpenAIDocumentEmbedder

            embedder_classes.append(("OpenAIDocumentEmbedder", OpenAIDocumentEmbedder))
        except ImportError:
            pass

        try:
            from haystack.components.embedders import SentenceTransformersTextEmbedder

            embedder_classes.append(
                ("SentenceTransformersTextEmbedder", SentenceTransformersTextEmbedder)
            )
        except ImportError:
            pass

        for name, cls in embedder_classes:
            if cls in _patched_classes:
                continue

            _patch_embedder_class(name, cls)
            _patched_classes.add(cls)

        logger.debug(f"Patched {len(embedder_classes)} Haystack embedders")

    except ImportError:
        logger.debug("Haystack embedders not installed")
    except Exception as e:
        logger.warning(f"Failed to patch Haystack embedders: {e}")


def _patch_embedder_class(name: str, cls: type) -> None:
    """Patch a specific embedder class."""
    original_run = getattr(cls, "run", None)

    if not original_run:
        return

    @functools.wraps(original_run)
    def traced_run(self, *args, **kwargs):
        """Traced version of Embedder.run."""
        from aigie.auto_instrument.trace import get_or_create_trace_sync
        from aigie.client import get_aigie

        aigie = get_aigie()
        if not aigie or not aigie._initialized:
            return original_run(self, *args, **kwargs)

        # Build metadata
        metadata = {
            "type": "haystack_embedder",
            "embedder_class": name,
        }

        # Get model info if available
        if hasattr(self, "model"):
            metadata["model"] = self.model
        if hasattr(self, "model_name"):
            metadata["model"] = self.model_name

        # Create span
        trace = get_or_create_trace_sync(name=f"Haystack Embedder: {name}", metadata=metadata)

        start_time = datetime.utcnow()

        try:
            result = original_run(self, *args, **kwargs)

            end_time = datetime.utcnow()
            duration_ms = (end_time - start_time).total_seconds() * 1000

            if trace and hasattr(trace, "_metadata"):
                trace._metadata["duration_ms"] = duration_ms
                trace._metadata["status"] = "success"

                # Extract embedding dimensions
                if isinstance(result, dict) and "embedding" in result:
                    embedding = result["embedding"]
                    if isinstance(embedding, list) and len(embedding) > 0:
                        trace._metadata["embedding_dimensions"] = len(embedding)

            return result

        except Exception as e:
            if trace and hasattr(trace, "_metadata"):
                trace._metadata["status"] = "error"
                trace._metadata["error"] = {"type": type(e).__name__, "message": str(e)}
            raise

    cls.run = traced_run


def _detect_component_type(class_name: str) -> str:
    """Detect Haystack component type from class name."""
    name_lower = class_name.lower()

    if "generator" in name_lower or "llm" in name_lower:
        return "generator"
    if "retriever" in name_lower:
        return "retriever"
    if "embedder" in name_lower:
        return "embedder"
    if "reader" in name_lower:
        return "reader"
    if "writer" in name_lower:
        return "writer"
    if "converter" in name_lower:
        return "converter"
    if "splitter" in name_lower:
        return "splitter"
    if "ranker" in name_lower:
        return "ranker"
    if "router" in name_lower:
        return "router"
    return "component"


def _serialize_inputs(args: tuple, kwargs: dict) -> dict[str, Any]:
    """Serialize inputs for tracing."""
    inputs = {}

    # Handle positional args
    for i, arg in enumerate(args):
        inputs[f"arg_{i}"] = _safe_serialize(arg)

    # Handle keyword args
    for key, value in kwargs.items():
        inputs[key] = _safe_serialize(value)

    return inputs


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

    # Handle Haystack Document objects
    if hasattr(value, "content") and hasattr(value, "meta"):
        return {
            "type": "Document",
            "content": str(value.content)[:500] if value.content else None,
            "meta": _safe_serialize(value.meta) if value.meta else None,
        }

    # For complex objects, use string representation
    try:
        return str(value)[:1000]
    except Exception:
        return f"<{type(value).__name__}>"
