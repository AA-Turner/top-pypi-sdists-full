"""
Agent ID Utilities

Utilities for parsing and handling Agent IDs.
"""

from typing import Tuple
from .exceptions import ValidationException


def extract_agent_id_from_arn(agent_id_or_arn: str) -> str:
    """Extract agent ID from ARN or direct agent ID
    
    Args:
        agent_id_or_arn: Agent ID or ARN format
        
    Returns:
        Clean agent ID
        
    Examples:
        >>> extract_agent_id_from_arn("my_agent-abc123")
        'my_agent-abc123'
        >>> extract_agent_id_from_arn("arn:aws:bedrock:us-east-1:123456:agent/my_agent-abc123")
        'my_agent-abc123'
    """
    if agent_id_or_arn.startswith("arn:"):
        # ARN format: arn:aws:bedrock:region:account-id:agent/agent-id
        # Extract the last part after '/'
        return agent_id_or_arn.split("/")[-1]
    return agent_id_or_arn


def extract_template_id_from_agent_id(agent_id: str) -> str:
    """Extract template_id from agent_id
    
    Agent ID format: {agent_name_with_underscores}-{template_id}
    
    Args:
        agent_id: Agent ID in format agent_name-template_id
        
    Returns:
        Template ID
        
    Raises:
        ValidationException: Invalid agent_id format
        
    Examples:
        >>> extract_template_id_from_agent_id("my_agent-abc123")
        'abc123'
        >>> extract_template_id_from_agent_id("customer_service_agent-tpl_abc456")
        'tpl_abc456'
    """
    # agent_id format: {agent_name}-{template_id}
    # Find the last hyphen to separate agent_name and template_id
    parts = agent_id.rsplit("-", 1)
    if len(parts) != 2:
        raise ValidationException(
            f"Invalid agentId format. Expected 'agent_name-template_id', got: {agent_id}"
        )
    
    template_id = parts[1]
    
    # Validate template_id is not empty
    if not template_id:
        raise ValidationException(
            f"Invalid agentId format. Template ID cannot be empty, got: {agent_id}"
        )
    
    return template_id


def extract_agent_name_from_agent_id(agent_id: str) -> str:
    """Extract agent name from agent_id
    
    Args:
        agent_id: Agent ID in format agent_name-template_id
        
    Returns:
        Agent name (with underscores)
        
    Raises:
        ValidationException: Invalid agent_id format
        
    Examples:
        >>> extract_agent_name_from_agent_id("my_agent-tpl_123")
        'my_agent'
        >>> extract_agent_name_from_agent_id("customer_service_agent-tpl_abc456")
        'customer_service_agent'
    """
    parts = agent_id.rsplit("-", 1)
    if len(parts) != 2:
        raise ValidationException(
            f"Invalid agentId format. Expected 'agent_name-template_id', got: {agent_id}"
        )
    
    return parts[0]


def normalize_agent_name(agent_name: str) -> str:
    """Normalize agent name by replacing hyphens with underscores
    
    This is used when generating agent_id from agent name and template_id
    to avoid multiple hyphens that would make parsing difficult.
    
    Args:
        agent_name: Original agent name (may contain hyphens)
        
    Returns:
        Normalized agent name (hyphens replaced with underscores)
        
    Examples:
        >>> normalize_agent_name("my-agent")
        'my_agent'
        >>> normalize_agent_name("customer-service-agent")
        'customer_service_agent'
        >>> normalize_agent_name("already_normalized")
        'already_normalized'
    """
    return agent_name.replace("-", "_")


def create_agent_id(agent_name: str, template_id: str) -> str:
    """Create agent_id from agent name and template_id
    
    Args:
        agent_name: Agent name (will be normalized)
        template_id: Template ID (any non-empty string)
        
    Returns:
        Agent ID in format: normalized_agent_name-template_id
        
    Raises:
        ValidationException: Invalid template_id (empty)
        
    Examples:
        >>> create_agent_id("my-agent", "abc123")
        'my_agent-abc123'
        >>> create_agent_id("customer-service", "tpl_abc456")
        'customer_service-tpl_abc456'
    """
    # Validate template_id is not empty
    if not template_id or not template_id.strip():
        raise ValidationException(
            "Template ID cannot be empty"
        )
    
    # Normalize agent name (replace hyphens with underscores)
    normalized_name = normalize_agent_name(agent_name)
    
    return f"{normalized_name}-{template_id}"


def parse_agent_id(agent_id_or_arn: str) -> Tuple[str, str]:
    """Parse agent ID or ARN to extract agent name and template_id
    
    Args:
        agent_id_or_arn: Agent ID or ARN format
        
    Returns:
        Tuple of (agent_name, template_id)
        
    Raises:
        ValidationException: Invalid format
        
    Examples:
        >>> parse_agent_id("my_agent-abc123")
        ('my_agent', 'abc123')
        >>> parse_agent_id("arn:aws:bedrock:us-east-1:123456:agent/my_agent-xyz789")
        ('my_agent', 'xyz789')
    """
    # First extract agent_id from ARN if needed
    agent_id = extract_agent_id_from_arn(agent_id_or_arn)
    
    # Then extract agent_name and template_id
    agent_name = extract_agent_name_from_agent_id(agent_id)
    template_id = extract_template_id_from_agent_id(agent_id)
    
    return agent_name, template_id

