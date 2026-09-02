# Novita Agent Runtime - HTTP Server Implementation
# Copyright (c) 2024 Novita
# Licensed under the MIT License

"""HTTP server implementation for Novita Agent Runtime based on Starlette."""

import asyncio
import inspect
import json
import logging
import time
import traceback
import uuid
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Union, AsyncGenerator, Generator

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse, StreamingResponse
from starlette.routing import Route
import uvicorn

from .models import RuntimeConfig, InvocationResponse, PingResponse, PingStatus
from .context import RequestContext, AgentRuntimeContext
from ..utils.safe_stdout_context import safe_stdout_context

logger = logging.getLogger(__name__)
class AgentRuntimeServer:
    """Agent Runtime Server"""
    
    def __init__(self, config: RuntimeConfig):
        """Initialize server
        
        Args:
            config: Runtime configuration
        """
        self.config = config
        self._entrypoint_func: Optional[Callable] = None
        self._ping_func: Optional[Callable] = None
        self._middlewares: List[Callable] = []
        self._app: Optional[Starlette] = None
        
        self._setup_app()
    
    def set_entrypoint_handler(self, func: Callable) -> None:
        """Set entrypoint handler function"""
        self._entrypoint_func = func
        logger.info(f"Entrypoint handler set: {func.__name__}")
    
    def set_ping_handler(self, func: Optional[Callable]) -> None:
        """Set health check handler function"""
        self._ping_func = func
        if func:
            logger.info(f"Ping handler set: {func.__name__}")
    
    def add_middleware(self, middleware_func: Callable) -> None:
        """Add middleware"""
        self._middlewares.append(middleware_func)
        logger.info(f"Middleware added: {middleware_func.__name__}")
    
    def run(self, port: int, host: str) -> None:
        """Start server"""
        logger.info(f"Starting Agent Runtime server on {host}:{port}")
        uvicorn.run(
            self._app,
            host=host,
            port=port,
            log_level="info" if self.config.debug else "warning",
            access_log=self.config.debug
        )
    
    def _setup_app(self) -> None:
        """Setup Starlette application"""
        middleware = []
        
        # CORS middleware
        if self.config.cors_origins:
            middleware.append(
                Middleware(
                    CORSMiddleware,
                    allow_origins=self.config.cors_origins,
                    allow_methods=["GET", "POST", "OPTIONS"],
                    allow_headers=["*"],
                )
            )
        
        # Routes
        routes = [
            Route("/", self._handle_root, methods=["GET"]),
            Route("/ping", self._handle_ping, methods=["GET"]),
            Route("/invocations", self._handle_invocations, methods=["POST"]),
        ]
        
        self._app = Starlette(
            debug=self.config.debug,
            routes=routes,
            middleware=middleware
        )
    
    async def _handle_root(self, request: Request) -> JSONResponse:
        """Handle root endpoint"""
        return JSONResponse({
            "service": "Novita Agent Runtime",
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "invocations": "/invocations",
                "ping": "/ping"
            }
        })
    
    async def _handle_ping(self, request: Request) -> JSONResponse:
        """Handle /ping endpoint"""
        try:
            if self._ping_func:
                # Call custom health check function
                if inspect.iscoroutinefunction(self._ping_func):
                    result = await self._ping_func()
                else:
                    result = self._ping_func()
                
                if isinstance(result, dict):
                    # PingResponse model now supports auto-normalizing status values
                    response = PingResponse(**result)
                elif isinstance(result, PingResponse):
                    response = result
                else:
                    response = PingResponse(
                        status=PingStatus.HEALTHY,
                        message=str(result) if result else None,
                        timestamp=datetime.now().isoformat()
                    )
            else:
                response = PingResponse(
                    status=PingStatus.HEALTHY,
                    timestamp=datetime.now().isoformat()
                )
            
            return JSONResponse(response.model_dump())
            
        except Exception as e:
            logger.error(f"Ping function error: {e}")
            error_response = PingResponse(
                status=PingStatus.HEALTHY_BUSY,
                message=f"Health check error: {str(e)}",
                timestamp=datetime.now().isoformat()
            )
            return JSONResponse(error_response.model_dump(), status_code=500)
    
    async def _handle_invocations(self, request: Request) -> Response:
        """Handle /invocations endpoint"""
        start_time = time.time()
        context = None
        
        try:
            # Check request size
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > self.config.max_request_size:
                return JSONResponse(
                    {"error": f"Request too large: {content_length} bytes"},
                    status_code=413
                )
            
            # Parse request body - keep original data without validation
            try:
                request_data = await request.json()
            except Exception as e:
                return JSONResponse(
                    {"error": f"Invalid JSON: {str(e)}"},
                    status_code=400
                )
            
            # Create request context - only extract system fields
            # Keep original request_data intact for user's entrypoint function
            context = RequestContext(
                sandbox_id=request_data.get("sandbox_id"),  # Optional, for backward compatibility
                request_id=str(uuid.uuid4()),  # System-generated
                headers=dict(request.headers)
            )
            
            # Set context
            AgentRuntimeContext.set_current_context(context)
            
            try:
                # Execute complete request handling through middleware chain
                # Pass original request_data (dict) instead of InvocationRequest model
                return await self._execute_through_middleware_chain(request, request_data, context, start_time)
                
            finally:
                # Clear context
                AgentRuntimeContext.clear_current_context()
                
        except Exception as e:
            logger.error(f"Invocation error: {e}\n{traceback.format_exc()}")
            duration = time.time() - start_time
            error_response = InvocationResponse(
                result=None,
                status="error",
                duration=duration,
                error=str(e),
                metadata={"request_id": context.request_id if context else None}
            )
            return JSONResponse(error_response.model_dump(), status_code=500)
    
    async def _execute_agent_function(self, request_data: Dict[str, Any], context: RequestContext) -> Any:
        """Execute Agent function
        
        Args:
            request_data: Original request data dict (not validated, preserves all user fields)
            context: Request context with system fields
            
        Returns:
            Result from agent function (can be any type, including generators)
        """
        if not self._entrypoint_func:
            raise RuntimeError("No entrypoint function registered")
        
        # Use safe stdout context to avoid BrokenPipeError
        with safe_stdout_context(logger):
            # Prepare function parameters
            func_signature = inspect.signature(self._entrypoint_func)
            params = list(func_signature.parameters.keys())
            
            # Determine parameters to pass based on function signature
            if len(params) >= 2:
                # Function accepts request and context parameters
                args = (request_data, context)
            else:
                # Function only accepts request parameter
                args = (request_data,)
            
            # Execute function
            if inspect.iscoroutinefunction(self._entrypoint_func):
                return await self._entrypoint_func(*args)
            else:
                # Execute sync function in thread pool
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, self._entrypoint_func, *args)
    
    def _is_streaming_result(self, result: Any) -> bool:
        """Check if result is a streaming result"""
        # Exclude dict and string, they have __iter__ but are not streaming results
        if isinstance(result, (dict, str, bytes)):
            return False
        
        return (
            inspect.isgenerator(result) or
            inspect.isasyncgen(result) or
            hasattr(result, '__aiter__') or
            (hasattr(result, '__iter__') and not isinstance(result, (list, tuple, set)))
        )
    
    async def _create_streaming_response(self, result: Any) -> StreamingResponse:
        """Create streaming response with real-time chunk delivery"""
        async def stream_generator():
            try:
                if inspect.isasyncgen(result):
                    # Async generator
                    async for chunk in result:
                        sse_data = self._serialize_chunk_to_sse(chunk)
                        # Yield as bytes to ensure immediate transmission
                        yield sse_data.encode('utf-8')
                elif inspect.isgenerator(result):
                    # Sync generator
                    for chunk in result:
                        sse_data = self._serialize_chunk_to_sse(chunk)
                        yield sse_data.encode('utf-8')
                elif hasattr(result, '__aiter__'):
                    # Async iterator
                    async for chunk in result:
                        sse_data = self._serialize_chunk_to_sse(chunk)
                        yield sse_data.encode('utf-8')
                else:
                    # Regular iterator
                    for chunk in result:
                        sse_data = self._serialize_chunk_to_sse(chunk)
                        yield sse_data.encode('utf-8')
            except Exception as e:
                logger.error(f"Streaming error: {e}")
                error_data = f"data: {json.dumps({'error': str(e)})}\n\n"
                yield error_data.encode('utf-8')
        
        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream",  # ✅ SSE standard format
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Disable nginx buffering
            }
        )
    
    def _serialize_chunk_to_sse(self, chunk: Any) -> str:
        try:
            # Try direct JSON serialization
            # This handles: dict, list, str, int, float, bool, None
            data = json.dumps(chunk, ensure_ascii=False)
        except (TypeError, ValueError):
            # For objects that cannot be directly serialized (e.g., custom class instances)
            # Convert to string first, then serialize
            data = json.dumps(str(chunk), ensure_ascii=False)
        
        # Return SSE format: "data: {json}\n\n"
        return f"data: {data}\n\n"

    async def _execute_through_middleware_chain(self, request: Request, request_data: Dict[str, Any], context: RequestContext, start_time: float) -> Response:
        """Execute complete request handling through middleware chain
        
        Args:
            request: Starlette Request object
            request_data: Original request data dict
            context: Request context
            start_time: Request start time
        """
        
        if not self._middlewares:
            # No middleware, execute core logic directly
            return await self._execute_core_agent_logic(request_data, context, start_time)
        
        # Build middleware chain in reverse
        middleware_chain = list(reversed(self._middlewares))
        
        # Build final handler function
        async def final_handler(req: Request) -> Response:
            return await self._execute_core_agent_logic(request_data, context, start_time)
        
        # Build middleware chain from innermost layer
        current_handler = final_handler
        
        for middleware in middleware_chain:
            current_handler = self._wrap_middleware(middleware, current_handler)
        
        # Execute complete middleware chain
        return await current_handler(request)
    
    def _wrap_middleware(self, middleware: Callable, next_handler: Callable) -> Callable:
        """Wrap middleware function"""
        async def wrapped_handler(request: Request) -> Response:
            async def call_next(modified_request: Request = None) -> Response:
                req = modified_request if modified_request is not None else request
                return await next_handler(req)
            
            if inspect.iscoroutinefunction(middleware):
                result = await middleware(request, call_next)
                return result
            else:
                # Sync middleware
                result = middleware(request, call_next)
                if inspect.iscoroutine(result):
                    result = await result
                return result
        
        return wrapped_handler
    
    async def _execute_core_agent_logic(self, request_data: Dict[str, Any], context: RequestContext, start_time: float) -> Response:
        """Execute core Agent processing logic
        
        Args:
            request_data: Original request data dict
            context: Request context
            start_time: Request start time
        """
        # Execute Agent function
        result = await self._execute_agent_function(request_data, context)
        
        # Automatically determine response type based on return value
        # If the function returns a generator/async generator, use SSE streaming
        if self._is_streaming_result(result):
            return await self._create_streaming_response(result)
        
        # Create regular JSON response for non-streaming results
        duration = time.time() - start_time
        response = InvocationResponse(
            result=result,
            status="success",
            duration=duration,
            metadata={"request_id": context.request_id}
        )
        
        return JSONResponse(response.model_dump())
    
    def _call_next_placeholder(self, request: Request):
        """Middleware call placeholder (deprecated)"""
        # This function has been replaced by the new middleware chain system
        pass
