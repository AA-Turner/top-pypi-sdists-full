from __future__ import annotations

import os
import time
from pathlib import Path

import polars_cloud.polars_cloud as pcr
import pytest
from polars_cloud import constants
from polars_cloud.constants import API_CLIENT

from tests.unit.utilities import access_token


@pytest.mark.forked
def test_login_hierarchy(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    # Override so it doesn't read from ~/.polars which might have an unrelated token
    monkeypatch.setenv(constants.ACCESS_TOKEN_PATH, str(tmp_path))

    with pytest.raises(
        pcr.AuthLoadError,
        match="Authentication token was not found\\.",
    ):
        API_CLIENT.authenticate(interactive=False)

    stored_token = access_token()
    for token in [
        constants.ACCESS_TOKEN_DEFAULT_NAME,
        constants.REFRESH_TOKEN_DEFAULT_NAME,
    ]:
        with (Path(str(os.getenv(constants.ACCESS_TOKEN_PATH))) / token).open(
            "w"
        ) as file:
            file.write(stored_token)

    assert API_CLIENT.get_auth_header() == f"Bearer {stored_token}"

    env_token = access_token()
    monkeypatch.setenv(constants.ACCESS_TOKEN, env_token)

    assert stored_token != env_token

    # Token loaded from the environment has the highest priority
    API_CLIENT.clear_authentication()
    assert API_CLIENT.get_auth_header() == f"Bearer {env_token}"


@pytest.mark.forked
def test_login_basic_no_secret(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    # Override so it doesn't read from ~/.polars which might have an unrelated token
    monkeypatch.setenv(constants.ACCESS_TOKEN_PATH, str(tmp_path))

    monkeypatch.setenv(constants.CLIENT_ID, "name")

    with pytest.raises(
        pcr.AuthLoadError,
        match="Authentication token was not found\\.",
    ):
        API_CLIENT.authenticate(interactive=False)


@pytest.mark.forked
def test_expired_token(monkeypatch: pytest.MonkeyPatch) -> None:
    older_time = time.time() - 5000
    monkeypatch.setattr(time, "time", lambda: older_time)

    env_token = access_token()
    monkeypatch.setenv(constants.ACCESS_TOKEN, env_token)

    with pytest.raises(
        pcr.AuthLoadError,
        match="The POLARS_CLOUD_ACCESS_TOKEN environment variable authentication token has expired",
    ):
        API_CLIENT.authenticate(interactive=False)


@pytest.mark.forked
def test_expired_disk_token_expired_refresh(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    # Override so it doesn't read from ~/.polars which might have an unrelated token
    monkeypatch.setenv(constants.ACCESS_TOKEN_PATH, str(tmp_path))

    older_time = time.time() - 5000
    monkeypatch.setattr(time, "time", lambda: older_time)

    tmp_path.mkdir(parents=True, exist_ok=True)
    with (tmp_path / constants.ACCESS_TOKEN_DEFAULT_NAME).open("w") as file:
        file.write(access_token())

    with (tmp_path / constants.REFRESH_TOKEN_DEFAULT_NAME).open("w") as file:
        file.write(access_token())

    with pytest.raises(
        pcr.AuthLoadError,
        match="The refresh token has expired\\.",
    ):
        API_CLIENT.authenticate(interactive=False)
