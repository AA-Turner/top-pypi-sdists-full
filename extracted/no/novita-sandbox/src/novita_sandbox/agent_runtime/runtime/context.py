# Novita Agent Runtime - Request Context Management
# Copyright (c) 2024 Novita
# Licensed under the MIT License

"""Request context management for Novita Agent Runtime."""

import uuid
from typing import Any, Dict, Optional
from contextvars import ContextVar
from pydantic import BaseModel, Field


class RequestContext(BaseModel):
    """Request context model"""
    
    sandbox_id: Optional[str] = None
    request_id: Optional[str] = None
    headers: Dict[str, str] = Field(default_factory=dict)
    
    # Backward compatible property
    @property
    def session_id(self) -> Optional[str]:
        """Session ID (equivalent to sandbox_id, backward compatibility)"""
        return self.sandbox_id
    
    class Config:
        extra = "allow"


class AgentRuntimeContext:
    """Runtime context manager"""
    
    _context_var: ContextVar[Optional[RequestContext]] = ContextVar(
        "agent_runtime_context", default=None
    )
    
    @classmethod
    def get_current_context(cls) -> Optional[RequestContext]:
        """Get current request context"""
        return cls._context_var.get()
    
    @classmethod
    def set_current_context(cls, context: RequestContext) -> None:
        """Set current request context"""
        cls._context_var.set(context)
    
    @classmethod
    def clear_current_context(cls) -> None:
        """Clear current request context"""
        cls._context_var.set(None)
