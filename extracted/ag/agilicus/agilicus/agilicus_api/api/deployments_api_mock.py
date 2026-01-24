from unittest.mock import MagicMock

class DeploymentsApiMock:

    def __init__(self):
        self.mock_create_deployment = MagicMock()
        self.mock_create_deployment_instance = MagicMock()
        self.mock_create_deployment_template = MagicMock()
        self.mock_delete_deployment = MagicMock()
        self.mock_delete_deployment_instance = MagicMock()
        self.mock_delete_deployment_template = MagicMock()
        self.mock_get_deployment = MagicMock()
        self.mock_get_deployment_instance = MagicMock()
        self.mock_get_deployment_template = MagicMock()
        self.mock_list_deployment_instances = MagicMock()
        self.mock_list_deployment_templates = MagicMock()
        self.mock_list_deployments = MagicMock()
        self.mock_update_deployment = MagicMock()
        self.mock_update_deployment_instance = MagicMock()
        self.mock_update_deployment_template = MagicMock()

    def create_deployment(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.create_deployment with MagicMock.
        """
        return self.mock_create_deployment(self, *args, **kwargs)

    def create_deployment_instance(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.create_deployment_instance with MagicMock.
        """
        return self.mock_create_deployment_instance(self, *args, **kwargs)

    def create_deployment_template(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.create_deployment_template with MagicMock.
        """
        return self.mock_create_deployment_template(self, *args, **kwargs)

    def delete_deployment(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.delete_deployment with MagicMock.
        """
        return self.mock_delete_deployment(self, *args, **kwargs)

    def delete_deployment_instance(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.delete_deployment_instance with MagicMock.
        """
        return self.mock_delete_deployment_instance(self, *args, **kwargs)

    def delete_deployment_template(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.delete_deployment_template with MagicMock.
        """
        return self.mock_delete_deployment_template(self, *args, **kwargs)

    def get_deployment(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.get_deployment with MagicMock.
        """
        return self.mock_get_deployment(self, *args, **kwargs)

    def get_deployment_instance(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.get_deployment_instance with MagicMock.
        """
        return self.mock_get_deployment_instance(self, *args, **kwargs)

    def get_deployment_template(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.get_deployment_template with MagicMock.
        """
        return self.mock_get_deployment_template(self, *args, **kwargs)

    def list_deployment_instances(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.list_deployment_instances with MagicMock.
        """
        return self.mock_list_deployment_instances(self, *args, **kwargs)

    def list_deployment_templates(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.list_deployment_templates with MagicMock.
        """
        return self.mock_list_deployment_templates(self, *args, **kwargs)

    def list_deployments(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.list_deployments with MagicMock.
        """
        return self.mock_list_deployments(self, *args, **kwargs)

    def update_deployment(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.update_deployment with MagicMock.
        """
        return self.mock_update_deployment(self, *args, **kwargs)

    def update_deployment_instance(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.update_deployment_instance with MagicMock.
        """
        return self.mock_update_deployment_instance(self, *args, **kwargs)

    def update_deployment_template(self, *args, **kwargs):
        """
        This method mocks the original api DeploymentsApi.update_deployment_template with MagicMock.
        """
        return self.mock_update_deployment_template(self, *args, **kwargs)

