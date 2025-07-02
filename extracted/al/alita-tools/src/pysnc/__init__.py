"""
Stub module for pysnc to satisfy ServiceNow API wrapper imports.
"""
class ServiceNowClient:
    """Stub ServiceNowClient for testing purposes."""
    def __init__(self, base_url, auth):
        # auth is a tuple (username, password)
        self.base_url = base_url
        self.auth = auth
    def __getattr__(self, name):
        # Return a dummy attribute to avoid attribute errors
        def method(*args, **kwargs):
            raise NotImplementedError(f"ServiceNowClient.{name} is not implemented in stub")
        return method