"""Database management endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/db", tags=["database"])


class DbStats(BaseModel):
    """Database statistics."""
    node_count: int
    relationship_count: int
    file_count: int
    function_count: int
    class_count: int
    community_count: int


class DbInitResponse(BaseModel):
    """Response from database initialization."""
    success: bool
    message: str


class DbTestResponse(BaseModel):
    """Response from database test."""
    connected: bool
    database_path: str
    message: str


def _get_connection():
    """Get database connection."""
    from ..graph.connection import KuzuConnection
    return KuzuConnection()


@router.post("/init", response_model=DbInitResponse)
async def db_init():
    """Initialize the Kuzu database schema.

    Creates all node and relationship tables required for the knowledge graph.
    """
    try:
        conn = _get_connection()
        from ..graph.schema import SchemaManager

        schema = SchemaManager(conn)
        schema.initialize_schema()

        return DbInitResponse(
            success=True,
            message="Database schema initialized successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear", response_model=DbInitResponse)
async def db_clear(confirm: bool = False):
    """Clear all data from the database.

    Args:
        confirm: Must be True to proceed with clearing
    """
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="Must set confirm=true to clear database"
        )

    try:
        conn = _get_connection()
        conn.clear_database()

        return DbInitResponse(
            success=True,
            message="Database cleared successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=DbStats)
async def db_stats():
    """Get database statistics."""
    try:
        conn = _get_connection()
        info = conn.get_database_info()

        return DbStats(
            node_count=info.get("node_count", 0),
            relationship_count=info.get("relationship_count", 0),
            file_count=info.get("file_count", 0),
            function_count=info.get("function_count", 0),
            class_count=info.get("class_count", 0),
            community_count=info.get("community_count", 0),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test", response_model=DbTestResponse)
async def db_test():
    """Test database connection."""
    try:
        conn = _get_connection()
        # Try to connect
        conn.connect()

        return DbTestResponse(
            connected=True,
            database_path=str(conn.database_path),
            message="Database connection successful"
        )
    except Exception as e:
        return DbTestResponse(
            connected=False,
            database_path="",
            message=str(e)
        )
