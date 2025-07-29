from unittest.mock import MagicMock

class LicensingApiMock:

    def __init__(self):
        self.mock_create_hypothetical_license_details_query = MagicMock()
        self.mock_create_license = MagicMock()
        self.mock_create_product_table_version = MagicMock()
        self.mock_delete_license = MagicMock()
        self.mock_delete_product_table_version = MagicMock()
        self.mock_get_license = MagicMock()
        self.mock_get_product_table_version = MagicMock()
        self.mock_list_license_details = MagicMock()
        self.mock_list_license_evaluation_contexts = MagicMock()
        self.mock_list_licenses = MagicMock()
        self.mock_list_product_table_versions = MagicMock()
        self.mock_replace_license = MagicMock()
        self.mock_replace_product_table_version = MagicMock()

    def create_hypothetical_license_details_query(self, *args, **kwargs):
        """
        This method mocks the original api LicensingApi.create_hypothetical_license_details_query with MagicMock.
        """
        return self.mock_create_hypothetical_license_details_query(self, *args, **kwargs)

    def create_license(self, *args, **kwargs):
        """
        This method mocks the original api LicensingApi.create_license with MagicMock.
        """
        return self.mock_create_license(self, *args, **kwargs)

    def create_product_table_version(self, *args, **kwargs):
        """
        This method mocks the original api LicensingApi.create_product_table_version with MagicMock.
        """
        return self.mock_create_product_table_version(self, *args, **kwargs)

    def delete_license(self, *args, **kwargs):
        """
        This method mocks the original api LicensingApi.delete_license with MagicMock.
        """
        return self.mock_delete_license(self, *args, **kwargs)

    def delete_product_table_version(self, *args, **kwargs):
        """
        This method mocks the original api LicensingApi.delete_product_table_version with MagicMock.
        """
        return self.mock_delete_product_table_version(self, *args, **kwargs)

    def get_license(self, *args, **kwargs):
        """
        This method mocks the original api LicensingApi.get_license with MagicMock.
        """
        return self.mock_get_license(self, *args, **kwargs)

    def get_product_table_version(self, *args, **kwargs):
        """
        This method mocks the original api LicensingApi.get_product_table_version with MagicMock.
        """
        return self.mock_get_product_table_version(self, *args, **kwargs)

    def list_license_details(self, *args, **kwargs):
        """
        This method mocks the original api LicensingApi.list_license_details with MagicMock.
        """
        return self.mock_list_license_details(self, *args, **kwargs)

    def list_license_evaluation_contexts(self, *args, **kwargs):
        """
        This method mocks the original api LicensingApi.list_license_evaluation_contexts with MagicMock.
        """
        return self.mock_list_license_evaluation_contexts(self, *args, **kwargs)

    def list_licenses(self, *args, **kwargs):
        """
        This method mocks the original api LicensingApi.list_licenses with MagicMock.
        """
        return self.mock_list_licenses(self, *args, **kwargs)

    def list_product_table_versions(self, *args, **kwargs):
        """
        This method mocks the original api LicensingApi.list_product_table_versions with MagicMock.
        """
        return self.mock_list_product_table_versions(self, *args, **kwargs)

    def replace_license(self, *args, **kwargs):
        """
        This method mocks the original api LicensingApi.replace_license with MagicMock.
        """
        return self.mock_replace_license(self, *args, **kwargs)

    def replace_product_table_version(self, *args, **kwargs):
        """
        This method mocks the original api LicensingApi.replace_product_table_version with MagicMock.
        """
        return self.mock_replace_product_table_version(self, *args, **kwargs)

