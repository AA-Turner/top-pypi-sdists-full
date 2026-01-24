import pytest
from selenium.webdriver.common.action_chains import ActionChains

from wbcore.contrib.authentication.factories import SuperUserFactory
from wbcore.contrib.authentication.models import User
from wbcore.contrib.example_app.models import SportPerson
from wbcore.contrib.example_app.serializers import SportPersonModelSerializer
from wbcore.contrib.example_app.tests.e2e import create_new_person_instance
from wbcore.test import (
    click_element_by_path,
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
class TestPerson:
    def test_create_edit_delete_person(self, live_server, selenium):
        # Creating a test user and login to the WB
        user: User = SuperUserFactory.create(plaintext_password=USER_PASSWORD)
        actions = ActionChains(selenium, 1000)
        set_up(selenium, live_server, user.email, USER_PASSWORD)

        # -----> CREATE A NEW PERSON <----- #
        person_a = create_new_person_instance(selenium, ["first_name", "last_name"], False)
        open_menu_item(selenium, "Persons")
        # TODO find a solution how to handle the case, that a navigation element has the same name as a subelement.
        click_element_by_path(selenium, '//div[@title="Persons"]')
        click_element_by_path(selenium, '//span[@title="Create Person"]//parent::div//div')

        window_width = (selenium.get_window_size().get("width")) / 1.75
        actions.move_by_offset(window_width, 0).perform()
        actions.click()

        assert is_counter_as_expected(selenium, SportPerson.objects.count())
        assert is_text_visible(selenium, person_a.last_name)

        click_new_button(selenium)
        assert is_text_visible(selenium, "Create Person")
        person_b = create_new_person_instance(selenium, ["first_name", "last_name"])

        assert is_counter_as_expected(selenium, SportPerson.objects.count())
        assert is_text_visible(selenium, person_b.last_name)

        # ------> EDIT A NEW PERSON <------ #

        edit_list_instance(
            selenium, actions, person_a.last_name, SportPersonModelSerializer(person_a), {"last_name": "Foobar"}
        )
        assert is_string_not_visible(selenium, person_a.last_name)
        assert is_text_visible(selenium, "Foobar")
        assert is_counter_as_expected(selenium, SportPerson.objects.count())

        # -----> Delete <----- #

        delete_list_entry(selenium, actions, person_b.last_name)
        assert is_counter_as_expected(selenium, SportPerson.objects.count())
        assert is_text_visible(selenium, "Foobar")
        assert is_string_not_visible(selenium, person_b.last_name)
