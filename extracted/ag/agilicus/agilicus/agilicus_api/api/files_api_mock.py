from unittest.mock import MagicMock

class FilesApiMock:

    def __init__(self):
        self.mock_add_file = MagicMock()
        self.mock_create_file_association = MagicMock()
        self.mock_create_file_association_clear_task = MagicMock()
        self.mock_create_file_template = MagicMock()
        self.mock_create_public_file_org_link = MagicMock()
        self.mock_delete_file = MagicMock()
        self.mock_delete_file_association = MagicMock()
        self.mock_delete_file_template = MagicMock()
        self.mock_delete_public_file_org_link = MagicMock()
        self.mock_get_download = MagicMock()
        self.mock_get_download_public = MagicMock()
        self.mock_get_file = MagicMock()
        self.mock_get_file_association = MagicMock()
        self.mock_get_file_template = MagicMock()
        self.mock_get_public_file_org_link = MagicMock()
        self.mock_list_file_associations = MagicMock()
        self.mock_list_file_templates = MagicMock()
        self.mock_list_files = MagicMock()
        self.mock_list_public_file_org_links = MagicMock()
        self.mock_render_file_template = MagicMock()
        self.mock_replace_file = MagicMock()
        self.mock_replace_file_template = MagicMock()
        self.mock_replace_public_file_org_link = MagicMock()
        self.mock_reupload_file = MagicMock()

    def add_file(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.add_file with MagicMock.
        """
        return self.mock_add_file(self, *args, **kwargs)

    def create_file_association(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.create_file_association with MagicMock.
        """
        return self.mock_create_file_association(self, *args, **kwargs)

    def create_file_association_clear_task(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.create_file_association_clear_task with MagicMock.
        """
        return self.mock_create_file_association_clear_task(self, *args, **kwargs)

    def create_file_template(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.create_file_template with MagicMock.
        """
        return self.mock_create_file_template(self, *args, **kwargs)

    def create_public_file_org_link(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.create_public_file_org_link with MagicMock.
        """
        return self.mock_create_public_file_org_link(self, *args, **kwargs)

    def delete_file(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.delete_file with MagicMock.
        """
        return self.mock_delete_file(self, *args, **kwargs)

    def delete_file_association(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.delete_file_association with MagicMock.
        """
        return self.mock_delete_file_association(self, *args, **kwargs)

    def delete_file_template(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.delete_file_template with MagicMock.
        """
        return self.mock_delete_file_template(self, *args, **kwargs)

    def delete_public_file_org_link(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.delete_public_file_org_link with MagicMock.
        """
        return self.mock_delete_public_file_org_link(self, *args, **kwargs)

    def get_download(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.get_download with MagicMock.
        """
        return self.mock_get_download(self, *args, **kwargs)

    def get_download_public(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.get_download_public with MagicMock.
        """
        return self.mock_get_download_public(self, *args, **kwargs)

    def get_file(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.get_file with MagicMock.
        """
        return self.mock_get_file(self, *args, **kwargs)

    def get_file_association(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.get_file_association with MagicMock.
        """
        return self.mock_get_file_association(self, *args, **kwargs)

    def get_file_template(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.get_file_template with MagicMock.
        """
        return self.mock_get_file_template(self, *args, **kwargs)

    def get_public_file_org_link(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.get_public_file_org_link with MagicMock.
        """
        return self.mock_get_public_file_org_link(self, *args, **kwargs)

    def list_file_associations(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.list_file_associations with MagicMock.
        """
        return self.mock_list_file_associations(self, *args, **kwargs)

    def list_file_templates(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.list_file_templates with MagicMock.
        """
        return self.mock_list_file_templates(self, *args, **kwargs)

    def list_files(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.list_files with MagicMock.
        """
        return self.mock_list_files(self, *args, **kwargs)

    def list_public_file_org_links(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.list_public_file_org_links with MagicMock.
        """
        return self.mock_list_public_file_org_links(self, *args, **kwargs)

    def render_file_template(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.render_file_template with MagicMock.
        """
        return self.mock_render_file_template(self, *args, **kwargs)

    def replace_file(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.replace_file with MagicMock.
        """
        return self.mock_replace_file(self, *args, **kwargs)

    def replace_file_template(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.replace_file_template with MagicMock.
        """
        return self.mock_replace_file_template(self, *args, **kwargs)

    def replace_public_file_org_link(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.replace_public_file_org_link with MagicMock.
        """
        return self.mock_replace_public_file_org_link(self, *args, **kwargs)

    def reupload_file(self, *args, **kwargs):
        """
        This method mocks the original api FilesApi.reupload_file with MagicMock.
        """
        return self.mock_reupload_file(self, *args, **kwargs)

