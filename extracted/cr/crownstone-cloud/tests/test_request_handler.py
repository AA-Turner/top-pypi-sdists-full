from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from crownstone_cloud.helpers.requests import RequestHandler
from crownstone_cloud import CrownstoneCloud
from tests.mocked_replies.errors import (
    auth_error,
    access_token_expired,
    not_verified
)
from crownstone_cloud.exceptions import CrownstoneAuthenticationError


class TestCrownstoneCloud(IsolatedAsyncioTestCase):
    """Test the request handler"""

    async def test_exceptions(self):
        cloud = CrownstoneCloud('email', 'password')

        # mock login with errors
        with self.assertRaises(CrownstoneAuthenticationError) as login_err:
            await cloud.request_handler.raise_on_error(auth_error)

        assert login_err.exception.type == 'LOGIN_FAILED'

        with self.assertRaises(CrownstoneAuthenticationError) as not_verified_err:
            await cloud.request_handler.raise_on_error(not_verified)

        assert not_verified_err.exception.type == 'LOGIN_FAILED_EMAIL_NOT_VERIFIED'

        await cloud.async_close_session()

    async def test_refresh_token(self):
        cloud = CrownstoneCloud('email', 'password')

        # mock access_token expired
        with patch.object(RequestHandler, 'request_login') as refresh_mock:
            result = await cloud.request_handler.raise_on_error(access_token_expired)

        assert result is True
        refresh_mock.assert_called()
        refresh_mock.assert_awaited()

        await cloud.async_close_session()
