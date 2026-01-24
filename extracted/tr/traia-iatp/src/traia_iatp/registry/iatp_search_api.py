#!/usr/bin/env python
"""
IATP Search API

This module provides high-level search API functions for finding MCP servers and utility agents
in the IATP registry using text search, Atlas Search, and vector search capabilities.
"""

import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import os
import logging

from pymongo import MongoClient
from pymongo import server_api

# Get environment variables
CLUSTER_URI = "traia-iatp-cluster.yzwjvgd.mongodb.net/?retryWrites=true&w=majority&appName=Traia-IATP-Cluster"
DATABASE_NAME = "iatp"

logger = logging.getLogger(__name__)

# Projection to exclude large embedding fields from query responses
# These fields are used internally for vector search but not needed by clients
MCP_PROJECTION_EXCLUDE_EMBEDDINGS = {
    "description_embedding": 0,
    "capabilities_embedding": 0
}

UTILITY_AGENT_PROJECTION_EXCLUDE_EMBEDDINGS = {
    "embeddings": 0  # Excludes embeddings.description, embeddings.agent_card, embeddings.search_text
}


@dataclass
class MCPServerInfo:
    """Information about an MCP server from the registry."""
    id: str
    name: str
    url: str
    description: str
    server_type: str
    capabilities: List[str]
    metadata: Dict[str, Any]
    tags: List[str]
    is_active: bool = False
    core_tests_passed: bool = False
    crewai_tests_passed: bool = False
    user_uuid: Optional[str] = None
    # Blockchain fields (from PostgreSQL, synced to MongoDB)
    operator_address: Optional[str] = None
    server_address: Optional[str] = None
    server_network: Optional[str] = None
    server_chain_id: Optional[int] = None
    # Token acceptance information
    accepts: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_registry_doc(cls, doc: Dict[str, Any]) -> 'MCPServerInfo':
        """Create MCPServerInfo from MongoDB document.
        
        Note: Embedding fields (description_embedding, capabilities_embedding) 
        should be excluded from queries via projection - they are not needed by clients.
        """
        # Extract tags from metadata if present
        metadata = doc.get('metadata', {})
        tags = metadata.get('tags', [])
        
        return cls(
            id=str(doc.get('_id', '')),
            name=doc.get('name', ''),
            url=doc.get('url', ''),
            description=doc.get('description', ''),
            server_type=doc.get('server_type', 'streamable-http'),
            capabilities=doc.get('capabilities', []),
            metadata=metadata,
            tags=tags,
            is_active=doc.get('is_active', False),
            core_tests_passed=doc.get('core_tests_passed', False),
            crewai_tests_passed=doc.get('crewai_tests_passed', False),
            user_uuid=doc.get('user_uuid'),
            # Blockchain fields
            operator_address=doc.get('operator_address'),
            server_address=doc.get('server_address'),
            server_network=doc.get('server_network'),
            server_chain_id=doc.get('server_chain_id'),
            # Token acceptance
            accepts=doc.get('accepts')
        )


@dataclass 
class UtilityAgentInfo:
    """Information about a utility agent from the registry."""
    agent_id: str
    name: str
    description: str
    base_url: str
    capabilities: List[str]
    tags: List[str]
    is_active: bool
    metadata: Dict[str, Any]
    skills: List[Dict[str, Any]]
    endpoints: Optional[Dict[str, Any]] = None
    # D402 payment fields
    d402_enabled: bool = False
    d402_payment_info: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_registry_doc(cls, doc: Dict[str, Any]) -> 'UtilityAgentInfo':
        """Create UtilityAgentInfo from MongoDB document.
        
        Note: The "embeddings" object (containing embeddings.description, 
        embeddings.agent_card, embeddings.search_text) should be excluded from 
        queries via projection - they are not needed by clients.
        """
        return cls(
            agent_id=doc.get('agent_id', ''),
            name=doc.get('name', ''),
            description=doc.get('description', ''),
            base_url=doc.get('base_url', ''),
            capabilities=doc.get('capabilities', []),
            tags=doc.get('tags', []),
            is_active=doc.get('is_active', True),
            metadata=doc.get('metadata', {}),
            skills=doc.get('skills', []),
            endpoints=doc.get('endpoints'),  # Get endpoints from root level
            d402_enabled=doc.get('d402_enabled', False),
            d402_payment_info=doc.get('d402_payment_info')
        )


