from configparser import ConfigParser
from importlib.metadata import version as get_version
from uuid import uuid4

import pytest
from pytest_console_scripts import ScriptRunner
from pytest_mock import MockerFixture
from requests_mock import Mocker as RequestsMocker

from montecarlodata.settings import MCD_DEFAULT_API_ENDPOINT


@pytest.fixture(scope="session")
def mcd_id() -> str:
    return str(uuid4())


@pytest.fixture(scope="session")
def mcd_token() -> str:
    return "facedeadbeef"


@pytest.fixture(scope="session")
def montecarlo_version() -> str:
    return get_version("montecarlodata")


@pytest.fixture(autouse=True)
def use_mock_configuration(mcd_id: str, mcd_token: str, mocker: MockerFixture) -> None:
    def mock_parser() -> ConfigParser:
        info = {"mcd_id": mcd_id, "mcd_token": mcd_token}
        parser = ConfigParser()
        parser.add_section("default")
        for key, value in info.items():
            parser.set("default", key, value)
        return parser

    mocker.patch("montecarlodata.config.configparser.ConfigParser", new=mock_parser)


def test_version(script_runner: ScriptRunner, montecarlo_version: str) -> None:
    result = script_runner.run(["montecarlo", "--version"])

    assert result.returncode == 0
    assert result.stderr == ""
    assert f"montecarlo, version {montecarlo_version}" in result.stdout


def test_help(script_runner: ScriptRunner) -> None:
    result = script_runner.run(["montecarlo", "--help"])

    assert result.returncode == 0
    assert result.stderr == ""
    assert "Usage" in result.stdout
    assert "Monte Carlo's CLI." in result.stdout


def test_validate(script_runner: ScriptRunner, requests_mock: RequestsMocker) -> None:
    requests_mock.post(
        MCD_DEFAULT_API_ENDPOINT,
        json={
            "data": {
                "getUser": {
                    "firstName": "Test",
                    "lastName": "Runner",
                },
            },
        },
    )

    result = script_runner.run(["montecarlo", "validate"])

    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == "Hi, Test! All is well.\n"
