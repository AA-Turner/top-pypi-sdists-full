import os
from unittest import mock

import responses  # type: ignore

from launchable.utils.session import write_build
from tests.cli_test_case import CliTestCase


class JasmineTest(CliTestCase):
    @responses.activate
    @mock.patch.dict(os.environ,
                     {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_record_tests_json(self):
        result = self.cli('record', 'tests', '--session', self.session,
                          'jasmine', str(self.test_files_dir.joinpath("jasmine-test-results.json")))

        self.assert_success(result)
        self.assert_record_tests_payload('record_test_result.json')

    @responses.activate
    @mock.patch.dict(os.environ,
                     {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_record_tests_without_filename(self):
        result = self.cli('record', 'tests', '--session', self.session,
                          'jasmine', str(self.test_files_dir.joinpath("jasmine-test-results-v3.99.0.json")))

        self.assertIn(
            "does not appear to be valid format. "
            "Make sure you are using Jasmine >= v4.6.0 and jasmine-json-test-reporter as the reporter.",
            result.output
        )

    @responses.activate
    @mock.patch.dict(os.environ,
                     {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_subset(self):
        write_build(self.build_name)

        subset_input = """spec/jasmine_examples/PlayerSpec.js
spec/jasmine_examples/UserSpec.js
"""
        result = self.cli('subset', '--target', '10%', 'jasmine', input=subset_input)
        self.assert_success(result)
        self.assert_subset_payload('subset_payload.json')
