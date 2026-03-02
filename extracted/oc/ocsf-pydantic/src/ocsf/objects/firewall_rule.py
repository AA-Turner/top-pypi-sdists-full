
from .rule import Rule


class FirewallRule(Rule):
    """
    The Firewall Rule object represents a specific rule within a firewall policy or
    event. It contains information about a rule's configuration, properties, and
    associated actions that define how network traffic is handled by the firewall.
    """

    # Optional:
    condition: str | None = None
    sensitivity: str | None = None
    match_location: str | None = None
    match_details: list[str] | None = None
    rate_limit: int | None = None
    duration: int | None = None # The rule response time duration, usually used for challenge
                                # completion time.
