import os

import pytest
import yaml

from cnvrgv2.config import Config
from cnvrgv2.config import CONFIG_FOLDER_NAME
from cnvrgv2.data import FileDownloader
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.base.data_owner import DataOwner
from cnvrgv2.modules.project import Project
from cnvrgv2.proxy import Proxy


class MockResponse:
    def __init__(self, status, json):
        self.status_code = status
        self._json = json

    def json(self):
        return self._json


class MockFileHandler:
    def __init__(self):
        self.in_progress = False
        self.errors = []


class TestProject:
    def test_delete_project_with_slug(self, mocker, empty_context):
        slug = "test-slug"

        def mock_call_api_get(*args, **kwargs):
            return {
                "data": {
                    "id": "17",
                    "type": "project",
                    "attributes": {
                        "title": "test-title",
                        "slug": slug,
                        "git": False,
                        "start_commit": "b6692ea5df920cad691c20319a6fffd7a4a766b8",
                        "commit": "5b384ce32d8cdef02bc3a139d4cac0a22bb029e8"
                    }
                }
            }

        mocker.patch.object(Proxy, 'call_api', side_effect=mock_call_api_get)
        project = Project(context=empty_context, slug=slug)

        mocked_delete = mocker.patch.object(Proxy, 'call_api')
        project.delete()
        assert mocked_delete.call_count == 1

    def test_validate_config(self, mocker, empty_context):
        test_slug = "real_slug"

        def mock_local_config_file_fake_slug(*args, **kwargs):
            return {
                "commit_sha1": "test-commit",
                "git": True,
                "project_slug": "fake_slug",
            }

        def mock_local_config_file_real_slug(*args, **kwargs):
            return {
                "commit_sha1": "test-commit",
                "git": True,
                "project_slug": test_slug,
            }

        mocker.patch("builtins.open", return_value=True)
        mocker.patch.object(os.path, "exists", return_value=True)
        mocker.patch.object(Config, "_load_legacy_config", lambda x: True)

        mocker.patch.object(yaml, "safe_load", mock_local_config_file_fake_slug)
        project = Project(context=empty_context, slug=test_slug)
        assert not project._validate_config_ownership()

        mocker.patch.object(yaml, "safe_load", mock_local_config_file_real_slug)
        project = Project(context=empty_context, slug=test_slug)
        assert project._validate_config_ownership()

    def test_fail_put_files_with_illegal_directory_name(self, mocker, empty_context):
        test_slug = "test_slug"

        mocker.patch('os.path.isdir', return_value=True)

        project = Project(context=empty_context, slug=test_slug)
        with pytest.raises(CnvrgArgumentsError):
            project.put_files(['~/illegal-directory-name/file.txt'])

    def test_put_files_success(self, mocker, empty_context):
        test_slug = "test_slug"
        file_name = '~/directory/file.txt'
        expected_sha1 = 'sha1_mock'

        mocker.patch('os.path.isfile', return_value=True)
        mocker.patch('os.path.isdir', return_value=False)
        mocker.patch('os.path.getsize', return_value=1)

        project = Project(context=empty_context, slug=test_slug)

        start_commit_mock = mocker.patch.object(DataOwner, '_start_commit', return_value=expected_sha1)
        end_commit_mock = mocker.patch.object(DataOwner, '_end_commit', return_value=expected_sha1)
        file_uploader_mock = mocker.patch.object(DataOwner, '_get_file_uploader',
                                                 return_value=self._get_mock_file_handler())

        result = project.put_files(file_name)
        assert result == expected_sha1
        assert start_commit_mock.call_count == 1
        assert end_commit_mock.call_count == 1
        assert file_uploader_mock.call_count == 1

    def _get_mock_file_handler(self):
        return MockFileHandler()

    def _get_mock_file_handler_with_errors(self):
        mock = MockFileHandler()
        mock.errors = [Exception()]

    def test_put_git_files(self, mocker, empty_context):
        test_slug = "test_slug"
        file_name = '~/directory/file.txt'
        expected_sha1 = 'sha1_mock'

        mocker.patch('os.path.isfile', return_value=True)
        mocker.patch('os.path.isdir', return_value=False)
        mocker.patch('os.path.getsize', return_value=1)

        mocker.patch.object(DataOwner, '_handle_git_files', return_value=[file_name])

        start_commit_mock = mocker.patch.object(DataOwner, '_start_commit', return_value=expected_sha1)
        end_commit_mock = mocker.patch.object(DataOwner, '_end_commit', return_value=expected_sha1)
        file_uploader_mock = mocker.patch.object(DataOwner, '_get_file_uploader',
                                                 return_value=self._get_mock_file_handler())

        project = Project(slug=test_slug, context=empty_context)
        result = project.put_files([], git_diff=True)

        assert result == expected_sha1
        assert start_commit_mock.call_count == 1
        assert end_commit_mock.call_count == 1
        assert file_uploader_mock.call_count == 1

    def test_put_files_on_upload(self, mocker, empty_context):
        test_slug = "test_slug"
        file_name = '~/directory/file.txt'
        expected_sha1 = 'sha1_mock'

        mocker.patch('os.path.isfile', return_value=True)
        mocker.patch('os.path.isdir', return_value=False)
        mocker.patch('os.path.getsize', return_value=1)
        reload_mock = mocker.patch('cnvrgv2.modules.base.data_owner.DataOwner.reload')

        project = Project(context=empty_context, slug=test_slug)

        start_commit_mock = mocker.patch.object(DataOwner, '_start_commit', return_value=expected_sha1)
        end_commit_mock = mocker.patch.object(DataOwner, '_end_commit', return_value=expected_sha1)
        file_uploader_mock = mocker.patch.object(DataOwner, '_get_file_uploader',
                                                 return_value=self._get_mock_file_handler())
        file_deleter_mock = mocker.patch.object(DataOwner, '_get_remote_file_deleter',
                                                return_value=self._get_mock_file_handler())

        result = project.put_files(file_name, upload=True)
        assert result == expected_sha1
        assert start_commit_mock.call_count == 1
        assert end_commit_mock.call_count == 1
        assert file_uploader_mock.call_count == 1
        assert file_deleter_mock.call_count == 1
        assert reload_mock.call_count == 1

    def test_clone(self, mocker, empty_context, tmpdir):
        working_dir = "./"
        test_slug = "real_slug"
        reload_mock = mocker.patch('cnvrgv2.modules.base.data_owner.DataOwner.reload')

        def mock_file_downloader_init(obj, *args, **kwargs):
            # Set the credentials variables:
            obj.commit_sha1 = 'commit_sha1'
            obj.errors = []

        def mock_get_attr(attr):
            return 'mocked_{0}'.format(attr)

        # If project folder already exists, and override set to false, should not download any file
        # (assert there was no call to file downloader)
        with mocker.patch('os.path.exists', side_effect={working_dir + test_slug: True,
                                                         working_dir + test_slug + '/' + CONFIG_FOLDER_NAME: True}.get):
            mocked_file_downloader_init = mocker.patch.object(FileDownloader, "__init__",
                                                              side_effect=mock_file_downloader_init)
            project = Project(context=empty_context, slug=test_slug)
            mocker.patch('os.path.isfile', return_value=True)
            mocker.patch('os.path.isdir', return_value=False)
            assert project.local_commit is None
            project.clone(progress_bar_enabled=False, override=False, commit=None)
            assert reload_mock.call_count == 1
            assert mocked_file_downloader_init.call_count == 0
            assert project.local_commit is None

        # If project folder does not exist, download files
        with mocker.patch('os.path.exists', side_effect={working_dir + test_slug: True,
                                                         working_dir + test_slug + '/' + CONFIG_FOLDER_NAME: False}.get
                          ):
            mocker.patch.object(FileDownloader, "__init__", mock_file_downloader_init)
            mocker.patch.object(FileDownloader, "in_progress", new_callable=mocker.PropertyMock, return_value=False)
            save_config_mock = mocker.patch('cnvrgv2.modules.project.Project.save_config')
            create_cnvrg_ignore_mock = mocker.patch('cnvrgv2.modules.base.data_owner.create_cnvrgignore')
            mocker.patch.object(DataOwner, '__getattr__', side_effect=mock_get_attr)
            project = Project(context=empty_context, slug=test_slug)
            mocker.patch('os.path.isfile', return_value=True)
            mocker.patch('os.path.isdir', return_value=False)
            assert project.local_commit is None
            project.clone(progress_bar_enabled=False, override=False, commit=None)
            assert reload_mock.call_count == 3
            assert project.local_commit == 'mocked_last_commit'
            assert save_config_mock.call_count == 1
            assert create_cnvrg_ignore_mock.call_count == 1