# Bundled read-only X.509 certificate for public registry access
# This certificate has ONLY read access to the registry collections
# No write, update, or delete permissions - safe to bundle in package
def _get_bundled_cert_path() -> str:
    """Get path to the bundled read-only X.509 certificate."""
    import pathlib
    # Certificate is bundled in the traia_iatp package root
    package_dir = pathlib.Path(__file__).parent.parent
    cert_path = package_dir / "X509-cert-2235240396129682827.pem"
    return str(cert_path)


def get_readonly_connection_string() -> str:
    """Get read-only MongoDB connection string.
    
    Authentication priority:
    1. IAM access (for AWS deployments)
    2. User-provided X.509 certificate
    3. User-provided credentials (MONGODB_USER/PASSWORD)
    4. User-provided connection string
    5. BUNDLED read-only X.509 certificate (default - no setup required!)
    
    The bundled X.509 certificate allows anyone using the IATP package
    to discover and search MCP servers and utility agents without any
    configuration. The certificate has read-only access to the registry.
    """

    # Try IAM access (for AWS Lambda, ECS, etc.)
    cluster_host_name = os.environ.get('CLUSTER_HOST_NAME', None)
    if cluster_host_name:
        logger.debug("Using IAM authentication for MongoDB")
        return f"mongodb+srv://{cluster_host_name}/?authMechanism=MONGODB-AWS&authSource=%24external&retryWrites=true&w=majority&appName=Traia-IATP-Cluster"

    # Try user-provided X.509 certificate (for custom access)
    cert_file = os.getenv("MONGODB_X509_CERT_FILE")
    if cert_file and os.path.exists(cert_file):
        logger.debug("Using user-provided X.509 certificate for MongoDB")
        cluster_host = CLUSTER_URI.split('?')[0]
        return f"mongodb+srv://{cluster_host}?authSource=$external&authMechanism=MONGODB-X509&tls=true&tlsCertificateKeyFile={cert_file}"
    
    # Try user-provided credentials
    user = os.getenv("MONGODB_USER")
    password = os.getenv("MONGODB_PASSWORD")
    if user and password:
        logger.debug("Using user-provided credentials for MongoDB")
        return f"mongodb+srv://{user}:{password}@{CLUSTER_URI}"
    
    # Try user-provided connection string
    conn_str = os.getenv("MONGODB_CONNECTION_STRING")
    if conn_str:
        logger.debug("Using user-provided connection string for MongoDB")
        return conn_str
    
    # Default: Use bundled read-only X.509 certificate (no setup required!)
    # This allows anyone to discover MCP servers and utility agents
    bundled_cert = _get_bundled_cert_path()
    if os.path.exists(bundled_cert):
        logger.debug("Using bundled read-only X.509 certificate for MongoDB registry access")
        cluster_host = CLUSTER_URI.split('?')[0]
        return f"mongodb+srv://{cluster_host}?authSource=$external&authMechanism=MONGODB-X509&tls=true&tlsCertificateKeyFile={bundled_cert}"
    
    raise ValueError(
        "MongoDB authentication required. The bundled certificate was not found.\n"
        "Please reinstall the package or provide credentials via:\n"
        "  MONGODB_X509_CERT_FILE, MONGODB_USER/PASSWORD, or MONGODB_CONNECTION_STRING"
    )


