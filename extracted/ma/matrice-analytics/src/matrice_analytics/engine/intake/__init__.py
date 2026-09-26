"""Boundary adapters that shape raw model output into the engine's detection contract.

Everything in :mod:`matrice_analytics.engine` past this package assumes a detection already has a
bounding box (contract Section 4). Most producers -- any ordinary object detector -- already
satisfy that. The exception is a whole-frame or whole-clip classifier (X3D-style action/event
models: accident/normal, fall/not-falling, drowsy/alert, ...), which has no box to give.
:mod:`~matrice_analytics.engine.intake.classification` is the adapter for that family.

A second, orthogonal gap: a detection that *does* have a box may also carry a second-stage
attribute decoded by a classifier chained upstream (``car`` + ``vehicle_type: ambulance``).
:mod:`~matrice_analytics.engine.intake.attributes` normalizes that producer envelope the same
way, ahead of :meth:`~matrice_analytics.engine.runtime.session.Session.process_frame`.

This package has no dependency on ``matrice_analytics.post_processing`` or
``matrice_analytics.analytics``, matching every other ``engine`` sub-package.
"""

from __future__ import annotations

from matrice_analytics.engine.intake.attributes import (
    AttributeSpec,
    attach_attributes,
    decode_attribute,
)
from matrice_analytics.engine.intake.classification import whole_frame_detections

__all__ = ["AttributeSpec", "attach_attributes", "decode_attribute", "whole_frame_detections"]
