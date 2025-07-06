import pytest
from tests.unit.modules.datasource.conftest import file_path


class TestDatasourceRemoveFile:

    def test_remove_file_success(self, datasource, mock_datasource_client, mock_normalize_file_path):
        normalized_path = mock_normalize_file_path.return_value
        datasource.client.delete_objects.return_value = {'Deleted': [{'Key': normalized_path}]}

        datasource.remove_file(file_path)

        datasource._normalize_file_path.assert_called_once_with(file_path)
        datasource.client.delete_objects.assert_called_once_with(
            Bucket=datasource.bucket_name,
            Delete={'Objects': [{'Key': normalized_path}]}
        )

    def test_remove_file_with_error(self, datasource, mock_datasource_client, mock_normalize_file_path):
        normalized_path = mock_normalize_file_path.return_value

        datasource.client.delete_objects.return_value = {
            'Errors': [{'Key': normalized_path, 'Message': 'ERROR!!!'}]
        }

        # Call the remove_file method and expect an exception
        with pytest.raises(Exception):
            datasource.remove_file(file_path)
