"""Auto-generated stub for module: models."""
from typing import Any

# Constants
METRICS_FILENAME: str
POST_PROCESSING_FILENAME: str
WIDGETS_FILENAME: str

# Classes
class ConfigProblem:
    # One thing wrong with one of the three files.
    #
    #     Problems are *returned*, never raised: a malformed sibling file must not stop the rest of the
    #     suite from running, in the same way :func:`~matrice_analytics.engine.testing.generate._resolve_app`
    #     turns a load failure into data.

    ...
class MetricEntry:
    # One element of ``metrics.json``.
    #
    #     ``key`` is the join to ``app.yaml`` ``metrics[].key`` and to ``widgets.json`` ``dataKey``, by
    #     exact string match. ``aggType`` is camelCase on the wire and ``agg_type`` in the manifest; the
    #     alias carries that difference so a check can compare the two directly.

    ...
class PostProcessingConfig:
    # ``post_processing_config.json`` — the only one of the three that reaches the engine.
    #
    #     be-inference copies this object verbatim into ``nodeConfig`` under **both** ``use_case_config``
    #     and ``post_processing_config`` and it becomes the analytics job's parameters unchanged, so the
    #     platform imposes no schema beyond it being an object. Only ``usecase`` is load-bearing here: it
    #     is the join to ``app.yaml`` ``app.id``.

    def as_dict(self: Any) -> dict[str, Any]: ...

class WidgetBinding:
    # One resolved ``dataKey`` token paired with the source that says where to look it up.
    #
    #     ``metric`` reads ``business_metrics[key]`` — our ``results-agg.metrics[].key``.
    #     ``tracking_class`` reads ``analytics[key]`` / ``analytics_totals[key]`` — our
    #     ``current_counts[].category``, i.e. an **entity name**, not a metric key. Two keyspaces, no
    #     cross-namespace fallback (``volumeAnalyticsHelpers.ts:385-424``).

    ...
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

