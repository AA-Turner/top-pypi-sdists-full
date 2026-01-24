import pytest
from selenium.webdriver.common.action_chains import ActionChains

from wbcore.contrib.authentication.factories import SuperUserFactory
from wbcore.contrib.authentication.models import User
from wbcore.contrib.example_app.factories import SportFactory
from wbcore.contrib.example_app.models import League
from wbcore.contrib.example_app.serializers import LeagueModelSerializer
from wbcore.contrib.example_app.tests.e2e import create_new_league_instance
from wbcore.test import (
    click_button_by_label,
    click_new_button,
    delete_list_entry,
    edit_list_instance,
    is_counter_as_expected,
    is_error_visible,
    is_string_not_visible,
    is_text_visible,
    open_menu_item,
    set_up,
)

USER_PASSWORD = "User_Password"


@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.django_db
class TestLeague:
    def test_create_edit_delete_league(self, live_server, selenium):
        # Creating a test user and login to the WB
        user: User = SuperUserFactory.create(plaintext_password=USER_PASSWORD)
        actions = ActionChains(selenium, 1000)
        set_up(selenium, live_server, user.email, USER_PASSWORD)

        # -----> CREATE A NEW LEAGUE <----- #
        sport = SportFactory.create()
        league_a = create_new_league_instance(
            selenium, ["name", "sport", "established_date", "points_per_win"], sport, False
        )
        open_menu_item(selenium, "Leagues", perform_mouse_move=True)

        assert is_counter_as_expected(selenium, League.objects.count())
        assert is_text_visible(selenium, league_a.name)

        # Trying to create a league without filling out anything -> We expect an error to be thrown.
        click_new_button(selenium)
        assert is_text_visible(selenium, "Create League")
        click_button_by_label(selenium, "Save and close")
        assert is_error_visible(selenium)

        league_b = create_new_league_instance(
            selenium, ["name", "sport", "established_date", "points_per_win"], sport, True
        )

        assert is_counter_as_expected(selenium, League.objects.count())
        assert is_text_visible(selenium, league_b.name)

        # ------> EDIT A NEW LEAGUE <------ #

        edit_list_instance(selenium, actions, league_a.name, LeagueModelSerializer(league_a), {"name": "Fun League"})
        assert is_string_not_visible(selenium, league_a.name)
        assert is_text_visible(selenium, "Fun League")
        assert is_counter_as_expected(selenium, League.objects.count())

        # -----> Delete <----- #

        delete_list_entry(selenium, actions, league_b.name)
        assert is_counter_as_expected(selenium, League.objects.count())
        assert is_text_visible(selenium, "Fun League")
        assert is_string_not_visible(selenium, league_b.name)
