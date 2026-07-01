"""Docker utility functions for running generated utility agents locally."""

import logging
import subprocess
import os
from pathlib import Path
from typing import Dict, Any, Optional
import docker
import httpx
import asyncio

logger = logging.getLogger(__name__)


class LocalDockerRunner:
    """Run generated utility agents locally using their Docker configuration."""
    
    def __init__(self):
        """Initialize Docker client."""
        try:
            self.client = docker.from_env()
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            raise RuntimeError("Docker is not available. Please ensure Docker is installed and running.")
    
    async def run_agent_docker(
        self, 
        agent_path: Path,
        port: int = 8000,
        environment: Optional[Dict[str, str]] = None,
        detached: bool = True
    ) -> Dict[str, Any]:
        """Run a generated utility agent using its Docker configuration.
        
        Args:
            agent_path: Path to the generated agent directory
            port: Port to expose (default: 8000)
            environment: Additional environment variables
            detached: Whether to run in detached mode
            
        Returns:
            Dict with deployment information
        """
        agent_path = Path(agent_path)
        
        # Verify the agent directory has required files
        required_files = ["Dockerfile", "docker-compose.yml", "pyproject.toml"]
        for file in required_files:
            if not (agent_path / file).exists():
                raise FileNotFoundError(f"Required file {file} not found in {agent_path}")
        
        # Create .env file if it doesn't exist
        env_file = agent_path / ".env"
        if not env_file.exists():
            self._create_env_file(agent_path, port, environment)
        
        # Use docker-compose to run the agent
        compose_file = agent_path / "docker-compose.yml"
        
        try:
            # Build the image
            logger.info(f"Building Docker image for agent at {agent_path}")
            subprocess.run(
                ["docker-compose", "-f", str(compose_file), "build"],
                cwd=str(agent_path),
                check=True,
                capture_output=True,
                text=True
            )
            
            # Run the container
            logger.info(f"Starting container on port {port}")
            cmd = ["docker-compose", "-f", str(compose_file), "up"]
            if detached:
                cmd.append("-d")
                
            result = subprocess.run(
                cmd,
                cwd=str(agent_path),
                check=True,
                capture_output=True,
                text=True,
                env={**os.environ, "PORT": str(port)}
            )
            
            # Get container info
            container_name = self._get_container_name(agent_path)
            
            # Wait for the service to be ready
            if detached:
                await self._wait_for_service(port)
            
            return {
                "success": True,
                "container_name": container_name,
                "port": port,
                "base_url": f"http://localhost:{port}",
                "iatp_endpoint": f"http://localhost:{port}/a2a",
                "health_endpoint": f"http://localhost:{port}/health",
                "logs_command": f"docker logs -f {container_name}",
                "stop_command": f"docker-compose -f {compose_file} down"
            }
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Docker command failed: {e.stderr}")
            raise RuntimeError(f"Failed to run agent: {e.stderr}")
        except Exception as e:
            logger.error(f"Error running agent: {e}")
            raise
    
    async def stop_agent_docker(self, agent_path: Path) -> bool:
        """Stop a running agent.
        
        Args:
            agent_path: Path to the agent directory
            
        Returns:
            True if stopped successfully
        """
        agent_path = Path(agent_path)
        compose_file = agent_path / "docker-compose.yml"
        
        if not compose_file.exists():
            raise FileNotFoundError(f"docker-compose.yml not found in {agent_path}")
        
        try:
            subprocess.run(
                ["docker-compose", "-f", str(compose_file), "down"],
                cwd=str(agent_path),
                check=True,
                capture_output=True,
                text=True
            )
            logger.info(f"Stopped agent at {agent_path}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to stop agent: {e.stderr}")
            return False
    
    def get_agent_logs(self, agent_path: Path, tail: int = 100) -> str:
        """Get logs from a running agent.
        
        Args:
            agent_path: Path to the agent directory
            tail: Number of lines to return
            
        Returns:
            Log output as string
        """
        container_name = self._get_container_name(agent_path)
        
        try:
            container = self.client.containers.get(container_name)
            return container.logs(tail=tail).decode('utf-8')
        except docker.errors.NotFound:
            return f"Container {container_name} not found"
        except Exception as e:
            return f"Error getting logs: {e}"
    
    def _create_env_file(self, agent_path: Path, port: int, environment: Optional[Dict[str, str]] = None):
        """Create a .env file for the agent."""
        env_content = [
            f"PORT={port}",
            "HOST=0.0.0.0",
            "LOG_LEVEL=INFO",
            ""
        ]
        
        # Add custom environment variables
        if environment:
            for key, value in environment.items():
                env_content.append(f"{key}={value}")
        
        env_file = agent_path / ".env"
        env_file.write_text("\n".join(env_content))
        logger.info(f"Created .env file at {env_file}")
    
    def _get_container_name(self, agent_path: Path) -> str:
        """Get the container name from the agent directory name."""
        return f"{agent_path.name}-local"
    
    async def _wait_for_service(self, port: int, timeout: int = 30):
        """Wait for the service to be ready."""
        start_time = asyncio.get_event_loop().time()
        
        async with httpx.AsyncClient() as client:
            while asyncio.get_event_loop().time() - start_time < timeout:
                try:
                    response = await client.get(f"http://localhost:{port}/health")
                    if response.status_code == 200:
                        logger.info(f"Service is ready on port {port}")
                        return
                except Exception:
                    pass
                await asyncio.sleep(1)
        
        logger.warning(f"Service did not become ready within {timeout} seconds")


def run_generated_agent_locally(
    agent_path: str,
    port: int = 8000,
    environment: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Convenience function to run a generated agent locally.
    
    This is a synchronous wrapper around the async functionality.
    
    Args:
        agent_path: Path to the generated agent directory
        port: Port to expose
        environment: Additional environment variables
        
    Returns:
        Dict with deployment information
    """
    runner = LocalDockerRunner()
    return asyncio.run(runner.run_agent_docker(
        Path(agent_path),
        port=port,
        environment=environment
    ))


def use_run_local_docker_script(agent_path: str) -> subprocess.CompletedProcess:
    """Run the agent using its generated run_local_docker.sh script.
    
    This is the simplest way to run a generated agent locally,
    as it uses the script generated from templates.
    
    Args:
        agent_path: Path to the generated agent directory
        
    Returns:
        CompletedProcess result
    """
    agent_path = Path(agent_path)
    script_path = agent_path / "run_local_docker.sh"
    
    if not script_path.exists():
        raise FileNotFoundError(f"run_local_docker.sh not found in {agent_path}")
    
    # Make sure the script is executable
    script_path.chmod(0o755)
    
    # Run the script
    return subprocess.run(
        ["./run_local_docker.sh"],
        cwd=str(agent_path),
        check=True
    ) 