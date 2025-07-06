from locust import TaskSet, Locust
from .mock_client import CustomLocust
from .mock_reader import read_mock_file, read_mock_file_as_dict
from appian_locust import (AppianTaskSet,
                           ComponentNotFoundException,
                           ChoiceNotFoundException,
                           InvalidComponentException)
from appian_locust.uiform import SailUiForm

import os
import unittest
from unittest.mock import patch, MagicMock
from typing import Optional
import json
from requests import Response
from appian_locust._actions import ACTIONS_ALL_PATH, ACTIONS_INTERFACE_PATH, ACTIONS_FEED_PATH, _Actions
from appian_locust._interactor import _Interactor


class TestActions(unittest.TestCase):

    actions = read_mock_file("actions_response.json")
    actions_interface = read_mock_file("actions_interface.json")
    actions_nav = read_mock_file("actions_nav.json")
    actions_feed = read_mock_file("actions_feed.json")

    action_under_test = "Create a Case::koBOPgHGLIgHRQzrdseY6-wW_trk0FY-87TIog3LDZ9dbSn9dYtlSaOQlWaz7PcZgV5FWdIgYk8QRlv1ARbE4czZL_8fj4ckCLzqA"

    def setUp(self) -> None:
        self.interactor: _Interactor = _Interactor("", "ase")
        setup_headers_mock = unittest.mock.Mock(return_value={})
        setattr(self.interactor, 'setup_sail_headers', setup_headers_mock)
        setattr(self.interactor, 'setup_request_headers', setup_headers_mock)
        self.actions_interactor: _Actions = _Actions(self.interactor)

    def test_actions_get_all(self) -> None:
        response_mock = unittest.mock.Mock(return_value=json.loads(self.actions))
        response = Response()
        setattr(response, 'json', response_mock)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, headers, label: response if uri == self.interactor.host + ACTIONS_ALL_PATH else ""
        )
        setattr(self.interactor, 'get_page', get_page_mock)
        all_actions = self.actions_interactor.get_all()
        self.assertTrue(len(list(all_actions.keys())) > 0)

    def test_actions_get(self) -> None:
        response_mock = unittest.mock.Mock(return_value=json.loads(self.actions))
        response = Response()
        setattr(response, 'json', response_mock)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, headers, label: response if uri == self.interactor.host + ACTIONS_ALL_PATH else ""
        )
        setattr(self.interactor, 'get_page', get_page_mock)

        action = self.actions_interactor.get_action(
            self.action_under_test)
        self.assertEqual(action['displayLabel'], 'Create a Case')

    def test_actions_get_corrupt_action(self) -> None:
        corrupt_actions = self.actions.replace('"opaqueId": "koBOPgHGLIgHRQzrdseZ66wChtz5aQqM_RBTDeSBi9lWr4b18XPJqrikBSQYzzp8_e2Wgw0ku-apJjK94StAV1R3DU5zipwSXfCTA"',
                                               '"corrupt_opaqueId": "koBOPgHGLIgHRQzrdseZ66wChtz5aQqM_RBTDeSBi9lWr4b18XPJqrikBSQYzzp8_e2Wgw0ku-apJjK94StAV1R3DU5zipwSXfCTA"')
        response_mock = unittest.mock.Mock(return_value=json.loads(corrupt_actions))
        response = Response()
        setattr(response, 'json', response_mock)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, headers, label: response if uri == self.interactor.host + ACTIONS_ALL_PATH else ""
        )
        setattr(self.interactor, 'get_page', get_page_mock)
        all_actions = self.actions_interactor.get_all()
        self.assertTrue("ERROR::1" in str(all_actions))
        self.assertTrue(self.actions_interactor.get_errors_count() == 1)

    def test_actions_zero_actions(self) -> None:
        corrupt_actions = self.actions.replace('"actions"', '"nonexistent_actions"')
        response_mock = unittest.mock.Mock(return_value=json.loads(corrupt_actions))
        response = Response()
        setattr(response, 'json', response_mock)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, headers, label: response if uri == self.interactor.host + ACTIONS_ALL_PATH else ""
        )
        setattr(self.interactor, 'get_page', get_page_mock)
        all_actions = self.actions_interactor.get_all()
        self.assertTrue(all_actions == {})

    def test_actions_get_partial_match(self) -> None:
        response_mock = unittest.mock.Mock(return_value=json.loads(self.actions))
        response = Response()
        setattr(response, 'json', response_mock)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, headers, label: response if uri == self.interactor.host + ACTIONS_ALL_PATH else ""
        )
        setattr(self.interactor, 'get_page', get_page_mock)
        action = self.actions_interactor.get_action("Create a Case", False)
        self.assertEqual(action['displayLabel'], 'Create a Case')

    def test_actions_get_multiple_matches(self) -> None:
        self.actions_interactor.clear_actions_cache()
        response_mock = unittest.mock.Mock(return_value=json.loads(self.actions))
        response = Response()
        setattr(response, 'json', response_mock)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, headers, label: response if uri == self.interactor.host + ACTIONS_ALL_PATH else ""
        )
        setattr(self.interactor, 'get_page', get_page_mock)
        action = self.actions_interactor.get_action("Create a C", False)
        self.assertTrue("Create a C" in action['displayLabel'])

    def test_actions_get_missing_action(self) -> None:
        response_mock = unittest.mock.Mock(return_value=json.loads(self.actions))
        response = Response()
        setattr(response, 'json', response_mock)
        get_page_mock = unittest.mock.Mock(
            side_effect=lambda uri, headers, label: response if uri == self.interactor.host + ACTIONS_ALL_PATH else ""
        )
        setattr(self.interactor, 'get_page', get_page_mock)
        with self.assertRaisesRegex(Exception, "There is no action with name .* in the system under test.*"):
            self.actions_interactor.get_action("Missing Action", exact_match=True)


if __name__ == '__main__':
    unittest.main()
