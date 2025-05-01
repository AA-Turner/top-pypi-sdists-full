from unittest.mock import MagicMock

class RegionsApiMock:

    def __init__(self):
        self.mock_add_cluster = MagicMock()
        self.mock_add_point_of_presence = MagicMock()
        self.mock_add_region = MagicMock()
        self.mock_delete_cluster = MagicMock()
        self.mock_delete_point_of_presence = MagicMock()
        self.mock_delete_region = MagicMock()
        self.mock_get_cluster = MagicMock()
        self.mock_get_point_of_presence = MagicMock()
        self.mock_get_region = MagicMock()
        self.mock_get_regional_locations = MagicMock()
        self.mock_list_clusters = MagicMock()
        self.mock_list_point_of_presences = MagicMock()
        self.mock_list_regions = MagicMock()
        self.mock_replace_cluster = MagicMock()
        self.mock_replace_point_of_presence = MagicMock()
        self.mock_replace_region = MagicMock()
        self.mock_routing_request = MagicMock()

    def add_cluster(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.add_cluster with MagicMock.
        """
        return self.mock_add_cluster(self, *args, **kwargs)

    def add_point_of_presence(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.add_point_of_presence with MagicMock.
        """
        return self.mock_add_point_of_presence(self, *args, **kwargs)

    def add_region(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.add_region with MagicMock.
        """
        return self.mock_add_region(self, *args, **kwargs)

    def delete_cluster(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.delete_cluster with MagicMock.
        """
        return self.mock_delete_cluster(self, *args, **kwargs)

    def delete_point_of_presence(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.delete_point_of_presence with MagicMock.
        """
        return self.mock_delete_point_of_presence(self, *args, **kwargs)

    def delete_region(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.delete_region with MagicMock.
        """
        return self.mock_delete_region(self, *args, **kwargs)

    def get_cluster(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.get_cluster with MagicMock.
        """
        return self.mock_get_cluster(self, *args, **kwargs)

    def get_point_of_presence(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.get_point_of_presence with MagicMock.
        """
        return self.mock_get_point_of_presence(self, *args, **kwargs)

    def get_region(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.get_region with MagicMock.
        """
        return self.mock_get_region(self, *args, **kwargs)

    def get_regional_locations(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.get_regional_locations with MagicMock.
        """
        return self.mock_get_regional_locations(self, *args, **kwargs)

    def list_clusters(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.list_clusters with MagicMock.
        """
        return self.mock_list_clusters(self, *args, **kwargs)

    def list_point_of_presences(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.list_point_of_presences with MagicMock.
        """
        return self.mock_list_point_of_presences(self, *args, **kwargs)

    def list_regions(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.list_regions with MagicMock.
        """
        return self.mock_list_regions(self, *args, **kwargs)

    def replace_cluster(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.replace_cluster with MagicMock.
        """
        return self.mock_replace_cluster(self, *args, **kwargs)

    def replace_point_of_presence(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.replace_point_of_presence with MagicMock.
        """
        return self.mock_replace_point_of_presence(self, *args, **kwargs)

    def replace_region(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.replace_region with MagicMock.
        """
        return self.mock_replace_region(self, *args, **kwargs)

    def routing_request(self, *args, **kwargs):
        """
        This method mocks the original api RegionsApi.routing_request with MagicMock.
        """
        return self.mock_routing_request(self, *args, **kwargs)

