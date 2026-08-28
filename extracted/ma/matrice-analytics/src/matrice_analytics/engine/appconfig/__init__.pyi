"""Stub file for engine.appconfig directory."""
from typing import Any

# Constants
logger: Any = ...  # From loader
METRICS_FILENAME: str = ...  # From models
POST_PROCESSING_FILENAME: str = ...  # From models
WIDGETS_FILENAME: str = ...  # From models

# Functions
# From loader
def load_app_config(root: str | Any) -> Any:
    """
    Parse ``metrics.json``, ``widgets.json`` and ``post_processing_config.json`` from a folder.
    """
    ...

# Classes
# From loader
class AppConfigBundle:
    # The three sibling files as parsed, plus everything wrong with them.
    #
    #     A ``None`` collection means the file was absent or could not be parsed at all — distinct from
    #     an empty tuple, which means the file was a well-formed empty array.

    def all_present(self: Any) -> bool: ...

    def errors(self: Any) -> tuple[Any, ...]: ...

    def metric_keys(self: Any) -> Any[str]: ...

    def none_present(self: Any) -> bool: ...

    def warnings(self: Any) -> tuple[Any, ...]: ...


# From models
class ConfigProblem:
    # One thing wrong with one of the three files.
    #
    #     Problems are *returned*, never raised: a malformed sibling file must not stop the rest of the
    #     suite from running, in the same way :func:`~matrice_analytics.engine.testing.generate._resolve_app`
    #     turns a load failure into data.

    ...

# From models
class MetricEntry:
    # One element of ``metrics.json``.
    #
    #     ``key`` is the join to ``app.yaml`` ``metrics[].key`` and to ``widgets.json`` ``dataKey``, by
    #     exact string match. ``aggType`` is camelCase on the wire and ``agg_type`` in the manifest; the
    #     alias carries that difference so a check can compare the two directly.

    ...

# From models
class PostProcessingConfig:
    # ``post_processing_config.json`` — the only one of the three that reaches the engine.
    #
    #     be-inference copies this object verbatim into ``nodeConfig`` under **both** ``use_case_config``
    #     and ``post_processing_config`` and it becomes the analytics job's parameters unchanged, so the
    #     platform imposes no schema beyond it being an object. Only ``usecase`` is load-bearing here: it
    #     is the join to ``app.yaml`` ``app.id``.

    def as_dict(self: Any) -> dict[str, Any]: ...


# From models
class WidgetBinding:
    # One resolved ``dataKey`` token paired with the source that says where to look it up.
    #
    #     ``metric`` reads ``business_metrics[key]`` — our ``results-agg.metrics[].key``.
    #     ``tracking_class`` reads ``analytics[key]`` / ``analytics_totals[key]`` — our
    #     ``current_counts[].category``, i.e. an **entity name**, not a metric key. Two keyspaces, no
    #     cross-namespace fallback (``volumeAnalyticsHelpers.ts:385-424``).

    ...

# From models
class WidgetEntry:
    # One element of ``widgets.json``.

    def resolve_bindings(self: Any) -> tuple[tuple[Any, ...], str | None]:
        """
        Pair each token with its source, or explain why the widget is invalid.
        
                Mirrors ``widgetKeySources`` / ``parseDataSources``. A single ``dataSource`` applies to
                every token; a CSV must be positionally 1:1 with ``dataKey``. **A length mismatch or an
                unknown source silently drops the whole widget on the live dashboard**, so this returns a
                reason rather than a partial binding.
        """
        ...

    def tokens(self: Any) -> tuple[str, ...]:
        """
        The ``dataKey`` CSV, split and trimmed. Blank falls back to the widget's own ``key``.
        """
        ...


from . import loader, models