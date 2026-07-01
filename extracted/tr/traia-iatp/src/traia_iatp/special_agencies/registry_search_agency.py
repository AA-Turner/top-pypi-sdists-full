"""
Registry Search Utility Agency

A special utility agency that provides search capabilities for finding other utility agencies.
This agency exposes MongoDB registry search functionality via the A2A protocol.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from a2a import A2AServer, ToolResult
import uvicorn
from datetime import datetime

from ..registry.mongodb_registry import UtilityAgencyRegistry
from ..utils import get_now_in_utc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Registry Search Utility Agency")

# Create A2A server
a2a_server = A2AServer(
    name="Registry Search Agency",
    description="Searches for utility agencies in the IATP registry",
    version="1.0.0"
)

# MongoDB registry instance
_registry: Optional[UtilityAgencyRegistry] = None


def get_registry() -> UtilityAgencyRegistry:
    """Get or create MongoDB registry instance."""
    global _registry
    if _registry is None:
        mongodb_uri = os.getenv("MONGODB_URI")
        if not mongodb_uri:
            raise ValueError("MONGODB_URI environment variable is required")
        _registry = UtilityAgencyRegistry(mongodb_uri)
    return _registry


@a2a_server.tool(
    name="search_utility_agencies",
    description="Search for utility agencies by query, tags, or capabilities"
)
async def search_utility_agencies(
    query: Optional[str] = None,
    tags: Optional[List[str]] = None,
    capabilities: Optional[List[str]] = None,
    limit: int = 10
) -> ToolResult:
    """Search for utility agencies in the registry."""
    try:
        registry = get_registry()
        
        # Query agencies
        agencies = await registry.query_agencies(
            query=query,
            tags=tags,
            capabilities=capabilities,
            active_only=True,
            limit=limit
        )
        
        # Convert to simple dict format
        results = []
        for agency in agencies:
            results.append({
                "agency_id": agency.agency_id,
                "name": agency.name,
                "description": agency.description,
                "endpoint": str(agency.endpoint),
                "capabilities": agency.capabilities,
                "tags": agency.tags,
                "is_active": agency.is_active
            })
        
        return ToolResult(
            output=results,
            metadata={
                "count": len(results),
                "query": query,
                "tags": tags,
                "capabilities": capabilities
            }
        )
    except Exception as e:
        logger.error(f"Error searching agencies: {e}")
        raise


@a2a_server.tool(
    name="get_agency_by_id",
    description="Get detailed information about a specific utility agency"
)
async def get_agency_by_id(agency_id: str) -> ToolResult:
    """Get a specific agency by ID."""
    try:
        registry = get_registry()
        
        agency = await registry.get_agency_by_id(agency_id)
        if not agency:
            return ToolResult(
                output=None,
                metadata={"error": f"Agency {agency_id} not found"}
            )
        
        result = {
            "agency_id": agency.agency_id,
            "name": agency.name,
            "description": agency.description,
            "endpoint": str(agency.endpoint),
            "capabilities": agency.capabilities,
            "tags": agency.tags,
            "metadata": agency.metadata,
            "registered_at": agency.registered_at.isoformat() if agency.registered_at else None,
            "last_health_check": agency.last_health_check.isoformat() if agency.last_health_check else None,
            "is_active": agency.is_active
        }
        
        return ToolResult(
            output=result,
            metadata={"agency_id": agency_id}
        )
    except Exception as e:
        logger.error(f"Error getting agency {agency_id}: {e}")
        raise


@a2a_server.tool(
    name="get_registry_statistics",
    description="Get statistics about the utility agency registry"
)
async def get_registry_statistics() -> ToolResult:
    """Get registry statistics."""
    try:
        registry = get_registry()
        
        stats = await registry.get_statistics()
        
        return ToolResult(
            output=stats,
            metadata={"timestamp": get_now_in_utc().isoformat()}
        )
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise


@a2a_server.tool(
    name="find_agencies_by_capability",
    description="Find all agencies that have a specific capability"
)
async def find_agencies_by_capability(capability: str, limit: int = 20) -> ToolResult:
    """Find agencies by specific capability."""
    try:
        registry = get_registry()
        
        agencies = await registry.query_agencies(
            capabilities=[capability],
            active_only=True,
            limit=limit
        )
        
        results = []
        for agency in agencies:
            results.append({
                "agency_id": agency.agency_id,
                "name": agency.name,
                "description": agency.description,
                "endpoint": str(agency.endpoint),
                "all_capabilities": agency.capabilities
            })
        
        return ToolResult(
            output=results,
            metadata={
                "capability": capability,
                "count": len(results)
            }
        )
    except Exception as e:
        logger.error(f"Error finding agencies by capability: {e}")
        raise


# FastAPI routes
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test MongoDB connection
        registry = get_registry()
        stats = await registry.get_statistics()
        return {
            "status": "healthy",
            "agency": "Registry Search Agency",
            "total_agencies": stats.get("total_agencies", 0),
            "active_agencies": stats.get("active_agencies", 0)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@app.get("/info")
async def get_info():
    """Get agency information."""
    return {
        "name": "Registry Search Agency",
        "description": "Searches for utility agencies in the IATP registry",
        "capabilities": [
            "search_utility_agencies",
            "get_agency_by_id",
            "get_registry_statistics",
            "find_agencies_by_capability"
        ],
        "type": "special_agency",
        "version": "1.0.0"
    }


@app.post("/a2a")
async def a2a_endpoint(request: dict):
    """Handle A2A protocol requests."""
    try:
        # Process the A2A request
        action = request.get("action")
        parameters = request.get("parameters", {})
        context = request.get("context", {})
        
        # Map action to tool
        tool_mapping = {
            "search_utility_agencies": search_utility_agencies,
            "get_agency_by_id": get_agency_by_id,
            "get_registry_statistics": get_registry_statistics,
            "find_agencies_by_capability": find_agencies_by_capability
        }
        
        if action not in tool_mapping:
            raise HTTPException(status_code=400, detail=f"Unknown action: {action}")
        
        # Execute the tool
        tool_func = tool_mapping[action]
        result = await tool_func(**parameters)
        
        return {
            "result": result.output,
            "status": "success",
            "metadata": result.metadata
        }
        
    except Exception as e:
        logger.error(f"A2A request error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    global _registry
    if _registry:
        _registry.close()
        _registry = None


def create_registry_search_agency_structure(output_dir: str = "special_agencies") -> str:
    """Create the folder structure for the registry search agency."""
    from pathlib import Path
    
    agency_path = Path(output_dir) / "registry_search_agency"
    agency_path.mkdir(parents=True, exist_ok=True)
    
    # Create Dockerfile
    dockerfile_content = """FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agency files
