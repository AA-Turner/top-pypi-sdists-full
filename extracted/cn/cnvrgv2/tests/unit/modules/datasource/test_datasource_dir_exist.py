import shutil
import tempfile
from unittest.mock import patch
import pytest
from cnvrgv2.config import error_messages
from cnvrgv2.errors import CnvrgAlreadyClonedError
from cnvrgv2.modules.datasource.datasource_operations import handle_dir_exist


class TestHandleDirExist:
    @pytest.fixture(scope="function")
    def setup_directory(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @patch('shutil.rmtree')
    def test_handle_dir_exist_force_true(self, mock_rmtree):
        path = 'test/path'
        handle_dir_exist(force=True, path=path)
        # Assert that shutil.rmtree was called with the correct path
        mock_rmtree.assert_called_once_with(path)

    @patch('shutil.rmtree')
    def test_handle_dir_exist_force_false(self, mock_rmtree):
        path = 'test/path'
        with pytest.raises(CnvrgAlreadyClonedError) as exception_info:
            handle_dir_exist(force=False, path=path)

        # Check if the exception message matches the expected error message
        assert error_messages.DATASOURCE_ALREADY_CLONED in str(exception_info.value)

    # this is e2e tests
    # def test_handle_dir_exist_force(self, setup_directory):
    #     # Create a subdirectory to test force deletion
    #     sub_dir = os.path.join(setup_directory, "test_sub_dir")
    #     os.mkdir(sub_dir)
    #     assert os.path.isdir(sub_dir)
    #
    #     # Call the function with force=True
    #     handle_dir_exist(force=True, path=sub_dir)
    #
    #     # Ensure the directory is deleted
    #     assert not os.path.exists(sub_dir)
    #
    # def test_handle_dir_exist_no_force(self, setup_directory):
    #     # Create a subdirectory to test non-force behavior
    #     sub_dir = os.path.join(setup_directory, "test_sub_dir")
    #     os.mkdir(sub_dir)
    #     assert os.path.isdir(sub_dir)
    #
    #     # Call the function with force=False and expect an exception
    #     with pytest.raises(CnvrgAlreadyClonedError) as excinfo:
    #         handle_dir_exist(force=False, path=sub_dir)
    #
    #     # Ensure the directory still exists
    #     assert os.path.isdir(sub_dir)
    #     assert str(excinfo.value) == "The datasource is already cloned"
