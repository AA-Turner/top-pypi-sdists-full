"""Test the authentication process."""

import asyncio

import pytest

from elmax_api.exceptions import ElmaxBadLoginError
from elmax_api.http import ElmaxLocal, Elmax
from tests import LOCAL_TEST, LOCAL_API_URL, PANEL_PIN
from tests.conftest import async_init_test

BAD_USERNAME = "thisIsWrong@gmail.com"
BAD_PASSWORD = "fakePassword"


@pytest.mark.asyncio
async def test_wrong_credentials():
    client = Elmax(username=BAD_USERNAME, password=BAD_PASSWORD) if LOCAL_TEST != "true" else ElmaxLocal(
        panel_api_url=LOCAL_API_URL, panel_code=PANEL_PIN)
    with pytest.raises(ElmaxBadLoginError):
        await client.login()


@pytest.mark.asyncio
async def test_good_credentials():
    client = await async_init_test()
    jwt_data = await client.login()
    assert isinstance(jwt_data, dict)

    username = client.get_authenticated_username()
    assert username is not None


@pytest.mark.asyncio
async def test_token_renew():
    client = await async_init_test()
    jwt_data = await client.login()
    assert isinstance(jwt_data, dict)
    old_expiration = client.token_expiration_time

    await asyncio.sleep(60)

    new_jwt_data = await client.renew_token()
    assert isinstance(new_jwt_data, dict)
    new_expiration = client.token_expiration_time

    assert new_expiration >= old_expiration + 60

