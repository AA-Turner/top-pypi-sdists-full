from unittest.mock import MagicMock

class FeaturesApiMock:

    def __init__(self):
        self.mock_add_feature_tag = MagicMock()
        self.mock_delete_feature_tag = MagicMock()
        self.mock_get_feature_tag = MagicMock()
        self.mock_list_feature_tags = MagicMock()
        self.mock_replace_feature_tag = MagicMock()

    def add_feature_tag(self, *args, **kwargs):
        """
        This method mocks the original api FeaturesApi.add_feature_tag with MagicMock.
        """
        return self.mock_add_feature_tag(self, *args, **kwargs)

    def delete_feature_tag(self, *args, **kwargs):
        """
        This method mocks the original api FeaturesApi.delete_feature_tag with MagicMock.
        """
        return self.mock_delete_feature_tag(self, *args, **kwargs)

    def get_feature_tag(self, *args, **kwargs):
        """
        This method mocks the original api FeaturesApi.get_feature_tag with MagicMock.
        """
        return self.mock_get_feature_tag(self, *args, **kwargs)

    def list_feature_tags(self, *args, **kwargs):
        """
        This method mocks the original api FeaturesApi.list_feature_tags with MagicMock.
        """
        return self.mock_list_feature_tags(self, *args, **kwargs)

    def replace_feature_tag(self, *args, **kwargs):
        """
        This method mocks the original api FeaturesApi.replace_feature_tag with MagicMock.
        """
        return self.mock_replace_feature_tag(self, *args, **kwargs)

