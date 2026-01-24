#!/usr/bin/env python
"""
D402 MCP Tool Adapter

A simple adapter for using d402-enabled MCP servers with CrewAI.
This adapter avoids the complexity of persistent SSE connections and background tasks.

Instead, it:
1. Lists available tools from the MCP server
2. Creates CrewAI BaseTool wrappers for each MCP tool
3. Each tool uses httpx with d402 payment hooks for requests
4. No persistent connections - simple request/response pattern

This is more reliable than MCPServerAdapter for d402 payment scenarios.
"""

import json
import logging
from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel, Field, create_model
from crewai.tools import BaseTool
import httpx

from traia_iatp.d402.clients.httpx import d402HttpxClient

logger = logging.getLogger(__name__)


def json_schema_to_pydantic_model(json_schema: Dict[str, Any], model_name: str = "ToolInput") -> type[BaseModel]:
    """
    Convert JSON schema to Pydantic BaseModel for CrewAI args_schema.
    
    CrewAI BaseTool expects args_schema to be a Pydantic BaseModel, not a Dict.
    Without this conversion, CrewAI cannot properly extract and validate tool arguments,
    causing arguments to be lost (empty dict sent to MCP server).
    
    Args:
        json_schema: JSON schema dictionary (OpenAPI format)
        model_name: Name for the generated Pydantic model
        
    Returns:
        Pydantic BaseModel class
    """
    if not json_schema or "properties" not in json_schema:
        # Return empty model if no schema
        return create_model(model_name, __base__=BaseModel)
    
    properties = json_schema.get("properties", {})
    required = json_schema.get("required", [])
    
    # Map JSON schema types to Python types
    type_mapping = {
        "string": str,
        "integer": int,
        "number": float,
        "boolean": bool,
        "array": list,
        "object": dict,
    }
    
    # Build field definitions
    field_definitions = {}
    for prop_name, prop_schema in properties.items():
        prop_type = prop_schema.get("type", "string")
        python_type = type_mapping.get(prop_type, str)
        
        # Get description for Field
        description = prop_schema.get("description", "")
        
        # Check if required
        is_required = prop_name in required
        
        # Create Field with description
        if is_required:
            field_definitions[prop_name] = (python_type, Field(description=description))
        else:
            # Optional field with default
            default_value = prop_schema.get("default", None)
            field_definitions[prop_name] = (Optional[python_type], Field(default=default_value, description=description))
    
    # Create Pydantic model
    if field_definitions:
        return create_model(model_name, **field_definitions)
    else:
        return create_model(model_name, __base__=BaseModel)


