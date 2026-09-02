"""
Template Manager

Manages Agent template queries, focused on core functionality
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict

from novita_sandbox.core.connection_config import ConnectionConfig
from novita_sandbox.core.api import AsyncApiClient, handle_api_exception
from .auth import AuthManager
from .exceptions import TemplateNotFoundError, NetworkError, AuthenticationError
from .models import AgentTemplate

logger = logging.getLogger(__name__)

class TemplateManager:
    """Template Manager with caching support"""
    
    def __init__(self, auth_manager: AuthManager, cache_ttl_seconds: int = 300):
        """Initialize template manager
        
        Args:
            auth_manager: Authentication manager
            cache_ttl_seconds: Cache TTL in seconds (default: 300 = 5 minutes)
        """
        self.auth_manager = auth_manager
        
        # Create connection config - following CLI project, use access_token
        self.connection_config = ConnectionConfig(
            access_token=self.auth_manager.api_key
        )
        self._client = None
        
        # Cache configuration
        self._cache_ttl_seconds = cache_ttl_seconds
        self._template_cache: Dict[str, AgentTemplate] = {}
        self._cache_updated_at: Optional[datetime] = None
        self._cache_lock = asyncio.Lock()
    
    async def _get_client(self) -> AsyncApiClient:
        """Get API client"""
        if self._client is None:
            # Import httpx.Limits for connection pool configuration
            import httpx
            self._client = AsyncApiClient(
                self.connection_config, 
                require_api_key=False, 
                require_access_token=True,
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
            )
        return self._client
    
    async def close(self):
        """Close HTTP client and clear cache"""
        if self._client:
            await self._client.get_async_httpx_client().aclose()
            self._client = None
        self.clear_cache()
    
    def clear_cache(self):
        """Clear template cache"""
        self._template_cache.clear()
        self._cache_updated_at = None
    
    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid
        
        Returns:
            True if cache is valid, False otherwise
        """
        if not self._cache_updated_at:
            return False
        
        age = datetime.now() - self._cache_updated_at
        return age.total_seconds() < self._cache_ttl_seconds
    
    def _update_cache(self, templates: List[AgentTemplate]):
        """Update template cache
        
        Args:
            templates: List of templates to cache
        """
        self._template_cache.clear()
        for template in templates:
            self._template_cache[template.template_id] = template
        self._cache_updated_at = datetime.now()
    
    def _map_template_data_to_model(self, template_data: dict) -> AgentTemplate:
        """Map API returned template data to AgentTemplate model
        
        Args:
            template_data: Template data dictionary returned by API
            
        Returns:
            AgentTemplate object
        """
        return AgentTemplate(
            template_id=template_data.get("templateID") or template_data.get("id"),
            name=template_data.get("aliases", [None])[0] if template_data.get("aliases") else "Unknown",
            version=template_data.get("version", "1.0.0"),
            description=template_data.get("description"),
            author=template_data.get("createdBy", {}).get("email") if template_data.get("createdBy") else None,
            tags=template_data.get("tags", []),
            created_at=datetime.fromisoformat(
                template_data.get("createdAt", datetime.now().isoformat()).replace('Z', '+00:00')
            ) if template_data.get("createdAt") else datetime.now(),
            updated_at=datetime.fromisoformat(
                template_data.get("updatedAt", datetime.now().isoformat()).replace('Z', '+00:00')
            ) if template_data.get("updatedAt") else datetime.now(),
            status="active",  # CLI doesn't have status field, default to active
            metadata=template_data.get("metadata", {}),
            size=None,  # CLI doesn't have size field
            build_time=None,  # CLI doesn't have build_time field
            dependencies=[],  # CLI doesn't have dependencies field
            runtime_info=None  # CLI doesn't have runtime_info field
        )
    
    async def list_templates(
        self, 
        use_cache: bool = True,
        with_metadata: bool = False
    ) -> List[AgentTemplate]:
        """List templates with caching support
        
        Args:
            tags: Tag filter
            name_filter: Name filter
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Template list, each template's metadata field contains Agent metadata
        """
        # Check cache if no filters are applied and cache is valid
        if use_cache:
            async with self._cache_lock:
                if self._is_cache_valid():
                    return list(self._template_cache.values())
        
        try:
            client = await self._get_client()
            
            # Build query parameters
            params = {}
            if with_metadata:
                params["metadata"] = "true"
            
            # Use ApiClient to make HTTP request
            response = await client.get_async_httpx_client().request(
                method="GET",
                url="/templates",
                params=params
            )
            
            # Handle response status code
            if response.status_code == 401:
                raise AuthenticationError("Invalid or expired API Key")
            elif response.status_code != 200:
                # Use handle_api_exception to handle errors
                from novita_sandbox.core.api.client.types import Response as NovitaResponse
                novita_response = NovitaResponse(
                    status_code=response.status_code,
                    content=response.content,
                    headers=response.headers,
                    parsed=None
                )
                raise handle_api_exception(novita_response)
            
            data = response.json()
            templates = []
            
            # Process response data - based on CLI pattern, data should be template array directly
            template_list = data if isinstance(data, list) else data.get("templates", [])
            
            for template_data in template_list:
                try:
                    # Use private method to map template data
                    template = self._map_template_data_to_model(template_data)
                    templates.append(template)
                except Exception as e:
                    # Skip invalid template data, log error but don't interrupt processing
                    logger.warning(f"Warning: Failed to parse template data: {e}")
                    continue
            
            # Update cache
            async with self._cache_lock:
                self._update_cache(templates)
            
            return templates
            
        except AuthenticationError:
            raise
        except NetworkError:
            raise
        except Exception as e:
            raise NetworkError(f"Failed to list templates: {str(e)}")
    
    async def get_template(self, template_id: str, use_cache: bool = True) -> AgentTemplate:
        """Get specific template with caching support
        
        Due to backend API limitations, this method fetches all templates
        and filters by template_id. Uses cache to avoid redundant API calls.
        
        Args:
            template_id: Template ID
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Template object containing complete Agent metadata
            
        Raises:
            TemplateNotFoundError: Raised when template does not exist
        """
        try:
            # Check cache first if enabled
            if use_cache:
                async with self._cache_lock:
                    if self._is_cache_valid() and template_id in self._template_cache:
                        return self._template_cache[template_id]
            
            # Get all templates (will use cache if valid)
            templates = await self.list_templates(use_cache=use_cache, with_metadata=True)
            
            # Find matching template
            for template in templates:
                if template.template_id == template_id:
                    return template
            
            # Template not found
            raise TemplateNotFoundError(f"Template {template_id} not found")
            
        except TemplateNotFoundError:
            raise
        except AuthenticationError:
            raise
        except NetworkError:
            raise
        except Exception as e:
            raise NetworkError(f"Failed to get template: {str(e)}")
    
    async def template_exists(self, template_id: str, use_cache: bool = True) -> bool:
        """Check if template exists with caching support
        
        Args:
            template_id: Template ID
            use_cache: Whether to use cache (default: True)
            
        Returns:
            Whether template exists
        """
        try:
            # Check cache first if enabled
            if use_cache:
                async with self._cache_lock:
                    if self._is_cache_valid():
                        return template_id in self._template_cache
            
            # Use list_templates to check (will use cache if valid)
            templates = await self.list_templates(use_cache=use_cache, with_metadata=False)
            return any(template.template_id == template_id for template in templates)
        except Exception:
            # Consider template non-existent on network errors, etc.
            return False
    
    async def refresh_templates(self) -> List[AgentTemplate]:
        """Force refresh template cache by fetching from API
        
        Returns:
            Updated list of templates
        """
        return await self.list_templates(use_cache=False)