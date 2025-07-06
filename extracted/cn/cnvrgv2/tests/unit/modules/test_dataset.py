import os

import psutil
import pytest
import yaml

from cnvrgv2.config import Config, error_messages
from cnvrgv2.data import FileDownloader
from cnvrgv2.errors import CnvrgError, CnvrgNotEnoughSpaceError
from cnvrgv2.modules.commits.dataset_commit import DatasetCommit
from cnvrgv2.modules.dataset import Dataset
from cnvrgv2.proxy import Proxy
from cnvrgv2.utils.json_api_format import JAF


class TestDataset:
    def test_get_commit_valid_values(self, mocker, empty_context):
        dataset = Dataset(context=empty_context, slug="test-slug")

        commit = dataset.get_commit(sha_1="fake-sha1")
        assert type(commit) == DatasetCommit

    def test_get_commit_invalid_values(self, mocker, empty_context):
        dataset = Dataset(context=empty_context, slug="test-slug")

        with pytest.raises(CnvrgError):
            dataset.get_commit(sha_1=1)

    def test_dataset_as_request_params(self, mocker, empty_context):
        slug = "test-slug"

        mocker.patch.object(Proxy, 'call_api')

        dataset = Dataset(context=empty_context, slug=slug)
        as_params = dataset.as_request_params()
        assert as_params['slug']

    def test_delete_dataset(self, mocker, empty_context):
        slug = "test-slug"

        dataset = Dataset(context=empty_context, slug=slug)

        mocked_delete = mocker.patch.object(Proxy, 'call_api')
        dataset.delete()
        assert mocked_delete.call_count == 1

    def test_validate_config(self, mocker, empty_context):
        test_slug = "real_slug"

        def mock_local_config_file_fake_slug(*args, **kwargs):
            return {
                "commit_sha1": "test-commit",
                "git": True,
                "dataset_slug": "fake_slug",
            }

        def mock_local_config_file_real_slug(*args, **kwargs):
            return {
                "commit_sha1": "test-commit",
                "git": True,
                "dataset_slug": test_slug,
            }

        mocker.patch("builtins.open", return_value=True)
        mocker.patch.object(os.path, "exists", return_value=True)
        mocker.patch.object(Config, "_load_legacy_config", lambda x: True)

        mocker.patch.object(yaml, "safe_load", mock_local_config_file_fake_slug)
        dataset = Dataset(context=empty_context, slug=test_slug)
        assert not dataset._validate_config_ownership()

        mocker.patch.object(yaml, "safe_load", mock_local_config_file_real_slug)
        dataset = Dataset(context=empty_context, slug=test_slug)
        assert dataset._validate_config_ownership()

    def test_verify(self, mocker, empty_context):
        test_slug = "slug_1"
        dataset = Dataset(context=empty_context, slug=test_slug)

        def mock_config_init(obj):
            obj.local_config = {}

        # Mock after dataset creation, otherwise it will fail
        mocker.patch.object(os, "getcwd", return_value='test_dir')
        mocker.patch.object(os.path, "isdir", return_value=False)
        assert not dataset.verify()

        mocker.patch.object(os, "getcwd", return_value='test_dir')
        mocker.patch.object(os.path, "isdir", return_value=True)
        mocker.patch.object(os, "chdir", return_value=True)
        mocker.patch.object(Config, "__init__", mock_config_init)
        mocker.patch.object(Config, "local_config_exists", True)
        assert dataset.verify()

        mocker.patch.object(os, "getcwd", return_value='test_dir')
        mocker.patch.object(os.path, "isdir", return_value=True)
        mocker.patch.object(os, "chdir", return_value=True)
        mocker.patch.object(Config, "__init__", mock_config_init)
        mocker.patch.object(Config, "local_config_exists", False)
        assert not dataset.verify()

    def test_clone_dataset_disk_has_no_space_error(self, empty_context, mocker, tmpdir):
        dataset = Dataset(context=empty_context, slug="test-slug")
        mocker.patch('cnvrgv2.modules.base.data_owner.DataOwner.reload')

        def mock_file_downloader_init(obj, *args, **kwargs):
            obj.commit_sha1 = 'commit_sha1'
            obj.errors = []

        def mock_call_api(*args, **kwargs):
            response = {
                "data": {
                    "id": "17",
                    "type": "dataset",
                    "attributes": {
                        "commit_size": 950,
                    }
                }
            }
            return JAF(response=response)

        mocker.patch.object(FileDownloader, "__init__", mock_file_downloader_init)
        mocker.patch.object(FileDownloader, "in_progress", new_callable=mocker.PropertyMock, return_value=False)
        mocker.patch.object(Proxy, "call_api", side_effect=mock_call_api)
        mocker.patch.object(psutil, 'disk_usage',
                            return_value=psutil._common.sdiskusage(free=650, used=0, total=0, percent=0))

        os.chdir(tmpdir.strpath)
        with pytest.raises(CnvrgNotEnoughSpaceError) as exception_info:
            dataset.clone(commit="test-commit")

        assert error_messages.NOT_ENOUGH_SPACE in str(exception_info.value)