def get_collection_names():
    """Get environment-specific collection names.
    
    Collections:
    - test: iatp-mcp-server-registry-test, iatp-utility-agent-registry-test
    - prod: PROD-iatp-mcp-server-registry, PROD-utility-agent-registry
    """
    env = os.getenv("ENV", "test").lower()
    
    # Validate environment
    valid_envs = ["test", "prod"]
    if env not in valid_envs:
        logger.warning(f"Invalid ENV '{env}', defaulting to 'test'. Valid values: {valid_envs}")
        env = "test"
    
    if env == "prod":
        return {
            "utility_agent": "PROD-utility-agent-registry",
            "mcp_server": "PROD-iatp-mcp-server-registry"
        }
    else:
        # test environment (default)
        return {
            "utility_agent": "iatp-utility-agent-registry-test",
            "mcp_server": "iatp-mcp-server-registry-test"
        }


class IATPSearchAPI:
    """
    Search API for finding MCP servers and utility agents in the IATP registry.
    Provides text search, Atlas Search, and vector search capabilities.
    """
    
    # Class variable to cache readonly connections
    _client = None
    _db = None
    
    @classmethod
    def _get_connection(cls):
        """Get or create read-only MongoDB connection."""
        if cls._client is None:
            conn_str = get_readonly_connection_string()
            cls._client = MongoClient(conn_str, server_api=server_api.ServerApi('1'))
            cls._db = cls._client[DATABASE_NAME]
        return cls._db
    
    @classmethod
    def find_utility_agent(
        cls,
        name: Optional[str] = None,
        agent_id: Optional[str] = None,
        capability: Optional[str] = None,
        tag: Optional[str] = None,
        query: Optional[str] = None
    ) -> Optional[UtilityAgentInfo]:
        """
        Find a utility agent in the registry.
        
        Args:
            name: Exact name of the agent
            agent_id: Exact agent_id of the agent
            capability: Find agents with this capability
            tag: Find agents with this tag
            query: Text search query (uses Atlas Search)
            
        Returns:
            UtilityAgentInfo if found, None otherwise
        """
        db = cls._get_connection()
        collection_names = get_collection_names()
        collection = db[collection_names["utility_agent"]]
        
        if agent_id:
            # Direct lookup by agent_id (exclude embeddings for performance)
            doc = collection.find_one(
                {"agent_id": agent_id, "is_active": True},
                UTILITY_AGENT_PROJECTION_EXCLUDE_EMBEDDINGS
            )
            if doc:
                return UtilityAgentInfo.from_registry_doc(doc)
        
        if name:
            # Direct lookup by name (exclude embeddings for performance)
            doc = collection.find_one(
                {"name": name, "is_active": True},
                UTILITY_AGENT_PROJECTION_EXCLUDE_EMBEDDINGS
            )
            if doc:
                return UtilityAgentInfo.from_registry_doc(doc)
        
        # If query is provided, use Atlas Search
        if query:
            env = os.getenv("ENV", "test").lower()
            atlas_index_name = f"utility_agent_atlas_search_{env}"
            
            pipeline = [
                {
                    "$search": {
                        "index": atlas_index_name,
                        "text": {
                            "query": query,
                            "path": ["name", "description", "tags", "capabilities", "skills.name", "skills.description", "skills.tags"]
                        }
                    }
                },
                {"$match": {"is_active": True}},
            ]
            
            # Add additional filters if provided
            match_filters = {}
            if capability:
                match_filters["capabilities"] = capability
            if tag:
                match_filters["tags"] = tag
            
            if match_filters:
                pipeline.append({"$match": match_filters})
            
            pipeline.append({"$limit": 1})
            
            results = list(collection.aggregate(pipeline))
            if results:
                return UtilityAgentInfo.from_registry_doc(results[0])
        else:
            # Build standard query filters
            filters = {"is_active": True}
            
            if capability:
                filters["capabilities"] = capability
            
            if tag:
                filters["tags"] = tag
            
            # Find first matching document (exclude embeddings for performance)
            doc = collection.find_one(filters, UTILITY_AGENT_PROJECTION_EXCLUDE_EMBEDDINGS)
            if doc:
                return UtilityAgentInfo.from_registry_doc(doc)
        
        return None
    
    @classmethod
    def list_utility_agents(
        cls,
        limit: int = 10,
        tags: Optional[List[str]] = None,
        capabilities: Optional[List[str]] = None,
        active_only: bool = True
    ) -> List[UtilityAgentInfo]:
        """
        List available utility agents from the registry.
        
        Args:
            limit: Maximum number of agents to return
            tags: Filter by tags
            capabilities: Filter by capabilities
            active_only: Only return active agents
            
        Returns:
            List of UtilityAgentInfo objects
        """
        db = cls._get_connection()
        collection_names = get_collection_names()
        collection = db[collection_names["utility_agent"]]
        
        # Build query filters
        filters = {}
        if active_only:
            filters["is_active"] = True
        if tags:
            filters["tags"] = {"$in": tags}
        if capabilities:
            filters["capabilities"] = {"$in": capabilities}
        
        # Query with limit (exclude embeddings for performance)
        cursor = collection.find(
            filters,
            UTILITY_AGENT_PROJECTION_EXCLUDE_EMBEDDINGS
        ).limit(limit).sort("registered_at", -1)
        
        return [UtilityAgentInfo.from_registry_doc(doc) for doc in cursor]
    
    @classmethod
    async def search_utility_agents(
        cls,
        query: str,
        limit: int = 10,
        active_only: bool = True,
        embedding_fields: Optional[List[str]] = None
    ) -> List[UtilityAgentInfo]:
        """
        Search utility agents using vector search.
        
        Args:
            query: Search query
            limit: Maximum number of results
            active_only: Only return active agents
            embedding_fields: Specific embedding fields to search on. If None, uses only search_text.
                            Options: ["description", "tags", "capabilities", "agent_card"]
            
        Returns:
            List of UtilityAgentInfo objects
        """
        # Generate query embedding (lazy import to avoid loading OpenAI/Cohere unless needed)
        try:
            from .embeddings import get_embedding_service
            embedding_service = get_embedding_service()
            query_embedding = await embedding_service.generate_query_embedding(query)
        except Exception as e:
            logger.error(f"Failed to generate query embedding: {e}")
            # Fallback to Atlas text search
            return await cls._fallback_atlas_search_agents(query, limit, active_only)
        
        db = cls._get_connection()
        collection_names = get_collection_names()
        collection = db[collection_names["utility_agent"]]
        
        env = os.getenv("ENV", "test").lower()
        vector_index_name = f"utility_agent_vector_search_{env}"
        
        # Default to search_text only, or use specified fields
        if embedding_fields is None:
            fields_to_search = ["embeddings.search_text"]
        else:
            # Map field names to embedding paths
            field_mapping = {
                "description": "embeddings.description",
                "tags": "embeddings.tags",
                "capabilities": "embeddings.capabilities",
                "agent_card": "embeddings.agent_card"
            }
            fields_to_search = [field_mapping.get(f, f"embeddings.{f}") for f in embedding_fields]
        
        # If only one field, do a simple search
        if len(fields_to_search) == 1:
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": vector_index_name,
                        "path": fields_to_search[0],
                        "queryVector": query_embedding,
                        "numCandidates": limit * 5,
                        "limit": limit,
                        "filter": {"is_active": True} if active_only else {}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "agent_id": 1,
                        "name": 1,
                        "description": 1,
                        "base_url": 1,
                        "capabilities": 1,
                        "tags": 1,
                        "is_active": 1,
                        "metadata": 1,
                        "skills": 1,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ]
            
            results = list(collection.aggregate(pipeline))
            return [UtilityAgentInfo.from_registry_doc(doc) for doc in results]
        
        # Multiple fields - aggregate results
        all_results = []
        seen_ids = set()
        
        for field in fields_to_search:
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": vector_index_name,
                        "path": field,
                        "queryVector": query_embedding,
                        "numCandidates": limit * 5,
                        "limit": limit,
                        "filter": {"is_active": True} if active_only else {}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "agent_id": 1,
                        "name": 1,
                        "description": 1,
                        "base_url": 1,
                        "capabilities": 1,
                        "tags": 1,
                        "is_active": 1,
                        "metadata": 1,
                        "skills": 1,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ]
            
            results = list(collection.aggregate(pipeline))
            
            # Add results avoiding duplicates
            for doc in results:
                if doc.get("agent_id") not in seen_ids:
                    seen_ids.add(doc.get("agent_id"))
                    all_results.append(doc)
        
        # Sort by score (highest first) and limit
        all_results.sort(key=lambda x: x.get("score", 0), reverse=True)
        all_results = all_results[:limit]
        
        # Convert to UtilityAgentInfo objects
        return [UtilityAgentInfo.from_registry_doc(doc) for doc in all_results]
    
    @classmethod
    async def _fallback_atlas_search_agents(
        cls,
        query: str,
        limit: int,
        active_only: bool
    ) -> List[UtilityAgentInfo]:
        """Fallback to Atlas text search if vector search fails."""
        db = cls._get_connection()
        collection_names = get_collection_names()
        collection = db[collection_names["utility_agent"]]
        
        env = os.getenv("ENV", "test").lower()
        atlas_index_name = f"utility_agent_atlas_search_{env}"
        
        pipeline = [
            {
                "$search": {
                    "index": atlas_index_name,
                    "text": {
                        "query": query,
                        "path": ["name", "description", "tags", "capabilities", "skills.name", "skills.description", "skills.tags"]
                    }
                }
            }
        ]
        
        if active_only:
            pipeline.append({"$match": {"is_active": True}})
        
        pipeline.append({"$limit": limit})
        
        results = list(collection.aggregate(pipeline))
        return [UtilityAgentInfo.from_registry_doc(doc) for doc in results]
    
    @classmethod
    def find_mcp_server(
        cls,
        name: Optional[str] = None,
        capability: Optional[str] = None,
        tag: Optional[str] = None,
        query: Optional[str] = None
    ) -> Optional[MCPServerInfo]:
        """
        Find an MCP server in the registry.
        
        Args:
            name: Exact name of the MCP server
            capability: Find servers with this capability
            tag: Find servers with this tag
            query: Text search query (uses Atlas Search)
            
        Returns:
            MCPServerInfo if found, None otherwise
        """
        db = cls._get_connection()
        collection_names = get_collection_names()
        collection = db[collection_names["mcp_server"]]
        
        if name:
            # Direct lookup by name
            doc = collection.find_one({"name": name, "is_active": True, "core_tests_passed": True})
            if doc:
                return MCPServerInfo.from_registry_doc(doc)
        
        # If query is provided, use Atlas Search
        if query:
            env = os.getenv("ENV", "test").lower()
            atlas_index_name = f"mcp_server_atlas_search_{env}"
            
            pipeline = [
                {
                    "$search": {
                        "index": atlas_index_name,
                        "text": {
                            "query": query,
                            "path": ["name", "description", "capabilities"]
                        }
                    }
                },
                {"$match": {"is_active": True, "core_tests_passed": True}},
            ]
            
            # Add additional filters if provided
            match_filters = {}
            if capability:
                match_filters["capabilities"] = capability
            if tag:
                # Tags are stored in metadata
                match_filters["metadata.tags"] = tag
            
            if match_filters:
                pipeline.append({"$match": match_filters})
            
            # Exclude embedding fields from results
            pipeline.append({"$project": MCP_PROJECTION_EXCLUDE_EMBEDDINGS})
            pipeline.append({"$limit": 1})
            
            results = list(collection.aggregate(pipeline))
            if results:
                return MCPServerInfo.from_registry_doc(results[0])
        else:
            # Build standard query filters
            filters = {"is_active": True, "core_tests_passed": True}
            
            if capability:
                filters["capabilities"] = capability
            
            if tag:
                # Tags are stored in metadata
                filters["metadata.tags"] = tag
            
            # Find first matching document (exclude embeddings for performance)
            doc = collection.find_one(filters, MCP_PROJECTION_EXCLUDE_EMBEDDINGS)
            if doc:
                return MCPServerInfo.from_registry_doc(doc)
        
        return None
    
    @classmethod
    def list_mcp_servers(
        cls,
        limit: int = 10,
        page: int = 1,
        tags: Optional[List[str]] = None,
        capabilities: Optional[List[str]] = None,
        user_uuid: Optional[str] = None
    ) -> List[MCPServerInfo]:
        """
        List available MCP servers from the registry.
        
        Args:
            limit: Maximum number of servers to return (default: 10)
            page: Page number for pagination, 1-indexed (default: 1)
            tags: Filter by tags
            capabilities: Filter by capabilities
            user_uuid: Filter by user UUID
            
        Returns:
            List of MCPServerInfo objects
            
        Examples:
            list_mcp_servers(limit=10, page=1)  # First 10 servers
            list_mcp_servers(limit=10, page=2)  # Next 10 servers
        """
        if page < 1:
            page = 1
        
        skip = (page - 1) * limit
        logger.info(f"list_mcp_servers: limit={limit}, page={page}, tags={tags}, capabilities={capabilities}, user_uuid={user_uuid}")
        
        db = cls._get_connection()
        collection_names = get_collection_names()
        collection = db[collection_names["mcp_server"]]
        
        logger.info(f"Using collection: {collection_names['mcp_server']}")
        
        # Build query filters
        filters = {"is_active": True, "core_tests_passed": True}
        if capabilities:
            filters["capabilities"] = {"$in": capabilities}
        if user_uuid:
            filters["user_uuid"] = user_uuid
        
        logger.info(f"Query filters: {filters}")
        
        # Count and log total
        total_count = collection.count_documents(filters)
        logger.info(f"Total documents matching filters: {total_count}")
        
        # Query with pagination (exclude embeddings for performance)
        cursor = collection.find(
            filters, 
            MCP_PROJECTION_EXCLUDE_EMBEDDINGS
        ).skip(skip).limit(limit).sort("registered_at", -1)
        
        # Manual filtering for tags if needed
        servers = []
        for doc in cursor:
            if tags:
                doc_tags = doc.get("metadata", {}).get("tags", [])
                if not any(tag in doc_tags for tag in tags):
                    continue
            
            servers.append(MCPServerInfo.from_registry_doc(doc))
        
        logger.info(f"Returning {len(servers)} servers")
        return servers
    
    @classmethod
    def get_mcp_server(cls, name: str) -> Optional[Dict[str, Any]]:
        """
        Get an MCP server by name (returns raw document).
        
        Args:
            name: Name of the MCP server
            
        Returns:
            MongoDB document if found, None otherwise
        """
        db = cls._get_connection()
        collection_names = get_collection_names()
        collection = db[collection_names["mcp_server"]]
        
        # Exclude embeddings from response (not needed by clients)
        doc = collection.find_one({"name": name}, MCP_PROJECTION_EXCLUDE_EMBEDDINGS)
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc
    
    @classmethod
    def close_connections(cls):
        """Close all registry connections."""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None

    @classmethod
    async def search_mcp_servers(
        cls,
        query: str,
        limit: int = 10,
        active_only: bool = True,
        embedding_fields: Optional[List[str]] = None
    ) -> List[MCPServerInfo]:
        """
        Search MCP servers using vector search.
        
        Args:
            query: Search query
            limit: Maximum number of results
            active_only: Only return active servers
            embedding_fields: Specific embedding fields to search on. If None, searches both description and capabilities.
                            Options: ["description", "capabilities"]
            
        Returns:
            List of MCPServerInfo objects
        """
        # Generate query embedding (lazy import to avoid loading OpenAI/Cohere unless needed)
        try:
            from .embeddings import get_embedding_service
            embedding_service = get_embedding_service()
            query_embedding = await embedding_service.generate_query_embedding(query)
        except Exception as e:
            logger.error(f"Failed to generate query embedding: {e}")
            # Fallback to Atlas text search
            return await cls._fallback_atlas_search_mcp_servers(query, limit, active_only)
        
        db = cls._get_connection()
        collection_names = get_collection_names()
        collection = db[collection_names["mcp_server"]]
        
        env = os.getenv("ENV", "test").lower()
        vector_index_name = f"mcp_server_vector_search_{env}"
        
        # Default to both fields, or use specified fields
        if embedding_fields is None:
            fields_to_search = ["description_embedding", "capabilities_embedding"]
        else:
            # Map field names to embedding paths
            field_mapping = {
                "description": "description_embedding",
                "capabilities": "capabilities_embedding"
            }
            fields_to_search = [field_mapping.get(f, f"{f}_embedding") for f in embedding_fields]
        
        # If only one field, do a simple search
        if len(fields_to_search) == 1:
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": vector_index_name,
                        "path": fields_to_search[0],
                        "queryVector": query_embedding,
                        "numCandidates": limit * 5,
                        "limit": limit,
                        "filter": {"is_active": True, "core_tests_passed": True} if active_only else {"core_tests_passed": True}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "name": 1,
                        "url": 1,
                        "description": 1,
                        "server_type": 1,
                        "capabilities": 1,
                        "metadata": 1,
                        "registered_at": 1,
                        "is_active": 1,
                        "core_tests_passed": 1,
                        "crewai_tests_passed": 1,
                        "user_uuid": 1,
                        "operator_address": 1,
                        "server_address": 1,
                        "server_network": 1,
                        "server_chain_id": 1,
                        "accepts": 1,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ]
            
            results = list(collection.aggregate(pipeline))
            return [MCPServerInfo.from_registry_doc(doc) for doc in results]
        
        # Multiple fields - aggregate results
        all_results = []
        seen_names = set()
        
        for field in fields_to_search:
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": vector_index_name,
                        "path": field,
                        "queryVector": query_embedding,
                        "numCandidates": limit * 5,
                        "limit": limit,
                        "filter": {"is_active": True, "core_tests_passed": True} if active_only else {"core_tests_passed": True}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "name": 1,
                        "url": 1,
                        "description": 1,
                        "server_type": 1,
                        "capabilities": 1,
                        "metadata": 1,
                        "registered_at": 1,
                        "is_active": 1,
                        "core_tests_passed": 1,
                        "crewai_tests_passed": 1,
                        "user_uuid": 1,
                        "operator_address": 1,
                        "server_address": 1,
                        "server_network": 1,
                        "server_chain_id": 1,
                        "accepts": 1,
                        "score": {"$meta": "vectorSearchScore"}
                    }
                }
            ]
            
            results = list(collection.aggregate(pipeline))
            
            # Add results avoiding duplicates
            for doc in results:
                if doc.get("name") not in seen_names:
                    seen_names.add(doc.get("name"))
                    all_results.append(doc)
        
        # Sort by score (highest first) and limit
        all_results.sort(key=lambda x: x.get("score", 0), reverse=True)
        all_results = all_results[:limit]
        
        # Convert to MCPServerInfo objects
        return [MCPServerInfo.from_registry_doc(doc) for doc in all_results]
    
    @classmethod
    async def _fallback_atlas_search_mcp_servers(
        cls,
        query: str,
        limit: int,
        active_only: bool
    ) -> List[MCPServerInfo]:
        """Fallback to Atlas text search if vector search fails."""
        db = cls._get_connection()
        collection_names = get_collection_names()
        collection = db[collection_names["mcp_server"]]
        
        env = os.getenv("ENV", "test").lower()
        atlas_index_name = f"mcp_server_atlas_search_{env}"
        
        pipeline = [
            {
                "$search": {
                    "index": atlas_index_name,
                    "text": {
                        "query": query,
                        "path": ["name", "description", "capabilities"]
                    }
                }
            }
        ]
        
        if active_only:
            pipeline.append({"$match": {"is_active": True, "core_tests_passed": True}})
        else:
            pipeline.append({"$match": {"core_tests_passed": True}})
        
        pipeline.append({"$limit": limit})
        
        results = list(collection.aggregate(pipeline))
        return [MCPServerInfo.from_registry_doc(doc) for doc in results]


