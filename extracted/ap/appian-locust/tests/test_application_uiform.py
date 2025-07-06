import unittest
import json

from locust import TaskSet, Locust
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust import AppianTaskSet
from appian_locust.exceptions import IncorrectDesignAccessException
from appian_locust.uiform import DesignObjectUiForm

RDO_HOST = "https://ai-skill-server.net"


class TestApplicationUiform(unittest.TestCase):
    ai_skill_design_object_response = read_mock_file("ai_skill_design_object_response.json")

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(Locust())
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "auth", ["", ""])
        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.host = ""

        # test_on_start_auth_success is covered here.
        self.custom_locust.set_response("auth?appian_environment=tempo", 200, '{}')
        self.task_set.on_start()

    def tearDown(self) -> None:
        self.task_set.on_stop()

    def test_click_design_object(self) -> None:
        app_landing_page = read_mock_file("design_app_landing_page.json")
        self.custom_locust.set_response("/suite/rest/a/applications/latest/app/design/app/yh4Z0_7aQfhi2FgIUOqaca_4Vlp", 200, app_landing_page)
        application = self.task_set.appian.visitor.visit_application_by_id("yh4Z0_7aQfhi2FgIUOqaca_4Vlp")
        result_state = '{"ase": "ase"}'
        self.custom_locust.set_response(
            "/suite/rest/a/applications/latest/app/design/lIBKSzmcS2f-JBIoXdpEpcXkuLVVXxoykWGSNEqB-oPAfjLayGXYe7CkjVo53babGjVtBl2x-96-oRsUrFC3i3bZm3cF0kG7wwaG-9H6213zpNl", 200, result_state)
        design_object = application.click_design_object("RE_stockData")
        self.assertEqual(type(design_object), DesignObjectUiForm)
        self.assertEqual(design_object.get_latest_state(), json.loads(result_state))

    def test_click_design_object_throws_ai_skill_exception(self) -> None:
        app_landing_page = read_mock_file("design_app_landing_page.json")
        self.custom_locust.set_response("/suite/rest/a/applications/latest/app/design/app/yh4Z0_7aQfhi2FgIUOqaca_4Vlp", 200, app_landing_page)
        application = self.task_set.appian.visitor.visit_application_by_id("yh4Z0_7aQfhi2FgIUOqaca_4Vlp")
        self.custom_locust.set_response(
            "/suite/rest/a/applications/latest/app/design/lIBKSzmcS2f-JBIoXdpEpcXkuLVVXxoykWGSNEqB-oPAfjLayGXYe7CkjVo53babGjVtBl2x-96-oRsUrFC3i3bZm3cF0kG7wwaG-9H6213zpNl",
            200,
            self.ai_skill_design_object_response
        )
        with self.assertRaises(IncorrectDesignAccessException) as context:
            application.click_design_object("RE_stockData")
        self.assertEqual(
            context.exception.args[0],
            "Selected Design Object was of type aiSkill, use click_ai_skill method instead")

    def test_click_ai_skill_object(self) -> None:
        bff_token_response = read_mock_file("bff_token_response.json")
        app_landing_page = read_mock_file("design_app_landing_page.json")

        # Setup RDO Interaction
        self.custom_locust.set_response("/suite/rfx/bff-token", 200, bff_token_response)
        self.custom_locust.set_response(f"{RDO_HOST}/rdo-server/DesignObjects/InterfaceAuthentication/v1", 200, "{}")

        self.custom_locust.set_response("/suite/rest/a/applications/latest/app/design/app/yh4Z0_7aQfhi2FgIUOqaca_4Vlp", 200, app_landing_page)
        application = self.task_set.appian.visitor.visit_application_by_id("yh4Z0_7aQfhi2FgIUOqaca_4Vlp")
        self.custom_locust.set_response(
            "/suite/rest/a/applications/latest/app/design/lIBKSzmcS2f-JBIoXdpEpcXkuLVVXxoykWGSNEqB-oPAfjLayGXYe7CkjVo53babGjVtBl2x-96-oRsUrFC3i3bZm3cF0kG7wwaG-9H6213zpNl",
            200,
            self.ai_skill_design_object_response
        )
        self.custom_locust.set_response(f"{RDO_HOST}/sail-server/SYSTEM_SYSRULES_aiSkillDesigner/ui", 200, "{\"this_is\": \"a_response\"}")

        ai_skill = application.click_ai_skill("RE_stockData")
        self.assertEqual(ai_skill.get_latest_state(), {"this_is": "a_response"})
