import json
import os
import tempfile
from pathlib import Path
from unittest import mock

import responses  # type: ignore

from launchable.utils.http_client import get_base_url
from tests.cli_test_case import CliTestCase


class CodeceptjsTest(CliTestCase):
    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_record_test_codeceptjs(self):
        result = self.cli(
            "record",
            "tests",
            "--session",
            self.session,
            "codeceptjs",
            str(self.test_files_dir.joinpath("codeceptjs-result.xml")),
        )

        self.assert_success(result)
        self.assert_record_tests_payload("record_test_result.json")

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_subset(self):
        """Test basic subset functionality with multiple test files"""
        pipe = "test/example_test.js\ntest/login_test.js\n"

        # Mock the subset API response to return test paths
        mock_response = {
            "testPaths": [
                [{"type": "file", "name": "test/example_test.js"}],
                [{"type": "file", "name": "test/login_test.js"}],
            ],
            "rest": [],
            "subsettingId": 456,
        }

        responses.replace(
            responses.POST,
            "{}/intake/organizations/{}/workspaces/{}/subset".format(
                get_base_url(), self.organization, self.workspace
            ),
            json=mock_response,
            status=200,
        )

        result = self.cli(
            "subset",
            "--target",
            "10%",
            "--session",
            self.session,
            "codeceptjs",
            input=pipe,
        )
        self.assert_success(result)

        # Verify the output is valid JSON
        output = result.output.strip()
        output_json = json.loads(output)
        self.assertEqual(
            output_json["tests"], ["test/example_test.js", "test/login_test.js"]
        )

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_subset_with_rest(self):
        """Test subset functionality with --rest option to save remaining tests"""
        pipe = "test/example_test.js\ntest/other_test.js\n"

        # Mock the subset API response with both testPaths and rest
        mock_response = {
            "testPaths": [
                [{"type": "file", "name": "test/example_test.js"}],
            ],
            "rest": [
                [{"type": "file", "name": "test/other_test.js"}],
            ],
            "subsettingId": 456,
        }

        responses.replace(
            responses.POST,
            "{}/intake/organizations/{}/workspaces/{}/subset".format(
                get_base_url(), self.organization, self.workspace
            ),
            json=mock_response,
            status=200,
        )

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".json"
        ) as rest_file:
            rest_file_path = rest_file.name

        try:
            result = self.cli(
                "subset",
                "--target",
                "50%",
                "--session",
                self.session,
                "--rest",
                rest_file_path,
                "codeceptjs",
                input=pipe,
            )
            self.assert_success(result)

            # Verify the output is valid JSON with "tests" key
            output = result.output.strip()
            output_json = json.loads(output)
            self.assertEqual(output_json["tests"], ["test/example_test.js"])

            # Verify rest file was created and contains valid JSON
            self.assertTrue(
                Path(rest_file_path).exists(), "Rest file should be created"
            )
            with open(rest_file_path, "r") as f:
                rest_json = json.load(f)
                self.assertEqual(rest_json["tests"], ["test/other_test.js"])
        finally:
            # Cleanup
            if Path(rest_file_path).exists():
                Path(rest_file_path).unlink()

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_subset_with_single_test(self):
        """Test subset functionality with a single test file"""
        pipe = "test/single_test.js\n"

        # Mock the subset API response
        mock_response = {
            "testPaths": [
                [{"type": "file", "name": "test/single_test.js"}],
            ],
            "rest": [],
            "subsettingId": 456,
        }

        responses.replace(
            responses.POST,
            "{}/intake/organizations/{}/workspaces/{}/subset".format(
                get_base_url(), self.organization, self.workspace
            ),
            json=mock_response,
            status=200,
        )

        result = self.cli(
            "subset",
            "--target",
            "10%",
            "--session",
            self.session,
            "codeceptjs",
            input=pipe,
        )
        self.assert_success(result)

        # Verify the output is valid JSON
        output = result.output.strip()
        output_json = json.loads(output)
        self.assertEqual(output_json["tests"], ["test/single_test.js"])

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_subset_strips_newlines(self):
        """Test that subset properly strips newlines from test paths"""
        # Test with various newline formats
        pipe = "test/example_test.js\n\ntest/login_test.js\r\ntest/signup_test.js\n"

        # Mock the subset API response
        mock_response = {
            "testPaths": [
                [{"type": "file", "name": "test/example_test.js"}],
                [{"type": "file", "name": "test/login_test.js"}],
                [{"type": "file", "name": "test/signup_test.js"}],
            ],
            "rest": [],
            "subsettingId": 456,
        }

        responses.replace(
            responses.POST,
            "{}/intake/organizations/{}/workspaces/{}/subset".format(
                get_base_url(), self.organization, self.workspace
            ),
            json=mock_response,
            status=200,
        )

        result = self.cli(
            "subset",
            "--target",
            "10%",
            "--session",
            self.session,
            "codeceptjs",
            input=pipe,
        )
        self.assert_success(result)

        # Verify the output is valid JSON
        output = result.output.strip()
        output_json = json.loads(output)
        self.assertEqual(
            output_json["tests"],
            ["test/example_test.js", "test/login_test.js", "test/signup_test.js"],
        )
