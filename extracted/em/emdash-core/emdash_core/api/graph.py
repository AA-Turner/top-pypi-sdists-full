"""Graph query endpoints for MCP server proxy."""

from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/graph", tags=["graph"])


class QueryRequest(BaseModel):
    """Request to execute a Cypher query."""
    query: str = Field(..., description="Cypher query to execute")
    params: dict[str, Any] = Field(default_factory=dict, description="Query parameters")


class QueryResponse(BaseModel):
    """Response from a Cypher query."""
    rows: list[dict[str, Any]] = Field(default_factory=list)
    columns: list[str] = Field(default_factory=list)
    row_count: int = 0


class GraphRefreshRequest(BaseModel):
    """Request to refresh graph for specific files."""
    files: list[dict[str, str]] = Field(
        ...,
        description="List of files with path and action (created/modified/deleted)"
    )


class GraphRefreshResponse(BaseModel):
    """Response from graph refresh."""
    nodes_updated: int = 0
    edges_updated: int = 0
    new_nodes: list[dict[str, Any]] = Field(default_factory=list)
    new_edges: list[dict[str, Any]] = Field(default_factory=list)
    summary: str = ""


class GraphDiffResponse(BaseModel):
    """Response for graph diff query."""
    added: dict[str, list[dict[str, Any]]] = Field(default_factory=dict)
    modified: dict[str, list[dict[str, Any]]] = Field(default_factory=dict)
    removed: dict[str, list[dict[str, Any]]] = Field(default_factory=dict)
    summary: str = ""


@router.post("/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    """Execute a read-only Cypher query.

    This endpoint is used by the MCP server to proxy queries through
    the emdash server, avoiding KuzuDB lock conflicts.

    Only read queries are allowed (no CREATE, MERGE, SET, DELETE).
    """
    # Basic safety check - block write operations
    query_upper = request.query.upper()
    write_keywords = ["CREATE", "MERGE", "SET ", "DELETE", "DROP", "REMOVE"]
    for keyword in write_keywords:
        if keyword in query_upper:
            raise HTTPException(
                status_code=400,
                detail=f"Write operations not allowed via this endpoint: {keyword}"
            )

    try:
        from ..graph.connection import get_read_connection

        conn = get_read_connection()
        rows = conn.execute(request.query, request.params)

        columns = list(rows[0].keys()) if rows else []

        return QueryResponse(
            rows=rows,
            columns=columns,
            row_count=len(rows),
        )
    except Exception as e:
        error_msg = str(e)
        # Provide helpful error for common issues
        if "not found" in error_msg.lower() or "does not exist" in error_msg.lower():
            raise HTTPException(
                status_code=404,
                detail=f"Query failed - table or property may not exist: {error_msg}"
            )
        raise HTTPException(status_code=500, detail=error_msg)


@router.get("/health")
async def graph_health():
    """Check if graph database is accessible."""
    try:
        from ..graph.connection import get_read_connection

        conn = get_read_connection()
        conn.execute("RETURN 1 AS num", {})
        return {"status": "healthy", "database": "kuzu"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@router.post("/refresh", response_model=GraphRefreshResponse)
async def refresh_graph(request: GraphRefreshRequest):
    """Refresh graph for specific files incrementally.
    
    Called after agent file modifications to update the knowledge graph.
    Returns summary of changes made.
    """
    from ..graph.builder import GraphBuilder
    
    builder = GraphBuilder()
    
    nodes_updated = 0
    edges_updated = 0
    new_nodes = []
    new_edges = []
    
    for file_info in request.files:
        file_path = file_info.get("path")
        action = file_info.get("action", "modified")
        
        if not file_path:
            continue
        
        try:
            # Parse the file and update graph incrementally
            result = builder.refresh_single_file(file_path)
            nodes_updated += result.get("nodes_updated", 0)
            edges_updated += result.get("edges_updated", 0)
            new_nodes.extend(result.get("new_nodes", []))
            new_edges.extend(result.get("new_edges", []))
        except Exception as e:
            # Log but don't fail - graph refresh is optional
            import logging
            logging.warning(f"Failed to refresh graph for {file_path}: {e}")
    
    # Generate summary
    file_count = len(request.files)
    summary = f"Refreshed {file_count} file(s). Updated {nodes_updated} nodes, {edges_updated} edges."
    
    return GraphRefreshResponse(
        nodes_updated=nodes_updated,
        edges_updated=edges_updated,
        new_nodes=new_nodes,
        new_edges=new_edges,
        summary=summary,
    )


@router.get("/diff", response_model=GraphDiffResponse)
async def get_graph_diff(
    since: Optional[str] = Query(
        None, description="ISO timestamp to get changes since"
    ),
    limit: int = Query(default=50, description="Maximum number of changes to return"),
):
    """Get changes in the graph since a given time.
    
    Returns added/modified/removed nodes and edges for real-time
    architectural feedback display in chat.
    """
    try:
        from ..graph.connection import get_read_connection
        
        conn = get_read_connection()
        
        # Query for recently modified nodes
        query = """
        MATCH (n)
        WHERE n.last_modified IS NOT NULL
        RETURN n, labels(n) as labels
        ORDER BY n.last_modified DESC
        LIMIT $limit
        """
        
        rows = conn.execute(query, {"limit": limit})
        
        added_nodes = []
        modified_nodes = []
        removed_nodes = []
        
        for row in rows:
            node_data = dict(row["n"])
            labels = row["labels"]
            node_type = labels[0] if labels else "Unknown"
            
            node_info = {
                "id": node_data.get("id") or node_data.get("qualified_name") or node_data.get("path"),
                "type": node_type,
                "data": node_data,
            }
            
            modified_nodes.append(node_info)
        
        summary = f"Found {len(modified_nodes)} recently modified nodes"
        
        return GraphDiffResponse(
            added={"nodes": added_nodes, "edges": []},
            modified={"nodes": modified_nodes, "edges": []},
            removed={"nodes": removed_nodes, "edges": []},
            summary=summary,
        )
    except Exception as e:
        return GraphDiffResponse(
            summary=f"Error fetching diff: {str(e)}"
        )


@router.get("/changes/recent")
async def get_recent_changes(
    limit: int = Query(default=20, description="Maximum number of changes to return"),
):
    """Get recently changed nodes/edges for real-time feedback.
    
    This is a fast query optimized for real-time display in chat.
    """
    try:
        from ..graph.connection import get_read_connection
        
        conn = get_read_connection()
        
        # Query for changed files and their relationships
        query = """
        MATCH (f:File)-[r]->(target)
        WHERE f.last_modified IS NOT NULL
        RETURN f, r, target
        ORDER BY f.last_modified DESC
        LIMIT $limit
        """
        
        rows = conn.execute(query, {"limit": limit})
        
        changes = []
        for row in rows:
            f = dict(row["f"])
            r = dict(row["r"])
            target = dict(row["target"])
            
            changes.append({
                "file": {
                    "path": f.get("path"),
                    "qualified_name": f.get("qualified_name"),
                    "type": "file",
                },
                "edge": {
                    "type": r.get("label", "relates_to"),
                    "target_type": target.get("label", "unknown"),
                    "target_name": target.get("qualified_name") or target.get("name"),
                },
                "timestamp": f.get("last_modified"),
            })
        
        return {
            "changes": changes,
            "count": len(changes),
        }
    except Exception as e:
        return {"changes": [], "count": 0, "error": str(e)}
