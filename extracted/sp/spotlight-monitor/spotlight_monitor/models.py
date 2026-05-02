"""
Spotlight SDK Models
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import uuid4


@dataclass
class ValidationResult:
    """Result of a validator execution."""
    name: str
    passed: bool
    failure_reason: Optional[str] = None
    execution_ms: Optional[int] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class RequestMetric:
    """A single request metric to send to Spotlight."""
    endpoint: str
    method: str
    status_code: int
    latency_ms: int
    timestamp: datetime
    request_id: str = field(default_factory=lambda: str(uuid4()))
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    validations: List[ValidationResult] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "endpoint": self.endpoint,
            "method": self.method,
            "status_code": self.status_code,
            "latency_ms": self.latency_ms,
            "timestamp": self.timestamp.isoformat(),
            "error_type": self.error_type,
            "error_message": self.error_message,
            "validations": [v.to_dict() for v in self.validations],
            "metadata": self.metadata,
        }


@dataclass
class HealthCheck:
    """Health check result."""
    service: str
    status: str  # healthy, degraded, unhealthy
    latency_ms: int
    timestamp: datetime
    dependencies: Dict[str, str] = field(default_factory=dict)  # name -> status

    def to_dict(self) -> dict:
        return {
            "service": self.service,
            "status": self.status,
            "latency_ms": self.latency_ms,
            "timestamp": self.timestamp.isoformat(),
            "dependencies": self.dependencies,
        }


@dataclass 
class MetricsBatch:
    """Batch of metrics to send."""
    service_slug: str
    requests: List[RequestMetric] = field(default_factory=list)
    health_checks: List[HealthCheck] = field(default_factory=list)
    environment: str = "production"  # Add this


    def to_dict(self) -> dict:
        return {
            "service_slug": self.service_slug,
            "requests": [r.to_dict() for r in self.requests],
            "environment": self.environment,  # Add this
            "health_checks": [h.to_dict() for h in self.health_checks],
        }
