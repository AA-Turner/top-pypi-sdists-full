"""
LlamaIndex callback handler for Aigie SDK.

Provides automatic tracing for LlamaIndex RAG workflows,
including query engines, chat engines, retrieval, and synthesis.
"""

import uuid
from datetime import datetime
from typing import Any

from ...buffer import EventType
from ...context_manager import merge_metadata


class LlamaIndexHandler:
    """
    LlamaIndex callback handler for Aigie.

    Automatically traces LlamaIndex workflow executions including:
    - Query engine operations
    - Chat engine conversations
    - Document retrieval with similarity scores
    - Response synthesis
    - LLM calls with tokens/cost
    - Embedding operations
    - Reranking operations

    Example:
        >>> from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
        >>> from aigie.integrations.llamaindex import LlamaIndexHandler
        >>>
        >>> handler = LlamaIndexHandler(
        ...     trace_name='rag-query',
        ...     metadata={'index_type': 'vector'}
        ... )
        >>>
        >>> index = VectorStoreIndex.from_documents(documents)
        >>> query_engine = index.as_query_engine()
        >>> response = query_engine.query("What is...")
    """

    def __init__(
        self,
        trace_name: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        capture_nodes: bool = True,
        max_nodes_captured: int = 10,
    ):
        """
        Initialize LlamaIndex handler.

        Args:
            trace_name: Name for the trace
            metadata: Additional metadata to attach
            tags: Tags to apply to trace and spans
            user_id: User ID for the trace
            session_id: Session ID for the trace
            capture_nodes: Whether to capture retrieved nodes
            max_nodes_captured: Maximum number of nodes to include
        """
        self.trace_name = trace_name
        self.metadata = metadata or {}
        self.tags = tags or []
        self.user_id = user_id
        self.session_id = session_id
        self.capture_nodes = capture_nodes
        self.max_nodes_captured = max_nodes_captured

        # State tracking
        self.trace_id: str | None = None
        self.query_map: dict[str, dict[str, Any]] = {}  # query_id -> {spanId, startTime}
        self.retrieve_map: dict[str, dict[str, Any]] = {}  # retrieve_id -> {spanId, startTime}
        self.synthesize_map: dict[str, dict[str, Any]] = {}  # synth_id -> {spanId, startTime}
        self.llm_call_map: dict[str, dict[str, Any]] = {}  # call_id -> {spanId, startTime}
        self.embedding_map: dict[str, dict[str, Any]] = {}  # embed_id -> {spanId, startTime}
        self.rerank_map: dict[str, dict[str, Any]] = {}  # rerank_id -> {spanId, startTime}
        self.chat_map: dict[str, dict[str, Any]] = {}  # chat_id -> {spanId, startTime}

        # Current context for parent relationships
        self._current_query_span_id: str | None = None
        self._current_chat_span_id: str | None = None
        self._aigie = None
        self._trace_context: Any | None = None

        # Statistics
        self.total_queries = 0
        self.total_retrievals = 0
        self.total_nodes_retrieved = 0
        self.total_tokens = 0
        self.total_cost = 0.0
        self.total_embeddings = 0

    def _get_aigie(self):
        """Lazy load Aigie client."""
        if self._aigie is None:
            from ...client import get_aigie

            self._aigie = get_aigie()
        return self._aigie

    def set_trace_context(self, trace_context: Any) -> None:
        """Set an existing trace context to use."""
        self._trace_context = trace_context
        if hasattr(trace_context, "id"):
            self.trace_id = str(trace_context.id)

    async def handle_query_start(
        self,
        query_id: str,
        query_str: str,
        query_type: str = "query",
        index_id: str | None = None,
    ) -> str:
        """
        Called when a query starts.

        Args:
            query_id: Unique query identifier
            query_str: The query string
            query_type: Type of query (query, chat)
            index_id: ID of the index being queried

        Returns:
            The span ID for this query
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return ""

        # Generate trace ID if not set
        if not self.trace_id:
            if self._trace_context and hasattr(self._trace_context, "id"):
                self.trace_id = str(self._trace_context.id)
            else:
                self.trace_id = str(uuid.uuid4())

        self.total_queries += 1
        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        self.query_map[query_id] = {
            "spanId": span_id,
            "startTime": start_time,
        }

        # Build trace name
        query_snippet = query_str[:50] + "..." if len(query_str) > 50 else query_str
        trace_name = self.trace_name or f"Query: {query_snippet}"

        # Build metadata
        trace_metadata = merge_metadata(
            {
                **self.metadata,
                "query_type": query_type,
                "query_length": len(query_str),
                "framework": "llamaindex",
            }
        )
        if index_id:
            trace_metadata["index_id"] = index_id

        # Create trace if we don't have one
        if not self._trace_context:
            trace_data = {
                "id": self.trace_id,
                "name": trace_name,
                "type": "chain",
                "input": {"query": query_str},
                "status": "pending",
                "tags": [*self.tags, "llamaindex", query_type],
                "metadata": merge_metadata(trace_metadata),
                "start_time": start_time.isoformat(),
                "created_at": start_time.isoformat(),
            }

            if self.user_id:
                trace_data["user_id"] = self.user_id
            if self.session_id:
                trace_data["session_id"] = self.session_id

            if aigie._buffer:
                await aigie._buffer.add(EventType.TRACE_CREATE, trace_data)

        # Create query span
        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "name": f"query:{query_type}",
            "type": "chain",
            "input": {"query": query_str[:1000]},
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "queryId": query_id,
                    "queryType": query_type,
                    "indexId": index_id,
                    "framework": "llamaindex",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        self._current_query_span_id = span_id

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_query_end(
        self,
        query_id: str,
        response: str | None = None,
        source_nodes: list[Any] | None = None,
    ) -> None:
        """
        Called when a query completes.

        Args:
            query_id: Unique query identifier
            response: The response text
            source_nodes: Source nodes used in the response
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        query_data = self.query_map.get(query_id)
        if not query_data:
            return

        end_time = datetime.now()
        duration = (end_time - query_data["startTime"]).total_seconds()

        output = {}
        if response:
            output["response"] = response[:2000]
        if source_nodes and self.capture_nodes:
            output["source_nodes"] = self._format_nodes(source_nodes[: self.max_nodes_captured])

        update_data = {
            "id": query_data["spanId"],
            "output": output,
            "status": "success",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        # Update trace
        trace_update = {
            "id": self.trace_id,
            "status": "success",
            "output": {
                "response": response[:1000] if response else None,
                "total_tokens": self.total_tokens,
                "total_cost": self.total_cost,
            },
            "end_time": end_time.isoformat(),
        }
        if aigie._buffer:
            await aigie._buffer.add(EventType.TRACE_UPDATE, trace_update)

        del self.query_map[query_id]

    async def handle_query_error(self, query_id: str, error: str) -> None:
        """Called when a query fails."""
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        query_data = self.query_map.get(query_id)
        if not query_data:
            return

        end_time = datetime.now()
        duration = (end_time - query_data["startTime"]).total_seconds()

        update_data = {
            "id": query_data["spanId"],
            "status": "failed",
            "error": error,
            "error_message": error,
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.query_map[query_id]

    async def handle_retrieve_start(
        self,
        retrieve_id: str,
        query_str: str,
        retriever_type: str = "vector",
        top_k: int | None = None,
    ) -> str:
        """
        Called when a retrieval operation starts.

        Args:
            retrieve_id: Unique retrieval identifier
            query_str: The query string for retrieval
            retriever_type: Type of retriever (vector, keyword, hybrid)
            top_k: Number of results to retrieve

        Returns:
            The span ID for this retrieval
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.total_retrievals += 1
        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        self.retrieve_map[retrieve_id] = {
            "spanId": span_id,
            "startTime": start_time,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": self._current_query_span_id or self._current_chat_span_id,
            "name": f"retrieve:{retriever_type}",
            "type": "tool",
            "input": {
                "query": query_str[:500],
                "top_k": top_k,
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "retrieveId": retrieve_id,
                    "retrieverType": retriever_type,
                    "topK": top_k,
                    "framework": "llamaindex",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_retrieve_end(
        self,
        retrieve_id: str,
        nodes: list[Any] | None = None,
        scores: list[float] | None = None,
    ) -> None:
        """
        Called when a retrieval operation completes.

        Args:
            retrieve_id: Unique retrieval identifier
            nodes: Retrieved nodes
            scores: Similarity scores for each node
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        retrieve_data = self.retrieve_map.get(retrieve_id)
        if not retrieve_data:
            return

        end_time = datetime.now()
        duration = (end_time - retrieve_data["startTime"]).total_seconds()

        num_nodes = len(nodes) if nodes else 0
        self.total_nodes_retrieved += num_nodes

        output = {
            "num_nodes": num_nodes,
        }
        if scores:
            output["top_score"] = max(scores) if scores else None
            output["avg_score"] = sum(scores) / len(scores) if scores else None
        if nodes and self.capture_nodes:
            output["nodes"] = self._format_nodes(nodes[: self.max_nodes_captured])

        update_data = {
            "id": retrieve_data["spanId"],
            "output": output,
            "status": "success",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.retrieve_map[retrieve_id]

    async def handle_synthesize_start(
        self,
        synth_id: str,
        query_str: str,
        num_nodes: int = 0,
    ) -> str:
        """
        Called when response synthesis starts.

        Args:
            synth_id: Unique synthesis identifier
            query_str: The original query
            num_nodes: Number of nodes being synthesized from

        Returns:
            The span ID for this synthesis
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        self.synthesize_map[synth_id] = {
            "spanId": span_id,
            "startTime": start_time,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": self._current_query_span_id or self._current_chat_span_id,
            "name": "synthesize",
            "type": "chain",
            "input": {
                "query": query_str[:500],
                "num_nodes": num_nodes,
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "synthId": synth_id,
                    "numNodes": num_nodes,
                    "framework": "llamaindex",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_synthesize_end(
        self,
        synth_id: str,
        response: str | None = None,
    ) -> None:
        """
        Called when response synthesis completes.

        Args:
            synth_id: Unique synthesis identifier
            response: The synthesized response
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        synth_data = self.synthesize_map.get(synth_id)
        if not synth_data:
            return

        end_time = datetime.now()
        duration = (end_time - synth_data["startTime"]).total_seconds()

        update_data = {
            "id": synth_data["spanId"],
            "output": {"response": response[:1000] if response else None},
            "status": "success",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.synthesize_map[synth_id]

    async def handle_llm_start(
        self,
        call_id: str,
        model: str,
        messages: Any,
        is_streaming: bool = False,
    ) -> str:
        """
        Called when an LLM call starts.

        Args:
            call_id: Unique ID for this call
            model: Model name
            messages: Input messages
            is_streaming: Whether this is a streaming call

        Returns:
            The span ID for this LLM call
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        # Get parent span
        parent_id = self._current_query_span_id or self._current_chat_span_id

        self.llm_call_map[call_id] = {
            "spanId": span_id,
            "startTime": start_time,
            "parentSpanId": parent_id,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": parent_id,
            "name": f"llm:{model}",
            "type": "llm",
            "input": self._serialize_messages(messages),
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "model": model,
                    "isStreaming": is_streaming,
                    "framework": "llamaindex",
                }
            ),
            "model": model,
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_llm_end(
        self,
        call_id: str,
        output: Any,
        input_tokens: int = 0,
        output_tokens: int = 0,
        cost: float = 0.0,
    ) -> None:
        """
        Called when an LLM call completes.

        Args:
            call_id: Unique ID for this call
            output: LLM output
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost: Cost of this call
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        call_data = self.llm_call_map.get(call_id)
        if not call_data:
            return

        # Track totals
        self.total_tokens += input_tokens + output_tokens
        self.total_cost += cost

        end_time = datetime.now()
        duration = (end_time - call_data["startTime"]).total_seconds()

        update_data = {
            "id": call_data["spanId"],
            "output": self._serialize_output(output),
            "status": "success",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
        }

        if cost > 0:
            update_data["total_cost"] = cost

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.llm_call_map[call_id]

    async def handle_llm_error(self, call_id: str, error: str) -> None:
        """Called when an LLM call fails."""
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        call_data = self.llm_call_map.get(call_id)
        if not call_data:
            return

        end_time = datetime.now()
        duration = (end_time - call_data["startTime"]).total_seconds()

        update_data = {
            "id": call_data["spanId"],
            "status": "failed",
            "error": error,
            "error_message": error,
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.llm_call_map[call_id]

    async def handle_embedding_start(
        self,
        embed_id: str,
        model: str,
        num_texts: int,
    ) -> str:
        """
        Called when an embedding operation starts.

        Args:
            embed_id: Unique embedding identifier
            model: Embedding model name
            num_texts: Number of texts being embedded

        Returns:
            The span ID for this embedding
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        self.total_embeddings += num_texts
        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        self.embedding_map[embed_id] = {
            "spanId": span_id,
            "startTime": start_time,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": self._current_query_span_id or self._current_chat_span_id,
            "name": f"embedding:{model}",
            "type": "llm",
            "input": {"num_texts": num_texts},
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "embedId": embed_id,
                    "model": model,
                    "numTexts": num_texts,
                    "framework": "llamaindex",
                }
            ),
            "model": model,
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_embedding_end(
        self,
        embed_id: str,
        embedding_dim: int | None = None,
        tokens: int = 0,
    ) -> None:
        """
        Called when an embedding operation completes.

        Args:
            embed_id: Unique embedding identifier
            embedding_dim: Dimension of the embeddings
            tokens: Number of tokens processed
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        embed_data = self.embedding_map.get(embed_id)
        if not embed_data:
            return

        end_time = datetime.now()
        duration = (end_time - embed_data["startTime"]).total_seconds()

        update_data = {
            "id": embed_data["spanId"],
            "output": {
                "embedding_dim": embedding_dim,
                "tokens": tokens,
            },
            "status": "success",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if tokens > 0:
            update_data["total_tokens"] = tokens

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.embedding_map[embed_id]

    async def handle_rerank_start(
        self,
        rerank_id: str,
        model: str,
        num_nodes: int,
        query: str,
    ) -> str:
        """
        Called when a reranking operation starts.

        Args:
            rerank_id: Unique rerank identifier
            model: Reranking model name
            num_nodes: Number of nodes being reranked
            query: Query for reranking

        Returns:
            The span ID for this rerank
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized or not self.trace_id:
            return ""

        span_id = str(uuid.uuid4())
        start_time = datetime.now()

        self.rerank_map[rerank_id] = {
            "spanId": span_id,
            "startTime": start_time,
        }

        span_data = {
            "id": span_id,
            "trace_id": self.trace_id,
            "parent_id": self._current_query_span_id,
            "name": f"rerank:{model}",
            "type": "tool",
            "input": {
                "num_nodes": num_nodes,
                "query": query[:300],
            },
            "status": "pending",
            "tags": self.tags or [],
            "metadata": merge_metadata(
                {
                    "rerankId": rerank_id,
                    "model": model,
                    "numNodes": num_nodes,
                    "framework": "llamaindex",
                }
            ),
            "start_time": start_time.isoformat(),
            "created_at": start_time.isoformat(),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_CREATE, span_data)

        return span_id

    async def handle_rerank_end(
        self,
        rerank_id: str,
        num_results: int,
        top_scores: list[float] | None = None,
    ) -> None:
        """
        Called when a reranking operation completes.

        Args:
            rerank_id: Unique rerank identifier
            num_results: Number of results after reranking
            top_scores: Top reranking scores
        """
        aigie = self._get_aigie()
        if not aigie or not aigie._initialized:
            return

        rerank_data = self.rerank_map.get(rerank_id)
        if not rerank_data:
            return

        end_time = datetime.now()
        duration = (end_time - rerank_data["startTime"]).total_seconds()

        update_data = {
            "id": rerank_data["spanId"],
            "output": {
                "num_results": num_results,
                "top_scores": top_scores[:5] if top_scores else None,
            },
            "status": "success",
            "end_time": end_time.isoformat(),
            "duration_ns": int(duration * 1_000_000_000),
        }

        if aigie._buffer:
            await aigie._buffer.add(EventType.SPAN_UPDATE, update_data)

        del self.rerank_map[rerank_id]

    def _format_nodes(self, nodes: list[Any]) -> list[dict[str, Any]]:
        """Format nodes for tracing."""
        formatted = []
        for node in nodes:
            node_info = {}
            try:
                # Get text content
                if hasattr(node, "text"):
                    node_info["text"] = (
                        node.text[:300] + "..." if len(node.text) > 300 else node.text
                    )
                elif hasattr(node, "get_content"):
                    content = node.get_content()
                    node_info["text"] = content[:300] + "..." if len(content) > 300 else content

                # Get score
                if hasattr(node, "score"):
                    node_info["score"] = node.score

                # Get node ID
                if hasattr(node, "node_id"):
                    node_info["node_id"] = node.node_id
                elif hasattr(node, "id_"):
                    node_info["node_id"] = node.id_

                # Get metadata
                if hasattr(node, "metadata"):
                    node_info["metadata"] = {
                        k: str(v)[:100] for k, v in list(node.metadata.items())[:5]
                    }

            except Exception:
                node_info["error"] = "Failed to format node"

            formatted.append(node_info)

        return formatted

    def _serialize_messages(self, messages: Any) -> Any:
        """Serialize messages for tracing."""
        if isinstance(messages, list):
            return [self._serialize_message(m) for m in messages]
        return self._serialize_message(messages)

    def _serialize_message(self, message: Any) -> Any:
        """Serialize a single message."""
        if isinstance(message, dict):
            return message
        if hasattr(message, "model_dump"):
            return message.model_dump()
        if hasattr(message, "dict"):
            return message.dict()
        if hasattr(message, "content"):
            return {
                "role": getattr(message, "role", "unknown"),
                "content": str(message.content)[:1000],
            }
        return str(message)[:1000]

    def _serialize_output(self, output: Any) -> Any:
        """Serialize output for tracing."""
        if isinstance(output, str):
            return output[:2000]
        if hasattr(output, "model_dump"):
            return output.model_dump()
        if hasattr(output, "dict"):
            return output.dict()
        return str(output)[:2000]

    def __repr__(self) -> str:
        return (
            f"LlamaIndexHandler("
            f"trace_id={self.trace_id}, "
            f"queries={self.total_queries}, "
            f"retrievals={self.total_retrievals}, "
            f"tokens={self.total_tokens}, "
            f"cost=${self.total_cost:.4f})"
        )
