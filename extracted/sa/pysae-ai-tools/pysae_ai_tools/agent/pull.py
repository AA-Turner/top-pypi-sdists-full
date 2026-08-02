"""Pull tickets from GitLab matching agent labels."""

from .common import fetch_with_label
from .models import Ticket


def fetch_ready_tickets(projects: list[str]) -> list[Ticket]:
    """Fetch tickets labelled agent::ready across the given projects."""
    return fetch_with_label(projects, "agent::ready")


def fetch_wip_tickets(projects: list[str]) -> list[Ticket]:
    """Fetch tickets labelled agent::wip across the given projects."""
    return fetch_with_label(projects, "agent::wip")
