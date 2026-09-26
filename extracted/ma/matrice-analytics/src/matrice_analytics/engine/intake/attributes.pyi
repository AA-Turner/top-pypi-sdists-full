"""Auto-generated stub for module: attributes."""
from typing import Any

# Functions
def attach_attributes(raw: Any, specs: Any[Any]) -> Any:
    """
    Decode every spec onto each detection in ``raw``, in place, and return it.
    
        Handles the same three envelopes as the legacy attach helpers
        (``vehicle_type_classification.py:144-174``): a bare list, ``{"detections": [...]}``, and
        a ``frame_id -> list`` mapping. A detection that carries nothing decodable is left without
        the key -- **never** given an ``"unknown"`` placeholder, because "the classifier said
        nothing" and "the classifier said unknown" are different facts and only the first one is a
        chain outage.
    """
    ...
def decode_attribute(det: Any[str, Any], spec: Any) -> tuple[str, float] | None:
    """
    One detection, one spec -> ``(label, confidence)`` or ``None``.
    
        Shapes tried in this order, matching legacy:
    
        1. ``heads[spec.head or spec.name]`` -> ``{label, confidence}``, else its ``top_k``;
        2. flat ``label`` + ``class_confidence``;
        3. flat ``top_k``;
        4. raw ``predictor_output`` logits + :attr:`AttributeSpec.index_to_label`.
    
        Returns ``None`` when nothing resolves, **including** when a bare class index does not
        resolve through ``index_to_label`` -- legacy drops that case rather than publishing the
        index as a label (``vehicle_type_classification.py:121-131``), and a dashboard legend
        reading ``817`` is worse than a missing row.
    """
    ...

# Classes
class AttributeSpec:
    # How to decode one attribute from one producer.
    #
    #     ``index_to_label`` exists only for the ``predictor_output`` shape and for a producer that
    #     hands back a bare class index instead of a label. It is consulted with **both** an int and
    #     a str key: a JSON-delivered mapping carries ``"817"`` and an in-code default carries
    #     ``817``, and trying only one silently misses every mapping from the other source
    #     (``vehicle_type_classification.py:78-80``).

    ...
