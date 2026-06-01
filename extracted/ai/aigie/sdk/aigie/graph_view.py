"""
Agent Graph View for visualizing agent execution flows.

Provides tools to build, visualize, and analyze agent execution graphs
showing the flow of operations, decision points, and data transformations.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class NodeType(Enum):
    """Types of nodes in an agent graph."""

    AGENT = "agent"
    TOOL = "tool"
    LLM = "llm"
    CHAIN = "chain"
    RETRIEVER = "retriever"
    DECISION = "decision"
    PARALLEL = "parallel"
    LOOP = "loop"
    START = "start"
    END = "end"
    ERROR = "error"
    HUMAN_INPUT = "human_input"
    SUBGRAPH = "subgraph"


class EdgeType(Enum):
    """Types of edges connecting nodes."""

    SEQUENTIAL = "sequential"
    CONDITIONAL = "conditional"
    PARALLEL = "parallel"
    ERROR = "error"
    RETRY = "retry"
    LOOP = "loop"
    CALLBACK = "callback"


class NodeStatus(Enum):
    """Execution status of a node."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class GraphNode:
    """A node in the agent execution graph."""

    id: str
    name: str
    type: NodeType
    status: NodeStatus = NodeStatus.PENDING

    # Execution details
    input_data: dict[str, Any] | None = None
    output_data: dict[str, Any] | None = None
    error: str | None = None

    # Timing
    started_at: datetime | None = None
    ended_at: datetime | None = None
    duration_ms: float | None = None

    # Metrics
    tokens_used: int = 0
    cost_usd: float | None = None

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)

    # Position for visualization
    x: float = 0.0
    y: float = 0.0

    # For subgraphs
    children: list[str] = field(default_factory=list)
    parent_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "status": self.status.value,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "error": self.error,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "duration_ms": self.duration_ms,
            "tokens_used": self.tokens_used,
            "cost_usd": self.cost_usd,
            "metadata": self.metadata,
            "tags": self.tags,
            "position": {"x": self.x, "y": self.y},
            "children": self.children,
            "parent_id": self.parent_id,
        }


@dataclass
class GraphEdge:
    """An edge connecting two nodes in the graph."""

    id: str
    source_id: str
    target_id: str
    type: EdgeType = EdgeType.SEQUENTIAL

    # Conditional edges
    condition: str | None = None
    condition_result: bool | None = None

    # Edge metadata
    label: str | None = None
    data_passed: dict[str, Any] | None = None

    # Timing
    traversed_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "type": self.type.value,
            "condition": self.condition,
            "condition_result": self.condition_result,
            "label": self.label,
            "data_passed": self.data_passed,
            "traversed_at": self.traversed_at.isoformat() if self.traversed_at else None,
        }


@dataclass
class ExecutionPath:
    """A single path through the graph during execution."""

    id: str
    node_sequence: list[str]
    edge_sequence: list[str]
    total_duration_ms: float
    total_tokens: int
    total_cost_usd: float
    success: bool
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "node_sequence": self.node_sequence,
            "edge_sequence": self.edge_sequence,
            "total_duration_ms": self.total_duration_ms,
            "total_tokens": self.total_tokens,
            "total_cost_usd": self.total_cost_usd,
            "success": self.success,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class GraphMetrics:
    """Aggregated metrics for a graph."""

    total_nodes: int = 0
    total_edges: int = 0
    total_executions: int = 0

    # Node type counts
    node_type_counts: dict[str, int] = field(default_factory=dict)

    # Performance
    avg_duration_ms: float = 0.0
    p50_duration_ms: float = 0.0
    p90_duration_ms: float = 0.0
    p99_duration_ms: float = 0.0

    # Success rates
    success_rate: float = 0.0
    error_rate: float = 0.0

    # Token usage
    total_tokens: int = 0
    avg_tokens_per_execution: float = 0.0

    # Cost
    total_cost_usd: float = 0.0
    avg_cost_per_execution: float = 0.0

    # Path analysis
    most_common_path: list[str] | None = None
    bottleneck_nodes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_nodes": self.total_nodes,
            "total_edges": self.total_edges,
            "total_executions": self.total_executions,
            "node_type_counts": self.node_type_counts,
            "avg_duration_ms": self.avg_duration_ms,
            "p50_duration_ms": self.p50_duration_ms,
            "p90_duration_ms": self.p90_duration_ms,
            "p99_duration_ms": self.p99_duration_ms,
            "success_rate": self.success_rate,
            "error_rate": self.error_rate,
            "total_tokens": self.total_tokens,
            "avg_tokens_per_execution": self.avg_tokens_per_execution,
            "total_cost_usd": self.total_cost_usd,
            "avg_cost_per_execution": self.avg_cost_per_execution,
            "most_common_path": self.most_common_path,
            "bottleneck_nodes": self.bottleneck_nodes,
        }


