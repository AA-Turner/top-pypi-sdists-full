"""
Sandbox Session Management

Manages the lifecycle of a single Sandbox instance and Agent invocations
"""

from datetime import datetime
from typing import Any, AsyncIterator, Dict, Optional, Union
import httpx
import logging
from novita_sandbox.core import AsyncSandbox

from .exceptions import (
    InvocationError, 
    NetworkError, 
    SandboxOperationError, 
    SessionNotFoundError
)
from .models import PingResponse, PingStatus, SessionStatus

# Logger for session operations
logger = logging.getLogger(__name__)


class SandboxSession:
    """Sandbox session management"""
    
    def __init__(
        self,
        template_id: str,
        sandbox: AsyncSandbox,  # Novita Sandbox instance
        client: "AgentRuntimeClient",
        agent_id: Optional[str] = None  # Optional agent_id for AWS compatibility
    ):
        """Initialize session
        
        Args:
            template_id: Template ID (internal identifier)
            sandbox: Novita Sandbox instance (one-to-one relationship)
            client: Agent Runtime client reference
            agent_id: Optional agent_id for AWS Agentcore compatibility
        """
        self.template_id = template_id
        self.agent_id = agent_id  # AWS Agentcore compatible agent identifier
        self.sandbox = sandbox
        self._client_ref = client  # Avoid circular reference
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.status = SessionStatus.ACTIVE
        self._host_url: Optional[str] = None
        self._http_client: Optional[httpx.AsyncClient] = None
    
    async def _get_http_client(self) -> httpx.AsyncClient:
        """Get HTTP client"""
        if self._http_client is None:
            # Get authentication headers from client reference
            auth_headers = self._client_ref.auth_manager.get_auth_headers()
            self._http_client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                headers=auth_headers  # Use complete authentication headers, including Authorization
            )
        return self._http_client
    
    async def _close_http_client(self):
        """Close HTTP client"""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None
    
    # === Core Invocation Methods ===
    async def invoke(
        self,
        request: Union[Dict[str, Any], str],
        timeout: Optional[int] = None
    ) -> Union[Dict[str, Any], AsyncIterator[str]]:
        """Invoke Agent (auto-detect streaming)
        
        The method automatically detects whether the Agent returns streaming or non-streaming
        response based on the Content-Type header:
        - Content-Type: application/json -> Returns Dict
        - Content-Type: text/event-stream -> Returns AsyncIterator
        
        Args:
            request: Invocation request (str or dict with any structure)
                    - str: Will be sent as {"prompt": "your string"}
                    - dict: Will be sent as-is, preserving all fields
            timeout: Optional timeout in seconds (default: 300)
            
        Returns:
            Dict[str, Any] for non-streaming responses
            AsyncIterator[str] for streaming responses (auto-detected)
            
        Raises:
            InvocationError: Raised when invocation fails
            SessionNotFoundError: Raised when session does not exist
            NetworkError: Raised on network error
            
        Example:
            # String request
            result = await session.invoke("Analyze this data")
            
            # Dict request with custom fields
            result = await session.invoke({
                "query": "Hello",
                "max_tokens": 1000,
                "temperature": 0.7,
                "custom_field": "any value"
            })
        """
        if self.status not in [SessionStatus.ACTIVE]:
            raise SessionNotFoundError(f"Session {self.sandbox_id} is not active (status: {self.status})")
        
        # Normalize request to dict - preserve all fields
        if isinstance(request, str):
            try:
                import json
                request_body = json.loads(request)
                # If parsing succeeds but result is not a dict (e.g., array, string, etc.), wrap it as prompt
                if not isinstance(request_body, dict):
                    request_body = {"prompt": request}
            except (json.JSONDecodeError, ValueError):
                # If not valid JSON, treat it as a plain prompt string
                request_body = {"prompt": request}
        elif isinstance(request, dict):
            request_body = request  # Use as-is, don't transform
        else:
            raise InvocationError(f"Invalid request format: {type(request)}. Must be str or dict.")
        
        try:
            self.last_activity = datetime.now()
            
            request_url = f"{self.host_url}/invocations"
            client = await self._get_http_client()
            
            # Log request details (verbose)
            logger.debug(f"Sending request to Agent:")
            logger.debug(f"  URL: {request_url}")
            logger.debug(f"  Payload: {request_body}")
            
            # Create HTTP request - MUST be done outside of context if streaming
            # We'll handle streaming responses separately
            
            # First, make a request to check headers (without reading body)
            request_obj = client.build_request(
                "POST",
                request_url,
                json=request_body,
                timeout=httpx.Timeout(timeout or 300),
                headers={"Content-Type": "application/json"}
            )
            
            # Send request and get response with streaming enabled
            response = await client.send(request_obj, stream=True)
            
            # Log response details
            logger.info(f"Response status: {response.status_code} {response.reason_phrase}")
            content_type = response.headers.get("content-type", "")
            logger.info(f"Response Content-Type: {content_type}")
            
            if response.status_code != 200:
                error_text = await response.aread()
                error_text = error_text.decode('utf-8')
                await response.aclose()
                logger.error(f"Error response body: {error_text}")
                raise InvocationError(
                    f"Agent returned status {response.status_code} from URL [{request_url}]: {error_text}"
                )
            
            # Auto-detect response type BEFORE reading body
            content_type_lower = content_type.lower()
            is_streaming = self._is_streaming_response(content_type_lower)

            logger.info(f"Is streaming: {is_streaming}")

            if is_streaming:
                # Streaming response - use TRUE streaming (don't read full body)
                logger.debug('Detected streaming response, using real-time stream')
                # Return async generator directly
                # NOTE: response will be closed by the generator when done
                return self._handle_streaming_response(response)

            # Non-streaming: read full body
            response_bytes = await response.aread()
            response_text = response_bytes.decode('utf-8')
            await response.aclose()
            logger.info(f"Response body (first 500 chars): {response_text[:500]}")
            logger.info(f"Response body length: {len(response_text)} bytes")
            
            # Check for empty response
            if not response_text or response_text.strip() == '':
                logger.error('Agent returned empty response (0 bytes)')
                logger.error('Possible causes:')
                logger.error('  1. Agent code missing return statement')
                logger.error('  2. Async function not awaited properly')
                logger.error('  3. Exception caught but not returned')
                logger.error('  4. Request payload format mismatch')
                raise InvocationError('Agent returned empty response. Check agent logs for errors.')
            
            # Fallback: detect SSE format even if Content-Type is wrong
            if response_text.startswith('data: '):
                logger.warning(f"Response looks like SSE but Content-Type is '{content_type}'")
                logger.warning("Agent should set Content-Type to 'text/event-stream' for streaming responses")
                return self._handle_streaming_response_from_text(response_text)
            
            # Non-streaming response - parse JSON
            logger.debug('Detected non-streaming response, parsing JSON...')
            try:
                import json
                result = json.loads(response_text)
                logger.debug('JSON parsed successfully')
                return result
            except json.JSONDecodeError as parse_error:
                logger.error(f'Failed to parse JSON: {parse_error}')
                logger.error(f'Raw response text: {response_text}')
                raise InvocationError(f'Failed to parse response as JSON: {parse_error}')
                
        except InvocationError:
            # Re-raise InvocationError as-is
            raise
        except Exception as e:
            if "connection" in str(e).lower() or "timeout" in str(e).lower():
                raise NetworkError(f"Network error during invocation: {str(e)}")
            else:
                logger.error(f"Unexpected error during invocation: {str(e)}", exc_info=True)
                raise InvocationError(f"Agent invocation failed: {str(e)}")
    
    def _is_streaming_response(self, content_type: str) -> bool:
        """Check if response is streaming based on Content-Type header
        
        Args:
            content_type: Content-Type header value (lowercased)
            
        Returns:
            True if streaming, False otherwise
        """
        return "text/event-stream" in content_type or "application/x-ndjson" in content_type
    
    async def _handle_streaming_response(self, response: httpx.Response) -> AsyncIterator[str]:
        """Handle streaming response (SSE format) with real-time chunk processing
        
        Args:
            response: httpx Response object (will be closed after streaming completes)
            
        Yields:
            Streamed data chunks
        """
        try:
            buffer = ""
            
            # Use aiter_text() to get text chunks as they arrive (real-time streaming)
            # This yields chunks as soon as they're received, without waiting for complete lines
            async for chunk in response.aiter_text():
                buffer += chunk
                
                # Process complete lines from the buffer
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    
                    # SSE format: "data: {json_content}"
                    if line.startswith("data: "):
                        data = line[6:]  # Remove "data: " prefix
                        if data.strip():
                            yield data
                    elif line.strip() and not line.startswith(":"):  # Not empty line or comment
                        # Plain text chunk (not SSE format)
                        yield line
            
            # Process remaining buffer if any
            if buffer.strip():
                if buffer.startswith("data: "):
                    data = buffer[6:]
                    if data.strip():
                        yield data
                elif not buffer.startswith(":"):
                    yield buffer
        finally:
            # Always close the response when done streaming
            await response.aclose()
    
    async def _handle_streaming_response_from_text(self, response_text: str):
        """Handle streaming response from already-read text (SSE format)
        
        This method is used when we've already read the response body as text
        and need to parse it as a streaming response.
        
        Args:
            response_text: Complete response text
            
        Yields:
            Streamed data chunks
        """
        logger.debug(f"Parsing streaming response from text ({len(response_text)} bytes)")
        
        chunks_found = 0
        for line in response_text.split('\n'):
            # SSE format: "data: {json_content}"
            if line.startswith("data: "):
                data = line[6:]  # Remove "data: " prefix
                if data.strip():
                    chunks_found += 1
                    yield data
            elif line.strip() and not line.startswith(":"):  # Not empty line or comment
                # Plain text chunk (not SSE format)
                chunks_found += 1
                yield line
        
        logger.debug(f"Streaming complete, yielded {chunks_found} chunks")
    
    # === Sandbox Lifecycle Management ===
    async def pause(self) -> None:
        """Pause Sandbox instance
        
        After pausing:
        - Sandbox enters sleep state, retains memory state
        - Stops CPU computation, saves resources
        - Can resume execution via resume()
        
        Raises:
            SandboxOperationError: Raised when pause fails
        """
        try:
            if hasattr(self.sandbox, 'pause'):
                await self.sandbox.pause()
            else:
                # If sandbox doesn't have pause method, use API call
                await self._call_sandbox_api("pause")
            
            self.status = SessionStatus.PAUSED
            
        except Exception as e:
            raise SandboxOperationError(f"Failed to pause sandbox: {str(e)}")
    
    async def resume(self) -> None:
        """Resume Sandbox instance
        
        After resuming:
        - Sandbox recovers from paused state
        - Maintains previous memory state and context
        - Can continue processing requests
        
        Raises:
            SandboxOperationError: Raised when resume fails
        """
        try:
            if hasattr(self.sandbox, 'resume'):
                await self.sandbox.resume()
            else:
                # If sandbox doesn't have resume method, use API call
                await self._call_sandbox_api("resume")
            
            self.status = SessionStatus.ACTIVE
            
        except Exception as e:
            raise SandboxOperationError(f"Failed to resume sandbox: {str(e)}")
    
    async def _call_sandbox_api(self, action: str) -> None:
        """Call Sandbox API to execute operation"""
        # This needs to be implemented based on actual Sandbox API
        # Using mock implementation for now
        pass
    
    # === Session Management ===
    async def ping(self) -> PingResponse:
        """Health check
        
        Returns:
            Health check response
            
        Raises:
            NetworkError: Raised on network error
            InvocationError: Raised when check fails
        """
        try:
            client = await self._get_http_client()
            
            response = await client.get(
                f"{self.host_url}/ping",
                timeout=httpx.Timeout(10.0)
            )
            
            if response.status_code == 200:
                data = response.json()
                return PingResponse(
                    status=data.get("status", "healthy"),
                    message=data.get("message"),
                    timestamp=data.get("timestamp", datetime.now().isoformat())
                )
            else:
                return PingResponse(
                    status=PingStatus.HEALTHY_BUSY,  # Use enum value to represent error state
                    message=f"HTTP {response.status_code}: {response.text}",
                    timestamp=datetime.now().isoformat()
                )
                
        except Exception as e:
            if "connection" in str(e).lower() or "timeout" in str(e).lower():
                raise NetworkError(f"Network error during ping: {str(e)}")
            else:
                raise InvocationError(f"Ping failed: {str(e)}")
    
    async def get_status(self) -> SessionStatus:
        """Get session status
        
        Returns:
            Session status (ACTIVE, PAUSED, INACTIVE, CLOSED, ERROR)
        """
        # Can add actual status check logic
        try:
            # Try ping to confirm status
            ping_response = await self.ping()
            # Support multiple healthy status formats (case insensitive)
            healthy_statuses = ["healthy", "Healthy", "HealthyBusy", "healthybusy"]
            if ping_response.status in healthy_statuses:
                if self.status == SessionStatus.PAUSED:
                    return SessionStatus.PAUSED
                else:
                    return SessionStatus.ACTIVE
            else:
                return SessionStatus.ERROR
        except Exception:
            return SessionStatus.ERROR
    
    async def refresh(self) -> None:
        """Refresh session (reset timeout)"""
        self.last_activity = datetime.now()
        # Can add actual refresh logic, such as sending keepalive signal to Sandbox
    
    async def close(self) -> None:
        """Close session and destroy Sandbox
        
        Execution steps:
        1. Stop Agent service
        2. Destroy Sandbox instance
        3. Release all resources
        4. Update session status to CLOSED
        """
        try:
            # Close HTTP client
            await self._close_http_client()
            
            # Destroy Sandbox instance
            if hasattr(self.sandbox, 'close'):
                await self.sandbox.close()
            elif hasattr(self.sandbox, 'kill'):
                await self.sandbox.kill()
            
            self.status = SessionStatus.CLOSED
            
        except Exception as e:
            self.status = SessionStatus.ERROR
            raise SandboxOperationError(f"Failed to close session: {str(e)}")
    
    # === Properties ===
    @property
    def host_url(self) -> str:
        """Get Sandbox host URL"""
        if not self._host_url:
            if self.sandbox and hasattr(self.sandbox, 'get_host'):
                # Use actual Sandbox API
                host = self.sandbox.get_host(8080)
                self._host_url = f"https://{host}"
            else:
                # Mock URL (for testing)
                self._host_url = f"https://{self.sandbox_id}.sandbox.novita.ai"
        return self._host_url
    
    @property
    def is_active(self) -> bool:
        """Check if session is active"""
        return self.status == SessionStatus.ACTIVE
    
    @property
    def is_paused(self) -> bool:
        """Check if session is paused"""
        return self.status == SessionStatus.PAUSED
    
    @property
    def sandbox_id(self) -> str:
        """Get Sandbox instance ID (also session ID)"""
        if hasattr(self.sandbox, 'id'):
            return self.sandbox.id
        elif hasattr(self.sandbox, 'sandbox_id'):
            return self.sandbox.sandbox_id
        else:
            return f"sandbox-{id(self.sandbox)}"
    
    @property
    def session_id(self) -> str:
        """Get session ID (equivalent to sandbox_id)"""
        return self.sandbox_id
    
    @property
    def runtime_session_id(self) -> str:
        """Get runtime session ID (AWS Agentcore compatible)
        
        This property provides AWS-compatible session identification.
        In most cases, this is the same as sandbox_id, but may differ
        when user provides custom runtimeSessionId.
        """
        return self.sandbox_id
    
    @property
    def age_seconds(self) -> float:
        """Get session age in seconds"""
        return (datetime.now() - self.created_at).total_seconds()
    
    @property
    def idle_seconds(self) -> float:
        """Get session idle time in seconds"""
        return (datetime.now() - self.last_activity).total_seconds()
    
    def __repr__(self) -> str:
        agent_info = f", agent={self.agent_id}" if self.agent_id else ""
        return f"SandboxSession(id={self.sandbox_id}, status={self.status}, template={self.template_id}{agent_info})"