# Keep backward compatibility - use IATPSearchAPI
class RegistryAPI(IATPSearchAPI):
    """Backward compatibility alias for IATPSearchAPI."""
    pass


# Convenience functions that don't require class instantiation
def find_utility_agent(
    name: Optional[str] = None,
    agent_id: Optional[str] = None,
    capability: Optional[str] = None,
    tag: Optional[str] = None,
    query: Optional[str] = None
) -> Optional[UtilityAgentInfo]:
    """Find a utility agent in the registry."""
    return IATPSearchAPI.find_utility_agent(name, agent_id, capability, tag, query)


def list_utility_agents(
    limit: int = 10,
    tags: Optional[List[str]] = None,
    capabilities: Optional[List[str]] = None,
    active_only: bool = True
) -> List[UtilityAgentInfo]:
    """List available utility agents from the registry."""
    return IATPSearchAPI.list_utility_agents(limit, tags, capabilities, active_only)


async def search_utility_agents(
    query: str,
    limit: int = 10,
    active_only: bool = True,
    embedding_fields: Optional[List[str]] = None
) -> List[UtilityAgentInfo]:
    """Search utility agents using vector search."""
    return await IATPSearchAPI.search_utility_agents(query, limit, active_only, embedding_fields)


def find_mcp_server(
    name: Optional[str] = None,
    capability: Optional[str] = None,
    tag: Optional[str] = None,
    query: Optional[str] = None
) -> Optional[MCPServerInfo]:
    """Find an MCP server in the registry."""
    return IATPSearchAPI.find_mcp_server(name, capability, tag, query)


