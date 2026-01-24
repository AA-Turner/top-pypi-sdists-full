import pytest
from selenium.webdriver.common.action_chains import ActionChains

from wbcore.contrib.authentication.factories import SuperUserFactory
from wbcore.contrib.authentication.models import User
from wbcore.contrib.example_app.models import Team
from wbcore.contrib.example_app.serializers import TeamModelSerializer
from wbcore.contrib.example_app.tests.e2e import create_new_team_instance
from wbcore.test import (
    click_new_button,
    delete_list_entry,
    edit_list_instance,
    is_counter_as_expected,
    is_string_not_visible,
    is_text_visible,
    open_menu_item,
    set_up,
)

USER_PASSWORD = "User_Password"


@pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.django_db
class TestTeam:
    def test_create_edit_delete_team(self, live_server, selenium):
        # Creating a test user and login to the WB
        user: User = SuperUserFactory.create(plaintext_password=USER_PASSWORD)  # noqa
        actions = ActionChains(selenium, 1000)
        set_up(selenium, live_server, user.email, USER_PASSWORD)

        # -----> CREATE A NEW TEAM <----- #
        team_a = create_new_team_instance(selenium, ["name", "founded_date"], False)
        open_menu_item(selenium, "Teams", perform_mouse_move=True)

        assert is_counter_as_expected(selenium, Team.objects.count())
        assert is_text_visible(selenium, team_a.name)
        click_new_button(selenium)
        assert is_text_visible(selenium, "Create Team")
        team_b = create_new_team_instance(selenium, ["name", "founded_date"], True)

        assert is_counter_as_expected(selenium, Team.objects.count())
        assert is_text_visible(selenium, team_b.name)

        # ------> EDIT A NEW LEAGUE <------ #

        edit_list_instance(selenium, actions, team_a.name, TeamModelSerializer(team_a), {"name": "Fun Team"})
        assert is_string_not_visible(selenium, team_a.name)
        assert is_text_visible(selenium, "Fun Team")
        assert is_counter_as_expected(selenium, Team.objects.count())

        # -----> Delete <----- #

        delete_list_entry(selenium, actions, team_b.name)
        assert is_counter_as_expected(selenium, Team.objects.count())
        assert is_text_visible(selenium, "Fun Team")
        assert is_string_not_visible(selenium, team_b.name)
