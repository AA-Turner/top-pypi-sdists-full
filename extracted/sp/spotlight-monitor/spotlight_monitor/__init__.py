"""
Spotlight Monitor SDK

AI-powered service monitoring with exception tracking and validation.

Usage:
    from spotlight_monitor import Spotlight

    # FastAPI
    app = FastAPI()
    spotlight = Spotlight(api_key="sp_xxx", service_slug="my-api")
    spotlight.instrument(app)

    # Airflow
    from spotlight_monitor.integrations.airflow import AirflowIntegration
    spotlight = Spotlight(api_key="sp_xxx", service_slug="daily-etl")
    airflow = AirflowIntegration(spotlight)

    @dag(on_failure_callback=airflow.on_failure)
    def my_dag():
        ...

    # Manual exception capture
    try:
        risky_operation()
    except Exception as e:
        spotlight.capture_exception(e)
        raise
"""
from .client import Spotlight
from .models import RequestMetric, ValidationResult, HealthCheck, MetricsBatch
from .validators import ValidatorRegistry, validator
from .exceptions import (
    Breadcrumb,
    RequestContext,
    capture_exception,
    ExceptionInfo,
)

# Re-export middleware for convenience
from .middleware import SpotlightMiddleware

__version__ = "0.3.0"
__all__ = [
    "Spotlight",
    "SpotlightMiddleware",
    "RequestMetric",
    "ValidationResult",
    "HealthCheck",
    "MetricsBatch",
    "ValidatorRegistry",
    "validator",
    "Breadcrumb",
    "RequestContext",
    "capture_exception",
    "ExceptionInfo",
]