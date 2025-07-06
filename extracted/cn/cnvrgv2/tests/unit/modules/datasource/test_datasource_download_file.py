import pytest
from tests.unit.modules.datasource.conftest import file_path


class TestDatasourceDownload:

    # Run the tests multiple times, with different params
    # Download with destination being relative or absolute path
    @pytest.mark.parametrize(
        "destination_path",
        [
            '/local-folder/my-file.txt',
            'local-folder/my-file.txt',
        ],
        ids=['1 - absolute destination path',
             '2 - relative destination path']
    )
    def test_download(self, datasource, mock_datasource_client, mock_normalize_file_path,
                      mock_datasource_files_downloader, destination_path):

        datasource.download_file(file_path, destination_path)
        datasource._normalize_file_path.assert_called_once_with(file_path)

        # Assert that the S3 client download_file method was called with correct arguments
        datasource.client.download_file.assert_called_once_with(
            Bucket=datasource.bucket_name,
            Key=mock_normalize_file_path.return_value,
            Filename=destination_path
        )
