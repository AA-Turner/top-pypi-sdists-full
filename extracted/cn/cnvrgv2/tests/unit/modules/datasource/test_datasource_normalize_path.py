import pytest


class TestDatasourceNormalizePath:

    # Run the tests multiple times, with different params
    @pytest.mark.parametrize(
        "datasource_path, file_name, expected_file_name",
        [
            # Test case 1 file_name
            # case 1
            ('path1', 'file_name', 'path1/file_name'),
            # case 2
            ('path2/', 'file_name', 'path2/file_name'),
            # case 3
            ('', 'file_name', 'file_name'),
            # Test case 2 path/to/file_name (relative path)
            # case 4
            ('path1', 'path/to/file_name', 'path1/path/to/file_name'),
            # case 5
            ('path2/', 'path/to/file_name', 'path2/path/to/file_name'),
            # case 6
            ('', 'path/to/file_name', 'path/to/file_name'),
            # Test case 3 /path/to/file_name (absolute path)
            # case 7
            ('path1', '/path/to/file_name', 'path1/path/to/file_name'),
            # case 8
            ('path2/', '/path/to/file_name', 'path2/path/to/file_name'),
            # case 9
            ('', '/path/to/file_name', '/path/to/file_name'),
            # Test case 4 datasource path: '/'
            # case 10
            ('/', 'file_name', '/file_name'),
            # case 11
            ('/', 'path/to/file_name', '/path/to/file_name'),
            # case 12
            ('/', '/path/to/file_name', '/path/to/file_name'),
            # Test case 5 path1/path/to/file_name (path already containing path)
            # case 13
            ('path1', 'path1/path/to/file_name', 'path1/path1/path/to/file_name'),
            # case 14
            ('path2/', 'path2/path/to/file_name', 'path2/path2/path/to/file_name'),

        ],
        ids=[
            # Test case 1 file_name
            "1 - path1 & file_name",
            "2 - path2 & file_name",
            "3 - no path & file_name",
            # Test case 2 path/to/file_name
            "4 - path1 & path/to/file_name",
            "5 - path2 & path/to/file_name",
            "6 - no path & path/to/file_name",
            # Test case 3 /path/to/file_name (absolute path)
            "7 - path1 & /path/to/file_name",
            "8 - path2 & /path/to/file_name",
            "9 - no path & /path/to/file_name",
            # Test case 4 /path/to/file_name (absolute path)
            "10 - / & file_name",
            "11 - / & path/to/file_name",
            "12 - / & /path/to/file_name",
            "13 - / & path1/path/to/file_name",
            "14 - / & path2/path/to/file_name",
             ]
    )
    def test_normalize_file_path(self, datasource, mock_datasource_client,
                                 datasource_path,  file_name, expected_file_name):
        datasource.path = datasource_path
        normalized_file_name = datasource._normalize_file_path(file_path=file_name)
        assert normalized_file_name == expected_file_name
