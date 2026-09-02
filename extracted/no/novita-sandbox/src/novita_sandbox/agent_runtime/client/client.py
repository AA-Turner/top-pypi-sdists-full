"""
Agent Runtime Client

Client for backend developers to manage Sandbox sessions and Agent invocations
"""

import asyncio
import json
from typing import Any, AsyncIterator, Dict, List, Optional, Union

from novita_sandbox.core import AsyncSandbox  # Import existing async Sandbox functionality
from .auth import AuthManager
from .exceptions import (
    AuthenticationError,
    InvocationError,
    SessionNotFoundError,
    SandboxCreationError,
    TemplateNotFoundError,
    ValidationException,
    ResourceNotFoundException
)
from .models import (
    AgentTemplate,
    ClientConfig,
    SandboxConfig
)
from .session import SandboxSession
from .template import TemplateManager
from .agent_id_utils import (
    extract_agent_id_from_arn,
    extract_template_id_from_agent_id
)


class AgentRuntimeClient:
    """Agent Runtime Client"""
    
    def __init__(
        self,
        api_key: Optional[str] = None
    ):
        """Initialize the client
        
        Args:
            api_key: API key, if not provided it will be read from environment variable NOVITA_API_KEY
            
        Environment Variables:
            NOVITA_API_KEY: API key
            
        Raises:
            AuthenticationError: Raised when API Key is not provided and environment variable does not exist
        """
        # Use default configuration (simplified)
        self.config = ClientConfig(timeout=300)
        
        # Initialize authentication manager
        self.auth_manager = AuthManager(api_key)
        
        # Initialize template manager (only pass auth_manager)
        self.template_manager = TemplateManager(self.auth_manager)
        
        # Session management (internal sandbox sessions)
        self._sessions: Dict[str, SandboxSession] = {}
        
        # Runtime session mapping (user-provided runtimeSessionId -> internal sandbox_id)
        self._runtime_sessions: Dict[str, SandboxSession] = {}
        self._session_mappings: Dict[str, str] = {}  # runtimeSessionId -> sandbox_id
        
        self._closed = False
    
    # === AWS Agentcore Compatible Methods ===
    async def invoke_agent_runtime(
        self,
        agentId: str,
        payload: bytes,
        runtimeSessionId: Optional[str] = None,
        timeout: Optional[int] = None,
        envVars: Optional[Dict[str, str]] = None
    ) -> Union[Dict[str, Any], AsyncIterator[Dict[str, Any]]]:
        """Invoke agent runtime (AWS Agentcore compatible - auto-detect streaming)
        
        This method automatically detects whether the Agent returns streaming or non-streaming
        response based on the Agent's implementation. The response type is determined by the
        Agent application's return type:
        - If Agent returns generator/async generator -> Returns AsyncIterator (streaming)
        - If Agent returns dict/object -> Returns Dict (non-streaming)
        
        Args:
            agentId: Agent identifier (format: agent_name-template_id or ARN)
            payload: Binary payload for the agent
            runtimeSessionId: Optional user-provided session ID (UUID)
            timeout: Optional timeout in seconds
            envVars: Optional environment variables for the sandbox
            
        Returns:
            Dict[str, Any] for non-streaming responses
            AsyncIterator[Dict[str, Any]] for streaming responses (auto-detected)
            
        Raises:
            ValidationException: Invalid agentId format or parameters
            ResourceNotFoundException: Agent or session not found
            InvocationError: Agent invocation failed
        """
        if self._closed:
            raise RuntimeError("Client is closed")
            
        # Extract agent_id and template_id from agentId
        agent_id = self._extract_agent_id(agentId)
        template_id = self._extract_template_id(agent_id)
        
        # Get or create session
        session, session_id = await self._get_or_create_session(
            template_id=template_id, 
            runtime_session_id=runtimeSessionId,
            timeout=timeout or self.config.timeout,
            env_vars=envVars
        )
        
        try:
            # Parse payload intelligently
            if payload:
                payload_str = payload.decode('utf-8')
                try:
                    # Try to parse as JSON - preserve structure
                    request_data = json.loads(payload_str)
                    # Invoke with dict to preserve all fields
                    result = await session.invoke(request_data)
                except json.JSONDecodeError:
                    # Not JSON, treat as plain text
                    result = await session.invoke(payload_str)
            else:
                # Empty payload
                result = await session.invoke({})
            
            # Check if result is an async iterator (streaming response)
            import inspect
            if inspect.isasyncgen(result):
                # Streaming response - wrap chunks with metadata
                return self._wrap_streaming_response(result, session_id, agentId)
            else:
                # Non-streaming response - return dict with metadata
                return {
                    "response": result,
                    "runtimeSessionId": session_id,
                    "status": "success",
                    "agentId": agentId
                }
            
        except Exception as e:
            raise InvocationError(f"Agent invocation failed: {str(e)}")
    
    async def _wrap_streaming_response(
        self,
        stream: AsyncIterator[str],
        session_id: str,
        agent_id: str
    ) -> AsyncIterator[Dict[str, Any]]:
        """Wrap streaming response with metadata
        
        Args:
            stream: Async iterator from agent
            session_id: Runtime session ID
            agent_id: Agent ID
            
        Yields:
            Dict containing chunk data and metadata
        """
        async for chunk in stream:
            yield {
                "chunk": chunk,
                "runtimeSessionId": session_id,
                "agentId": agent_id
            }
    
    # === Internal Helper Methods ===
    def _extract_agent_id(self, agent_id_or_arn: str) -> str:
        """Extract agent ID from ARN or direct agent ID
        
        Args:
            agent_id_or_arn: Agent ID or ARN format
            
        Returns:
            Clean agent ID
        """
        return extract_agent_id_from_arn(agent_id_or_arn)
    
    def _extract_template_id(self, agent_id: str) -> str:
        """Extract template_id from agent_id (format: agent_name-template_id)
        
        Args:
            agent_id: Agent ID in format agent_name-template_id
            
        Returns:
            Template ID
            
        Raises:
            ValidationException: Invalid agent_id format
        """
        return extract_template_id_from_agent_id(agent_id)
    
    async def _get_or_create_session(
        self,
        template_id: str,
        runtime_session_id: Optional[str] = None,
        timeout: int = 300,
        env_vars: Optional[Dict[str, str]] = None
    ) -> tuple[SandboxSession, str]:
        """Get existing session or create new session
        
        Args:
            template_id: Template ID
            runtime_session_id: Optional user-provided session ID
            timeout: Session timeout
            env_vars: Optional environment variables for the sandbox
            
        Returns:
            Tuple of (SandboxSession, effective_runtime_session_id)
        """
        if runtime_session_id:
            # User provided runtimeSessionId, check if session exists
            if runtime_session_id in self._runtime_sessions:
                session = self._runtime_sessions[runtime_session_id]
                return session, runtime_session_id
            
            # Create new session with user-provided runtimeSessionId
            session = await self._create_internal_session(
                template_id=template_id,
                timeout=timeout,
                env_vars=env_vars
            )
            
            # Map user runtimeSessionId to internal sandbox_id
            self._runtime_sessions[runtime_session_id] = session
            self._session_mappings[runtime_session_id] = session.sandbox_id
            
            return session, runtime_session_id
        
        else:
            # No runtimeSessionId provided, create new session and use sandbox_id as runtimeSessionId
            session = await self._create_internal_session(
                template_id=template_id,
                timeout=timeout,
                env_vars=env_vars
            )
            
            # Use sandbox_id as runtimeSessionId
            runtime_session_id = session.sandbox_id
            self._runtime_sessions[runtime_session_id] = session
            
            return session, runtime_session_id
    
    async def _create_internal_session(
        self,
        template_id: str,
        timeout: int,
        env_vars: Optional[Dict[str, str]] = None
    ) -> SandboxSession:
        """Create internal sandbox session
        
        Args:
            template_id: Template ID
            timeout: Session timeout in seconds
            env_vars: Optional environment variables for the sandbox
            
        Returns:
            SandboxSession object
            
        Raises:
            SandboxCreationError: Raised when creation fails
            TemplateNotFoundError: Raised when template does not exist
        """
        try:
            # Get template to retrieve metadata
            template = await self.template_manager.get_template(template_id)
            
            # Extract entrypoint from template metadata
            startup_cmd = None
            if template.metadata:
                # Template metadata contains AgentConfig from CLI
                agentRuntimeMetadataJson = template.metadata.get('agent_runtime', "")
                agentRuntimeMetadata = json.loads(agentRuntimeMetadataJson)
                spec = agentRuntimeMetadata.get('spec', {})
                entrypoint = spec.get('entrypoint', "")

                if entrypoint:
                    # Generate startup command: cd /app && sudo -E python ${entrypoint}
                    startup_cmd = f"cd /app && sudo -E python {entrypoint}"
            
            # Create sandbox configuration with provided parameters
            sandbox_config = SandboxConfig(
                env_vars=env_vars or {},
                startup_cmd=startup_cmd
            )
            
            # Create Sandbox instance
            sandbox = await self._create_sandbox_instance(
                template_id=template_id,
                timeout_seconds=timeout,
                config=sandbox_config,
            )
            # Create session
            session = SandboxSession(
                template_id=template_id,
                sandbox=sandbox,
                client=self
            )

            if startup_cmd:
                await self._wait_for_service_ready(session)
            
            # Register session in internal tracking
            self._sessions[session.sandbox_id] = session
            
            return session
            
        except TemplateNotFoundError as e:
            # Convert TemplateNotFoundError to AWS-compatible ResourceNotFoundException
            raise ResourceNotFoundException(f"Agent template not found: {template_id}")
        except ResourceNotFoundException:
            raise
        except AuthenticationError:
            raise
        except Exception as e:
            raise SandboxCreationError(f"Failed to create sandbox session: {str(e)}")
    
    async def _create_sandbox_instance(
        self,
        template_id: str,
        timeout_seconds: int,
        config: SandboxConfig,
    ) -> AsyncSandbox:
        """Create Sandbox instance"""
        try:
            sandbox = await AsyncSandbox.create(
                template=template_id,
                timeout=timeout_seconds,
                metadata={"created_by": "agent_runtime_client"},
                envs=config.env_vars,
                api_key=self.auth_manager.api_key,
                # Secure mode, default is True
                secure=True,
            )

            if config.startup_cmd:
                # Run startup command in background to avoid blocking
                # (useful for starting HTTP servers or long-running services)
                await sandbox.commands.run(config.startup_cmd, background=True)

            
            return sandbox
            
        except Exception as e:
            raise SandboxCreationError(f"Failed to create sandbox instance: {str(e)}")
    
    async def _wait_for_service_ready(
        self, 
        session: SandboxSession, 
        timeout: int = 60,
        interval: float = 3.0
    ) -> None:
        """Wait for service to be ready by polling ping endpoint
        
        Args:
            session: Sandbox session to check
            timeout: Maximum wait time in seconds (default: 30)
            interval: Polling interval in seconds (default: 1.0)
            
        Raises:
            SandboxCreationError: Raised when service doesn't become ready within timeout
        """
        import time
        start_time = time.time()
        
        while True:
            # Check timeout
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                raise SandboxCreationError(
                    f"Service failed to start within {timeout} seconds"
                )
            
            try:
                # Try to ping the service
                ping_response = await session.ping()
                
                # Check if service is healthy
                if ping_response.status in ["healthy", "Healthy"]:
                    # Service is ready
                    return
                    
            except Exception:
                # Ignore errors and continue polling
                pass
            
            # Wait before next attempt
            await asyncio.sleep(interval)
    
    # === Legacy Methods (maintained for backward compatibility) ===
    async def get_session(self, sandbox_id: str) -> Optional[SandboxSession]:
        """Get existing session by internal sandbox_id
        
        Args:
            sandbox_id: Internal sandbox ID
            
        Returns:
            Session object, or None if not found
        """
        return self._sessions.get(sandbox_id)
    
    async def get_session_by_runtime_id(self, runtime_session_id: str) -> Optional[SandboxSession]:
        """Get existing session by runtimeSessionId
        
        Args:
            runtime_session_id: User-facing runtime session ID
            
        Returns:
            Session object, or None if not found
        """
        return self._runtime_sessions.get(runtime_session_id)
    
    async def list_sessions(self) -> List[SandboxSession]:
        """List all active sessions
        
        Returns:
            List of sessions
        """
        return list(self._sessions.values())
    
    async def close_session(self, runtime_session_id: str) -> None:
        """Close specified session by runtimeSessionId
        
        Args:
            runtime_session_id: Runtime session ID
            
        Raises:
            SessionNotFoundError: Raised when session does not exist
        """
        session = self._runtime_sessions.get(runtime_session_id)
        if not session:
            raise SessionNotFoundError(f"Session {runtime_session_id} not found")
        
        try:
            await session.close()
        finally:
            # Remove from both mappings
            self._runtime_sessions.pop(runtime_session_id, None)
            if runtime_session_id in self._session_mappings:
                sandbox_id = self._session_mappings[runtime_session_id]
                self._sessions.pop(sandbox_id, None)
                self._session_mappings.pop(runtime_session_id, None)
    
    async def close_session_by_sandbox_id(self, sandbox_id: str) -> None:
        """Close specified session by internal sandbox_id (legacy method)
        
        Args:
            sandbox_id: Internal sandbox ID
            
        Raises:
            SessionNotFoundError: Raised when session does not exist
        """
        session = self._sessions.get(sandbox_id)
        if not session:
            raise SessionNotFoundError(f"Session {sandbox_id} not found")
        
        try:
            await session.close()
        finally:
            # Remove from all mappings
            self._sessions.pop(sandbox_id, None)
            # Find and remove runtime session mappings
            for runtime_id, mapped_sandbox_id in list(self._session_mappings.items()):
                if mapped_sandbox_id == sandbox_id:
                    self._runtime_sessions.pop(runtime_id, None)
                    self._session_mappings.pop(runtime_id, None)
    
    async def close_all_sessions(self) -> None:
        """Close all sessions"""
        sessions = list(self._sessions.values())
        self._sessions.clear()
        self._runtime_sessions.clear()
        self._session_mappings.clear()
        
        # Close all sessions concurrently
        if sessions:
            await asyncio.gather(
                *[session.close() for session in sessions],
                return_exceptions=True
            )
    
    # === Template Management ===
    async def list_templates(
        self, 
        with_metadata: bool = False
    ) -> List[AgentTemplate]:
        """List available Agent templates
        
        Args:
            with_metadata: Whether to include metadata in response
        
        Returns:
            List of templates
        """
        return await self.template_manager.list_templates(with_metadata=with_metadata)
    
    async def get_template(self, template_id: str) -> AgentTemplate:
        """Get specific template information
        
        Args:
            template_id: Template ID
            
        Returns:
            Template object
            
        Raises:
            TemplateNotFoundError: Raised when template does not exist
        """
        return await self.template_manager.get_template(template_id)
    
    # === Context Manager Support ===
    async def __aenter__(self) -> "AgentRuntimeClient":
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit"""
        await self.close()
    
    async def close(self) -> None:
        """Close client and clean up resources"""
        if self._closed:
            return
        
        self._closed = True
        
        # Close all sessions
        await self.close_all_sessions()
        
        # Close template manager
        await self.template_manager.close()
    
    def __repr__(self) -> str:
        return f"AgentRuntimeClient(sessions={len(self._sessions)}, runtime_sessions={len(self._runtime_sessions)}, closed={self._closed})"