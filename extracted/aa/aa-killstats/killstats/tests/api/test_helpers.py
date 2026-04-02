# Django
from django.test import RequestFactory, TestCase
from django.urls import reverse

# Alliance Auth
from allianceauth.eveonline.models import EveCorporationInfo

# AA Killstats
from killstats.api.account_manager import AccountManager
from killstats.api.killstats.api_helper import get_alliances, get_corporations
from killstats.tests.testdata.load_allianceauth import load_allianceauth
from killstats.tests.testdata.utils import create_user_from_evecharacter

MODULE_PATH = "killstats.api.account_manager"


class TestApiHelpers(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_allianceauth()
        cls.factory = RequestFactory()

        cls.user, cls.char_owner = create_user_from_evecharacter(
            1001,
            permissions=[
                "killstats.basic_access",
            ],
        )
        cls.user2, _ = create_user_from_evecharacter(
            1002,
            permissions=[
                "killstats.basic_access",
            ],
        )
        cls.user3, _ = create_user_from_evecharacter(
            1003,
        )
        cls.user4, _ = create_user_from_evecharacter(
            1004,
        )
        cls.user5, _ = create_user_from_evecharacter(
            1005,
        )
        cls.corp = EveCorporationInfo.objects.get(corporation_id=2001)

    def test_get_main_and_alts_all_char_in_chars(self):
        # given
        request = self.factory.get("/")
        request.user = self.user

        expected_char_list = [
            1001,
            1002,
            1003,
            1004,
            1005,
        ]

        account = AccountManager()
        # when
        __, char_list = account.get_mains_alts()

        # then
        self.assertEqual(char_list, expected_char_list)

    def test_no_corp_or_ally(self):

        request = self.factory.get(reverse("killstats:index"))
        request.user = self.user

        corp_list = get_corporations(request)

        expected_data = []

        self.assertEqual(corp_list, expected_data)

        ally_list = get_alliances(request)

        expected_data = []

        self.assertEqual(ally_list, expected_data)
