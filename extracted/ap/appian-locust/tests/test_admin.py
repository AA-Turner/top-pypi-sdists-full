import unittest

from tests.mock_client import CustomLocust
from tests.mock_reader import read_mock_file
from appian_locust._admin import ADMIN_URI_PATH, _Admin
from appian_locust._interactor import _Interactor
from locust import Locust


class TestAdmin(unittest.TestCase):
    admin = read_mock_file("admin_console_landing_page.json")

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(Locust())
        setattr(self.custom_locust.client, "feature_flag", "")
        setattr(self.custom_locust.client, "feature_flag_extended", "")

        self.interactor = _Interactor(self.custom_locust.client, "")
        self.interactor.login(["", ""])
        self.admin_interactor: _Admin = _Admin(self.interactor)

        self.custom_locust.set_response(ADMIN_URI_PATH, 200, self.admin)

    def test_fetch_admin_json(self) -> None:
        # Given setup,
        # When:
        admin = self.admin_interactor.fetch_admin_json()

        # Then:
        self.assertEqual('/admin', admin['sail-navigation-bookmark-url'])
        self.assertEqual('/rest/a/applications/latest/app/admin', admin['sail-navigation-endpoint-url'])


if __name__ == '__main__':
    unittest.main()
