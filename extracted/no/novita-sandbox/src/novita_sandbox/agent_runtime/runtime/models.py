# Novita Agent Runtime - Data Models
# Copyright (c) 2024 Novita
# Licensed under the MIT License

"""Data models for Novita Agent Runtime."""

import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Literal, Union
from pydantic import BaseModel, Field, field_validator


class DeploymentPhase(str, Enum):
    """Deployment phase enumeration"""
    PENDING = "pending"
    BUILDING = "building" 
    DEPLOYED = "deployed"
    FAILED = "failed"


class PingStatus(str, Enum):
    """Health status enumeration"""
    HEALTHY = "Healthy"
    HEALTHY_BUSY = "HealthyBusy"


class AgentMetadata(BaseModel):
    """Agent metadata"""
    name: str = Field(..., description="Agent name, must be lowercase letters, numbers and hyphens")
    version: str = Field(..., description="Agent version") 
    author: str = Field(..., description="Author email (required)")
    description: Optional[str] = Field(None, description="Agent description")
    created: Optional[str] = Field(None, description="Creation time (ISO 8601 format)")


class RuntimeSpec(BaseModel):
    """Runtime specification configuration"""
    timeout: Optional[int] = Field(None, ge=1, le=3600, description="Startup timeout in seconds (1-3600)")
    memory_limit: Optional[str] = Field(None, description="Memory limit, e.g. '512Mi', '1Gi'")
    cpu_limit: Optional[str] = Field(None, description="CPU limit, e.g. '1', '1000m'")


class SandboxSpec(BaseModel):
    """Sandbox specification configuration"""
    template_id: Optional[str] = Field(None, description="Template ID after deployment")


class AgentSpec(BaseModel):
    """Agent specification configuration"""
    entrypoint: str = Field(..., pattern=r".*\.py$", description="Python entry file, must be .py file")
    runtime: Optional[RuntimeSpec] = Field(None, description="Runtime configuration")
    sandbox: Optional[SandboxSpec] = Field(None, description="Sandbox configuration")


class AgentStatus(BaseModel):
    """Agent status information (maintained by system)"""
    phase: Optional[DeploymentPhase] = Field(None, description="Current deployment phase")
    template_id: Optional[str] = Field(None, description="Actual template ID after successful build")
    last_deployed: Optional[str] = Field(None, description="Last deployment time")
    build_id: Optional[str] = Field(None, description="Unique identifier for deployment")


class AgentConfig(BaseModel):
    """Agent configuration class - Kubernetes-style configuration structure"""
    apiVersion: Literal["v1"] = Field("v1", description="API version")
    kind: Literal["Agent"] = Field("Agent", description="Resource type")
    metadata: AgentMetadata = Field(..., description="Agent metadata")
    spec: AgentSpec = Field(..., description="Agent specification configuration")
    status: Optional[AgentStatus] = Field(None, description="Agent status information (maintained by system)")


class RuntimeConfig(BaseModel):
    """Runtime configuration class - for Agent Runtime server configuration"""
    host: str = "0.0.0.0"
    port: int = 8080
    debug: bool = False
    timeout: int = 300
    max_request_size: int = 1024 * 1024  # 1MB
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])
    enable_metrics: bool = True
    enable_middleware: bool = True


class InvocationResponse(BaseModel):
    """Invocation response model"""
    result: Any
    status: str = "success"
    duration: float
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class PingResponse(BaseModel):
    """Health check response model"""
    status: PingStatus = PingStatus.HEALTHY
    message: Optional[str] = None
    timestamp: Optional[str] = None
    
    @field_validator('status', mode='before')
    @classmethod
    def normalize_status(cls, v):
        """Normalize status value, supports string input"""
        if isinstance(v, PingStatus):
            return v
        
        if isinstance(v, str):
            # Handle common case variations
            status_lower = v.lower()
            if status_lower in ['healthy', 'ok', 'up']:
                return PingStatus.HEALTHY
            elif status_lower in ['healthybusy', 'busy', 'working']:
                return PingStatus.HEALTHY_BUSY
            else:
                # Try direct enum value matching
                for enum_val in PingStatus:
                    if enum_val.value.lower() == status_lower:
                        return enum_val
        
        # Default to healthy status
        return PingStatus.HEALTHY
