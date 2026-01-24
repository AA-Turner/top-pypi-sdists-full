"""Template generator for A2A utility agents.

This module provides functionality to generate utility agent code from templates.
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
import logging

logger = logging.getLogger(__name__)


class IATPServerTemplateGenerator:
    """Generate utility agent code from Jinja2 templates."""
    
    def __init__(self, templates_dir: Optional[Path] = None):
        """Initialize the template generator.
        
        Args:
            templates_dir: Directory containing the Jinja2 templates
        """
        if templates_dir is None:
            templates_dir = Path(__file__).parent / "templates"
        
        self.templates_dir = templates_dir
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def generate_agent(
        self,
        output_dir: Path,
        agent_name: str,
        agent_id: str,
        mcp_server_name: str,
        mcp_server_url: str,
        mcp_server_description: str,
        mcp_server_capabilities: List[str],
        agent_description: Optional[str] = None,
        agent_version: str = "0.1.0",
        mcp_server_type: str = "streamable-http",
        mcp_server_metadata: Optional[Dict[str, Any]] = None,
        expose_individual_tools: bool = False,
        auth_required: bool = False,
        auth_schemes: Optional[List[str]] = None,
        skill_examples: Optional[List[str]] = None,
        additional_dependencies: Optional[List[str]] = None,
        environment_variables: Optional[List[Dict[str, str]]] = None,
        use_simple_server: bool = True,
        additional_ignores: Optional[List[str]] = None,
        **kwargs
    ) -> Path:
        """Generate a complete utility agent from templates.
        
        Args:
            output_dir: Directory to write the generated agent
            agent_name: Human-readable name of the agent
            agent_id: Unique identifier for the agent
            mcp_server_name: Name of the MCP server
            mcp_server_url: URL or path to the MCP server
            mcp_server_description: Description of the MCP server
            mcp_server_capabilities: List of capabilities provided by the MCP server
            agent_description: Description of the agent (defaults to auto-generated)
            agent_version: Version of the agent
            mcp_server_type: Type of MCP server (stdio, http, etc.)
            mcp_server_metadata: Additional metadata for the MCP server
            expose_individual_tools: Whether to expose individual MCP tools as A2A skills
            auth_required: Whether authentication is required
            auth_schemes: List of authentication schemes if auth is required
            skill_examples: Example prompts for the main skill
            additional_dependencies: Extra Python dependencies
            environment_variables: Environment variables for Dockerfile
            use_simple_server: Whether to use the simplified server.py template
            additional_ignores: Additional patterns to add to .gitignore
            **kwargs: Additional template variables
            
        Returns:
            Path to the generated agency directory
        """
        # Create output directory
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate default values
        if agent_description is None:
            agent_description = f"Utility agent that exposes {mcp_server_name} capabilities via A2A protocol"
        
        if skill_examples is None:
            skill_examples = [
                f"Help me use {mcp_server_name}",
                f"Process this request with {mcp_server_name}",
                "Execute this operation"
            ]
        
        if mcp_server_metadata is None:
            mcp_server_metadata = {}
        
        if additional_dependencies is None:
            additional_dependencies = []
        
        if environment_variables is None:
            environment_variables = []
        
        if additional_ignores is None:
            additional_ignores = []
        
        # Convert agent name to valid Python identifiers
        class_name = ''.join(word.capitalize() for word in agent_name.replace('-', ' ').split())
        package_name = agent_name.lower().replace(' ', '_').replace('-', '_')
        module_name = package_name
        docker_image = f"traia/{agent_id}:latest"
        
        # Extract D402 parameters from kwargs (populated by deploy_utility_agent)
        d402_enabled = kwargs.get("d402_enabled", False)
        d402_contract_address = kwargs.get("d402_contract_address", "")
        d402_operator_private_key = kwargs.get("d402_operator_private_key", "")
        d402_price_usd = kwargs.get("d402_price_usd", "0.01")
        d402_token_symbol = kwargs.get("d402_token_symbol", "USDC")
        d402_token_address = kwargs.get("d402_token_address", "")
        d402_token_decimals = kwargs.get("d402_token_decimals", 6)
        d402_network = kwargs.get("d402_network", "sepolia")
        d402_facilitator_url = kwargs.get("d402_facilitator_url", "http://localhost:7070")
        d402_testing_mode = kwargs.get("d402_testing_mode", "false")
        
        # Prepare template context
        context = {
            "agent_name": agent_name,
            "agent_id": agent_id,
            "agent_description": agent_description,
            "agent_version": agent_version,
            "mcp_server_name": mcp_server_name,
            "mcp_server_url": mcp_server_url,
            "mcp_server_description": mcp_server_description,
            "mcp_server_type": mcp_server_type,
            "mcp_server_capabilities": mcp_server_capabilities,
            "mcp_server_metadata": mcp_server_metadata,
            "expose_individual_tools": expose_individual_tools,
            "auth_required": auth_required,
            "auth_schemes": auth_schemes or [],
            "skill_examples": skill_examples,
            "class_name": class_name,
            "package_name": package_name,
            "module_name": module_name,
            "docker_image": docker_image,
            "additional_dependencies": additional_dependencies,
            "environment_variables": environment_variables,
            "additional_ignores": additional_ignores,
            "use_uv_lock": False,  # Will be true after first uv sync
            # D402 payment configuration
            "d402_enabled": d402_enabled,
            "d402_contract_address": d402_contract_address,
            "d402_operator_private_key": d402_operator_private_key,
            "d402_price_usd": d402_price_usd,
            "d402_token_symbol": d402_token_symbol,
            "d402_token_address": d402_token_address,
            "d402_token_decimals": d402_token_decimals,
            "d402_network": d402_network,
            "d402_facilitator_url": d402_facilitator_url,
            "d402_testing_mode": d402_testing_mode,
            **kwargs
        }
        
        # Generate files
        files_to_generate = []
        
        # Common files for both approaches
        common_files = [
            ("agent_config.json.j2", "agent_config.json"),
            ("pyproject.toml.j2", "pyproject.toml"),
            ("Dockerfile.j2", "Dockerfile"),
            ("README.md.j2", "README.md"),
            ("docker-compose.yml.j2", "docker-compose.yml"),
            ("env.example.j2", ".env.example"),
            ("gitignore.j2", ".gitignore"),
            (".dockerignore.j2", ".dockerignore"),
            ("run_local_docker.sh.j2", "run_local_docker.sh"),
        ]
        
        if use_simple_server:
            # Simple single-file approach
            files_to_generate = [
                ("server.py.j2", "server.py"),
            ] + common_files
        else:
            # Modular approach with separate files
            # Create package directory
            pkg_dir = output_dir / package_name
            pkg_dir.mkdir(exist_ok=True)
            
            files_to_generate = [
                ("agent.py.j2", f"{package_name}/agent.py"),
                ("agent_executor.py.j2", f"{package_name}/agent_executor.py"),
                ("__main__.py.j2", f"{package_name}/__main__.py"),
            ] + common_files
            
            # Create __init__.py
            (output_dir / package_name / "__init__.py").write_text("")
        
        # Render and write templates
        for template_name, output_name in files_to_generate:
            try:
                template = self.env.get_template(template_name)
                content = template.render(context)
                output_path = output_dir / output_name
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(content)
                logger.info(f"Generated {output_path}")
                
                # Make run_local_docker.sh executable
                if output_name == "run_local_docker.sh":
                    output_path.chmod(0o755)
                    logger.info(f"Made {output_path} executable")
            except Exception as e:
                logger.error(f"Error generating {output_name} from {template_name}: {e}")
                raise
        
        # # Copy mcp_agent_template.py
        # self._copy_mcp_agent_template(output_dir)
        
        logger.info(f"Successfully generated utility agent at {output_dir}")
        return output_dir
    
    # def _copy_mcp_agent_template(self, output_dir: Path):
    #     """Copy the mcp_agent_template.py file to the generated agent.
        
    #     Args:
    #         output_dir: Output directory for the agent
    #     """
    #     # Find the mcp_agent_template.py file
    #     mcp_template_path = Path(__file__).parent.parent / "mcp" / "mcp_agent_template.py"
    #     agent_adapter_path = Path(__file__).parent.parent / "mcp" / "traia_mcp_adapter.py"
        
    #     if mcp_template_path.exists():
    #         # Copy to output directory
    #         dest_path_one = output_dir / "mcp_agent_template.py"
    #         dest_path_two = output_dir / "traia_mcp_adapter.py"
    #         shutil.copy2(mcp_template_path, dest_path_one)
    #         shutil.copy2(agent_adapter_path, dest_path_two)
    #         logger.info(f"Copied mcp_agent_template.py to {dest_path_one}")
    #         logger.info(f"Copied traia_mcp_adapter.py to {dest_path_two}")
    #     else:
    #         logger.warning(f"Could not find mcp_agent_template.py at {mcp_template_path}")
    #         logger.warning(f"Could not find traia_mcp_adapter.py at {agent_adapter_path}")
    
    def list_templates(self) -> List[str]:
        """List available templates.
        
        Returns:
            List of template file names
        """
        return [f.name for f in self.templates_dir.glob("*.j2")] 