def list_mcp_servers(
    limit: int = 10,
    page: int = 1,
    tags: Optional[List[str]] = None,
    capabilities: Optional[List[str]] = None,
    user_uuid: Optional[str] = None
) -> List[MCPServerInfo]:
    """
    List available MCP servers from the registry.
    
    Args:
        limit: Maximum number of servers to return (default: 10)
        page: Page number for pagination, 1-indexed (default: 1)
        tags: Filter by tags
        capabilities: Filter by capabilities
        user_uuid: Filter by user UUID
        
    Returns:
        List of MCPServerInfo objects
        
    Examples:
        servers = list_mcp_servers(limit=10, page=1)  # First page
        servers = list_mcp_servers(limit=10, page=2)  # Second page
    """
    return IATPSearchAPI.list_mcp_servers(limit, page, tags, capabilities, user_uuid)


async def search_mcp_servers(
    query: str,
    limit: int = 10,
    embedding_fields: Optional[List[str]] = None
) -> List[MCPServerInfo]:
    """
    Search MCP servers using vector search.
    
    Args:
        query: Search query
        limit: Maximum number of results
        embedding_fields: Specific embedding fields to search on. If None, searches both description and capabilities.
                        Options: ["description", "capabilities"]
        
    Returns:
        List of MCPServerInfo objects
    """
    return await IATPSearchAPI.search_mcp_servers(query, limit, active_only=True, embedding_fields=embedding_fields)


def get_mcp_server(name: str) -> Optional[Dict[str, Any]]:
    """Get an MCP server by name (returns raw document)."""
    return IATPSearchAPI.get_mcp_server(name) 