from unittest.mock import patch
from tests.unit.modules.datasource.conftest import file_path


class TestDatasourceUpload:
    destination_path = 'destination_path'

    @patch('os.path.basename')
    def test_upload(self, mock_basename, empty_context, datasource, mock_datasource_client, mock_normalize_file_path):
        datasource.upload_file(file_path=file_path, destination_path=self.destination_path)

        datasource._normalize_file_path.assert_called_once_with(self.destination_path)
        datasource.client.upload_file.assert_called_once_with(
            Bucket=datasource.bucket_name,
            Filename=file_path,
            Key=mock_normalize_file_path.return_value
        )

    @patch('os.path.basename')
    def test_upload_destination_none(self, mock_basename, empty_context, datasource, mock_datasource_client,
                                     mock_normalize_file_path):
        datasource.upload_file(file_path=file_path, destination_path=None)

        datasource._normalize_file_path.assert_called_once_with(file_path)
        datasource.client.upload_file.assert_called_once_with(
            Bucket=datasource.bucket_name,
            Filename=file_path,
            Key=mock_normalize_file_path.return_value
        )

    @patch('os.path.basename')
    def test_upload_destination_not_provided(self, mock_basename, empty_context, datasource, mock_datasource_client,
                                             mock_normalize_file_path):
        datasource.upload_file(file_path=file_path)

        datasource._normalize_file_path.assert_called_once_with(file_path)
        datasource.client.upload_file.assert_called_once_with(
            Bucket=datasource.bucket_name,
            Filename=file_path,
            Key=mock_normalize_file_path.return_value
        )

    @patch('os.path.basename')
    def test_upload_destination_empty_str(self, mock_basename, empty_context, datasource, mock_datasource_client,
                                          mock_normalize_file_path):
        datasource.upload_file(file_path=file_path, destination_path='')

        datasource._normalize_file_path.assert_called_once_with(file_path)
        datasource.client.upload_file.assert_called_once_with(
            Bucket=datasource.bucket_name,
            Filename=file_path,
            Key=mock_normalize_file_path.return_value
        )
