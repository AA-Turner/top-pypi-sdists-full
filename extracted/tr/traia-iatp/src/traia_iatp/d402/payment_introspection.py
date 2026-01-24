"""
Helper to extract payment configurations from @require_payment_for_tool decorators.

This allows us to have a single source of truth - payment config is declared
in the decorator, and we introspect it to build TOOL_PAYMENT_CONFIGS.
"""

import logging
from typing import Dict, Any, Optional

from .types import TokenAmount

logger = logging.getLogger(__name__)


def extract_payment_configs_from_mcp(mcp_server, server_address: str) -> Dict[str, Dict[str, Any]]:
    """
    Extract payment configurations from tools decorated with @require_payment_for_tool.
    
    This introspects the decorator closures to extract TokenAmount objects,
    eliminating the need to duplicate payment configuration.
    
    Args:
        mcp_server: FastMCP server instance
        server_address: Server's payment address
    
    Returns:
        Dict mapping tool names to payment configurations
        Format: {"tool_name": {"price_wei": "1000", "token_address": "0x...", ...}}
    
    Usage:
        mcp = FastMCP("Server")
        
        # Add tools with @require_payment_for_tool decorators
        @mcp.tool()
        @require_payment_for_tool(price=TokenAmount(...))
        async def my_tool(context): ...
        
        # Extract configs dynamically
        TOOL_PAYMENT_CONFIGS = extract_payment_configs_from_mcp(mcp, SERVER_ADDRESS)
        
        # Add middleware with extracted configs
        app.add_middleware(D402PaymentMiddleware, tool_payment_configs=TOOL_PAYMENT_CONFIGS, ...)
    """
    tool_payment_configs = {}
    
    try:
        # Get registered tools from FastMCP
        tools = mcp_server._tool_manager.list_tools()
        
        for tool in tools:
            if not hasattr(tool, 'fn'):
                continue
            
            fn = tool.fn
            tool_name = tool.name
            
            # Check if function has payment metadata (from @require_payment_for_tool decorator)
            # New approach: metadata stored as attribute (no closure needed)
            if hasattr(fn, '_d402_payment_config'):
                payment_config = fn._d402_payment_config
                price = payment_config.get('price')
                description = payment_config.get('description', tool_name)
                
                if isinstance(price, TokenAmount):
                    token_amount = price
                else:
                    logger.debug(f"Tool {tool_name}: price is not TokenAmount")
                    continue
            # Fallback: Check closure for backwards compatibility
            elif hasattr(fn, '__closure__') and fn.__closure__:
                token_amount = None
                description = None
                for cell in fn.__closure__:
                    try:
                        val = cell.cell_contents
                        if isinstance(val, TokenAmount):
                            token_amount = val
                        elif isinstance(val, str):
                            description = val
                    except:
                        pass
                
                if not token_amount:
                    logger.debug(f"Tool {tool_name}: No TokenAmount in closure")
                    continue
                    
                description = description or tool.description or tool_name
            else:
                logger.debug(f"Tool {tool_name}: No payment metadata found")
                continue
            
            if token_amount:
                # Extract payment config from TokenAmount (including EIP712 domain)
                # Use description from metadata if available, otherwise from tool
                final_description = description if 'description' in locals() else (tool.description or tool_name)
                
                config = {
                    "price_wei": token_amount.amount,
                    "token_address": token_amount.asset.address,
                    "network": token_amount.asset.network,
                    "server_address": server_address,
                    "description": final_description,
                    "eip712_domain": {
                        "name": token_amount.asset.eip712.name if token_amount.asset.eip712 else "USD Coin",
                        "version": token_amount.asset.eip712.version if token_amount.asset.eip712 else "2"
                    }
                }
                
                tool_payment_configs[tool_name] = config
                logger.info(f"✅ Extracted payment config for {tool_name}: {config['price_wei']} wei on {config['network']}")
            else:
                logger.debug(f"Tool {tool_name}: No TokenAmount found (free tool)")
        
        logger.info(f"📊 Extracted {len(tool_payment_configs)} payment configs from decorators")
        
    except Exception as e:
        logger.error(f"Error extracting payment configs: {e}")
        import traceback
        logger.error(traceback.format_exc())
    
    return tool_payment_configs


__all__ = ["extract_payment_configs_from_mcp"]

