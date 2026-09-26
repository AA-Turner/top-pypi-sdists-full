"""Auto-generated stub for module: legacy_agg_bridge."""
from typing import Any, Dict, Optional

# Functions
def legacy_shape_agg_summary(agg_summary: Optional[Dict[str, Any]], stream_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Re-key a zone-keyed engine ``agg_summary`` into the legacy frame-keyed shape (PY-5).
    
        The two shapes are a deliberate, documented divergence
        (:class:`~matrice_analytics.engine.contract.schemas.FrameSummaryEntry`), and the engine's is the
        better one -- it is the only form that works for a multi-zone app. But every consumer was built
        against legacy, so this bridges rather than migrates:
    
        ==========================  ==========================  ==================================
        field                       legacy                      engine
        ==========================  ==========================  ==================================
        top-level key               frame number (``"45507"``)  zone (``"global"``, ``"inside"``)
        ``human_text``              on the frame entry          inside ``tracking_stats``
        ``zone_analysis``           on the frame entry          implicit in the zone keys
        ==========================  ==========================  ==================================
    
        So: the per-zone entries collapse into one frame entry, ``human_text`` is lifted back out,
        ``zone_analysis`` is rebuilt from the zone keys (and mirrored inside ``tracking_stats``, which
        is where legacy puts it too), and ``alerts`` / ``incidents`` / ``business_analytics`` are
        merged. Nothing is dropped: the per-zone view survives in full under ``zone_analysis``.
    
        Returns the input unchanged when the bridge is disabled, when there is nothing to convert, or
        when the payload is already frame-keyed -- so it is idempotent and safe to call twice.
    """
    ...
