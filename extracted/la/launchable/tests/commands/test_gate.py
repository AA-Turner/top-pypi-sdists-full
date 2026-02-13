import json
import os
from unittest import mock

import responses

from launchable.utils.http_client import get_base_url
from tests.cli_test_case import CliTestCase


class GateTest(CliTestCase):
    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_gate_passed(self):
        """Test gate command exits with 0 when status is PASSED"""
        responses.add(
            responses.GET,
            "{}/intake/organizations/{}/workspaces/{}/gate".format(
                get_base_url(),
                self.organization,
                self.workspace),
            json={
                'status': 'PASSED',
                'quarantinedFailures': 5,
                'actionableFailures': 0
            },
            status=200)

        result = self.cli('gate', '--session', self.session)
        self.assert_success(result)
        self.assertIn('PASSED', result.output)

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_gate_failed(self):
        """Test gate command exits with 1 when status is FAILED"""
        responses.add(
            responses.GET,
            "{}/intake/organizations/{}/workspaces/{}/gate".format(
                get_base_url(),
                self.organization,
                self.workspace),
            json={
                'status': 'FAILED',
                'quarantinedFailures': 2,
                'actionableFailures': 3
            },
            status=200)

        result = self.cli('gate', '--session', self.session)
        self.assert_exit_code(result, 1)
        self.assertIn('FAILED', result.output)

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_gate_passed_json_format(self):
        """Test gate command with --json flag when status is PASSED"""
        gate_data = {
            'status': 'PASSED',
            'quarantinedFailures': 5,
            'actionableFailures': 0
        }

        responses.add(
            responses.GET,
            "{}/intake/organizations/{}/workspaces/{}/gate".format(
                get_base_url(),
                self.organization,
                self.workspace),
            json=gate_data,
            status=200)

        result = self.cli('gate', '--session', self.session, '--json')
        self.assert_success(result)

        # Verify JSON output
        output_json = json.loads(result.output)
        self.assertEqual(output_json['status'], 'PASSED')
        self.assertEqual(output_json['quarantinedFailures'], 5)
        self.assertEqual(output_json['actionableFailures'], 0)

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_gate_failed_json_format(self):
        """Test gate command with --json flag when status is FAILED"""
        gate_data = {
            'status': 'FAILED',
            'quarantinedFailures': 2,
            'actionableFailures': 3
        }

        responses.add(
            responses.GET,
            "{}/intake/organizations/{}/workspaces/{}/gate".format(
                get_base_url(),
                self.organization,
                self.workspace),
            json=gate_data,
            status=200)

        result = self.cli('gate', '--session', self.session, '--json')
        self.assert_exit_code(result, 1)

        # Verify JSON output
        output_json = json.loads(result.output)
        self.assertEqual(output_json['status'], 'FAILED')
        self.assertEqual(output_json['quarantinedFailures'], 2)
        self.assertEqual(output_json['actionableFailures'], 3)

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_gate_not_found(self):
        """Test gate command when gate data is not available"""
        responses.add(
            responses.GET,
            "{}/intake/organizations/{}/workspaces/{}/gate".format(
                get_base_url(),
                self.organization,
                self.workspace),
            json={},
            status=404)

        result = self.cli('gate', '--session', self.session)
        # Should exit with 0 when gate data is not available (non-error case)
        self.assert_success(result)
        self.assertIn('Gate data currently not available', result.output)
