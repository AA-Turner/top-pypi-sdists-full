import unittest
from unittest.mock import patch
from cnvrgv2.config import error_messages
from cnvrgv2.errors import CnvrgArgumentsError
import pytest


class TestDatasourceClone:
    page_size = 50
    max_workers = 4

    @patch('cnvrgv2.modules.datasource.datasource.handle_dir_exist')
    @patch('os.path.isdir')
    def test_clone(self, mock_isdir,
                   mock_handle_dir_exist, datasource, mock_datasource_client, mock_datasource_files_downloader):
        # Clone with default params: skip_if_exists=False, force=False when datasource has not already been cloned
        # Datasource folder does not exist
        mock_isdir.return_value = False

        # Call the clone method

        datasource.clone(page_size=self.page_size, max_workers=self.max_workers, skip_if_exists=False, force=False)

        # Datasource should be cloned to datasource.slug folder
        destination_folder = datasource.slug
        mock_isdir.assert_called_once_with(destination_folder)
        mock_handle_dir_exist.assert_not_called()

        datasource.get_files_downloader.assert_called_once_with(
            page_size=self.page_size,
            max_workers=self.max_workers,
            destination_folder=destination_folder
        )
        # Ensure the downloader download_objects method is called for each page
        expected_calls = [unittest.mock.call(page) for page in datasource.get_files_downloader.page_iterator]
        datasource.get_files_downloader.download_objects.assert_has_calls(expected_calls, any_order=False)

    @patch('cnvrgv2.modules.datasource.datasource.handle_dir_exist')
    @patch('os.path.isdir')
    def test_clone_skip_if_exists(self, mock_isdir, mock_handle_dir_exist, datasource, mock_datasource_client,
                                  mock_datasource_files_downloader):
        # Clone with params: skip_if_exists=True, force=False when datasource has already been cloned
        # Datasource folder exists
        mock_isdir.return_value = True

        # Call the clone method with skip_if_exists=True
        datasource.clone(page_size=self.page_size, max_workers=self.max_workers, skip_if_exists=True, force=False)

        mock_isdir.assert_called_once_with(datasource.slug)
        mock_handle_dir_exist.assert_not_called()
        datasource.get_files_downloader.assert_not_called()

    @patch('cnvrgv2.modules.datasource.datasource.handle_dir_exist')
    @patch('os.path.isdir')
    def test_clone_force_delete(self, mock_isdir, mock_handle_dir_exist, datasource, mock_datasource_client,
                                mock_datasource_files_downloader):
        # Clone with params: skip_if_exists=False, force=True when datasource has already been cloned
        # Datasource folder exists
        mock_isdir.return_value = True

        # Call the clone method with force=True
        datasource.clone(page_size=self.page_size, max_workers=self.max_workers, skip_if_exists=False, force=True)

        # Assertions
        mock_isdir.assert_called_once_with(datasource.slug)
        mock_handle_dir_exist.assert_called_once_with(True, datasource.slug)

        datasource.get_files_downloader.assert_called_once_with(
            page_size=self.page_size,
            max_workers=self.max_workers,
            destination_folder=datasource.slug,
        )
        # Ensure the downloader download_objects method is called for each page
        expected_calls = [unittest.mock.call(page) for page in datasource.get_files_downloader.page_iterator]
        datasource.get_files_downloader.download_objects.assert_has_calls(expected_calls, any_order=False)

    @patch('cnvrgv2.modules.datasource.datasource.handle_dir_exist')
    @patch('os.path.isdir')
    def test_clone_args_error(self, mock_isdir, mock_handle_dir_exist, datasource, mock_datasource_client):
        # Clone with params: skip_if_exists=True, force=True - both cannot be set to True
        mock_isdir.return_value = True

        # Call the clone method with skip_if_exists=True and force=True (should raise error)
        with pytest.raises(CnvrgArgumentsError) as exception_info:
            datasource.clone(skip_if_exists=True, force=True)

        # Check if the exception message matches the expected error message
        assert error_messages.DATASOURCE_BAD_FORCE_ARGUMENTS in str(exception_info.value)

        # Assert handle_dir_exist was not called because of the error
        mock_handle_dir_exist.assert_not_called()
