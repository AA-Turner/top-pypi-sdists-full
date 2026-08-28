"""The three files an app version uploads beside ``app.yaml``, and their parser.

``app.yaml`` says what the engine computes. These three say how the dashboard displays it, and one
of them says what the worker runs. They meet nowhere on the server — the join happens in the
browser, by exact string match (``_contracts/appversion/00-SYNTHESIS.md`` §1).

    from matrice_analytics.engine.appconfig import load_app_config

    bundle = load_app_config("./v1.4")     # never raises; failures are bundle.problems

Cross-checking the parsed result against a manifest, and against what the engine really publishes,
is :mod:`matrice_analytics.engine.testing.generate` checks 6 and 7 — not this package.
"""

from __future__ import annotations

from .loader import AppConfigBundle, load_app_config
from .models import (
    CHART_TYPES_RENDERED,
    DATA_SOURCES,
    METRICS_FILENAME,
    POST_PROCESSING_FILENAME,
    RESERVED_WIDGET_TOKENS,
    WIDGETS_FILENAME,
    ConfigProblem,
    MetricEntry,
    PostProcessingConfig,
    WidgetBinding,
    WidgetEntry,
)

__all__ = [
    "CHART_TYPES_RENDERED",
    "DATA_SOURCES",
    "METRICS_FILENAME",
    "POST_PROCESSING_FILENAME",
    "RESERVED_WIDGET_TOKENS",
    "WIDGETS_FILENAME",
    "AppConfigBundle",
    "ConfigProblem",
    "MetricEntry",
    "PostProcessingConfig",
    "WidgetBinding",
    "WidgetEntry",
    "load_app_config",
]
