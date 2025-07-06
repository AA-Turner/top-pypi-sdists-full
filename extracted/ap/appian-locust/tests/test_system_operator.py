import unittest

from locust import TaskSet, Locust
from .mock_client import CustomLocust
from .mock_reader import read_mock_file
from appian_locust import AppianTaskSet

from appian_locust._actions import ACTIONS_INTERFACE_PATH, ACTIONS_FEED_PATH


class TestSystemOperator(unittest.TestCase):

    actions = read_mock_file("actions_response.json")
    actions_interface = read_mock_file("actions_interface.json")
    actions_nav = read_mock_file("actions_nav.json")
    actions_feed = read_mock_file("actions_feed.json")

    action_under_test = "Create a Case::koBOPgHGLIgHRQzrdseY6-wW_trk0FY-87TIog3LDZ9dbSn9dYtlSaOQlWaz7PcZgV5FWdIgYk8QRlv1ARbE4czZL_8fj4ckCLzqA"

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(Locust())
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "auth", ["", ""])
        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.host = ""

        # test_on_start_auth_success is covered here.
        self.custom_locust.set_response(
            "auth?appian_environment=tempo", 200, '{}')
        self.task_set.on_start()

        self.custom_locust.set_response(
            "/suite/api/tempo/open-a-case/available-actions?ids=%5B%5D", 200, self.actions)
        self.custom_locust.set_response(ACTIONS_INTERFACE_PATH, 200, self.actions_interface)
        self.custom_locust.set_response("/suite/rest/a/sites/latest/D6JMim/page/actions/nav", 200, self.actions_nav)
        self.custom_locust.set_response(ACTIONS_FEED_PATH, 200, self.actions_feed)

    def tearDown(self) -> None:
        self.task_set.on_stop()

    def setup_action_response_no_ui(self) -> None:
        action = self.task_set.appian.actions_info.get_action_info("Create a Case", False)
        self.custom_locust.set_response(action['formHref'], 200, "{}")

    def test_actions_start(self) -> None:
        self.setup_action_response_no_ui()
        self.task_set.appian.system_operator.start_action(
            self.action_under_test)
        # TODO: Add assertion

    def test_actions_start_skip_design_call(self) -> None:
        self.task_set.appian.system_operator.start_action(
            self.action_under_test,
            True)
        # TODO: Add assertion

    def test_get_webapi(self) -> None:
        self.custom_locust.set_response(
            "?query=val", 200, '{"query": "result"}')
        output = self.task_set.appian.system_operator.get_webapi(
            "", query_parameters={"query": "val"})
        self.assertEqual('{"query": "result"}', output.text)
