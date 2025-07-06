import os
import yaml
import shutil
import pytest

from contextlib import contextmanager

from cnvrgv2.config import Config
from cnvrgv2.errors import CnvrgError


class TestConfig:
    @staticmethod
    def destroy_config():
        config = Config()
        # Destroy global config
        if os.path.exists(config.global_cnvrg_path):
            shutil.rmtree(config.global_cnvrg_path)

        # Destroy local config
        if os.path.exists(config.local_cnvrg_path):
            shutil.rmtree(config.local_cnvrg_path)

    @staticmethod
    @contextmanager
    def create_config(path, content):
        """
        Creates a config file context manager with cleanup
        @param path: The path of the config file
        @param content: the content of the config file
        @return: None
        """
        with open(path, "w+") as f:
            yaml.dump(content, f)

        yield
        os.remove(path)

    def test_init_empty_config_files(self, mocker):
        mocker.patch.object(Config, "global_config_exists", False)
        mocker.patch.object(Config, "_load_legacy_config", lambda x: True)

        config = Config()
        for key in Config.global_config_attributes.keys():
            assert getattr(config, key) is None

        for key in Config.local_config_attributes.keys():
            assert getattr(config, key) is None

    def test_init_global_config_files(self, mocker):
        global_config = {
            "organization": "test-org",
            "domain": "test-domain",
            "token": "test-token",
            "user": "test-user",
            "check_certificate": "test-cert",
            "keep_duration_days": "test-dur",
            "version": "test-version",
            "sso_version": "v2",
            "digest": "sha1"
        }

        # Set up that only global config is loaded
        mocker.patch.object(Config, "_load_legacy_config", lambda x: True)
        mocker.patch.object(Config, "_load_local_config", lambda x: True)

        # Create the global config
        global_config_path = os.getcwd() + "/.global.config"
        mocker.patch.object(Config, "global_config_exists", True)
        mocker.patch.object(Config, "global_config_file_path", global_config_path)

        with TestConfig.create_config(global_config_path, global_config):
            config = Config()

            for key in Config.global_config_attributes.keys():
                assert getattr(config, key) == global_config[key]

    def test_init_local_config_files(self, mocker):
        local_config = {
            "commit_sha1": "test-commit",
            "git": True,
            "project_slug": "test-project",
        }

        # Set up that only local config is loaded
        mocker.patch.object(Config, "_load_legacy_config", lambda x: True)
        mocker.patch.object(Config, "_load_global_config", lambda x: True)

        # Create the local config
        local_config_path = os.getcwd() + "/.local.config"
        mocker.patch.object(Config, "local_config_exists", True)
        mocker.patch.object(Config, "local_config_file_path", local_config_path)

        with TestConfig.create_config(local_config_path, local_config):
            config = Config()

            for key in local_config.keys():
                assert getattr(config, key) == local_config[key]

    def test_init_legacy_config_files(self, mocker, sample_netrc):
        # TODO: only checks local legacy config file
        legacy_config = {
            ":project_name": "test-commit",
            ":project_slug": "test-slug",
            ":owner": "test-org",
            ":git": True,
        }

        # Set up that only legacy config is loaded
        mocker.patch.object(Config, "_load_global_config", lambda x: True)
        mocker.patch.object(Config, "_load_local_config", lambda x: True)

        # Create the legacy config
        legacy_config_path = os.getcwd() + "/.legacy.config"
        mocker.patch.object(Config, "legacy_local_config_file_path", legacy_config_path)

        with TestConfig.create_config(legacy_config_path, legacy_config):
            config = Config()

            # Check fake netrc file
            assert config.user == "test@test.com"
            assert config.token == "sample_token"

            # Check config
            assert config.git == legacy_config[":git"]
            assert config.organization == legacy_config[":owner"]
            assert config.project_slug == legacy_config[":project_slug"]
            assert config.data_owner_slug == legacy_config[":project_slug"]
            assert config.dataset_slug is None

    def test_update_config_file(self, mocker):
        global_config = {
            "organization": "test-org",
            "domain": "test-domain",
        }
        local_config = {
            "commit_sha1": "test-commit",
            "git": "test-git",
        }

        test_global_cnvrg_path = os.path.join(os.path.expanduser("~"), ".cnvrg-test")
        mocker.patch("cnvrgv2.config.config.CONFIG_FOLDER_NAME", ".cnvrg-test")
        mocker.patch("cnvrgv2.config.config.GLOBAL_CNVRG_PATH", test_global_cnvrg_path)

        Config().update(**{**global_config, **local_config})

        try:
            config = Config()

            for key in global_config:
                assert getattr(config, key) == global_config[key]

            for key in local_config:
                assert getattr(config, key) == local_config[key]
        finally:
            # Clean files
            TestConfig.destroy_config()

    def test_save_config_file(self, mocker):
        global_config = {
            "organization": "test-org",
            "domain": "test-domain",
        }
        local_config = {
            "commit_sha1": "test-commit",
            "git": False,
        }

        mocker.patch("cnvrgv2.config.config.CONFIG_FOLDER_NAME", ".cnvrg-test")
        mocker.patch("cnvrgv2.config.config.GLOBAL_CNVRG_PATH", os.path.join(os.path.expanduser("~"), ".cnvrg-test"))

        try:
            config = Config()
            for key in global_config:
                setattr(config, key, global_config[key])
            for key in local_config:
                setattr(config, key, local_config[key])

            config.save()

            config = Config()
            for key in global_config:
                assert getattr(config, key) == global_config[key]

            for key in local_config:
                assert getattr(config, key) == local_config[key]
        finally:
            # Clean files
            TestConfig.destroy_config()

    def test_remove_config_fields(self, mocker):
        mocker.patch("cnvrgv2.config.config.CONFIG_FOLDER_NAME", ".cnvrg-test")
        mocker.patch("cnvrgv2.config.config.GLOBAL_CNVRG_PATH", os.path.join(os.path.expanduser("~"), ".cnvrg-test"))

        try:
            Config().update(**{"organization": "test-org"})

            config = Config()
            assert getattr(config, "organization") == "test-org"

            config.remove_config_fields("organization")

            config = Config()
            assert getattr(config, "organization") is None

        finally:
            # Clean files
            TestConfig.destroy_config()

    def test_remove_config_fields_invalid_field(self, mocker):
        config = Config()
        with pytest.raises(CnvrgError) as exception_info:
            config.remove_config_fields("fake")

        assert "fake" in str(exception_info.value)

    def test_get_credential_variables_empty(self, mocker):
        mocker.patch.object(Config, "_load_legacy_config", lambda x: True)
        mocker.patch("cnvrgv2.config.config.CONFIG_FOLDER_NAME", ".cnvrg-test")
        mocker.patch("cnvrgv2.config.config.GLOBAL_CNVRG_PATH", os.path.join(os.path.expanduser("~"), ".cnvrg-test"))

        config = Config()
        token, domain, user = config.get_credential_variables()
        assert token is False
        assert domain is False
        assert user is False

    def test_get_credential_variables_valid(self, mocker):
        global_config = {
            "domain": "test-domain",
            "token": "test-token",
            "user": "test-user",
        }

        mocker.patch.object(Config, "_load_legacy_config", lambda x: True)
        mocker.patch("cnvrgv2.config.config.CONFIG_FOLDER_NAME", ".cnvrg-test")
        mocker.patch("cnvrgv2.config.config.GLOBAL_CNVRG_PATH", os.path.join(os.path.expanduser("~"), ".cnvrg-test"))

        def mock_global_config_file(*args, **kwargs):
            return global_config

        mocker.patch.object(yaml, "safe_load", mock_global_config_file)
        mocker.patch.object(os.path, "exists", return_value=True)
        mocker.patch.object(Config, '_load_legacy_config', return_value=True)
        mocker.patch("builtins.open", return_value=True)

        config = Config()
        token, domain, user = config.get_credential_variables()
        assert token == "test-token"
        assert domain == "test-domain"
        assert user == "test-user"

    def test_get_data_owner_name(self, mocker):
        local_config = {"project_slug": "test-project"}

        def mock_local_config_file(*args, **kwargs):
            return local_config

        mocker.patch("cnvrgv2.config.config.CONFIG_FOLDER_NAME", ".cnvrg-test")
        mocker.patch("cnvrgv2.config.config.GLOBAL_CNVRG_PATH", os.path.join(os.path.expanduser("~"), ".cnvrg-test"))

        mocker.patch.object(yaml, "safe_load", mock_local_config_file)
        mocker.patch.object(os.path, "exists", return_value=True)
        mocker.patch.object(Config, '_load_legacy_config', return_value=True)
        mocker.patch("builtins.open", return_value=True)

        config = Config()
        assert config.project_slug == "test-project"
        assert config.data_owner_slug == "test-project"
