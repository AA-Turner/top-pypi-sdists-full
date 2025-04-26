from unittest.mock import MagicMock

class ConnectorsApiMock:

    def __init__(self):
        self.mock_create_agent_connector = MagicMock()
        self.mock_create_agent_csr = MagicMock()
        self.mock_create_agent_stats = MagicMock()
        self.mock_create_configure_publishing_request = MagicMock()
        self.mock_create_connector_proxy = MagicMock()
        self.mock_create_csr = MagicMock()
        self.mock_create_instance = MagicMock()
        self.mock_create_ipsec_connector = MagicMock()
        self.mock_create_queue = MagicMock()
        self.mock_create_service = MagicMock()
        self.mock_create_transfer = MagicMock()
        self.mock_delete_agent_connector = MagicMock()
        self.mock_delete_connector = MagicMock()
        self.mock_delete_connector_queue = MagicMock()
        self.mock_delete_instance = MagicMock()
        self.mock_delete_ipsec_connector = MagicMock()
        self.mock_delete_proxy = MagicMock()
        self.mock_delete_service = MagicMock()
        self.mock_delete_transfer = MagicMock()
        self.mock_get_agent_connector = MagicMock()
        self.mock_get_agent_connector_dynamic_stats = MagicMock()
        self.mock_get_agent_csr = MagicMock()
        self.mock_get_agent_info = MagicMock()
        self.mock_get_agent_stats = MagicMock()
        self.mock_get_connector = MagicMock()
        self.mock_get_connector_queue = MagicMock()
        self.mock_get_connector_queues = MagicMock()
        self.mock_get_connector_usage_metrics = MagicMock()
        self.mock_get_encrypted_data = MagicMock()
        self.mock_get_instance = MagicMock()
        self.mock_get_ipsec_connector = MagicMock()
        self.mock_get_ipsec_connector_info = MagicMock()
        self.mock_get_proxy = MagicMock()
        self.mock_get_queues = MagicMock()
        self.mock_get_service = MagicMock()
        self.mock_get_stats_config = MagicMock()
        self.mock_get_transfer = MagicMock()
        self.mock_list_agent_connector = MagicMock()
        self.mock_list_agent_csr = MagicMock()
        self.mock_list_connector = MagicMock()
        self.mock_list_connector_guid_mapping = MagicMock()
        self.mock_list_connector_stats = MagicMock()
        self.mock_list_instances = MagicMock()
        self.mock_list_ipsec_connector = MagicMock()
        self.mock_list_proxies = MagicMock()
        self.mock_list_services = MagicMock()
        self.mock_list_transfers = MagicMock()
        self.mock_replace_agent_connector = MagicMock()
        self.mock_replace_agent_connector_local_auth_info = MagicMock()
        self.mock_replace_agent_csr = MagicMock()
        self.mock_replace_encrypted_data = MagicMock()
        self.mock_replace_instance = MagicMock()
        self.mock_replace_ipsec_connector = MagicMock()
        self.mock_replace_proxy = MagicMock()
        self.mock_replace_transfer = MagicMock()

    def create_agent_connector(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.create_agent_connector with MagicMock.
        """
        return self.mock_create_agent_connector(self, *args, **kwargs)

    def create_agent_csr(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.create_agent_csr with MagicMock.
        """
        return self.mock_create_agent_csr(self, *args, **kwargs)

    def create_agent_stats(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.create_agent_stats with MagicMock.
        """
        return self.mock_create_agent_stats(self, *args, **kwargs)

    def create_configure_publishing_request(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.create_configure_publishing_request with MagicMock.
        """
        return self.mock_create_configure_publishing_request(self, *args, **kwargs)

    def create_connector_proxy(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.create_connector_proxy with MagicMock.
        """
        return self.mock_create_connector_proxy(self, *args, **kwargs)

    def create_csr(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.create_csr with MagicMock.
        """
        return self.mock_create_csr(self, *args, **kwargs)

    def create_instance(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.create_instance with MagicMock.
        """
        return self.mock_create_instance(self, *args, **kwargs)

    def create_ipsec_connector(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.create_ipsec_connector with MagicMock.
        """
        return self.mock_create_ipsec_connector(self, *args, **kwargs)

    def create_queue(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.create_queue with MagicMock.
        """
        return self.mock_create_queue(self, *args, **kwargs)

    def create_service(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.create_service with MagicMock.
        """
        return self.mock_create_service(self, *args, **kwargs)

    def create_transfer(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.create_transfer with MagicMock.
        """
        return self.mock_create_transfer(self, *args, **kwargs)

    def delete_agent_connector(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.delete_agent_connector with MagicMock.
        """
        return self.mock_delete_agent_connector(self, *args, **kwargs)

    def delete_connector(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.delete_connector with MagicMock.
        """
        return self.mock_delete_connector(self, *args, **kwargs)

    def delete_connector_queue(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.delete_connector_queue with MagicMock.
        """
        return self.mock_delete_connector_queue(self, *args, **kwargs)

    def delete_instance(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.delete_instance with MagicMock.
        """
        return self.mock_delete_instance(self, *args, **kwargs)

    def delete_ipsec_connector(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.delete_ipsec_connector with MagicMock.
        """
        return self.mock_delete_ipsec_connector(self, *args, **kwargs)

    def delete_proxy(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.delete_proxy with MagicMock.
        """
        return self.mock_delete_proxy(self, *args, **kwargs)

    def delete_service(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.delete_service with MagicMock.
        """
        return self.mock_delete_service(self, *args, **kwargs)

    def delete_transfer(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.delete_transfer with MagicMock.
        """
        return self.mock_delete_transfer(self, *args, **kwargs)

    def get_agent_connector(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_agent_connector with MagicMock.
        """
        return self.mock_get_agent_connector(self, *args, **kwargs)

    def get_agent_connector_dynamic_stats(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_agent_connector_dynamic_stats with MagicMock.
        """
        return self.mock_get_agent_connector_dynamic_stats(self, *args, **kwargs)

    def get_agent_csr(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_agent_csr with MagicMock.
        """
        return self.mock_get_agent_csr(self, *args, **kwargs)

    def get_agent_info(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_agent_info with MagicMock.
        """
        return self.mock_get_agent_info(self, *args, **kwargs)

    def get_agent_stats(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_agent_stats with MagicMock.
        """
        return self.mock_get_agent_stats(self, *args, **kwargs)

    def get_connector(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_connector with MagicMock.
        """
        return self.mock_get_connector(self, *args, **kwargs)

    def get_connector_queue(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_connector_queue with MagicMock.
        """
        return self.mock_get_connector_queue(self, *args, **kwargs)

    def get_connector_queues(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_connector_queues with MagicMock.
        """
        return self.mock_get_connector_queues(self, *args, **kwargs)

    def get_connector_usage_metrics(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_connector_usage_metrics with MagicMock.
        """
        return self.mock_get_connector_usage_metrics(self, *args, **kwargs)

    def get_encrypted_data(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_encrypted_data with MagicMock.
        """
        return self.mock_get_encrypted_data(self, *args, **kwargs)

    def get_instance(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_instance with MagicMock.
        """
        return self.mock_get_instance(self, *args, **kwargs)

    def get_ipsec_connector(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_ipsec_connector with MagicMock.
        """
        return self.mock_get_ipsec_connector(self, *args, **kwargs)

    def get_ipsec_connector_info(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_ipsec_connector_info with MagicMock.
        """
        return self.mock_get_ipsec_connector_info(self, *args, **kwargs)

    def get_proxy(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_proxy with MagicMock.
        """
        return self.mock_get_proxy(self, *args, **kwargs)

    def get_queues(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_queues with MagicMock.
        """
        return self.mock_get_queues(self, *args, **kwargs)

    def get_service(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_service with MagicMock.
        """
        return self.mock_get_service(self, *args, **kwargs)

    def get_stats_config(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_stats_config with MagicMock.
        """
        return self.mock_get_stats_config(self, *args, **kwargs)

    def get_transfer(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.get_transfer with MagicMock.
        """
        return self.mock_get_transfer(self, *args, **kwargs)

    def list_agent_connector(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.list_agent_connector with MagicMock.
        """
        return self.mock_list_agent_connector(self, *args, **kwargs)

    def list_agent_csr(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.list_agent_csr with MagicMock.
        """
        return self.mock_list_agent_csr(self, *args, **kwargs)

    def list_connector(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.list_connector with MagicMock.
        """
        return self.mock_list_connector(self, *args, **kwargs)

    def list_connector_guid_mapping(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.list_connector_guid_mapping with MagicMock.
        """
        return self.mock_list_connector_guid_mapping(self, *args, **kwargs)

    def list_connector_stats(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.list_connector_stats with MagicMock.
        """
        return self.mock_list_connector_stats(self, *args, **kwargs)

    def list_instances(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.list_instances with MagicMock.
        """
        return self.mock_list_instances(self, *args, **kwargs)

    def list_ipsec_connector(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.list_ipsec_connector with MagicMock.
        """
        return self.mock_list_ipsec_connector(self, *args, **kwargs)

    def list_proxies(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.list_proxies with MagicMock.
        """
        return self.mock_list_proxies(self, *args, **kwargs)

    def list_services(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.list_services with MagicMock.
        """
        return self.mock_list_services(self, *args, **kwargs)

    def list_transfers(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.list_transfers with MagicMock.
        """
        return self.mock_list_transfers(self, *args, **kwargs)

    def replace_agent_connector(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.replace_agent_connector with MagicMock.
        """
        return self.mock_replace_agent_connector(self, *args, **kwargs)

    def replace_agent_connector_local_auth_info(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.replace_agent_connector_local_auth_info with MagicMock.
        """
        return self.mock_replace_agent_connector_local_auth_info(self, *args, **kwargs)

    def replace_agent_csr(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.replace_agent_csr with MagicMock.
        """
        return self.mock_replace_agent_csr(self, *args, **kwargs)

    def replace_encrypted_data(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.replace_encrypted_data with MagicMock.
        """
        return self.mock_replace_encrypted_data(self, *args, **kwargs)

    def replace_instance(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.replace_instance with MagicMock.
        """
        return self.mock_replace_instance(self, *args, **kwargs)

    def replace_ipsec_connector(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.replace_ipsec_connector with MagicMock.
        """
        return self.mock_replace_ipsec_connector(self, *args, **kwargs)

    def replace_proxy(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.replace_proxy with MagicMock.
        """
        return self.mock_replace_proxy(self, *args, **kwargs)

    def replace_transfer(self, *args, **kwargs):
        """
        This method mocks the original api ConnectorsApi.replace_transfer with MagicMock.
        """
        return self.mock_replace_transfer(self, *args, **kwargs)