COPY . .

# Expose port
EXPOSE 8000

# Run the server
CMD ["python", "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    
    with open(agency_path / "Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    # Create requirements.txt
    requirements = """fastapi>=0.100.0
uvicorn>=0.20.0
a2a>=0.1.0
pymongo>=4.0.0
python-dotenv>=1.0.0
"""
    
    with open(agency_path / "requirements.txt", "w") as f:
        f.write(requirements)
    
    # Copy this file as server.py
    import shutil
    shutil.copy(__file__, agency_path / "server.py")
    
    # Create README.md
    readme_content = """# Registry Search Utility Agency

A special utility agency that provides search capabilities for finding other utility agencies in the IATP registry.

## Features
- Search agencies by text query
- Filter by tags and capabilities
- Get detailed agency information
- View registry statistics

## Environment Variables
- `MONGODB_URI`: MongoDB connection string (required)

## Running the Agency

### Using Docker
```bash
docker build -t registry-search-agency .
docker run -p 8000:8000 -e MONGODB_URI="your-mongodb-uri" registry-search-agency
```

### Without Docker
```bash
export MONGODB_URI="your-mongodb-uri"
pip install -r requirements.txt
python -m uvicorn server:app --host 0.0.0.0 --port 8000
```

## A2A Tools Available
- `search_utility_agencies`: Search for agencies
- `get_agency_by_id`: Get specific agency details
- `get_registry_statistics`: Get registry stats
- `find_agencies_by_capability`: Find agencies by capability

## Usage Example

```python
from traia_iatp import create_utility_agency_tools

# This agency will be discoverable like any other
tools = create_utility_agency_tools(
    query="registry search"
)

# Use the tool to find other agencies
result = tools[0]._run(
    action="search_utility_agencies",
    parameters={"query": "data processing", "limit": 5}
)
```
"""
    
    with open(agency_path / "README.md", "w") as f:
        f.write(readme_content)
    
    # Create .env.example
    env_example = """# MongoDB connection string (required)
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/iatp
"""
    
    with open(agency_path / ".env.example", "w") as f:
        f.write(env_example)
    
    logger.info(f"Created registry search agency structure at: {agency_path}")
    return str(agency_path)


if __name__ == "__main__":
    # Running directly - start the server
    uvicorn.run(app, host="0.0.0.0", port=8000) 