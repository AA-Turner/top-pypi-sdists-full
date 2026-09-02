# Novita Agent Runtime - Main Application Class
# Copyright (c) 2024 Novita
# Licensed under the MIT License

"""Main application class for Novita Agent Runtime."""

import asyncio
import logging
from typing import Callable, Optional

from .context import RequestContext, AgentRuntimeContext
from .models import RuntimeConfig
from .server import AgentRuntimeServer


logger = logging.getLogger(__name__)


class AgentRuntimeApp:
    """Novita Agent Runtime Application Class"""
    
    def __init__(
        self, 
        config: Optional[RuntimeConfig] = None, 
        debug: bool = False
    ) -> None:
        """Initialize application
        
        Args:
            config: Runtime configuration, uses default if not provided
            debug: Enable debug mode (backward compatibility)
        """
        self.config = config or RuntimeConfig()
        if debug:
            self.config.debug = True
        
        self._server: Optional[AgentRuntimeServer] = None
        self._entrypoint_func: Optional[Callable] = None
        self._ping_func: Optional[Callable] = None
        
        logger.info("Agent Runtime App initialized")
    
    def entrypoint(self, func: Callable) -> Callable:
        """Register main entrypoint function - core decorator
        
        Supported function signatures:
        - func(request: dict) -> Any
        - func(request: dict, context: RequestContext) -> Any
        - async func(request: dict) -> Any
        - async func(request: dict, context: RequestContext) -> Any
        
        Supported return types:
        - Basic types: str, dict, list, int, float, bool
        - Generator: Generator[str, None, None] (sync streaming)
        - Async generator: AsyncGenerator[str, None] (async streaming)
        
        Args:
            func: Function to register
            
        Returns:
            Decorated function
        """
        self._entrypoint_func = func
        logger.info(f"Entrypoint function registered: {func.__name__}")
        return func
    
    def ping(self, func: Callable) -> Callable:
        """Register custom health check function (optional)
        
        Supported function signatures:
        - func() -> PingStatus
        - func() -> dict
        - async func() -> PingStatus
        - async func() -> dict
        
        Args:
            func: Health check function
            
        Returns:
            Decorated function
        """
        self._ping_func = func
        logger.info(f"Ping function registered: {func.__name__}")
        return func
    
    def middleware(self, middleware_func: Callable) -> Callable:
        """Register middleware function
        
        Middleware function signature:
        - async func(request: Request, call_next: Callable) -> Response
        
        Args:
            middleware_func: Middleware function
            
        Returns:
            Decorated function
        """
        if not self._server:
            self._server = AgentRuntimeServer(self.config)
        
        self._server.add_middleware(middleware_func)
        logger.info(f"Middleware registered: {middleware_func.__name__}")
        return middleware_func
    
    def run(
        self, 
        port: Optional[int] = None, 
        host: Optional[str] = None
    ) -> None:
        """Start server
        
        Args:
            port: Port number, uses configured port if not provided (default 8080)
            host: Host address, uses configured address if not provided (default 0.0.0.0)
        """
        # Update configuration
        if port is not None:
            self.config.port = port
        if host is not None:
            self.config.host = host
        
        # Check if entrypoint function is registered
        if not self._entrypoint_func:
            raise RuntimeError("No entrypoint function registered. Use @app.entrypoint decorator.")
        
        # Create and configure server (if not already created)
        if not self._server:
            self._server = AgentRuntimeServer(self.config)
        
        self._server.set_entrypoint_handler(self._entrypoint_func)
        
        if self._ping_func:
            self._server.set_ping_handler(self._ping_func)
        
        # Start server
        self._server.run(self.config.port, self.config.host)
    
    @property
    def context(self) -> Optional[RequestContext]:
        """Get current request context"""
        return AgentRuntimeContext.get_current_context()
