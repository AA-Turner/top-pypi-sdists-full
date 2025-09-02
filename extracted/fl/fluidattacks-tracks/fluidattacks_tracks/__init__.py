"""Fluid Attacks Tracks SDK."""

from fluidattacks_tracks.client import TracksClient, TracksClientConfig
from fluidattacks_tracks.resources.event import EventResource


class Tracks:
    """Tracks SDK interface."""

    def __init__(self, config: TracksClientConfig | None = None) -> None:
        """Initialize the Tracks client."""
        self.client = TracksClient(config)
        self.event = EventResource(self.client)