class AgentGraph:
    """
    Represents an agent execution graph.

    Usage:
        graph = AgentGraph(name="research_agent")

        # Define graph structure
        start = graph.add_node("start", NodeType.START)
        planner = graph.add_node("planner", NodeType.LLM)
        search = graph.add_node("search", NodeType.TOOL)
        synthesize = graph.add_node("synthesize", NodeType.LLM)
        end = graph.add_node("end", NodeType.END)

        # Define edges
        graph.add_edge(start, planner)
        graph.add_edge(planner, search, condition="needs_search")
        graph.add_edge(search, synthesize)
        graph.add_edge(synthesize, end)

        # Record execution
        graph.start_execution("exec_123")
        graph.record_node_start("planner")
        graph.record_node_end("planner", output={"plan": "..."})
        ...
    """

    def __init__(
        self,
        id: str | None = None,
        name: str = "agent_graph",
        description: str | None = None,
    ):
        self.id = id or str(uuid4())
        self.name = name
        self.description = description

        self._nodes: dict[str, GraphNode] = {}
        self._edges: dict[str, GraphEdge] = {}
        self._execution_paths: list[ExecutionPath] = []

        # Current execution state
        self._current_execution_id: str | None = None
        self._current_path: list[str] = []
        self._current_edges: list[str] = []

        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    # =========================================================================
    # Graph Building
    # =========================================================================

    def add_node(
        self,
        name: str,
        type: NodeType,
        id: str | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        x: float = 0.0,
        y: float = 0.0,
    ) -> str:
        """Add a node to the graph."""
        node_id = id or str(uuid4())
        node = GraphNode(
            id=node_id,
            name=name,
            type=type,
            metadata=metadata or {},
            tags=tags or [],
            x=x,
            y=y,
        )
        self._nodes[node_id] = node
        self.updated_at = datetime.utcnow()
        return node_id

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        type: EdgeType = EdgeType.SEQUENTIAL,
        condition: str | None = None,
        label: str | None = None,
    ) -> str:
        """Add an edge between two nodes."""
        edge_id = str(uuid4())
        edge = GraphEdge(
            id=edge_id,
            source_id=source_id,
            target_id=target_id,
            type=type,
            condition=condition,
            label=label,
        )
        self._edges[edge_id] = edge
        self.updated_at = datetime.utcnow()
        return edge_id

    def add_subgraph(
        self,
        parent_id: str,
        subgraph: AgentGraph,
    ) -> str:
        """Add a subgraph as a child of a node."""
        # Add all nodes from subgraph
        for node in subgraph._nodes.values():
            node.parent_id = parent_id
            self._nodes[node.id] = node

        # Add all edges from subgraph
        for edge in subgraph._edges.values():
            self._edges[edge.id] = edge

        # Update parent's children
        if parent_id in self._nodes:
            self._nodes[parent_id].children.extend(list(subgraph._nodes.keys()))

        self.updated_at = datetime.utcnow()
        return subgraph.id

    def remove_node(self, node_id: str) -> bool:
        """Remove a node and its connected edges."""
        if node_id not in self._nodes:
            return False

        # Remove connected edges
        edges_to_remove = [
            edge_id
            for edge_id, edge in self._edges.items()
            if node_id in (edge.source_id, edge.target_id)
        ]
        for edge_id in edges_to_remove:
            del self._edges[edge_id]

        del self._nodes[node_id]
        self.updated_at = datetime.utcnow()
        return True

    def remove_edge(self, edge_id: str) -> bool:
        """Remove an edge."""
        if edge_id in self._edges:
            del self._edges[edge_id]
            self.updated_at = datetime.utcnow()
            return True
        return False

    # =========================================================================
    # Execution Recording
    # =========================================================================

    def start_execution(self, execution_id: str | None = None) -> str:
        """Start recording a new execution."""
        self._current_execution_id = execution_id or str(uuid4())
        self._current_path = []
        self._current_edges = []

        # Reset all node statuses
        for node in self._nodes.values():
            node.status = NodeStatus.PENDING
            node.started_at = None
            node.ended_at = None
            node.duration_ms = None
            node.input_data = None
            node.output_data = None
            node.error = None

        return self._current_execution_id

    def record_node_start(
        self,
        node_id: str,
        input_data: dict[str, Any] | None = None,
    ) -> bool:
        """Record that a node has started execution."""
        if node_id not in self._nodes:
            return False

        node = self._nodes[node_id]
        node.status = NodeStatus.RUNNING
        node.started_at = datetime.utcnow()
        node.input_data = input_data

        self._current_path.append(node_id)
        return True

    def record_node_end(
        self,
        node_id: str,
        output_data: dict[str, Any] | None = None,
        status: NodeStatus = NodeStatus.SUCCESS,
        error: str | None = None,
        tokens_used: int = 0,
        cost_usd: float | None = None,
    ) -> bool:
        """Record that a node has finished execution."""
        if node_id not in self._nodes:
            return False

        node = self._nodes[node_id]
        node.ended_at = datetime.utcnow()
        node.output_data = output_data
        node.status = status
        node.error = error
        node.tokens_used = tokens_used
        node.cost_usd = cost_usd

        if node.started_at:
            node.duration_ms = (node.ended_at - node.started_at).total_seconds() * 1000

        return True

    def record_edge_traversal(
        self,
        edge_id: str,
        condition_result: bool | None = None,
        data_passed: dict[str, Any] | None = None,
    ) -> bool:
        """Record that an edge was traversed."""
        if edge_id not in self._edges:
            return False

        edge = self._edges[edge_id]
        edge.traversed_at = datetime.utcnow()
        edge.condition_result = condition_result
        edge.data_passed = data_passed

        self._current_edges.append(edge_id)
        return True

    def end_execution(self, success: bool = True) -> ExecutionPath | None:
        """End the current execution and save the path."""
        if not self._current_execution_id:
            return None

        # Calculate totals
        total_duration = sum(
            n.duration_ms or 0 for n in self._nodes.values() if n.id in self._current_path
        )
        total_tokens = sum(
            n.tokens_used for n in self._nodes.values() if n.id in self._current_path
        )
        total_cost = sum(
            n.cost_usd or 0 for n in self._nodes.values() if n.id in self._current_path
        )

        path = ExecutionPath(
            id=self._current_execution_id,
            node_sequence=self._current_path.copy(),
            edge_sequence=self._current_edges.copy(),
            total_duration_ms=total_duration,
            total_tokens=total_tokens,
            total_cost_usd=total_cost,
            success=success,
        )

        self._execution_paths.append(path)
        self._current_execution_id = None
        self._current_path = []
        self._current_edges = []

        return path

    # =========================================================================
    # Analysis
    # =========================================================================

    def get_node(self, node_id: str) -> GraphNode | None:
        """Get a node by ID."""
        return self._nodes.get(node_id)

    def get_edge(self, edge_id: str) -> GraphEdge | None:
        """Get an edge by ID."""
        return self._edges.get(edge_id)

    def get_nodes(
        self,
        type: NodeType | None = None,
        status: NodeStatus | None = None,
    ) -> list[GraphNode]:
        """Get nodes with optional filtering."""
        nodes = list(self._nodes.values())

        if type:
            nodes = [n for n in nodes if n.type == type]

        if status:
            nodes = [n for n in nodes if n.status == status]

        return nodes

    def get_edges_from(self, node_id: str) -> list[GraphEdge]:
        """Get all edges originating from a node."""
        return [e for e in self._edges.values() if e.source_id == node_id]

    def get_edges_to(self, node_id: str) -> list[GraphEdge]:
        """Get all edges pointing to a node."""
        return [e for e in self._edges.values() if e.target_id == node_id]

    def get_children(self, node_id: str) -> list[GraphNode]:
        """Get child nodes of a subgraph node."""
        node = self._nodes.get(node_id)
        if not node:
            return []
        return [self._nodes[cid] for cid in node.children if cid in self._nodes]

    def get_metrics(self) -> GraphMetrics:
        """Calculate aggregated metrics for the graph."""
        metrics = GraphMetrics()
        metrics.total_nodes = len(self._nodes)
        metrics.total_edges = len(self._edges)
        metrics.total_executions = len(self._execution_paths)

        # Node type counts
        for node in self._nodes.values():
            type_name = node.type.value
            metrics.node_type_counts[type_name] = metrics.node_type_counts.get(type_name, 0) + 1

        if self._execution_paths:
            durations = [p.total_duration_ms for p in self._execution_paths]
            durations.sort()

            metrics.avg_duration_ms = sum(durations) / len(durations)
            metrics.p50_duration_ms = durations[len(durations) // 2]
            metrics.p90_duration_ms = durations[int(len(durations) * 0.9)]
            metrics.p99_duration_ms = durations[int(len(durations) * 0.99)]

            success_count = sum(1 for p in self._execution_paths if p.success)
            metrics.success_rate = success_count / len(self._execution_paths)
            metrics.error_rate = 1 - metrics.success_rate

            metrics.total_tokens = sum(p.total_tokens for p in self._execution_paths)
            metrics.avg_tokens_per_execution = metrics.total_tokens / len(self._execution_paths)

            metrics.total_cost_usd = sum(p.total_cost_usd for p in self._execution_paths)
            metrics.avg_cost_per_execution = metrics.total_cost_usd / len(self._execution_paths)

            # Find most common path
            path_counts: dict[str, int] = {}
            for path in self._execution_paths:
                path_key = ",".join(path.node_sequence)
                path_counts[path_key] = path_counts.get(path_key, 0) + 1

            if path_counts:
                most_common = max(path_counts, key=path_counts.get)
                metrics.most_common_path = most_common.split(",")

            # Find bottleneck nodes (highest avg duration)
            node_durations: dict[str, list[float]] = {}
            for path in self._execution_paths:
                for node_id in path.node_sequence:
                    node = self._nodes.get(node_id)
                    if node and node.duration_ms:
                        if node_id not in node_durations:
                            node_durations[node_id] = []
                        node_durations[node_id].append(node.duration_ms)

            if node_durations:
                avg_durations = {nid: sum(durs) / len(durs) for nid, durs in node_durations.items()}
                sorted_nodes = sorted(avg_durations, key=avg_durations.get, reverse=True)
                metrics.bottleneck_nodes = sorted_nodes[:3]

        return metrics

    def find_critical_path(self) -> list[str]:
        """Find the critical path (longest duration) through the graph."""
        if not self._execution_paths:
            return []

        # Find the path with longest duration
        longest_path = max(self._execution_paths, key=lambda p: p.total_duration_ms)
        return longest_path.node_sequence

    def find_error_prone_nodes(self, threshold: float = 0.1) -> list[tuple[str, float]]:
        """Find nodes with error rate above threshold."""
        node_errors: dict[str, int] = {}
        node_total: dict[str, int] = {}

        for path in self._execution_paths:
            for node_id in path.node_sequence:
                node = self._nodes.get(node_id)
                if node:
                    node_total[node_id] = node_total.get(node_id, 0) + 1
                    if node.status == NodeStatus.FAILURE:
                        node_errors[node_id] = node_errors.get(node_id, 0) + 1

        error_prone = []
        for node_id, total in node_total.items():
            error_count = node_errors.get(node_id, 0)
            error_rate = error_count / total
            if error_rate >= threshold:
                error_prone.append((node_id, error_rate))

        return sorted(error_prone, key=lambda x: x[1], reverse=True)

    # =========================================================================
    # Serialization
    # =========================================================================

    def to_dict(self) -> dict[str, Any]:
        """Convert graph to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "nodes": [n.to_dict() for n in self._nodes.values()],
            "edges": [e.to_dict() for e in self._edges.values()],
            "execution_paths": [p.to_dict() for p in self._execution_paths],
            "metrics": self.get_metrics().to_dict(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert graph to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AgentGraph:
        """Create graph from dictionary."""
        graph = cls(
            id=data.get("id"),
            name=data.get("name", "agent_graph"),
            description=data.get("description"),
        )

        # Restore nodes
        for node_data in data.get("nodes", []):
            node = GraphNode(
                id=node_data["id"],
                name=node_data["name"],
                type=NodeType(node_data["type"]),
                status=NodeStatus(node_data.get("status", "pending")),
                input_data=node_data.get("input_data"),
                output_data=node_data.get("output_data"),
                error=node_data.get("error"),
                tokens_used=node_data.get("tokens_used", 0),
                cost_usd=node_data.get("cost_usd"),
                metadata=node_data.get("metadata", {}),
                tags=node_data.get("tags", []),
                x=node_data.get("position", {}).get("x", 0),
                y=node_data.get("position", {}).get("y", 0),
                children=node_data.get("children", []),
                parent_id=node_data.get("parent_id"),
            )
            graph._nodes[node.id] = node

        # Restore edges
        for edge_data in data.get("edges", []):
            edge = GraphEdge(
                id=edge_data["id"],
                source_id=edge_data["source_id"],
                target_id=edge_data["target_id"],
                type=EdgeType(edge_data.get("type", "sequential")),
                condition=edge_data.get("condition"),
                condition_result=edge_data.get("condition_result"),
                label=edge_data.get("label"),
                data_passed=edge_data.get("data_passed"),
            )
            graph._edges[edge.id] = edge

        return graph

    def to_mermaid(self) -> str:
        """Export graph as Mermaid diagram syntax."""
        lines = ["flowchart TD"]

        # Add nodes
        for node in self._nodes.values():
            shape_start, shape_end = self._get_mermaid_shape(node.type)
            lines.append(f'    {node.id}{shape_start}"{node.name}"{shape_end}')

        # Add edges
        for edge in self._edges.values():
            arrow = self._get_mermaid_arrow(edge.type)
            label = f"|{edge.label}|" if edge.label else ""
            lines.append(f"    {edge.source_id} {arrow}{label} {edge.target_id}")

        return "\n".join(lines)

    def _get_mermaid_shape(self, node_type: NodeType) -> tuple[str, str]:
        """Get Mermaid shape syntax for node type."""
        shapes = {
            NodeType.START: ("([", "])"),
            NodeType.END: ("([", "])"),
            NodeType.AGENT: ("[", "]"),
            NodeType.LLM: ("[[", "]]"),
            NodeType.TOOL: ("{{", "}}"),
            NodeType.CHAIN: ("[/", "\\]"),
            NodeType.DECISION: ("{", "}"),
            NodeType.PARALLEL: ("[[", "]]"),
            NodeType.LOOP: ("(((", ")))"),
            NodeType.ERROR: (">", "]"),
            NodeType.HUMAN_INPUT: ("((", "))"),
            NodeType.SUBGRAPH: ("[[", "]]"),
            NodeType.RETRIEVER: ("[(", ")]"),
        }
        return shapes.get(node_type, ("[", "]"))

    def _get_mermaid_arrow(self, edge_type: EdgeType) -> str:
        """Get Mermaid arrow syntax for edge type."""
        arrows = {
            EdgeType.SEQUENTIAL: "-->",
            EdgeType.CONDITIONAL: "-.->",
            EdgeType.PARALLEL: "==>",
            EdgeType.ERROR: "-. error .->",
            EdgeType.RETRY: "-. retry .->",
            EdgeType.LOOP: "-->",
            EdgeType.CALLBACK: "~~>",
        }
        return arrows.get(edge_type, "-->")


class GraphBuilder:
    """
    Fluent builder for constructing agent graphs.

    Usage:
        graph = (GraphBuilder("my_agent")
            .start("entry")
            .llm("planner", "Plan the task")
            .decision("needs_search")
                .on_true()
                    .tool("search", "Web search")
                    .end_branch()
                .on_false()
                    .llm("answer", "Direct answer")
                    .end_branch()
            .llm("synthesize", "Combine results")
            .end("complete")
            .build())
    """

    def __init__(self, name: str, description: str | None = None):
        self._graph = AgentGraph(name=name, description=description)
        self._current_node: str | None = None
        self._branch_stack: list[str] = []
        self._x_pos = 0
        self._y_pos = 0

    def _add_node(self, name: str, type: NodeType, **kwargs) -> GraphBuilder:
        """Internal method to add a node."""
        node_id = self._graph.add_node(
            name=name,
            type=type,
            x=self._x_pos,
            y=self._y_pos,
            **kwargs,
        )

        if self._current_node:
            self._graph.add_edge(self._current_node, node_id)

        self._current_node = node_id
        self._y_pos += 100
        return self

    def start(self, name: str = "start") -> GraphBuilder:
        """Add a start node."""
        return self._add_node(name, NodeType.START)

    def end(self, name: str = "end") -> GraphBuilder:
        """Add an end node."""
        return self._add_node(name, NodeType.END)

    def llm(self, name: str, description: str | None = None) -> GraphBuilder:
        """Add an LLM node."""
        return self._add_node(name, NodeType.LLM, metadata={"description": description})

    def tool(self, name: str, description: str | None = None) -> GraphBuilder:
        """Add a tool node."""
        return self._add_node(name, NodeType.TOOL, metadata={"description": description})

    def agent(self, name: str, description: str | None = None) -> GraphBuilder:
        """Add an agent node."""
        return self._add_node(name, NodeType.AGENT, metadata={"description": description})

    def chain(self, name: str, description: str | None = None) -> GraphBuilder:
        """Add a chain node."""
        return self._add_node(name, NodeType.CHAIN, metadata={"description": description})

    def decision(self, name: str, condition: str | None = None) -> GraphBuilder:
        """Add a decision node."""
        self._add_node(name, NodeType.DECISION, metadata={"condition": condition})
        self._branch_stack.append(self._current_node)
        return self

    def on_true(self) -> GraphBuilder:
        """Start the true branch of a decision."""
        self._x_pos -= 150
        return self

    def on_false(self) -> GraphBuilder:
        """Start the false branch of a decision."""
        self._x_pos += 150
        return self

    def end_branch(self) -> GraphBuilder:
        """End current branch and return to decision point."""
        if self._branch_stack:
            self._current_node = self._branch_stack[-1]
        self._x_pos = 0
        return self

    def merge(self, name: str = "merge") -> GraphBuilder:
        """Add a merge point after branches."""
        self._branch_stack.pop() if self._branch_stack else None
        return self._add_node(name, NodeType.CHAIN)

    def parallel(self, name: str, branches: list[Callable[[GraphBuilder], None]]) -> GraphBuilder:
        """Add parallel execution branches."""
        self._add_node(name, NodeType.PARALLEL)
        start_node = self._current_node

        for i, branch_fn in enumerate(branches):
            self._current_node = start_node
            self._x_pos = (i - len(branches) // 2) * 150
            branch_fn(self)

        self._x_pos = 0
        return self

    def build(self) -> AgentGraph:
        """Build and return the graph."""
        return self._graph


# Convenience function
def create_graph(name: str, description: str | None = None) -> AgentGraph:
    """Create a new agent graph."""
    return AgentGraph(name=name, description=description)


def create_graph_builder(name: str, description: str | None = None) -> GraphBuilder:
    """Create a new graph builder."""
    return GraphBuilder(name=name, description=description)
