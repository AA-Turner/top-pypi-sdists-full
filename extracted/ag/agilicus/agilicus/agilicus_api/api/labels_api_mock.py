from unittest.mock import MagicMock

class LabelsApiMock:

    def __init__(self):
        self.mock_bulk_delete_labelled_objects = MagicMock()
        self.mock_create_labelled_object = MagicMock()
        self.mock_create_labelled_object_label = MagicMock()
        self.mock_create_object_label = MagicMock()
        self.mock_delete_labelled_object = MagicMock()
        self.mock_delete_labelled_object_label = MagicMock()
        self.mock_delete_object_label = MagicMock()
        self.mock_get_labelled_object = MagicMock()
        self.mock_get_object_label = MagicMock()
        self.mock_list_labelled_objects = MagicMock()
        self.mock_list_object_labels = MagicMock()
        self.mock_replace_labelled_object = MagicMock()
        self.mock_replace_object_label = MagicMock()

    def bulk_delete_labelled_objects(self, *args, **kwargs):
        """
        This method mocks the original api LabelsApi.bulk_delete_labelled_objects with MagicMock.
        """
        return self.mock_bulk_delete_labelled_objects(self, *args, **kwargs)

    def create_labelled_object(self, *args, **kwargs):
        """
        This method mocks the original api LabelsApi.create_labelled_object with MagicMock.
        """
        return self.mock_create_labelled_object(self, *args, **kwargs)

    def create_labelled_object_label(self, *args, **kwargs):
        """
        This method mocks the original api LabelsApi.create_labelled_object_label with MagicMock.
        """
        return self.mock_create_labelled_object_label(self, *args, **kwargs)

    def create_object_label(self, *args, **kwargs):
        """
        This method mocks the original api LabelsApi.create_object_label with MagicMock.
        """
        return self.mock_create_object_label(self, *args, **kwargs)

    def delete_labelled_object(self, *args, **kwargs):
        """
        This method mocks the original api LabelsApi.delete_labelled_object with MagicMock.
        """
        return self.mock_delete_labelled_object(self, *args, **kwargs)

    def delete_labelled_object_label(self, *args, **kwargs):
        """
        This method mocks the original api LabelsApi.delete_labelled_object_label with MagicMock.
        """
        return self.mock_delete_labelled_object_label(self, *args, **kwargs)

    def delete_object_label(self, *args, **kwargs):
        """
        This method mocks the original api LabelsApi.delete_object_label with MagicMock.
        """
        return self.mock_delete_object_label(self, *args, **kwargs)

    def get_labelled_object(self, *args, **kwargs):
        """
        This method mocks the original api LabelsApi.get_labelled_object with MagicMock.
        """
        return self.mock_get_labelled_object(self, *args, **kwargs)

    def get_object_label(self, *args, **kwargs):
        """
        This method mocks the original api LabelsApi.get_object_label with MagicMock.
        """
        return self.mock_get_object_label(self, *args, **kwargs)

    def list_labelled_objects(self, *args, **kwargs):
        """
        This method mocks the original api LabelsApi.list_labelled_objects with MagicMock.
        """
        return self.mock_list_labelled_objects(self, *args, **kwargs)

    def list_object_labels(self, *args, **kwargs):
        """
        This method mocks the original api LabelsApi.list_object_labels with MagicMock.
        """
        return self.mock_list_object_labels(self, *args, **kwargs)

    def replace_labelled_object(self, *args, **kwargs):
        """
        This method mocks the original api LabelsApi.replace_labelled_object with MagicMock.
        """
        return self.mock_replace_labelled_object(self, *args, **kwargs)

    def replace_object_label(self, *args, **kwargs):
        """
        This method mocks the original api LabelsApi.replace_object_label with MagicMock.
        """
        return self.mock_replace_object_label(self, *args, **kwargs)

