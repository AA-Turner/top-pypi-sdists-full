import json
import os
import unittest
from unittest.mock import Mock
from typing import Optional

from appian_locust import AppianClient, AppianTaskSet
from appian_locust.utilities.helper import find_component_by_attribute_in_dict
from appian_locust.utilities import logger
from locust import Locust, TaskSet
from appian_locust._save_request_builder import save_builder

from .mock_client import CustomLocust, SampleAppianTaskSequence
from .mock_reader import read_mock_file

log = logger.getLogger(__name__)


class TestSaveRequestBuilder(unittest.TestCase):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    record_action_launch_form_before_refresh = read_mock_file("record_action_launch_form_before_refresh.json")
    record_action_component_payload_json = read_mock_file("record_action_component_payload.json")
    record_action_trigger_payload_json = read_mock_file("record_action_trigger_payload.json")
    default_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    mobile_user_agent = "AppianAndroid/24.4 (Google AOSP on IA Emulator, 9; Build 0-SNAPSHOT; AppianPhone)"

    def setUpWithPath(self, base_path_override: Optional[str] = None) -> None:
        self.custom_locust = CustomLocust(Locust())
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "credentials", [["", ""]])
        setattr(parent_task_set, "auth", ["", ""])
        if base_path_override:
            setattr(parent_task_set, "base_path_override", base_path_override)

        self.task_set = AppianTaskSet(parent_task_set)

        self.task_set.on_start()

    def setUp(self) -> None:
        self.setUpWithPath()

    def test_record_action_refresh_builder(self) -> None:
        # Test the interaction with _save_builder used by _interactor.refresh_after_record_action
        record_action_component = find_component_by_attribute_in_dict("label", "Update Table 1 (Dup) (PSF)",
                                                                      json.loads(
                                                                          self.record_action_launch_form_before_refresh
                                                                      ))
        record_action_trigger_component = find_component_by_attribute_in_dict(
            "_actionName",
            "sail:record-action-trigger",
            json.loads(
                self.record_action_launch_form_before_refresh
            ))
        context = find_component_by_attribute_in_dict("type", "stateful",
                                                      json.loads(
                                                          self.record_action_launch_form_before_refresh
                                                      ))
        uuid = "345f89d4-b2b4-4c8c-a2a3-2b578e6292df"

        # Get the payload for the record action on submit
        record_action_payload = save_builder() \
            .component(record_action_component) \
            .context(context) \
            .uuid(uuid) \
            .value(dict()) \
            .build()

        # Get the payload for the record action trigger
        record_action_trigger_payload = save_builder() \
            .component(record_action_trigger_component) \
            .context(context) \
            .uuid(uuid) \
            .value(dict()) \
            .build()

        self.assertEqual(record_action_payload, json.loads(self.record_action_component_payload_json))
        self.assertEqual(record_action_trigger_payload, json.loads(self.record_action_trigger_payload_json))
