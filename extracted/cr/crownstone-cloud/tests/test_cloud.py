"""Tests for the Crownstone Cloud library."""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import aiohttp

from crownstone_cloud import CrownstoneCloud
from crownstone_cloud.helpers.requests import RequestHandler
from crownstone_cloud.exceptions import CrownstoneAbilityError, AbilityError
from crownstone_cloud.cloud_models.spheres import Spheres
from crownstone_cloud.const import (
    DIMMING_ABILITY,
    TAP_TO_TOGGLE_ABILITY
)

from tests.mocked_replies.login_data import login_data
from tests.mocked_replies.sphere_data import (
    sphere_data,
    key_data,
    expected_key_data,
)
from tests.mocked_replies.crownstone_data import (
    crownstone_data,
)
from tests.mocked_replies.user_data import user_data
from tests.mocked_replies.location_data import (
    location_data_init,
    location_data_removed,
    presence_data
)


class TestCrownstoneCloud(IsolatedAsyncioTestCase):
    """Test the main class"""

    async def test_init(self):
        """Initialize test case."""
        cloud = CrownstoneCloud('email', 'password')
        assert isinstance(cloud.request_handler.client_session, aiohttp.ClientSession)

        await cloud.async_close_session()

    @patch.object(RequestHandler, 'request_login')
    @patch.object(CrownstoneCloud, 'async_synchronize')
    async def test_initialize(self, mock_sync, mock_request):
        """Test fetching the cloud data."""
        cloud = CrownstoneCloud('email', 'password')
        # patch the result of login request
        mock_request.return_value = login_data
        await cloud.async_initialize()
        assert cloud.access_token == 'my_access_token'
        assert cloud.cloud_data.user_id == 'user_id'
        assert mock_sync.call_count == 1

        await cloud.async_close_session()

    @patch.object(RequestHandler, 'get')
    async def test_data_structure(self, mock_request):
        """Test if data structure is correctly initialized with the cloud data."""
        cloud = CrownstoneCloud('email', 'password')
        # create fake instance
        cloud.spheres = Spheres(cloud, 'user_id')
        # add fake sphere data for test
        mock_request.return_value = sphere_data
        await cloud.spheres.async_update_sphere_data()
        mock_request.assert_awaited()

        # test getting a sphere by id and name
        sphere = cloud.spheres.find_by_id('my_awesome_sphere_id_2')
        assert sphere.cloud_id == 'my_awesome_sphere_id_2'
        sphere2 = cloud.spheres.find('my_awesome_sphere')
        assert sphere2.name == 'my_awesome_sphere'

        # test getting keys
        mock_request.return_value = key_data
        keys = await sphere.async_get_keys()
        mock_request.assert_awaited()
        assert keys == expected_key_data

        # add fake crownstone data for test
        mock_request.return_value = crownstone_data
        await sphere.crownstones.async_update_crownstone_data()
        mock_request.assert_awaited()

        # add fake user data for test
        mock_request.return_value = user_data
        await sphere.users.async_update_user_data()
        mock_request.assert_awaited()

        # add fake location data for test
        mock_request.return_value = location_data_init
        await sphere.locations.async_update_location_data()
        mock_request.assert_awaited()
        # presence
        mock_request.return_value = presence_data
        await sphere.locations.async_update_location_presence()
        mock_request.assert_awaited()

        # test getting crownstone, users, locations by id & name
        crownstone = sphere.crownstones.find('my_awesome_crownstone')
        crownstone_by_id = sphere.crownstones.find_by_id('my_awesome_crownstone_id_2')
        assert crownstone.name == 'my_awesome_crownstone'
        assert crownstone_by_id.cloud_id == 'my_awesome_crownstone_id_2'
        # test state
        assert crownstone.state == 0
        # test abilities
        assert crownstone_by_id.abilities.get(DIMMING_ABILITY).is_enabled is False
        assert crownstone_by_id.abilities.get(TAP_TO_TOGGLE_ABILITY).is_enabled is True

        location = sphere.locations.find('my_awesome_location_1')
        location_by_id = sphere.locations.find_by_id('my_awesome_location_id_3')
        assert location.cloud_id == 'my_awesome_location_id_1'
        assert location_by_id.name == 'my_awesome_location_3'
        # test presence
        assert len(location.present_people) == 1
        assert len(location_by_id.present_people) == 1

        mock_request.return_value = location_data_removed
        await sphere.locations.async_update_location_data()
        # test when the location data gets updated
        assert 'my_awesome_location_id_2' not in sphere.locations.data
        assert 'my_awesome_location_id_3' in sphere.locations.data

        mock_request.return_value = location_data_init
        await sphere.locations.async_update_location_data()
        # test when the presence data gets updated
        assert 'my_awesome_location_id_2' in sphere.locations.data

        user_first = sphere.users.find_by_first_name('I am')
        user_last = sphere.users.find_by_last_name('Awesome')
        user_by_id = sphere.users.find_by_id('we_are_awesome_id')
        assert 'You are' and 'We are' not in user_first
        assert len(user_last) == 3
        assert user_by_id.first_name == 'We are'
        assert user_by_id.last_name == 'Awesome'

        # test setting brightness of a crownstone
        with patch.object(RequestHandler, 'put') as brightness_mock:
            # test if it doesn't run if dimming not enabled
            with self.assertRaises(CrownstoneAbilityError) as ability_err:
                await crownstone_by_id.async_set_brightness(50)

            assert ability_err.exception.type == AbilityError['NOT_ENABLED']
            brightness_mock.assert_not_called()
            # test error when wrong value is given
            with self.assertRaises(ValueError):
                await crownstone.async_set_brightness(101)

        await cloud.async_close_session()