class D402MCPTool(BaseTool):
    """
    CrewAI tool wrapper for a single MCP tool with d402 payment support.
    
    Each instance represents one MCP tool and handles d402 payments automatically.
    """
    
    name: str = "mcp_tool"
    description: str = "MCP tool with d402 payment"
    mcp_server_url: str = ""  # Full MCP server URL (will be cleaned of trailing slash)
    mcp_tool_name: str = ""
    mcp_session_id: str = ""
    d402_operator_account: Optional[Any] = None  # Operator account (EOA) for signing
    d402_wallet_address: Optional[str] = None  # IATPWallet contract address
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    # Generic additional header support (e.g., X-Polymarket-Key for Polymarket).
    additional_headers: Optional[Dict[str, str]] = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self, **data):
        """Initialize with custom data."""
        super().__init__(**data)
        # Ensure args_schema is preserved if provided
        # BaseTool.__init__ might not preserve it properly, so set it explicitly
        if "args_schema" in data and data["args_schema"] is not None:
            self.args_schema = data["args_schema"]
    
    def _set_args_schema(self):
        """
        Override to prevent BaseTool from overriding our args_schema.
        
        If args_schema is already set (from input_schema conversion), keep it.
        Otherwise, let BaseTool infer it from _run signature.
        """
        # Only set args_schema if it's not already set (i.e., still the placeholder)
        from crewai.tools.base_tool import BaseTool as BaseToolClass
        if self.args_schema == BaseToolClass._ArgsSchemaPlaceholder:
            # Call parent to infer from _run signature
            super()._set_args_schema()
        # Otherwise, keep our custom args_schema from input_schema conversion
    
    def _run(self, **kwargs) -> Dict[str, Any]:
        """
        Synchronous wrapper that runs async _arun.
        
        This method receives arguments from CrewAI. If kwargs is empty, it means
        CrewAI didn't extract arguments properly from the LLM's tool call.
        
        IMPORTANT: This method signature must match what CrewAI expects.
        CrewAI will call this with keyword arguments based on args_schema.
        """
        # Debug: Log what arguments we received
        if not kwargs:
            logger.error(f"❌ D402MCPTool._run called with EMPTY kwargs for {self.name}")
            logger.error(f"   This means CrewAI/LLM didn't provide arguments!")
            logger.error(f"   args_schema: {self.args_schema}")
            if hasattr(self.args_schema, 'model_fields'):
                required_fields = [name for name, field in self.args_schema.model_fields.items() 
                                 if field.is_required()]
                logger.error(f"   Required fields: {required_fields}")
                logger.error(f"   All fields: {list(self.args_schema.model_fields.keys())}")
            logger.error(f"   Tool description: {self.description[:200]}...")
            # Don't fail here - let the MCP server validate and return proper error
        else:
            logger.info(f"✅ D402MCPTool._run called with kwargs: {kwargs}")
        
        import asyncio
        try:
            # Run the async method in a new event loop
            return asyncio.run(self._arun(**kwargs))
        except RuntimeError:
            # If we're already in an event loop, use run_until_complete
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self._arun(**kwargs))
    
    async def _arun(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the MCP tool with d402 payment support.
        
        This method:
        1. Creates d402HttpxClient with built-in payment handling
        2. Makes MCP tools/call request
        3. d402 hooks automatically handle any 402 responses
        4. Returns the result
        """
        
        # Remove trailing slash to avoid redirects
        mcp_url = self.mcp_server_url.rstrip('/')
        
        # Create d402HttpxClient with built-in payment hooks
        # This ensures the hooks have a reference to the client for retries
        async with d402HttpxClient(
            operator_account=self.d402_operator_account,
            wallet_address=self.d402_wallet_address,
            timeout=60.0,
            http2=False  # Disable HTTP/2 for compatibility
        ) as client:
            
            # Create MCP tools/call request
            # kwargs contains the actual arguments from CrewAI (e.g., {"q": "test"})
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": self.mcp_tool_name,
                    "arguments": kwargs  # Pass arguments directly from CrewAI
                }
            }
            
            try:
                # Build headers with session ID and optional additional headers
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                    "mcp-session-id": self.mcp_session_id
                }
                
                # Add additional headers (preferred)
                if self.additional_headers:
                    headers.update(self.additional_headers)
                
                # Make request - d402 hooks will handle any 402 responses automatically
                response = await client.post(
                    mcp_url,  # Use full URL without trailing slash
                    json=mcp_request,
                    headers=headers,
                    follow_redirects=False  # Don't follow redirects - causes issues
                )
                
                # Read response content
                content = await response.aread()
                content_str = content.decode() if content else ""
                
                # Parse SSE format if present
                if "data:" in content_str:
                    sse_lines = content_str.strip().split('\n')
                    for line in sse_lines:
                        if line.startswith("data:"):
                            content_str = line[5:].strip()
                            break
                
                # Parse JSON response
                response_data = json.loads(content_str)
                
                # Extract result
                if "result" in response_data:
                    result = response_data["result"]
                    # Return structured content if available, otherwise full result
                    if isinstance(result, dict) and "structuredContent" in result:
                        return result["structuredContent"].get("result", result)
                    return result
                elif "error" in response_data:
                    return {"error": response_data["error"]}
                else:
                    return response_data
                    
            except Exception as e:
                logger.error(f"Error calling MCP tool {self.mcp_tool_name}: {e}")
                return {"error": str(e)}


class D402MCPToolAdapter:
    """
    Adapter for using d402-enabled MCP servers with CrewAI.
    
    This adapter is simpler and more reliable than MCPServerAdapter for d402:
    - No persistent SSE connections
    - No background tasks
    - Direct request/response with d402 hooks
    
    Usage:
        ```python
        from eth_account import Account
        from traia_iatp.mcp import D402MCPToolAdapter
        
        account = Account.from_key("0x...")
        adapter = D402MCPToolAdapter(
            url="http://localhost:8000/mcp",
            account=account
        )
        
        with adapter as tools:
            agent = Agent(
                role="Analyst",
                goal="Analyze data",
                tools=tools
            )
        ```
    """
    
    def __init__(
        self,
        url: str,
        account: Any,  # Operator account (EOA) for signing
        wallet_address: str = None,  # IATPWallet contract address
        max_value: Optional[int] = None,
        additional_headers: Optional[Dict[str, str]] = None
    ):
        """
        Initialize the d402 MCP adapter.
        
        Args:
            url: MCP server URL (e.g., "http://localhost:8000/mcp")
            account: Operator account (EOA) with private key for signing payments
            wallet_address: IATPWallet contract address (if None, uses account.address for testing)
            max_value: Optional maximum payment value in base units
            additional_headers: Optional dictionary of extra headers to send to the MCP server
                               (e.g., {"X-Polymarket-Key": "<private_key>"}).
        """
        self.url = url
        self.account = account  # Operator EOA
        self.wallet_address = wallet_address or account.address  # IATPWallet or EOA for testing
        self.max_value = max_value
        self.additional_headers = additional_headers or {}
        self.tools: List[BaseTool] = []
        self.session_id: Optional[str] = None
    
    async def _initialize_session(self) -> str:
        """Initialize MCP session and return session ID."""
        # Remove trailing slash to avoid redirects
        mcp_url = self.url.rstrip('/')
        
        async with httpx.AsyncClient(timeout=30.0, http2=False) as client:
            init_request = {
                "jsonrpc": "2.0",
                "id": "init",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "d402-crewai-client", "version": "1.0"}
                }
            }
            
            # Build headers with optional additional headers
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
            
            # Add additional headers (preferred)
            if self.additional_headers:
                headers.update(self.additional_headers)
            
            response = await client.post(
                mcp_url,  # Use full URL without trailing slash
                json=init_request,
                headers=headers,
                follow_redirects=False  # Don't follow redirects - causes issues
            )
            
            session_id = response.headers.get("mcp-session-id")
            if not session_id:
                raise RuntimeError("Failed to establish MCP session")
            
            return session_id
    
    async def _list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from the MCP server."""
        # Remove trailing slash to avoid redirects
        mcp_url = self.url.rstrip('/')
        
        async with httpx.AsyncClient(timeout=30.0, http2=False) as client:
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }
            
            # Build headers with session ID and optional additional headers
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "mcp-session-id": self.session_id
            }
            
            # Add additional headers (preferred)
            if self.additional_headers:
                headers.update(self.additional_headers)
            
            response = await client.post(
                mcp_url,  # Use full URL without trailing slash
                json=mcp_request,
                headers=headers,
                follow_redirects=False  # Don't follow redirects - causes issues
            )
            
            # Read response content (SSE format)
            content = await response.aread()
            content_str = content.decode() if content else ""
            
            # Parse SSE format if present
            if "data:" in content_str:
                sse_lines = content_str.strip().split('\n')
                for line in sse_lines:
                    if line.startswith("data:"):
                        content_str = line[5:].strip()
                        break
            
            response_data = json.loads(content_str)
            
            if "result" in response_data and "tools" in response_data["result"]:
                return response_data["result"]["tools"]
            return []
    
    def __enter__(self) -> List[BaseTool]:
        """
        Enter context manager - set up session and create tool wrappers.
        
        Returns:
            List of CrewAI BaseTool objects for each MCP tool
        """
        import asyncio
        
        logger.info("="*80)
        logger.info("🚀 D402MCPToolAdapter.__enter__() starting...")
        logger.info("="*80)
        
        # Handle nested event loop scenario (e.g., when CrewAI already has an event loop running)
        logger.info("🔍 Step 1: Checking for existing event loop...")
        try:
            # Try to get existing event loop
            loop = asyncio.get_running_loop()
            logger.info(f"   ✅ Found existing event loop: {loop}")
            # We have a running loop - use nest_asyncio to allow nested asyncio.run()
            logger.info("   Attempting to apply nest_asyncio...")
            try:
                import nest_asyncio
                logger.info("   nest_asyncio imported successfully")
                nest_asyncio.apply()
                logger.info("   📡 Applied nest_asyncio for nested event loop support")
            except ImportError as e:
                logger.warning(f"   ⚠️  nest_asyncio not available: {e}")
                logger.warning("   This WILL cause hanging with nested event loops")
        except RuntimeError as e:
            # No event loop running - asyncio.run() will work fine
            logger.info(f"   ✅ No existing event loop detected (RuntimeError: {e})")
            logger.info("   asyncio.run() will work without nest_asyncio")
        
        # Initialize session
        logger.info("")
        logger.info("🔍 Step 2: Initializing MCP session...")
        logger.info(f"   URL: {self.url}")
        logger.info("   About to call: asyncio.run(self._initialize_session())")
        try:
            self.session_id = asyncio.run(self._initialize_session())
            logger.info(f"   ✅ Session established: {self.session_id}")
        except Exception as e:
            logger.error(f"   ❌ Session initialization failed: {e}")
            raise
        
        # List available tools
        logger.info("")
        logger.info("🔍 Step 3: Listing available tools...")
        logger.info("   About to call: asyncio.run(self._list_tools())")
        try:
            mcp_tools = asyncio.run(self._list_tools())
            logger.info(f"   ✅ Found {len(mcp_tools)} tools")
        except Exception as e:
            logger.error(f"   ❌ Tool listing failed: {e}")
            raise
        
        logger.info("")
        logger.info("🔍 Step 4: Creating CrewAI tool wrappers...")
        logger.info(f"   Creating wrappers for {len(mcp_tools)} tools...")
        
        # Create CrewAI tool wrappers for each MCP tool
        self.tools = []
        for mcp_tool in mcp_tools:
            tool_name = mcp_tool.get("name", "unknown")
            tool_description = mcp_tool.get("description", f"MCP tool: {tool_name}")
            input_schema = mcp_tool.get("inputSchema", {})
            
            # Convert JSON schema to Pydantic model for CrewAI args_schema
            # This is critical: CrewAI BaseTool expects args_schema to be a Pydantic BaseModel,
            # not a Dict. Without this conversion, CrewAI cannot properly extract arguments,
            # causing arguments to be lost (empty dict sent to MCP server).
            model_name = f"{tool_name}Input"
            args_schema = json_schema_to_pydantic_model(input_schema, model_name)
            
            # Create tool instance with all necessary data
            tool_instance = D402MCPTool(
                name=tool_name,
                description=tool_description,
                mcp_server_url=self.url,
                mcp_tool_name=tool_name,
                mcp_session_id=self.session_id,
                d402_operator_account=self.account,  # Operator EOA for signing
                d402_wallet_address=self.wallet_address,  # IATPWallet contract (or EOA for testing)
                input_schema=input_schema,  # Keep for reference, but args_schema is what CrewAI uses
                args_schema=args_schema,  # Set the Pydantic model for CrewAI argument extraction
                # Pass additional headers for MCP-specific auth (e.g., Polymarket)
                additional_headers=self.additional_headers
            )
            # Note: args_schema is preserved by __init__ override, no need to set again
            # BaseTool will automatically enhance the description with argument info
            
            self.tools.append(tool_instance)
        
        logger.info(f"✅ Created {len(self.tools)} CrewAI tool wrappers")
        return self.tools
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager - cleanup."""
        logger.info("🔌 Closing D402MCPToolAdapter")
        return False


def create_d402_mcp_adapter(
    url: str,
    account: Any,  # Operator account (EOA) for signing
    wallet_address: str = None,  # IATPWallet contract address
    max_value: Optional[int] = None,
    additional_headers: Optional[Dict[str, str]] = None
) -> D402MCPToolAdapter:
    """
    Create a d402 MCP adapter for CrewAI.
    
    Args:
        url: MCP server URL
        account: Operator account (EOA) for signing payments
        wallet_address: IATPWallet contract address (if None, uses account.address for testing)
        max_value: Optional maximum payment value in base units
        additional_headers: Optional dictionary of extra headers to send to the MCP server
        
    Returns:
        D402MCPToolAdapter instance
        
    Example:
        ```python
        from eth_account import Account
        from traia_iatp.mcp import create_d402_mcp_adapter
        
        # For testing (uses mock wallet address)
        operator_account = Account.from_key("0x...")
        mock_wallet = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"  # Different from operator
        adapter = create_d402_mcp_adapter(
            url="http://localhost:8000/mcp",
            account=operator_account,
            wallet_address=mock_wallet,
            max_value=1_000_000  # $1.00 in USDC
        )
        
        # For Polymarket with session-based auth
        adapter = create_d402_mcp_adapter(
            url="https://polymarket-api-mcp.example.com/mcp",
            account=operator_account,
            wallet_address=wallet_address,
            additional_headers={"X-Polymarket-Key": "0x..."}  # Polymarket private key
        )
        
        with adapter as tools:
            agent = Agent(
                role="Analyst",
                goal="Analyze data",
                tools=tools
            )
        ```
    """
    return D402MCPToolAdapter(
        url, 
        account, 
        wallet_address, 
        max_value,
        additional_headers
    )


__all__ = ["D402MCPTool", "D402MCPToolAdapter", "create_d402_mcp_adapter"]

