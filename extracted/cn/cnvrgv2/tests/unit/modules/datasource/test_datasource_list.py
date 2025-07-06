import pytest
from tests.unit.modules.datasource.conftest import bucket_files_without_path1, bucket_files_without_path2, bucket_files


class TestDatasourceList:

    # Run the tests multiple times, with different params
    # List with different paths
    @pytest.mark.parametrize(
        "datasource_path, expected_result",
        [
            ('path1', bucket_files_without_path1),
            ('path2', bucket_files_without_path2),
            ('', bucket_files),
            ('path1/', bucket_files_without_path1),
            ('path2/', bucket_files_without_path2),
            ('/', bucket_files),

        ],
        ids=['1 - path1',
             '2 - path2',
             '3 - no path',
             '4 - path1/',
             '5 - path2/',
             '6 - /'
             ]
    )
    def test_list_objects(self, datasource, mock_datasource_client, mock_datasource_client_paginator,
                          datasource_path, expected_result):
        """
        Parametrized test for testing list_objects with different paths and expected results.
        """
        datasource.path = datasource_path

        result = list(datasource.list_objects(page_size=100))

        # Assert that the result matches the expected files for the provided path
        assert result == expected_result

        # Verify the correct paginator was created
        datasource.client.get_paginator.assert_called_once_with('list_objects_v2')
        datasource.client.get_paginator().paginate.assert_called_once_with(
            Bucket=datasource.bucket_name, Prefix=datasource.path,
            PaginationConfig={'PageSize': 100}
        )
