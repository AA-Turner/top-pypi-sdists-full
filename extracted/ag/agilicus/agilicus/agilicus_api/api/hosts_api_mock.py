from unittest.mock import MagicMock

class HostsApiMock:

    def __init__(self):
        self.mock_add_host = MagicMock()
        self.mock_add_host_bundle = MagicMock()
        self.mock_add_host_label = MagicMock()
        self.mock_delete_host = MagicMock()
        self.mock_delete_host_bundle = MagicMock()
        self.mock_delete_host_label = MagicMock()
        self.mock_get_host = MagicMock()
        self.mock_get_host_bundle = MagicMock()
        self.mock_get_host_label = MagicMock()
        self.mock_list_host_bundles = MagicMock()
        self.mock_list_host_labels = MagicMock()
        self.mock_list_host_orgs = MagicMock()
        self.mock_list_hosts = MagicMock()
        self.mock_replace_host = MagicMock()
        self.mock_replace_host_bundle = MagicMock()

    def add_host(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.add_host with MagicMock.
        """
        return self.mock_add_host(self, *args, **kwargs)

    def add_host_bundle(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.add_host_bundle with MagicMock.
        """
        return self.mock_add_host_bundle(self, *args, **kwargs)

    def add_host_label(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.add_host_label with MagicMock.
        """
        return self.mock_add_host_label(self, *args, **kwargs)

    def delete_host(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.delete_host with MagicMock.
        """
        return self.mock_delete_host(self, *args, **kwargs)

    def delete_host_bundle(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.delete_host_bundle with MagicMock.
        """
        return self.mock_delete_host_bundle(self, *args, **kwargs)

    def delete_host_label(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.delete_host_label with MagicMock.
        """
        return self.mock_delete_host_label(self, *args, **kwargs)

    def get_host(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.get_host with MagicMock.
        """
        return self.mock_get_host(self, *args, **kwargs)

    def get_host_bundle(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.get_host_bundle with MagicMock.
        """
        return self.mock_get_host_bundle(self, *args, **kwargs)

    def get_host_label(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.get_host_label with MagicMock.
        """
        return self.mock_get_host_label(self, *args, **kwargs)

    def list_host_bundles(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.list_host_bundles with MagicMock.
        """
        return self.mock_list_host_bundles(self, *args, **kwargs)

    def list_host_labels(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.list_host_labels with MagicMock.
        """
        return self.mock_list_host_labels(self, *args, **kwargs)

    def list_host_orgs(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.list_host_orgs with MagicMock.
        """
        return self.mock_list_host_orgs(self, *args, **kwargs)

    def list_hosts(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.list_hosts with MagicMock.
        """
        return self.mock_list_hosts(self, *args, **kwargs)

    def replace_host(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.replace_host with MagicMock.
        """
        return self.mock_replace_host(self, *args, **kwargs)

    def replace_host_bundle(self, *args, **kwargs):
        """
        This method mocks the original api HostsApi.replace_host_bundle with MagicMock.
        """
        return self.mock_replace_host_bundle(self, *args, **kwargs)

