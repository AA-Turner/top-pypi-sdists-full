"""OAuth endpoint discovery for MCP servers.

This module implements Authorization Server Metadata discovery (RFC8414) 
for finding OAuth endpoints from the MCP server's base URL.
"""

import httpx
from typing import Dict, Optional, Any, Tuple
import logging
from urllib.parse import urlparse, urlunparse

from ..exceptions import NotOAuthCompliantError

logger = logging.getLogger(__name__)



async def discover_mcp_oauth_config(mcp_server_url: str) -> Tuple[str, Dict[str, Any]]:
    """Discover OAuth configuration for an MCP server.
    
    This directly discovers Authorization Server Metadata from the MCP server base URL.
    
    Args:
        mcp_server_url: The MCP server URL
        
    Returns:
        Tuple of (authorization_server_url, oauth_metadata)
        
    Raises:
        httpx.HTTPError: If discovery requests fail
        ValueError: If responses are invalid or missing required fields
    """
    # Get base URL by removing path component
    parsed = urlparse(mcp_server_url)
    auth_server_url = urlunparse((parsed.scheme, parsed.netloc, '', '', '', ''))
    
    logger.info(f"Discovering OAuth configuration from: {auth_server_url}")
    
    # Discover the authorization server's metadata directly
    auth_metadata = await discover_authorization_server_metadata(auth_server_url)
    
    return auth_server_url, auth_metadata



async def discover_authorization_server_metadata(auth_server_url: str) -> Dict[str, Any]:
    """Discover Authorization Server Metadata according to RFC8414.
    
    This should be at: <auth_server_url>/.well-known/oauth-authorization-server
    
    Args:
        auth_server_url: The authorization server URL
        
    Returns:
        Dictionary containing authorization server metadata
        
    Raises:
        httpx.HTTPError: If discovery request fails
        ValueError: If response is invalid
    """
    # Ensure URL has no trailing slash
    auth_server_url = auth_server_url.rstrip('/')
    
    # Build authorization server metadata URL
    metadata_url = f"{auth_server_url}/.well-known/oauth-authorization-server"
    
    logger.info(f"Discovering authorization server metadata from: {metadata_url}")
    
    try:
        async with httpx.AsyncClient() as client:
            # Include MCP protocol version header as recommended
            headers = {
                'MCP-Protocol-Version': '2025-03-26'  # Latest stable version
            }
            
            response = await client.get(metadata_url, headers=headers)
            response.raise_for_status()
            
        try:
            metadata = response.json()
        except Exception as e:
            raise ValueError(f"Invalid JSON response from auth server metadata: {e}")
            
        # Validate required fields according to RFC8414
        required_fields = ['issuer', 'authorization_endpoint', 'token_endpoint']
        missing_fields = [f for f in required_fields if f not in metadata]
        
        if missing_fields:
            raise ValueError(
                f"Authorization server metadata missing required fields: {', '.join(missing_fields)}"
            )
        
        # Validate issuer matches the URL
        if metadata['issuer'].rstrip('/') != auth_server_url:
            logger.warning(
                f"Issuer mismatch: metadata issuer '{metadata['issuer']}' "
                f"doesn't match server URL '{auth_server_url}'"
            )
        
        # Log important discovery information
        discovery_info = [
            f"OAuth discovery successful for {auth_server_url}:",
            f"  Issuer: {metadata.get('issuer')}",
            f"  Authorization: {metadata.get('authorization_endpoint')}",
            f"  Token: {metadata.get('token_endpoint')}"
        ]
        
        if metadata.get('registration_endpoint'):
            discovery_info.append(f"  Registration: {metadata.get('registration_endpoint')}")
        if metadata.get('revocation_endpoint'):
            discovery_info.append(f"  Revocation: {metadata.get('revocation_endpoint')}")
        if metadata.get('scopes_supported'):
            discovery_info.append(f"  Scopes: {', '.join(metadata.get('scopes_supported', []))}")
        if metadata.get('code_challenge_methods_supported'):
            discovery_info.append(f"  PKCE methods: {', '.join(metadata.get('code_challenge_methods_supported', []))}")
        
        logger.info("\n".join(discovery_info))
        # Extract all relevant OAuth configuration
        result = {
            'issuer': metadata['issuer'],
            'authorization_endpoint': metadata['authorization_endpoint'],
            'token_endpoint': metadata['token_endpoint'],
            'registration_endpoint': metadata.get('registration_endpoint'),
            'scopes_supported': metadata.get('scopes_supported', []),
            'response_types_supported': metadata.get('response_types_supported', ['code']),
            'grant_types_supported': metadata.get('grant_types_supported', []),
            'code_challenge_methods_supported': metadata.get(
                'code_challenge_methods_supported', ['S256']
            ),
            'token_endpoint_auth_methods_supported': metadata.get(
                'token_endpoint_auth_methods_supported', ['none']
            ),
        }
        
        # Add optional endpoints
        optional_endpoints = [
            'revocation_endpoint', 'introspection_endpoint', 'userinfo_endpoint',
            'jwks_uri', 'end_session_endpoint'
        ]
        for endpoint in optional_endpoints:
            if endpoint in metadata:
                result[endpoint] = metadata[endpoint]
        
        return result
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            logger.info(
                f"Authorization server metadata not found at {metadata_url}. "
                f"Server does not support OAuth."
            )
            raise NotOAuthCompliantError(
                f"OAuth metadata endpoint not found at {metadata_url}. "
                f"Server does not appear to support OAuth authentication."
            )
        else:
            logger.error(f"HTTP error during auth server discovery: {e}")
            raise
        
    except httpx.RequestError as e:
        logger.error(f"Network error during auth server discovery: {e}")
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error during auth server discovery: {e}")
        raise


def get_default_auth_endpoints(auth_server_url: str) -> Dict[str, Any]:
    """Get default OAuth endpoints when discovery is not supported.
    
    According to MCP spec, if no metadata discovery, use these defaults:
    - /authorize for authorization endpoint
    - /token for token endpoint  
    - /register for registration endpoint
    
    Args:
        auth_server_url: The authorization server base URL
        
    Returns:
        Dictionary with default endpoints
    """
    base_url = auth_server_url.rstrip('/')
    
    logger.info(f"Using default OAuth endpoints for {base_url}")
    
    return {
        'issuer': base_url,
        'authorization_endpoint': f"{base_url}/authorize",
        'token_endpoint': f"{base_url}/token",
        'registration_endpoint': f"{base_url}/register",
        'scopes_supported': [],  # Unknown
        'response_types_supported': ['code'],  # OAuth 2.1 default
        'grant_types_supported': ['authorization_code', 'refresh_token'],
        'code_challenge_methods_supported': ['S256'],  # Required by OAuth 2.1
        'token_endpoint_auth_methods_supported': ['none'],  # For public clients
    }


 