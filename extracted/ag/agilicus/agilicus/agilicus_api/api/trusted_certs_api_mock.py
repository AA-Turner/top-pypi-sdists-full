from unittest.mock import MagicMock

class TrustedCertsApiMock:

    def __init__(self):
        self.mock_create_bundle = MagicMock()
        self.mock_create_label = MagicMock()
        self.mock_create_trusted_cert = MagicMock()
        self.mock_delete_bundle = MagicMock()
        self.mock_delete_label = MagicMock()
        self.mock_delete_trusted_cert = MagicMock()
        self.mock_get_bundle = MagicMock()
        self.mock_get_label = MagicMock()
        self.mock_get_trusted_cert = MagicMock()
        self.mock_list_bundles = MagicMock()
        self.mock_list_cert_orgs = MagicMock()
        self.mock_list_labels = MagicMock()
        self.mock_list_trusted_certs = MagicMock()
        self.mock_replace_bundle = MagicMock()
        self.mock_replace_trusted_cert = MagicMock()

    def create_bundle(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.create_bundle with MagicMock.
        """
        return self.mock_create_bundle(self, *args, **kwargs)

    def create_label(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.create_label with MagicMock.
        """
        return self.mock_create_label(self, *args, **kwargs)

    def create_trusted_cert(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.create_trusted_cert with MagicMock.
        """
        return self.mock_create_trusted_cert(self, *args, **kwargs)

    def delete_bundle(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.delete_bundle with MagicMock.
        """
        return self.mock_delete_bundle(self, *args, **kwargs)

    def delete_label(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.delete_label with MagicMock.
        """
        return self.mock_delete_label(self, *args, **kwargs)

    def delete_trusted_cert(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.delete_trusted_cert with MagicMock.
        """
        return self.mock_delete_trusted_cert(self, *args, **kwargs)

    def get_bundle(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.get_bundle with MagicMock.
        """
        return self.mock_get_bundle(self, *args, **kwargs)

    def get_label(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.get_label with MagicMock.
        """
        return self.mock_get_label(self, *args, **kwargs)

    def get_trusted_cert(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.get_trusted_cert with MagicMock.
        """
        return self.mock_get_trusted_cert(self, *args, **kwargs)

    def list_bundles(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.list_bundles with MagicMock.
        """
        return self.mock_list_bundles(self, *args, **kwargs)

    def list_cert_orgs(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.list_cert_orgs with MagicMock.
        """
        return self.mock_list_cert_orgs(self, *args, **kwargs)

    def list_labels(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.list_labels with MagicMock.
        """
        return self.mock_list_labels(self, *args, **kwargs)

    def list_trusted_certs(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.list_trusted_certs with MagicMock.
        """
        return self.mock_list_trusted_certs(self, *args, **kwargs)

    def replace_bundle(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.replace_bundle with MagicMock.
        """
        return self.mock_replace_bundle(self, *args, **kwargs)

    def replace_trusted_cert(self, *args, **kwargs):
        """
        This method mocks the original api TrustedCertsApi.replace_trusted_cert with MagicMock.
        """
        return self.mock_replace_trusted_cert(self, *args, **kwargs)

