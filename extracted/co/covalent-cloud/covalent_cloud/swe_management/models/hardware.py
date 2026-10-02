# Copyright 2025 Agnostiq Inc.

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator


class HardwareSpec(BaseModel):
    """
    Represents hardware specifications and pricing information.

    Attributes:
        id: Unique hardware identifier
        name: Display name of the hardware configuration
        provider: Hardware provider name
        status: Current availability status (ACTIVE, DOWN, etc.)
        cost_per_hour: Hourly cost in dollars
        display_cost: Formatted cost string (e.g., "$0.50")
        gpu_type: Type/model of GPU if available
        gpus_allowed: List of allowed GPU counts
        memory: Total memory in MB
        vcpus: Number of virtual CPUs
        gpu_memory: GPU memory in MB if GPU available
        gpu_vendor: GPU vendor (e.g., NVIDIA, AMD)
        vcpu_type: Type/architecture of CPU
        gpu_cuda_cores: Number of CUDA cores if NVIDIA GPU
        gpu_tensor_cores: Number of tensor cores if available
        gpu_tensor_core_type: Type of tensor cores
        gpu_memory_type: Type of GPU memory (e.g., GDDR6)
        gpu_compute_capability: CUDA compute capability
        gpu_interconnect: GPU interconnect type
        memory_per_gpu: Memory allocated per GPU in MB
        vcpu_per_gpu: vCPUs allocated per GPU
        created_at: Timestamp when hardware was created
        updated_at: Timestamp when hardware was last updated
        is_active: Whether hardware is active
        has_gpu: Whether this hardware configuration includes GPU(s)
    """

    id: str
    name: str
    provider: str
    status: str
    cost_per_hour: float
    display_cost: str
    gpu_type: Optional[str] = None
    gpus_allowed: Optional[List[int]] = Field(
        default=None, description="List of allowed GPU counts"
    )
    memory: int
    vcpus: int
    gpu_memory: Optional[int] = None
    gpu_vendor: Optional[str] = None
    vcpu_type: Optional[str] = None
    gpu_cuda_cores: Optional[int] = None
    gpu_tensor_cores: Optional[int] = None
    gpu_tensor_core_type: Optional[str] = None
    gpu_memory_type: Optional[str] = None
    gpu_compute_capability: Optional[str] = None
    gpu_interconnect: Optional[str] = None
    memory_per_gpu: Optional[int] = None
    vcpu_per_gpu: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    has_gpu: bool = False

    @model_validator(mode="after")
    def set_has_gpu(self) -> "HardwareSpec":
        """Set has_gpu based on gpu_type availability."""
        self.has_gpu = bool(self.gpu_type and self.gpu_type.strip())
        return self

    def __str__(self) -> str:
        # Format memory in GB if large enough
        memory_display = f"{self.memory // 1024}GB" if self.memory >= 1024 else f"{self.memory}MB"

        gpu_section = ""
        if self.has_gpu:
            gpu_section = f"""
GPU Information:
  Type: {self.gpu_type}
  Vendor: {self.gpu_vendor or 'N/A'}
  Memory: {f"{self.gpu_memory // 1024}GB" if self.gpu_memory and self.gpu_memory >= 1024 else f"{self.gpu_memory}MB" if self.gpu_memory else 'N/A'}"""

            if self.gpu_cuda_cores:
                gpu_section += f"\n  CUDA Cores: {self.gpu_cuda_cores}"
            if self.gpu_compute_capability:
                gpu_section += f"\n  Compute Capability: {self.gpu_compute_capability}"

        return f"""Hardware Specification
=====================
Name: {self.name}
Provider: {self.provider}
Status: {self.status}
Cost: {self.display_cost}/hour

Compute Resources:
  vCPUs: {self.vcpus}
  Memory: {memory_display}
  vCPU Type: {self.vcpu_type or 'N/A'}{gpu_section}

Active: {'Yes' if self.is_active else 'No'}"""


class HardwareListResponse(BaseModel):
    """
    Contains list of hardware specifications with metadata.

    Attributes:
        hardware: List of hardware specifications
        metadata: Pagination and count metadata
    """

    hardware: List[HardwareSpec] = Field(default_factory=list)
    metadata: Optional[dict] = None

    def __str__(self) -> str:
        return f"HardwareListResponse({len(self.hardware)} hardware specifications)"

    @model_validator(mode="before")
    @classmethod
    def convert_server_response(cls, values):
        """Convert server response format to our schema."""
        if isinstance(values, dict) and "hardware" in values:
            # Server returns the hardware list directly
            return values
        return values
