"""
LlamaIndex auto-instrumentation.

Automatically patches LlamaIndex classes to create traces and inject handlers.
"""

import functools
import logging
import uuid
from typing import Any

logger = logging.getLogger(__name__)

_patched_classes: set[Any] = set()


def patch_llamaindex() -> bool:
    """Patch LlamaIndex classes for auto-instrumentation.

    Returns:
        True if patching was successful (or already patched)
    """
    success = True
    success = _patch_query_engine() and success
    success = _patch_retriever() and success
    return _patch_chat_engine() and success


def unpatch_llamaindex() -> None:
    """Remove LlamaIndex patches (for testing)."""
    global _patched_classes
    _patched_classes.clear()


def is_llamaindex_patched() -> bool:
    """Check if LlamaIndex has been patched."""
    return len(_patched_classes) > 0


def _patch_query_engine() -> bool:
    """Patch QueryEngine.query() and aquery() methods."""
    try:
        from llama_index.core.query_engine import BaseQueryEngine

        if BaseQueryEngine in _patched_classes:
            return True

        original_query = BaseQueryEngine.query
        original_aquery = getattr(BaseQueryEngine, "aquery", None)

        @functools.wraps(original_query)
        def traced_query(self, query_str, **kwargs):
            """Traced version of QueryEngine.query()."""
            import asyncio

            from ...client import get_aigie
            from .handler import LlamaIndexHandler

            aigie = get_aigie()
            if aigie and aigie._initialized:
                handler = LlamaIndexHandler(
                    trace_name=f"Query: {query_str[:50]}...",
                    metadata={"query_engine_type": type(self).__name__},
                )
                handler._aigie = aigie

                query_id = str(uuid.uuid4())

                # Run async handler in sync context
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        import concurrent.futures

                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(
                                asyncio.run,
                                handler.handle_query_start(
                                    query_id=query_id,
                                    query_str=query_str,
                                    query_type="query",
                                ),
                            )
                            future.result(timeout=5)
                    else:
                        loop.run_until_complete(
                            handler.handle_query_start(
                                query_id=query_id,
                                query_str=query_str,
                                query_type="query",
                            )
                        )
                except Exception as e:
                    logger.debug(f"Error starting query trace: {e}")

                self._aigie_handler = handler

                try:
                    result = original_query(self, query_str, **kwargs)

                    response_text = str(result) if result else None
                    source_nodes = getattr(result, "source_nodes", None)

                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            import concurrent.futures

                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                future = executor.submit(
                                    asyncio.run,
                                    handler.handle_query_end(
                                        query_id=query_id,
                                        response=response_text,
                                        source_nodes=source_nodes,
                                    ),
                                )
                                future.result(timeout=5)
                        else:
                            loop.run_until_complete(
                                handler.handle_query_end(
                                    query_id=query_id,
                                    response=response_text,
                                    source_nodes=source_nodes,
                                )
                            )
                    except Exception as e:
                        logger.debug(f"Error ending query trace: {e}")

                    return result

                except Exception as e:
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            import concurrent.futures

                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                future = executor.submit(
                                    asyncio.run, handler.handle_query_error(query_id, str(e))
                                )
                                future.result(timeout=5)
                        else:
                            loop.run_until_complete(handler.handle_query_error(query_id, str(e)))
                    except Exception:
                        pass
                    raise

            return original_query(self, query_str, **kwargs)

        if original_aquery:

            @functools.wraps(original_aquery)
            async def traced_aquery(self, query_str, **kwargs):
                """Traced version of QueryEngine.aquery()."""
                from ...client import get_aigie
                from .handler import LlamaIndexHandler

                aigie = get_aigie()
                if aigie and aigie._initialized:
                    handler = LlamaIndexHandler(
                        trace_name=f"Query: {query_str[:50]}...",
                        metadata={"query_engine_type": type(self).__name__},
                    )
                    handler._aigie = aigie

                    query_id = str(uuid.uuid4())

                    await handler.handle_query_start(
                        query_id=query_id,
                        query_str=query_str,
                        query_type="query",
                    )

                    self._aigie_handler = handler

                    try:
                        result = await original_aquery(self, query_str, **kwargs)

                        response_text = str(result) if result else None
                        source_nodes = getattr(result, "source_nodes", None)

                        await handler.handle_query_end(
                            query_id=query_id,
                            response=response_text,
                            source_nodes=source_nodes,
                        )

                        return result

                    except Exception as e:
                        await handler.handle_query_error(query_id, str(e))
                        raise

                return await original_aquery(self, query_str, **kwargs)

            BaseQueryEngine.aquery = traced_aquery

        BaseQueryEngine.query = traced_query
        _patched_classes.add(BaseQueryEngine)

        logger.debug("Patched BaseQueryEngine for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("LlamaIndex not installed, skipping QueryEngine patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch QueryEngine: {e}")
        return False


def _patch_retriever() -> bool:
    """Patch BaseRetriever.retrieve() and aretrieve() methods."""
    try:
        from llama_index.core.retrievers import BaseRetriever

        if BaseRetriever in _patched_classes:
            return True

        original_retrieve = BaseRetriever.retrieve
        getattr(BaseRetriever, "aretrieve", None)

        @functools.wraps(original_retrieve)
        def traced_retrieve(self, query_str, **kwargs):
            """Traced version of BaseRetriever.retrieve()."""
            import asyncio

            from ...client import get_aigie

            aigie = get_aigie()
            handler = getattr(self, "_aigie_handler", None)

            if not handler:
                # Try to get handler from parent query engine
                parent = getattr(self, "_parent_query_engine", None)
                if parent:
                    handler = getattr(parent, "_aigie_handler", None)

            if aigie and aigie._initialized and handler:
                retrieve_id = str(uuid.uuid4())

                try:
                    loop = asyncio.get_event_loop()
                    if not loop.is_running():
                        loop.run_until_complete(
                            handler.handle_retrieve_start(
                                retrieve_id=retrieve_id,
                                query_str=query_str,
                                retriever_type=type(self).__name__,
                            )
                        )
                except Exception as e:
                    logger.debug(f"Error starting retrieve trace: {e}")

            result = original_retrieve(self, query_str, **kwargs)

            if aigie and aigie._initialized and handler:
                nodes = result if isinstance(result, list) else []
                scores = [getattr(n, "score", None) for n in nodes if hasattr(n, "score")]

                try:
                    loop = asyncio.get_event_loop()
                    if not loop.is_running():
                        loop.run_until_complete(
                            handler.handle_retrieve_end(
                                retrieve_id=retrieve_id,
                                nodes=nodes,
                                scores=[s for s in scores if s is not None],
                            )
                        )
                except Exception as e:
                    logger.debug(f"Error ending retrieve trace: {e}")

            return result

        BaseRetriever.retrieve = traced_retrieve
        _patched_classes.add(BaseRetriever)

        logger.debug("Patched BaseRetriever for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("LlamaIndex not installed, skipping Retriever patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch Retriever: {e}")
        return False


def _patch_chat_engine() -> bool:
    """Patch ChatEngine.chat() and achat() methods."""
    try:
        from llama_index.core.chat_engine import BaseChatEngine

        if BaseChatEngine in _patched_classes:
            return True

        original_chat = BaseChatEngine.chat
        original_achat = getattr(BaseChatEngine, "achat", None)

        @functools.wraps(original_chat)
        def traced_chat(self, message, chat_history=None, **kwargs):
            """Traced version of ChatEngine.chat()."""
            import asyncio

            from ...client import get_aigie
            from .handler import LlamaIndexHandler

            aigie = get_aigie()
            if aigie and aigie._initialized:
                handler = LlamaIndexHandler(
                    trace_name=f"Chat: {message[:50]}...",
                    metadata={"chat_engine_type": type(self).__name__},
                )
                handler._aigie = aigie

                query_id = str(uuid.uuid4())

                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        import concurrent.futures

                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(
                                asyncio.run,
                                handler.handle_query_start(
                                    query_id=query_id,
                                    query_str=message,
                                    query_type="chat",
                                ),
                            )
                            future.result(timeout=5)
                    else:
                        loop.run_until_complete(
                            handler.handle_query_start(
                                query_id=query_id,
                                query_str=message,
                                query_type="chat",
                            )
                        )
                except Exception as e:
                    logger.debug(f"Error starting chat trace: {e}")

                self._aigie_handler = handler

                try:
                    result = original_chat(self, message, chat_history, **kwargs)

                    response_text = (
                        str(result.response) if hasattr(result, "response") else str(result)
                    )
                    source_nodes = getattr(result, "source_nodes", None)

                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            import concurrent.futures

                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                future = executor.submit(
                                    asyncio.run,
                                    handler.handle_query_end(
                                        query_id=query_id,
                                        response=response_text,
                                        source_nodes=source_nodes,
                                    ),
                                )
                                future.result(timeout=5)
                        else:
                            loop.run_until_complete(
                                handler.handle_query_end(
                                    query_id=query_id,
                                    response=response_text,
                                    source_nodes=source_nodes,
                                )
                            )
                    except Exception as e:
                        logger.debug(f"Error ending chat trace: {e}")

                    return result

                except Exception as e:
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            import concurrent.futures

                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                future = executor.submit(
                                    asyncio.run, handler.handle_query_error(query_id, str(e))
                                )
                                future.result(timeout=5)
                        else:
                            loop.run_until_complete(handler.handle_query_error(query_id, str(e)))
                    except Exception:
                        pass
                    raise

            return original_chat(self, message, chat_history, **kwargs)

        if original_achat:

            @functools.wraps(original_achat)
            async def traced_achat(self, message, chat_history=None, **kwargs):
                """Traced version of ChatEngine.achat()."""
                from ...client import get_aigie
                from .handler import LlamaIndexHandler

                aigie = get_aigie()
                if aigie and aigie._initialized:
                    handler = LlamaIndexHandler(
                        trace_name=f"Chat: {message[:50]}...",
                        metadata={"chat_engine_type": type(self).__name__},
                    )
                    handler._aigie = aigie

                    query_id = str(uuid.uuid4())

                    await handler.handle_query_start(
                        query_id=query_id,
                        query_str=message,
                        query_type="chat",
                    )

                    self._aigie_handler = handler

                    try:
                        result = await original_achat(self, message, chat_history, **kwargs)

                        response_text = (
                            str(result.response) if hasattr(result, "response") else str(result)
                        )
                        source_nodes = getattr(result, "source_nodes", None)

                        await handler.handle_query_end(
                            query_id=query_id,
                            response=response_text,
                            source_nodes=source_nodes,
                        )

                        return result

                    except Exception as e:
                        await handler.handle_query_error(query_id, str(e))
                        raise

                return await original_achat(self, message, chat_history, **kwargs)

            BaseChatEngine.achat = traced_achat

        BaseChatEngine.chat = traced_chat
        _patched_classes.add(BaseChatEngine)

        logger.debug("Patched BaseChatEngine for auto-instrumentation")
        return True

    except ImportError:
        logger.debug("LlamaIndex not installed, skipping ChatEngine patch")
        return True
    except Exception as e:
        logger.warning(f"Failed to patch ChatEngine: {e}")
        return False
