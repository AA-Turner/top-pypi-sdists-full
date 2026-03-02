"""Memory management tools for the Open Agent.

Tools for interacting with the memory system:
- Long-term: Learned preferences and patterns
- Short-term: Session context

User identity is stored in .emdash/rules/USER.md (not in memory tools).
"""

from typing import Dict, Any, List, Optional
from emdash_core.agent.open.memory import HierarchicalMemory, MemoryEntry


class MemoryToolSet:
    """Collection of memory management tools."""

    def __init__(self, memory: HierarchicalMemory):
        self.memory = memory

    def remember(
        self,
        content: str,
        layer: str = "long_term",
        key: Optional[str] = None,
        importance: float = 0.5,
        context: str = "general",
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Store information in memory.

        Args:
            content: The information to remember
            layer: Memory layer ("long_term", "short_term")
            key: Optional identifier
            importance: 0.0-1.0 importance score
            context: Category (e.g., "coding", "preferences", "projects")
            tags: List of tags for organization

        Returns:
            Success status and stored key
        """
        try:
            stored_key = self.memory.store(
                content=content,
                layer=layer,
                key=key,
                importance=importance,
                context=context,
                tags=tags or [],
            )

            return {
                "success": True,
                "key": stored_key,
                "layer": layer,
                "message": f"Stored in {layer} memory: {stored_key}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def recall(
        self,
        query: str,
        layers: Optional[List[str]] = None,
        context: Optional[str] = None,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """Search memory for information.

        Args:
            query: Search query
            layers: Which layers to search ("long_term", "short_term")
            context: Filter by context category
            top_k: Max results per layer

        Returns:
            Matching memories grouped by layer
        """
        try:
            results = self.memory.query(
                query=query,
                layers=layers,
                context=context,
                top_k=top_k,
            )

            # Format for LLM consumption
            formatted = {}
            for layer, items in results.items():
                if items:
                    formatted[layer] = [
                        {
                            "key": k,
                            "content": e.content,
                            "context": e.context,
                            "importance": e.importance,
                            "tags": e.tags,
                        }
                        for k, e in items
                    ]

            return {
                "success": True,
                "query": query,
                "results": formatted,
                "total_found": sum(len(v) for v in results.values()),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def forget(
        self,
        key: str,
        layer: str = "long_term",
    ) -> Dict[str, Any]:
        """Remove a memory entry.

        Args:
            key: Memory key to remove
            layer: Which layer to remove from ("long_term")

        Returns:
            Success status
        """
        try:
            if layer == "long_term":
                if key in self.memory.long_term.entries:
                    del self.memory.long_term.entries[key]
                    self.memory.long_term._save()
                    removed = True
                else:
                    removed = False
            elif layer == "short_term":
                return {
                    "success": False,
                    "error": "Short-term memory doesn't support keyed removal. Use reset_memory(layer='short_term') instead.",
                }
            else:
                return {
                    "success": False,
                    "error": f"Unknown layer: {layer}. Use 'long_term'.",
                }

            return {
                "success": removed,
                "message": f"Memory {key} {'removed' if removed else 'not found'}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def list_memories(
        self,
        layer: str = "long_term",
        context: Optional[str] = None,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """List memories from a layer.

        Args:
            layer: Which layer to list ("long_term", "short_term")
            context: Optional filter by context
            limit: Max results
        """
        try:
            if layer == "long_term":
                if context:
                    entries = self.memory.long_term.get_by_context(context)
                else:
                    entries = dict(
                        sorted(
                            self.memory.long_term.entries.items(),
                            key=lambda x: -x[1].importance,
                        )
                    )
                memories = [
                    {
                        "key": k,
                        "content": e.content,
                        "context": e.context,
                        "importance": e.importance,
                        "tags": e.tags,
                        "access_count": e.access_count,
                    }
                    for k, e in list(entries.items())[:limit]
                ]
            elif layer == "short_term":
                recent = self.memory.short_term.get_recent(limit, context)
                memories = [
                    {
                        "content": e.content,
                        "context": e.context,
                        "importance": e.importance,
                    }
                    for e in recent
                ]
            else:
                return {
                    "success": False,
                    "error": f"Unknown layer: {layer}",
                }

            return {
                "success": True,
                "layer": layer,
                "count": len(memories),
                "memories": memories,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def suggest_consolidation(self) -> Dict[str, Any]:
        """Analyze short-term memory and suggest what to remember long-term."""
        suggestions = self.memory.consolidate_short_term()

        if not suggestions:
            return {
                "success": True,
                "suggestions": [],
                "message": "No high-importance items found in short-term memory.",
            }

        formatted = []
        for s in suggestions:
            formatted.append({
                "content": s["content"],
                "context": s["context"],
                "reason": s["reason"],
                "suggested_importance": 0.7,
                "action": "Use remember() to store this in long_term memory",
            })

        return {
            "success": True,
            "suggestions": formatted,
            "message": f"Found {len(formatted)} items that might be worth remembering long-term.",
        }

    def export_memory(self, layer: Optional[str] = None) -> Dict[str, Any]:
        """Export memory data.

        Args:
            layer: Specific layer or all if None
        """
        try:
            if layer:
                if layer == "long_term":
                    data = {k: e.to_dict() for k, e in self.memory.long_term.entries.items()}
                elif layer == "short_term":
                    data = [e.to_dict() for e in self.memory.short_term.entries]
                else:
                    return {
                        "success": False,
                        "error": f"Unknown layer: {layer}",
                    }
                return {
                    "success": True,
                    "layer": layer,
                    "data": data,
                }
            else:
                return {
                    "success": True,
                    "all_layers": self.memory.export_all(),
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        stats = self.memory.get_stats()
        return {
            "success": True,
            "stats": stats,
            "summary": {
                "total_entries": sum(s["entry_count"] for s in stats.values()),
                "total_capacity": sum(s["max_entries"] for s in stats.values()),
                "utilization": f"{sum(s['entry_count'] for s in stats.values()) / sum(s['max_entries'] for s in stats.values()):.1%}",
            },
        }

    def reset_memory(
        self,
        layer: Optional[str] = None,
        confirm: bool = False,
    ) -> Dict[str, Any]:
        """Reset memory layer(s).

        Args:
            layer: Which layer ("long_term", "short_term", or None for all)
            confirm: Must be True to actually reset
        """
        if not confirm:
            return {
                "success": False,
                "error": "Must set confirm=True to reset memory. This cannot be undone.",
                "warning": f"This will reset {'all' if layer is None else layer} memory layers.",
            }

        try:
            self.memory.reset(layer)
            return {
                "success": True,
                "message": f"Reset {'all' if layer is None else layer} memory.",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
