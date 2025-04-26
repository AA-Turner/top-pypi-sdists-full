import os
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import pytest

from mcli import config
from mcli.config import MCLI_DISABLE_UPGRADE_CHECK_ENV, FeatureFlag
from mcli.utils.utils_pypi import NeedsUpdateError, check_new_update_available
from mcli.version import Version


# Mock current version
@pytest.fixture
def mock_current_version(mocker):
    """Mock the current version the checker sees
    """

    def _mock_current_version(version_str: str):
        v = Version.from_string(version_str)
        from mcli.utils import utils_pypi
        mocker.patch.object(utils_pypi, '_current_version', v)

    return _mock_current_version


RELEASE_VERSION = '2.0.1'
ALPHA_VERSION = '2.0.1a1'


@pytest.fixture
def on_release(mock_current_version):
    """Current version is not an alpha release
    """
    mock_current_version(RELEASE_VERSION)


@pytest.fixture
def on_alpha(mock_current_version):
    """Current version is on an alpha release
    """
    mock_current_version(ALPHA_VERSION)


# Mock latest pypi
@pytest.fixture
def mock_pypi_version(mocker):
    """Mock the returned pypi versions. Returns a callable that can be used to set the pypi version
    """

    def _mock_pypy_version(version):

        class Resp():

            @staticmethod
            def json() -> Dict[str, Dict[str, Any]]:
                value = {'info': {'version': version}, 'releases': {version: None}}
                return value

        mocker.patch('requests.get', return_value=Resp())

    return _mock_pypy_version


# Default MCLI config
@pytest.fixture()
def needs_check(base_mcli_setup):
    """Update needs to be checked
    """
    conf = config.MCLIConfig.load_config()
    conf.last_update_check = datetime.now() - timedelta(days=config.UPDATE_CHECK_FREQUENCY_DAYS, minutes=1)
    conf.save_config()


@pytest.fixture()
def already_checked(base_mcli_setup):
    """Update doesn't need checking
    """
    conf = config.MCLIConfig.load_config()
    conf.last_update_check = datetime.now() - timedelta(days=config.UPDATE_CHECK_FREQUENCY_DAYS, minutes=-60)
    conf.save_config()


@contextmanager
def alpha_tester(tester: bool):
    conf = config.MCLIConfig.load_config()
    previous = conf.feature_flags.get(FeatureFlag.ALPHA_TESTER.value, False)
    conf.feature_flags[FeatureFlag.ALPHA_TESTER.value] = tester
    conf.save_config()
    yield
    conf.feature_flags[FeatureFlag.ALPHA_TESTER.value] = previous
    conf.save_config()


@contextmanager
def dev_mode(dev: bool):
    prior_env_mode = os.environ.get(config.MCLI_MODE_ENV, None)
    os.environ[config.MCLI_MODE_ENV] = 'DEV'
    yield
    if prior_env_mode:
        os.environ[config.MCLI_MODE_ENV] = prior_env_mode


def get_offset_version(current: str,
                       major: int = 0,
                       minor: int = 0,
                       patch: int = 0,
                       extras: Optional[str] = None) -> str:
    """Get a new version string, offset by the given values
    """
    v = Version.from_string(current)
    offset = Version(v.major + major, v.minor + minor, v.patch + patch, extras if extras is not None else v.extras)
    return str(offset).lstrip('v')


# Test already checked
def test_already_checked(already_checked, mock_pypi_version):
    mock_pypi_version('10.0.0')
    assert check_new_update_available() is None


# Test on current
@pytest.mark.parametrize('alpha', [False, True])
def test_on_current(needs_check, on_release, mock_pypi_version, alpha):
    with alpha_tester(alpha):
        mock_pypi_version(RELEASE_VERSION)
        assert check_new_update_available() is None


# Test patch off by 1
def test_patch_off_1(needs_check, on_release, mock_pypi_version):
    pypi_version = get_offset_version(RELEASE_VERSION, patch=1)
    mock_pypi_version(pypi_version)
    assert check_new_update_available() is None
    conf = config.MCLIConfig.load_config()
    print(conf.last_update_check)


# Test minor off by 1
def test_minor_off_1(needs_check, on_release, mock_pypi_version):
    with pytest.raises(NeedsUpdateError):
        pypi_version = get_offset_version(RELEASE_VERSION, minor=1)
        mock_pypi_version(pypi_version)
        assert check_new_update_available() is None


# Test major off by 1
def test_major_off_1(needs_check, on_release, mock_pypi_version):
    with pytest.raises(NeedsUpdateError):
        pypi_version = get_offset_version(RELEASE_VERSION, major=1)
        mock_pypi_version(pypi_version)
        assert check_new_update_available() is None


# Test alpha tester off by 1
@pytest.mark.parametrize('alpha', [False, True])
def test_new_alpha_build(needs_check, on_alpha, mock_pypi_version, alpha):
    pypi_version = get_offset_version(ALPHA_VERSION, extras='a2')
    mock_pypi_version(pypi_version)
    assert check_new_update_available() is None


# Test non-alpha tester on new alpha build
def test_non_alpha_user(needs_check, on_alpha, mock_pypi_version):
    pypi_version = get_offset_version(ALPHA_VERSION, patch=-1, extras='')
    mock_pypi_version(pypi_version)
    assert check_new_update_available() is None


# Test on old alpha build
@pytest.mark.parametrize('alpha', [False, True])
def test_old_alpha_build(needs_check, on_alpha, mock_pypi_version, alpha):
    mock_pypi_version(RELEASE_VERSION)  # RELEASE_VERSION is newer than ALPHA_VERSION
    assert check_new_update_available() is None


# Test dev mode always succeeds
@pytest.mark.parametrize('dev_version', [ALPHA_VERSION, RELEASE_VERSION, '1.0.0', '3.0.0'])
def test_dev_mode_always_succeeds(needs_check, on_release, mock_pypi_version, dev_version):
    with dev_mode(True):
        mock_pypi_version(dev_version)
        assert check_new_update_available() is None


def test_no_upgrade_override(monkeypatch, mock_pypi_version, mock_current_version):
    mock_pypi_version("9.9.9")
    mock_current_version("0.0.0")

    with pytest.raises(NeedsUpdateError):
        assert check_new_update_available() is None

    monkeypatch.setenv(MCLI_DISABLE_UPGRADE_CHECK_ENV, 'true')
    assert check_new_update_available() is None
