import os
from unittest import mock

import responses  # type: ignore

from launchable.utils.http_client import get_base_url
from tests.cli_test_case import CliTestCase


class ModelTest(CliTestCase):
    mock_json = {
        "training_cutoff_test_session_id": 256
    }

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_model(self):
        responses.replace(responses.GET, "{}/intake/organizations/{}/workspaces/{}/model-metadata".format(
            get_base_url(), self.organization, self.workspace), json=self.mock_json, status=200)

        result = self.cli('inspect', 'model', mix_stderr=False)
        expect = """| Metadata                        |   Value |
|---------------------------------|---------|
| Training Cutoff Test Session ID |     256 |
"""

        self.assertEqual(result.stdout, expect)

    @responses.activate
    @mock.patch.dict(os.environ, {"LAUNCHABLE_TOKEN": CliTestCase.launchable_token})
    def test_model_json_format(self):
        responses.replace(responses.GET, "{}/intake/organizations/{}/workspaces/{}/model-metadata".format(
            get_base_url(), self.organization, self.workspace), json=self.mock_json, status=200)

        result = self.cli('inspect', 'model', "--json", mix_stderr=False)

        self.assertEqual(result.stdout, """{
  "training_cutoff_test_session_id": 256
}
"""
                         )
