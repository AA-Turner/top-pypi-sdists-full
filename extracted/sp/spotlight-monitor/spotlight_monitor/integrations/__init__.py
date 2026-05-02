"""
Spotlight Integrations

Auto-instrumentation for various frameworks and platforms.

Available integrations:
    - FastAPI: Built-in via spotlight.instrument(app) or SpotlightMiddleware
    - Airflow: from spotlight_monitor.integrations.airflow import AirflowIntegration
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .airflow import AirflowIntegration
    from .fastapi import FastAPIIntegration

__all__ = [
    "AirflowIntegration",
    "FastAPIIntegration",
]