"""
Utility functions for LlamaIndex integration.
"""

import contextlib
import logging
from typing import Any

logger = logging.getLogger(__name__)


def is_llamaindex_available() -> bool:
    """Check if LlamaIndex is installed and importable.

    Returns:
        True if LlamaIndex is available
    """
    try:
        import llama_index.core

        return True
    except ImportError:
        return False


def get_llamaindex_version() -> str | None:
    """Get the installed LlamaIndex version.

    Returns:
        Version string or None if not installed
    """
    try:
        import llama_index.core

        return getattr(llama_index.core, "__version__", "unknown")
    except ImportError:
        return None


def safe_str(value: Any, max_length: int = 1000) -> str:
    """Safely convert a value to string with length limit.

    Args:
        value: Value to convert
        max_length: Maximum length of output string

    Returns:
        String representation, truncated if necessary
    """
    try:
        if value is None:
            return ""
        s = str(value)
        if len(s) > max_length:
            return s[:max_length] + "..."
        return s
    except Exception as e:
        return f"<error: {e}>"


def extract_node_info(node: Any) -> dict[str, Any]:
    """Extract information from a LlamaIndex node.

    Args:
        node: The node object

    Returns:
        Dictionary with node information
    """
    info = {
        "node_id": None,
        "text_length": 0,
        "score": None,
        "metadata": {},
    }

    try:
        # Get node ID
        if hasattr(node, "node_id"):
            info["node_id"] = node.node_id
        elif hasattr(node, "id_"):
            info["node_id"] = node.id_

        # Get text content
        text = None
        if hasattr(node, "text"):
            text = node.text
        elif hasattr(node, "get_content"):
            text = node.get_content()
        if text:
            info["text_length"] = len(text)
            info["text_preview"] = text[:200] + "..." if len(text) > 200 else text

        # Get score
        if hasattr(node, "score"):
            info["score"] = node.score

        # Get metadata
        if hasattr(node, "metadata"):
            info["metadata"] = {k: safe_str(v, 100) for k, v in list(node.metadata.items())[:5]}

    except Exception as e:
        logger.debug(f"Error extracting node info: {e}")

    return info


def extract_response_info(response: Any) -> dict[str, Any]:
    """Extract information from a LlamaIndex response.

    Args:
        response: The response object

    Returns:
        Dictionary with response information
    """
    info = {
        "response_length": 0,
        "source_node_count": 0,
        "has_metadata": False,
    }

    try:
        # Get response text
        response_text = None
        if hasattr(response, "response"):
            response_text = str(response.response)
        elif hasattr(response, "text"):
            response_text = response.text
        else:
            response_text = str(response)

        if response_text:
            info["response_length"] = len(response_text)
            info["response_preview"] = (
                response_text[:300] + "..." if len(response_text) > 300 else response_text
            )

        # Get source nodes
        if hasattr(response, "source_nodes"):
            info["source_node_count"] = len(response.source_nodes) if response.source_nodes else 0

        # Check for metadata
        if hasattr(response, "metadata"):
            info["has_metadata"] = bool(response.metadata)

    except Exception as e:
        logger.debug(f"Error extracting response info: {e}")

    return info


def extract_index_info(index: Any) -> dict[str, Any]:
    """Extract information from a LlamaIndex index.

    Args:
        index: The index object

    Returns:
        Dictionary with index information
    """
    info = {
        "index_type": type(index).__name__,
        "doc_count": 0,
        "index_id": None,
    }

    try:
        # Get index ID
        if hasattr(index, "index_id"):
            info["index_id"] = index.index_id

        # Try to get document count
        if hasattr(index, "docstore"):
            docstore = index.docstore
            if hasattr(docstore, "docs"):
                info["doc_count"] = len(docstore.docs)

    except Exception as e:
        logger.debug(f"Error extracting index info: {e}")

    return info


def format_retrieval_results(nodes: list[Any], max_nodes: int = 5) -> list[dict[str, Any]]:
    """Format retrieval results for tracing.

    Args:
        nodes: List of retrieved nodes
        max_nodes: Maximum number of nodes to include

    Returns:
        List of formatted node dictionaries
    """
    formatted = []

    for node in nodes[:max_nodes]:
        node_info = extract_node_info(node)
        formatted.append(node_info)

    if len(nodes) > max_nodes:
        formatted.append({"note": f"... and {len(nodes) - max_nodes} more nodes"})

    return formatted


def get_retrieval_summary(nodes: list[Any]) -> dict[str, Any]:
    """Get a summary of retrieval results.

    Args:
        nodes: List of retrieved nodes

    Returns:
        Dictionary with retrieval summary
    """
    summary = {
        "total_nodes": len(nodes),
        "avg_score": None,
        "max_score": None,
        "min_score": None,
        "total_text_length": 0,
    }

    scores = []
    for node in nodes:
        if hasattr(node, "score") and node.score is not None:
            scores.append(node.score)

        text = None
        if hasattr(node, "text"):
            text = node.text
        elif hasattr(node, "get_content"):
            with contextlib.suppress(Exception):
                text = node.get_content()

        if text:
            summary["total_text_length"] += len(text)

    if scores:
        summary["avg_score"] = sum(scores) / len(scores)
        summary["max_score"] = max(scores)
        summary["min_score"] = min(scores)

    return summary


def mask_sensitive_content(content: str, patterns: list[str] | None = None) -> str:
    """Mask potentially sensitive content in strings.

    Args:
        content: Content to mask
        patterns: Optional list of regex patterns to mask

    Returns:
        Content with sensitive data masked
    """
    import re

    if not content:
        return content

    # Default patterns for common sensitive data
    default_patterns = [
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]"),  # Email
        (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[PHONE]"),  # Phone
        (r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "[CARD]"),  # Credit card
        (r"\b\d{3}[-]?\d{2}[-]?\d{4}\b", "[SSN]"),  # SSN
        (r"(?i)(password|secret|token|api_key|apikey)[\s]*[=:]\s*[^\s,]+", "[REDACTED]"),  # Keys
    ]

    patterns_to_use = patterns if patterns is not None else default_patterns

    result = content
    for pattern, replacement in patterns_to_use:
        result = re.sub(pattern, replacement, result)

    return result
