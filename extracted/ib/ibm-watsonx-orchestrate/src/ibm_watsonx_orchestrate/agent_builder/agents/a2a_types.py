from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class AgentCard(BaseModel):
    """
    Agent Card for A2A protocol (simplified for WxO integration).
    Only includes fields needed for conversion to WxO external agent format.
    """
    model_config = ConfigDict(
        extra='allow',
    )
    
    name: str = Field(description="Agent name")
    description: str = Field(description="Agent description")
    url: str = Field(description="Base URL of the agent")

    def convert_to_wxo_external_agent_dict(
        self,
        agent_name: Optional[str] = None,
        app_id: Optional[str] = None,
        control_plane_only: bool = True,
    ) -> Dict[str, Any]:
        """
        Convert AgentCard to WxO external agent specification dictionary.
        
        Args:
            agent_name: Override agent name (defaults to card name)
            app_id: Connection app_id for authentication (optional)
            control_plane_only: Whether the agent is registered for control plane only (default: True)
            
        Returns:
            Dictionary matching WxO external agent YAML structure
        """
        
        final_name = agent_name or self.name.lower().replace(" ", "_")
        cpo = control_plane_only if control_plane_only is not None else True
        
        # Build the minimal external agent spec dictionary
        spec = {
            "spec_version": "v1",
            "kind": "external",
            "name": final_name,
            "title": self.name,
            "provider": "external_chat/A2A/0.3.0",  # A2A protocol version
            "description": self.description,
            "api_url": self.url,
            "config": {
                "control_plane_only": cpo,
            },
        }
        
        # Add app_id if provided (indicates authenticated agent)
        if app_id:
            spec["app_id"] = app_id
        
        return spec
