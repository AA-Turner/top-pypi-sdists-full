"""FortiOS CMDB - PasswordPolicyConform category"""

from .select import Select

__all__ = [
    "PasswordPolicyConform",
    "Select",
]


class PasswordPolicyConform:
    """PasswordPolicyConform endpoints wrapper for CMDB API."""

    def __init__(self, client):
        """PasswordPolicyConform endpoints.
        
        Args:
            client: HTTP client instance for API communication
        """
        self.select = Select(client)
