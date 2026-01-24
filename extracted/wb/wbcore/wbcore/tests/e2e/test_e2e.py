import pytest

from wbcore.contrib.authentication.factories import SuperUserFactory
from wbcore.contrib.authentication.models import User
from wbcore.test import find_element, login

USER_PASSWORD = "User_Password"


@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.django_db
class TestE2ELogin:
    def test_login_success(self, live_server, selenium):
        user: User = SuperUserFactory(plaintext_password=USER_PASSWORD)  # noqa
        selenium.get(live_server.url)
        assert not find_element(selenium, "//div[contains(@class, 'sidebar')]")
        login(selenium, user.email, USER_PASSWORD)
        assert find_element(selenium, "//div[contains(@class, 'sidebar')]")

    def test_login_failure(self, live_server, selenium):
        user: User = SuperUserFactory(plaintext_password=USER_PASSWORD)  # noqa
        selenium.get(live_server.url)
        assert not find_element(selenium, "//p[@type='error']")
        login(selenium, user.email + "Wrong Name", USER_PASSWORD)
        assert find_element(selenium, "//p[@type='error']")
