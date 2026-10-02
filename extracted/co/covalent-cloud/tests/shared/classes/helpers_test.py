# Copyright 2023 Agnostiq Inc.

import responses

from covalent_cloud.shared.classes.exceptions import CovalentSDKError
from covalent_cloud.shared.classes.helpers import check_env_is_ready
from covalent_cloud.shared.classes.settings import Settings


class TestHelpersShould:
    @responses.activate
    def test_check_env_is_ready_returns_true_when_ready(self):
        settings = Settings()
        settings.dispatcher_uri = "https://api.test.covalent.xyz"
        responses.add(
            responses.GET,
            "https://api.test.covalent.xyz/api/v2/envs?name=env_name",
            status=200,
            json={"records": [{"status": "READY"}]},
        )

        env_is_ready, env_response = check_env_is_ready("env_name", settings)

        assert env_is_ready == True  # noqa: E712

    @responses.activate
    def test_check_env_is_ready_throws_exception_when_dne(self):
        settings = Settings()
        settings.dispatcher_uri = "https://api.test.covalent.xyz"
        responses.add(
            responses.GET,
            "https://api.test.covalent.xyz/api/v2/envs?name=env_name",
            status=200,
            json={"records": []},
        )
        try:
            env_is_ready, env_response = check_env_is_ready("env_name", settings)
        except CovalentSDKError as e:
            assert 'Environment "env_name" does not exist.' in str(e)

    @responses.activate
    def test_check_env_is_ready_throws_exception_when_not_ready(self):
        settings = Settings()
        settings.dispatcher_uri = "https://api.test.covalent.xyz"
        responses.add(
            responses.GET,
            "https://api.test.covalent.xyz/api/v2/envs?name=env_name",
            status=200,
            json={"records": [{"status": "CREATING"}]},
        )
        try:
            env_is_ready, env_response = check_env_is_ready("env_name", settings)
        except CovalentSDKError as e:
            assert 'Environment "env_name" is not ready.' in str(e)
