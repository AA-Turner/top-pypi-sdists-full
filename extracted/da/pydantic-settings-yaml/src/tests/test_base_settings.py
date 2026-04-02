from pathlib import Path
from typing import List
from unittest.mock import Mock

import pytest
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict

from pydantic_settings_yaml import YamlBaseSettings
from pydantic_settings_yaml.base_settings import (
    replace_secrets,
    yaml_config_settings_source,
)


def test_replace_secrets():
    data = """
        database:
            password: <file:database_password>
            username: <file:database_username>
    """
    data = replace_secrets(Path("src/tests/data"), data)

    assert (
        data
        == """
        database:
            password: dummy_database_password
            username: dummy_database_username
    """
    )


def test_replace_two_secrets_on_one_line():
    data = """
        database_conn_str: <file:database_username>:<file:database_password>
    """
    data = replace_secrets(Path("src/tests/data"), data)

    assert (
        data
        == """
        database_conn_str: dummy_database_username:dummy_database_password
    """
    )


def test_missing_secret_file_error():
    data = """
        database_conn_str: <file:missing_secret>
    """
    with pytest.raises(FileNotFoundError):
        replace_secrets(Path("src/tests/data"), data)


@pytest.fixture()
def mocked_yamlbasesettings():
    settings = Mock()
    settings.model_config = SettingsConfigDict(
        secrets_dir="src/tests/data", yaml_file="src/tests/data/config.yaml"
    )
    return settings


def test_yaml_config_settings_source(mocked_yamlbasesettings):
    data = yaml_config_settings_source(mocked_yamlbasesettings)
    assert data == {
        "debug": True,
        "allowed_hosts": [{"name": "domain.com"}, {"name": "example.com"}],
        "database": {
            "password": "dummy_database_password",
            "user": {"username": "dummy_database_username"},
        },
    }


def test_yaml_config_settings_source_no_files(mocked_yamlbasesettings):
    mocked_yamlbasesettings.model_config["yaml_file"] = ""
    with pytest.raises(AssertionError):
        yaml_config_settings_source(mocked_yamlbasesettings)

    mocked_yamlbasesettings.model_config[
        "yaml_file"
    ] = "/src/tests/data/not_existing_config.yaml"
    with pytest.raises(FileNotFoundError):
        yaml_config_settings_source(mocked_yamlbasesettings)

    mocked_yamlbasesettings.model_config["yaml_file"] = "/src/tests/data/config.yaml"
    mocked_yamlbasesettings.model_config["secrets_dir"] = None
    with pytest.raises(AssertionError):
        yaml_config_settings_source(mocked_yamlbasesettings)


class User(BaseModel):
    username: str


class Database(BaseModel):
    user: User
    password: str


class Host(BaseModel):
    name: str


class Settings(YamlBaseSettings):
    debug: bool = False
    database: Database
    allowed_hosts: List[Host]

    model_config = SettingsConfigDict(
        secrets_dir="src/tests/data", yaml_file="src/tests/data/config.yaml"
    )


def test_yaml_base_settings():
    s = Settings()
    assert s.model_dump() == {
        "debug": True,
        "allowed_hosts": [{"name": "domain.com"}, {"name": "example.com"}],
        "database": {
            "password": "dummy_database_password",
            "user": {
                "username": "dummy_database_username",
            },
        },
    }
