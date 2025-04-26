from contextlib import suppress

import pytest as pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.notification_integration import NotificationEmail, NotificationIntegration
from tests.integ.utils import random_string


# Note: all secret looking things in this file are made up

pytestmark = [
    # All tests in this file need this Snowflake version
    pytest.mark.min_sf_ver("8.36.0"),
    pytest.mark.internal_only,
]


@pytest.fixture()
@pytest.mark.use_accountadmin
def notification_integration_extended(notification_integrations, set_internal_params):

    names_list = []
    for _ in range(5):
        names_list.append(random_string(10, "test_notification_integration_iter_a_"))
    for _ in range(7):
        names_list.append(random_string(10, "test_notification_integration_iter_b_"))
    for _ in range(3):
        names_list.append(random_string(10, "test_notification_integration_iter_c_"))

    allowed_recipients = ["test1@snowflake.com", "test2@snowflake.com"]
    default_recipients = ["test1@snowflake.com"]
    default_subject = "test default subject"
    try:
        with set_internal_params({"ENABLE_LIMIT_RECIPIENTS_TO_SENDING_ACCOUNT": False}):
            for ni_name in names_list:
                new_integration = NotificationIntegration(
                    name=ni_name,
                    notification_hook=NotificationEmail(
                        allowed_recipients=allowed_recipients,
                        default_recipients=default_recipients,
                        default_subject=default_subject,
                    ),
                    enabled=True,
                )
                notification_integrations.create(new_integration)

        yield notification_integrations
    finally:
        for ni_name in names_list:
            with suppress(NotFoundError):
                notification_integrations[ni_name].drop()


def test_iter_raw(notification_integration_extended):
    assert len(list(notification_integration_extended.iter())) >= 15


def test_iter_like(notification_integration_extended):
    assert len(list(notification_integration_extended.iter(like="test_view_iter_"))) == 0
    assert len(list(notification_integration_extended.iter(like="test_notification_integration_iter_a_%%"))) == 5
    assert len(list(notification_integration_extended.iter(like="test_notification_integration_iter_b_%%"))) == 7
    assert len(list(notification_integration_extended.iter(like="test_notification_integration_iter_c_%%"))) == 3
