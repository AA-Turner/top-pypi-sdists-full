"""Primitives: the one interface every pipeline stage implements.

``_contracts/09-tobe-engine-architecture.md`` §3.  This is the import path app authors
write against, and the one the authoring guide (``10``) documents::

    from matrice_analytics.engine.primitives import FrameContext, PrimitiveOutput
    from matrice_analytics.engine.state import StateStore

One file per primitive, implemented **once** (objective **O2**).  ``base.py`` holds the
protocol and the four data types; the concrete primitives land alongside it as they are
built, each registering itself with :data:`REGISTRY`.

Nothing here knows the wire format -- a primitive returns primitive-shaped data and
:mod:`matrice_analytics.engine.contract.emit` is the only thing that builds a payload
(**O1**).  Nothing here knows an app's name either (``09`` §1).
"""

from __future__ import annotations

from matrice_analytics.engine.primitives.base import (
    REGISTRY,
    Clock,
    CustomPrimitive,
    FrameClock,
    FrameContext,
    Keypoint,
    MaskRef,
    PipelineDetection,
    Primitive,
    PrimitiveEvent,
    PrimitiveOutput,
    PrimitiveRegistrationError,
    PrimitiveRegistry,
    PrimitiveValueError,
    Scalar,
    SourceResolutionError,
    TrackState,
    WallClock,
    WindowOutput,
    conformance_problems,
    register,
    resolve_value,
)

__all__ = [
    # the interface
    "Primitive",
    "CustomPrimitive",
    "conformance_problems",
    # what a primitive sees
    "FrameContext",
    "Keypoint",
    "MaskRef",
    "PipelineDetection",
    # what a primitive returns
    "PrimitiveEvent",
    "PrimitiveOutput",
    "Scalar",
    "TrackState",
    "WindowOutput",
    "resolve_value",
    # the clock (PY-13)
    "Clock",
    "FrameClock",
    "WallClock",
    # the registry
    "REGISTRY",
    "PrimitiveRegistry",
    "register",
    # errors
    "PrimitiveRegistrationError",
    "PrimitiveValueError",
    "SourceResolutionError",
]

# ---------------------------------------------------------------------------
# Concrete primitives
# ---------------------------------------------------------------------------
# Importing this package registers every primitive on REGISTRY, so a manifest
# can name any of them without the caller knowing which module defines it.
#
# These imports live here, and only here, on purpose: four agents built these
# in parallel, and a shared __init__ would have been the one file they all
# contended on. Registration itself happens via the @register decorator inside
# each module, so adding a primitive is one line here and nothing else.
#
# Import for side effects (registration); the classes are re-exported below.
from matrice_analytics.engine.primitives.detect import Detect
from matrice_analytics.engine.primitives.dwell import Dwell
from matrice_analytics.engine.primitives.incident_quantise import IncidentQuantise
from matrice_analytics.engine.primitives.keypoint_pose import KeypointPose
from matrice_analytics.engine.primitives.line_crossing import LineCrossing
from matrice_analytics.engine.primitives.ratio_compliance import RatioCompliance
from matrice_analytics.engine.primitives.segmentation_area import SegmentationArea
from matrice_analytics.engine.primitives.state_machine import StateMachine
from matrice_analytics.engine.primitives.track import Track
from matrice_analytics.engine.primitives.unique_count import UniqueCount
from matrice_analytics.engine.primitives.velocity_state import VelocityState
from matrice_analytics.engine.primitives.zone_occupancy import ZoneOccupancy

__all__ += [
    "Detect",
    "Dwell",
    "IncidentQuantise",
    "KeypointPose",
    "LineCrossing",
    "RatioCompliance",
    "SegmentationArea",
    "StateMachine",
    "Track",
    "UniqueCount",
    "VelocityState",
    "ZoneOccupancy",
]
