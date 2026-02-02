"""
This module contains classes for beamline checks, used to check the beamline status.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from bec_lib.device import Device


class BeamlineCondition(ABC):
    """Abstract base class for beamline checks."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enabled = True

    @property
    @abstractmethod
    def name(self) -> str:
        """Return a name for the beamline check."""

    @abstractmethod
    def run(self) -> bool:
        """Run the beamline check and return True if the beam is okay, False otherwise."""

    @abstractmethod
    def on_failure_msg(self) -> str:
        """Return a message that will be displayed if the beamline check fails."""


class ShutterCondition(BeamlineCondition):
    """Check if the shutter is open."""

    def __init__(self, shutter: Device):
        super().__init__()
        self.shutter = shutter

    @property
    def name(self):
        return "shutter"

    def run(self):
        shutter_val = self.shutter.read(cached=True)
        return shutter_val["value"].lower() == "open"

    def on_failure_msg(self):
        return "Check beam failed: Shutter is closed."


class LightAvailableCondition(BeamlineCondition):
    """Check if the light is available."""

    def __init__(self, machine_status: Device):
        super().__init__()
        self.machine_status = machine_status

    @property
    def name(self):
        return "light_available"

    def run(self):
        machine_status = self.machine_status.read(cached=True)
        return machine_status["value"] in ["Light Available", "Light-Available"]

    def on_failure_msg(self):
        return "Check beam failed: Light not available."


class FastOrbitFeedbackCondition(BeamlineCondition):
    """Check if the fast orbit feedback is running."""

    def __init__(self, sls_fast_orbit_feedback: Device):
        super().__init__()
        self.sls_fast_orbit_feedback = sls_fast_orbit_feedback

    @property
    def name(self):
        return "fast_orbit_feedback"

    def run(self):
        fast_orbit_feedback = self.sls_fast_orbit_feedback.read(cached=True)
        return fast_orbit_feedback["value"] == "running"

    def on_failure_msg(self):
        return "Check beam failed: Fast orbit feedback is not running."
