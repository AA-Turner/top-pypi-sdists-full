import datetime as dt
from typing import NamedTuple, Optional

from memberaudit.tests.testdata.factories_2 import (
    CharacterFactory,
    CharacterOnlineStatusFactory,
)

from django.utils.timezone import now

from app_utils.testing import NoSocketsTestCase

from inactivity import core
from inactivity.tests.factories import UserMainRequestorFactory


class TestCheckUserActive(NoSocketsTestCase):
    def test_should_report_whether_user_is_active(self):
        # given

        class Case(NamedTuple):
            name: str
            last_login: Optional[dt.datetime]
            last_logout: Optional[dt.datetime]
            want: bool

        _now = now()
        cases = [
            Case(
                name="logged out after threshold",
                last_login=_now - dt.timedelta(hours=24),
                last_logout=_now - dt.timedelta(hours=20),
                want=True,
            ),
            Case(
                name="logged in recently, is still online and no logout data",
                last_login=_now - dt.timedelta(hours=24),
                last_logout=None,
                want=True,
            ),
            Case(
                name="logged in recently, still online and recent logout",
                last_login=_now - dt.timedelta(hours=24),
                last_logout=_now - dt.timedelta(days=2),
                want=True,
            ),
            Case(
                name="logged in recently, still online and last logout before threshold",
                last_login=_now - dt.timedelta(hours=24),
                last_logout=_now - dt.timedelta(days=4),
                want=True,
            ),
            Case(
                name="logged out after threshold and no login data",
                last_login=None,
                last_logout=_now - dt.timedelta(days=1),
                want=True,
            ),
            Case(
                name="logged out before threshold and has login data",
                last_login=_now - dt.timedelta(days=5),
                last_logout=_now - dt.timedelta(days=5) + dt.timedelta(hours=4),
                want=False,
            ),
            Case(
                name="logged out before threshold and no login data",
                last_login=None,
                last_logout=_now - dt.timedelta(days=5) + dt.timedelta(hours=4),
                want=False,
            ),
            Case(
                name="no login data",
                last_login=None,
                last_logout=None,
                want=False,
            ),
            Case(
                name="logged in before threshold and no logout data",
                last_login=_now - dt.timedelta(days=4),
                last_logout=None,
                want=True,
            ),
            Case(
                name="logged in before threshold and last logout earlier",
                last_login=_now - dt.timedelta(days=4),
                last_logout=_now - dt.timedelta(days=10),
                want=True,
            ),
        ]

        threshold_date = _now.date() - dt.timedelta(days=3)

        for tc in cases:
            with self.subTest(name=tc.name):
                user = UserMainRequestorFactory()
                character = CharacterFactory(user=user)
                CharacterOnlineStatusFactory(
                    character=character,
                    last_login=tc.last_login,
                    last_logout=tc.last_logout,
                )

                # when
                got = core.check_user_active(user, threshold_date)

                # then
                self.assertEqual(got, tc.want)
