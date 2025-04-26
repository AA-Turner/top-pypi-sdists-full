from unittest.mock import MagicMock

class PolicyConfigApiMock:

    def __init__(self):
        self.mock_delete_authz_bundle = MagicMock()
        self.mock_delete_resource_url_bundle = MagicMock()
        self.mock_get_authz_bundle = MagicMock()
        self.mock_get_resource_url_bundle = MagicMock()

    def delete_authz_bundle(self, *args, **kwargs):
        """
        This method mocks the original api PolicyConfigApi.delete_authz_bundle with MagicMock.
        """
        return self.mock_delete_authz_bundle(self, *args, **kwargs)

    def delete_resource_url_bundle(self, *args, **kwargs):
        """
        This method mocks the original api PolicyConfigApi.delete_resource_url_bundle with MagicMock.
        """
        return self.mock_delete_resource_url_bundle(self, *args, **kwargs)

    def get_authz_bundle(self, *args, **kwargs):
        """
        This method mocks the original api PolicyConfigApi.get_authz_bundle with MagicMock.
        """
        return self.mock_get_authz_bundle(self, *args, **kwargs)

    def get_resource_url_bundle(self, *args, **kwargs):
        """
        This method mocks the original api PolicyConfigApi.get_resource_url_bundle with MagicMock.
        """
        return self.mock_get_resource_url_bundle(self, *args, **kwargs)

