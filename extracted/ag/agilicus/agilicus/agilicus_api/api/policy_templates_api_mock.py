from unittest.mock import MagicMock

class PolicyTemplatesApiMock:

    def __init__(self):
        self.mock_create_policy_template_instance = MagicMock()
        self.mock_delete_policy_template_instance = MagicMock()
        self.mock_get_policy_template_instance = MagicMock()
        self.mock_list_policy_template_instances = MagicMock()
        self.mock_replace_policy_template_instance = MagicMock()

    def create_policy_template_instance(self, *args, **kwargs):
        """
        This method mocks the original api PolicyTemplatesApi.create_policy_template_instance with MagicMock.
        """
        return self.mock_create_policy_template_instance(self, *args, **kwargs)

    def delete_policy_template_instance(self, *args, **kwargs):
        """
        This method mocks the original api PolicyTemplatesApi.delete_policy_template_instance with MagicMock.
        """
        return self.mock_delete_policy_template_instance(self, *args, **kwargs)

    def get_policy_template_instance(self, *args, **kwargs):
        """
        This method mocks the original api PolicyTemplatesApi.get_policy_template_instance with MagicMock.
        """
        return self.mock_get_policy_template_instance(self, *args, **kwargs)

    def list_policy_template_instances(self, *args, **kwargs):
        """
        This method mocks the original api PolicyTemplatesApi.list_policy_template_instances with MagicMock.
        """
        return self.mock_list_policy_template_instances(self, *args, **kwargs)

    def replace_policy_template_instance(self, *args, **kwargs):
        """
        This method mocks the original api PolicyTemplatesApi.replace_policy_template_instance with MagicMock.
        """
        return self.mock_replace_policy_template_instance(self, *args, **kwargs)

