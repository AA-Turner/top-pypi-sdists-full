from unittest.mock import MagicMock

class CredentialsApiMock:

    def __init__(self):
        self.mock_create_object_credential = MagicMock()
        self.mock_delete_object_credential = MagicMock()
        self.mock_get_object_credential = MagicMock()
        self.mock_list_object_credential_existence_info = MagicMock()
        self.mock_list_object_credentials = MagicMock()
        self.mock_replace_object_credential = MagicMock()

    def create_object_credential(self, *args, **kwargs):
        """
        This method mocks the original api CredentialsApi.create_object_credential with MagicMock.
        """
        return self.mock_create_object_credential(self, *args, **kwargs)

    def delete_object_credential(self, *args, **kwargs):
        """
        This method mocks the original api CredentialsApi.delete_object_credential with MagicMock.
        """
        return self.mock_delete_object_credential(self, *args, **kwargs)

    def get_object_credential(self, *args, **kwargs):
        """
        This method mocks the original api CredentialsApi.get_object_credential with MagicMock.
        """
        return self.mock_get_object_credential(self, *args, **kwargs)

    def list_object_credential_existence_info(self, *args, **kwargs):
        """
        This method mocks the original api CredentialsApi.list_object_credential_existence_info with MagicMock.
        """
        return self.mock_list_object_credential_existence_info(self, *args, **kwargs)

    def list_object_credentials(self, *args, **kwargs):
        """
        This method mocks the original api CredentialsApi.list_object_credentials with MagicMock.
        """
        return self.mock_list_object_credentials(self, *args, **kwargs)

    def replace_object_credential(self, *args, **kwargs):
        """
        This method mocks the original api CredentialsApi.replace_object_credential with MagicMock.
        """
        return self.mock_replace_object_credential(self, *args, **kwargs)

